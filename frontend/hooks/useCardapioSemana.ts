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

// Mock no formato REAL da API (lista achatada de ItemCardapio), com as categorias que
// o RU sempre publica em cada refeição (café não tem prato principal/sobremesa; o
// jantar troca guarnição/acompanhamentos/sobremesa/bebida do almoço por sopa e torrada).
const itensMock: ItemCardapioAPI[] = [
  { data: "2026-09-14", refeicao: "cafe_da_manha", categoria: "Bebidas", item: "Café, leite, suco de caju" },
  { data: "2026-09-14", refeicao: "cafe_da_manha", categoria: "Panificação", item: "Pão francês, pão de queijo" },
  { data: "2026-09-14", refeicao: "cafe_da_manha", categoria: "Gordura", item: "Margarina" },
  { data: "2026-09-14", refeicao: "cafe_da_manha", categoria: "Complemento Padrão", item: "Presunto e queijo" },
  { data: "2026-09-14", refeicao: "cafe_da_manha", categoria: "Complemento Ovolactovegetariano", item: "Ovo mexido" },
  { data: "2026-09-14", refeicao: "cafe_da_manha", categoria: "Complemento Vegetariano Estrito", item: "Pasta de grão-de-bico" },
  { data: "2026-09-14", refeicao: "cafe_da_manha", categoria: "Fruta", item: "Banana" },

  { data: "2026-09-14", refeicao: "almoco", categoria: "Salada 1", item: "Alface e tomate" },
  { data: "2026-09-14", refeicao: "almoco", categoria: "Salada 2", item: "Beterraba ralada" },
  { data: "2026-09-14", refeicao: "almoco", categoria: "Molho para Salada", item: "Vinagrete" },
  { data: "2026-09-14", refeicao: "almoco", categoria: "Prato Principal Padrão", item: "Frango grelhado" },
  { data: "2026-09-14", refeicao: "almoco", categoria: "Prato Principal Ovolactovegetariano", item: "Omelete de legumes" },
  { data: "2026-09-14", refeicao: "almoco", categoria: "Prato Principal Vegetariano Estrito", item: "Grão-de-bico ao curry" },
  { data: "2026-09-14", refeicao: "almoco", categoria: "Guarnição", item: "Arroz e feijão" },
  { data: "2026-09-14", refeicao: "almoco", categoria: "Acompanhamentos", item: "Farofa" },
  { data: "2026-09-14", refeicao: "almoco", categoria: "Sobremesa", item: "Gelatina" },
  { data: "2026-09-14", refeicao: "almoco", categoria: "Bebida", item: "Refresco de maracujá" },

  { data: "2026-09-14", refeicao: "jantar", categoria: "Salada 1", item: "Repolho roxo" },
  { data: "2026-09-14", refeicao: "jantar", categoria: "Salada 2", item: "Cenoura ralada" },
  { data: "2026-09-14", refeicao: "jantar", categoria: "Molho para Salada", item: "Vinagrete" },
  { data: "2026-09-14", refeicao: "jantar", categoria: "Prato Principal Padrão", item: "Carne de panela" },
  { data: "2026-09-14", refeicao: "jantar", categoria: "Prato Principal Ovolactovegetariano", item: "Ovo à parmegiana" },
  { data: "2026-09-14", refeicao: "jantar", categoria: "Prato Principal Vegetariano Estrito", item: "Tofu ao molho" },
  { data: "2026-09-14", refeicao: "jantar", categoria: "Sopa", item: "Sopa de legumes" },
  { data: "2026-09-14", refeicao: "jantar", categoria: "Torrada", item: "Torrada" },
];

export function useCardapioSemana() {
  const { data, loading, error } = useApiResource<ItemCardapioAPI[]>("/cardapio/semana", itensMock);
  return { cardapio: mapItensToCardapio(data), loading, error };
}
