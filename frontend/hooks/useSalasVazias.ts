"use client";

import { useApiResource } from "./useApiResource";
import { useState } from "react";
import type { Sala } from "./useSalas";

export const HORARIOS = [
    "08:00", "08:55", "10:00", "10:55", "12:00", "12:55", "14:00",
    "14:55", "16:00", "16:55", "18:00", "19:00", "19:50", "20:50", "21:40",
];

const DIAS_API = [null, "segunda", "terca", "quarta", "quinta", "sexta", "sabado"];

function caminhoSalasVazias(dia: string, horario: string) {
    return `/salas/vazias?dia=${dia}&horario=${horario}`;
}

export function minutosDoInicio(horario: string) {
    const [hora, min] = horario.split(":").map(Number);
    return hora * 60 + min;
}

export function aulaAgora(agora = new Date()): { dia: string; horario: string } | null {
    const dia = DIAS_API[agora.getDay()];
    if (!dia) return null;

    const minutos = agora.getHours() * 60 + agora.getMinutes();
    const horario = HORARIOS.filter((h) => minutosDoInicio(h) <= minutos).pop();
    if (!horario || minutos >= minutosDoInicio(horario) + 55) return null;

    return { dia, horario };
}

export function useSalasVazias() {
    const [dia, setDia] = useState("segunda");
    const [horario, setHorario] = useState("08:00");

    const { data, loading, error } = useApiResource<Sala[]>(caminhoSalasVazias(dia, horario), []);
    return { salas: data, loading, error, dia, horario, setDia, setHorario };
}

export function useSalasVaziasAgora() {
    const agora = aulaAgora();
    const { data, loading, error } = useApiResource<Sala[]>(
        caminhoSalasVazias(agora?.dia ?? "segunda", agora?.horario ?? "08:00"), [],
    );

    return { quantidade: data.length, horario: agora?.horario ?? null, foraDoHorario: agora === null, loading, error };
}
