import datetime

from pydantic.fields import Field

from pydantic_db_backend.backend import BackendModel
from pydantic_db_backend.utils import utcnow


class EventModel(BackendModel):
    payload: dict | None = Field(default_factory=dict)
    schedule_time: datetime.datetime | None = Field(default_factory=utcnow)
    unique_key: str | None = None
    priority: int | None = 0


