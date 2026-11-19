"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { CerradinhoFlower, ChevronRightIcon, CodeIcon } from "@/components/Icons";
import { MODULOS } from "@/components/modulos";

// Fora de "Módulos": não é um domínio de dados, é a documentação para quem integra
// com a API. No desktop fica no rodapé da sidebar; no celular, como último item da barra.
const DESENVOLVEDORES = {
  href: "/desenvolvedores",
  label: "Desenvolvedores",
  curto: "API",
  Icon: CodeIcon,
  viva: "text-sidebar-foreground-active",
  borda: "border-sidebar-foreground-active",
} as const;

const ITENS_CELULAR = [...MODULOS, DESENVOLVEDORES];

function estaAtivo(pathname: string, href: string) {
  return pathname === href || pathname.startsWith(`${href}/`);
}

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <>
      <aside className="sticky top-0 hidden h-screen w-55 shrink-0 flex-col self-start bg-sidebar pb-6 lg:flex">
        <Link href="/" className="flex items-center gap-2 px-5 pb-8 pt-6">
          <CerradinhoFlower className="h-14 w-14 shrink-0" aria-hidden />
          <span className="flex flex-col">
            <span className="text-lg font-semibold leading-tight tracking-tight text-sidebar-foreground-active">
              Cerradinho
            </span>
            <span className="text-[11px] text-sidebar-foreground">UnB · Campus Gama</span>
          </span>
        </Link>

        <div className="mx-6 mb-5 h-px bg-white/10" />

        <span className="px-6 pb-3 text-[10px] font-semibold uppercase tracking-widest text-sidebar-foreground">
          Módulos
        </span>

        <nav className="flex-1 overflow-y-auto">
          {MODULOS.map(({ href, label, Icon, viva, borda }) => {
            const active = estaAtivo(pathname, href);
            return (
              <Link
                key={href}
                href={href}
                aria-current={active ? "page" : undefined}
                className={`flex items-center gap-3 border-l-[3px] px-6 py-2.5 text-sm transition-colors ${
                  active
                    ? `${borda} bg-sidebar-active font-semibold text-sidebar-foreground-active`
                    : "border-transparent text-sidebar-foreground hover:text-sidebar-foreground-active"
                }`}
              >
                <Icon className={`h-4.5 w-4.5 ${viva}`} />
                {label}
                {active && <ChevronRightIcon className="ml-auto h-3.5 w-3.5 opacity-50" />}
              </Link>
            );
          })}
        </nav>

        <div className="mx-6 mb-3 h-px bg-white/10" />
        <Link
          href={DESENVOLVEDORES.href}
          aria-current={estaAtivo(pathname, DESENVOLVEDORES.href) ? "page" : undefined}
          className={`flex items-center gap-3 border-l-[3px] px-6 py-2.5 transition-colors ${
            estaAtivo(pathname, DESENVOLVEDORES.href)
              ? "border-accent bg-sidebar-active text-sidebar-foreground-active"
              : "border-transparent text-sidebar-foreground hover:text-sidebar-foreground-active"
          }`}
        >
          <CodeIcon className="h-4.5 w-4.5 shrink-0" />
          <span className="flex flex-col">
            <span className="text-sm font-semibold">Desenvolvedores</span>
            <span className="text-[10px] uppercase tracking-wide opacity-70">Documentação da API</span>
          </span>
        </Link>
      </aside>

      {/* Celular e tablet: barra fixa embaixo no lugar da sidebar. */}
      <nav className="fixed inset-x-0 bottom-0 z-40 flex border-t border-white/10 bg-sidebar pb-[env(safe-area-inset-bottom)] lg:hidden">
        {ITENS_CELULAR.map(({ href, curto, Icon, viva, borda }) => {
          const active = estaAtivo(pathname, href);
          return (
            <Link
              key={href}
              href={href}
              aria-current={active ? "page" : undefined}
              className={`flex h-16 min-w-0 flex-1 flex-col items-center justify-center gap-1 border-t-2 text-[10px] transition-colors ${
                active
                  ? `${borda} font-semibold text-sidebar-foreground-active`
                  : "border-transparent text-sidebar-foreground"
              }`}
            >
              <Icon className={`h-5 w-5 ${viva}`} />
              <span className="max-w-full truncate px-0.5">{curto}</span>
            </Link>
          );
        })}
      </nav>
    </>
  );
}
