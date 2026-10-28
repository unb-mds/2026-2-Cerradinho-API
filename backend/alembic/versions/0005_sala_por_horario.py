"""move sala de turma pra horario (turma pode usar salas diferentes por dia)

O SIGAA pode listar mais de uma sala pra mesma turma quando ela usa salas
diferentes em dias diferentes (ex. "FCTE - S1 / MOCAP"), e isso não cabia
no `turmas.sala_id` (uma sala só por turma) - ver app/domain/disciplinas.py.
Essa migration move a referência de sala pra `horarios`, preservando a
sala que a turma já tinha em cada um de seus horários existentes (o
desdobramento por dia só passa a valer com a próxima raspagem, quando
cada turma é regravada do zero - ver RF15).

Revision ID: 0005
Revises: 0004
Create Date: 2026-10-27

"""

import sqlalchemy as sa

from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("horarios", sa.Column("sala_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_horarios_sala_id_salas"), "horarios", "salas", ["sala_id"], ["id"]
    )

    bind = op.get_bind()
    bind.execute(
        sa.text(
            "UPDATE horarios SET sala_id = ("
            "SELECT sala_id FROM turmas WHERE turmas.id = horarios.turma_id"
            ")"
        )
    )

    op.drop_constraint(op.f("fk_turmas_sala_id_salas"), "turmas", type_="foreignkey")
    op.drop_column("turmas", "sala_id")


def downgrade() -> None:
    op.add_column("turmas", sa.Column("sala_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_turmas_sala_id_salas"), "turmas", "salas", ["sala_id"], ["id"]
    )

    bind = op.get_bind()
    # pega a sala de qualquer um dos horários da turma - se a turma tinha
    # salas diferentes por dia, essa informação já não existe mais pra
    # recompor com certeza.
    bind.execute(
        sa.text(
            "UPDATE turmas SET sala_id = ("
            "SELECT sala_id FROM horarios WHERE horarios.turma_id = turmas.id "
            "AND horarios.sala_id IS NOT NULL LIMIT 1"
            ")"
        )
    )

    op.drop_constraint(op.f("fk_horarios_sala_id_salas"), "horarios", type_="foreignkey")
    op.drop_column("horarios", "sala_id")
