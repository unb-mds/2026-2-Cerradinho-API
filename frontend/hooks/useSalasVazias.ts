"use client";

import { predioDoGama } from "@/lib/campus";
import { useApiResource } from "./useApiResource";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import type { Sala } from "./useSalas";

export const HORARIOS = [
    "08:00", "08:55", "10:00", "10:55", "12:00", "12:55", "14:00",
    "14:55", "16:00", "16:55", "18:00", "19:00", "19:50", "20:50", "21:40",
];

export const DIAS_API = [null, "segunda", "terca", "quarta", "quinta", "sexta", "sabado"];

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

// Fora do horário de aula (intervalo, noite, domingo), a próxima aula que começa.
export function proximaAula(agora = new Date()): { dia: string; horario: string } {
    const minutos = agora.getHours() * 60 + agora.getMinutes();
    const hoje = DIAS_API[agora.getDay()];
    const maisTarde = HORARIOS.find((h) => minutosDoInicio(h) > minutos);
    if (hoje && maisTarde) return { dia: hoje, horario: maisTarde };

    // Hoje já acabou (ou é domingo): primeira aula do próximo dia letivo.
    for (let i = 1; i <= 7; i++) {
        const dia = DIAS_API[(agora.getDay() + i) % 7];
        if (dia) return { dia, horario: HORARIOS[0] };
    }
    return { dia: "segunda", horario: HORARIOS[0] };
}

export function linkSalasVazias(dia: string, horario: string) {
    return `/salas/vazias?dia=${dia}&horario=${horario}`;
}

// Dia e horário vêm da URL (?dia=quinta&horario=14:00), pra o link ser
// compartilhável e o card da home abrir no mesmo horário que contou. Sem
// parâmetro, abre na aula de agora - ou na próxima, fora do horário de aula.
// Usa useSearchParams: a página precisa envolver isto num <Suspense>.
export function useSalasVazias() {
    const params = useSearchParams();
    const router = useRouter();
    const pathname = usePathname();

    const agora = aulaAgora();
    const padrao = agora ?? proximaAula();
    const diaUrl = params.get("dia");
    const horarioUrl = params.get("horario");
    const dia = diaUrl && DIAS_API.includes(diaUrl) ? diaUrl : padrao.dia;
    const horario = horarioUrl && HORARIOS.includes(horarioUrl) ? horarioUrl : padrao.horario;

    const ir = (novoDia: string, novoHorario: string) =>
        router.replace(`${pathname}?dia=${novoDia}&horario=${novoHorario}`, { scroll: false });

    const { data, loading, error } = useApiResource<Sala[]>(caminhoSalasVazias(dia, horario), []);
    return {
        salas: data.filter((s) => predioDoGama(s.predio)),
        loading,
        error,
        dia,
        horario,
        // "agora" quando é a aula em andamento; "proxima" quando é o padrão fora do horário.
        momento: agora && agora.dia === dia && agora.horario === horario
            ? ("agora" as const)
            : !agora && padrao.dia === dia && padrao.horario === horario
                ? ("proxima" as const)
                : null,
        temAulaAgora: agora !== null,
        setDia: (novo: string) => ir(novo, horario),
        setHorario: (novo: string) => ir(dia, novo),
        voltarParaAgora: () => router.replace(pathname, { scroll: false }),
    };
}

// Home: salas livres na aula de agora (ou na próxima, fora do horário).
// `agora` vem do navegador; null enquanto a página não hidratou, e aí não busca nada.
export function useSalasLivresAgora(agora: Date | null) {
    const emAula = agora ? aulaAgora(agora) : null;
    const slot = agora ? (emAula ?? proximaAula(agora)) : null;
    const { data, loading, error } = useApiResource<Sala[]>(
        slot ? caminhoSalasVazias(slot.dia, slot.horario) : null, [],
    );

    return {
        salas: data.filter((s) => predioDoGama(s.predio)),
        slot,
        emAula: emAula !== null,
        href: slot ? linkSalasVazias(slot.dia, slot.horario) : "/salas/vazias",
        loading,
        error,
    };
}
