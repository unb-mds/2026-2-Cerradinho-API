"""schema inicial: professores, salas, disciplinas, turmas, horarios, cardapios

Revision ID: 0001
Revises:
Create Date: 2026-09-13

"""

import sqlalchemy as sa

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "professores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_professores")),
    )

    op.create_table(
        "salas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=50), nullable=False),
        sa.Column("predio", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_salas")),
    )

    op.create_table(
        "disciplinas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("codigo", sa.String(length=20), nullable=False),
        sa.Column("nome", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_disciplinas")),
        sa.UniqueConstraint("codigo", name=op.f("uq_disciplinas_codigo")),
    )

    op.create_table(
        "turmas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("numero", sa.String(length=10), nullable=False),
        sa.Column("ano_periodo", sa.String(length=10), nullable=False),
        sa.Column("unidade", sa.String(length=100), nullable=False),
        sa.Column("vagas_ofertadas", sa.Integer(), nullable=False),
        sa.Column("vagas_ocupadas", sa.Integer(), nullable=False),
        sa.Column("disciplina_id", sa.Integer(), nullable=False),
        sa.Column("sala_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["disciplina_id"],
            ["disciplinas.id"],
            name=op.f("fk_turmas_disciplina_id_disciplinas"),
        ),
        sa.ForeignKeyConstraint(
            ["sala_id"],
            ["salas.id"],
            name=op.f("fk_turmas_sala_id_salas"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_turmas")),
        sa.UniqueConstraint(
            "disciplina_id", "numero", "ano_periodo", name=op.f("uq_turmas_disciplina_id")
        ),
    )

    op.create_table(
        "turma_professores",
        sa.Column("turma_id", sa.Integer(), nullable=False),
        sa.Column("professor_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["turma_id"],
            ["turmas.id"],
            name=op.f("fk_turma_professores_turma_id_turmas"),
        ),
        sa.ForeignKeyConstraint(
            ["professor_id"],
            ["professores.id"],
            name=op.f("fk_turma_professores_professor_id_professores"),
        ),
        sa.PrimaryKeyConstraint("turma_id", "professor_id", name=op.f("pk_turma_professores")),
    )

    op.create_table(
        "horarios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("codigo", sa.String(length=20), nullable=False),
        sa.Column("descricao", sa.String(length=200), nullable=False),
        sa.Column("turma_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["turma_id"],
            ["turmas.id"],
            name=op.f("fk_horarios_turma_id_turmas"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_horarios")),
    )

    op.create_table(
        "cardapios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("data", sa.Date(), nullable=False),
        sa.Column("cafe", sa.Text(), nullable=True),
        sa.Column("almoco", sa.Text(), nullable=True),
        sa.Column("jantar", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cardapios")),
        sa.UniqueConstraint("data", name=op.f("uq_cardapios_data")),
    )


def downgrade() -> None:
    op.drop_table("cardapios")
    op.drop_table("horarios")
    op.drop_table("turma_professores")
    op.drop_table("turmas")
    op.drop_table("disciplinas")
    op.drop_table("salas")
    op.drop_table("professores")
