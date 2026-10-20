"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

interface ResourceState<T> {
  data: T;
  loading: boolean;
  error: string | null;
}

/**
 * Busca `path` na API (`/v1`) e devolve { data, loading, error }.
 * Os componentes não chamam este hook direto: usam os hooks de domínio
 * (useDisciplinas, useProfessores etc.).
 * `mock` é o valor exibido enquanto a API não responde (nos hooks, uma lista vazia).
 */
export function useApiResource<T>(path: string, mock: T): ResourceState<T> {
  const [data, setData] = useState<T>(mock);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    api
      .get<T>(path)
      .then((res) => {
        if (active) setData(res.data);
      })
      .catch(() => {
        if (active) {
          setError("Não foi possível conectar à API.");
        }
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [path]);

  return { data, loading, error };
}
