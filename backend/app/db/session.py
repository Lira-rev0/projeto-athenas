import logging
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import Settings

logger = logging.getLogger(__name__)


def create_database_engine(settings: Settings) -> Engine:
    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_timeout=3,
        connect_args={"connect_timeout": 3, "options": "-c statement_timeout=3000"},
    )


def get_engine(request: Request) -> Engine:
    return request.app.state.engine


def get_session(engine: Annotated[Engine, Depends(get_engine)]) -> Iterator[Session]:
    """Uma transacao por request; usar scope='function' antes de enviar a resposta."""
    try:
        with Session(engine, expire_on_commit=False) as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
    except SQLAlchemyError:
        # Excecoes SQL podem conter credenciais e valores privados dos parametros.
        logger.warning("Task database operation failed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from None
