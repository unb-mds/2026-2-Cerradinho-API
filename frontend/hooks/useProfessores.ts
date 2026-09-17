"use client";

import { useApiResource } from "./useApiResource";

export interface Professor {
  id: string;
  nome: string;
  titulo: string;
  departamento: string;
  disciplinas: string[];
}

const professoresMock: Professor[] = [
  { id: "1", nome: "Ana Souza", titulo: "Profa. Dra.", departamento: "FGA", disciplinas: ["FGA0071", "FGA0066"] },
  { id: "2", nome: "Carlos Lima", titulo: "Prof. Dr.", departamento: "CIC", disciplinas: ["CIC0004"] },
  { id: "3", nome: "Beatriz Alves", titulo: "Profa. Dra.", departamento: "CIC", disciplinas: ["CIC0097"] },
];

export function useProfessores() {
  const { data, loading, error } = useApiResource<Professor[]>("/professores", professoresMock);
  return { professores: data, loading, error };
}
