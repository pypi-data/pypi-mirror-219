from pydantic_db_backend.exceptions import AlreadyExists, NotFound, RevisionConflict
from webexception.webexception import WebException


class TaskNotUnique(WebException):
    status_code = 409

    def __init__(self, uid: str) -> None:
        super().__init__(
            f"Task with uid '{uid}' already exists and task unique is not activated for overwriting.",
            uid=uid
        )


class NoTaskFound(WebException):
    status_code = 204

    def __init__(self, namespace: str) -> None:
        super().__init__(
            f"No task for namespace {namespace}",
            namespace=namespace
        )


class TaskNotRegistered(WebException):
    status_code = 404

    def __init__(self, task: str) -> None:
        super().__init__(
            f"Task '{task}' not registered.",
            task=task
        )



backend_exceptions = [
    AlreadyExists,
    NotFound,
    RevisionConflict
]

