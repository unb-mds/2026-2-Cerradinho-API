import Link from "next/link";
import { ChevronRightIcon, GridIcon } from "@/components/Icons";

interface PageHeaderProps {
  title: string;
  sub: string;
}

export default function PageHeader({ title, sub }: PageHeaderProps) {
  return (
    <div className="px-10 pt-8">
      <div className="mb-3 flex items-center gap-1.5 text-[13px]">
        <Link href="/" className="flex items-center gap-1 text-muted transition-colors hover:text-foreground">
          <GridIcon className="h-3.5 w-3.5" /> Visão Geral
        </Link>
        <ChevronRightIcon className="h-3 w-3 text-muted" />
        <span className="font-semibold text-foreground">{title}</span>
      </div>
      <h1 className="text-2xl font-bold tracking-tight text-foreground">{title}</h1>
      <p className="mt-1.5 text-sm text-muted">{sub}</p>
    </div>
  );
}
