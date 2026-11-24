from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Professor")


@_attrs_define
class Professor:
    """
    Attributes:
        nome (str): Nome do docente como aparece no SIGAA.
        id (None | int | Unset): Identificador interno do docente, o mesmo de GET /v1/professores. Nulo antes de
            persistir.
    """

    nome: str
    id: None | int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        nome = self.nome

        id: None | int | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "nome": nome,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        nome = d.pop("nome")

        def _parse_id(data: object) -> None | int | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | int | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        professor = cls(
            nome=nome,
            id=id,
        )

        professor.additional_properties = d
        return professor

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
