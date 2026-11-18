# Como contribuir

Regras para levar uma mudança até a `dev`. Como o time se organiza (sprints, ritos, Definition of Done) está no [PROCESSO.md](docs/PROCESSO.md); como rodar o projeto, no [README](README.md).

## Se você não é do time

Qualquer pessoa pode contribuir, seja com código, documentação, um bug reportado ou um dado errado que encontrou. Quem participa segue o [Código de Conduta](CODE_OF_CONDUCT.md).

1. Procure uma issue aberta, de preferência com o rótulo [`good first issue`](https://github.com/unb-mds/2026-2-Cerradinho-API/labels/good%20first%20issue), e comente nela que vai trabalhar. Para algo que ainda não tem issue, abra uma antes e espere uma resposta do time, assim ninguém faz trabalho repetido.
2. Faça um fork do repositório e crie uma branch a partir da `dev`, com um nome que diga o que ela faz (ex.: `fix-sala-sem-predio`).
3. Rode o projeto e os testes antes e depois da mudança:

   ```bash
   cd backend
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements-dev.txt
   pytest
   ruff check .
   ```

   Os testes de integração precisam do Postgres do `docker compose up` e são pulados sem ele. Os detalhes estão no [README do backend](backend/README.md).
4. Abra o pull request do seu fork para a `dev`, preencha o [template](.github/PULL_REQUEST_TEMPLATE.md) e siga os padrões de commit e de código abaixo.

As seções seguintes valem para todo mundo. A de branches descreve como o time organiza o próprio trabalho, e quem vem de fora usa o fork no lugar da branch `R2-nome`.

## 1. Branches

```
main  ← estável, recebe a dev no fechamento de cada release
dev   ← integração, recebe os PRs
R2-nome  ← uma branch por pessoa na release, criada a partir da dev (ex.: R2-gabriel)
```

- Cada pessoa tem a sua branch `R2-nome`, com o primeiro nome em minúsculas, sem acento. Ela é criada uma vez, a partir da `dev` atualizada: `git switch dev && git pull && git switch -c R2-nome && git push -u origin R2-nome`.
- Todo o seu trabalho da release vai nessa branch. Cada entrega (issue) vira um PR da `R2-nome` para a `dev`, e a branch continua aberta depois do merge.
- **Não faça commit direto na `dev` nem na `main`.** Toda mudança entra por pull request, inclusive documentação e atas.
- Mantenha a branch em dia com a `dev`: antes de começar uma tarefa e antes de abrir cada PR, rode `git switch R2-nome && git pull origin dev` e resolva os conflitos na sua branch.

## 2. Commits

Mensagens em [Conventional Commits](https://www.conventionalcommits.org/pt-br/), em português:

```
tipo: descrição curta no imperativo
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

Exemplos do histórico: `feat: adiciona endpoints /v1/professores e /v1/salas`, `fix: limita concurrency do celery_worker a 1`, `docs: registra no AI-USAGE.md o ajuste de lista vazia em Professores e Salas`.

Mudança que quebra compatibilidade leva `!` depois do tipo (`feat!: ...`) e é discutida antes, por causa do versionamento da API ([ADR 0005](docs/adr/0005-api-versionada-desde-o-inicio.md)).

## 3. Pull requests

1. Abra o PR da sua branch para a **`dev`** e preencha o [template](.github/PULL_REQUEST_TEMPLATE.md).
2. Ligue a issue. Como o `Closes #N` só fecha a issue quando a mudança chega na `main`, use `Refs #N` quando a issue não termina com esse PR.
3. Peça revisão a pelo menos uma pessoa do time. **A revisão precisa estar registrada no PR**, como aprovação ou comentário. Combinado por mensagem ou de forma verbal não conta.
4. O merge só acontece com o CI verde. O pipeline roda ruff, bandit, testes unitários, testes de contrato e testes de integração com Postgres.
5. Se usou IA, registre no [AI-USAGE.md](AI-USAGE.md) no mesmo PR.

## 4. Padrões de código

### Separação de responsabilidades

- **Scrapers** só acessam a fonte; **parsers** só transformam o conteúdo no contrato Pydantic; **routers** só recebem a requisição e chamam o domínio. A tabela completa está nos [componentes do backend](docs/ARQUITETURA.md#nivel-3-componente).
- Regra de negócio (normalizar nome de professor, calcular salas vazias) fica em `app/domain/`, em um único lugar.
- Consulta ao banco passa pelo domínio e pelos models SQLAlchemy, nunca direto no router.
- No frontend, chamada à API fica nos hooks de `frontend/hooks/`, fora dos componentes visuais.

### Estilo

- Prefira retorno antecipado a condicionais aninhadas; se passar de 3 níveis de aninhamento, extraia uma função.
- Funções com mais de ~50 linhas ou arquivos com mais de ~200 linhas devem ser quebrados.
- Trate erros de forma explícita: capture a exceção esperada, não `Exception` genérica sem necessidade.
- Evite módulos genéricos como `utils.py` ou `helpers.py`. Use nomes do domínio.

### Bibliotecas

Antes de escrever algo do zero, veja se existe um pacote que resolve (por exemplo, `slowapi` para rate limit, `schemathesis` para contrato, `Typer` para a CLI). Código próprio se justifica para regra de negócio do domínio ou quando nenhuma biblioteca atende. Dependência nova precisa ser conferida antes de entrar: se o pacote existe, é mantido e é confiável. Troca de tecnologia relevante ganha um [ADR](docs/adr/template.md).

### Testes

- Todo código novo no backend vem com teste em `backend/tests/`, na pasta da camada correspondente.
- Teste precisa verificar o resultado. Teste que só confere que "não lançou exceção" não é aceito.
- Rota nova ou alterada precisa passar nos testes de contrato (`tests/contract/`).
- Mudança no banco ou em tamanho de coluna precisa passar nos testes de integração com Postgres (`tests/integration/`).
