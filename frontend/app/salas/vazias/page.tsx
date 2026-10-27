"use client";

import { useSalasVazias } from "@/hooks/useSalasVazias";
import ApiStatus from "@/components/ApiStatus";
import PageHeader from "@/components/PageHeader";
import { FilterBar, FilterPills, FilterSelect } from "@/components/Filters";

const DIAS: Record<string, string> = {
    Segunda: "segunda",
    Terça: "terca",
    Quarta: "quarta",
    Quinta: "quinta",
    Sexta: "sexta",
    Sábado: "sabado",
};

const HORARIOS = [
    "08:00", "08:55", "10:00", "10:55", "12:00", "12:55", "14:00",
    "14:55", "16:00", "16:55", "18:00", "18:55", "20:00", "20:55",
];

export default function SalasVaziasPage() {
    const { salas, loading, error, dia, horario, setDia, setHorario } = useSalasVazias();
    const rotuloDia = Object.keys(DIAS).find((rotulo) => DIAS[rotulo] === dia) ?? "Segunda";


    return (
        <main className="flex flex-1 flex-col pb-10">
            <PageHeader
                title="Salas Vazias"
                sub={loading ? "Carregando..." : `${salas.length} salas sem aula cadastrada`}
            />

            <div className="px-10 pt-4">
                <ApiStatus loading={loading} error={error} />
            </div>

            <FilterBar hasFilters={false} onClear={() => { }}>
                <FilterPills
                    label="Dia"
                    value={rotuloDia}
                    onChange={(rotulo) => setDia(DIAS[rotulo])}
                    options={Object.keys(DIAS)}
                />
                <FilterSelect label="Horário" value={horario} onChange={setHorario} options={HORARIOS} />
            </FilterBar>
            <p className="px-10 pt-4 text-xs text-muted">
                Vazia quer dizer sem aula cadastrada no SIGAA. Reserva informal e eventos não aparecem aqui.
            </p>

            <div className="px-10 pt-5">
                <div className="overflow-x-auto rounded-xl border border-border bg-surface">
                    <table className="w-full border-collapse text-sm">
                        <thead>
                            <tr className="border-b border-border bg-background text-left text-[10px] font-bold uppercase tracking-wide text-muted">
                                <th className="px-4 py-3">Sala</th>
                                <th className="px-4 py-3">Prédio</th>
                            </tr>
                        </thead>
                        <tbody>
                            {salas.length === 0 ? (
                                <tr>
                                    <td colSpan={2} className="px-6 py-12 text-center text-sm text-muted">
                                        {loading || error ? "" : "Nenhuma sala vazia nesse horário."}
                                    </td>
                                </tr>
                            ) : (
                                salas.map((s) => (
                                    <tr key={s.id} className="border-t border-border">
                                        <td className="whitespace-nowrap px-4 py-3.5 font-mono text-sm font-semibold text-brand">
                                            {s.nome}
                                        </td>
                                        <td className="px-4 py-3.5 text-foreground">{s.predio || "-"}</td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </main>
    );
}
