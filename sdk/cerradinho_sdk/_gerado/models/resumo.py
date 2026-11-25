from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Resumo")


@_attrs_define
class Resumo:
    """
    Attributes:
        turmas (int): Total de turmas capturadas no período.
        disciplinas (int): Total de disciplinas distintas.
        professores (int): Total de docentes distintos.
        salas (int): Total de salas distintas.
    """

    turmas: int
    disciplinas: int
    professores: int
    salas: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        turmas = self.turmas

        disciplinas = self.disciplinas

        professores = self.professores

        salas = self.salas

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "turmas": turmas,
                "disciplinas": disciplinas,
                "professores": professores,
                "salas": salas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        turmas = d.pop("turmas")

        disciplinas = d.pop("disciplinas")

        professores = d.pop("professores")

        salas = d.pop("salas")

        resumo = cls(
            turmas=turmas,
            disciplinas=disciplinas,
            professores=professores,
            salas=salas,
        )

        resumo.additional_properties = d
        return resumo

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
