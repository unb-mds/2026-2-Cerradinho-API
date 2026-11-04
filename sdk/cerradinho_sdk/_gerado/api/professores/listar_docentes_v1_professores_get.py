from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.docente import Docente
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    nome: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_nome: None | str | Unset
    if isinstance(nome, Unset):
        json_nome = UNSET
    else:
        json_nome = nome
    params["nome"] = json_nome

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/professores",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[Docente] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Docente.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[Docente]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    nome: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | list[Docente]]:
    """Listar professores

     Lista os docentes que dão aula no período, em ordem alfabética, com os códigos das disciplinas de
    cada um. Aceita busca parcial por nome em `nome`, sem diferenciar maiúsculas/minúsculas ou acentos.
    Os dados vêm das turmas do SIGAA público, atualizadas semanalmente, aos domingos.

    Args:
        nome (None | str | Unset): Busca parcial por nome, normalizada

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[Docente]]
    """

    kwargs = _get_kwargs(
        nome=nome,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    nome: None | str | Unset = UNSET,
) -> HTTPValidationError | list[Docente] | None:
    """Listar professores

     Lista os docentes que dão aula no período, em ordem alfabética, com os códigos das disciplinas de
    cada um. Aceita busca parcial por nome em `nome`, sem diferenciar maiúsculas/minúsculas ou acentos.
    Os dados vêm das turmas do SIGAA público, atualizadas semanalmente, aos domingos.

    Args:
        nome (None | str | Unset): Busca parcial por nome, normalizada

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[Docente]
    """

    return sync_detailed(
        client=client,
        nome=nome,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    nome: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | list[Docente]]:
    """Listar professores

     Lista os docentes que dão aula no período, em ordem alfabética, com os códigos das disciplinas de
    cada um. Aceita busca parcial por nome em `nome`, sem diferenciar maiúsculas/minúsculas ou acentos.
    Os dados vêm das turmas do SIGAA público, atualizadas semanalmente, aos domingos.

    Args:
        nome (None | str | Unset): Busca parcial por nome, normalizada

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[Docente]]
    """

    kwargs = _get_kwargs(
        nome=nome,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    nome: None | str | Unset = UNSET,
) -> HTTPValidationError | list[Docente] | None:
    """Listar professores

     Lista os docentes que dão aula no período, em ordem alfabética, com os códigos das disciplinas de
    cada um. Aceita busca parcial por nome em `nome`, sem diferenciar maiúsculas/minúsculas ou acentos.
    Os dados vêm das turmas do SIGAA público, atualizadas semanalmente, aos domingos.

    Args:
        nome (None | str | Unset): Busca parcial por nome, normalizada

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[Docente]
    """

    return (
        await asyncio_detailed(
            client=client,
            nome=nome,
        )
    ).parsed
