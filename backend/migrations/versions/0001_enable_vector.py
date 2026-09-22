"""Habilita pgvector sem criar tabelas de dominio."""

from alembic import op

revision: str = "0001_enable_vector"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    # Sem CASCADE: recusa a remocao se houver objetos dependentes no futuro.
    op.execute("DROP EXTENSION IF EXISTS vector")
