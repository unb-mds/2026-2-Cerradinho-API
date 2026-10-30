"use client";

import { useApiResource } from "./useApiResource";
import { useState } from "react";
import type { Sala } from "./useSalas";

// A grade noturna do backend (domain/salas.py) não bate com o SIGAA: N1, N2 e N3
// começam às 19:00, 19:50 e 20:50, mas ele as conhece como 18:55, 20:00 e 20:55.
// Remover este mapa quando a grade for corrigida lá.
const HORARIO_NO_BACKEND: Record<string, string> = {
    "19:00": "18:55",
    "19:50": "20:00",
    "20:50": "20:55",
};

export function useSalasVazias() {
    const [dia, setDia] = useState("segunda");
    const [horario, setHorario] = useState("08:00");

    const { data, loading, error } = useApiResource<Sala[]>(
        `/salas/vazias?dia=${dia}&horario=${HORARIO_NO_BACKEND[horario] ?? horario}`,
        [],
    );
    return { salas: data, loading, error, dia, horario, setDia, setHorario };
}
