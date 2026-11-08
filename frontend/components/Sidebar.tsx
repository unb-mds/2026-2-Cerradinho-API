"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BookIcon,
  BowlIcon,
  CerradinhoFlower,
  ChevronRightIcon,
  CodeIcon,
  DoorOpenIcon,
  UserIcon,
} from "@/components/Icons";

// `curto` é o rótulo da barra inferior do celular, onde cada item tem ~1/5 da largura.
const NAV_ITEMS = [
  { href: "/disciplinas", label: "Disciplinas", curto: "Disciplinas", Icon: BookIcon },
  { href: "/cardapio", label: "Cardápio", curto: "Cardápio", Icon: BowlIcon },
  { href: "/professores", label: "Professores", curto: "Professores", Icon: UserIcon },
  { href: "/salas/vazias", label: "Salas Vazias", curto: "Salas", Icon: DoorOpenIcon },
  { href: "/desenvolvedores", label: "Desenvolvedores", curto: "API", Icon: CodeIcon },
] as const;

function estaAtivo(pathname: string, href: string) {
  return pathname === href || pathname.startsWith(`${href}/`);
}

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <>
      <aside className="hidden min-h-screen w-55 shrink-0 flex-col bg-sidebar pb-6 md:flex">
        <Link href="/" className="flex flex-col gap-1 px-6 pb-8 pt-7">
          <span className="flex items-center gap-2.5">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand">
              <CerradinhoFlower className="h-9 w-9" />
            </span>
            <span className="font-semibold tracking-tight text-sidebar-foreground-active">
              Cerradinho
            </span>
          </span>
          <span className="pl-10.5 text-[10px] uppercase tracking-wide text-sidebar-foreground">
            UnB · Dados do Campus
          </span>
        </Link>

        <div className="mx-6 mb-5 h-px bg-white/10" />

        <span className="px-6 pb-3 text-[10px] font-semibold uppercase tracking-widest text-sidebar-foreground">
          Módulos
        </span>

        <nav className="flex-1">
          {NAV_ITEMS.map(({ href, label, Icon }) => {
            const active = estaAtivo(pathname, href);
            return (
              <Link
                key={href}
                href={href}
                className={`flex items-center gap-3 border-l-[3px] px-6 py-2.5 text-sm transition-colors ${
                  active
                    ? "border-accent bg-sidebar-active font-semibold text-sidebar-foreground-active"
                    : "border-transparent text-sidebar-foreground hover:text-sidebar-foreground-active"
                }`}
              >
                <Icon className="h-4.5 w-4.5" />
                {label}
                {active && <ChevronRightIcon className="ml-auto h-3.5 w-3.5 opacity-50" />}
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Celular: barra fixa embaixo no lugar da sidebar. */}
      <nav className="fixed inset-x-0 bottom-0 z-40 flex border-t border-white/10 bg-sidebar pb-[env(safe-area-inset-bottom)] md:hidden">
        {NAV_ITEMS.map(({ href, curto, Icon }) => {
          const active = estaAtivo(pathname, href);
          return (
            <Link
              key={href}
              href={href}
              aria-current={active ? "page" : undefined}
              className={`flex h-16 min-w-0 flex-1 flex-col items-center justify-center gap-1 border-t-2 text-[10px] transition-colors ${
                active
                  ? "border-accent font-semibold text-sidebar-foreground-active"
                  : "border-transparent text-sidebar-foreground"
              }`}
            >
              <Icon className="h-5 w-5" />
              <span className="max-w-full truncate px-0.5">{curto}</span>
            </Link>
          );
        })}
      </nav>
    </>
  );
}
