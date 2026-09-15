interface ApiStatusProps {
  loading: boolean;
  error: string | null;
}

export default function ApiStatus({ loading, error }: ApiStatusProps) {
  if (loading) {
    return <p className="text-sm text-zinc-500 dark:text-zinc-400">Carregando…</p>;
  }

  if (error) {
    return (
      <p className="rounded-md bg-amber-50 px-3 py-2 text-sm text-amber-800 dark:bg-amber-950 dark:text-amber-200">
        {error}
      </p>
    );
  }

  return null;
}
