interface SeatBarProps {
  ocupadas: number;
  total: number;
}

export default function SeatBar({ ocupadas, total }: SeatBarProps) {
  const pct = total > 0 ? Math.min((ocupadas / total) * 100, 100) : 0;
  const cheia = ocupadas >= total;
  const color = cheia ? "bg-accent" : pct >= 80 ? "bg-amber-500" : "bg-brand";

  return (
    <div className="flex flex-col gap-1">
      <span className="font-mono text-xs text-foreground">
        {ocupadas}/{total}
      </span>
      <div className="h-1 w-14 overflow-hidden rounded-full bg-muted-bg">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
