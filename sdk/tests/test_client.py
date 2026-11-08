"""Testes do CerradinhoClient contra respostas HTTP mockadas (respx) -
nunca contra a API em produção, nem contra o backend rodando."""

import httpx
import pytest
import respx

from cerradinho_sdk import CerradinhoClient, ProfessorNaoEncontrado, RespostaInesperada

BASE_URL = "https://api.cerradinho.teste"


@pytest.fixture
def cerradinho():
    with CerradinhoClient(BASE_URL) as cliente:
        yield cliente


@respx.mock
def test_listar_disciplinas(cerradinho):
    turma = {
        "disciplina_codigo": "FGA0242",
        "disciplina_nome": "Métodos de Desenvolvimento de Software",
        "numero": "01",
        "ano_periodo": "2026.2",
        "professores": [{"nome": "Ana Souza"}],
        "horarios": [{"codigo": "6T2345", "descricao": "Sexta-feira 14:00 às 17:50"}],
        "sala": {"descricao": "FCTE - I9/I10"},
        "vagas_ofertadas": 40,
        "vagas_ocupadas": 38,
    }
    respx.get(f"{BASE_URL}/v1/disciplinas").mock(return_value=httpx.Response(200, json=[turma]))

    turmas = cerradinho.listar_disciplinas()

    assert len(turmas) == 1
    assert turmas[0].disciplina_codigo == "FGA0242"
    assert turmas[0].professores[0].nome == "Ana Souza"


@respx.mock
def test_listar_professores_filtra_por_nome(cerradinho):
    rota = respx.get(f"{BASE_URL}/v1/professores").mock(
        return_value=httpx.Response(200, json=[{"id": 1, "nome": "Ana Souza", "disciplinas": ["FGA0242"]}])
    )

    professores = cerradinho.listar_professores(nome="ana")

    assert rota.calls.last.request.url.params["nome"] == "ana"
    assert [p.nome for p in professores] == ["Ana Souza"]


@respx.mock
def test_obter_agenda(cerradinho):
    agenda = {
        "id": 12,
        "nome": "André Barros de Sales",
        "turmas": [
            {
                "disciplina_codigo": "FGA0242",
                "disciplina_nome": "Métodos de Desenvolvimento de Software",
                "numero": "01",
                "ano_periodo": "2026.2",
                "horarios": [
                    {
                        "dia": "sexta",
                        "inicio": "14:00",
                        "fim": "17:50",
                        "sala": {"id": 7, "predio": "FCTE", "nome": "I9/I10"},
                    }
                ],
            }
        ],
    }
    respx.get(f"{BASE_URL}/v1/professores/12/agenda").mock(return_value=httpx.Response(200, json=agenda))

    resposta = cerradinho.obter_agenda(12)

    assert resposta.nome == "André Barros de Sales"
    bloco = resposta.turmas[0].horarios[0]
    assert (bloco.dia, bloco.inicio, bloco.fim, bloco.sala.nome) == (
        "sexta",
        "14:00",
        "17:50",
        "I9/I10",
    )


@respx.mock
def test_obter_agenda_professor_inexistente_levanta_erro(cerradinho):
    respx.get(f"{BASE_URL}/v1/professores/999/agenda").mock(return_value=httpx.Response(404))

    with pytest.raises(ProfessorNaoEncontrado):
        cerradinho.obter_agenda(999)


@respx.mock
def test_obter_agenda_resposta_fora_do_contrato_levanta_erro(cerradinho):
    """Status inesperado (não documentado pro endpoint) - ex. uma mudança de
    contrato que esta versão do SDK ainda não conhece (RF12)."""
    respx.get(f"{BASE_URL}/v1/professores/1/agenda").mock(return_value=httpx.Response(500))

    with pytest.raises(RespostaInesperada):
        cerradinho.obter_agenda(1)


@respx.mock
def test_listar_salas(cerradinho):
    respx.get(f"{BASE_URL}/v1/salas").mock(
        return_value=httpx.Response(200, json=[{"id": 1, "nome": "I9/I10", "predio": "FCTE"}])
    )

    salas = cerradinho.listar_salas()

    assert [(s.predio, s.nome) for s in salas] == [("FCTE", "I9/I10")]


