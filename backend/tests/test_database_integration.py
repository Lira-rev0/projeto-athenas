import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.core.config import Settings
from app.db.session import create_database_engine
from app.main import create_app

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.getenv("ATHENAS_RUN_INTEGRATION") != "1",
        reason="Defina ATHENAS_RUN_INTEGRATION=1 com PostgreSQL e migrations disponiveis",
    ),
]


def test_health_against_real_postgresql() -> None:
    with TestClient(create_app(Settings())) as client:
        response = client.get("/health/database")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_vector_extension_is_enabled() -> None:
    engine = create_database_engine(Settings())
    try:
        with engine.connect() as connection:
            version = connection.execute(
                text("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
            ).scalar_one()
        assert version
    finally:
        engine.dispose()
