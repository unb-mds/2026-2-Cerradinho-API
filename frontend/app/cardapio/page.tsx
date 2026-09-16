"use client";

import { useCardapioSemana } from "@/hooks/useCardapioSemana";
import ApiStatus from "@/components/ApiStatus";

export default function CardapioPage() {
  const { cardapio, loading, error } = useCardapioSemana();

  return (
    <main className="mx-auto flex w-full max-w-3xl flex-1 flex-col gap-6 px-6 py-12">
      <div>
        <h1 className="text-2xl font-semibold text-zinc-900 dark:text-zinc-50">Cardápio do RU</h1>
        <p className="text-sm text-zinc-500 dark:text-zinc-400">Cardápio da semana atual.</p>
      </div>

      <ApiStatus loading={loading} error={error} />

      <ul className="flex flex-col gap-3">
        {cardapio.map((c) => (
          <li
            key={c.dia}
            className="rounded-lg border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900"
          >
            <div className="flex items-center justify-between gap-4">
              <span className="font-medium text-zinc-900 dark:text-zinc-50">{c.dia}</span>
              <span className="text-xs text-zinc-400">{c.refeicao}</span>
            </div>
            <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
              {c.pratoPrincipal} · Veg: {c.opcaoVegetariana} · {c.sobremesa}
            </p>
          </li>
        ))}
      </ul>
    </main>
  );
}
