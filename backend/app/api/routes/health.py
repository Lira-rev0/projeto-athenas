import logging
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_engine

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


@router.get("", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness: confirma que a API responde, independentemente do banco."""
    return HealthResponse()


@router.get(
    "/database",
    response_model=HealthResponse,
    responses={503: {"description": "Banco de dados indisponivel"}},
)
def database_health(engine: Annotated[Engine, Depends(get_engine)]) -> HealthResponse:
    """Readiness: abre uma conexao e executa SELECT 1 no PostgreSQL."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1")).scalar_one()
    except SQLAlchemyError:
        # Nao expor a excecao: ela pode conter host, usuario ou detalhes de conexao.
        logger.warning("Database health check failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from None
    return HealthResponse()
