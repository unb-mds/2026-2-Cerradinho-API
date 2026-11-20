import Link from "next/link";
import type { ReactNode } from "react";
import Badge from "@/components/Badge";
import CodeBlock from "@/components/CodeBlock";
import { API_URL } from "@/lib/api";
import { CerradinhoFlower } from "@/components/Icons";
import ExemplosChamada from "./ExemplosChamada";
import ResumoApi from "./ResumoApi";
import SwaggerViewer from "./SwaggerViewer";

const REPO_URL = "https://github.com/unb-mds/2026-2-Cerradinho-API";
const DOCS_URL = `${REPO_URL}/tree/main/docs`;

// O SDK e a CLI ainda não estão no PyPI nem na main: instalam direto da pasta
// sdk/ da dev. Quando a release 2 entrar na main, trocar pra "main".
const BRANCH_SDK = "dev";
const SDK_URL = `${REPO_URL}/tree/${BRANCH_SDK}/sdk`;
const SDK_INSTALACAO = `pip install "git+${REPO_URL}.git@${BRANCH_SDK}#subdirectory=sdk"`;

// O SDK recebe a URL sem o /v1 (ele monta os caminhos de /v1/ sozinho).
// Um exemplo por domínio da API (RF13, #208) - mesma cobertura do sdk/README.md.
const SDK_EXEMPLO = `from cerradinho_sdk import CerradinhoClient

with CerradinhoClient("${API_URL.replace(/\/v1$/, "")}") as cerradinho:
    turmas = cerradinho.listar_disciplinas(busca="fga", limite=20)
    docentes = cerradinho.listar_professores(nome="andre")
    agenda = cerradinho.obter_agenda(professor_id=12)
    salas = cerradinho.listar_salas()
    salas_vazias = cerradinho.listar_salas_vazias(dia="segunda", horario="08:00")
    cardapio = cerradinho.obter_cardapio_semana()
    execucoes = cerradinho.listar_execucoes(limite=10)
    resumo = cerradinho.obter_resumo()`;

// A CLI vem no mesmo pacote do SDK e, como ele, recebe a URL sem o /v1.
const CLI_URL = `${SDK_URL}#cli`;
const CLI_CONFIGURACAO = `export CERRADINHO_API_URL=${API_URL.replace(/\/v1$/, "")}
cerradinho --help`;
const CLI_EXEMPLO = `cerradinho salas-vazias segunda 08:00
cerradinho professores "maria"
cerradinho --json cardapio`;

// Espelha os routers de backend/app/routers. Ao criar/mudar rota lá, atualizar aqui.
const ENDPOINTS = [
  {
    caminho: "/disciplinas",
    descricao:
      "Lista as turmas do período, com professores, horários, sala e vagas",
  },
  {
    caminho: "/professores?nome=",
    descricao:
      "Lista professores; busca parcial por nome, sem diferenciar acentos",
  },
  {
    caminho: "/professores/{id}/agenda",
    descricao: "Agenda semanal do professor",
  },
  { caminho: "/salas", descricao: "Lista as salas que têm aula no período" },
  {
    caminho: "/salas/vazias?dia=&horario=",
    descricao: "Salas livres em um dia e horário",
  },
  {
    caminho: "/cardapio/semana?data_inicio=",
    descricao: "Cardápio do RU dos sete dias a partir da data",
  },
  {
    caminho: "/execucoes",
    descricao: "Histórico das coletas automáticas dos dados",
  },
  {
    caminho: "/resumo",
    descricao:
      "Totais de turmas, disciplinas, professores e salas, sem baixar as listas",
  },
];

const PARAMETROS_SALAS_VAZIAS = [
  {
    nome: "dia",
    tipo: "texto",
    descricao:
      "Dia da semana: segunda, terca, quarta, quinta, sexta, sabado ou domingo",
  },
  {
    nome: "horario",
    tipo: "texto (HH:MM)",
    descricao: "Horário de início da aula, ex.: 08:00",
  },
];

const RESPOSTA_EXEMPLO = `[
  { "id": 7, "nome": "I9/I10", "predio": "FCTE" },
  { "id": 12, "nome": "S1", "predio": "UAC" }
]`;

const NAV = [
  { href: "#endpoints", label: "Endpoints" },
  { href: "#exemplos", label: "Exemplos" },
  { href: "#swagger", label: "Swagger" },
  { href: "#sdk", label: "SDK e CLI" },
];

