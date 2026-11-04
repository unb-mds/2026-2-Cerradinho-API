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

URL_BASE_PADRAO = "https://api.cerradinho.sslip.io"


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
        super().__init__(
            f"Resposta inesperada da API (status={status_code}): {corpo!r}"
        )
        self.status_code = status_code
        self.corpo = corpo


class CerradinhoClient:
    """Cliente pra API pública da Cerradinho (`/v1/`, RF10).

    >>> with CerradinhoClient() as cerradinho:
    ...     cerradinho.listar_salas_vazias(dia="segunda", horario="14:00")

    `base_url` default aponta pro deploy em produção (ver ADR 0011); passe
    outro valor pra testar contra um ambiente local, ex.
    `CerradinhoClient("http://localhost:8000")`.
    """

    def __init__(
        self, base_url: str = URL_BASE_PADRAO, *, timeout: float = 10.0
    ) -> None:
        self._cliente = _ClienteGerado(
            base_url=base_url, timeout=httpx.Timeout(timeout)
        )

    def __enter__(self) -> Self:
        self._cliente.__enter__()
        return self

    def __exit__(
        self,
        tipo_excecao: type[BaseException] | None,
        excecao: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._cliente.__exit__(tipo_excecao, excecao, traceback)

    def fechar(self) -> None:
        """Encerra as conexões HTTP abertas. Opcional fora de um `with`."""
        self._cliente.get_httpx_client().close()

    def listar_disciplinas(self) -> list[Turma]:
        """Turmas ofertadas no período, com professores, horários, sala e vagas (RF01-05)."""
        return _disciplinas.sync(client=self._cliente) or []

    def listar_professores(self, nome: str | None = None) -> list[Docente]:
        """Docentes do período, com as disciplinas que lecionam (RF04).

        `nome` filtra por busca parcial, sem diferenciar acento ou caixa."""
        resultado = _professores.sync(
            client=self._cliente, nome=nome if nome is not None else UNSET
        )
        return resultado if isinstance(resultado, list) else []

    def obter_agenda(self, professor_id: int) -> Agenda:
        """Agenda semanal do professor, com horário decomposto em dia/início/fim
        e a sala de cada bloco de aula (RF18).

        Levanta `ProfessorNaoEncontrado` se `professor_id` não existir."""
        resposta = _agenda.sync_detailed(professor_id, client=self._cliente)
        if resposta.status_code == httpx.codes.NOT_FOUND:
            raise ProfessorNaoEncontrado(professor_id)
        if not isinstance(resposta.parsed, Agenda):
            raise RespostaInesperada(resposta.status_code, resposta.parsed)
        return resposta.parsed

    def listar_salas(self) -> list[Espaco]:
        """Salas com aula no período, ordenadas por prédio e nome (RF05)."""
        return _salas.sync(client=self._cliente) or []

    def listar_salas_vazias(self, dia: DiaSemana | str, horario: str) -> list[Espaco]:
        """Salas sem nenhuma turma cadastrada no dia/horário dados (RF17).

        `dia` é um dos nomes de `DiaSemana` ("segunda", "terca", ...); `horario`
        é o início de uma aula, no formato "HH:MM" (ex. "14:00")."""
        resultado = _salas_vazias.sync(
            client=self._cliente, dia=DiaSemana(dia), horario=horario
        )
        return resultado if isinstance(resultado, list) else []

    def obter_cardapio_semana(
        self, data_inicio: datetime.date | None = None
    ) -> CardapioSemana:
        """Cardápio do RU (Darcy) dos 7 dias a partir de `data_inicio` (hoje, se
        omitido), agrupado por dia e refeição, sempre com os 7 dias (RF19)."""
        resultado = _cardapio.sync(
            client=self._cliente,
            data_inicio=data_inicio if data_inicio is not None else UNSET,
        )
        if not isinstance(resultado, CardapioSemana):
            raise RespostaInesperada(None, resultado)
        return resultado

    def listar_execucoes(self, limite: int = 50) -> list[Execucao]:
        """Histórico de execuções dos scrapers, da mais recente pra mais antiga
        (RF16). `limite` é o número máximo de execuções devolvidas."""
        resultado = _execucoes.sync(client=self._cliente, limite=limite)
        return resultado if isinstance(resultado, list) else []
