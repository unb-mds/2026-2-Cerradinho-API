"use client";

import Link from "next/link";
import { useState } from "react";
import { API_URL } from "@/lib/api";

// O site é uma das aplicações feitas sobre a API: cada tela mostra a chamada
// que a preencheu, com os filtros atuais, pra quem quiser fazer a mesma coisa.
const PREFIXO = new URL(API_URL).pathname.replace(/\/$/, ""); // "/v1"

interface ChamadaApiProps {
  caminho: string; // como o hook chama a API, ex.: "/salas/vazias?dia=quinta&horario=14:55"
  nota?: string;
}

export default function ChamadaApi({ caminho, nota }: ChamadaApiProps) {
  const [copiado, setCopiado] = useState(false);
  const url = `${API_URL}${caminho}`;

  async function copiar() {
    try {
      await navigator.clipboard.writeText(url);
      setCopiado(true);
      setTimeout(() => setCopiado(false), 1500);
    } catch {
      // clipboard bloqueado (http sem permissão): o link "Ver JSON" ainda leva à URL
    }
  }

  const acao =
    "rounded-md px-2 py-1 text-xs font-semibold text-sidebar-foreground transition-colors hover:bg-white/10 hover:text-sidebar-foreground-active";

  return (
    <div className="mt-4 flex flex-col gap-1.5">
      <div className="flex w-fit max-w-full flex-wrap items-center gap-x-3 gap-y-1 rounded-lg border border-white/5 bg-sidebar py-1.5 pl-2 pr-1.5">
        <div className="flex min-w-0 items-center gap-2">
          <span className="rounded bg-sidebar-active px-1.5 py-0.5 font-mono text-[11px] font-semibold text-sidebar-foreground">
            GET
          </span>
          <code className="min-w-0 break-all font-mono text-xs text-sidebar-foreground-active">
            {PREFIXO}
            {caminho}
          </code>
        </div>
        <div className="flex items-center">
          <button type="button" onClick={copiar} className={acao} aria-label="Copiar a URL desta chamada">
            {copiado ? "Copiado" : "Copiar"}
          </button>
          <a href={url} target="_blank" rel="noreferrer" className={acao}>
            Ver JSON
          </a>
          <Link href="/desenvolvedores#endpoints" className={acao}>
            Docs
          </Link>
        </div>
      </div>
      {nota && <p className="text-xs text-muted">{nota}</p>}
    </div>
  );
}
