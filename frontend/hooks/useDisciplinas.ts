"use client";

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
  sala: string;
  vagas: number;
  vagasOcupadas: number;
}

// Formato que a API real devolve (espelha backend/app/schemas/disciplina.py:Turma).
// É isto que `api.get("/disciplinas")` vai retornar quando o endpoint existir.
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
function extrairDia(descricao: string): string {
  const primeiraPalavra = descricao.split(" ")[0].replace("-feira", "").toLowerCase();
  return DIA_ABREV[primeiraPalavra] ?? descricao;
}

function extrairHorario(descricao: string): string {
  const match = descricao.match(/(\d{2}:\d{2}) às (\d{2}:\d{2})/);
  return match ? `${match[1]}–${match[2]}` : descricao;
}

// disciplina_codigo vem como "CIC0004" — as letras antes do primeiro dígito são o departamento.
function extrairDepartamento(disciplinaCodigo: string): string {
  return disciplinaCodigo.replace(/\d.*$/, "");
}

// Traduz o contrato do backend (Turma) pro formato que esta tela usa (Disciplina).
export function mapTurmaToDisciplina(turma: TurmaAPI): Disciplina {
  const dias = [...new Set(turma.horarios.map((h) => extrairDia(h.descricao)))].join("/");

  return {
    codigo: turma.disciplina_codigo,
    nome: turma.disciplina_nome,
    turma: turma.numero,
    departamento: extrairDepartamento(turma.disciplina_codigo),
    professor: turma.professores.map((p) => p.nome).join(", ") || "A definir",
    dias: dias || "-",
    horario: turma.horarios[0] ? extrairHorario(turma.horarios[0].descricao) : "-",
    sala: turma.sala.descricao,
    vagas: turma.vagas_ofertadas,
    vagasOcupadas: turma.vagas_ocupadas,
  };
}

// Mock no formato REAL da API (TurmaAPI), não no formato da tela — assim a tradução
// acima é exercitada mesmo antes do endpoint /disciplinas existir de verdade.
const turmasMock: TurmaAPI[] = [
  {
    disciplina_codigo: "CIC0004",
    disciplina_nome: "Algoritmos e Programação",
    numero: "A",
    ano_periodo: "2026.2",
    professores: [{ nome: "Carlos Lima" }],
    horarios: [
      { codigo: "2M1234", descricao: "Segunda-feira 14:00 às 16:00" },
      { codigo: "4M1234", descricao: "Quarta-feira 14:00 às 16:00" },
      { codigo: "6M1234", descricao: "Sábado 8:00 às 12:00" },
    ],
    sala: { descricao: "LINF-02" },
    vagas_ofertadas: 40,
    vagas_ocupadas: 38,
  },
  {
    disciplina_codigo: "CIC0097",
    disciplina_nome: "Organização de Computadores",
    numero: "B",
    ano_periodo: "2026.2",
    professores: [{ nome: "Beatriz Alves" }],
    horarios: [
      { codigo: "3M1234", descricao: "Terça-feira 10:00 às 12:00" },
      { codigo: "5M1234", descricao: "Quinta-feira 10:00 às 12:00" },
    ],
    sala: { descricao: "LINF-04" },
    vagas_ofertadas: 35,
    vagas_ocupadas: 30,
  },
  {
    disciplina_codigo: "FGA0071",
    disciplina_nome: "Prática de Eletrônica Digital 1",
    numero: "A",
    ano_periodo: "2026.2",
    professores: [{ nome: "Ana Souza" }],
    horarios: [{ codigo: "2M1234", descricao: "Segunda-feira 08:00 às 10:00" }],
    sala: { descricao: "FGA-A1" },
    vagas_ofertadas: 20,
    vagas_ocupadas: 20,
  },
];

export function useDisciplinas() {
  const { data, loading, error } = useApiResource<TurmaAPI[]>("/disciplinas", turmasMock);
  return { disciplinas: data.map(mapTurmaToDisciplina), loading, error };
}
