import Link from "next/link";

const screens = [
  { href: "/disciplinas", label: "Disciplinas", description: "Turmas, horários e vagas ofertadas no semestre." },
  { href: "/cardapio", label: "Cardápio do RU", description: "Cardápio semanal do Restaurante Universitário." },
  { href: "/professores", label: "Professores", description: "Professores e as disciplinas que lecionam." },
  { href: "/salas", label: "Salas", description: "Salas de aula, prédios e capacidade." },
];

export default function Home() {
  return (
    <main className="mx-auto flex w-full max-w-3xl flex-1 flex-col gap-8 px-6 py-16">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-semibold text-zinc-900 dark:text-zinc-50">Cerradinho</h1>
        <p className="max-w-xl text-zinc-600 dark:text-zinc-400">
          API aberta que consolida dados institucionais da UnB — disciplinas, professores, salas e cardápio do
          RU hoje espalhados em vários sistemas.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {screens.map((s) => (
          <Link
            key={s.href}
            href={s.href}
            className="rounded-lg border border-zinc-200 bg-white p-4 shadow-sm transition-colors hover:border-zinc-400 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-zinc-600"
          >
            <span className="font-medium text-zinc-900 dark:text-zinc-50">{s.label}</span>
            <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">{s.description}</p>
          </Link>
        ))}
      </div>
    </main>
  );
}
