import Link from "next/link";
import type { ReactNode } from "react";

interface StatCardProps {
  icon: ReactNode;
  label: string;
  stat: string;
  sub: string;
  href?: string;
  active?: boolean;
}

export default function StatCard({ icon, label, stat, sub, href, active }: StatCardProps) {
  const content = (
    <div
      className={`flex flex-1 flex-col gap-3 rounded-xl border p-5 transition-colors ${
        active
          ? "border-transparent bg-brand text-brand-foreground"
          : "border-border bg-surface hover:border-brand/40"
      }`}
    >
      <div className="flex items-center justify-between">
        <span
          className={`flex h-9 w-9 items-center justify-center rounded-lg ${
            active ? "bg-white/15" : "bg-muted-bg text-brand"
          }`}
        >
          {icon}
        </span>
        <span
          className={`text-[10px] font-semibold uppercase tracking-wide ${
            active ? "text-brand-foreground/70" : "text-muted"
          }`}
        >
          {label}
        </span>
      </div>
      <div>
        <div className="text-2xl font-bold tracking-tight">{stat}</div>
        <div className={`mt-1 font-mono text-xs ${active ? "text-brand-foreground/70" : "text-muted"}`}>
          {sub}
        </div>
      </div>
    </div>
  );

  if (!href) return content;

  return (
    <Link href={href} className="flex flex-1">
      {content}
    </Link>
  );
}
