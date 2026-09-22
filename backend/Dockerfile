FROM ghcr.io/astral-sh/uv:0.11.28 AS uv
FROM python:3.13-slim-bookworm

COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-cache
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./

RUN useradd --system --uid 10001 athenas
USER athenas
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
