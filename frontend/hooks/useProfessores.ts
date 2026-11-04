"use client";

import { useApiResource } from "./useApiResource";

interface ProfessorAPI {
  id: number;
  nome: string;
  disciplinas: string[];
}

export interface Professor {
  id: number;
  nome: string;
  unidades: string[];
  disciplinas: string[];
}

export function unidadesDasDisciplinas(codigos: string[]): string[] {
  return [...new Set(codigos.map((codigo) => codigo.replace(/\d.*$/, "")))];
}

function mapProfessor(p: ProfessorAPI): Professor {
  const unidades = unidadesDasDisciplinas(p.disciplinas);
  return { ...p, unidades };
}

export function useProfessores() {
  const { data, loading, error } = useApiResource<ProfessorAPI[]>("/professores", []);
  return { professores: data.map(mapProfessor), loading, error };
}
