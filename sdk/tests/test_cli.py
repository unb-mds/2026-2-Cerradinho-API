"""Testes da CLI (RF13) contra respostas HTTP mockadas (respx).

O mock fica no nível do HTTP, e não do `CerradinhoClient`: assim cada teste
passa pela CLI e pelo SDK juntos, e confirma que a CLI consulta a API só pelo SDK.
"""

import json

import httpx
import pytest
import respx
from typer.testing import CliRunner

from cerradinho_sdk import __version__
from cerradinho_sdk.cli import app

BASE_URL = "https://api.cerradinho.teste"

TURMA = {
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

AGENDA = {
    "id": 7,
    "nome": "Ana Souza",
    "turmas": [
        {
            "disciplina_codigo": "FGA0242",
            "disciplina_nome": "MDS",
            "numero": "01",
            "ano_periodo": "2026.2",
            "horarios": [
                {"dia": "sexta", "inicio": "14:00", "fim": "15:50", "sala": {"id": 3, "nome": "I9", "predio": "FCTE"}},
                {"dia": "sexta", "inicio": "19:00", "fim": "20:40", "sala": None},
            ],
        }
    ],
}


def _dia(data, publicado=True):
    item = [{"categoria": "Prato principal", "item": "Feijoada"}] if publicado else []
    return {"data": data, "cafe_da_manha": [], "almoco": item, "jantar": [], "publicado": publicado}


CARDAPIO = {
    "data_inicio": "2026-11-09",
    "data_fim": "2026-11-15",
    "dias": [_dia("2026-11-09"), _dia("2026-11-10", publicado=False)],
}


@pytest.fixture
def cerradinho(monkeypatch):
    """Roda a CLI com a URL de teste na variável de ambiente, como um usuário faria."""
    monkeypatch.delenv("CERRADINHO_API_URL", raising=False)
    runner = CliRunner()

    def rodar(*args, env=None):
        ambiente = {"CERRADINHO_API_URL": BASE_URL, "COLUMNS": "200"}
        ambiente.update(env or {})
        return runner.invoke(app, list(args), env=ambiente)

    return rodar


def _get(rota, status=200, **kwargs):
    return respx.get(f"{BASE_URL}{rota}").mock(return_value=httpx.Response(status, **kwargs))


@respx.mock
def test_disciplinas_em_tabela(cerradinho):
    _get("/v1/disciplinas", json=[TURMA])

    resultado = cerradinho("disciplinas")

    assert resultado.exit_code == 0, resultado.output
    for esperado in ("FGA0242", "Ana Souza", "6T2345", "FCTE - I9/I10", "38/40"):
        assert esperado in resultado.output


@respx.mock
def test_disciplinas_repassa_busca_departamento_e_paginacao(cerradinho):
    rota = _get("/v1/disciplinas", json=[])

    cerradinho("disciplinas", "--busca", "métodos", "--departamento", "FGA", "--limite", "10", "--offset", "20")

    params = rota.calls.last.request.url.params
    assert dict(params) == {"busca": "métodos", "departamento": "FGA", "limite": "10", "offset": "20"}


@respx.mock
def test_json_devolve_a_resposta_da_api(cerradinho):
    _get("/v1/disciplinas", json=[TURMA])

    resultado = cerradinho("--json", "disciplinas")

    assert resultado.exit_code == 0
    assert json.loads(resultado.output) == [TURMA]


@respx.mock
def test_lista_vazia_avisa_que_nao_ha_resultado(cerradinho):
    _get("/v1/salas", json=[])

    resultado = cerradinho("salas")

    assert resultado.exit_code == 0
    assert "Nenhum resultado." in resultado.output


@respx.mock
def test_professores_filtra_por_nome(cerradinho):
    rota = _get("/v1/professores", json=[{"id": 7, "nome": "Ana Souza", "disciplinas": ["FGA0242"]}])

    resultado = cerradinho("professores", "ana")

    assert resultado.exit_code == 0
    assert rota.calls.last.request.url.params["nome"] == "ana"
    assert "Ana Souza" in resultado.output and "7" in resultado.output


@respx.mock
def test_agenda_mostra_cada_aula_e_aula_sem_sala(cerradinho):
    _get("/v1/professores/7/agenda", json=AGENDA)

    resultado = cerradinho("agenda", "7")

    assert resultado.exit_code == 0
    assert "Ana Souza" in resultado.output
    assert "FCTE - I9" in resultado.output
    assert "sem sala" in resultado.output


@respx.mock
def test_agenda_de_professor_inexistente_sai_com_erro(cerradinho):
    _get("/v1/professores/99/agenda", status=404, json={"detail": "Professor não encontrado"})

    resultado = cerradinho("agenda", "99")

    assert resultado.exit_code == 1
    assert "Nenhum professor com id=99" in resultado.output


@respx.mock
def test_salas_vazias_repassa_dia_e_horario(cerradinho):
    rota = _get("/v1/salas/vazias", json=[{"id": 3, "nome": "I9", "predio": "FCTE"}])

    resultado = cerradinho("salas-vazias", "segunda", "14:00")

    assert resultado.exit_code == 0
    assert dict(rota.calls.last.request.url.params) == {"dia": "segunda", "horario": "14:00"}
    assert "FCTE" in resultado.output


@respx.mock
def test_dia_invalido_e_recusado_antes_de_chamar_a_api(cerradinho):
    rota = _get("/v1/salas/vazias", json=[])

    resultado = cerradinho("salas-vazias", "feriado", "14:00")

    assert resultado.exit_code == 2
    assert not rota.called


@respx.mock
def test_cardapio_mostra_dia_nao_publicado(cerradinho):
    rota = _get("/v1/cardapio/semana", json=CARDAPIO)

    resultado = cerradinho("cardapio", "--data-inicio", "2026-11-09")

    assert resultado.exit_code == 0
    assert rota.calls.last.request.url.params["data_inicio"] == "2026-11-09"
    assert "09/11 a 15/11" in resultado.output
    assert "Feijoada" in resultado.output
    assert "não publicado" in resultado.output


@respx.mock
def test_execucoes_repassa_limite_e_mostra_falha(cerradinho):
    execucao = {
        "id": 9,
        "task_name": "app.tasks.cardapio.scrape_cardapio_task",
        "status": "falha",
        "criado_em": "2026-11-08T08:00:00Z",
        "tipo_falha": "fonte",
        "mensagem": "RU fora do ar",
    }
    rota = _get("/v1/execucoes", json=[execucao])

    resultado = cerradinho("execucoes", "--limite", "5")

    assert resultado.exit_code == 0
    assert rota.calls.last.request.url.params["limite"] == "5"
    for esperado in ("scrape_cardapio_task", "falha", "fonte", "RU fora do ar", "08/11/2026 08:00"):
        assert esperado in resultado.output


@respx.mock
def test_resumo(cerradinho):
    _get("/v1/resumo", json={"turmas": 6500, "disciplinas": 3000, "professores": 2700, "salas": 900})

    resultado = cerradinho("resumo")

    assert resultado.exit_code == 0
    assert "6500" in resultado.output and "Professores" in resultado.output


@respx.mock
def test_base_url_pela_opcao_tem_prioridade_sobre_a_variavel(cerradinho):
    rota = respx.get("http://localhost:8000/v1/salas").mock(return_value=httpx.Response(200, json=[]))

    resultado = cerradinho("--base-url", "http://localhost:8000", "salas")

    assert resultado.exit_code == 0
    assert rota.called


def test_sem_base_url_a_cli_pede_o_endereco(cerradinho):
    resultado = cerradinho("salas", env={"CERRADINHO_API_URL": None})

    assert resultado.exit_code == 2
    assert "--base-url" in resultado.output


def test_version(cerradinho):
    resultado = cerradinho("--version", env={"CERRADINHO_API_URL": None})

    assert resultado.exit_code == 0
    assert __version__ in resultado.output


@respx.mock
def test_api_fora_do_ar_vira_mensagem_e_nao_traceback(cerradinho):
    respx.get(f"{BASE_URL}/v1/salas").mock(side_effect=httpx.ConnectError("conexão recusada"))

    resultado = cerradinho("salas")

    assert resultado.exit_code == 1
    assert f"Não foi possível acessar a API em {BASE_URL}" in resultado.output
    assert resultado.exception is None or isinstance(resultado.exception, SystemExit)


@respx.mock
def test_timeout_vira_mensagem(cerradinho):
    respx.get(f"{BASE_URL}/v1/salas").mock(side_effect=httpx.ReadTimeout("lento"))

    resultado = cerradinho("--timeout", "2", "salas")

    assert resultado.exit_code == 1
    assert "não respondeu em 2 s" in resultado.output


@pytest.mark.parametrize(
    ("status", "corpo", "mensagem"),
    [
        (404, None, "versão anterior"),
        (429, {"error": "Rate limit exceeded"}, "Limite de requisições"),
        (500, None, "status 500"),
    ],
)
@respx.mock
def test_resposta_fora_do_contrato_vira_mensagem(cerradinho, status, corpo, mensagem):
    _get("/v1/resumo", status=status, json=corpo)

    resultado = cerradinho("resumo")

    assert resultado.exit_code == 1
    assert mensagem in resultado.output
