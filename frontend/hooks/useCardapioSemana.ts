"use client";

import { useApiResource } from "./useApiResource";

// Formato que a API real devolve (espelha backend/app/schemas/cardapio.py:ItemCardapio) —
// uma linha por item, não agrupada por dia. `data` chega como string ISO ("2026-09-14"),
// já que é assim que o Pydantic serializa um campo `date` em JSON.
type RefeicaoAPI = "cafe_da_manha" | "almoco" | "jantar";

interface ItemCardapioAPI {
  data: string;
  refeicao: RefeicaoAPI;
  categoria: string;
  item: string;
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
const ORDEM_REFEICAO: Record<RefeicaoAPI, number> = { cafe_da_manha: 0, almoco: 1, jantar: 2 };

// "2026-09-14" -> "Segunda". Usa meio-dia UTC pra não sofrer com o fuso horário
// virando a data um dia pra trás/frente ao converter pra Date local.
function nomeDoDia(data: string): string {
  return NOMES_DIA[new Date(`${data}T12:00:00Z`).getUTCDay()];
}

interface Grupo {
  data: string;
  refeicao: RefeicaoAPI;
  itens: ItemCardapio[];
}

// Agrupa a lista achatada de itens em um card por (data, refeição).
export function mapItensToCardapio(itens: ItemCardapioAPI[]): CardapioRefeicao[] {
  const grupos = new Map<string, Grupo>();

  for (const item of itens) {
    const chave = `${item.data}__${item.refeicao}`;
    let grupo = grupos.get(chave);
    if (!grupo) {
      grupo = { data: item.data, refeicao: item.refeicao, itens: [] };
      grupos.set(chave, grupo);
    }
    grupo.itens.push({ categoria: item.categoria, item: item.item });
  }

  return [...grupos.values()]
    .sort((a, b) => a.data.localeCompare(b.data) || ORDEM_REFEICAO[a.refeicao] - ORDEM_REFEICAO[b.refeicao])
    .map((g) => ({ data: g.data, dia: nomeDoDia(g.data), refeicao: REFEICAO_LABEL[g.refeicao], itens: g.itens }));
}


function segundaDaSemana(hoje = new Date()): string {
  const segunda = new Date(hoje);
  segunda.setDate(hoje.getDate() - ((hoje.getDay() + 6) % 7));
  const mes = String(segunda.getMonth() + 1).padStart(2, "0");
  const dia = String(segunda.getDate()).padStart(2, "0");
  return `${segunda.getFullYear()}-${mes}-${dia}`;
}

export function useCardapioSemana() {
  const { data, loading, error } = useApiResource<ItemCardapioAPI[]>(
    `/cardapio/semana?data_inicio=${segundaDaSemana()}`,
    [],
  );
  return { cardapio: mapItensToCardapio(data), loading, error };
}