from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Metadata compartilhado pelos modelos de persistencia e pelo Alembic."""
