"use client";

import { useAgendaProfessor } from "@/hooks/useAgendaProfessor";
import ApiStatus from "@/components/ApiStatus";
import Link from "next/link";
import { useParams } from "next/navigation";

export default function AgendaProfessorPage() {
    const { id } = useParams<{ id: string }>();
    const { agenda, loading, error } = useAgendaProfessor(id);

    return (
        <main className="flex flex-1 flex-col px-10 py-9">
            <Link href="/professores" className="text-sm font-semibold text-brand">
                ← Voltar para Professores
            </Link>
            <div className="mt-6">
                <ApiStatus loading={loading} error={error} />
            </div>
            {agenda && <h1 className="text-2xl font-bold text-foreground">{agenda.nome}</h1>}
        </main>
    );
}
