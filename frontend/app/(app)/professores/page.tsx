"use client";

import { useState } from "react";
import { useProfessores } from "@/hooks/useProfessores";
import { casaBusca } from "@/lib/busca";
import ApiStatus from "@/components/ApiStatus";
import PageHeader from "@/components/PageHeader";
import { FilterBar, FilterSelect, SearchInput } from "@/components/Filters";
import Badge from "@/components/Badge";
import Link from "next/link";
import ProfessorAvatar from "@/components/ProfessorAvatar";

export default function ProfessoresPage() {
  const { professores, loading, error } = useProfessores();
  const unidades = ["Todos", ...[... new Set(professores.flatMap((p) => p.unidades))].sort()];
  const [departamento, setDepartamento] = useState("Todos");
  const [busca, setBusca] = useState("");

  const filtrados = professores.filter((p) => {
    const matchDepartamento = departamento === "Todos" || p.unidades.includes(departamento);
    const matchBusca = casaBusca(busca, p.nome, ...p.disciplinas);
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

      <div className="px-4 md:px-10 pt-4">
        <ApiStatus loading={loading} error={error} />
      </div>

      <FilterBar hasFilters={hasFilters} onClear={limparFiltros}>
        <SearchInput value={busca} onChange={setBusca} placeholder="Buscar por nome ou disciplina..." />
        <FilterSelect label="Unidade" value={departamento} onChange={setDepartamento} options={unidades} />
      </FilterBar>

      <div className="px-4 md:px-10 pt-5">
        <ul className="divide-y divide-border rounded-xl border border-border bg-surface md:hidden">
          {filtrados.length === 0 ? (
            <li className="px-4 py-12 text-center text-sm text-muted">
              {loading || error ? "" : "Nenhum professor encontrado."}
            </li>
          ) : (
            filtrados.map((p) => (
              <li key={p.id} className="flex flex-col gap-2.5 px-4 py-3.5">
                <div className="flex items-center gap-3">
                  <ProfessorAvatar nome={p.nome} />
                  <Link href={`/professores/${p.id}`} className="font-semibold text-foreground hover:text-brand">
                    {p.nome}
                  </Link>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {p.unidades.map((u) => (
                    <Badge key={u}>{u}</Badge>
                  ))}
                  {p.disciplinas.map((codigo) => (
                    <Badge key={codigo} tone="brand">
                      {codigo}
                    </Badge>
                  ))}
                </div>
              </li>
            ))
          )}
        </ul>
        <div className="hidden overflow-x-auto rounded-xl border border-border bg-surface md:block">
          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="border-b border-border bg-background text-left text-[10px] font-bold uppercase tracking-wide text-muted">
                <th className="px-4 py-3">Professor(a)</th>
                <th className="px-4 py-3">Unidade</th>
                <th className="px-4 py-3">Disciplinas</th>
              </tr>
            </thead>
            <tbody>
              {filtrados.length === 0 ? (
                <tr>
                  <td colSpan={3} className="px-6 py-12 text-center text-sm text-muted">
                    {loading || error ? "" : "Nenhum professor encontrado."}
                  </td>
                </tr>
              ) : (
                filtrados.map((p) => (
                  <tr key={p.id} className="border-t border-border">
                    <td className="px-4 py-3.5">
                      <div className="flex items-center gap-3">
                        <ProfessorAvatar nome={p.nome} />
                        <Link
                          href={`/professores/${p.id}`}
                          className="font-semibold text-foreground hover:text-brand hover:underLine"
                        >
                          {p.nome}
                        </Link>
                      </div>
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="flex flex-wrap gap-1.5">
                        {p.unidades.map((u) => (
                          <Badge key={u}>{u}</Badge>
                        ))}
                      </div>
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
