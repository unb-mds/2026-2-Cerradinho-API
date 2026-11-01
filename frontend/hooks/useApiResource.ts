"use client";

import { isAxiosError } from "axios";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

interface ResourceState<T> {
  data: T;
  loading: boolean;
  error: string | null;
  status: number | null;
}

/**
 * Busca `path` na API (`/v1`) e devolve { data, loading, error, status }.
 * `status` é o código HTTP da falha, ou null se não houve resposta da API.
 * Os componentes não chamam este hook direto: usam os hooks de domínio
 * (useDisciplinas, useProfessores etc.).
 * `mock` é o valor exibido enquanto a API não responde (nos hooks, uma lista vazia).
 */
export function useApiResource<T>(path: string, mock: T): ResourceState<T> {
  const [state, setState] = useState<{ path: string | null; data: T; error: string | null; status: number | null }>({
    path: null,
    data: mock,
    error: null,
    status: null,
  });

  useEffect(() => {
    let active = true;

    api
      .get<T>(path)
      .then((res) => {
        if (active) setState({ path, data: res.data, error: null, status: null });
      })
      .catch((erro: unknown) => {
        if (active) {
          const status = isAxiosError(erro) ? (erro.response?.status ?? null) : null;
          setState((atual) => ({ ...atual, path, error: "Não foi possível conectar à API.", status }));
        }
      });

    return () => {
      active = false;
    };
  }, [path]);

  // Enquanto carrega um path novo, ou se ele falhou, não mostra o dado do path anterior.
  const loading = state.path !== path;
  const error = loading ? null : state.error;
  const status = loading ? null : state.status;
  return { data: loading || error ? mock : state.data, loading, error, status };
}
