# Como contribuir

Obrigado pelo interesse no Cerradinho. Toda contribuição ajuda, seja código, documentação, um bug reportado ou um dado errado que você encontrou. Quem participa segue o [Código de Conduta](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/CODE_OF_CONDUCT.md).

## Antes de começar

- **Bug ou dado errado:** abra uma [issue](https://github.com/unb-mds/2026-2-Cerradinho-API/issues/new/choose) contando o que aconteceu e como reproduzir.
- **Falha de segurança:** não abra issue pública. Siga a [política de segurança](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/SECURITY.md).
- **Ideia nova:** abra uma issue de feature e espere uma resposta antes de escrever o código, assim ninguém faz trabalho repetido ou fora do escopo.
- **Quer só programar?** Procure as issues com [`good first issue`](https://github.com/unb-mds/2026-2-Cerradinho-API/labels/good%20first%20issue) e comente que vai pegar.

## Passo a passo

1. Faça um fork do repositório e clone o seu fork.
2. Crie uma branch a partir da `dev`, com um nome que diga o que ela faz:

   ```bash
   git switch dev
   git switch -c fix-sala-sem-predio
   ```

3. Prepare o ambiente da parte que você vai mexer (veja abaixo) e rode os testes antes de mudar qualquer coisa.
4. Faça a mudança, com testes, e rode os testes de novo.
5. Abra o pull request do seu fork para a `dev` e preencha o template.

A `main` recebe a `dev` a cada versão. Pull requests vão sempre para a `dev`.

## Preparando o ambiente

### Backend (API, scrapers, Celery)

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
playwright install chromium
pytest
ruff check .
bandit -r app -lll
```

Os testes de integração precisam do Postgres do `docker compose up` e são pulados sem ele. Os detalhes estão no [README do backend](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/backend/README.md).

### Frontend (site)

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
npm run lint
```

### SDK e CLI

```bash
cd sdk
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
```

Se o contrato da API mudar, regenere o cliente com `sdk/scripts/gerar_cliente.sh`. O [README do SDK](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/sdk/README.md) explica como.

## Commits

Mensagens em [Conventional Commits](https://www.conventionalcommits.org/pt-br/), em português e no imperativo:

```
tipo: descrição curta
```

| Tipo | Quando usar |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Só documentação |
| `test` | Adiciona ou corrige testes |
| `refactor` | Muda o código sem mudar o comportamento |
| `build` | Dependências e build |
| `ci` | Pipeline de CI |
| `chore` | Manutenção que não afeta o código (configuração, templates) |

Exemplos: `feat: adiciona endpoints /v1/professores e /v1/salas`, `fix: aceita a data entre parenteses no pdf do cardapio do RU`.

Mudança que quebra quem já usa a API leva `!` depois do tipo (`feat!: ...`) e precisa ser discutida numa issue antes, porque a API é versionada ([ADR 0005](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/0005-api-versionada-desde-o-inicio.md)).

## Pull requests

- Um assunto por PR. Mudanças grandes ficam mais fáceis de revisar em PRs menores.
- Ligue a issue com `Closes #N`, ou `Refs #N` quando o PR resolve só uma parte.
- O CI precisa ficar verde. Ele roda ruff, bandit, testes unitários, testes de contrato e testes de integração com Postgres.
- Pelo menos uma pessoa que mantém o projeto revisa antes do merge. A revisão fica registrada no próprio PR.
- Mudança visual vem com print do antes e do depois.

## Padrões de código

### Onde cada coisa fica

- **Scrapers** só acessam a fonte. **Parsers** só transformam o conteúdo no contrato Pydantic. **Routers** só recebem a requisição e chamam o domínio. A tabela completa está nos [componentes do backend](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/ARQUITETURA.md#nivel-3-componente).
- Regra de negócio, como normalizar o nome de um professor ou calcular salas vazias, fica em `app/domain/`, num lugar só.
- Consulta ao banco passa pelo domínio e pelos models SQLAlchemy, nunca direto no router.
- No frontend, chamada à API fica nos hooks de `frontend/hooks/`, fora dos componentes visuais.

### Estilo

- Prefira retorno antecipado a condicionais aninhadas. Passou de 3 níveis, extraia uma função.
- Funções com mais de 50 linhas ou arquivos com mais de 200 linhas devem ser quebrados.
- Trate erros de forma explícita. Capture a exceção esperada, não `Exception` genérica.
- Evite módulos genéricos como `utils.py` ou `helpers.py`. Use nomes do domínio.

### Dependências

Antes de escrever algo do zero, veja se existe um pacote mantido que resolve, como `slowapi` para rate limit ou `Typer` para a CLI. Dependência nova precisa ser conferida: se o pacote existe, é mantido e é confiável. Troca de tecnologia relevante ganha um [ADR](https://github.com/unb-mds/2026-2-Cerradinho-API/blob/dev/docs/adr/template.md).

### Testes

- Código novo no backend vem com teste em `backend/tests/`, na pasta da camada correspondente.
- Teste precisa verificar o resultado. Teste que só confere que "não lançou exceção" não é aceito.
- Rota nova ou alterada precisa passar nos testes de contrato (`tests/contract/`).
- Mudança no banco ou em tamanho de coluna precisa passar nos testes de integração com Postgres (`tests/integration/`).

## Uso de IA

Pode usar ferramentas de IA. Você continua responsável pelo código: revise, rode os testes e conte no PR o que a IA fez.
