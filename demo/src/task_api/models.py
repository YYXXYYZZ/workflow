from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Status(str, Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CreateTaskRequest(StrictModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=1000)
    status: Status = Status.TODO

    @field_validator("title", "description", mode="before")
    @classmethod
    def trim_text(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value


class UpdateStatusRequest(StrictModel):
    status: Status


class TaskResponse(StrictModel):
    id: UUID
    title: str
    description: str
    status: Status
    created_at: datetime
    updated_at: datetime


class ErrorBody(StrictModel):
    code: str
    message: str = Field(min_length=1)


class ErrorResponse(StrictModel):
    error: ErrorBody
