import type { ReactNode } from "react";
import { FilterIcon, SearchIcon } from "@/components/Icons";

interface FilterBarProps {
  children: ReactNode;
  hasFilters: boolean;
  onClear: () => void;
}

export function FilterBar({ children, hasFilters, onClear }: FilterBarProps) {
  return (
    <div className="px-10 pt-5">
      <div className="flex flex-wrap items-center gap-4 rounded-xl border border-border bg-surface px-5 py-3.5">
        <div className="flex items-center gap-2 text-muted">
          <FilterIcon className="h-4 w-4" />
          <span className="text-xs font-semibold uppercase tracking-wide">Filtrar</span>
        </div>
        <div className="h-6 w-px bg-border" />
        {children}
        {hasFilters && (
          <>
            <div className="h-6 w-px bg-border" />
            <button
              type="button"
              onClick={onClear}
              className="text-xs font-semibold text-muted transition-colors hover:text-foreground"
            >
              Limpar
            </button>
          </>
        )}
      </div>
    </div>
  );
}

interface FilterSelectProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: string[];
}

export function FilterSelect({ label, value, onChange, options }: FilterSelectProps) {
  return (
    <label className="flex flex-col gap-1 text-[10px] font-bold uppercase tracking-wide text-muted">
      {label}
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-lg border border-border bg-background px-2.5 py-1.5 text-sm font-normal normal-case tracking-normal text-foreground"
      >
        {options.map((option) => (
          <option key={option}>{option}</option>
        ))}
      </select>
    </label>
  );
}

interface FilterPillsProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: string[];
}

export function FilterPills({ label, value, onChange, options }: FilterPillsProps) {
  return (
    <div className="flex flex-col gap-1">
      <span className="text-[10px] font-bold uppercase tracking-wide text-muted">{label}</span>
      <div className="flex gap-1">
        {options.map((option) => {
          const active = value === option;
          return (
            <button
              key={option}
              type="button"
              onClick={() => onChange(option)}
              className={`rounded-md px-2.5 py-1.5 text-xs font-semibold transition-colors ${
                active ? "bg-brand text-brand-foreground" : "border border-border bg-background text-foreground"
              }`}
            >
              {option}
            </button>
          );
        })}
      </div>
    </div>
  );
}

interface SearchInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
}

export function SearchInput({ value, onChange, placeholder }: SearchInputProps) {
  return (
    <div className="relative min-w-[180px] flex-1">
      <SearchIcon className="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-muted" />
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full rounded-lg border border-border bg-background py-2 pl-8 pr-3 text-sm text-foreground outline-none"
      />
    </div>
  );
}
