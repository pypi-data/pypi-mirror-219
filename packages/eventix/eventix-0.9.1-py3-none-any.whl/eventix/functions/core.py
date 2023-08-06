import functools
import functools
import logging
from inspect import signature
from typing import Callable, Dict, Any

from pydantic import BaseModel

from eventix.contexts import namespace_context, delay_tasks_context
from eventix.functions.task_scheduler import TaskScheduler
from eventix.pydantic.task import TaskModel

log = logging.getLogger(__name__)


class EventixTaskBase(object):
    pass


def task(store_result: bool = True, unique_key_generator: Callable = None, retry: bool = True, max_retries: int | None = None, error_expires: int | None = None, result_expires: int | None = 604800):
    # parameters suggested:
    #
    # store_result: bool , wether to store or not to store results
    # unique_uid: ....  having a unique id, which leads to update the task if it is rescheduled.

    # retry: bool, wether to retry failed tasks
    # max_retry: int, maximum retries default 5 ... each retry doubles the time to wait, starting with 30 sec

    is_unique = unique_key_generator is not None

    def inner(f):
        class EventixTask(EventixTaskBase):
            def __init__(self):
                self.func = f
                self.func_name = f.__name__
                self.arg_spec = list(signature(f).parameters.values())
                self.arg_spec_args = [arg.annotation for arg in self.arg_spec]
                self.arg_spec_kwargs = {arg.name: arg.annotation for arg in self.arg_spec}
                assert True

            def restore_pydantic_instances(self, args, kwargs) -> tuple[list[Any], Dict[str, Any]]:
                new_args = []
                for i, arg in enumerate(args):
                    if isinstance(arg, dict):
                        cls = self.arg_spec_args[i]
                        if issubclass(cls, BaseModel):
                            arg = cls.parse_obj(arg)
                    new_args.append(arg)
                new_kwargs = {}
                for kw, arg in kwargs.items():
                    if isinstance(arg, dict):
                        cls = self.arg_spec_kwargs[kw]
                        if issubclass(cls, BaseModel):
                            arg = cls.parse_obj(arg)
                    new_kwargs[kw] = arg
                return new_args, new_kwargs

            @functools.wraps(f)
            def delay(self, *args, _priority: int | None = 0, **kwargs) -> TaskModel:
                # priority has to be negated, needed for fixing ascending sort order
                tm = self.make_task_model(args, kwargs, priority=_priority * -1)
                with delay_tasks_context() as delay:
                    if delay:
                        tm = TaskScheduler.schedule(tm)
                    else:
                        self.run(*args, **kwargs)

                # IDEA: It could be possible to run worker execute with generated task during tests
                return tm

            @functools.wraps(f)
            def run(self, *args, **kwargs):
                args, kwargs = self.restore_pydantic_instances(args, kwargs)
                return self.func(*args, **kwargs)

            def make_task_model(self, args, kwargs, priority) -> TaskModel:
                with namespace_context() as namespace:
                    params = dict(
                        task=self.func_name,
                        args=args,
                        kwargs=kwargs,
                        priority=priority,
                        store_result=store_result,
                        retry=retry,
                        max_retries=max_retries,
                        error_expires=error_expires,
                        result_expires=result_expires,
                        namespace=kwargs['namespace'] if "namespace" in kwargs else namespace
                    )

                    if is_unique:
                        unique_key = unique_key_generator(*args, **kwargs)
                        params |= dict(unique_key=unique_key)

                return TaskModel.parse_obj(params)

        return EventixTask()

    return inner
