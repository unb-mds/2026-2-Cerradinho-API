"use client";

import { useApiResource } from "./useApiResource";
import type { Sala } from "./useSalas";

export interface BlocoAgenda {
  dia: string;
  inicio: string;
  fim: string;
  sala: Sala | null;
}

export interface TurmaAgenda {
  disciplina_codigo: string;
  disciplina_nome: string;
  numero: string;
  ano_periodo: string;
  horarios: BlocoAgenda[];
}

export interface Agenda {
  id: number;
  nome: string;
  turmas: TurmaAgenda[];
}

export function useAgendaProfessor(id: string) {
  const { data, loading, error } = useApiResource<Agenda | null>(`/professores/${id}/agenda`, null);
  return { agenda: data, loading, error };
}
