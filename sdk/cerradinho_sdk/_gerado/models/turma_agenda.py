from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from typing_extensions import Self

if TYPE_CHECKING:
    from ..models.bloco_agenda import BlocoAgenda


T = TypeVar("T", bound="TurmaAgenda")


@_attrs_define
class TurmaAgenda:
    """
    Attributes:
        disciplina_codigo (str): Código da disciplina.
        disciplina_nome (str): Nome da disciplina.
        numero (str): Número da turma dentro da disciplina.
        ano_periodo (str): Ano e período letivo.
        horarios (list[BlocoAgenda]): Blocos de aula da turma, ordenados por dia e início.
    """

    disciplina_codigo: str
    disciplina_nome: str
    numero: str
    ano_periodo: str
    horarios: list[BlocoAgenda]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        disciplina_codigo = self.disciplina_codigo

        disciplina_nome = self.disciplina_nome

        numero = self.numero

        ano_periodo = self.ano_periodo

        horarios = []
        for horarios_item_data in self.horarios:
            horarios_item = horarios_item_data.to_dict()
            horarios.append(horarios_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "disciplina_codigo": disciplina_codigo,
                "disciplina_nome": disciplina_nome,
                "numero": numero,
                "ano_periodo": ano_periodo,
                "horarios": horarios,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.bloco_agenda import BlocoAgenda

        d = dict(src_dict)
        disciplina_codigo = d.pop("disciplina_codigo")

        disciplina_nome = d.pop("disciplina_nome")

        numero = d.pop("numero")

        ano_periodo = d.pop("ano_periodo")

        horarios = []
        _horarios = d.pop("horarios")
        for horarios_item_data in _horarios:
            horarios_item = BlocoAgenda.from_dict(horarios_item_data)

            horarios.append(horarios_item)

        turma_agenda = cls(
            disciplina_codigo=disciplina_codigo,
            disciplina_nome=disciplina_nome,
            numero=numero,
            ano_periodo=ano_periodo,
            horarios=horarios,
        )

        turma_agenda.additional_properties = d
        return turma_agenda

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
