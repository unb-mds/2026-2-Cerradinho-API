import Link from "next/link";
import type { ProfessorDaTurma } from "@/hooks/useDisciplinas";

// Professores de uma turma, cada um com link pra própria agenda. Sem id
// (API ainda sem o campo, ou docente não persistido), o nome fica em texto puro.
export default function ProfessoresDaTurma({ professores }: { professores: ProfessorDaTurma[] }) {
  if (professores.length === 0) return <span>A definir</span>;

  return (
    <span>
      {professores.map((p, i) => (
        <span key={p.id ?? p.nome}>
          {i > 0 && ", "}
          {p.id != null ? (
            <Link href={`/professores/${p.id}`} className="underline decoration-muted/50 underline-offset-2 hover:text-brand hover:decoration-brand">
              {p.nome}
            </Link>
          ) : (
            p.nome
          )}
        </span>
      ))}
    </span>
  );
}
