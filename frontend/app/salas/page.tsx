"use client";

import { useState } from "react";
import { useSalas } from "@/hooks/useSalas";
import ApiStatus from "@/components/ApiStatus";
import PageHeader from "@/components/PageHeader";
import { FilterBar, FilterSelect, SearchInput } from "@/components/Filters";
import Badge from "@/components/Badge";

const TIPOS = ["Todos", "Sala de Aula", "Laboratório", "Auditório"];

export default function SalasPage() {
  const { salas, loading, error } = useSalas();
  const [tipo, setTipo] = useState("Todos");
  const [busca, setBusca] = useState("");

  const filtradas = salas.filter((s) => {
    const matchTipo = tipo === "Todos" || s.tipo === tipo;
    const termo = busca.toLowerCase();
    const matchBusca =
      busca === "" || s.codigo.toLowerCase().includes(termo) || s.predio.toLowerCase().includes(termo);
    return matchTipo && matchBusca;
  });

  const hasFilters = tipo !== "Todos" || busca !== "";
  const limparFiltros = () => {
    setTipo("Todos");
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
        <FilterSelect label="Tipo" value={tipo} onChange={setTipo} options={TIPOS} />
      </FilterBar>

      <div className="px-10 pt-5">
        <div className="overflow-x-auto rounded-xl border border-border bg-surface">
          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="border-b border-border bg-background text-left text-[10px] font-bold uppercase tracking-wide text-muted">
                <th className="px-4 py-3">Sala</th>
                <th className="px-4 py-3">Prédio</th>
                <th className="px-4 py-3">Tipo</th>
                <th className="px-4 py-3">Capacidade</th>
              </tr>
            </thead>
            <tbody>
              {filtradas.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-6 py-12 text-center text-sm text-muted">
                    Nenhuma sala encontrada.
                  </td>
                </tr>
              ) : (
                filtradas.map((s) => (
                  <tr key={s.id} className="border-t border-border">
                    <td className="whitespace-nowrap px-4 py-3.5 font-mono text-sm font-semibold text-brand">
                      {s.codigo}
                    </td>
                    <td className="px-4 py-3.5 text-foreground">{s.predio}</td>
                    <td className="px-4 py-3.5">
                      <Badge>{s.tipo}</Badge>
                    </td>
                    <td className="px-4 py-3.5 font-mono text-xs text-foreground">{s.capacidade} lug.</td>
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
