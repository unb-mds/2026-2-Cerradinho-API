"use client";

interface ApiStatusProps {
  loading: boolean;
  error: string | null;
}

export default function ApiStatus({ loading, error }: ApiStatusProps) {
  if (loading) {
    return (
      <p role="status" className="flex items-center gap-2 text-sm text-muted">
        <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-brand" />
        Carregando…
      </p>
    );
  }

  if (error) {
    // Recarregar a página refaz todas as chamadas dela; é o que resolve quando a API
    // estava fora do ar ou a conexão caiu.
    return (
      <div
        role="alert"
        className="flex flex-wrap items-center justify-between gap-3 rounded-md border border-border bg-danger-surface px-3 py-2 text-sm text-danger"
      >
        <span>{error} Confira sua conexão ou tente de novo em alguns segundos.</span>
        <button
          type="button"
          onClick={() => window.location.reload()}
          className="rounded-md border border-danger/40 px-2.5 py-1 text-xs font-semibold transition-colors hover:bg-danger/10"
        >
          Tentar de novo
        </button>
      </div>
    );
  }

  return null;
}
