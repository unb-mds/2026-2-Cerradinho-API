# cerradinho-sdk

Cliente Python pra [API pública da Cerradinho](https://github.com/unb-mds/2026-2-Cerradinho-API) (RF13) — pra integrar sem montar requisição HTTP na mão.

## Instalação

```bash
pip install -e sdk/  # a partir da raiz do repositório
```

Ainda não publicado no PyPI (ver `specs/RF13-*.md` pra critérios de aceitação e rastreabilidade).

## Uso

```python
from cerradinho_sdk import CerradinhoClient, ProfessorNaoEncontrado

with CerradinhoClient("https://api.<ip>.sslip.io") as cerradinho:
    turmas = cerradinho.listar_disciplinas()
    salas_vazias = cerradinho.listar_salas_vazias(dia="segunda", horario="14:00")
    cardapio = cerradinho.obter_cardapio_semana()
    resumo = cerradinho.obter_resumo()  # só as contagens, sem baixar a lista inteira

    try:
        agenda = cerradinho.obter_agenda(professor_id=12)
    except ProfessorNaoEncontrado:
        ...
```

`listar_disciplinas` e `listar_professores` aceitam busca/filtro e paginação:

```python
    pagina = cerradinho.listar_disciplinas(busca="fga", departamento="FGA", limite=20, offset=0)
    docentes = cerradinho.listar_professores(nome="andre", limite=10)
```

O total depois do filtro vem no cabeçalho `X-Total-Count` da resposta HTTP,
que esta versão do SDK não expõe — pagine conferindo se a página voltou
mais curta que o `limite` pedido.

`base_url` é obrigatório — não tem um padrão de produção embutido (o IP da instância ainda não é fixo, ver `docs/DEPLOY.md`). Pra testar contra um ambiente local:

```python
CerradinhoClient("http://localhost:8000")
```

## CLI

A instalação do SDK também instala o comando `cerradinho`, para consultar a API pelo terminal sem escrever código. A CLI chama os métodos do `CerradinhoClient` e só formata a resposta. Também dá para rodar com `python -m cerradinho_sdk`.

```bash
pip install -e sdk/
export CERRADINHO_API_URL=https://api.<ip>.sslip.io   # ou --base-url em cada comando
cerradinho --help
```

| Comando | O que mostra |
|---|---|
| `cerradinho disciplinas [--busca TEXTO] [--departamento FGA] [--limite N] [--offset N]` | Turmas do período, com professores, horários, sala e vagas |
| `cerradinho professores [NOME]` | Docentes e o id de cada um, usado em `agenda` |
| `cerradinho agenda PROFESSOR_ID` | Agenda semanal do professor, com a sala de cada aula |
| `cerradinho salas` | Salas com aula no período |
| `cerradinho salas-vazias DIA HH:MM` | Salas sem turma no dia e horário, ex. `salas-vazias segunda 14:00` |
| `cerradinho cardapio [--data-inicio AAAA-MM-DD]` | Cardápio do RU dos 7 dias a partir da data (padrão: hoje) |
| `cerradinho execucoes [--limite N]` | Últimas execuções dos scrapers, com sucesso ou falha |
| `cerradinho resumo` | Total de turmas, disciplinas, professores e salas |

Opções gerais, antes do comando:

- `--json`: imprime a resposta da API em JSON, para usar com `jq` ou em scripts. Ex.: `cerradinho --json salas-vazias segunda 14:00 | jq '.[].nome'`.
- `--timeout SEGUNDOS`: tempo máximo de cada requisição (padrão: 30).
- `--version`: versão do SDK e da CLI.

Erros da API (professor inexistente, API fora do ar, limite de requisições, rota que a API no ar ainda não tem) saem como uma mensagem curta, com código de saída 1. Argumento inválido, como um dia da semana que não existe, sai com código 2, sem chamar a API.

## Estrutura

- `cerradinho_sdk/cli.py` — a CLI `cerradinho`, com [Typer](https://typer.tiangolo.com/). Um comando por método do `CerradinhoClient`, sem chamada HTTP própria.
- `cerradinho_sdk/client.py` — `CerradinhoClient`, a interface pública do SDK: métodos simples, um por endpoint de `/v1/`, tipados pelos mesmos modelos que a API devolve. **Escrito à mão** — é aqui que qualquer mudança na interface do SDK (ex. a combinada com a CLI) acontece.
- `cerradinho_sdk/_gerado/` — cliente HTTP de baixo nível, **gerado** a partir do OpenAPI que o backend expõe (RF11), via [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client). Não edite à mão.
- `scripts/gerar_cliente.sh` — regera `_gerado/` a partir do schema atual do backend. Rode depois de qualquer mudança num router (`backend/app/routers/`):

  ```bash
  sdk/scripts/gerar_cliente.sh
  ```

  Revise o diff antes de commitar — o gerador reescreve o diretório inteiro, incluindo formatação.

O SDK é um cliente fino: ele só encapsula as chamadas a `/v1/` e espelha os schemas que a API já devolve, sem recalcular nada que o backend já computa (salas vazias, agenda do professor).

## Testes

```bash
pip install -e sdk/[dev]
pytest sdk/tests
```

Os testes rodam contra respostas HTTP mockadas (`respx`), nunca contra a API em produção.

## Versionamento

A versão do SDK (`cerradinho_sdk.__version__`) acompanha a versão da API que ele cobre (RF12) — hoje, `/v1/` (`1.0.0`). Uma mudança incompatível em `/v1/` → `/v2/` exige uma versão maior nova do SDK, não um remendo de compatibilidade silencioso.
