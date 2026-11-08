from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ItemRefeicao")


@_attrs_define
class ItemRefeicao:
    """
    Attributes:
        categoria (str): Categoria do item, como aparece no cardápio do RU.
        item (str): Descrição do item.
    """

    categoria: str
    item: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        categoria = self.categoria

        item = self.item

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "categoria": categoria,
                "item": item,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        categoria = d.pop("categoria")

        item = d.pop("item")

        item_refeicao = cls(
            categoria=categoria,
            item=item,
        )

        item_refeicao.additional_properties = d
        return item_refeicao

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
