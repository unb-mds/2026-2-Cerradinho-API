import pytest

from app.scrapers.cardapio.scraper import URLS_CARDAPIO
from app.scrapers.disciplinas.scraper import URL_BUSCA_TURMAS, URL_HOME
from scripts.uptimerobot import ErroUptimeRobot, criar_monitores, main, monitores, parametros


class UptimeRobotFalso:
    """Guarda as chamadas e responde como a API v2 do UptimeRobot."""

    def __init__(self, existentes=(), contatos=("111", "222")):
        self.existentes = list(existentes)
        self.contatos = contatos
        self.chamadas = []

    def __call__(self, url, dados):
        metodo = url.rsplit("/", 1)[-1]
        self.chamadas.append((metodo, dados))
        if metodo == "getMonitors":
            return {"stat": "ok", "monitors": [{"friendly_name": n} for n in self.existentes]}
        if metodo == "getAlertContacts":
            return {"stat": "ok", "alert_contacts": [{"id": c} for c in self.contatos]}
        if metodo == "newMonitor":
            return {"stat": "ok", "monitor": {"id": 1}}
        return {"stat": "fail", "error": {"message": "método desconhecido"}}

    def criados(self):
        return [dados for metodo, dados in self.chamadas if metodo == "newMonitor"]


def test_fontes_monitoradas_sao_as_mesmas_que_os_scrapers_acessam():
    # Se a URL de um scraper mudar, o monitor da fonte antiga deixa de servir para
    # o RNF03: alertaria (ou não) sobre uma página que a coleta nem usa mais.
    urls_fontes = {m.url for m in monitores() if m.eh_fonte}
    assert urls_fontes == {URL_HOME, URL_BUSCA_TURMAS, *URLS_CARDAPIO}


def test_api_e_monitorada_pela_rota_health():
    (api,) = [m for m in monitores("https://api.exemplo.com/") if not m.eh_fonte]
    assert api.url == "https://api.exemplo.com/health"
    assert api.nome.startswith("[API]")


def test_todo_monitor_diz_no_nome_se_e_fonte_ou_api():
    assert all(m.nome.startswith(("[API] ", "[FONTE] ")) for m in monitores())


def test_cria_todos_os_monitores_com_os_contatos_de_alerta():
    falso = UptimeRobotFalso()

    criados = criar_monitores("chave", enviar=falso)

    assert criados == [m.nome for m in monitores()]
    assert all(dados["alert_contacts"] == "111_0_0-222_0_0" for dados in falso.criados())
    assert all(dados["api_key"] == "chave" for _, dados in falso.chamadas)


def test_nao_recria_monitor_que_ja_existe():
    falso = UptimeRobotFalso(existentes=["[API] Cerradinho", "[FONTE] SIGAA home"])

    criados = criar_monitores("chave", enviar=falso)

    assert "[API] Cerradinho" not in criados
    assert "[FONTE] SIGAA home" not in criados
    assert len(falso.criados()) == len(monitores()) - 2


def test_dry_run_nao_cria_nada():
    falso = UptimeRobotFalso()

    criados = criar_monitores("chave", dry_run=True, enviar=falso)

    assert len(criados) == len(monitores())
    assert falso.criados() == []


def test_monitor_do_ru_alerta_quando_o_cardapio_some_da_pagina():
    ru = next(m for m in monitores() if m.url == "https://ru.unb.br/cardapio/")

    params = parametros(ru, contatos=[])

    assert params["type"] == "2"  # palavra-chave
    assert params["keyword_type"] == "2"  # alerta se não existir
    assert params["keyword_value"] == "Cardápio"
    assert params["interval"] == "900"
    assert "alert_contacts" not in params


def test_monitor_http_nao_leva_palavra_chave():
    api = monitores()[0]

    params = parametros(api, contatos=["9"])

    assert params["type"] == "1"
    assert params["interval"] == "300"
    assert "keyword_type" not in params


def test_erro_da_api_do_uptimerobot_vira_excecao():
    def recusa(url, dados):
        return {"stat": "fail", "error": {"message": "api_key inválida"}}

    with pytest.raises(ErroUptimeRobot, match="api_key inválida"):
        criar_monitores("errada", enviar=recusa)


def test_sem_chave_o_script_falha_sem_chamar_a_api(monkeypatch, capsys):
    monkeypatch.delenv("UPTIMEROBOT_API_KEY", raising=False)

    assert main([]) == 1
    assert "UPTIMEROBOT_API_KEY" in capsys.readouterr().out


def test_dry_run_sem_chave_lista_o_plano(monkeypatch, capsys):
    monkeypatch.delenv("UPTIMEROBOT_API_KEY", raising=False)

    assert main(["--dry-run", "--api-url", "https://api.exemplo.com"]) == 0
    assert "https://api.exemplo.com/health" in capsys.readouterr().out
