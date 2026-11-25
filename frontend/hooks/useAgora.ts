"use client";

import { useSyncExternalStore } from "react";

// Hora do navegador, atualizada a cada minuto. No servidor (pré-renderização)
// devolve null: a hora do build não é a do aluno, e usar ela daria erro de
// hidratação. Quem usa mostra um estado de carregando enquanto vem null.
let atual: Date | null = null;

function lerAgora(): Date {
  const agora = Date.now();
  // Mesmo objeto dentro do mesmo minuto, senão o React re-renderiza sem parar.
  if (!atual || Math.floor(atual.getTime() / 60_000) !== Math.floor(agora / 60_000)) {
    atual = new Date(agora);
  }
  return atual;
}

function assinar(avisar: () => void) {
  const id = setInterval(avisar, 30_000);
  return () => clearInterval(id);
}

export function useAgora(): Date | null {
  return useSyncExternalStore(assinar, lerAgora, () => null);
}