@respx.mock
def test_listar_salas_vazias(cerradinho):
    rota = respx.get(f"{BASE_URL}/v1/salas/vazias").mock(
        return_value=httpx.Response(200, json=[{"id": 1, "nome": "MOCAP", "predio": "FCTE"}])
    )

    vazias = cerradinho.listar_salas_vazias(dia="segunda", horario="14:00")

    assert rota.calls.last.request.url.params["dia"] == "segunda"
    assert rota.calls.last.request.url.params["horario"] == "14:00"
    assert [s.nome for s in vazias] == ["MOCAP"]


@respx.mock
def test_obter_cardapio_semana(cerradinho):
    semana = {
        "data_inicio": "2026-10-26",
        "data_fim": "2026-11-01",
        "dias": [
            {
                "data": "2026-10-26",
                "cafe_da_manha": [],
                "almoco": [{"categoria": "Prato Principal", "item": "Frango grelhado"}],
                "jantar": [],
                "publicado": True,
            }
        ]
        + [
            {
                "data": f"2026-10-{d:02d}",
                "cafe_da_manha": [],
                "almoco": [],
                "jantar": [],
                "publicado": False,
            }
            for d in range(27, 32)
        ]
        + [
            {
                "data": "2026-11-01",
                "cafe_da_manha": [],
                "almoco": [],
                "jantar": [],
                "publicado": False,
            }
        ],
    }
    respx.get(f"{BASE_URL}/v1/cardapio/semana").mock(return_value=httpx.Response(200, json=semana))

    cardapio = cerradinho.obter_cardapio_semana()

    assert len(cardapio.dias) == 7
    assert cardapio.dias[0].almoco[0].item == "Frango grelhado"


@respx.mock
def test_listar_execucoes_usa_o_limite_informado(cerradinho):
    rota = respx.get(f"{BASE_URL}/v1/execucoes").mock(return_value=httpx.Response(200, json=[]))

    cerradinho.listar_execucoes(limite=10)

    assert rota.calls.last.request.url.params["limite"] == "10"


@pytest.mark.parametrize(
    ("metodo", "args", "kwargs", "rota"),
    [
        ("listar_disciplinas", (), {}, "/v1/disciplinas"),
        ("listar_professores", (), {}, "/v1/professores"),
        ("listar_salas", (), {}, "/v1/salas"),
        ("listar_salas_vazias", (), {"dia": "segunda", "horario": "14h"}, "/v1/salas/vazias"),
        ("listar_execucoes", (), {}, "/v1/execucoes"),
    ],
)
@respx.mock
def test_metodos_de_lista_levantam_erro_em_resposta_inesperada(cerradinho, metodo, args, kwargs, rota):
    """Achado da revisão do Gabriel: um 422/429/500 não pode virar lista
    vazia em silêncio - "nenhuma sala vazia" e "não tem turma" são
    respostas válidas só quando a API realmente devolve `[]` com 200."""
    corpo_422 = {"detail": [{"loc": ["query", "parametro"], "msg": "inválido", "type": "value_error"}]}
    respx.get(f"{BASE_URL}{rota}").mock(return_value=httpx.Response(422, json=corpo_422))

    with pytest.raises(RespostaInesperada):
        getattr(cerradinho, metodo)(*args, **kwargs)


@respx.mock
def test_obter_cardapio_semana_resposta_fora_do_contrato_levanta_erro(cerradinho):
    respx.get(f"{BASE_URL}/v1/cardapio/semana").mock(return_value=httpx.Response(500))

    with pytest.raises(RespostaInesperada):
        cerradinho.obter_cardapio_semana()


def test_usar_cliente_depois_de_fechado_levanta_erro_claro():
    """Achado da revisão do Gabriel: usar o cliente depois do `with` (ou de
    `fechar()`) dava um `RuntimeError` do httpx sobre conexão fechada, não
    um erro claro do SDK."""
    with CerradinhoClient(BASE_URL) as cliente:
        pass

    with pytest.raises(RuntimeError, match="já foi fechado"):
        cliente.listar_disciplinas()


def test_fechar_duas_vezes_nao_quebra():
    cliente = CerradinhoClient(BASE_URL)
    cliente.fechar()
    cliente.fechar()  # não pode levantar erro
