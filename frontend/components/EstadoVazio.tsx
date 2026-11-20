import type { ReactNode } from "react";
import { CerradinhoFlower } from "@/components/Icons";

// Tela sem resultado: a caliandra e uma frase curta, e opcionalmente uma ação.
export default function EstadoVazio({ children, acao }: { children: ReactNode; acao?: ReactNode }) {
  return (
    <div className="flex flex-col items-center gap-3 px-6 py-10 text-center">
      <CerradinhoFlower className="h-12 w-12" aria-hidden />
      <p className="max-w-sm text-sm text-muted text-balance">{children}</p>
      {acao}
    </div>
  );
}
