from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Espaco")


@_attrs_define
class Espaco:
    """
    Attributes:
        id (int): Identificador interno da sala.
        nome (str): Nome da sala dentro do prédio.
        predio (str): Prédio ou unidade. Vem vazio quando o SIGAA não informa o prédio.
    """

    id: int
    nome: str
    predio: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        nome = self.nome

        predio = self.predio

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "nome": nome,
                "predio": predio,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        nome = d.pop("nome")

        predio = d.pop("predio")

        espaco = cls(
            id=id,
            nome=nome,
            predio=predio,
        )

        espaco.additional_properties = d
        return espaco

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
