import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cardapio_semana import CardapioSemana
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    data_inicio: datetime.date | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_data_inicio: str | Unset = UNSET
    if not isinstance(data_inicio, Unset):
        json_data_inicio = data_inicio.isoformat()
    params["data_inicio"] = json_data_inicio

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/cardapio/semana",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CardapioSemana | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CardapioSemana.from_dict(response.json())

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
) -> Response[CardapioSemana | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    data_inicio: datetime.date | Unset = UNSET,
) -> Response[CardapioSemana | HTTPValidationError]:
    """Cardápio da semana

     Devolve o cardápio do RU (campus Darcy Ribeiro) dos sete dias a partir de `data_inicio`, agrupado
    por dia e por refeição (RF19). A resposta sempre tem os sete dias. Um dia sem cardápio coletado vem
    com `publicado` falso e as refeições vazias. O cardápio é atualizado diariamente a partir do PDF
    semanal publicado pelo RU.

    Args:
        data_inicio (datetime.date | Unset): Primeiro dia da semana (default: hoje)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardapioSemana | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        data_inicio=data_inicio,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    data_inicio: datetime.date | Unset = UNSET,
) -> CardapioSemana | HTTPValidationError | None:
    """Cardápio da semana

     Devolve o cardápio do RU (campus Darcy Ribeiro) dos sete dias a partir de `data_inicio`, agrupado
    por dia e por refeição (RF19). A resposta sempre tem os sete dias. Um dia sem cardápio coletado vem
    com `publicado` falso e as refeições vazias. O cardápio é atualizado diariamente a partir do PDF
    semanal publicado pelo RU.

    Args:
        data_inicio (datetime.date | Unset): Primeiro dia da semana (default: hoje)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardapioSemana | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        data_inicio=data_inicio,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    data_inicio: datetime.date | Unset = UNSET,
) -> Response[CardapioSemana | HTTPValidationError]:
    """Cardápio da semana

     Devolve o cardápio do RU (campus Darcy Ribeiro) dos sete dias a partir de `data_inicio`, agrupado
    por dia e por refeição (RF19). A resposta sempre tem os sete dias. Um dia sem cardápio coletado vem
    com `publicado` falso e as refeições vazias. O cardápio é atualizado diariamente a partir do PDF
    semanal publicado pelo RU.

    Args:
        data_inicio (datetime.date | Unset): Primeiro dia da semana (default: hoje)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CardapioSemana | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        data_inicio=data_inicio,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    data_inicio: datetime.date | Unset = UNSET,
) -> CardapioSemana | HTTPValidationError | None:
    """Cardápio da semana

     Devolve o cardápio do RU (campus Darcy Ribeiro) dos sete dias a partir de `data_inicio`, agrupado
    por dia e por refeição (RF19). A resposta sempre tem os sete dias. Um dia sem cardápio coletado vem
    com `publicado` falso e as refeições vazias. O cardápio é atualizado diariamente a partir do PDF
    semanal publicado pelo RU.

    Args:
        data_inicio (datetime.date | Unset): Primeiro dia da semana (default: hoje)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CardapioSemana | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            data_inicio=data_inicio,
        )
    ).parsed
