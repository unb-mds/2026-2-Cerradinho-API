"""funde salas e professores duplicados por falta de normalizacao

Dados gravados antes da normalização de sala/professor existir (ou com o
ponto de "LAB." inconsistente) ficaram como linhas soltas, sem nunca
convergir pra forma canônica das raspagens novas. Essa migration reaplica
a normalização de app/domain/disciplinas.py (congelada aqui, de propósito -
mudanças futuras naquele módulo não devem alterar o resultado de uma
migration já aplicada) a cada linha existente, funde as que colidem no
mesmo canônico e realoca turmas/turma_professores pra sobrevivente.

Revision ID: 0004
Revises: 0003
Create Date: 2026-10-27

"""

import re
from collections import defaultdict

import sqlalchemy as sa

from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None

_SEPARADOR_SALA = re.compile(r"\s*[-/]\s*")
_PADRAO_LAB_COM_PONTO = re.compile(r"\bLAB\.\s*")


def _normalizar_sala_legada(predio: str, nome: str) -> tuple[str, str]:
    if predio.strip():
        predio_canonico = predio.strip().upper()
        nome_bruto = nome
    else:
        # linha gravada antes da normalização existir: nome ainda é a
        # descrição bruta do SIGAA, com prédio e sala juntos.
        descricao = nome.strip()
        match = _SEPARADOR_SALA.search(descricao)
        if match:
            predio_canonico = descricao[: match.start()].strip().upper()
            nome_bruto = descricao[match.end() :].strip()
        else:
            predio_canonico = ""
            nome_bruto = descricao
    nome_canonico = _PADRAO_LAB_COM_PONTO.sub("LAB ", nome_bruto.upper()).strip()
    return predio_canonico, nome_canonico


def _normalizar_professor_legado(nome: str) -> str:
    return nome.split(" (", 1)[0].strip()


def upgrade() -> None:
    bind = op.get_bind()

    # --- salas: aplica a normalização e funde duplicadas ----------------
    salas = bind.execute(sa.text("SELECT id, predio, nome FROM salas")).fetchall()
    grupos: dict[tuple[str, str], list[int]] = defaultdict(list)
    for id_, predio, nome in salas:
        grupos[_normalizar_sala_legada(predio, nome)].append(id_)

    for (predio_canonico, nome_canonico), ids in grupos.items():
        sobrevivente, *duplicadas = sorted(ids)
        for duplicada in duplicadas:
            bind.execute(
                sa.text("UPDATE turmas SET sala_id = :sobrevivente WHERE sala_id = :duplicada"),
                {"sobrevivente": sobrevivente, "duplicada": duplicada},
            )
            bind.execute(sa.text("DELETE FROM salas WHERE id = :duplicada"), {"duplicada": duplicada})
        bind.execute(
            sa.text("UPDATE salas SET predio = :predio, nome = :nome WHERE id = :id"),
            {"predio": predio_canonico, "nome": nome_canonico, "id": sobrevivente},
        )

    # --- professores: tira "(XXh)" do nome e funde duplicados -----------
    professores = bind.execute(sa.text("SELECT id, nome FROM professores")).fetchall()
    grupos_professores: dict[str, list[int]] = defaultdict(list)
    for id_, nome in professores:
        grupos_professores[_normalizar_professor_legado(nome)].append(id_)

    for nome_canonico, ids in grupos_professores.items():
        sobrevivente, *duplicados = sorted(ids)
        for duplicado in duplicados:
            bind.execute(
                sa.text(
                    "UPDATE turma_professores SET professor_id = :sobrevivente "
                    "WHERE professor_id = :duplicado "
                    "AND turma_id NOT IN ("
                    "SELECT turma_id FROM turma_professores WHERE professor_id = :sobrevivente"
                    ")"
                ),
                {"sobrevivente": sobrevivente, "duplicado": duplicado},
            )
            bind.execute(
                sa.text("DELETE FROM turma_professores WHERE professor_id = :duplicado"),
                {"duplicado": duplicado},
            )
            bind.execute(sa.text("DELETE FROM professores WHERE id = :duplicado"), {"duplicado": duplicado})
        bind.execute(
            sa.text("UPDATE professores SET nome = :nome WHERE id = :id"),
            {"nome": nome_canonico, "id": sobrevivente},
        )


def downgrade() -> None:
    # fusão de dados não é reversível: as linhas duplicadas apagadas (e a
    # ligação original de cada turma a elas) não têm como ser reconstruídas.
    raise NotImplementedError("0004 funde dados duplicados e não tem downgrade")
