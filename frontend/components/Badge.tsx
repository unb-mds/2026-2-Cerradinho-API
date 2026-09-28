import type { ReactNode } from "react";

interface BadgeProps {
  children: ReactNode;
  tone?: "brand" | "accent" | "muted";
}

const TONES = {
  brand: "bg-brand/10 text-brand",
  accent: "bg-accent-surface text-accent",
  muted: "bg-muted-bg text-foreground",
} as const;

export default function Badge({ children, tone = "muted" }: BadgeProps) {
  return (
    <span
      className={`inline-block whitespace-nowrap rounded-md px-2 py-0.5 font-mono text-[11px] font-semibold ${TONES[tone]}`}
    >
      {children}
    </span>
  );
}
