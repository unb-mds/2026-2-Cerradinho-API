"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/disciplinas", label: "Disciplinas" },
  { href: "/cardapio", label: "Cardápio" },
  { href: "/professores", label: "Professores" },
  { href: "/salas", label: "Salas" },
];

export default function Nav() {
  const pathname = usePathname();

  return (
    <nav className="border-b border-zinc-200 bg-white dark:border-zinc-800 dark:bg-black">
      <div className="mx-auto flex w-full max-w-3xl items-center gap-1 px-6">
        <Link
          href="/"
          className="mr-4 py-3 text-sm font-semibold text-zinc-900 dark:text-zinc-50"
        >
          Cerradinho
        </Link>
        <ul className="flex gap-1">
          {links.map(({ href, label }) => {
            const active = pathname === href;
            return (
              <li key={href}>
                <Link
                  href={href}
                  className={`inline-block border-b-2 px-3 py-3 text-sm font-medium transition-colors ${
                    active
                      ? "border-zinc-900 text-zinc-900 dark:border-zinc-50 dark:text-zinc-50"
                      : "border-transparent text-zinc-500 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-50"
                  }`}
                >
                  {label}
                </Link>
              </li>
            );
          })}
        </ul>
      </div>
    </nav>
  );
}
