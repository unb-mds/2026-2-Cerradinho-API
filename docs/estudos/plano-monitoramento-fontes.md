# Plano de monitoramento das fontes de dado

> Deriva do [`relatorio-risco-fontes.md`](relatorio-risco-fontes.md).
> Atende RNF03 (observabilidade) e apoia RNF05 (resiliência).
> Responsável: João Paulo (QA/Integração).

---

## 1. O problema que este plano resolve

Monitorar disponibilidade não basta. O achado A2 do relatório de risco mostra
por quê: a página `ru.unb.br/cardapio` responde HTTP 200, com HTML válido, e
serve dado de cinco semanas atrás. Qualquer monitor de uptime convencional
marcaria essa fonte como saudável.

O monitoramento precisa, portanto, de três camadas com perguntas diferentes:

| Camada | Pergunta | Detecta |
|---|---|---|
| Disponibilidade | A fonte responde? | Queda do servidor, DNS, certificado |
| Estrutura | A página ainda tem o formato esperado? | Mudança de layout, seletor ausente |
| Frescor | O dado é recente? | Publicação interrompida, URL abandonada |

A terceira é a que falta na maioria dos projetos e a que teria pego o A2.

## 2. Camada 1 — disponibilidade

Ferramenta prevista: UptimeRobot (plano gratuito).

| Monitor | Alvo | Intervalo | Alerta |
|---|---|---|---|
| SIGAA home | `sigaa.unb.br/sigaa/public/` | 5 min | 2 falhas consecutivas |
| SIGAA busca | `sigaa.unb.br/sigaa/public/turmas/listar.jsf` | 5 min | 2 falhas consecutivas |
| RU cardápio | `ru.unb.br/cardapio-refeitorio/` | 15 min | 2 falhas consecutivas |

Exigir duas falhas consecutivas evita alerta por instabilidade momentânea.

**Limite conhecido:** essa camada só responde "o servidor está de pé". Serve para
distinguir "o scraper falhou porque a fonte caiu" de "o scraper falhou por bug
nosso" — que é exatamente a informação necessária na hora de triar um incidente.

## 3. Camada 2 — estrutura

Verificação executada junto com a coleta, não em serviço separado. A regra é:
**todo parser valida o que esperava encontrar antes de persistir.**

Invariantes a verificar no SIGAA:

- O `select` de unidades existe e retorna pelo menos uma opção
- Os quatro campos do formulário estão presentes
- A resposta da busca não contém marcador de sessão expirada
- O resultado tem ao menos uma turma, para unidade sabidamente ativa

Invariantes a verificar no RU:

- A página lista ao menos um link de PDF por campus esperado
- Cada link tem intervalo de datas reconhecível no texto
- O PDF baixado contém os três blocos de refeição
- A tabela extraída tem cinco colunas de dia

Quando uma invariante falha, o comportamento correto é levantar exceção e não
gravar nada. Registro parcial no banco é pior que registro ausente: a API passa
a servir dado incompleto com aparência de dado completo.

## 4. Camada 3 — frescor

A verificação decisiva, derivada do achado A2.

**Cardápio do RU.** O intervalo de datas do cardápio coletado precisa conter a
data corrente. Se o scraper rodar em 13/09 e o cardápio mais recente cobrir
10/08 a 16/08, a fonte está abandonada — falhar explicitamente.

Tolerância sugerida: alerta se o cardápio mais recente terminar há mais de sete
dias.

**Oferta de disciplinas.** O ano e o período retornados precisam corresponder ao
semestre letivo corrente. Coletar a oferta de 2026.1 em pleno 2026.2 é o mesmo
tipo de falha silenciosa.

**Registro de última coleta bem-sucedida.** Guardar o timestamp da última coleta
válida por fonte e expor isso na API (por exemplo, em um endpoint de health ou
como metadado da resposta). Consumidor que sabe quando o dado foi coletado pode
decidir se confia nele — e isso conversa diretamente com RNF07 (documentação
viva).

## 5. Coleta manual de linha de base

Antes de automatizar, medir. Uma semana de amostragem para ter números reais de
latência e estabilidade, em vez de suposições.

Comandos para executar localmente, fora do ambiente do projeto:

```bash
# Latência e status, uma medição
curl -sS -o /dev/null \
  -w "http=%{http_code} dns=%{time_namelookup}s conexao=%{time_connect}s total=%{time_total}s\n" \
  https://ru.unb.br/cardapio-refeitorio/

# robots.txt das duas fontes
curl -sS https://ru.unb.br/robots.txt
curl -sS https://sigaa.unb.br/robots.txt

# Amostragem: 10 medições espaçadas, registrando data e hora
for i in $(seq 1 10); do
  printf "%s " "$(date -Iseconds)"
  curl -sS -o /dev/null -w "%{http_code} %{time_total}\n" \
    https://sigaa.unb.br/sigaa/public/turmas/listar.jsf
  sleep 60
done | tee linha-de-base-sigaa.txt
```

Dados a consolidar no relatório de risco ao final da amostragem:

- Latência mediana e pior caso, por fonte
- Ocorrência de erro 5xx no período
- Variação entre horário de pico e madrugada
- Existência e conteúdo do `robots.txt`

Repetir a amostragem durante o período de matrícula, quando o SIGAA está sob
carga alta — é o cenário em que a coleta tem mais chance de falhar e o momento
em que o dado é mais requisitado.

## 6. Resposta a incidente

Quando um alerta disparar:

1. Identificar a camada que falhou. Disponibilidade indica problema na UnB;
   estrutura ou frescor indicam mudança na fonte, que exige mudança no código.
2. Verificar manualmente antes de mexer em código. Instabilidade institucional é
   comum e frequentemente se resolve sozinha.
3. Se for mudança de estrutura, salvar o HTML ou PDF novo como fixture **antes**
   de corrigir o parser. A fixture vira o teste de regressão.
4. Registrar o incidente e a causa. O histórico de quebras é o que permite
   estimar, no Release 2, quão volátil cada fonte realmente é.

## 7. Escopo desta sprint

Entregue agora:

- [x] Definição das três camadas
- [x] Alvos e intervalos de monitoramento
- [x] Invariantes de estrutura por fonte
- [x] Regras de frescor
- [x] Procedimento de coleta de linha de base

Pendente para as próximas sprints:

- [ ] Configuração efetiva dos monitores no UptimeRobot
- [ ] Execução da amostragem de uma semana
- [ ] Implementação das invariantes nos scrapers (depende dos scrapers existirem)
- [ ] Endpoint de health expondo a última coleta bem-sucedida
