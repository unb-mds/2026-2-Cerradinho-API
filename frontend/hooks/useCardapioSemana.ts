"use client";

import { useApiResource } from "./useApiResource";

export interface CardapioDia {
  dia: string;
  refeicao: string;
  pratoPrincipal: string;
  opcaoVegetariana: string;
  sobremesa: string;
}

const cardapioMock: CardapioDia[] = [
  { dia: "Segunda", refeicao: "Almoço", pratoPrincipal: "Frango grelhado", opcaoVegetariana: "Grão-de-bico", sobremesa: "Fruta" },
  { dia: "Terça", refeicao: "Almoço", pratoPrincipal: "Carne de panela", opcaoVegetariana: "Tofu ao molho", sobremesa: "Gelatina" },
  { dia: "Quarta", refeicao: "Almoço", pratoPrincipal: "Peixe assado", opcaoVegetariana: "Legumes salteados", sobremesa: "Fruta" },
];

export function useCardapioSemana() {
  const { data, loading, error } = useApiResource<CardapioDia[]>("/cardapio/semana", cardapioMock);
  return { cardapio: data, loading, error };
}
