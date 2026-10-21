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
  const [state, setState] = useState<{ path: string | null; data: T; error: string | null }>({
    path: null,
    data: mock,
    error: null,
  });

  useEffect(() => {
    let active = true;

    api
      .get<T>(path)
      .then((res) => {
        if (active) setState({ path, data: res.data, error: null });
      })
      .catch(() => {
        if (active) {
          setState((atual) => ({ path, data: atual.data, error: "Não foi possível conectar à API." }));
        }
      });

    return () => {
      active = false;
    };
  }, [path]);

  const loading = state.path !== path;
  return { data: state.data, loading, error: loading ? null : state.error };
}
