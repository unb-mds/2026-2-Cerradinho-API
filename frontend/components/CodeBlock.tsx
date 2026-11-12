"use client";

import { useState } from "react";

export default function CodeBlock({ code }: { code: string }) {
    const [copiado, setCopiado] = useState(false);

    async function copiar() {
        try {
            await navigator.clipboard.writeText(code);
            setCopiado(true);
            setTimeout(() => setCopiado(false), 1500);
        } catch {
            // clipboard pode ser bloqueado (http, permissão); sem fallback por enquanto
        }
    }

    return (
        <div className="relative rounded-xl border border-border bg-surface">
            <button
                type="button"
                onClick={copiar}
                className="absolute right-2 top-2 rounded-md border border-border bg-background px-2 py-1 text-xs font-semibold text-muted hover:text-foreground"
            >
                {copiado ? "Copiado" : "Copiar"}
            </button>
            <pre className="overflow-x-auto p-4 pr-20 font-mono text-xs text-foreground">
                <code>{code}</code>
            </pre>
        </div>
    );
}