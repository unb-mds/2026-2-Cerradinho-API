"""alarga horarios.codigo pra caber codigo com varios segmentos

Revision ID: 0003
Revises: 0002
Create Date: 2026-10-27

"""

import sqlalchemy as sa

from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "horarios",
        "codigo",
        existing_type=sa.String(length=20),
        type_=sa.String(length=100),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "horarios",
        "codigo",
        existing_type=sa.String(length=100),
        type_=sa.String(length=20),
        nullable=False,
    )
