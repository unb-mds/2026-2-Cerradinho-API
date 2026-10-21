"use client";

import { useState } from "react";
import { useCardapioSemana, somarDias, hojeISO, nomeDoDia } from "@/hooks/useCardapioSemana";
import ApiStatus from "@/components/ApiStatus";
import PageHeader from "@/components/PageHeader";
import { FilterBar, FilterPills } from "@/components/Filters";
import Badge from "@/components/Badge";

function formatarData(data: string): string {
  const [, mes, dia] = data.split("-");
  return `${dia}/${mes}`;
}

const DIAS_DA_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"];

export default function CardapioPage() {
  const { cardapio, loading, error, inicio, ehSemanaAtual, semanaAnterior, proximaSemana, semanaAtual } =
    useCardapioSemana();
  const [dia, setDia] = useState<string | null>(null);

  const nomeHoje = nomeDoDia(hojeISO());
  const dias = ["Todos", ...DIAS_DA_SEMANA];
  const diaAtivo = dia ?? (ehSemanaAtual ? nomeHoje : "Todos");
  const filtrado = diaAtivo === "Todos" ? cardapio : cardapio.filter((c) => c.dia === diaAtivo);

  return (
    <main className="flex flex-1 flex-col pb-10">
      <PageHeader title="Cardápio" sub="Cardápio da semana · Restaurante Universitário" />

      <div className="px-10 pt-4">
        <ApiStatus loading={loading} error={error} />
      </div>

      <div className="flex items-center gap-3 px-10 pt-4">
        <button type="button" onClick={() => { setDia(null); semanaAnterior(); }} className="rounded-lg border border-border bg-surface px-3 py-1.5 text-sm text-foreground hover:bg-background">
          ← Anterior
        </button>
        <span className="text-sm font-medium text-foreground">
          {formatarData(inicio)} a {formatarData(somarDias(inicio, 6))}
        </span>
        <button type="button" onClick={() => { setDia(null); proximaSemana(); }} className="rounded-lg border border-border bg-surface px-3 py-1.5 text-sm text-foreground hover:bg-background">
          Próxima →
        </button>
        <button type="button" onClick={() => { setDia(null); semanaAtual(); }} className="rounded-lg border border-border bg-surface px-3 py-1.5 text-sm text-foreground hover:bg-background">
          Hoje
        </button>

      </div>
      <FilterBar hasFilters={diaAtivo !== "Todos"} onClear={() => setDia("Todos")}>
        <FilterPills label="Dia" value={diaAtivo} onChange={setDia} options={dias} />
      </FilterBar>

      <div className="flex flex-col gap-4 px-10 pt-5">
        {!loading && !error && filtrado.length === 0 && (
          <p className="rounded-xl border border-border bg-surface px-6 py-12 text-center text-sm text-muted">
            {diaAtivo === "Todos"
              ? "Nenhum cardápio publicado para essa semana."
              : `Sem cardápio publicado para ${diaAtivo}, ${formatarData(somarDias(inicio, DIAS_DA_SEMANA.indexOf(diaAtivo)))}.`}
          </p>
        )}
        {filtrado.map((c) => (
          <div key={`${c.data}-${c.refeicao}`} className="overflow-hidden rounded-xl border border-border bg-surface">
            <div className="flex items-center gap-3 bg-background px-6 py-4">
              <div className="font-bold text-foreground">{c.dia}, {formatarData(c.data)}</div>
              {c.data === hojeISO() && <Badge>Hoje</Badge>}
              <Badge>{c.refeicao}</Badge>
            </div>
            <ul className="divide-y divide-border">
              {c.itens.map((item, i) => (
                <li key={`${item.categoria}-${i}`} className="grid grid-cols-[minmax(0,10rem)_1fr] items-center gap-4 px-6 py-3">
                  <span className="text-xs text-muted">{item.categoria}:</span>
                  <span className="text-sm text-foreground">{item.item}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </main>
  );
}
