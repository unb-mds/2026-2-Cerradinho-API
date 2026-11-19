"use client";

import Form from "next/form";
import Link from "next/link";
import type { ReactNode } from "react";
import { useAgora } from "@/hooks/useAgora";
import { useDisciplinas } from "@/hooks/useDisciplinas";
import { useProfessores } from "@/hooks/useProfessores";
import { DIAS_API, useSalasLivresAgora } from "@/hooks/useSalasVazias";
import { hojeISO, useCardapioSemana, type CardapioRefeicao } from "@/hooks/useCardapioSemana";
import ApiStatus from "@/components/ApiStatus";
import { ChevronRightIcon, SearchIcon } from "@/components/Icons";

// Home "Agora no Gama": responde o que o aluno procura entre uma aula e outra
// (sala livre agora, RU de hoje, achar uma disciplina) e mostra que o site é uma das
// aplicações feitas sobre a API do Cerradinho.

const NOME_DIA: Record<string, string> = {
  segunda: "Segunda",
  terca: "Terça",
  quarta: "Quarta",
  quinta: "Quinta",
  sexta: "Sexta",
  sabado: "Sábado",
};

const SALAS_NA_HOME = 12;

function dataCurta(d: Date) {
  return `${String(d.getDate()).padStart(2, "0")}/${String(d.getMonth() + 1).padStart(2, "0")}`;
}

// Do cardápio de uma refeição, o prato principal e a opção vegetariana.
function pratos(refeicao: CardapioRefeicao) {
  const achar = (trecho: string) =>
    refeicao.itens.find((i) => i.categoria.toUpperCase().includes(trecho))?.item;
  return { principal: achar("PRINCIPAL PADRÃO"), vegetariano: achar("OVOLACTOVEGETARIANO") };
}

