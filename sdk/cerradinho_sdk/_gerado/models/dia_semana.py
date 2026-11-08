from enum import StrEnum


class DiaSemana(StrEnum):
    DOMINGO = "domingo"
    QUARTA = "quarta"
    QUINTA = "quinta"
    SABADO = "sabado"
    SEGUNDA = "segunda"
    SEXTA = "sexta"
    TERCA = "terca"

    def __str__(self) -> str:
        return str(self.value)
