"""Cria o primeiro dominio de tarefas."""

import sqlalchemy as sa
from alembic import op

revision: str = "0002_create_tasks"
down_revision: str | None = "0001_enable_vector"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=5000), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "pendente",
                "em_andamento",
                "concluida",
                "cancelada",
                name="ck_tasks_status",
                native_enum=False,
                create_constraint=True,
            ),
            server_default="pendente",
            nullable=False,
        ),
        sa.Column(
            "priority",
            sa.Enum(
                "baixa",
                "media",
                "alta",
                "urgente",
                name="ck_tasks_priority",
                native_enum=False,
                create_constraint=True,
            ),
            server_default="media",
            nullable=False,
        ),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("length(btrim(title)) > 0", name="ck_tasks_title"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("tasks")
