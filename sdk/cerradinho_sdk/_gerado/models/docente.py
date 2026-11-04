from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

T = TypeVar("T", bound="Docente")


@_attrs_define
class Docente:
    """
    Attributes:
        id (int): Identificador interno do docente.
        nome (str): Nome do docente como aparece no SIGAA.
        disciplinas (list[str]): Códigos das disciplinas que o docente leciona no período, sem repetição.
    """

    id: int
    nome: str
    disciplinas: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        nome = self.nome

        disciplinas = self.disciplinas

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "nome": nome,
                "disciplinas": disciplinas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        id = d.pop("id")

        nome = d.pop("nome")

        disciplinas = cast(list[str], d.pop("disciplinas"))

        docente = cls(
            id=id,
            nome=nome,
            disciplinas=disciplinas,
        )

        docente.additional_properties = d
        return docente

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
