# Cerradinho — Frontend

Site de demonstração em Next.js. O produto do Cerradinho é a API, e este site existe só para mostrar uma aplicação
real do que dá para fazer com ela: home do campus Gama, disciplinas, professores e agenda, salas vazias, cardápio do RU e
o portal do desenvolvedor. Ele usa apenas as rotas públicas de `/v1`, como qualquer outro cliente.

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

## Comportamento

Todas as telas consomem a API real em `/v1`, sem dados de exemplo. Enquanto a API carrega, as telas mostram "Carregando...". Se a API não responder, aparece um aviso de erro.

Protótipo de UI: [Cerradinho no Figma](https://www.figma.com/design/6LIOBmUcLfMeyCCD4mKbKY/Cerradinho-API?node-id=0-1&t=AsgTNL9BLDTmmhxe-1)
