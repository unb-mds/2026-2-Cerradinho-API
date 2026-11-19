import Link from "next/link";
import { ChevronRightIcon, GridIcon } from "@/components/Icons";
import type { ReactNode } from "react";
import ChamadaApi from "@/components/ChamadaApi";
import { modulo, type Modulo } from "@/components/modulos";

interface PageHeaderProps {
  title: string;
  sub: ReactNode;
  // Módulo da página: dá o ícone e a cor do cerrado ao lado do título.
  href?: Modulo["href"];
  // A chamada da API que preenche a página; aparece logo abaixo do título.
  api?: { caminho: string; nota?: string };
}

export default function PageHeader({ title, sub, href, api }: PageHeaderProps) {
  const m = href ? modulo(href) : null;
  return (
    <div className="px-4 lg:px-10 pt-8">
      <div className="mb-3 flex items-center gap-1.5 text-[13px]">
        <Link href="/" className="flex items-center gap-1 text-muted transition-colors hover:text-foreground">
          <GridIcon className="h-3.5 w-3.5" /> Visão Geral
        </Link>
        <ChevronRightIcon className="h-3 w-3 text-muted" />
        <span className="font-semibold text-foreground">{title}</span>
      </div>
      <div className="flex items-center gap-3">
        {m && (
          <span className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${m.fundo}`}>
            <m.Icon className={`h-5 w-5 ${m.cor}`} />
          </span>
        )}
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">{title}</h1>
          <p className="mt-0.5 flex flex-wrap items-center gap-x-1.5 text-sm text-muted">{sub}</p>
        </div>
      </div>
      {api && <ChamadaApi caminho={api.caminho} nota={api.nota} />}
    </div>
  );
}
