"use client";

import { useState } from "react";
import { useProfessores } from "@/hooks/useProfessores";
import ApiStatus from "@/components/ApiStatus";
import PageHeader from "@/components/PageHeader";
import { FilterBar, FilterSelect, SearchInput } from "@/components/Filters";
import Badge from "@/components/Badge";

const DEPARTAMENTOS = ["Todos", "CIC", "FGA"];

function iniciais(nome: string) {
  return nome
    .split(" ")
    .slice(0, 2)
    .map((parte) => parte[0])
    .join("");
}

export default function ProfessoresPage() {
  const { professores, loading, error } = useProfessores();
  const [departamento, setDepartamento] = useState("Todos");
  const [busca, setBusca] = useState("");

  const filtrados = professores.filter((p) => {
    const matchDepartamento = departamento === "Todos" || p.departamento === departamento;
    const termo = busca.toLowerCase();
    const matchBusca =
      busca === "" || p.nome.toLowerCase().includes(termo) || p.departamento.toLowerCase().includes(termo);
    return matchDepartamento && matchBusca;
  });

  const hasFilters = departamento !== "Todos" || busca !== "";
  const limparFiltros = () => {
    setDepartamento("Todos");
    setBusca("");
  };

  return (
    <main className="flex flex-1 flex-col pb-10">
      <PageHeader title="Professores" sub={`${filtrados.length} de ${professores.length} docentes ativos`} />

      <div className="px-10 pt-4">
        <ApiStatus loading={loading} error={error} />
      </div>

      <FilterBar hasFilters={hasFilters} onClear={limparFiltros}>
        <SearchInput value={busca} onChange={setBusca} placeholder="Buscar por nome ou departamento..." />
        <FilterSelect label="Unidade" value={departamento} onChange={setDepartamento} options={DEPARTAMENTOS} />
      </FilterBar>

      <div className="px-10 pt-5">
        <div className="overflow-x-auto rounded-xl border border-border bg-surface">
          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="border-b border-border bg-background text-left text-[10px] font-bold uppercase tracking-wide text-muted">
                <th className="px-4 py-3">Professor(a)</th>
                <th className="px-4 py-3">Titulação</th>
                <th className="px-4 py-3">Unidade</th>
                <th className="px-4 py-3">Disciplinas</th>
              </tr>
            </thead>
            <tbody>
              {filtrados.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-6 py-12 text-center text-sm text-muted">
                    Nenhum professor encontrado.
                  </td>
                </tr>
              ) : (
                filtrados.map((p) => (
                  <tr key={p.id} className="border-t border-border">
                    <td className="px-4 py-3.5">
                      <div className="flex items-center gap-3">
                        <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-muted-bg text-xs font-bold text-brand">
                          {iniciais(p.nome)}
                        </span>
                        <span className="font-semibold text-foreground">{p.nome}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3.5 text-xs text-muted">{p.titulo}</td>
                    <td className="px-4 py-3.5">
                      <Badge>{p.departamento}</Badge>
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="flex flex-wrap gap-1.5">
                        {p.disciplinas.map((codigo) => (
                          <Badge key={codigo} tone="brand">
                            {codigo}
                          </Badge>
                        ))}
                      </div>
                    </td>
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
