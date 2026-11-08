from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.horario import Horario
    from ..models.professor import Professor
    from ..models.sala import Sala


T = TypeVar("T", bound="Turma")


@_attrs_define
class Turma:
    """
    Attributes:
        disciplina_codigo (str): Código da disciplina.
        disciplina_nome (str): Nome da disciplina.
        numero (str): Número da turma dentro da disciplina.
        ano_periodo (str): Ano e período letivo.
        professores (list[Professor]): Docentes da turma.
        horarios (list[Horario]): Horários de aula da turma.
        sala (Sala):
        vagas_ofertadas (int): Total de vagas da turma.
        vagas_ocupadas (int): Vagas já preenchidas.
    """

    disciplina_codigo: str
    disciplina_nome: str
    numero: str
    ano_periodo: str
    professores: list[Professor]
    horarios: list[Horario]
    sala: Sala
    vagas_ofertadas: int
    vagas_ocupadas: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        disciplina_codigo = self.disciplina_codigo

        disciplina_nome = self.disciplina_nome

        numero = self.numero

        ano_periodo = self.ano_periodo

        professores = []
        for professores_item_data in self.professores:
            professores_item = professores_item_data.to_dict()
            professores.append(professores_item)

        horarios = []
        for horarios_item_data in self.horarios:
            horarios_item = horarios_item_data.to_dict()
            horarios.append(horarios_item)

        sala = self.sala.to_dict()

        vagas_ofertadas = self.vagas_ofertadas

        vagas_ocupadas = self.vagas_ocupadas

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "disciplina_codigo": disciplina_codigo,
                "disciplina_nome": disciplina_nome,
                "numero": numero,
                "ano_periodo": ano_periodo,
                "professores": professores,
                "horarios": horarios,
                "sala": sala,
                "vagas_ofertadas": vagas_ofertadas,
                "vagas_ocupadas": vagas_ocupadas,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.horario import Horario  # noqa: PLC0415
        from ..models.professor import Professor  # noqa: PLC0415
        from ..models.sala import Sala  # noqa: PLC0415

        d = dict(src_dict)
        disciplina_codigo = d.pop("disciplina_codigo")

        disciplina_nome = d.pop("disciplina_nome")

        numero = d.pop("numero")

        ano_periodo = d.pop("ano_periodo")

        professores = []
        _professores = d.pop("professores")
        for professores_item_data in _professores:
            professores_item = Professor.from_dict(professores_item_data)

            professores.append(professores_item)

        horarios = []
        _horarios = d.pop("horarios")
        for horarios_item_data in _horarios:
            horarios_item = Horario.from_dict(horarios_item_data)

            horarios.append(horarios_item)

        sala = Sala.from_dict(d.pop("sala"))

        vagas_ofertadas = d.pop("vagas_ofertadas")

        vagas_ocupadas = d.pop("vagas_ocupadas")

        turma = cls(
            disciplina_codigo=disciplina_codigo,
            disciplina_nome=disciplina_nome,
            numero=numero,
            ano_periodo=ano_periodo,
            professores=professores,
            horarios=horarios,
            sala=sala,
            vagas_ofertadas=vagas_ofertadas,
            vagas_ocupadas=vagas_ocupadas,
        )

        turma.additional_properties = d
        return turma

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
