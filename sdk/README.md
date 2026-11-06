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

    try:
        agenda = cerradinho.obter_agenda(professor_id=12)
    except ProfessorNaoEncontrado:
        ...
```

`base_url` é obrigatório — não tem um padrão de produção embutido (o IP da instância ainda não é fixo, ver `docs/DEPLOY.md`). Pra testar contra um ambiente local:

```python
CerradinhoClient("http://localhost:8000")
```

## Estrutura

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
