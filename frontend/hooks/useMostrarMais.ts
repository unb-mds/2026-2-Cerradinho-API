import { useState } from "react";

// Mostra a lista aos poucos: com ~6.500 turmas, montar tudo de uma vez (e em
// dobro, já que a lista do celular e a tabela do desktop ficam no DOM juntas)
// trava a página. `chave` são os filtros atuais: mudou o filtro, volta pro início.
export function useMostrarMais<T>(itens: T[], chave: string, passo = 50) {
  const [estado, setEstado] = useState({ chave, limite: passo });
  const limite = estado.chave === chave ? estado.limite : passo;

  return {
    visiveis: itens.slice(0, limite),
    restantes: Math.max(itens.length - limite, 0),
    mostrarMais: () => setEstado({ chave, limite: limite + passo }),
  };
}
