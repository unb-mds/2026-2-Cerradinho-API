"use client";

import { useAgendaProfessor } from "@/hooks/useAgendaProfessor";
import ApiStatus from "@/components/ApiStatus";
import Link from "next/link";
import { useParams } from "next/navigation";
import { unidadesDasDisciplinas } from "@/hooks/useProfessores";
import ProfessorAvatar from "@/components/ProfessorAvatar";
import Badge from "@/components/Badge";
import GradeSemanal from "@/components/GradeSemanal";
import { blocosDaAgenda, turmasSemHorario } from "@/hooks/useAgendaProfessor";

export default function AgendaProfessorPage() {
    const { id } = useParams<{ id: string }>();
    const { agenda, loading, error } = useAgendaProfessor(id);
    const unidades = agenda ? unidadesDasDisciplinas(agenda.turmas.map((t) => t.disciplina_codigo)) : [];
    const periodo = agenda?.turmas[0]?.ano_periodo ?? null;
    const blocos = agenda ? blocosDaAgenda(agenda) : [];
    const semHorario = agenda ? turmasSemHorario(agenda) : [];

    return (
        <main className="flex flex-1 flex-col px-4 md:px-10 py-9">
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
                        {blocos.length > 0 ? (
                            <GradeSemanal blocos={blocos} />
                        ) : (
                            <p className="rounded-xl border border-border bg-surface px-6 py-12 text-center text-sm text-muted">
                                Nenhum horário cadastrado para este professor.
                            </p>
                        )}
                    </div>

                    {semHorario.length > 0 && (
                        <section className="mt-6">
                            <h2 className="text-sm font-semibold text-foreground">Turmas sem horário definido</h2>
                            <ul className="mt-2 overflow-hidden rounded-xl border border-border bg-surface text-sm">
                                {semHorario.map((t) => (
                                    <li
                                        key={`${t.disciplina_codigo}-${t.numero}-${t.ano_periodo}`}
                                        className="border-t border-border px-4 py-3 first:border-t-0"
                                    >
                                        <span className="font-mono text-xs font-semibold text-brand">{t.disciplina_codigo}</span>
                                        <span className="ml-3 text-foreground">{t.disciplina_nome}</span>
                                        <span className="ml-2 text-xs text-muted">Turma {t.numero}</span>
                                    </li>
                                ))}
                            </ul>
                        </section>
                    )}
                </>
            )}
        </main>
    );
}
