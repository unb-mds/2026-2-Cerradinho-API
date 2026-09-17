"use client";

import { useApiResource } from "./useApiResource";

export interface Sala {
  id: string;
  codigo: string;
  predio: string;
  tipo: string;
  capacidade: number;
}

const salasMock: Sala[] = [
  { id: "1", codigo: "BSA-T01", predio: "BSA Sul", tipo: "Sala de Aula", capacidade: 50 },
  { id: "2", codigo: "FGA-A1", predio: "UnB Gama", tipo: "Laboratório", capacidade: 40 },
  { id: "3", codigo: "ICC-Norte-101", predio: "ICC Norte", tipo: "Sala de Aula", capacidade: 60 },
];

export function useSalas() {
  const { data, loading, error } = useApiResource<Sala[]>("/salas", salasMock);
  return { salas: data, loading, error };
}
