// O frontend mostra só o campus Gama (FCTE); a API continua servindo a UnB
// inteira e não expõe a unidade nas respostas, então o recorte é feito aqui
// com o que cada endpoint devolve.

// Códigos de disciplina da FCTE: "FGA0242" (antigo) e "FCTE0001" (novo).
const PREFIXOS_DISCIPLINA_GAMA = ["FGA", "FCTE"];

// Prédio das salas do Gama em /salas e /salas/vazias.
export const PREDIO_GAMA = "FCTE";

export function disciplinaDoGama(codigo: string): boolean {
  const prefixo = codigo.replace(/\d.*$/, "").toUpperCase();
  return PREFIXOS_DISCIPLINA_GAMA.includes(prefixo);
}

// sala.descricao das turmas chega como "FCTE - S7" (ou "FGA - I1" em dados antigos).
export function salaDoGama(descricao: string): boolean {
  return /^\s*(FCTE|FGA)\b/i.test(descricao);
}

export function predioDoGama(predio: string): boolean {
  return predio.trim().toUpperCase() === PREDIO_GAMA;
}
