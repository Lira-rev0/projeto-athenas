from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.models.task import Task, TaskPriority, TaskStatus
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services import tasks

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={503: {"description": "Banco de dados indisponivel"}},
)
TaskSession = Annotated[Session, Depends(get_session, scope="function")]


def _get_task_or_404(session: Session, task_id: UUID) -> Task:
    task = tasks.get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, session: TaskSession) -> TaskRead:
    return TaskRead.model_validate(tasks.create_task(session, data))


@router.get("", response_model=list[TaskRead])
def list_tasks(
    session: TaskSession,
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
) -> list[TaskRead]:
    return [TaskRead.model_validate(task) for task in tasks.list_tasks(session, status, priority)]


@router.get(
    "/{task_id}", response_model=TaskRead, responses={404: {"description": "Tarefa ausente"}}
)
def get_task(task_id: UUID, session: TaskSession) -> TaskRead:
    return TaskRead.model_validate(_get_task_or_404(session, task_id))


@router.patch(
    "/{task_id}", response_model=TaskRead, responses={404: {"description": "Tarefa ausente"}}
)
def update_task(task_id: UUID, data: TaskUpdate, session: TaskSession) -> TaskRead:
    """Preserva campos omitidos. Um objeto vazio nao modifica updated_at."""
    task = _get_task_or_404(session, task_id)
    return TaskRead.model_validate(tasks.update_task(session, task, data))


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Tarefa ausente"}},
)
def delete_task(task_id: UUID, session: TaskSession) -> Response:
    tasks.delete_task(session, _get_task_or_404(session, task_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
