"use client";

import { useApiResource } from "./useApiResource";
import { useState } from "react";

// Formato que a API real devolve (espelha backend/app/schemas/api/cardapio.py:CardapioSemana,
// RF19): os 7 dias da janela, cada um com as três refeições já separadas. `data` chega como
// string ISO ("2026-09-14"), já que é assim que o Pydantic serializa um campo `date` em JSON.
type RefeicaoAPI = "cafe_da_manha" | "almoco" | "jantar";

interface CardapioDiaAPI {
  data: string;
  cafe_da_manha: ItemCardapio[];
  almoco: ItemCardapio[];
  jantar: ItemCardapio[];
  publicado: boolean;
}

interface CardapioSemanaAPI {
  data_inicio: string;
  data_fim: string;
  dias: CardapioDiaAPI[];
}

// Formato que a tela consome: um card por (dia, refeição), com a lista de itens
// exatamente como a API descreve — sem assumir campos fixos tipo "prato principal"
// ou "sobremesa", porque a quantidade e o tipo de categoria muda por refeição
// (café da manhã não tem prato principal nem sobremesa, por exemplo).
export interface ItemCardapio {
  categoria: string;
  item: string;
}

export interface CardapioRefeicao {
  data: string;
  dia: string;
  refeicao: string;
  itens: ItemCardapio[];
}

const NOMES_DIA = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"];
const REFEICAO_LABEL: Record<RefeicaoAPI, string> = {
  cafe_da_manha: "Café da manhã",
  almoco: "Almoço",
  jantar: "Jantar",
};
const REFEICOES: RefeicaoAPI[] = ["cafe_da_manha", "almoco", "jantar"];

// "2026-09-14" -> "Segunda". Usa meio-dia UTC pra não sofrer com o fuso horário
// virando a data um dia pra trás/frente ao converter pra Date local.
export function nomeDoDia(data: string): string {
  return NOMES_DIA[new Date(`${data}T12:00:00Z`).getUTCDay()];
}

export function hojeISO(hoje = new Date()): string {
  const mes = String(hoje.getMonth() + 1).padStart(2, "0");
  const dia = String(hoje.getDate()).padStart(2, "0");
  return `${hoje.getFullYear()}-${mes}-${dia}`;
}

// Um card por (dia, refeição). A API já manda os dias em ordem e os itens na ordem do PDF;
// refeição sem item (dia não publicado, feriado sem jantar) não vira card.
export function mapDiasToCardapio(dias: CardapioDiaAPI[]): CardapioRefeicao[] {
  return dias.flatMap((d) =>
    REFEICOES.filter((refeicao) => d[refeicao].length > 0).map((refeicao) => ({
      data: d.data,
      dia: nomeDoDia(d.data),
      refeicao: REFEICAO_LABEL[refeicao],
      itens: d[refeicao],
    })),
  );
}


function segundaDaSemana(hoje = new Date()): string {
  const segunda = new Date(hoje);
  segunda.setDate(hoje.getDate() - ((hoje.getDay() + 6) % 7));
  const mes = String(segunda.getMonth() + 1).padStart(2, "0");
  const dia = String(segunda.getDate()).padStart(2, "0");
  return `${segunda.getFullYear()}-${mes}-${dia}`;
}

export function useCardapioSemana() {
  const [inicio, setInicio] = useState(() => segundaDaSemana());

  const { data, loading, error } = useApiResource<CardapioSemanaAPI | null>(
    `/cardapio/semana?data_inicio=${inicio}`,
    null,
  );

  return {
    cardapio: mapDiasToCardapio(data?.dias ?? []),
    loading,
    error,
    inicio,
    ehSemanaAtual: inicio === segundaDaSemana(),
    semanaAnterior: () => setInicio((atual) => somarDias(atual, -7)),
    proximaSemana: () => setInicio((atual) => somarDias(atual, 7)),
    semanaAtual: () => setInicio(segundaDaSemana()),
  };
}

export function somarDias(data: string, dias: number): string {
  const d = new Date(`${data}T12:00:00Z`);
  d.setUTCDate(d.getUTCDate() + dias);
  return d.toISOString().slice(0, 10);
}