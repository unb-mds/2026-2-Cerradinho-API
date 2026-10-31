"""Leitura dos docentes gravados pelo domínio de disciplinas (RF04).

Não existe scraper próprio de professores: a tabela é preenchida por
`app/domain/disciplinas.py` a partir das turmas capturadas.
"""

import unicodedata

from sqlalchemy.orm import Session

from app.domain.salas import DIA_PARA_DIGITO, horario_para_intervalos_por_dia
from app.models import Professor
from app.schemas.api.agenda import Agenda, BlocoAgenda, TurmaAgenda
from app.schemas.api.professor import Docente
from app.schemas.api.sala import Espaco

_DIA_POR_DIGITO = {digito: dia for dia, digito in DIA_PARA_DIGITO.items()}


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


def _bloco_para_resposta(dia: str, inicio: str, fim: str, sala) -> BlocoAgenda:
    espaco = Espaco(id=sala.id, nome=sala.nome, predio=sala.predio) if sala is not None else None
    return BlocoAgenda(dia=dia, inicio=inicio, fim=fim, sala=espaco)


def _turma_para_agenda(turma) -> TurmaAgenda:
    blocos = []
    for horario in turma.horarios:
        for dia_digito, intervalos in horario_para_intervalos_por_dia(horario.codigo).items():
            dia = _DIA_POR_DIGITO.get(dia_digito)
            if dia is None:
                continue
            for inicio, fim in intervalos:
                blocos.append(_bloco_para_resposta(dia, inicio, fim, horario.sala))
    blocos.sort(key=lambda bloco: (int(DIA_PARA_DIGITO[bloco.dia]), bloco.inicio))

    return TurmaAgenda(
        disciplina_codigo=turma.disciplina.codigo,
        disciplina_nome=turma.disciplina.nome,
        numero=turma.numero,
        ano_periodo=turma.ano_periodo,
        horarios=blocos,
    )


def obter_agenda_professor(session: Session, professor_id: int) -> Agenda | None:
    """Agenda semanal do professor: todas as turmas vinculadas a ele (RF02),
    com o horário decomposto em dia/início/fim (reaproveita a grade do
    RF17) e a sala de cada bloco — uma turma pode ter salas diferentes por
    dia (ADR 0010). `None` se o professor não existir."""
    professor = session.get(Professor, professor_id)
    if professor is None:
        return None

    turmas = sorted(professor.turmas, key=lambda turma: (turma.disciplina.codigo, turma.numero))
    return Agenda(id=professor.id, nome=professor.nome, turmas=[_turma_para_agenda(t) for t in turmas])
