from datetime import date, datetime, timedelta, timezone

import pytest
import schemathesis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.domain.cardapio import persistir_cardapio
from app.domain.disciplinas import persistir_turma
from app.main import app
from app.models import Base, ExecucaoLog
from app.schemas.cardapio import ItemCardapio
from app.schemas.disciplina import Horario, Professor, Sala, Turma


def _popular_banco(db_session: Session) -> None:
    # sem dados as rotas devolvem [] e o schemathesis nunca valida o formato de
    # uma Turma ou de um ItemCardapio
    persistir_turma(
        db_session,
        Turma(
            disciplina_codigo="FGA0242",
            disciplina_nome="Métodos de Desenvolvimento de Software",
            numero="01",
            ano_periodo="2026.2",
            professores=[Professor(nome="Ana Souza")],
            horarios=[Horario(codigo="6T2345", descricao="Sexta-feira 14:00 às 17:50")],
            sala=Sala(descricao="FCTE - I9/I10"),
            vagas_ofertadas=40,
            vagas_ocupadas=38,
        ),
        unidade="FCTE",
    )

    # segunda sala com aula em outro dia e turno, pra /v1/salas/vazias não devolver sempre a mesma lista
    persistir_turma(
        db_session,
        Turma(
            disciplina_codigo="FGA0158",
            disciplina_nome="Orientação a Objetos",
            numero="02",
            ano_periodo="2026.2",
            professores=[Professor(nome="Carlos Lima")],
            horarios=[Horario(codigo="35M12", descricao="Terça-feira 08:00 às 09:50 Quinta-feira 08:00 às 09:50")],
            sala=Sala(descricao="FCTE - S10"),
            vagas_ofertadas=50,
            vagas_ocupadas=45,
        ),
        unidade="FCTE",
    )

    agora = datetime.now(timezone.utc)
    db_session.add_all(
        [
            ExecucaoLog(
                task_name="app.tasks.scraping.scrape_disciplinas_task",
                status="sucesso",
                criado_em=agora - timedelta(hours=1),
            ),
            ExecucaoLog(
                task_name="app.tasks.cardapio.scrape_cardapio_task",
                status="falha",
                tipo_falha="fonte",
                mensagem="ConnectionError: ru.unb.br não respondeu",
                criado_em=agora,
            ),
        ]
    )

    # /v1/cardapio/semana sem data_inicio devolve de hoje até hoje + 6 dias
    hoje = date.today()
    persistir_cardapio(
        db_session,
        [
            ItemCardapio(data=hoje, refeicao="almoco", categoria="Prato Principal Padrão", item="Frango grelhado"),
            ItemCardapio(data=hoje, refeicao="almoco", categoria="Guarnição", item="Arroz e feijão"),
            ItemCardapio(data=hoje + timedelta(days=1), refeicao="jantar", categoria="Sopa", item="Sopa de legumes"),
        ],
    )
    db_session.commit()


@pytest.fixture
def api_schema():
    # banco sqlite em memória no lugar do postgres, igual aos testes de routers -
    # o schemathesis chama o app via ASGI, sem precisar subir servidor nem banco real
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    db_session = Session(engine)
    _popular_banco(db_session)

    app.dependency_overrides[get_db] = lambda: db_session
    yield schemathesis.openapi.from_asgi("/openapi.json", app)
    app.dependency_overrides.clear()
    db_session.close()
