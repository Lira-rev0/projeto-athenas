"""CRUD real em schemas temporarios: nunca apaga tarefas do banco de desenvolvimento."""

import os
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from fastapi.testclient import TestClient
from sqlalchemy import Engine, inspect, select, text
from sqlalchemy.exc import IntegrityError

from app.core.config import Settings
from app.db.session import create_database_engine, get_engine
from app.main import create_app
from app.models.task import Task

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.getenv("ATHENAS_RUN_INTEGRATION") != "1",
        reason="Defina ATHENAS_RUN_INTEGRATION=1 com PostgreSQL e migrations disponiveis",
    ),
]


@pytest.fixture
def task_engine() -> Iterator[Engine]:
    engine = create_database_engine(Settings())
    schema = f"athenas_test_{uuid4().hex}"
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    migration = ScriptDirectory.from_config(config).get_revision("0002_create_tasks")
    assert migration is not None
    try:
        with engine.begin() as connection:
            connection.execute(text(f'CREATE SCHEMA "{schema}"'))
            connection.execute(text(f'SET LOCAL search_path TO "{schema}", public'))
            with Operations.context(MigrationContext.configure(connection)):
                migration.module.upgrade()
        yield engine.execution_options(schema_translate_map={None: schema})
    finally:
        # O nome e gerado neste teste; nenhum schema existente e reutilizado.
        with engine.begin() as connection:
            connection.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
        engine.dispose()


@pytest.fixture
def task_client(task_engine: Engine) -> Iterator[TestClient]:
    application = create_app(Settings())
    application.dependency_overrides[get_engine] = lambda: task_engine
    with TestClient(application) as client:
        yield client


def create_task(client: TestClient, **fields: object) -> dict:
    response = client.post("/tasks", json={"title": "Preparar demonstracao ficticia", **fields})
    assert response.status_code == 201, response.text
    return response.json()


def test_create_defaults_and_committed_persistence(
    task_client: TestClient, task_engine: Engine
) -> None:
    task = create_task(task_client, title="  Preparar demonstracao  ")

    assert UUID(task["id"]).version == 4
    assert task["title"] == "Preparar demonstracao"
    assert task["status"] == "pendente"
    assert task["priority"] == "media"
    assert task["description"] is None
    assert task["due_at"] is None
    assert datetime.fromisoformat(task["created_at"]).tzinfo is not None
    assert datetime.fromisoformat(task["updated_at"]).tzinfo is not None
    # Uma nova conexao enxerga o commit realizado pela sessao HTTP.
    with task_engine.connect() as connection:
        row = connection.execute(select(Task).where(Task.id == UUID(task["id"]))).one()
        assert row.title == "Preparar demonstracao"
        assert row.created_at.tzinfo is not None
    assert task_engine.pool.checkedout() == 0


def test_create_preserves_due_instant(task_client: TestClient) -> None:
    task = create_task(
        task_client,
        description="Somente dados ficticios",
        priority="alta",
        due_at="2030-03-10T14:30:00-03:00",
    )

    detail = task_client.get(f"/tasks/{task['id']}")
    assert detail.status_code == 200
    assert detail.json()["description"] == "Somente dados ficticios"
    assert detail.json()["priority"] == "alta"
    assert datetime.fromisoformat(detail.json()["due_at"]) == datetime(
        2030, 3, 10, 17, 30, tzinfo=UTC
    )


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": ""},
        {"title": " \t\n "},
        {"title": "x" * 201},
        {"title": "Teste", "description": "x" * 5001},
        {"title": "Teste", "status": "desconhecido"},
        {"title": "Teste", "priority": "desconhecida"},
        {"title": "Teste", "due_at": "2030-01-01T10:00:00"},
        {"title": "Teste", "due_at": "data-invalida"},
    ],
)
def test_invalid_creation_does_not_persist(task_client: TestClient, payload: dict) -> None:
    assert task_client.post("/tasks", json=payload).status_code == 422
    assert task_client.get("/tasks").json() == []