export default function Home() {
  const agora = useAgora();
  const salas = useSalasLivresAgora(agora);
  const { disciplinas, loading: carregandoDisciplinas, error: erroDisciplinas } = useDisciplinas();
  const { professores, loading: carregandoProfessores, error: erroProfessores } = useProfessores();
  const { cardapio, loading: carregandoCardapio, error: erroCardapio } = useCardapioSemana();

  const loading = salas.loading || carregandoDisciplinas || carregandoProfessores || carregandoCardapio;
  const error = salas.error ?? erroDisciplinas ?? erroProfessores ?? erroCardapio;

  const hoje = agora ? NOME_DIA[DIAS_API[agora.getDay()] ?? ""] : undefined;
  const contexto = !agora
    ? "Carregando…"
    : `${hoje ?? "Domingo"}, ${dataCurta(agora)} · ${
        salas.emAula && salas.slot ? `aula das ${salas.slot.horario}` : "fora do horário de aula"
      }`;

  const ruHoje = agora ? cardapio.filter((c) => c.data === hojeISO(agora) && c.refeicao !== "Café da manhã") : [];

  return (
    <main className="flex flex-1 flex-col gap-8 px-4 py-9 lg:px-10">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Agora no Gama</h1>
        <p className="mt-1.5 text-sm text-muted">{contexto}</p>
      </div>

      <ApiStatus loading={loading} error={error} />

      <div className="grid gap-4 xl:grid-cols-[3fr_2fr]">
        <section className="flex flex-col gap-4 rounded-xl border border-border bg-surface p-5 md:p-6">
          <div className="flex items-baseline justify-between gap-3">
            <h2 className="font-semibold text-foreground">
              {salas.emAula ? "Salas livres agora" : "Salas livres na próxima aula"}
            </h2>
            {salas.slot && (
              <span className="font-mono text-xs text-muted">
                {NOME_DIA[salas.slot.dia]}, {salas.slot.horario}
              </span>
            )}
          </div>
          <p className="text-4xl font-bold tracking-tight text-brand">
            {salas.loading || salas.error ? "–" : salas.salas.length}
          </p>
          {!salas.loading && salas.salas.length > 0 && (
            <ul className="flex flex-wrap gap-1.5">
              {salas.salas.slice(0, SALAS_NA_HOME).map((s) => (
                <li key={s.id} className="rounded-md bg-muted-bg px-2 py-1 font-mono text-xs font-semibold text-foreground">
                  {s.nome}
                </li>
              ))}
            </ul>
          )}
          <LinkSeta href={salas.href}>
            {salas.salas.length > SALAS_NA_HOME ? `Ver todas as ${salas.salas.length} salas` : "Ver salas vazias"}
          </LinkSeta>
        </section>

        <section className="flex flex-col gap-4 rounded-xl border border-border bg-surface p-5 md:p-6">
          <div>
            <h2 className="font-semibold text-foreground">RU hoje</h2>
            <p className="mt-0.5 text-xs text-muted">Darcy Ribeiro · o cardápio do Gama ainda não está na API</p>
          </div>
          {carregandoCardapio || !agora ? (
            <p className="text-sm text-muted">Carregando…</p>
          ) : ruHoje.length === 0 ? (
            <p className="text-sm text-muted">O RU ainda não publicou o cardápio de hoje.</p>
          ) : (
            <dl className="flex flex-col gap-3">
              {ruHoje.map((r) => {
                const { principal, vegetariano } = pratos(r);
                return (
                  <div key={r.refeicao} className="grid grid-cols-[4.5rem_1fr] gap-3">
                    <dt className="text-xs font-semibold text-muted">{r.refeicao}</dt>
                    <dd className="text-sm text-foreground">
                      {principal ?? r.itens[0]?.item}
                      {vegetariano && <span className="block text-xs text-muted">Vegetariano: {vegetariano}</span>}
                    </dd>
                  </div>
                );
              })}
            </dl>
          )}
          <LinkSeta href="/cardapio">Ver cardápio da semana</LinkSeta>
        </section>
      </div>

      <section className="flex flex-col gap-3">
        <h2 className="font-semibold text-foreground">
          <label htmlFor="busca-disciplinas">Buscar disciplina</label>
        </h2>
        <Form action="/disciplinas" className="flex flex-col gap-2 sm:flex-row">
          <div className="relative flex-1">
            <SearchIcon className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
            <input
              id="busca-disciplinas"
              name="busca"
              type="search"
              placeholder="Nome, código ou professor"
              className="w-full rounded-xl border border-border bg-surface py-3 pl-10 pr-4 text-sm text-foreground placeholder:text-muted focus:border-brand focus:outline-2 focus:outline-brand/30"
            />
          </div>
          <button type="submit" className="rounded-xl bg-brand px-5 py-3 text-sm font-semibold text-brand-foreground transition-colors hover:bg-brand-dark">
            Buscar
          </button>
        </Form>
      </section>

      <section className="flex flex-col gap-3">
        <h2 className="font-semibold text-foreground">Explorar</h2>
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          <Atalho href="/disciplinas" numero={carregandoDisciplinas ? "–" : String(disciplinas.length)} rotulo="turmas no semestre" />
          <Atalho href="/professores" numero={carregandoProfessores ? "–" : String(professores.length)} rotulo="professores" />
          <Atalho href="/salas/vazias" rotulo="Salas vazias por dia e horário" />
          <Atalho href="/cardapio" rotulo="Cardápio da semana" />
        </div>
      </section>

      <section className="flex flex-col gap-5 rounded-xl bg-sidebar p-6 text-sidebar-foreground md:p-8">
        <div className="max-w-2xl">
          <h2 className="text-lg font-semibold text-sidebar-foreground-active">O Cerradinho é uma API aberta</h2>
          <p className="mt-2 text-sm leading-relaxed">
            Disciplinas, professores, salas e cardápio da UnB inteira, coletados de fontes públicas e servidos num só
            lugar. Este site é uma das aplicações feitas com ela, recortada para o campus Gama.
          </p>
        </div>
        <div className="flex flex-col gap-1.5">
          <code className="w-fit max-w-full overflow-x-auto rounded-lg bg-white/10 px-3 py-2 font-mono text-xs text-sidebar-foreground-active">
            GET /v1/salas/vazias?dia={salas.slot?.dia ?? "quinta"}&amp;horario={salas.slot?.horario ?? "14:00"}
          </code>
          <span className="text-xs">A mesma chamada que preenche as salas livres lá em cima.</span>
        </div>
        <div className="flex flex-wrap items-center gap-x-5 gap-y-3">
          <Link
            href="/desenvolvedores"
            className="flex items-center gap-1.5 rounded-lg bg-sidebar-foreground-active px-4 py-2 text-sm font-semibold text-sidebar"
          >
            Documentação da API <ChevronRightIcon className="h-3.5 w-3.5" />
          </Link>
          <Link href="/desenvolvedores#sdk" className="text-sm font-semibold text-sidebar-foreground-active underline-offset-4 hover:underline">
            SDK Python e CLI
          </Link>
        </div>
      </section>
    </main>
  );
}

function LinkSeta({ href, children }: { href: string; children: ReactNode }) {
  return (
    <Link href={href} className="mt-auto flex w-fit items-center gap-1 text-sm font-semibold text-brand hover:underline">
      {children} <ChevronRightIcon className="h-3.5 w-3.5" />
    </Link>
  );
}

function Atalho({ href, numero, rotulo }: { href: string; numero?: string; rotulo: string }) {
  return (
    <Link
      href={href}
      className="flex flex-col justify-center gap-0.5 rounded-xl border border-border bg-surface px-4 py-3.5 transition-colors hover:border-brand/40"
    >
      {numero && <span className="text-xl font-bold tracking-tight text-foreground">{numero}</span>}
      <span className={numero ? "text-xs text-muted" : "text-sm font-semibold text-foreground"}>{rotulo}</span>
    </Link>
  );
}
