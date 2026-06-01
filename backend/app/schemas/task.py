from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    task_date: date
    due_time: Optional[time] = None

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("title must not be empty")
        return stripped


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    due_time: Optional[time] = None
    is_done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        stripped = value.strip()
        if not stripped:
            raise ValueError("title must not be empty")
        return stripped


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    task_date: date
    due_time: Optional[time]
    is_done: bool
    created_at: datetime
