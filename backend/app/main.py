from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import Settings
from app.db.session import create_database_engine


def create_app(settings: Settings | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        engine = create_database_engine(settings or Settings())
        application.state.engine = engine
        try:
            yield
        finally:
            engine.dispose()

    application = FastAPI(title="Athenas API", version="0.1.0", lifespan=lifespan)
    application.include_router(health_router)
    return application


app = create_app()
