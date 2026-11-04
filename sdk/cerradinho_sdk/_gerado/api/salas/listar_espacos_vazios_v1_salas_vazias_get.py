from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dia_semana import DiaSemana
from ...models.espaco import Espaco
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    dia: DiaSemana,
    horario: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_dia = dia.value
    params["dia"] = json_dia

    params["horario"] = horario

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/salas/vazias",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[Espaco] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Espaco.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[Espaco]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    dia: DiaSemana,
    horario: str,
) -> Response[HTTPValidationError | list[Espaco]]:
    """Listar salas vazias por dia e horário

     Lista as salas sem nenhuma turma cadastrada no dia e horário dados (RF17). `horario` é o início de
    uma aula, no formato "HH:MM" (ex.: "14:00"). "Vazia" é só "sem aula cadastrada via RF01" — não
    reflete reserva informal, evento ou uso fora da grade de disciplinas.

    Args:
        dia (DiaSemana):
        horario (str): Início de uma aula, no formato HH:MM

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[Espaco]]
    """

    kwargs = _get_kwargs(
        dia=dia,
        horario=horario,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    dia: DiaSemana,
    horario: str,
) -> HTTPValidationError | list[Espaco] | None:
    """Listar salas vazias por dia e horário

     Lista as salas sem nenhuma turma cadastrada no dia e horário dados (RF17). `horario` é o início de
    uma aula, no formato "HH:MM" (ex.: "14:00"). "Vazia" é só "sem aula cadastrada via RF01" — não
    reflete reserva informal, evento ou uso fora da grade de disciplinas.

    Args:
        dia (DiaSemana):
        horario (str): Início de uma aula, no formato HH:MM

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[Espaco]
    """

    return sync_detailed(
        client=client,
        dia=dia,
        horario=horario,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    dia: DiaSemana,
    horario: str,
) -> Response[HTTPValidationError | list[Espaco]]:
    """Listar salas vazias por dia e horário

     Lista as salas sem nenhuma turma cadastrada no dia e horário dados (RF17). `horario` é o início de
    uma aula, no formato "HH:MM" (ex.: "14:00"). "Vazia" é só "sem aula cadastrada via RF01" — não
    reflete reserva informal, evento ou uso fora da grade de disciplinas.

    Args:
        dia (DiaSemana):
        horario (str): Início de uma aula, no formato HH:MM

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[Espaco]]
    """

    kwargs = _get_kwargs(
        dia=dia,
        horario=horario,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    dia: DiaSemana,
    horario: str,
) -> HTTPValidationError | list[Espaco] | None:
    """Listar salas vazias por dia e horário

     Lista as salas sem nenhuma turma cadastrada no dia e horário dados (RF17). `horario` é o início de
    uma aula, no formato "HH:MM" (ex.: "14:00"). "Vazia" é só "sem aula cadastrada via RF01" — não
    reflete reserva informal, evento ou uso fora da grade de disciplinas.

    Args:
        dia (DiaSemana):
        horario (str): Início de uma aula, no formato HH:MM

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[Espaco]
    """

    return (
        await asyncio_detailed(
            client=client,
            dia=dia,
            horario=horario,
        )
    ).parsed
