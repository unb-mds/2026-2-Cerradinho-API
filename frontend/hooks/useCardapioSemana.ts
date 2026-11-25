"use client";

import { useApiResource } from "./useApiResource";
import { useAgora } from "./useAgora";
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


function segundaDaSemana(hoje: Date): string {
  const segunda = new Date(hoje);
  segunda.setDate(hoje.getDate() - ((hoje.getDay() + 6) % 7));
  const mes = String(segunda.getMonth() + 1).padStart(2, "0");
  const dia = String(segunda.getDate()).padStart(2, "0");
  return `${segunda.getFullYear()}-${mes}-${dia}`;
}

// A semana parte da data do navegador (useAgora), que é null na pré-renderização:
// calcular "hoje" no build dava erro de hidratação, porque a data do build não é a do aluno.
// Enquanto ela não chega, `inicio`, `hoje` e `caminho` ficam null e nada é buscado.
export function useCardapioSemana() {
  const agora = useAgora();
  const [semanas, setSemanas] = useState(0); // semanas de distância da atual

  const inicio = agora ? somarDias(segundaDaSemana(agora), 7 * semanas) : null;
  const caminho = inicio ? `/cardapio/semana?data_inicio=${inicio}` : null;
  const { data, loading, error } = useApiResource<CardapioSemanaAPI | null>(caminho, null);

  return {
    cardapio: mapDiasToCardapio(data?.dias ?? []),
    caminho,
    loading,
    error,
    inicio,
    hoje: agora ? hojeISO(agora) : null,
    ehSemanaAtual: semanas === 0,
    semanaAnterior: () => setSemanas((s) => s - 1),
    proximaSemana: () => setSemanas((s) => s + 1),
    semanaAtual: () => setSemanas(0),
  };
}

export function somarDias(data: string, dias: number): string {
  const d = new Date(`${data}T12:00:00Z`);
  d.setUTCDate(d.getUTCDate() + dias);
  return d.toISOString().slice(0, 10);
}