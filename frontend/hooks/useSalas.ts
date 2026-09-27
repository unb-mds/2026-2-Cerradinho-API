"use client";

import { useApiResource } from "./useApiResource";

export interface Sala {
  id: number;
  nome: string;
  predio: string;
}

export function useSalas() {
  const { data, loading, error } = useApiResource<Sala[]>("/salas", []);
  return { salas: data, loading, error };
}
