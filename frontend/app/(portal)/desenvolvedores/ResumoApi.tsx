"use client";

import { useApiResource } from "@/hooks/useApiResource";

interface Resumo {
  turmas: number;
  professores: number;
  salas: number;
}

const numero = new Intl.NumberFormat("pt-BR");

// Totais ao vivo de /resumo: mostra o tamanho do que a API cobre (a UnB inteira),
// já que o app ao lado só exibe o recorte do campus Gama.
export default function ResumoApi() {
  const { data, loading, error } = useApiResource<Resumo | null>("/resumo", null);
  if (loading || error || !data) return null;

  return (
    <p className="mt-4 text-sm text-sidebar-foreground">
      Agora mesmo: <strong className="font-semibold text-sidebar-foreground-active">{numero.format(data.turmas)}</strong>{" "}
      turmas, <strong className="font-semibold text-sidebar-foreground-active">{numero.format(data.professores)}</strong>{" "}
      professores e <strong className="font-semibold text-sidebar-foreground-active">{numero.format(data.salas)}</strong>{" "}
      salas de todos os campi, direto de <code className="whitespace-nowrap font-mono text-xs">GET /v1/resumo</code>.
    </p>
  );
}
