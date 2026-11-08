from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Execucao")


@_attrs_define
class Execucao:
    """
    Attributes:
        id (int): Identificador interno do registro.
        task_name (str): Nome completo da task do Celery.
        status (str): 'sucesso' ou 'falha'.
        criado_em (datetime.datetime): Quando a execução terminou.
        tipo_falha (None | str | Unset): Só preenchido em falha: 'fonte' (sites fora do ar) ou 'interna' (bug no
            código).
        mensagem (None | str | Unset): Mensagem da exceção.
    """

    id: int
    task_name: str
    status: str
    criado_em: datetime.datetime
    tipo_falha: None | str | Unset = UNSET
    mensagem: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        task_name = self.task_name

        status = self.status

        criado_em = self.criado_em.isoformat()

        tipo_falha: None | str | Unset
        if isinstance(self.tipo_falha, Unset):
            tipo_falha = UNSET
        else:
            tipo_falha = self.tipo_falha

        mensagem: None | str | Unset
        if isinstance(self.mensagem, Unset):
            mensagem = UNSET
        else:
            mensagem = self.mensagem

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "task_name": task_name,
                "status": status,
                "criado_em": criado_em,
            }
        )
        if tipo_falha is not UNSET:
            field_dict["tipo_falha"] = tipo_falha
        if mensagem is not UNSET:
            field_dict["mensagem"] = mensagem

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        task_name = d.pop("task_name")

        status = d.pop("status")

        criado_em = datetime.datetime.fromisoformat(d.pop("criado_em"))

        def _parse_tipo_falha(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tipo_falha = _parse_tipo_falha(d.pop("tipo_falha", UNSET))

        def _parse_mensagem(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        mensagem = _parse_mensagem(d.pop("mensagem", UNSET))

        execucao = cls(
            id=id,
            task_name=task_name,
            status=status,
            criado_em=criado_em,
            tipo_falha=tipo_falha,
            mensagem=mensagem,
        )

        execucao.additional_properties = d
        return execucao

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
