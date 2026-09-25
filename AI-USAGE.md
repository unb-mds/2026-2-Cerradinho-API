# Registro de uso de IA — Cerradinho

Conforme a política de uso de IA da disciplina (MDS 2026/2): o uso de assistentes e agentes de IA é **esperado, não tolerado**, desde que registrado. Este arquivo documenta onde e como IA foi usada no projeto.

**Não é permitido uso de IA em**: arguições individuais, quizzes, avaliação por pares, ensaio de reflexão crítica. Esses instrumentos avaliam o que cada pessoa entende individualmente.

**É esperado e deve ser registrado em**: implementação, testes, documentação, exploração de bibliotecas, refatoração.

## Formato de registro

Cada entrada deve conter: data, pessoa, ferramenta usada, o que foi pedido, o que foi aceito/rejeitado/ajustado.

## Registros

### Release 1

| Data | Pessoa | Ferramenta | O que foi feito | Aceito/ajustado/rejeitado |
|---|---|---|---|---|
| 13/09/2026 | Gabriel | Claude Code | Auxícilio no schema inicial SQLAlchemy (Professor, Sala, Disciplina, Turma, Horario, Cardapio, ajustado pra bater com o contrato de dados real do scraper de RF01 já mergeado), e correção de um bug pré-existente em `backend/pytest.ini` (`pythonpath` apontava pra um caminho que não existia) | a primeira versão modelou Disciplina/Turma como uma única tabela; após puxar o `origin/dev` e o schema já mergeado do Vitor, foi refeita como Disciplina + Turma separadas |

| 13/09/2026 | Vitor | Claude Code | Camada `app/domain/disciplinas.py` ligando o parser de RF01 (`app/schemas/disciplina.py`) aos models de banco do Gabriel: get-or-create de Disciplina/Sala/Professor, split de "PRÉDIO - SALA" e upsert de Turma+Horario pela chave natural (disciplina, numero, ano_periodo) pra não duplicar linha quando o scraper reagendar. Testes em `tests/domain/test_disciplinas.py` cobrindo criação, atualização sem duplicar, troca de professores/horários sem acumular órfão, e reaproveitamento de Sala/Professor entre turmas. Também corrigido bug pré-existente em `backend/pytest.ini` (chave `pythonpath` duplicada, que quebrava toda a suíte) | Aceito sem ajuste |
| 14/09/2026 | Daniel | Claude Code | Nas 4 telas de consulta do protótipo (Disciplinas, Cardápio, Professores, Salas): extraída a lógica de chamada de API pra `frontend/hooks/` (um hook por domínio sobre um helper `useApiResource` compartilhado, com fallback pro mock quando a API ainda não responde) e cliente Axios em `frontend/lib/api.ts`; removido o boilerplate do `create-next-app` (home, metadata, README) e aplicada estilização básica em Tailwind nas telas e na Nav | Aceito sem ajuste |
| 17/09/2026 | Daniel | Claude Code | Alinhamento dos hooks `useDisciplinas` e `useCardapioSemana` ao contrato real da API (`backend/app/schemas/`): mock reescrito no formato de `Turma`/`ItemCardapio` da API em vez do formato da tela, com função de tradução explícita pra cada um; `useCardapioSemana`/`app/cardapio/page.tsx` redesenhados de 3 campos fixos pra lista dinâmica de categorias, pra refletir a estrutura real do cardápio do RU (café da manhã não tem prato principal/sobremesa); adicionado "Sáb" ao filtro de dias em `app/disciplinas/page.tsx`; removido `app/disciplinas/route.ts` (conflitava com `page.tsx` na mesma rota) | Ajustado — a primeira função `extrairDia` só tratava dias com sufixo "-feira" (quebrava em sábado/domingo); o usuário propôs uma correção própria (`if (!descricao.includes("-feira")) return descricao`) que só mascarava o sintoma sem resolver, então foi revisada pra extrair a primeira palavra da descrição em vez de depender do sufixo |

### Release 2

| Data | Pessoa | Ferramenta | O que foi feito | Aceito/ajustado/rejeitado |
| ---- | ------ | ---------- | --------------- | ------------------------- |
| 14/09/2026 | Ítalo | Claude Code | Integração do protótipo de scraper de Cardápio do RU (RF06/RF07), testado à parte em `Backend-Testing/`, ao backend: `app/schemas/cardapio.py` (contrato `ItemCardapio`), `app/scrapers/cardapio/` (scraper.py com requests + parser.py com BeautifulSoup/pdfplumber, replicando as descobertas de layout do protótipo — tabela "fantasma", células quebradas em várias linhas, refeição identificada por categoria e não por ordem de página) e `app/domain/cardapio.py` (agrega os itens por data+refeição num bloco de texto e faz upsert no model `Cardapio` já existente, sem migration nova). Testes em `tests/domain/test_cardapio.py` e `tests/scrapers/test_cardapio_parser.py` (este com o PDF real de exemplo como fixture) | Ajustado: URL de origem trocada de `ru.unb.br/cardapio/` para `ru.unb.br/cardapio-refeitorio/` (a primeira está desatualizada — risco A2 documentado em `docs/estudos/fonte-ru-cardapio.md`); download do PDF passou a manter o conteúdo em memória em vez de gravar em disco; filtro de campus e função de seleção de PDF viraram parâmetros explícitos em vez de constantes |
| 24/09/2026 | Daniel | Gemini | Geração da arte da flor do cerrado usada como identidade visual do Cerradinho: favicon `frontend/app/icon.svg` e o desenho do componente `CerradinhoFlower` (logo da sidebar em `frontend/components/Icons.tsx`) | Aceito sem ajuste |
| 24/09/2026 | Daniel | Claude Code | Diagnóstico de por que o front não exibia dados da API em Docker: adicionado `CORSMiddleware` em `backend/app/main.py` com origens configuráveis (`cors_origins` em `backend/app/core/config.py`, padrão `localhost:3000`/`127.0.0.1:3000`) e `--reload` no serviço `api` do `docker-compose.yml` (o código já era montado por volume mas não recarregava) | Aceito sem ajuste |

## Observações gerais

- Código gerado por IA passa pela mesma revisão de PR que qualquer outro código (ver `PROCESSO.md`)
- Testes gerados por IA são revisados quanto a asserção real (não aceitar teste que só verifica "não lançou exceção")
- Dependências sugeridas por IA são conferidas antes de instalar (existe de verdade, é mantida, não é maliciosa)