def test_empty_list(task_client: TestClient) -> None:
    response = task_client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_order_and_combined_filters(task_client: TestClient, task_engine: Engine) -> None:
    first = create_task(task_client, priority="alta")
    second = create_task(task_client, status="em_andamento", priority="alta")
    third = create_task(task_client, priority="baixa")
    tasks = task_client.get("/tasks").json()
    assert [task["id"] for task in tasks] == [third["id"], second["id"], first["id"]]
    assert [task["id"] for task in task_client.get("/tasks?status=pendente").json()] == [
        third["id"],
        first["id"],
    ]
    assert [task["id"] for task in task_client.get("/tasks?priority=alta").json()] == [
        second["id"],
        first["id"],
    ]
    filtered = task_client.get("/tasks?status=em_andamento&priority=alta")
    assert [task["id"] for task in filtered.json()] == [second["id"]]
    assert task_client.get("/tasks?status=invalido").status_code == 422
    assert task_client.get("/tasks?priority=invalida").status_code == 422
    # Empates no timestamp tambem tem ordem estavel.
    with task_engine.begin() as connection:
        connection.execute(
            Task.__table__.update().values(created_at=datetime(2030, 1, 1, tzinfo=UTC))
        )
    ids = [task["id"] for task in task_client.get("/tasks").json()]
    assert ids == sorted(ids, reverse=True)


def test_patch_preserves_omitted_fields_and_updates_timestamp(task_client: TestClient) -> None:
    task = create_task(
        task_client,
        description="Manter descricao",
        priority="urgente",
        due_at="2030-01-01T12:00:00Z",
    )
    response = task_client.patch(f"/tasks/{task['id']}", json={"title": "Titulo revisado"})
    assert response.status_code == 200
    updated = response.json()
    assert updated["title"] == "Titulo revisado"
    for field in ("id", "description", "status", "priority", "due_at", "created_at"):
        assert updated[field] == task[field]
    assert datetime.fromisoformat(updated["updated_at"]) > datetime.fromisoformat(
        task["updated_at"]
    )
    assert task_client.get(f"/tasks/{task['id']}").json() == updated


def test_patch_changes_status_and_clears_optional_fields(task_client: TestClient) -> None:
    task = create_task(task_client, description="Remover", due_at="2030-01-01T12:00:00Z")
    response = task_client.patch(
        f"/tasks/{task['id']}",
        json={"status": "concluida", "priority": "baixa", "description": None, "due_at": None},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "concluida"
    assert response.json()["priority"] == "baixa"
    assert response.json()["description"] is None
    assert response.json()["due_at"] is None


@pytest.mark.parametrize(
    "patch", [{"title": None}, {"status": None}, {"priority": None}, {"title": " "}]
)
def test_invalid_patch_preserves_task(task_client: TestClient, patch: dict) -> None:
    task = create_task(task_client)
    assert task_client.patch(f"/tasks/{task['id']}", json=patch).status_code == 422
    assert task_client.get(f"/tasks/{task['id']}").json() == task


def test_empty_patch_is_noop(task_client: TestClient) -> None:
    task = create_task(task_client)
    response = task_client.patch(f"/tasks/{task['id']}", json={})
    assert response.status_code == 200
    assert response.json() == task


def test_delete_is_committed(task_client: TestClient, task_engine: Engine) -> None:
    task = create_task(task_client)
    response = task_client.delete(f"/tasks/{task['id']}")
    assert response.status_code == 204
    assert response.content == b""
    assert task_client.get(f"/tasks/{task['id']}").status_code == 404
    with task_engine.connect() as connection:
        assert connection.execute(select(Task.id)).all() == []


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_missing_task_returns_404(task_client: TestClient, method: str) -> None:
    kwargs = {"json": {"status": "concluida"}} if method == "patch" else {}
    assert task_client.request(method, f"/tasks/{uuid4()}", **kwargs).status_code == 404


def test_invalid_uuid_returns_422(task_client: TestClient) -> None:
    assert task_client.get("/tasks/not-a-uuid").status_code == 422


def test_database_constraints_and_transaction_recovery(task_engine: Engine) -> None:
    for invalid in ({"title": " "}, {"status": "invalido"}, {"priority": "outra"}):
        with pytest.raises(IntegrityError), task_engine.begin() as connection:
            connection.execute(Task.__table__.insert().values(**{"title": "Valida", **invalid}))
    with task_engine.begin() as connection:
        connection.execute(Task.__table__.insert().values(title="Apos rollback"))
    with task_engine.connect() as connection:
        assert connection.execute(select(Task.title)).scalars().all() == ["Apos rollback"]


def test_task_migration_downgrade_and_upgrade(task_engine: Engine) -> None:
    schema = task_engine.get_execution_options()["schema_translate_map"][None]
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    migration = ScriptDirectory.from_config(config).get_revision("0002_create_tasks")
    assert migration is not None
    with task_engine.begin() as connection:
        connection.execute(text(f'SET LOCAL search_path TO "{schema}", public'))
        with Operations.context(MigrationContext.configure(connection)):
            migration.module.downgrade()
            assert not inspect(connection).has_table("tasks", schema=schema)
            migration.module.upgrade()
            assert inspect(connection).has_table("tasks", schema=schema)
