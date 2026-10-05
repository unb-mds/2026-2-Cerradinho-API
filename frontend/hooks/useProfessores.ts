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

function mapProfessor(p: ProfessorAPI): Professor {
  const unidades = [... new Set(p.disciplinas.map((codigo) => codigo.replace(/\d.*$/, "")))];
  return { ...p, unidades };
}

export function useProfessores() {
  const { data, loading, error } = useApiResource<ProfessorAPI[]>("/professores", []);
  return { professores: data.map(mapProfessor), loading, error };
}
