"use client";

import Link from "next/link";
import { useDisciplinas } from "@/hooks/useDisciplinas";
import { useProfessores } from "@/hooks/useProfessores";
import { useSalas } from "@/hooks/useSalas";
import StatCard from "@/components/StatCard";
import Badge from "@/components/Badge";
import SeatBar from "@/components/SeatBar";
import { BookIcon, BowlIcon, BuildingIcon, ChevronRightIcon, UserIcon } from "@/components/Icons";

export default function Home() {
  const { disciplinas } = useDisciplinas();
  const { professores } = useProfessores();
  const { salas } = useSalas();

  return (
    <main className="flex flex-1 flex-col gap-7 px-10 py-9">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Visão Geral</h1>
        <p className="mt-1.5 text-sm text-muted">Universidade de Brasília — UnB</p>
      </div>

      <div className="flex flex-wrap gap-3.5">
        <StatCard
          icon={<BookIcon className="h-[18px] w-[18px]" />}
          label="Disciplinas"
          stat={String(disciplinas.length)}
          sub="turmas ofertadas"
          href="/disciplinas"
          active
        />
        <StatCard
          icon={<BowlIcon className="h-[18px] w-[18px]" />}
          label="Cardápio"
          stat="RU"
          sub="cardápio da semana"
          href="/cardapio"
        />
        <StatCard
          icon={<UserIcon className="h-[18px] w-[18px]" />}
          label="Professores"
          stat={String(professores.length)}
          sub="docentes ativos"
          href="/professores"
        />
        <StatCard
          icon={<BuildingIcon className="h-[18px] w-[18px]" />}
          label="Salas"
          stat={String(salas.length)}
          sub="espaços cadastrados"
          href="/salas"
        />
      </div>

      <div className="overflow-hidden rounded-xl border border-border bg-surface">
        <div className="flex items-center justify-between border-b border-border px-6 py-4">
          <div>
            <h2 className="text-sm font-semibold text-foreground">Disciplinas em Oferta</h2>
            <span className="text-xs text-muted">Semestre atual</span>
          </div>
          <Link
            href="/disciplinas"
            className="flex items-center gap-1.5 rounded-lg bg-muted-bg px-3 py-1.5 text-xs font-semibold text-brand"
          >
            Ver todas <ChevronRightIcon className="h-3 w-3" />
          </Link>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="bg-background text-left text-[10px] font-bold uppercase tracking-wide text-muted">
                <th className="whitespace-nowrap px-4 py-2.5">Código</th>
                <th className="px-4 py-2.5">Disciplina</th>
                <th className="px-4 py-2.5">Turma</th>
                <th className="whitespace-nowrap px-4 py-2.5">Horário</th>
                <th className="whitespace-nowrap px-4 py-2.5">Sala</th>
                <th className="px-4 py-2.5">Vagas</th>
              </tr>
            </thead>
            <tbody>
              {disciplinas.map((d) => (
                <tr key={d.codigo + d.turma} className="border-t border-border">
                  <td className="whitespace-nowrap px-4 py-3 font-mono text-xs font-medium text-brand">
                    {d.codigo}
                  </td>
                  <td className="px-4 py-3">
                    <div className="font-medium text-foreground">{d.nome}</div>
                    <div className="mt-0.5 text-xs text-muted">{d.professor}</div>
                  </td>
                  <td className="px-4 py-3">
                    <Badge>
                      {d.departamento}-{d.turma}
                    </Badge>
                  </td>
                  <td className="whitespace-nowrap px-4 py-3">
                    <div className="font-mono text-xs text-foreground">{d.dias}</div>
                    <div className="text-xs text-muted">{d.horario}</div>
                  </td>
                  <td className="whitespace-nowrap px-4 py-3 font-mono text-xs text-muted">{d.sala}</td>
                  <td className="px-4 py-3">
                    <SeatBar ocupadas={d.vagasOcupadas} total={d.vagas} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
