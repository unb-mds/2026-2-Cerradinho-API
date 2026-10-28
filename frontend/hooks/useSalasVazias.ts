"use client";

import { useApiResource } from "./useApiResource";
import { useState } from "react";
import type { Sala } from "./useSalas";

export function useSalasVazias() {
    const [dia, setDia] = useState("segunda");
    const [horario, setHorario] = useState("08:00");

    const { data, loading, error } = useApiResource<Sala[]>(
        `/salas/vazias?dia=${dia}&horario=${horario}`,
        [],
    );
    return { salas: data, loading, error, dia, horario, setDia, setHorario };
}
