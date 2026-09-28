"use client";

import { useState } from "react";
import { useCardapioSemana } from "@/hooks/useCardapioSemana";
import ApiStatus from "@/components/ApiStatus";
import PageHeader from "@/components/PageHeader";
import { FilterBar, FilterPills } from "@/components/Filters";
import Badge from "@/components/Badge";

export default function CardapioPage() {
  const { cardapio, loading, error } = useCardapioSemana();
  const [dia, setDia] = useState("Todos");

  const dias = ["Todos", ...new Set(cardapio.map((c) => c.dia))];
  const filtrado = dia === "Todos" ? cardapio : cardapio.filter((c) => c.dia === dia);

  return (
    <main className="flex flex-1 flex-col pb-10">
      <PageHeader title="Cardápio" sub="Cardápio da semana · Restaurante Universitário" />

      <div className="px-10 pt-4">
        <ApiStatus loading={loading} error={error} />
      </div>

      <FilterBar hasFilters={dia !== "Todos"} onClear={() => setDia("Todos")}>
        <FilterPills label="Dia" value={dia} onChange={setDia} options={dias} />
      </FilterBar>

      <div className="flex flex-col gap-4 px-10 pt-5">
        {filtrado.map((c) => (
          <div key={`${c.data}-${c.refeicao}`} className="overflow-hidden rounded-xl border border-border bg-surface">
            <div className="flex items-center justify-between bg-background px-6 py-4">
              <div className="font-bold text-foreground">{c.dia}</div>
              <Badge>{c.refeicao}</Badge>
            </div>
            <ul className="divide-y divide-border">
              {c.itens.map((item) => (
                <li key={item.categoria} className="flex items-center justify-between gap-3 px-6 py-3">
                  <span className="text-sm text-foreground">{item.item}</span>
                  <span className="text-xs text-muted">{item.categoria}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </main>
  );
}
