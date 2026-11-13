from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.turma import Turma
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    busca: None | str | Unset = UNSET,
    departamento: None | str | Unset = UNSET,
    limite: int | None | Unset = UNSET,
    offset: int | Unset = 0,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_busca: None | str | Unset
    if isinstance(busca, Unset):
        json_busca = UNSET
    else:
        json_busca = busca
    params["busca"] = json_busca

    json_departamento: None | str | Unset
    if isinstance(departamento, Unset):
        json_departamento = UNSET
    else:
        json_departamento = departamento
    params["departamento"] = json_departamento

    json_limite: int | None | Unset
    if isinstance(limite, Unset):
        json_limite = UNSET
    else:
        json_limite = limite
    params["limite"] = json_limite

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/disciplinas",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[Turma] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Turma.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | list[Turma]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    busca: None | str | Unset = UNSET,
    departamento: None | str | Unset = UNSET,
    limite: int | None | Unset = UNSET,
    offset: int | Unset = 0,
) -> Response[HTTPValidationError | list[Turma]]:
    """Listar disciplinas

     Lista as turmas ofertadas no período, com professores, horários, sala e vagas. Aceita busca parcial
    em `busca` (código ou nome da disciplina, nome de professor - sem diferenciar maiúsculas/minúsculas
    ou acentos), filtro por `departamento` (prefixo do código, ex. "FGA") e paginação com
    `limite`/`offset` (o total depois do filtro vem no cabeçalho `X-Total-Count`). Sem nenhum parâmetro,
    devolve todas as turmas, como sempre. Os dados vêm do SIGAA público e são atualizados semanalmente,
    aos domingos.

    Args:
        busca (None | str | Unset): Busca parcial por código, disciplina ou professor
        departamento (None | str | Unset): Prefixo do código da disciplina, ex. "FGA"
        limite (int | None | Unset): Máximo de turmas a devolver
        offset (int | Unset): Quantas turmas pular, pra paginar Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[Turma]]
    """

    kwargs = _get_kwargs(
        busca=busca,
        departamento=departamento,
        limite=limite,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    busca: None | str | Unset = UNSET,
    departamento: None | str | Unset = UNSET,
    limite: int | None | Unset = UNSET,
    offset: int | Unset = 0,
) -> HTTPValidationError | list[Turma] | None:
    """Listar disciplinas

     Lista as turmas ofertadas no período, com professores, horários, sala e vagas. Aceita busca parcial
    em `busca` (código ou nome da disciplina, nome de professor - sem diferenciar maiúsculas/minúsculas
    ou acentos), filtro por `departamento` (prefixo do código, ex. "FGA") e paginação com
    `limite`/`offset` (o total depois do filtro vem no cabeçalho `X-Total-Count`). Sem nenhum parâmetro,
    devolve todas as turmas, como sempre. Os dados vêm do SIGAA público e são atualizados semanalmente,
    aos domingos.

    Args:
        busca (None | str | Unset): Busca parcial por código, disciplina ou professor
        departamento (None | str | Unset): Prefixo do código da disciplina, ex. "FGA"
        limite (int | None | Unset): Máximo de turmas a devolver
        offset (int | Unset): Quantas turmas pular, pra paginar Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[Turma]
    """

    return sync_detailed(
        client=client,
        busca=busca,
        departamento=departamento,
        limite=limite,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    busca: None | str | Unset = UNSET,
    departamento: None | str | Unset = UNSET,
    limite: int | None | Unset = UNSET,
    offset: int | Unset = 0,
) -> Response[HTTPValidationError | list[Turma]]:
    """Listar disciplinas

     Lista as turmas ofertadas no período, com professores, horários, sala e vagas. Aceita busca parcial
    em `busca` (código ou nome da disciplina, nome de professor - sem diferenciar maiúsculas/minúsculas
    ou acentos), filtro por `departamento` (prefixo do código, ex. "FGA") e paginação com
    `limite`/`offset` (o total depois do filtro vem no cabeçalho `X-Total-Count`). Sem nenhum parâmetro,
    devolve todas as turmas, como sempre. Os dados vêm do SIGAA público e são atualizados semanalmente,
    aos domingos.

    Args:
        busca (None | str | Unset): Busca parcial por código, disciplina ou professor
        departamento (None | str | Unset): Prefixo do código da disciplina, ex. "FGA"
        limite (int | None | Unset): Máximo de turmas a devolver
        offset (int | Unset): Quantas turmas pular, pra paginar Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[Turma]]
    """

    kwargs = _get_kwargs(
        busca=busca,
        departamento=departamento,
        limite=limite,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    busca: None | str | Unset = UNSET,
    departamento: None | str | Unset = UNSET,
    limite: int | None | Unset = UNSET,
    offset: int | Unset = 0,
) -> HTTPValidationError | list[Turma] | None:
    """Listar disciplinas

     Lista as turmas ofertadas no período, com professores, horários, sala e vagas. Aceita busca parcial
    em `busca` (código ou nome da disciplina, nome de professor - sem diferenciar maiúsculas/minúsculas
    ou acentos), filtro por `departamento` (prefixo do código, ex. "FGA") e paginação com
    `limite`/`offset` (o total depois do filtro vem no cabeçalho `X-Total-Count`). Sem nenhum parâmetro,
    devolve todas as turmas, como sempre. Os dados vêm do SIGAA público e são atualizados semanalmente,
    aos domingos.

    Args:
        busca (None | str | Unset): Busca parcial por código, disciplina ou professor
        departamento (None | str | Unset): Prefixo do código da disciplina, ex. "FGA"
        limite (int | None | Unset): Máximo de turmas a devolver
        offset (int | Unset): Quantas turmas pular, pra paginar Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[Turma]
    """

    return (
        await asyncio_detailed(
            client=client,
            busca=busca,
            departamento=departamento,
            limite=limite,
            offset=offset,
        )
    ).parsed
