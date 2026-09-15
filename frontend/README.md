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

Protótipo em desenvolvimento (Sprint 1): telas de consulta com dados de exemplo, que os hooks trocam
automaticamente pela resposta real assim que os endpoints correspondentes do backend estiverem disponíveis.

Link do protótipo de UI (Figma/mockup): _a definir_.
