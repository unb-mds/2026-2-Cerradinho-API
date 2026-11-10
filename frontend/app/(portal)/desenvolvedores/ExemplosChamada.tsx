"use client";

import { useState } from "react";
import CodeBlock from "@/components/CodeBlock";

type Linguagem = "curl" | "python" | "javascript";

const ABAS: { id: Linguagem; label: string }[] = [
  { id: "curl", label: "curl" },
  { id: "python", label: "Python" },
  { id: "javascript", label: "JavaScript" },
];

function exemplos(baseUrl: string): Record<Linguagem, string> {
  const url = `${baseUrl}/salas/vazias?dia=segunda&horario=08:00`;
  return {
    curl: `curl "${url}"`,
    python: [
      "import requests",
      "",
      `resposta = requests.get("${baseUrl}/salas/vazias", params={"dia": "segunda", "horario": "08:00"})`,
      "salas = resposta.json()",
    ].join("\n"),
    javascript: [
      `const resposta = await fetch("${url}");`,
      "const salas = await resposta.json();",
    ].join("\n"),
  };
}

export default function ExemplosChamada({ baseUrl }: { baseUrl: string }) {
  const [ativa, setAtiva] = useState<Linguagem>("curl");
  const codigo = exemplos(baseUrl)[ativa];

  return (
    <div className="flex flex-col gap-3">
      <div
        role="tablist"
        aria-label="Linguagem do exemplo"
        className="flex flex-wrap gap-2"
      >
        {ABAS.map(({ id, label }) => (
          <button
            key={id}
            type="button"
            role="tab"
            aria-selected={ativa === id}
            onClick={() => setAtiva(id)}
            className={`rounded-md border px-3 py-2 text-sm font-medium transition-colors ${
              ativa === id
                ? "border-brand bg-brand text-brand-foreground"
                : "border-border bg-surface text-foreground hover:border-brand"
            }`}
          >
            {label}
          </button>
        ))}
      </div>
      <CodeBlock code={codigo} />
    </div>
  );
}
