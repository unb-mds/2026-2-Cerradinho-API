"use client";

import { useAgendaProfessor } from "@/hooks/useAgendaProfessor";
import ApiStatus from "@/components/ApiStatus";
import Link from "next/link";
import { useParams } from "next/navigation";
import { unidadesDasDisciplinas } from "@/hooks/useProfessores";
import ProfessorAvatar from "@/components/ProfessorAvatar";
import Badge from "@/components/Badge";
import GradeSemanal from "@/components/GradeSemanal";
import { blocosDaAgenda } from "@/hooks/useAgendaProfessor";

export default function AgendaProfessorPage() {
    const { id } = useParams<{ id: string }>();
    const { agenda, loading, error } = useAgendaProfessor(id);
    const unidades = agenda ? unidadesDasDisciplinas(agenda.turmas.map((t) => t.disciplina_codigo)) : [];
    const periodo = agenda?.turmas[0]?.ano_periodo ?? null;

    return (
        <main className="flex flex-1 flex-col px-10 py-9">
            <Link href="/professores"
                className="self-start rounded-lg border border-border bg-surface px-3.5 py-2 text-sm font-semibold text-brand transition-colors hover:bg-background"
            >
                ← Voltar para Professores
            </Link>
            <div className="mt-6">
                <ApiStatus loading={loading} error={error} />
            </div>
            {agenda && (
                <>
                    <div className="mt-6 flex items-center gap-4">
                        <ProfessorAvatar nome={agenda.nome} className="h-13 w-13 text-lg" />
                        <div>
                            <h1 className="text-2xl font-bold text-foreground">{agenda.nome}</h1>
                            <div className="mt-1 flex items-center gap-2 text-sm text-muted">
                                {unidades.map((u) => <Badge key={u}>{u}</Badge>)}
                                <span>
                                    {agenda.turmas.length} {agenda.turmas.length === 1 ? "turma" : "turmas"}
                                    {periodo && ` · ${periodo}`}
                                </span>
                            </div>
                        </div>
                    </div>

                    <div className="mt-6">
                        <GradeSemanal blocos={blocosDaAgenda(agenda)} />
                    </div>
                </>
            )}
        </main>
    );
}
