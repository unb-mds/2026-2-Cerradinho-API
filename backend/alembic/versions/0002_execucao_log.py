import sqlalchemy as sa

from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "execucao_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("task_name", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("tipo_falha", sa.String(length=20), nullable=True),
        sa.Column("mensagem", sa.Text(), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_execucao_logs")),
    )

def downgrade() -> None:
    op.drop_table("execucao_logs")