function Secao({
  id,
  titulo,
  sub,
  children,
}: {
  id: string;
  titulo: string;
  sub: string;
  children: ReactNode;
}) {
  return (
    <section
      id={id}
      className="scroll-mt-20 border-b border-border px-4 py-10 md:px-16 md:py-12"
    >
      <h2 className="text-2xl font-bold tracking-tight text-foreground md:text-[28px]">
        {titulo}
      </h2>
      <p className="mt-2 text-sm text-muted">{sub}</p>
      <div className="mt-6 flex flex-col gap-6">{children}</div>
    </section>
  );
}

function Tabela({
  colunas,
  linhas,
}: {
  colunas: string[];
  linhas: ReactNode[][];
}) {
  return (
    <>
      {/* celular: cada linha vira um card, com a 1ª e 2ª colunas no topo */}
      <ul className="divide-y divide-border rounded-xl border border-border bg-surface text-[13px] md:hidden">
        {linhas.map(([primeira, segunda, ...resto], i) => (
          <li
            key={i}
            className="flex flex-col gap-1.5 px-4 py-3 text-foreground"
          >
            <div className="flex flex-wrap items-center gap-2 break-all">
              {primeira}
              {segunda}
            </div>
            {resto.map((celula, j) => (
              <div key={j} className="text-muted">
                {celula}
              </div>
            ))}
          </li>
        ))}
      </ul>
      <div className="hidden overflow-x-auto rounded-xl border border-border bg-surface md:block">
        <table className="w-full text-left text-[13px]">
          <thead className="bg-muted-bg text-foreground">
            <tr>
              {colunas.map((c) => (
                <th key={c} className="px-4 py-3 font-semibold">
                  {c}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {linhas.map((celulas, i) => (
              <tr key={i}>
                {celulas.map((celula, j) => (
                  <td key={j} className="px-4 py-3 align-top text-foreground">
                    {celula}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

function CartaoFerramenta({
  titulo,
  descricao,
  link,
  children,
}: {
  titulo: string;
  descricao: string;
  link: string;
  children: ReactNode;
}) {
  return (
    <div className="flex min-w-0 flex-1 flex-col gap-3 rounded-xl border border-border bg-surface p-6">
      <h3 className="text-lg font-bold text-foreground">{titulo}</h3>
      <p className="text-sm text-muted">{descricao}</p>
      {children}
      <a
        href={link}
        target="_blank"
        rel="noreferrer"
        className="text-sm font-semibold text-foreground underline underline-offset-2 hover:text-brand"
      >
        Ver no GitHub
      </a>
    </div>
  );
}

export default function PortalDesenvolvedorPage() {
  return (
    <>
      <header className="sticky top-0 z-30 flex flex-wrap items-center justify-between gap-x-6 gap-y-2 border-b border-white/10 bg-sidebar px-4 py-3.5 md:px-16">
        <Link href="/desenvolvedores" className="flex items-center gap-2.5">
          <CerradinhoFlower className="h-10 w-10" aria-hidden />
          <span className="text-sm font-semibold text-sidebar-foreground-active">Cerradinho</span>
          <span className="rounded bg-sidebar-active px-1.5 py-0.5 font-mono text-[11px] font-semibold text-sidebar-foreground">
            API v1
          </span>
        </Link>
        <nav className="flex flex-wrap items-center gap-x-5 gap-y-1 text-sm font-semibold">
          {NAV.map(({ href, label }) => (
            <a
              key={href}
              href={href}
              className="hidden text-sidebar-foreground transition-colors hover:text-sidebar-foreground-active sm:inline"
            >
              {label}
            </a>
          ))}
          <a
            href={REPO_URL}
            target="_blank"
            rel="noreferrer"
            className="text-sidebar-foreground transition-colors hover:text-sidebar-foreground-active"
          >
            GitHub
          </a>
          <Link href="/" className="text-sidebar-foreground-active underline-offset-4 hover:underline">
            Ver o app do Gama
          </Link>
        </nav>
      </header>

      <main className="flex-1">
        <section className="grid gap-10 bg-sidebar px-4 pb-14 pt-10 md:px-16 md:pb-20 md:pt-16 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)] lg:items-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-balance text-sidebar-foreground-active md:text-[44px] md:leading-[1.1]">
              API aberta de dados da UnB
            </h1>
            <p className="mt-4 max-w-xl text-base leading-relaxed text-sidebar-foreground">
              Disciplinas, professores, salas vazias e o cardápio do RU, coletados de fontes públicas e servidos em
              JSON. Use no seu app, bot ou script.
            </p>
            <ResumoApi />
            <div className="mt-7 max-w-xl">
              <p className="mb-2 text-xs font-semibold text-sidebar-foreground">URL base</p>
              <CodeBlock code={API_URL} />
            </div>
            <div className="mt-6 flex flex-wrap gap-3">
              <a
                href="#swagger"
                className="rounded-md bg-sidebar-foreground-active px-4 py-3 text-sm font-semibold text-sidebar transition-colors hover:bg-white"
              >
                Experimentar no Swagger
              </a>
              <a
                href="#sdk"
                className="rounded-md border border-white/25 px-4 py-3 text-sm font-semibold text-sidebar-foreground-active transition-colors hover:bg-white/10"
              >
                Instalar o SDK
              </a>
            </div>
          </div>

          <figure className="overflow-hidden rounded-xl border border-white/10 bg-black/25">
            <div className="flex items-center gap-2 border-b border-white/10 px-4 py-3">
              <span className="rounded bg-sidebar-active px-1.5 py-0.5 font-mono text-[11px] font-semibold text-sidebar-foreground">
                GET
              </span>
              <code className="min-w-0 break-all font-mono text-xs text-sidebar-foreground-active">
                /v1/salas/vazias?dia=quinta&amp;horario=14:00
              </code>
            </div>
            <pre className="overflow-x-auto px-4 py-4 font-mono text-xs leading-relaxed text-sidebar-foreground">
              <code>{RESPOSTA_EXEMPLO}</code>
            </pre>
            <figcaption className="border-t border-white/10 px-4 py-3 text-xs text-sidebar-foreground">
              Exemplo de resposta, resumido. É a mesma chamada que alimenta a tela de Salas Vazias do app.
            </figcaption>
          </figure>
        </section>

        <Secao
          id="endpoints"
          titulo="Endpoints"
          sub="Todos os caminhos partem da URL base. Todas as respostas são JSON."
        >
          <Tabela
            colunas={["Método", "Caminho", "Descrição"]}
            linhas={ENDPOINTS.map(({ caminho, descricao }) => [
              <Badge key="m" tone="brand">
                GET
              </Badge>,
              <code key="c" className="font-mono">
                {caminho}
              </code>,
              descricao,
            ])}
          />
        </Secao>

        <Secao
          id="exemplos"
          titulo="Exemplos"
          sub="Faça sua primeira chamada em poucos passos."
        >
          <ExemplosChamada baseUrl={API_URL} />
          <div>
            <h3 className="mb-3 text-sm font-bold text-foreground">
              Resposta (ilustrativa)
            </h3>
            <CodeBlock code={RESPOSTA_EXEMPLO} />
          </div>
          <div>
            <h3 className="mb-3 text-sm font-bold text-foreground">
              Parâmetros de <code className="font-mono">/salas/vazias</code>
            </h3>
            <Tabela
              colunas={["Parâmetro", "Tipo", "Descrição"]}
              linhas={PARAMETROS_SALAS_VAZIAS.map(
                ({ nome, tipo, descricao }) => [
                  <code key="n" className="font-mono">
                    {nome}
                  </code>,
                  tipo,
                  descricao,
                ],
              )}
            />
          </div>
        </Secao>

        <Secao
          id="swagger"
          titulo="Documentação interativa (Swagger)"
          sub="Teste os endpoints direto no navegador."
        >
          <div className="overflow-hidden rounded-xl border border-border bg-white">
            <SwaggerViewer />
          </div>
        </Secao>

        <Secao
          id="sdk"
          titulo="SDK e CLI"
          sub="Use a API sem montar as requisições na mão."
        >
          <div className="flex flex-col gap-6 md:flex-row">
            <CartaoFerramenta
              titulo="SDK"
              descricao="Biblioteca Python (3.11+) para usar a API direto no seu código, com os mesmos tipos que a API devolve."
              link={SDK_URL}
            >
              <CodeBlock code={SDK_INSTALACAO} />
              <CodeBlock code={SDK_EXEMPLO} />
            </CartaoFerramenta>
            <CartaoFerramenta
              titulo="CLI"
              descricao="Comando cerradinho, instalado junto com o SDK, para consultar a API pelo terminal. A saída vem em tabela ou, com --json, em JSON."
              link={CLI_URL}
            >
              <CodeBlock code={CLI_CONFIGURACAO} />
              <CodeBlock code={CLI_EXEMPLO} />
            </CartaoFerramenta>
          </div>
        </Secao>
      </main>

      <footer className="flex flex-wrap items-center justify-between gap-3 bg-surface px-4 py-5 text-sm font-semibold text-foreground md:px-16">
        <span>Cerradinho API · dados abertos da UnB</span>
        <div className="flex gap-5">
          <a
            href={REPO_URL}
            target="_blank"
            rel="noreferrer"
            className="hover:text-brand"
          >
            GitHub
          </a>
          <a
            href={DOCS_URL}
            target="_blank"
            rel="noreferrer"
            className="hover:text-brand"
          >
            Docs da equipe
          </a>
        </div>
      </footer>
    </>
  );
}
