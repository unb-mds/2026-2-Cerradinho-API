"""Leitura dos docentes gravados pelo domínio de disciplinas (RF04).

Não existe scraper próprio de professores: a tabela é preenchida por
`app/domain/disciplinas.py` a partir das turmas capturadas.
"""

import unicodedata

from sqlalchemy.orm import Session

from app.models import Professor
from app.schemas.api.professor import Docente


def _normalizar_busca(texto: str) -> str:
    """Remove acentuação e ignora maiúsculas/minúsculas pra comparação de
    busca — "andré" e "Andre" e "ANDRÉ" todos viram a mesma chave."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return sem_acento.casefold()


def _professor_para_resposta(professor: Professor) -> Docente:
    codigos = sorted({turma.disciplina.codigo for turma in professor.turmas})
    return Docente(id=professor.id, nome=professor.nome, disciplinas=codigos)


def listar_professores(session: Session, nome: str | None = None) -> list[Docente]:
    """nome filtra por busca parcial, normalizada (sem diferenciar
    maiúsculas/minúsculas ou acentos). Cada palavra de `nome` precisa
    aparecer em algum lugar do nome do professor, em qualquer ordem — assim
    "luis araujo" acha "André Luis Araújo" mesmo sem ser substring exata.
    Filtra em Python, não em SQL: o volume de professores é pequeno, e
    acento/caixa não são tratados de forma portável entre SQLite (testes)
    e Postgres (produção) sem extensão (unaccent)."""
    professores = session.query(Professor).order_by(Professor.nome).all()
    if nome:
        termos = _normalizar_busca(nome).split()
        professores = [
            p for p in professores if all(termo in _normalizar_busca(p.nome) for termo in termos)
        ]
    return [_professor_para_resposta(professor) for professor in professores]
