from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.item_refeicao import ItemRefeicao


T = TypeVar("T", bound="CardapioDia")


@_attrs_define
class CardapioDia:
    """
    Attributes:
        data (datetime.date): Dia do cardápio.
        cafe_da_manha (list[ItemRefeicao]): Itens do café da manhã, na ordem do PDF.
        almoco (list[ItemRefeicao]): Itens do almoço, na ordem do PDF.
        jantar (list[ItemRefeicao]): Itens do jantar, na ordem do PDF.
        publicado (bool): Falso quando o RU ainda não publicou ou o Cerradinho não coletou o cardápio do dia. Nesse caso
            as três refeições vêm vazias.
    """

    data: datetime.date
    cafe_da_manha: list[ItemRefeicao]
    almoco: list[ItemRefeicao]
    jantar: list[ItemRefeicao]
    publicado: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        data = self.data.isoformat()

        cafe_da_manha = []
        for cafe_da_manha_item_data in self.cafe_da_manha:
            cafe_da_manha_item = cafe_da_manha_item_data.to_dict()
            cafe_da_manha.append(cafe_da_manha_item)

        almoco = []
        for almoco_item_data in self.almoco:
            almoco_item = almoco_item_data.to_dict()
            almoco.append(almoco_item)

        jantar = []
        for jantar_item_data in self.jantar:
            jantar_item = jantar_item_data.to_dict()
            jantar.append(jantar_item)

        publicado = self.publicado

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "cafe_da_manha": cafe_da_manha,
                "almoco": almoco,
                "jantar": jantar,
                "publicado": publicado,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.item_refeicao import ItemRefeicao  # noqa: PLC0415

        d = dict(src_dict)
        data = datetime.date.fromisoformat(d.pop("data"))

        cafe_da_manha = []
        _cafe_da_manha = d.pop("cafe_da_manha")
        for cafe_da_manha_item_data in _cafe_da_manha:
            cafe_da_manha_item = ItemRefeicao.from_dict(cafe_da_manha_item_data)

            cafe_da_manha.append(cafe_da_manha_item)

        almoco = []
        _almoco = d.pop("almoco")
        for almoco_item_data in _almoco:
            almoco_item = ItemRefeicao.from_dict(almoco_item_data)

            almoco.append(almoco_item)

        jantar = []
        _jantar = d.pop("jantar")
        for jantar_item_data in _jantar:
            jantar_item = ItemRefeicao.from_dict(jantar_item_data)

            jantar.append(jantar_item)

        publicado = d.pop("publicado")

        cardapio_dia = cls(
            data=data,
            cafe_da_manha=cafe_da_manha,
            almoco=almoco,
            jantar=jantar,
            publicado=publicado,
        )

        cardapio_dia.additional_properties = d
        return cardapio_dia

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
