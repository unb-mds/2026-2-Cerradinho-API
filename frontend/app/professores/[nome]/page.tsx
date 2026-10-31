"use client";

import { nomeDoSlug } from "@/hooks/useProfessores";
import Link from "next/link";
import { useParams } from "next/navigation";

export default function AgendaProfessorPage() {
    const { nome: slug } = useParams<{ nome: string }>();
    const nome = nomeDoSlug(slug);

    return (
        <main className="flex flex-1 flex-col px-10 py-9">
            <Link href="/professores" className="text-sm font-semibold text-brand">
                ← Voltar para Professores
            </Link>
            <h1 className="mt-6 text-2xl font-bold text-foreground">{nome}</h1>
        </main>
    );
}