"use client";

import { useApiResource } from "./useApiResource";
import { useState } from "react";
import type { Sala } from "./useSalas";

// blocos de duas aulas das 8h as 17h50
export const HORARIOS = ["08:00", "10:00", "12:00", "14:00", "16:00"];
const DURACAO_BLOCO = 110;

const DIAS_API = [null, "segunda", "terca", "quarta", "quinta", "sexta", "sabado"];

// so as salas i1 a i10 e s1 a s10 do campus gama aparecem no site
const PREDIOS_DO_CAMPUS = ["FCTE", "FGA"];
const SALA_DE_AULA = /^[IS]([1-9]|10)$/;

export function doCampus(salas: Sala[]): Sala[] {
    return salas
        .filter((sala) => PREDIOS_DO_CAMPUS.includes(sala.predio.trim().toUpperCase()))
        .filter((sala) => SALA_DE_AULA.test(sala.nome.trim().toUpperCase()))
        .sort((a, b) => a.nome.localeCompare(b.nome, "pt-BR", { numeric: true }));
}

export function minutosDoInicio(horario: string) {
    const [hora, min] = horario.split(":").map(Number);
    return hora * 60 + min;
}

export function fimDoBloco(horario: string) {
    const fim = minutosDoInicio(horario) + DURACAO_BLOCO;
    return `${String(Math.floor(fim / 60)).padStart(2, "0")}:${String(fim % 60).padStart(2, "0")}`;
}

function caminhoSalasVazias(dia: string, horario: string) {
    return `/salas/vazias?dia=${dia}&horario=${horario}&fim=${fimDoBloco(horario)}`;
}

export function aulaAgora(agora = new Date()): { dia: string; horario: string } | null {
    const dia = DIAS_API[agora.getDay()];
    if (!dia) return null;

    const minutos = agora.getHours() * 60 + agora.getMinutes();
    const horario = HORARIOS.filter((h) => minutosDoInicio(h) <= minutos).pop();
    if (!horario || minutos >= minutosDoInicio(horario) + DURACAO_BLOCO) return null;

    return { dia, horario };
}

export const DIAS_DA_SEMANA = [
    { dia: "segunda", rotulo: "Segunda" },
    { dia: "terca", rotulo: "Terça" },
    { dia: "quarta", rotulo: "Quarta" },
    { dia: "quinta", rotulo: "Quinta" },
    { dia: "sexta", rotulo: "Sexta" },
    { dia: "sabado", rotulo: "Sábado" },
];

// uma chamada por dia pra mostrar a semana inteira no bloco escolhido
export function useSalasVazias() {
    const [horario, setHorario] = useState("08:00");

    const segunda = useApiResource<Sala[]>(caminhoSalasVazias("segunda", horario), []);
    const terca = useApiResource<Sala[]>(caminhoSalasVazias("terca", horario), []);
    const quarta = useApiResource<Sala[]>(caminhoSalasVazias("quarta", horario), []);
    const quinta = useApiResource<Sala[]>(caminhoSalasVazias("quinta", horario), []);
    const sexta = useApiResource<Sala[]>(caminhoSalasVazias("sexta", horario), []);
    const sabado = useApiResource<Sala[]>(caminhoSalasVazias("sabado", horario), []);
    const respostas = [segunda, terca, quarta, quinta, sexta, sabado];

    const dias = DIAS_DA_SEMANA.map(({ dia, rotulo }, i) => ({ dia, rotulo, salas: doCampus(respostas[i].data) }));
    const loading = respostas.some((r) => r.loading);
    const error = respostas.find((r) => r.error)?.error ?? null;
    return { dias, loading, error, horario, setHorario, hoje: DIAS_API[new Date().getDay()] };
}

export function useSalasVaziasAgora() {
    const agora = aulaAgora();
    const { data, loading, error } = useApiResource<Sala[]>(
        caminhoSalasVazias(agora?.dia ?? "segunda", agora?.horario ?? "08:00"), [],
    );

    return { quantidade: doCampus(data).length, horario: agora?.horario ?? null, foraDoHorario: agora === null, loading, error };
}
