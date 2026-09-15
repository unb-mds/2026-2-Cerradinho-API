"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

interface ResourceState<T> {
  data: T;
  loading: boolean;
  error: string | null;
}

/**
 * Internal helper shared by the domain hooks below — components should
 * never call this directly, only useDisciplinas/useCardapioSemana/etc.
 * Starts from `mock` so screens render immediately, then swaps in the
 * real API response once it arrives (or reports an error and keeps the mock).
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
          setError("Não foi possível conectar à API. Exibindo dados de exemplo.");
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
