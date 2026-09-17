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
    <nav className="border-b border-border bg-surface">
      <div className="mx-auto flex w-full max-w-3xl items-center gap-1 px-6">
        <Link href="/" className="mr-4 flex items-center gap-2 py-3">
          <span className="flex h-6 w-6 items-center justify-center rounded-md bg-brand text-xs font-bold text-brand-foreground">
            C
          </span>
          <span className="text-sm font-semibold text-foreground">Cerradinho</span>
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
                      ? "border-brand text-foreground"
                      : "border-transparent text-muted hover:text-foreground"
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
