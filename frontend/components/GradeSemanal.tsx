"use client";

import { useState } from "react";
import { chaveDoBloco, type BlocoDaGrade } from "@/hooks/useAgendaProfessor";
import { minutosDoInicio } from "@/hooks/useSalasVazias";
import { DIAS } from "@/app/(app)/salas/vazias/page";

const HORAS = [8, 10, 12, 14, 16, 18, 20, 22];
const ALTURA_LINHA = 78; // altura em px de cada faixa de 2 horas
const INICIO_GRADE = 8 * 60; // a grade começa às 08:00, em minutos
const FIM_GRADE = 22 * 60 + 30; // e termina às 22:30, fim da última aula da noite
const ALTURA_GRADE = ((FIM_GRADE - INICIO_GRADE) / 120) * ALTURA_LINHA;
const ALTURA_BLOCO_COMPLETO = 65; // menos que isso, as três linhas do bloco não cabem

// Turmas no mesmo dia com exatamente o mesmo início e fim viram um bloco só.
// Sem isso, um professor com 12 turmas simultâneas (caso real em Música)
// dividia a coluna do dia em 12 fatias ilegíveis.
type Celula = { chave: string; dia: string; inicio: string; fim: string; blocos: BlocoDaGrade[] };
type NaColuna<T> = T & { coluna: number; colunas: number };

function alturaDaFaixa(hora: number) {
    return Math.min(ALTURA_LINHA, ((FIM_GRADE - hora * 60) / 120) * ALTURA_LINHA);
}

function posicao(inicio: string, fim: string) {
    const top = ((minutosDoInicio(inicio) - INICIO_GRADE) / 120) * ALTURA_LINHA;
    const height = ((minutosDoInicio(fim) - minutosDoInicio(inicio)) / 120) * ALTURA_LINHA;
    return { top, height };
}

function rotuloDoDia(dia: string) {
    return Object.keys(DIAS).find((rotulo) => DIAS[rotulo] === dia) ?? dia;
}

function agruparPorHorario(blocos: BlocoDaGrade[]): Celula[] {
    const celulas = new Map<string, Celula>();
    for (const bloco of blocos) {
        const chave = `${bloco.dia}-${bloco.inicio}-${bloco.fim}`;
        const celula = celulas.get(chave);
        if (celula) celula.blocos.push(bloco);
        else celulas.set(chave, { chave, dia: bloco.dia, inicio: bloco.inicio, fim: bloco.fim, blocos: [bloco] });
    }
    return [...celulas.values()];
}

// Células que se sobrepõem no mesmo dia dividem a largura da coluna, lado a lado.
function organizarEmColunas<T extends { inicio: string; fim: string }>(itens: T[]): NaColuna<T>[] {
    const ordenados = [...itens].sort((a, b) => a.inicio.localeCompare(b.inicio) || b.fim.localeCompare(a.fim));
    const organizados: NaColuna<T>[] = [];
    let grupo: NaColuna<T>[] = [];
    let fimDoGrupo = "";

    const fecharGrupo = () => {
        const colunas = Math.max(...grupo.map((b) => b.coluna)) + 1;
        organizados.push(...grupo.map((b) => ({ ...b, colunas })));
        grupo = [];
    };

    for (const item of ordenados) {
        if (grupo.length > 0 && item.inicio >= fimDoGrupo) fecharGrupo();

        const ocupadas = grupo.filter((b) => b.fim > item.inicio).map((b) => b.coluna);
        let coluna = 0;
        while (ocupadas.includes(coluna)) coluna++;

        fimDoGrupo = grupo.length === 0 || item.fim > fimDoGrupo ? item.fim : fimDoGrupo;
        grupo.push({ ...item, coluna, colunas: 1 });
    }
    if (grupo.length > 0) fecharGrupo();

    return organizados;
}

// Sala comum a todas as turmas da célula, ou null se variar.
function salaComum(blocos: BlocoDaGrade[]): string | null {
    const salas = new Set(blocos.map((b) => b.sala));
    return salas.size === 1 ? blocos[0].sala : null;
}

