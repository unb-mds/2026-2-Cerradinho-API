import Link from "next/link";
import { ChevronRightIcon, GridIcon } from "@/components/Icons";
import type { ReactNode } from "react";
import ChamadaApi from "@/components/ChamadaApi";
import { modulo, type Modulo } from "@/components/modulos";

interface PageHeaderProps {
  title: string;
  sub: ReactNode;
  // Módulo da página: o topo vira uma faixa na cor do cerrado dele.
  href?: Modulo["href"];
  // A chamada da API que preenche a página; aparece logo abaixo da faixa.
  api?: { caminho: string; nota?: string };
}

export default function PageHeader({ title, sub, href, api }: PageHeaderProps) {
  const m = href ? modulo(href) : null;
  return (
    <div>
      <div className={m ? `${m.faixa} ${m.faixaTexto}` : "text-foreground"}>
        <div className="px-4 pb-6 pt-5 lg:px-10 lg:pb-7 lg:pt-6">
          <div className="mb-4 flex items-center gap-1.5 text-[13px]">
            <Link href="/" className="flex items-center gap-1 opacity-90 transition-opacity hover:opacity-100 hover:underline">
              <GridIcon className="h-3.5 w-3.5" /> Visão Geral
            </Link>
            <ChevronRightIcon className="h-3 w-3 opacity-70" />
            <span className="font-semibold">{title}</span>
          </div>
          <div className="flex items-center gap-3.5">
            {m && <m.Icon className="h-9 w-9 shrink-0" />}
            <div>
              <h1 className="text-2xl font-bold tracking-tight md:text-3xl">{title}</h1>
              <p className="mt-0.5 flex flex-wrap items-center gap-x-1.5 text-sm">{sub}</p>
            </div>
          </div>
        </div>
      </div>
      {api && (
        <div className="px-4 lg:px-10">
          <ChamadaApi caminho={api.caminho} nota={api.nota} />
        </div>
      )}
    </div>
  );
}
