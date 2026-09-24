from typing import Annotated, Self
from uuid import UUID

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)
from pydantic.json_schema import SkipJsonSchema

from app.models.task import TaskPriority, TaskStatus

TaskTitle = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
TaskDescription = Annotated[str, StringConstraints(max_length=5000)]


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: TaskTitle
    description: TaskDescription | None = None
    status: TaskStatus = TaskStatus.PENDENTE
    priority: TaskPriority = TaskPriority.MEDIA
    due_at: AwareDatetime | None = None


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # None representa omissao internamente; nao e um valor ou default valido na API.
    title: TaskTitle | SkipJsonSchema[None] = Field(default_factory=lambda: None)
    description: TaskDescription | None = None
    status: TaskStatus | SkipJsonSchema[None] = Field(default_factory=lambda: None)
    priority: TaskPriority | SkipJsonSchema[None] = Field(default_factory=lambda: None)
    due_at: AwareDatetime | None = None

    @model_validator(mode="after")
    def reject_null_required_fields(self) -> Self:
        for name in ("title", "status", "priority"):
            if name in self.model_fields_set and getattr(self, name) is None:
                raise ValueError(f"{name} cannot be null")
        return self


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_at: AwareDatetime | None
    created_at: AwareDatetime
    updated_at: AwareDatetime
