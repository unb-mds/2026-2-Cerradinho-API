from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agenda import Agenda
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    professor_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/professores/{professor_id}/agenda".format(
            professor_id=quote(str(professor_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Agenda | Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = Agenda.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Agenda | Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    professor_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Agenda | Any | HTTPValidationError]:
    """Agenda semanal do professor

     Lista as turmas do docente no período, com o horário decomposto em dia/início/fim e a sala de cada
    bloco de aula. 404 se o docente não existir.

    Args:
        professor_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Agenda | Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        professor_id=professor_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    professor_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Agenda | Any | HTTPValidationError | None:
    """Agenda semanal do professor

     Lista as turmas do docente no período, com o horário decomposto em dia/início/fim e a sala de cada
    bloco de aula. 404 se o docente não existir.

    Args:
        professor_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Agenda | Any | HTTPValidationError
    """

    return sync_detailed(
        professor_id=professor_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    professor_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Agenda | Any | HTTPValidationError]:
    """Agenda semanal do professor

     Lista as turmas do docente no período, com o horário decomposto em dia/início/fim e a sala de cada
    bloco de aula. 404 se o docente não existir.

    Args:
        professor_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Agenda | Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        professor_id=professor_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    professor_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Agenda | Any | HTTPValidationError | None:
    """Agenda semanal do professor

     Lista as turmas do docente no período, com o horário decomposto em dia/início/fim e a sala de cada
    bloco de aula. 404 se o docente não existir.

    Args:
        professor_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Agenda | Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            professor_id=professor_id,
            client=client,
        )
    ).parsed
