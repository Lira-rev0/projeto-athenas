from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.models.task import TaskPriority, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


def test_create_trims_title_and_uses_domain_defaults() -> None:
    task = TaskCreate(title="  Preparar pauta ficticia \n")

    assert task.title == "Preparar pauta ficticia"
    assert task.status is TaskStatus.PENDENTE
    assert task.priority is TaskPriority.MEDIA
    assert task.description is None
    assert task.due_at is None


@pytest.mark.parametrize("title", ["", " ", "\n\t", "\u00a0", "x" * 201, None, 123])
def test_create_rejects_invalid_title(title: object) -> None:
    with pytest.raises(ValidationError):
        TaskCreate.model_validate({"title": title})


def test_create_requires_title() -> None:
    with pytest.raises(ValidationError):
        TaskCreate.model_validate({})


@pytest.mark.parametrize("schema", [TaskCreate, TaskUpdate])
@pytest.mark.parametrize(
    "values",
    [
        {"description": "x" * 5001},
        {"status": "unknown"},
        {"priority": "unknown"},
        {"due_at": "not-a-date"},
        {"due_at": "2026-09-22T10:00:00"},
        {"created_at": "2026-09-22T10:00:00Z"},
    ],
)
def test_input_rejects_invalid_values(
    schema: type[TaskCreate] | type[TaskUpdate], values: dict[str, object]
) -> None:
    with pytest.raises(ValidationError):
        schema.model_validate({"title": "Tarefa ficticia", **values})


@pytest.mark.parametrize("schema", [TaskCreate, TaskUpdate])
def test_timezone_offset_preserves_deadline_instant(
    schema: type[TaskCreate] | type[TaskUpdate],
) -> None:
    task = schema.model_validate(
        {"title": "Revisao ficticia", "due_at": "2026-09-22T10:00:00-03:00"}
    )

    assert task.due_at is not None
    assert task.due_at.astimezone(UTC) == datetime(2026, 9, 22, 13, tzinfo=UTC)


def test_update_preserves_omitted_fields_and_accepts_null_for_optional_fields() -> None:
    task = TaskUpdate(description=None, due_at=None)

    assert task.model_dump(exclude_unset=True) == {"description": None, "due_at": None}
    assert TaskUpdate().model_dump(exclude_unset=True) == {}


@pytest.mark.parametrize("field", ["title", "status", "priority"])
def test_update_rejects_explicit_null_for_required_fields(field: str) -> None:
    with pytest.raises(ValidationError):
        TaskUpdate.model_validate({field: None})


def test_update_schema_documents_omission_separately_from_nullable_values() -> None:
    schema = TaskUpdate.model_json_schema()

    assert schema.get("required", []) == []
    for field in ("title", "status", "priority"):
        field_schema = schema["properties"][field]
        if "$ref" in field_schema:
            field_schema = schema["$defs"][field_schema["$ref"].split("/")[-1]]
        assert field_schema["type"] == "string"
        assert "default" not in schema["properties"][field]
    for field in ("description", "due_at"):
        assert {"type": "null"} in schema["properties"][field]["anyOf"]


def test_maximum_title_and_description_lengths_are_accepted() -> None:
    task = TaskCreate(title="x" * 200, description="x" * 5000)

    assert len(task.title) == 200
    assert task.description is not None
    assert len(task.description) == 5000
