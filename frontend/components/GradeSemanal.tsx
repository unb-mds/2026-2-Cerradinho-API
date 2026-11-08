import { chaveDoBloco, type BlocoDaGrade } from "@/hooks/useAgendaProfessor";
import { minutosDoInicio } from "@/hooks/useSalasVazias";
import { DIAS } from "@/app/(app)/salas/vazias/page";

const HORAS = [8, 10, 12, 14, 16, 18, 20, 22];
const ALTURA_LINHA = 78; // altura em px de cada faixa de 2 horas
const INICIO_GRADE = 8 * 60; // a grade começa às 08:00, em minutos
const FIM_GRADE = 22 * 60 + 30; // e termina às 22:30, fim da última aula da noite
const ALTURA_GRADE = ((FIM_GRADE - INICIO_GRADE) / 120) * ALTURA_LINHA;
const ALTURA_BLOCO_COMPLETO = 65; // menos que isso, as três linhas do bloco não cabem

type BlocoNaColuna = BlocoDaGrade & { coluna: number; colunas: number };

function alturaDaFaixa(hora: number) {
    return Math.min(ALTURA_LINHA, ((FIM_GRADE - hora * 60) / 120) * ALTURA_LINHA);
}

function posicao(inicio: string, fim: string) {
    const top = ((minutosDoInicio(inicio) - INICIO_GRADE) / 120) * ALTURA_LINHA;
    const height = ((minutosDoInicio(fim) - minutosDoInicio(inicio)) / 120) * ALTURA_LINHA;
    return { top, height };
}

// Blocos que se sobrepõem no mesmo dia dividem a largura da coluna, lado a lado.
function organizarEmColunas(blocos: BlocoDaGrade[]): BlocoNaColuna[] {
    const ordenados = [...blocos].sort((a, b) => a.inicio.localeCompare(b.inicio) || b.fim.localeCompare(a.fim));
    const organizados: BlocoNaColuna[] = [];
    let grupo: BlocoNaColuna[] = [];
    let fimDoGrupo = "";

    const fecharGrupo = () => {
        const colunas = Math.max(...grupo.map((b) => b.coluna)) + 1;
        organizados.push(...grupo.map((b) => ({ ...b, colunas })));
        grupo = [];
    };

    for (const bloco of ordenados) {
        if (grupo.length > 0 && bloco.inicio >= fimDoGrupo) fecharGrupo();

        const ocupadas = grupo.filter((b) => b.fim > bloco.inicio).map((b) => b.coluna);
        let coluna = 0;
        while (ocupadas.includes(coluna)) coluna++;

        fimDoGrupo = grupo.length === 0 || bloco.fim > fimDoGrupo ? bloco.fim : fimDoGrupo;
        grupo.push({ ...bloco, coluna, colunas: 1 });
    }
    if (grupo.length > 0) fecharGrupo();

    return organizados;
}

export default function GradeSemanal({ blocos }: { blocos: BlocoDaGrade[] }) {
    return (
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
                        {organizarEmColunas(blocos.filter((b) => b.dia === dia)).map((b) => {
                            const { top, height } = posicao(b.inicio, b.fim);
                            const compacto = height < ALTURA_BLOCO_COMPLETO;
                            return (
                                <div
                                    key={chaveDoBloco(b)}
                                    title={[`${b.codigo} · Turma ${b.numero}`, `${b.inicio}–${b.fim}`, b.sala].filter(Boolean).join("\n")}
                                    style={{
                                        top,
                                        height,
                                        left: `calc(${(b.coluna / b.colunas) * 100}% + 4px)`,
                                        width: `calc(${100 / b.colunas}% - 8px)`,
                                    }}
                                    className={`absolute overflow-hidden rounded-lg border border-border bg-muted-bg ${
                                        compacto ? "px-2 py-px leading-tight" : "px-2.5 py-2"
                                    }`}
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
                        })}
                    </div>
                ))}
            </div>
        </div>
    );
}