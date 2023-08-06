import datetime
from traceback import format_tb
from typing import List, Any, Tuple

from webexception.webexception import WebException

from eventix.pydantic.pagination import PaginationParametersModel
from eventix.pydantic.task import TaskModel, task_model_status
from pydantic_db_backend.backend import Backend
from pydantic_db_backend.exceptions import RevisionConflict

# post
# already exists
# still scheduled -> update

# not scheduled --> post new.
# scheduled -> update
#
#   update:
#       get task
#       scheck scheduled, if not post
#       update task
#
#       if worker grabs , version should conflict
#       if conflict: try again


import logging

from pydantic_db_backend.utils import utcnow

log = logging.getLogger(__name__)


def task_post(task: TaskModel) -> TaskModel:
    is_unique = task.unique_key is not None

    if not is_unique:
        # not unique , just try to save. If exists, raise error
        # noinspection PyTypeChecker
        return Backend.post_instance(task)

    # has unique_key

    while True:

        # noinspection PyTypeChecker
        existing_tasks: List[TaskModel] = Backend.get_instances(TaskModel, 0, 10, {"unique_key": task.unique_key})
        next_scheduled_task = next(filter(lambda t: t.status == "scheduled", existing_tasks), None)

        if next_scheduled_task is None:
            # no existing ones that are only scheduled, we have to post
            # noinspection PyTypeChecker
            return Backend.post_instance(task)

        #   update:
        #       get task
        #       scheck scheduled, if not post
        #       update task
        #
        #       if worker grabs , version should conflict
        #       if conflict: try again

        next_scheduled_task.unique_update_from(task)
        try:
            updated_task = Backend.put_instance(next_scheduled_task)
            # noinspection PyTypeChecker
            log.debug(f"updated task {updated_task.uid}")
            # noinspection PyTypeChecker
            return updated_task  # update worked
        except RevisionConflict as e:
            continue  # try again.


def task_clean_expired_workers():
    params = dict(
        model=TaskModel,
        skip=0,
        limit=1,
        query_filter=dict(
            worker_expires={
                "$and": [
                    {"$ne": None},
                    {"$lt": utcnow()},
                ]
            }  # no worker assigned
        ),
        sort=[
            {"priority": "asc"},
            {"eta": "asc"}
        ]
    )

    while True:
        # noinspection PyTypeChecker
        existing_task: TaskModel | None = next(iter(Backend.get_instances(**params)), None)

        # repeat until we were able to take something or nothing is left.
        if existing_task is None:
            break

        existing_task.status = "scheduled"
        existing_task.worker_id = None
        existing_task.worker_expires = None

        try:
            Backend.put_instance(existing_task)
            log.info(f"Released task {existing_task.uid}")
            # noinspection PyTypeChecker
        except RevisionConflict as e:
            continue


def task_clean_expired_tasks():
    params = dict(
        model=TaskModel,
        skip=0,
        limit=100,
        query_filter=dict(
            expires={
                "$and": [
                    {"$ne": None},
                    {"$lt": utcnow()},
                ]
            }  # task expired
        ),
        # sort=[
        #     {"priority": "asc"},
        #     {"eta": "asc"}
        # ]
    )

    while True:
        # noinspection PyTypeChecker
        existing_uids = Backend.get_uids(**params)

        # repeat until we were able to take something or nothing is left.
        if len(existing_uids) == 0:
            break

        for uid in existing_uids:
            Backend.delete_uid(TaskModel, uid)
            log.info(f"Removed expired task {uid}")


def task_next_scheduled(worker_id: str, namespace: str, expires: int = 300) -> TaskModel | None:
    log.debug(f"[{worker_id}] Worker getting next scheduled task...")

    # looking up possible tasks in right order
    # take first one
    # try to set worker_id and expiration

    eta = utcnow().isoformat()  # eta has to be now or in the past

    query_filter = dict(
        namespace=namespace,  # namespace has to match
        worker_id=None,  # no worker assigned
        status={"$in": ["scheduled", "retry"]},
        eta={"$lte": eta}
    )
    sort = [
        {"priority": "asc"},
        {"eta": "asc"}
    ]

    while True:  # repeat until we were able to take something or nothing is left.

        # noinspection PyTypeChecker
        existing_task: TaskModel | None = next(iter(Backend.get_instances(
            TaskModel,
            0,
            1,
            query_filter=query_filter,
            sort=sort
        )), None)

        if existing_task is None:
            return None  # no task left

        existing_task.status = "processing"
        existing_task.worker_id = worker_id
        existing_task.worker_expires = utcnow() + datetime.timedelta(seconds=expires)

        try:
            # noinspection PyTypeChecker
            t: TaskModel = Backend.put_instance(existing_task)
            return t
        except RevisionConflict as e:
            continue


def task_set_error(task: TaskModel, error: Any):
    if isinstance(error, WebException):
        task.result = error.dict()
    elif isinstance(error, Exception):
        task.result = dict(
            error_class=error.__class__.__name__,
            error_message=str(error),
            error_status_code=500,
            error_traceback=format_tb(error.__traceback__),
            error_payload={}
        )
    else:
        task.result = error

    if task.retry and (task.max_retries is None or task.max_retries != 0):
        task.status = "retry"
        if task.max_retries is not None:
            task.max_retries -= 1  # decrease max_retries until it reaches zero.

        task.eta = utcnow() + datetime.timedelta(seconds=task.error_eta_inc)
        task.error_eta_inc = min([task.error_eta_inc * 2, task.error_eta_max])

        task.worker_id = None

    else:
        task.status = "error"
        if task.error_expires is not None:
            task.expires = utcnow() + datetime.timedelta(seconds=task.error_expires)

    task.worker_expires = None  # removes worker_expires for cleanup prevention


def task_set_result(task: TaskModel, result: Any):
    task.status = "done"
    if task.store_result:
        task.result = result
        if task.result_expires is not None:
            task.expires = utcnow() + datetime.timedelta(seconds=task.result_expires)
    else:
        task.expires = utcnow()

    task.worker_expires = None  # removes worker_expires for cleanup prevention


def tasks_by_status(
    status: task_model_status | None = None,
    namespace: str | None = None,
    pagination: PaginationParametersModel | None = None
) -> Tuple[List[TaskModel], int]:
    query_filter = {}
    if status is not None:
        query_filter["status"] = {"$eq": status}
    if namespace is not None:
        query_filter["namespace"] = {"$eq": namespace}
    params = {
        "query_filter": query_filter,
        **pagination.dict(),
    }
    # noinspection PyTypeChecker
    tasks, max_results = Backend.get_instances(TaskModel, **params, max_results=True)
    tasks: List[TaskModel]
    return tasks, max_results
