"use client";

import { useApiResource } from "./useApiResource";

export interface Disciplina {
  codigo: string;
  nome: string;
  turma: string;
  horario: string;
  vagas: number;
}

const disciplinasMock: Disciplina[] = [
  { codigo: "CIC0004", nome: "Algoritmos e Programação", turma: "A", horario: "14:00–16:00", vagas: 40 },
  { codigo: "CIC0097", nome: "Organização de Computadores", turma: "B", horario: "10:00–12:00", vagas: 35 },
  { codigo: "FGA0071", nome: "Prática de Eletrônica Digital 1", turma: "A", horario: "08:00–10:00", vagas: 20 },
];

export function useDisciplinas() {
  const { data, loading, error } = useApiResource<Disciplina[]>("/disciplinas", disciplinasMock);
  return { disciplinas: data, loading, error };
}
