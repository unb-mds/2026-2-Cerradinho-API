"use client";

import { isAxiosError } from "axios";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

// Duas telas (ou dois hooks na mesma tela) pedindo o mesmo path ao mesmo tempo
// compartilham uma requisição só - a home e Professores pedem /disciplinas, que
// é grande, por dois hooks. Só junta pedidos em andamento; nada fica em cache.
const emAndamento = new Map<string, Promise<unknown>>();

function buscar<T>(path: string): Promise<T> {
  let pedido = emAndamento.get(path);
  if (!pedido) {
    pedido = api.get<T>(path).then((res) => res.data).finally(() => emAndamento.delete(path));
    emAndamento.set(path, pedido);
  }
  return pedido as Promise<T>;
}

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
 * `path` null não busca nada e fica em loading (ex.: esperando a hora do navegador).
 */
export function useApiResource<T>(path: string | null, mock: T): ResourceState<T> {
  const [state, setState] = useState<{ path: string | null; data: T; error: string | null; status: number | null }>({
    path: null,
    data: mock,
    error: null,
    status: null,
  });

  useEffect(() => {
    if (path === null) return;
    let active = true;

    buscar<T>(path)
      .then((data) => {
        if (active) setState({ path, data, error: null, status: null });
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
  const loading = path === null || state.path !== path;
  const error = loading ? null : state.error;
  const status = loading ? null : state.status;
  return { data: loading || error ? mock : state.data, loading, error, status };
}
