"use client";

import { useMemo } from "react";
import { disciplinaDoGama, salaDoGama } from "@/lib/campus";
import { useApiResource } from "./useApiResource";

interface ProfessorAPI {
  id: number;
  nome: string;
  disciplinas: string[];
}

// Só o que este hook usa de /v1/disciplinas.
interface TurmaAPI {
  professores: { nome: string }[];
  sala: { descricao: string } | null;
}

export interface Professor {
  id: number;
  nome: string;
  unidades: string[];
  disciplinas: string[];
}

export function unidadesDasDisciplinas(codigos: string[]): string[] {
  return [...new Set(codigos.map((codigo) => codigo.replace(/\d.*$/, "")))];
}

function mapProfessor(p: ProfessorAPI): Professor {
  const unidades = unidadesDasDisciplinas(p.disciplinas);
  return { ...p, unidades };
}

const chaveDoNome = (nome: string) => nome.trim().toUpperCase();

// Só o campus Gama: docentes com alguma disciplina da FCTE, ou com turma em sala
// da FCTE - quem dá Física 1, Química Geral ou Cálculo no Gama tem disciplina do
// instituto (IFD, IQD, MAT), e /professores não diz onde a turma acontece. Por
// isso o cruzamento com /disciplinas, pelo nome (a turma não traz o id do docente).
// A lista não espera /disciplinas: os da FCTE aparecem na hora e os outros entram
// quando ela chega; se ela falhar, fica só o primeiro recorte.
export function useProfessores() {
  const { data, loading, error } = useApiResource<ProfessorAPI[]>("/professores", []);
  const { data: turmas } = useApiResource<TurmaAPI[]>("/disciplinas", []);

  const comTurmaNoGama = useMemo(
    () =>
      new Set(
        turmas
          .filter((t) => salaDoGama(t.sala?.descricao ?? ""))
          .flatMap((t) => t.professores.map((p) => chaveDoNome(p.nome))),
      ),
    [turmas],
  );

  const doGama = data.filter((p) => p.disciplinas.some(disciplinaDoGama) || comTurmaNoGama.has(chaveDoNome(p.nome)));
  return { professores: doGama.map(mapProfessor), caminho: "/professores", loading, error };
}
