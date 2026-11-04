"use client";

import { useApiResource } from "./useApiResource";
import type { Sala } from "./useSalas";

export interface BlocoAgenda {
  dia: string;
  inicio: string;
  fim: string;
  sala: Sala | null;
}

export interface TurmaAgenda {
  disciplina_codigo: string;
  disciplina_nome: string;
  numero: string;
  ano_periodo: string;
  horarios: BlocoAgenda[];
}

export interface Agenda {
  id: number;
  nome: string;
  turmas: TurmaAgenda[];
}

export function useAgendaProfessor(id: string) {
  const { data, loading, error, status } = useApiResource<Agenda | null>(`/professores/${id}/agenda`, null);
  // 404 é id inexistente; 422, id que nem é número (ex. /professores/abc).
  const naoEncontrado = status === 404 || status === 422;
  return { agenda: data, loading, error: naoEncontrado ? "Professor não encontrado." : error };
}

export function turmasSemHorario(agenda: Agenda): TurmaAgenda[] {
  return agenda.turmas.filter((turma) => turma.horarios.length === 0);
}

export interface BlocoDaGrade {
  codigo: string;
  numero: string;
  dia: string;
  inicio: string;
  fim: string;
  sala: string | null;
}

export function chaveDoBloco(b: Pick<BlocoDaGrade, "codigo" | "numero" | "dia" | "inicio" | "fim">): string {
  return `${b.codigo}-${b.numero}-${b.dia}-${b.inicio}-${b.fim}`;
}

function rotuloDaSala(sala: Sala | null): string | null {
  if (!sala) return null;
  return sala.predio ? `${sala.predio}-${sala.nome}` : sala.nome;
}

// A API devolve um bloco por sala: turma com duas salas no mesmo horário vira um bloco só.
export function blocosDaAgenda(agenda: Agenda): BlocoDaGrade[] {
  const blocos = new Map<string, BlocoDaGrade>();

  for (const turma of agenda.turmas) {
    for (const h of turma.horarios) {
      const chave = chaveDoBloco({ codigo: turma.disciplina_codigo, numero: turma.numero, ...h });
      const sala = rotuloDaSala(h.sala);
      const existente = blocos.get(chave);

      if (!existente) {
        blocos.set(chave, {
          codigo: turma.disciplina_codigo,
          numero: turma.numero,
          dia: h.dia,
          inicio: h.inicio,
          fim: h.fim,
          sala,
        });
      } else if (sala && !existente.sala?.split(" / ").includes(sala)) {
        existente.sala = existente.sala ? `${existente.sala} / ${sala}` : sala;
      }
    }
  }

  return [...blocos.values()];
}
