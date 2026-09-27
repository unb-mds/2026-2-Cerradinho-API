"""Leitura dos docentes gravados pelo domínio de disciplinas (RF04).

Não existe scraper próprio de professores: a tabela é preenchida por
`app/domain/disciplinas.py` a partir das turmas capturadas.
"""

from sqlalchemy.orm import Session

from app.models import Professor
from app.schemas.api.professor import Professor as ProfessorResposta


def _professor_para_resposta(professor: Professor) -> ProfessorResposta:
    codigos = sorted({turma.disciplina.codigo for turma in professor.turmas})
    return ProfessorResposta(id=professor.id, nome=professor.nome, disciplinas=codigos)


def listar_professores(session: Session) -> list[ProfessorResposta]:
    professores = session.query(Professor).order_by(Professor.nome).all()
    return [_professor_para_resposta(professor) for professor in professores]
