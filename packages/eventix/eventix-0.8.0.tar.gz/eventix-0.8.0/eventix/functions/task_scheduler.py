import logging

from eventix.contexts import namespace_context
from eventix.exceptions import backend_exceptions
from eventix.functions.errors import raise_errors
from eventix.functions.eventix_client import EventixClient
from eventix.pydantic.task import TaskModel

log = logging.getLogger(__name__)


class TaskScheduler(EventixClient):

    @classmethod
    def schedule(cls, task: TaskModel) -> TaskModel:
        if task.namespace is None:
            with namespace_context() as namespace:
                task.namespace = namespace
        log.debug(f"scheduling task: {task.task} namespace: {task.namespace} uid: {task.uid} eta: {task.eta} unique_key: {task.unique_key}")
        return cls.task_post(task)

    @classmethod
    def task_get(cls, uid: str) -> TaskModel:
        r = cls.interface.get(f'/task/{uid}')
        with raise_errors(r, backend_exceptions):
            return TaskModel.parse_raw(r.content)

    @classmethod
    def task_post(cls, task: TaskModel) -> TaskModel:
        r = cls.interface.post('/task', data=task.json())
        with raise_errors(r, backend_exceptions):
            return TaskModel.parse_raw(r.content)
