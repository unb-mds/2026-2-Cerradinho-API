"""Cliente ergonômico pra Cerradinho API (RF13).

Encapsula o cliente HTTP gerado (`cerradinho_sdk._gerado`, ver RF11) em
métodos simples e tipados pelos mesmos modelos que a API devolve - não
recalcula nada que o backend já computa (salas vazias e agenda do
professor continuam sendo só leitura do que a API responde).
"""

from __future__ import annotations

import datetime
from types import TracebackType
from typing import Self

import httpx

from ._gerado import Client as _ClienteGerado
from ._gerado.api.cardapio import (
    listar_cardapio_da_semana_v1_cardapio_semana_get as _cardapio,
)
from ._gerado.api.disciplinas import (
    listar_disciplinas_v1_disciplinas_get as _disciplinas,
)
from ._gerado.api.execucoes import listar_v1_execucoes_get as _execucoes
from ._gerado.api.professores import listar_docentes_v1_professores_get as _professores
from ._gerado.api.professores import (
    obter_agenda_v1_professores_professor_id_agenda_get as _agenda,
)
from ._gerado.api.salas import listar_espacos_v1_salas_get as _salas
from ._gerado.api.salas import (
    listar_espacos_vazios_v1_salas_vazias_get as _salas_vazias,
)
from ._gerado.models import (
    Agenda,
    CardapioSemana,
    DiaSemana,
    Docente,
    Espaco,
    Execucao,
    Turma,
)
from ._gerado.types import UNSET


class ProfessorNaoEncontrado(Exception):
    """Nenhum professor com esse id (RF18)."""

    def __init__(self, professor_id: int) -> None:
        super().__init__(f"Nenhum professor com id={professor_id}")
        self.professor_id = professor_id


class RespostaInesperada(Exception):
    """A API devolveu algo fora do que o contrato documenta (RF11) - ex. um
    422 de validação, ou uma mudança de contrato que esta versão do SDK
    ainda não conhece (RF12)."""

    def __init__(self, status_code: int | None, corpo: object) -> None:
        super().__init__(f"Resposta inesperada da API (status={status_code}): {corpo!r}")
        self.status_code = status_code
        self.corpo = corpo


class CerradinhoClient:
    """Cliente pra API pública da Cerradinho (`/v1/`, RF10).

    >>> with CerradinhoClient("https://api.<ip>.sslip.io") as cerradinho:
    ...     cerradinho.listar_salas_vazias(dia="segunda", horario="14:00")

    `base_url` é obrigatório e não tem um padrão de produção embutido: o
    deploy (ADR 0011) usa `https://api.<ip>.sslip.io`, com o IP real da
    instância (ver `docs/DEPLOY.md`), que muda a cada deploy e ainda não é
    fixo — um valor fixo aqui resolveria DNS errado silenciosamente.
    """

    def __init__(self, base_url: str, *, timeout: float = 10.0) -> None:
        self._cliente = _ClienteGerado(base_url=base_url, timeout=httpx.Timeout(timeout))
        self._fechado = False

    def __enter__(self) -> Self:
        self._verificar_aberto()
        self._cliente.__enter__()
        return self

    def __exit__(
        self,
        tipo_excecao: type[BaseException] | None,
        excecao: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._cliente.__exit__(tipo_excecao, excecao, traceback)
        self._fechado = True

    def _verificar_aberto(self) -> None:
        if self._fechado:
            raise RuntimeError(
                "CerradinhoClient já foi fechado (saiu do `with` ou chamou fechar()) - crie um novo pra continuar."
            )

    def fechar(self) -> None:
        """Encerra as conexões HTTP abertas. Opcional fora de um `with`;
        chamar duas vezes, ou sem nunca ter feito uma requisição, não tem
        efeito."""
        if not self._fechado:
            self._cliente.get_httpx_client().close()
            self._fechado = True

    def listar_disciplinas(self) -> list[Turma]:
        """Turmas ofertadas no período, com professores, horários, sala e vagas (RF01-05)."""
        self._verificar_aberto()
        resposta = _disciplinas.sync_detailed(client=self._cliente)
        if not isinstance(resposta.parsed, list):
            raise RespostaInesperada(resposta.status_code, resposta.parsed)
        return resposta.parsed

    def listar_professores(self, nome: str | None = None) -> list[Docente]:
        """Docentes do período, com as disciplinas que lecionam (RF04).

        `nome` filtra por busca parcial, sem diferenciar acento ou caixa."""
        self._verificar_aberto()
        resposta = _professores.sync_detailed(client=self._cliente, nome=nome if nome is not None else UNSET)
        if not isinstance(resposta.parsed, list):
            raise RespostaInesperada(resposta.status_code, resposta.parsed)
        return resposta.parsed

    def obter_agenda(self, professor_id: int) -> Agenda:
        """Agenda semanal do professor, com horário decomposto em dia/início/fim
        e a sala de cada bloco de aula (RF18).

        Levanta `ProfessorNaoEncontrado` se `professor_id` não existir."""
        self._verificar_aberto()
        resposta = _agenda.sync_detailed(professor_id, client=self._cliente)
        if resposta.status_code == httpx.codes.NOT_FOUND:
            raise ProfessorNaoEncontrado(professor_id)
        if not isinstance(resposta.parsed, Agenda):
            raise RespostaInesperada(resposta.status_code, resposta.parsed)
        return resposta.parsed

    def listar_salas(self) -> list[Espaco]:
        """Salas com aula no período, ordenadas por prédio e nome (RF05)."""
        self._verificar_aberto()
        resposta = _salas.sync_detailed(client=self._cliente)
        if not isinstance(resposta.parsed, list):
            raise RespostaInesperada(resposta.status_code, resposta.parsed)
        return resposta.parsed

    def listar_salas_vazias(self, dia: DiaSemana | str, horario: str) -> list[Espaco]:
        """Salas sem nenhuma turma cadastrada no dia/horário dados (RF17).

        `dia` é um dos nomes de `DiaSemana` ("segunda", "terca", ...); `horario`
        é o início de uma aula, no formato "HH:MM" (ex. "14:00")."""
        self._verificar_aberto()
        resposta = _salas_vazias.sync_detailed(client=self._cliente, dia=DiaSemana(dia), horario=horario)
        if not isinstance(resposta.parsed, list):
            raise RespostaInesperada(resposta.status_code, resposta.parsed)
        return resposta.parsed

    def obter_cardapio_semana(self, data_inicio: datetime.date | None = None) -> CardapioSemana:
        """Cardápio do RU (Darcy) dos 7 dias a partir de `data_inicio` (hoje, se
        omitido), agrupado por dia e refeição, sempre com os 7 dias (RF19)."""
        self._verificar_aberto()
        resposta = _cardapio.sync_detailed(
            client=self._cliente,
            data_inicio=data_inicio if data_inicio is not None else UNSET,
        )
        if not isinstance(resposta.parsed, CardapioSemana):
            raise RespostaInesperada(resposta.status_code, resposta.parsed)
        return resposta.parsed

    def listar_execucoes(self, limite: int = 50) -> list[Execucao]:
        """Histórico de execuções dos scrapers, da mais recente pra mais antiga
        (RF16). `limite` é o número máximo de execuções devolvidas."""
        self._verificar_aberto()
        resposta = _execucoes.sync_detailed(client=self._cliente, limite=limite)
        if not isinstance(resposta.parsed, list):
            raise RespostaInesperada(resposta.status_code, resposta.parsed)
        return resposta.parsed
