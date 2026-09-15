"use client";

import { useProfessores } from "@/hooks/useProfessores";
import ApiStatus from "@/components/ApiStatus";

export default function ProfessoresPage() {
  const { professores, loading, error } = useProfessores();

  return (
    <main className="mx-auto flex w-full max-w-3xl flex-1 flex-col gap-6 px-6 py-12">
      <div>
        <h1 className="text-2xl font-semibold text-zinc-900 dark:text-zinc-50">Professores</h1>
        <p className="text-sm text-zinc-500 dark:text-zinc-400">Professores e as disciplinas que lecionam.</p>
      </div>

      <ApiStatus loading={loading} error={error} />

      <ul className="flex flex-col gap-3">
        {professores.map((p) => (
          <li
            key={p.id}
            className="rounded-lg border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900"
          >
            <div className="flex items-center justify-between gap-4">
              <span className="font-medium text-zinc-900 dark:text-zinc-50">{p.nome}</span>
              <span className="text-xs text-zinc-400">{p.departamento}</span>
            </div>
            <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
              Disciplinas: {p.disciplinas.join(", ")}
            </p>
          </li>
        ))}
      </ul>
    </main>
  );
}
