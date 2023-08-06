from __future__ import annotations

import importlib
import logging
import os
import sys
import time
from typing import List, Dict

import dotenv
import requests.exceptions
from pydantic_db_backend.utils import utcnow

from eventix.contexts import worker_id_context, namespace_provider
from eventix.exceptions import TaskNotRegistered, backend_exceptions
from eventix.functions.core import EventixTaskBase, namespace_context
from eventix.functions.errors import raise_errors
from eventix.functions.eventix_client import EventixClient
from eventix.functions.schedule import schedule_set_next_schedule
from eventix.functions.task import task_set_error, task_set_result
from eventix.functions.tools import setup_logging
from eventix.pydantic.schedule import Schedule
from eventix.pydantic.task import TaskModel

log = logging.getLogger(__name__)


class TaskWorker(EventixClient):
    _wait_interval = 10
    _tasks = {}
    _schedule: Dict[str, Schedule] = {}

    namespace: str = None
    schedule_enabled: bool = False
    log_level: str = None

    @classmethod
    def config(cls, config: dict):

        base_url = os.environ.get("EVENTIX_URL", "")
        if base_url == "":
            log.error("No EVENTIX_URL set.")
            sys.exit()

        cls.set_base_url(base_url)

        cls.config_register_tasks(config)

        if "namespace" in config:
            cls.namespace = config['namespace']

        namespace = os.environ.get("EVENTIX_NAMESPACE", "")
        if namespace != "":
            cls.namespace = namespace

        schedule_enabled = os.environ.get("EVENTIX_SCHEDULE_ENABLED", "false")
        cls.schedule_enabled = schedule_enabled.lower() == "true"

        cls.config_schedule(config)

    @classmethod
    def config_register_tasks(cls, config):
        if "register_tasks" in config:
            cls.register_tasks(config['register_tasks'])

    @classmethod
    def config_schedule(cls, config):
        if "schedule" in config:
            for entry in config['schedule']:
                s = Schedule.parse_obj(entry)
                if s.task not in cls._tasks:
                    raise TaskNotRegistered(s.task)

                schedule_set_next_schedule(s)
                cls._schedule[s.uid] = s
                log.info(f"Scheduled '{s.name}' on '{s.schedule}'")

    @classmethod
    def check_scheduled_tasks(cls):
        log.debug(f"Check scheduled tasks...")
        for s in cls._schedule.values():
            if s.next_schedule <= utcnow():
                # trigger task
                # update schedule
                log.debug(f"triggering scheduled task '{s.name}'")
                cls._tasks[s.task].delay(*s.args, _priority=s.priority, **s.kwargs)
                schedule_set_next_schedule(s)

    @classmethod
    def register_tasks(cls, paths=List[str]):
        log.info("registering tasks...")
        # noinspection PyTypeChecker
        for path in paths:
            try:
                imported_module = importlib.import_module(path)
                for f in filter(
                    lambda x: isinstance(x, EventixTaskBase),
                    [getattr(imported_module, x) for x in dir(imported_module)]
                ):
                    log.info(f"registered '{f.func_name}' from {path}")
                    cls._tasks[f.func_name] = f
            except ImportError as e:
                print(e)

    # with raise_errors(r):
    #     return TaskModel.parse_raw(r.content)

    @classmethod
    def task_next_scheduled(cls) -> TaskModel | None:
        with namespace_context() as namespace:
            with worker_id_context() as worker_id:
                params = dict(
                    worker_id=worker_id,
                    namespace=namespace
                )
                r = cls.interface.get(f'/tasks/next_scheduled', params=params)
                try:
                    with raise_errors(r, backend_exceptions):
                        if r.status_code == 200:
                            tm = TaskModel.parse_raw(r.content)
                            return tm
                        if r.status_code == 204:
                            return None
                except Exception as e:
                    log.error("Upstream server error:")
                    log.exception(str(e))
                    return None
    @classmethod
    def listen(cls, endless=True, schedule_enabled: bool = False):
        log.info(f"Schedule {'enabled' if schedule_enabled else 'disabled'}")
        log.info("Start listening...")
        while True:
            try:
                if schedule_enabled:
                    cls.check_scheduled_tasks()
                log.debug("Looking for tasks...")
                t = cls.task_next_scheduled()
                if t is not None:
                    cls.execute_task(t)
                else:
                    log.info(f"Nothing to do... waiting {cls._wait_interval}s")
                    if not endless:
                        return
                    time.sleep(cls._wait_interval)
            except requests.exceptions.ConnectionError as e:
                log.error(f"Upstream Eventix server {cls.interface.base_url} not reachable.")
                time.sleep(5)

    @classmethod
    def execute_task(cls, task: TaskModel):
        try:
            log.info(f"Executing task: {task.task} uid: {task.uid} ...")

            if task.task not in cls._tasks:
                raise TaskNotRegistered(task=task.task)  # Task not registered in worker

            f = cls._tasks[task.task]
            r = f.run(*task.args, **task.kwargs)
            task_set_result(task, r)

        except TaskNotRegistered as e:
            log.exception(e)
            task_set_error(
                task,
                TaskNotRegistered(task=task.task)
            )

        except Exception as e:
            log.exception(e)
            task_set_error(task, e)

        finally:
            cls.task_write_back(task)

    @classmethod
    def task_write_back(cls, task: TaskModel) -> TaskModel | None:
        try:

            if task.expires is not None and task.expires < utcnow():  # gammel
                # if task is already expired, delete it instead of updating
                r = cls.interface.delete(f'/task/{task.uid}')
                return None
            else:
                # task not yet expired.... update
                r = cls.interface.put(f'/task/{task.uid}', data=task.json())

            with raise_errors(r, backend_exceptions):
                if r.status_code == 200:
                    tm = TaskModel.parse_raw(r.content)
                    return tm

        except Exception as e:
            log.error("Exception raised when calling eventix")
            log.exception(e)
            log.error("Exception used this task info")
            log.error(task.json())

        return None

    @classmethod
    def load_env(cls):
        dotenv.load_dotenv(".env.local")

    def __init__(self, config: dict) -> None:
        self.load_env()
        self.init_logging()
        self.config(config)

    def init_logging(self):
        self.log_level = os.environ.get("EVENTIX_WORKER_LOG_LEVEL", "INFO")
        urllib3_logger = logging.getLogger("urllib3.connectionpool")
        urllib3_logger.setLevel(logging.INFO)
        setup_logging(level=self.log_level.upper(), module=False, prefix="[WORKER]")

    def start(self, endless: bool | None = True):
        log.info(f"Using namespace: {self.namespace}")
        with namespace_provider(self.namespace):
            self.listen(endless, self.schedule_enabled)
