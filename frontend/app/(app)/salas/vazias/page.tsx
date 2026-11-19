"use client";

import ApiStatus from "@/components/ApiStatus";
import PageHeader from "@/components/PageHeader";
import { FilterBar, FilterSelect } from "@/components/Filters";
import { useSalasVazias, HORARIOS, fimDoBloco } from "@/hooks/useSalasVazias";

// usado tambem pela grade semanal do professor
export const DIAS: Record<string, string> = {
    Segunda: "segunda",
    Terça: "terca",
    Quarta: "quarta",
    Quinta: "quinta",
    Sexta: "sexta",
    Sábado: "sabado",
};

// "08:00 às 09:50"
const BLOCOS: Record<string, string> = Object.fromEntries(HORARIOS.map((h) => [`${h} às ${fimDoBloco(h)}`, h]));

export default function SalasVaziasPage() {
    const { dias, loading, error, horario, setHorario, hoje } = useSalasVazias();
    const rotuloBloco = Object.keys(BLOCOS).find((rotulo) => BLOCOS[rotulo] === horario) ?? "";

    return (
        <main className="flex flex-1 flex-col pb-10">
            <PageHeader
                title="Salas Vazias"
                sub={loading ? "Carregando..." : `Salas sem aula das ${rotuloBloco}, de segunda a sábado`}
            />

            <div className="px-4 md:px-10 pt-4">
                <ApiStatus loading={loading} error={error} />
            </div>

            <FilterBar hasFilters={false} onClear={() => { }}>
                <FilterSelect label="Horário" value={rotuloBloco} onChange={(rotulo) => setHorario(BLOCOS[rotulo])} options={Object.keys(BLOCOS)} />
            </FilterBar>
            <p className="px-4 md:px-10 pt-4 text-xs text-muted">
                Só aparecem as salas I1 a I10 e S1 a S10 da FCTE, em blocos de duas aulas das 8h às 17h50. Vazia quer dizer sem aula cadastrada no SIGAA no bloco inteiro. Reserva informal e eventos não aparecem aqui.
            </p>

            <div className="grid grid-cols-1 gap-4 px-4 pt-5 sm:grid-cols-2 md:px-10 xl:grid-cols-3">
                {dias.map(({ dia, rotulo, salas }) => (
                    <section
                        key={dia}
                        className={`rounded-xl border bg-surface ${dia === hoje ? "border-brand" : "border-border"}`}
                    >
                        <header className="flex items-baseline justify-between gap-3 border-b border-border px-4 py-3">
                            <h2 className="text-sm font-bold text-foreground">
                                {rotulo}
                                {dia === hoje && <span className="ml-2 text-[10px] font-bold uppercase tracking-wide text-brand">hoje</span>}
                            </h2>
                            <span className="text-xs text-muted">
                                {loading || error ? "" : `${salas.length} ${salas.length === 1 ? "sala" : "salas"}`}
                            </span>
                        </header>
                        {loading || error ? (
                            <p className="px-4 py-6 text-sm text-muted">{loading ? "Carregando..." : "-"}</p>
                        ) : salas.length === 0 ? (
                            <p className="px-4 py-6 text-sm text-muted">Nenhuma sala vazia nesse horário.</p>
                        ) : (
                            <ul className="flex flex-wrap gap-2 px-4 py-4">
                                {salas.map((s) => (
                                    <li
                                        key={s.id}
                                        className="rounded-md border border-border bg-background px-2.5 py-1 font-mono text-sm font-semibold text-brand"
                                    >
                                        {s.nome}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </section>
                ))}
            </div>
        </main>
    );
}
