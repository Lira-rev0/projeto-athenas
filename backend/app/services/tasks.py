from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task, TaskPriority, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(session: Session, data: TaskCreate) -> Task:
    task = Task(**data.model_dump())
    session.add(task)
    session.flush()
    session.refresh(task)
    return task


def list_tasks(
    session: Session, status: TaskStatus | None = None, priority: TaskPriority | None = None
) -> list[Task]:
    statement = select(Task).order_by(Task.created_at.desc(), Task.id.desc())
    if status is not None:
        statement = statement.where(Task.status == status)
    if priority is not None:
        statement = statement.where(Task.priority == priority)
    return list(session.scalars(statement))


def get_task(session: Session, task_id: UUID) -> Task | None:
    return session.get(Task, task_id)


def update_task(session: Session, task: Task, data: TaskUpdate) -> Task:
    changes = data.model_dump(exclude_unset=True)
    if changes:
        for field, value in changes.items():
            setattr(task, field, value)
        task.updated_at = datetime.now(UTC)
        session.flush()
        session.refresh(task)
    return task


def delete_task(session: Session, task: Task) -> None:
    session.delete(task)
    session.flush()
