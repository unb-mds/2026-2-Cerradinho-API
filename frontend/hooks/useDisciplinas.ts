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
function extrairDias(descricao: string): string[] {
  const encontrados = descricao.match(/segunda|terça|quarta|quinta|sexta|sábado|domingo/gi) ?? [];
  return encontrados.map((d) => DIA_ABREV[d.toLocaleLowerCase()]);
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
  const dias = [...new Set(turma.horarios.flatMap((h) => extrairDias(h.descricao)))].join("/");

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

export function useDisciplinas() {
  const { data, loading, error } = useApiResource<TurmaAPI[]>("/disciplinas", []);
  return { disciplinas: data.map(mapTurmaToDisciplina), loading, error };
}
