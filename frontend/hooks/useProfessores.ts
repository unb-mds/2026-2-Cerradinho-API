"use client";

import { disciplinaDoGama } from "@/lib/campus";
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
  // Só o campus Gama: docentes com alguma disciplina da FCTE.
  const doGama = data.filter((p) => p.disciplinas.some(disciplinaDoGama));
  return { professores: doGama.map(mapProfessor), loading, error };
}