export default function GradeSemanal({ blocos }: { blocos: BlocoDaGrade[] }) {
    const [aberta, setAberta] = useState<Celula | null>(null);
    const celulas = agruparPorHorario(blocos);

    return (
        <>
            <div className="overflow-x-auto overflow-y-hidden rounded-xl border border-border bg-surface">
                <div className="grid min-w-190 grid-cols-[5rem_repeat(6,minmax(0,1fr))]">
                    <div className="border-b border-border bg-background" />
                    {Object.keys(DIAS).map((rotulo) => (
                        <div
                            key={rotulo}
                            className="border-b border-l border-border bg-background px-3 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-muted"
                        >
                            {rotulo}
                        </div>
                    ))}

                    <div>
                        {HORAS.map((hora) => (
                            <div
                                key={hora}
                                style={{ height: alturaDaFaixa(hora) }}
                                className="border-t border-border px-3 pt-2 font-mono text-[11px] text-muted first:border-t-0"
                            >
                                {String(hora).padStart(2, "0")}:00
                            </div>
                        ))}
                    </div>

                    {Object.values(DIAS).map((dia) => (
                        <div
                            key={dia}
                            className="relative border-l border-border"
                            style={{ height: ALTURA_GRADE }}
                        >
                            {HORAS.map((hora) => (
                                <div key={hora} style={{ height: alturaDaFaixa(hora) }} className="border-t border-border first:border-t-0" />
                            ))}
                            {organizarEmColunas(celulas.filter((c) => c.dia === dia)).map((c) => {
                                const { top, height } = posicao(c.inicio, c.fim);
                                const compacto = height < ALTURA_BLOCO_COMPLETO;
                                const estilo = {
                                    top,
                                    height,
                                    left: `calc(${(c.coluna / c.colunas) * 100}% + 4px)`,
                                    width: `calc(${100 / c.colunas}% - 8px)`,
                                };
                                const espacamento = compacto ? "px-2 py-px leading-tight" : "px-2.5 py-2";

                                if (c.blocos.length === 1) {
                                    const b = c.blocos[0];
                                    return (
                                        <div
                                            key={chaveDoBloco(b)}
                                            title={[`${b.codigo} · Turma ${b.numero}`, `${b.inicio}–${b.fim}`, b.sala].filter(Boolean).join("\n")}
                                            style={estilo}
                                            className={`absolute overflow-hidden rounded-lg border border-border bg-muted-bg ${espacamento}`}
                                        >
                                            {compacto ? (
                                                <div className="truncate font-mono text-xs font-semibold text-foreground">
                                                    {b.codigo} · T{b.numero}
                                                </div>
                                            ) : (
                                                <>
                                                    <div className="truncate font-mono text-xs font-semibold text-foreground">{b.codigo}</div>
                                                    <div className="truncate text-xs text-foreground">Turma {b.numero}</div>
                                                </>
                                            )}
                                            {b.sala && <div className="truncate font-mono text-[10px] text-muted">{b.sala}</div>}
                                        </div>
                                    );
                                }

                                const selecionada = aberta?.chave === c.chave;
                                const sala = salaComum(c.blocos);
                                return (
                                    <button
                                        key={c.chave}
                                        type="button"
                                        onClick={() => setAberta(selecionada ? null : c)}
                                        aria-expanded={selecionada}
                                        aria-controls="grade-turmas-simultaneas"
                                        title={[`${c.blocos.length} turmas · ${c.inicio}–${c.fim}`, ...c.blocos.map((b) => `${b.codigo} · Turma ${b.numero}`)].join("\n")}
                                        style={estilo}
                                        className={`absolute overflow-hidden rounded-lg border text-left transition-colors ${espacamento} ${
                                            selecionada
                                                ? "border-brand bg-brand text-brand-foreground"
                                                : "border-brand/40 bg-muted-bg text-foreground hover:border-brand"
                                        }`}
                                    >
                                        <div className="truncate text-xs font-semibold">{c.blocos.length} turmas</div>
                                        {!compacto && (
                                            <div className={`truncate text-[11px] ${selecionada ? "" : "text-brand"}`}>
                                                {selecionada ? "Ocultar lista" : "Ver lista"}
                                            </div>
                                        )}
                                        {sala && (
                                            <div className={`truncate font-mono text-[10px] ${selecionada ? "" : "text-muted"}`}>{sala}</div>
                                        )}
                                    </button>
                                );
                            })}
                        </div>
                    ))}
                </div>
            </div>

            {aberta && (
                <section id="grade-turmas-simultaneas" className="mt-4 overflow-hidden rounded-xl border border-border bg-surface">
                    <div className="flex items-center justify-between gap-4 border-b border-border bg-background px-4 py-3">
                        <h2 className="text-sm font-semibold text-foreground">
                            {rotuloDoDia(aberta.dia)} · {aberta.inicio}–{aberta.fim} · {aberta.blocos.length} turmas no mesmo horário
                        </h2>
                        <button
                            type="button"
                            onClick={() => setAberta(null)}
                            className="text-sm font-semibold text-brand hover:underline"
                        >
                            Fechar
                        </button>
                    </div>
                    <ul className="text-sm">
                        {aberta.blocos.map((b) => (
                            <li key={chaveDoBloco(b)} className="flex items-center gap-3 border-t border-border px-4 py-2.5 first:border-t-0">
                                <span className="font-mono text-xs font-semibold text-brand">{b.codigo}</span>
                                <span className="text-foreground">Turma {b.numero}</span>
                                {b.sala && <span className="ml-auto font-mono text-xs text-muted">{b.sala}</span>}
                            </li>
                        ))}
                    </ul>
                </section>
            )}
        </>
    );
}
