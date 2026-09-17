interface ApiStatusProps {
  loading: boolean;
  error: string | null;
}

export default function ApiStatus({ loading, error }: ApiStatusProps) {
  if (loading) {
    return (
      <p className="flex items-center gap-2 text-sm text-muted">
        <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-brand" />
        Carregando…
      </p>
    );
  }

  if (error) {
    return (
      <p className="rounded-md border border-border bg-danger-surface px-3 py-2 text-sm text-danger">
        {error}
      </p>
    );
  }

  return null;
}
