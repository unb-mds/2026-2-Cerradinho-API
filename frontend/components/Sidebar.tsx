"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BookIcon,
  BowlIcon,
  BuildingIcon,
  ChevronRightIcon,
  UserIcon,
} from "@/components/Icons";

const NAV_ITEMS = [
  { href: "/disciplinas", label: "Disciplinas", Icon: BookIcon },
  { href: "/cardapio", label: "Cardápio", Icon: BowlIcon },
  { href: "/professores", label: "Professores", Icon: UserIcon },
  { href: "/salas", label: "Salas", Icon: BuildingIcon },
] as const;

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex min-h-screen w-[220px] flex-shrink-0 flex-col bg-sidebar pb-6">
      <Link href="/" className="flex flex-col gap-1 px-6 pb-8 pt-7">
        <span className="flex items-center gap-2.5">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#C8D3A8" strokeWidth="2" strokeLinecap="round">
              <circle cx="12" cy="12" r="3" />
              <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
            </svg>
          </span>
          <span className="font-semibold tracking-tight text-sidebar-foreground-active">
            Cerradinho
          </span>
        </span>
        <span className="pl-[42px] text-[10px] uppercase tracking-wide text-sidebar-foreground">
          UnB · Dados do Campus
        </span>
      </Link>

      <div className="mx-6 mb-5 h-px bg-white/10" />

      <span className="px-6 pb-3 text-[10px] font-semibold uppercase tracking-widest text-sidebar-foreground">
        Módulos
      </span>

      <nav className="flex-1">
        {NAV_ITEMS.map(({ href, label, Icon }) => {
          const active = pathname === href;
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
              <Icon className="h-[18px] w-[18px]" />
              {label}
              {active && <ChevronRightIcon className="ml-auto h-3.5 w-3.5 opacity-50" />}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
