from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session


@pytest.fixture
def task_session() -> Iterator[MagicMock]:
    with patch("app.db.session.Session") as factory:
        session = MagicMock(spec=Session)
        factory.return_value.__enter__.return_value = session
        session.scalars.return_value = []
        yield session
        factory.return_value.__exit__.assert_called_once()


def test_successful_request_commits_and_exits_session(
    client: TestClient, task_session: MagicMock
) -> None:
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []
    task_session.commit.assert_called_once()
    task_session.rollback.assert_not_called()


@pytest.mark.parametrize("failure_at", ["scalars", "commit"])
def test_database_failure_rolls_back_before_http_response(
    client: TestClient,
    task_session: MagicMock,
    failure_at: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    getattr(task_session, failure_at).side_effect = OperationalError(
        "private-sql", {}, Exception("sensitive-database-details")
    )

    response = client.get("/tasks")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
    task_session.rollback.assert_called_once()
    assert "private-sql" not in caplog.text
    assert "sensitive-database-details" not in caplog.text


def test_not_found_rolls_back_and_preserves_http_error(
    client: TestClient, task_session: MagicMock
) -> None:
    task_session.get.return_value = None

    response = client.get("/tasks/00000000-0000-0000-0000-000000000001")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
    task_session.rollback.assert_called_once()
    task_session.commit.assert_not_called()


def test_unexpected_error_rolls_back_and_propagates(
    client: TestClient, task_session: MagicMock
) -> None:
    task_session.scalars.side_effect = RuntimeError("Application error")

    with pytest.raises(RuntimeError, match="Application error"):
        client.get("/tasks")

    task_session.rollback.assert_called_once()
    task_session.commit.assert_not_called()
