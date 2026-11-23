"use client";

import { useState } from "react";
import { useCardapioSemana, somarDias, nomeDoDia } from "@/hooks/useCardapioSemana";
import ApiStatus from "@/components/ApiStatus";
import PageHeader from "@/components/PageHeader";
import EstadoVazio from "@/components/EstadoVazio";
import { FilterBar, FilterPills } from "@/components/Filters";
import Badge from "@/components/Badge";

function formatarData(data: string): string {
  const [, mes, dia] = data.split("-");
  return `${dia}/${mes}`;
}

const DIAS_DA_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"];

// O RU do Gama não abre no fim de semana; o cardápio da API tem os sete dias, que valem para os outros campi.
const FIM_DE_SEMANA = ["Sábado", "Domingo"];

const BOTAO = "rounded-lg border border-border bg-surface px-3 py-1.5 text-sm text-foreground hover:bg-background";

// Dia com cardápio mais perto do escolhido: o próximo depois dele, ou o último antes.
function diaPublicadoMaisPerto(publicados: string[], escolhido: string): string | undefined {
  const i = DIAS_DA_SEMANA.indexOf(escolhido);
  const ordem = (d: string) => DIAS_DA_SEMANA.indexOf(d);
  return publicados.find((d) => ordem(d) > i) ?? [...publicados].reverse().find((d) => ordem(d) < i);
}

export default function CardapioPage() {
  const { cardapio, caminho, loading, error, inicio, hoje, ehSemanaAtual, semanaAnterior, proximaSemana, semanaAtual } =
    useCardapioSemana();
  const [dia, setDia] = useState<string | null>(null);

  const nomeHoje = hoje ? nomeDoDia(hoje) : null;
  const dias = ["Todos", ...DIAS_DA_SEMANA];
  const diaAtivo = dia ?? (ehSemanaAtual && nomeHoje ? nomeHoje : "Todos");
  const filtrado = diaAtivo === "Todos" ? cardapio : cardapio.filter((c) => c.dia === diaAtivo);
  const diasPublicados = DIAS_DA_SEMANA.filter((d) => cardapio.some((c) => c.dia === d));
  const sugestao = diaAtivo === "Todos" ? undefined : diaPublicadoMaisPerto(diasPublicados, diaAtivo);
  const dataDoDia = (d: string) => (inicio ? formatarData(somarDias(inicio, DIAS_DA_SEMANA.indexOf(d))) : "");

  return (
    <main className="flex flex-1 flex-col pb-10">
      <PageHeader title="Cardápio" sub="Cardápio da semana · RU UnB" href="/cardapio" api={{ caminho: caminho ?? "/cardapio/semana" }} />

      <div className="px-4 lg:px-10 pt-4">
        <ApiStatus loading={loading} error={error} />
      </div>

      <div className="flex flex-wrap items-center gap-3 px-4 lg:px-10 pt-4">
        <button type="button" onClick={() => { setDia(null); semanaAnterior(); }} className={BOTAO}>
          ← Anterior
        </button>
        <span className="text-sm font-medium text-foreground">
          {inicio ? `${formatarData(inicio)} a ${formatarData(somarDias(inicio, 6))}` : "Carregando…"}
        </span>
        <button type="button" onClick={() => { setDia(null); proximaSemana(); }} className={BOTAO}>
          Próxima →
        </button>
        <button type="button" onClick={() => { setDia(null); semanaAtual(); }} className={BOTAO}>
          Hoje
        </button>

      </div>
      <FilterBar hasFilters={diaAtivo !== "Todos"} onClear={() => setDia("Todos")}>
        <FilterPills label="Dia" value={diaAtivo} onChange={setDia} options={dias} />
      </FilterBar>

      <div className="flex flex-col gap-4 px-4 lg:px-10 pt-5">
        {FIM_DE_SEMANA.includes(diaAtivo) && (
          <p className="rounded-xl border border-border bg-surface px-4 py-3 text-sm text-foreground md:px-6">
            <span className="font-semibold">O RU do Gama não abre no fim de semana.</span>{" "}
            <span className="text-muted">O cardápio abaixo vale para os outros campi.</span>
          </p>
        )}
        {!loading && !error && filtrado.length === 0 && (
          <div className="rounded-xl border border-border bg-surface">
            {cardapio.length === 0 ? (
              <EstadoVazio
                acao={
                  <button type="button" onClick={() => { setDia(null); semanaAnterior(); }} className={BOTAO}>
                    ← Ver a semana anterior
                  </button>
                }
              >
                {ehSemanaAtual
                  ? "O RU ainda não publicou o cardápio desta semana."
                  : "Nenhum cardápio publicado para essa semana."}
              </EstadoVazio>
            ) : (
              <EstadoVazio
                acao={
                  sugestao && (
                    <button type="button" onClick={() => setDia(sugestao)} className={BOTAO}>
                      Ver {sugestao}, {dataDoDia(sugestao)} →
                    </button>
                  )
                }
              >
                Sem cardápio publicado para {diaAtivo}, {dataDoDia(diaAtivo)}.
              </EstadoVazio>
            )}
          </div>
        )}
        {filtrado.map((c) => (
          <div key={`${c.data}-${c.refeicao}`} className="overflow-hidden rounded-xl border border-border bg-surface">
            <div className="flex flex-wrap items-center gap-3 bg-background px-4 py-4 md:px-6">
              <div className="font-bold text-foreground">{c.dia}, {formatarData(c.data)}</div>
              {c.data === hoje && <Badge>Hoje</Badge>}
              <Badge>{c.refeicao}</Badge>
              {FIM_DE_SEMANA.includes(c.dia) && diaAtivo === "Todos" && <Badge>Só nos outros campi</Badge>}
            </div>
            <ul className="divide-y divide-border">
              {c.itens.map((item, i) => (
                <li key={`${item.categoria}-${i}`} className="grid grid-cols-1 items-center gap-1 px-4 py-3 sm:grid-cols-[minmax(0,10rem)_1fr] sm:gap-4 md:px-6">
                  <span className="text-xs text-muted">{item.categoria}:</span>
                  <span className="text-sm text-foreground">{item.item}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </main>
  );
}
