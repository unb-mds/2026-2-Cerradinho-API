"use client";

import { useState } from "react";
import { useDisciplinas } from "@/hooks/useDisciplinas";
import ApiStatus from "@/components/ApiStatus";
import PageHeader from "@/components/PageHeader";
import { FilterBar, FilterPills, FilterSelect, SearchInput } from "@/components/Filters";
import Badge from "@/components/Badge";
import SeatBar from "@/components/SeatBar";

const DEPARTAMENTOS = ["Todos", "CIC", "FGA"];
const DIAS = ["Todos", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];
const HORARIOS = ["Todos", "08:00", "10:00", "14:00"];

export default function DisciplinasPage() {
  const { disciplinas, loading, error } = useDisciplinas();
  const [departamento, setDepartamento] = useState("Todos");
  const [dia, setDia] = useState("Todos");
  const [horario, setHorario] = useState("Todos");
  const [busca, setBusca] = useState("");

  const filtradas = disciplinas.filter((d) => {
    const matchDepartamento = departamento === "Todos" || d.departamento === departamento;
    const matchDia = dia === "Todos" || d.dias.includes(dia);
    const matchHorario = horario === "Todos" || d.horario.startsWith(horario);
    const termo = busca.toLowerCase();
    const matchBusca =
      busca === "" ||
      d.nome.toLowerCase().includes(termo) ||
      d.codigo.toLowerCase().includes(termo) ||
      d.professor.toLowerCase().includes(termo);
    return matchDepartamento && matchDia && matchHorario && matchBusca;
  });

  const hasFilters = departamento !== "Todos" || dia !== "Todos" || horario !== "Todos" || busca !== "";
  const limparFiltros = () => {
    setDepartamento("Todos");
    setDia("Todos");
    setHorario("Todos");
    setBusca("");
  };

  return (
    <main className="flex flex-1 flex-col pb-10">
      <PageHeader title="Disciplinas" sub={`${filtradas.length} de ${disciplinas.length} turmas · semestre atual`} />

      <div className="px-10 pt-4">
        <ApiStatus loading={loading} error={error} />
      </div>

      <FilterBar hasFilters={hasFilters} onClear={limparFiltros}>
        <SearchInput value={busca} onChange={setBusca} placeholder="Buscar por nome, código ou professor..." />
        <FilterSelect label="Unidade" value={departamento} onChange={setDepartamento} options={DEPARTAMENTOS} />
        <FilterPills label="Dia" value={dia} onChange={setDia} options={DIAS} />
        <FilterSelect label="Horário" value={horario} onChange={setHorario} options={HORARIOS} />
      </FilterBar>

      <div className="px-10 pt-5">
        <div className="overflow-x-auto rounded-xl border border-border bg-surface">
          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="border-b border-border bg-background text-left text-[10px] font-bold uppercase tracking-wide text-muted">
                <th className="whitespace-nowrap px-4 py-3">Código</th>
                <th className="px-4 py-3">Disciplina / Professor</th>
                <th className="px-4 py-3">Turma</th>
                <th className="whitespace-nowrap px-4 py-3">Dias</th>
                <th className="whitespace-nowrap px-4 py-3">Horário</th>
                <th className="whitespace-nowrap px-4 py-3">Sala</th>
                <th className="px-4 py-3">Vagas</th>
                <th className="px-4 py-3" />
              </tr>
            </thead>
            <tbody>
              {filtradas.length === 0 ? (
                <tr>
                  <td colSpan={8} className="px-6 py-12 text-center text-sm text-muted">
                    Nenhuma disciplina encontrada.
                  </td>
                </tr>
              ) : (
                filtradas.map((d) => {
                  const lotada = d.vagasOcupadas >= d.vagas;
                  return (
                    <tr key={d.codigo + d.turma} className="border-t border-border">
                      <td className="whitespace-nowrap px-4 py-3.5 font-mono text-xs font-semibold text-brand">
                        {d.codigo}
                      </td>
                      <td className="max-w-xs px-4 py-3.5">
                        <div className="font-semibold text-foreground">{d.nome}</div>
                        <div className="mt-0.5 text-xs text-muted">{d.professor}</div>
                      </td>
                      <td className="px-4 py-3.5">
                        <Badge>
                          {d.departamento}-{d.turma}
                        </Badge>
                      </td>
                      <td className="whitespace-nowrap px-4 py-3.5 font-mono text-xs text-foreground">{d.dias}</td>
                      <td className="whitespace-nowrap px-4 py-3.5 font-mono text-xs text-foreground">
                        {d.horario}
                      </td>
                      <td className="whitespace-nowrap px-4 py-3.5 font-mono text-xs text-muted">{d.sala}</td>
                      <td className="px-4 py-3.5">
                        <SeatBar ocupadas={d.vagasOcupadas} total={d.vagas} />
                      </td>
                      <td className="whitespace-nowrap px-4 py-3.5">
                        {lotada ? <Badge tone="accent">Lotada</Badge> : <Badge tone="brand">Disponível</Badge>}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
