# Cerradinho — Frontend

Interface Next.js para consulta pública dos dados do Cerradinho (disciplinas, cardápio do RU, professores e
salas) e futura base do portal do desenvolvedor.

## Rodando localmente

```bash
npm install
npm run dev
```

Abra [http://localhost:3000](http://localhost:3000).

## Configuração

Copie `.env.example` para `.env.local` e ajuste a URL da API caso o backend não esteja em
`http://localhost:8000`:

```bash
cp .env.example .env.local
```

## Estrutura

- `app/` — páginas (App Router)
- `components/` — componentes visuais
- `hooks/` — chamadas à API do Cerradinho (`/v1`), isoladas dos componentes visuais — ver `docs/ARQUITETURA.md`
- `lib/` — configuração de infraestrutura compartilhada (cliente Axios)

## Status

As telas de consulta (Visão Geral, Disciplinas, Cardápio, Professores e Salas) consomem a API real em `/v1`,
sem dados de exemplo. Enquanto a API carrega, as telas mostram "Carregando...". Se a API não responder, aparece um aviso de erro.

Link do protótipo de UI (Figma/mockup): [Cerradinho no Figma](https://www.figma.com/make/0xz0SuyDpsy3e05VknPfkc/Cerradinho?t=YZTahmjwBzk1zsxR-1)
