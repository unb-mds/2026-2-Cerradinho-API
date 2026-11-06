from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.espaco import Espaco


T = TypeVar("T", bound="BlocoAgenda")


@_attrs_define
class BlocoAgenda:
    """
    Attributes:
        dia (str): Dia da semana, no mesmo formato de GET /v1/salas/vazias.
        inicio (str): Início do bloco, no formato HH:MM.
        fim (str): Fim do bloco, no formato HH:MM.
        sala (Espaco | None): Sala do bloco, nula se a turma não tem sala.
    """

    dia: str
    inicio: str
    fim: str
    sala: Espaco | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.espaco import Espaco

        dia = self.dia

        inicio = self.inicio

        fim = self.fim

        sala: dict[str, Any] | None
        if isinstance(self.sala, Espaco):
            sala = self.sala.to_dict()
        else:
            sala = self.sala

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dia": dia,
                "inicio": inicio,
                "fim": fim,
                "sala": sala,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.espaco import Espaco

        d = dict(src_dict)
        dia = d.pop("dia")

        inicio = d.pop("inicio")

        fim = d.pop("fim")

        def _parse_sala(data: object) -> Espaco | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sala_type_0 = Espaco.from_dict(data)

                return sala_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Espaco | None, data)

        sala = _parse_sala(d.pop("sala"))

        bloco_agenda = cls(
            dia=dia,
            inicio=inicio,
            fim=fim,
            sala=sala,
        )

        bloco_agenda.additional_properties = d
        return bloco_agenda

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
