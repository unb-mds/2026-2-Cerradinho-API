"use client";

import { useApiResource } from "./useApiResource";

export interface Professor {
  id: string;
  nome: string;
  departamento: string;
  disciplinas: string[];
}

const professoresMock: Professor[] = [
  { id: "1", nome: "Ana Souza", departamento: "FGA", disciplinas: ["FGA0071", "FGA0066"] },
  { id: "2", nome: "Carlos Lima", departamento: "CIC", disciplinas: ["CIC0004"] },
  { id: "3", nome: "Beatriz Alves", departamento: "CIC", disciplinas: ["CIC0097"] },
];

export function useProfessores() {
  const { data, loading, error } = useApiResource<Professor[]>("/professores", professoresMock);
  return { professores: data, loading, error };
}
