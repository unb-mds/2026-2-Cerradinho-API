import type { Disciplina } from "@/hooks/useDisciplinas";
import Badge from "@/components/Badge";
import SeatBar from "@/components/SeatBar";

// Versão em card de uma linha da tabela de disciplinas, para telas pequenas
// (a tabela tem colunas demais pra caber em ~375px).
export default function DisciplinaCard({ disciplina: d, mostrarStatus = false }: {
  disciplina: Disciplina;
  mostrarStatus?: boolean;
}) {
  const lotada = d.vagasOcupadas >= d.vagas;

  return (
    <div className="flex flex-col gap-2 px-4 py-3.5">
      <div className="flex items-center justify-between gap-2">
        <span className="font-mono text-xs font-semibold text-brand">{d.codigo}</span>
        <Badge>
          {d.departamento}-{d.turma}
        </Badge>
      </div>
      <div>
        <div className="font-semibold text-foreground">{d.nome}</div>
        <div className="mt-0.5 text-xs text-muted">{d.professor}</div>
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1 font-mono text-xs">
        <span className="text-foreground">{d.dias}</span>
        <span className="text-foreground">{d.horario}</span>
        <span className="text-muted">{d.sala}</span>
      </div>
      <div className="flex items-center justify-between gap-3">
        <SeatBar ocupadas={d.vagasOcupadas} total={d.vagas} />
        {mostrarStatus && (lotada ? <Badge tone="accent">Lotada</Badge> : <Badge tone="brand">Disponível</Badge>)}
      </div>
    </div>
  );
}
