"use client";

import { useState } from "react";
import { useSalas } from "@/hooks/useSalas";
import ApiStatus from "@/components/ApiStatus";
import PageHeader from "@/components/PageHeader";
import { FilterBar, FilterSelect, SearchInput } from "@/components/Filters";

export default function SalasPage() {
  const { salas, loading, error } = useSalas();
  const predios = ["Todos", ...[...new Set(salas.map((s) => s.predio).filter(Boolean))].sort()];
  const [predio, setPredio] = useState("Todos");
  const [busca, setBusca] = useState("");

  const filtradas = salas.filter((s) => {
    const matchPredio = predio === "Todos" || s.predio === predio;
    const termo = busca.toLowerCase();
    const matchBusca =
      busca === "" || s.nome.toLowerCase().includes(termo) || s.predio.toLowerCase().includes(termo);
    return matchPredio && matchBusca;
  });

  const hasFilters = predio !== "Todos" || busca !== "";
  const limparFiltros = () => {
    setPredio("Todos");
    setBusca("");
  };

  return (
    <main className="flex flex-1 flex-col pb-10">
      <PageHeader title="Salas e Espaços" sub={`${filtradas.length} de ${salas.length} espaços cadastrados`} />

      <div className="px-10 pt-4">
        <ApiStatus loading={loading} error={error} />
      </div>

      <FilterBar hasFilters={hasFilters} onClear={limparFiltros}>
        <SearchInput value={busca} onChange={setBusca} placeholder="Buscar por sala ou prédio..." />
        <FilterSelect label="Prédio" value={predio} onChange={setPredio} options={predios} />
      </FilterBar>

      <div className="px-10 pt-5">
        <div className="overflow-x-auto rounded-xl border border-border bg-surface">
          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="border-b border-border bg-background text-left text-[10px] font-bold uppercase tracking-wide text-muted">
                <th className="px-4 py-3">Sala</th>
                <th className="px-4 py-3">Prédio</th>
              </tr>
            </thead>
            <tbody>
              {filtradas.length === 0 ? (
                <tr>
                  <td colSpan={2} className="px-6 py-12 text-center text-sm text-muted">
                    {loading || error ? "" : "Nenhuma sala encontrada."}
                  </td>
                </tr>
              ) : (
                filtradas.map((s) => (
                  <tr key={s.id} className="border-t border-border">
                    <td className="whitespace-nowrap px-4 py-3.5 font-mono text-sm font-semibold text-brand">
                      {s.nome}
                    </td>
                    <td className="px-4 py-3.5 text-foreground">{s.predio || "-"}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
