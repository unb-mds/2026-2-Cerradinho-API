"use client";

import { predioDoGama } from "@/lib/campus";
import { useApiResource } from "./useApiResource";

export interface Sala {
  id: number;
  nome: string;
  predio: string;
}

export function useSalas() {
  const { data, loading, error } = useApiResource<Sala[]>("/salas", []);
  return { salas: data.filter((s) => predioDoGama(s.predio)), loading, error };
}
