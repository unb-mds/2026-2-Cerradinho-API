"""Cria no UptimeRobot os monitores de disponibilidade do RNF03.

Uso (na pasta backend/):

    UPTIMEROBOT_API_KEY=<chave principal da conta> python -m scripts.uptimerobot
    python -m scripts.uptimerobot --dry-run   # só mostra o que seria criado

O script é idempotente: monitor com o mesmo nome já existente na conta é mantido
como está. Todos os contatos de alerta da conta (o e-mail do cadastro, no mínimo)
são ligados aos monitores novos.

O prefixo do nome separa os dois tipos de incidente do RNF03, porque o nome do
monitor vem no assunto do e-mail de alerta:
- [API]   nosso serviço fora do ar: olhar o deploy;
- [FONTE] SIGAA ou RU fora do ar: nada a fazer no código, a API segue servindo o
          último dado coletado e o scraper tenta de novo no próximo agendamento.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass

API_UPTIMEROBOT = "https://api.uptimerobot.com/v2/"
API_CERRADINHO_PADRAO = "https://api.3-147-228-104.sslip.io"

TIPO_HTTP = 1
TIPO_PALAVRA_CHAVE = 2
ALERTA_SE_PALAVRA_SUMIR = 2  # keyword_type 2: alerta quando a palavra não aparece


@dataclass(frozen=True)
class Monitor:
    nome: str
    url: str
    intervalo_min: int
    palavra_chave: str | None = None

    @property
    def eh_fonte(self) -> bool:
        return self.nome.startswith("[FONTE]")


def monitores(api_url: str = API_CERRADINHO_PADRAO) -> tuple[Monitor, ...]:
    """Monitores do RNF03. As URLs das fontes são as mesmas que os scrapers acessam."""
    return (
        # /health roda SELECT 1 no banco e devolve 503 sem ele; /docs ou uma rota
        # com cache responderiam 200 com o banco fora do ar.
        Monitor("[API] Cerradinho", f"{api_url.rstrip('/')}/health", 5),
        Monitor("[FONTE] SIGAA home", "https://sigaa.unb.br/sigaa/public/", 5),
        Monitor("[FONTE] SIGAA busca de turmas", "https://sigaa.unb.br/sigaa/public/turmas/listar.jsf?aba=p-ensino", 5),
        # O RU já respondeu 200 com a página sem cardápio; a palavra-chave pega isso.
        Monitor("[FONTE] RU cardápio", "https://ru.unb.br/cardapio/", 15, palavra_chave="Cardápio"),
        Monitor(
            "[FONTE] RU cardápio refeitório", "https://ru.unb.br/cardapio-refeitorio/", 15, palavra_chave="Cardápio"
        ),
    )


Enviar = Callable[[str, dict[str, str]], dict]


def _post(url: str, dados: dict[str, str]) -> dict:
    corpo = urllib.parse.urlencode(dados).encode()
    requisicao = urllib.request.Request(url, data=corpo, method="POST")
    requisicao.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(requisicao, timeout=30) as resposta:  # nosec B310
        return json.load(resposta)


class ErroUptimeRobot(RuntimeError):
    pass


def chamar(metodo: str, api_key: str, enviar: Enviar = _post, **params: str) -> dict:
    resposta = enviar(API_UPTIMEROBOT + metodo, {"api_key": api_key, "format": "json", **params})
    if resposta.get("stat") != "ok":
        raise ErroUptimeRobot(f"{metodo} falhou: {resposta.get('error', resposta)}")
    return resposta


def parametros(monitor: Monitor, contatos: list[str]) -> dict[str, str]:
    params = {
        "friendly_name": monitor.nome,
        "url": monitor.url,
        "type": str(TIPO_HTTP),
        "interval": str(monitor.intervalo_min * 60),
    }
    if monitor.palavra_chave:
        params |= {
            "type": str(TIPO_PALAVRA_CHAVE),
            "keyword_type": str(ALERTA_SE_PALAVRA_SUMIR),
            "keyword_value": monitor.palavra_chave,
        }
    if contatos:
        # formato <id>_<limiar>_<recorrência>; 0_0 = avisa na primeira confirmação, uma vez
        params["alert_contacts"] = "-".join(f"{c}_0_0" for c in contatos)
    return params


def criar_monitores(
    api_key: str, api_url: str = API_CERRADINHO_PADRAO, *, dry_run: bool = False, enviar: Enviar = _post
) -> list[str]:
    """Cria os monitores que ainda não existem na conta. Devolve os nomes criados."""
    existentes = {m["friendly_name"] for m in chamar("getMonitors", api_key, enviar).get("monitors", [])}
    contatos = [str(c["id"]) for c in chamar("getAlertContacts", api_key, enviar).get("alert_contacts", [])]

    criados = []
    for monitor in monitores(api_url):
        if monitor.nome in existentes:
            print(f"já existe:  {monitor.nome}")
            continue
        if not dry_run:
            chamar("newMonitor", api_key, enviar, **parametros(monitor, contatos))
        print(f"{'criaria' if dry_run else 'criado'}:    {monitor.nome} -> {monitor.url}")
        criados.append(monitor.nome)
    return criados


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--api-url", default=os.environ.get("CERRADINHO_API_URL", API_CERRADINHO_PADRAO))
    parser.add_argument("--dry-run", action="store_true", help="só mostra o que seria criado")
    args = parser.parse_args(argv)

    api_key = os.environ.get("UPTIMEROBOT_API_KEY")
    if not api_key:
        if args.dry_run:
            for monitor in monitores(args.api_url):
                print(f"criaria:    {monitor.nome} -> {monitor.url}")
            return 0
        print("Defina UPTIMEROBOT_API_KEY com a chave principal da conta (no painel do UptimeRobot, na seção de API).")
        return 1

    try:
        criar_monitores(api_key, args.api_url, dry_run=args.dry_run)
    except ErroUptimeRobot as erro:
        print(erro, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
