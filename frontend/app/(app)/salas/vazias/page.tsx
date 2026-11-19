"use client";

import { Suspense } from "react";
import ApiStatus from "@/components/ApiStatus";
import PageHeader from "@/components/PageHeader";
import { FilterBar, FilterPills, FilterSelect } from "@/components/Filters";
import { useSalasVazias, HORARIOS } from "@/hooks/useSalasVazias";
import { useMostrarMais } from "@/hooks/useMostrarMais";
import MostrarMais from "@/components/MostrarMais";

export const DIAS: Record<string, string> = {
    Segunda: "segunda",
    Terça: "terca",
    Quarta: "quarta",
    Quinta: "quinta",
    Sexta: "sexta",
    Sábado: "sabado",
};


// Dia e horário vêm da URL (useSearchParams), que só existe no navegador:
// o Suspense deixa o build pré-renderizar o resto e mostra o cabeçalho enquanto isso.
export default function SalasVaziasPage() {
    return (
        <Suspense
            fallback={
                <main className="flex flex-1 flex-col pb-10">
                    <PageHeader title="Salas Vazias" sub="Carregando..." />
                </main>
            }
        >
            <SalasVazias />
        </Suspense>
    );
}

const MOMENTO: Record<"agora" | "proxima", string> = { agora: " (agora)", proxima: " (próxima aula)" };

function SalasVazias() {
    const { salas, caminho, loading, error, dia, horario, momento, temAulaAgora, setDia, setHorario, voltarParaAgora } = useSalasVazias();
    const { visiveis, restantes, mostrarMais } = useMostrarMais(salas, `${dia}|${horario}`);
    const rotuloDia = Object.keys(DIAS).find((rotulo) => DIAS[rotulo] === dia) ?? "Segunda";
    const quando = `${rotuloDia}, ${horario}${momento ? MOMENTO[momento] : ""}`;
    const contagem = salas.length === 1 ? "1 sala livre" : `${salas.length} salas livres`;

    return (
        <main className="flex flex-1 flex-col pb-10">
            <PageHeader
                title="Salas Vazias"
                sub={loading ? `Carregando · ${quando}` : `${contagem} · ${quando}`}
                api={{ caminho, nota: "A API responde para todos os campi; este site mostra só as salas da FCTE." }}
            />

            <div className="px-4 lg:px-10 pt-4">
                <ApiStatus loading={loading} error={error} />
            </div>

            <FilterBar hasFilters={momento === null} onClear={voltarParaAgora} clearLabel={temAulaAgora ? "Agora" : "Próxima aula"}>
                <FilterPills
                    label="Dia"
                    value={rotuloDia}
                    onChange={(rotulo) => setDia(DIAS[rotulo])}
                    options={Object.keys(DIAS)}
                />
                <FilterSelect label="Horário" value={horario} onChange={setHorario} options={HORARIOS} />
            </FilterBar>
            <p className="px-4 lg:px-10 pt-4 text-xs text-muted">
                Vazia quer dizer sem aula cadastrada no SIGAA. Reserva informal e eventos não aparecem aqui.
            </p>

            <div className="px-4 lg:px-10 pt-5">
                <ul className="divide-y divide-border rounded-xl border border-border bg-surface xl:hidden">
                    {salas.length === 0 ? (
                        <li className="px-4 py-12 text-center text-sm text-muted">
                            {loading || error ? "" : "Nenhuma sala vazia nesse horário."}
                        </li>
                    ) : (
                        visiveis.map((s) => (
                            <li key={s.id} className="flex items-center justify-between gap-3 px-4 py-3">
                                <span className="font-mono text-sm font-semibold text-brand">{s.nome}</span>
                            </li>
                        ))
                    )}
                </ul>
                <div className="hidden overflow-x-auto rounded-xl border border-border bg-surface xl:block">
                    <table className="w-full border-collapse text-sm">
                        <thead>
                            <tr className="border-b border-border bg-background text-left text-[10px] font-bold uppercase tracking-wide text-muted">
                                <th className="px-4 py-3">Sala</th>
                            </tr>
                        </thead>
                        <tbody>
                            {salas.length === 0 ? (
                                <tr>
                                    <td className="px-6 py-12 text-center text-sm text-muted">
                                        {loading || error ? "" : "Nenhuma sala vazia nesse horário."}
                                    </td>
                                </tr>
                            ) : (
                                visiveis.map((s) => (
                                    <tr key={s.id} className="border-t border-border">
                                        <td className="whitespace-nowrap px-4 py-3.5 font-mono text-sm font-semibold text-brand">
                                            {s.nome}
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
                <MostrarMais restantes={restantes} onClick={mostrarMais} />
            </div>
        </main>
    );
}
