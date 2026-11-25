from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cardapio_dia import CardapioDia


T = TypeVar("T", bound="CardapioSemana")


@_attrs_define
class CardapioSemana:
    """
    Attributes:
        data_inicio (datetime.date): Primeiro dia da janela.
        data_fim (datetime.date): Último dia da janela (data_inicio + 6 dias).
        dias (list[CardapioDia]): Os 7 dias da janela, em ordem.
    """

    data_inicio: datetime.date
    data_fim: datetime.date
    dias: list[CardapioDia]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        data_inicio = self.data_inicio.isoformat()

        data_fim = self.data_fim.isoformat()

        dias = []
        for dias_item_data in self.dias:
            dias_item = dias_item_data.to_dict()
            dias.append(dias_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "dias": dias,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cardapio_dia import CardapioDia  # noqa: PLC0415

        d = dict(src_dict)
        data_inicio = datetime.date.fromisoformat(d.pop("data_inicio"))

        data_fim = datetime.date.fromisoformat(d.pop("data_fim"))

        dias = []
        _dias = d.pop("dias")
        for dias_item_data in _dias:
            dias_item = CardapioDia.from_dict(dias_item_data)

            dias.append(dias_item)

        cardapio_semana = cls(
            data_inicio=data_inicio,
            data_fim=data_fim,
            dias=dias,
        )

        cardapio_semana.additional_properties = d
        return cardapio_semana

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
