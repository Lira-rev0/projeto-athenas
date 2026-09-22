from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.exc import OperationalError, TimeoutError

from app.db.session import get_engine


def test_health_does_not_require_a_database(client: TestClient) -> None:
    engine = MagicMock(spec=Engine)
    engine.connect.side_effect = AssertionError("Liveness must not connect to the database")
    client.app.dependency_overrides[get_engine] = lambda: engine

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_database_health_executes_a_query(client: TestClient) -> None:
    engine = MagicMock(spec=Engine)
    connection = engine.connect.return_value.__enter__.return_value
    connection.execute.return_value.scalar_one.return_value = 1
    client.app.dependency_overrides[get_engine] = lambda: engine

    response = client.get("/health/database")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert str(connection.execute.call_args.args[0]) == "SELECT 1"
    engine.connect.return_value.__exit__.assert_called_once()


@pytest.mark.parametrize("failure_at", ["connect", "query"])
def test_database_failure_is_sanitized(
    client: TestClient, failure_at: str, caplog: pytest.LogCaptureFixture
) -> None:
    engine = MagicMock(spec=Engine)
    error = OperationalError("SELECT 1", {}, Exception("sensitive-database-details"))
    if failure_at == "connect":
        engine.connect.side_effect = error
    else:
        engine.connect.return_value.__enter__.return_value.execute.side_effect = error
    client.app.dependency_overrides[get_engine] = lambda: engine

    response = client.get("/health/database")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
    assert "sensitive-database-details" not in caplog.text
    assert client.get("/health").status_code == 200


def test_database_recovers_after_pool_timeout(client: TestClient) -> None:
    engine = MagicMock(spec=Engine)
    connection_context = MagicMock()
    connection_context.__enter__.return_value.execute.return_value.scalar_one.return_value = 1
    engine.connect.side_effect = [TimeoutError("Pool exhausted"), connection_context]
    client.app.dependency_overrides[get_engine] = lambda: engine

    assert client.get("/health/database").status_code == 503
    assert client.get("/health/database").status_code == 200
