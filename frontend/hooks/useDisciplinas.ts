"use client";

import { disciplinaDoGama, salaDoGama } from "@/lib/campus";
import { useApiResource } from "./useApiResource";

// Formato que a tela de Disciplinas consome (tabela, filtros, badges).
export interface Disciplina {
  codigo: string;
  nome: string;
  turma: string;
  departamento: string;
  professor: string;
  dias: string;
  horario: string;
  // Início e fim (em minutos) de cada aula da semana, pro filtro de horário.
  aulas: { inicio: number; fim: number }[];
  sala: string;
  vagas: number;
  vagasOcupadas: number;
}

// Formato que a API devolve em /v1/disciplinas (espelha backend/app/schemas/disciplina.py:Turma).
interface TurmaAPI {
  disciplina_codigo: string;
  disciplina_nome: string;
  numero: string;
  ano_periodo: string;
  professores: { nome: string }[];
  horarios: { codigo: string; descricao: string }[];
  sala: { descricao: string };
  vagas_ofertadas: number;
  vagas_ocupadas: number;
}

const DIA_ABREV: Record<string, string> = {
  segunda: "Seg",
  terça: "Ter",
  quarta: "Qua",
  quinta: "Qui",
  sexta: "Sex",
  sábado: "Sáb",
  domingo: "Dom",
};

// horarios[].descricao chega como "Sexta-feira 14:00 às 17:50" ou "Sábado 08:00 às 12:00"
// (sábado/domingo não têm o sufixo "-feira") — extrai só o dia abreviado nos dois formatos.
function extrairDias(descricao: string): string[] {
  const encontrados = descricao.match(/segunda|terça|quarta|quinta|sexta|sábado|domingo/gi) ?? [];
  return encontrados.map((d) => DIA_ABREV[d.toLocaleLowerCase()]);
}

function extrairHorario(descricao: string): string {
  const match = descricao.match(/(\d{2}:\d{2}) às (\d{2}:\d{2})/);
  return match ? `${match[1]}–${match[2]}` : descricao;
}

export function emMinutos(hora: string): number {
  const [h, m] = hora.split(":").map(Number);
  return h * 60 + m;
}

function extrairAula(descricao: string): { inicio: number; fim: number } | null {
  const match = descricao.match(/(\d{2}:\d{2}) às (\d{2}:\d{2})/);
  return match ? { inicio: emMinutos(match[1]), fim: emMinutos(match[2]) } : null;
}

// Mesmo horário em todos os dias: "08:00–09:50". Horários diferentes por dia:
// "Seg 08:00–09:50 · Qua 14:00–15:50" (antes só aparecia o primeiro).
function descreverHorario(horarios: TurmaAPI["horarios"]): string {
  const faixas = [...new Set(horarios.map((h) => extrairHorario(h.descricao)))];
  if (faixas.length <= 1) return faixas[0] ?? "-";
  return horarios.map((h) => `${extrairDias(h.descricao).join("/")} ${extrairHorario(h.descricao)}`).join(" · ");
}

// disciplina_codigo vem como "CIC0004" — as letras antes do primeiro dígito são o departamento.
function extrairDepartamento(disciplinaCodigo: string): string {
  return disciplinaCodigo.replace(/\d.*$/, "");
}

// Traduz o contrato do backend (Turma) pro formato que esta tela usa (Disciplina).
export function mapTurmaToDisciplina(turma: TurmaAPI): Disciplina {
  const dias = [...new Set(turma.horarios.flatMap((h) => extrairDias(h.descricao)))].join("/");

  return {
    codigo: turma.disciplina_codigo,
    nome: turma.disciplina_nome,
    turma: turma.numero,
    departamento: extrairDepartamento(turma.disciplina_codigo),
    professor: turma.professores.map((p) => p.nome).join(", ") || "A definir",
    dias: dias || "-",
    horario: descreverHorario(turma.horarios),
    aulas: turma.horarios.map((h) => extrairAula(h.descricao)).filter((a) => a !== null),
    sala: turma.sala.descricao,
    vagas: turma.vagas_ofertadas,
    vagasOcupadas: turma.vagas_ocupadas,
  };
}

export function useDisciplinas() {
  const { data, loading, error } = useApiResource<TurmaAPI[]>("/disciplinas", []);
  // Só o campus Gama: disciplinas da FCTE e turmas de outros departamentos com aula em sala da FCTE.
  const doGama = data.filter((t) => disciplinaDoGama(t.disciplina_codigo) || salaDoGama(t.sala.descricao));
  return { disciplinas: doGama.map(mapTurmaToDisciplina), caminho: "/disciplinas", loading, error };
}
