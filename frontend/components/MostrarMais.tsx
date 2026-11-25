export default function MostrarMais({
  restantes,
  onClick,
}: {
  restantes: number;
  onClick: () => void;
}) {
  if (restantes <= 0) return null;

  return (
    <div className="flex justify-center pt-4">
      <button
        type="button"
        onClick={onClick}
        className="rounded-lg border border-border bg-surface px-4 py-2 text-sm font-semibold text-foreground transition-colors hover:border-brand hover:text-brand"
      >
        Mostrar mais ({restantes} restantes)
      </button>
    </div>
  );
}
