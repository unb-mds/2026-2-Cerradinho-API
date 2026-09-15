"use client";

import { useApiResource } from "./useApiResource";

export interface Sala {
  id: string;
  codigo: string;
  predio: string;
  capacidade: number;
}

const salasMock: Sala[] = [
  { id: "1", codigo: "BSA-T01", predio: "BSA Sul", capacidade: 50 },
  { id: "2", codigo: "FGA-A1", predio: "UnB Gama", capacidade: 40 },
  { id: "3", codigo: "ICC-Norte-101", predio: "ICC Norte", capacidade: 60 },
];

export function useSalas() {
  const { data, loading, error } = useApiResource<Sala[]>("/salas", salasMock);
  return { salas: data, loading, error };
}
