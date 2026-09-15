# Relatório de risco das fontes de dado

> Entrega da Sprint 1 (issue #65, segundo critério de aceitação). Responsável: João Paulo (QA/Integração).
> Fichas detalhadas por fonte: [`fonte-sigaa-disciplinas.md`](fonte-sigaa-disciplinas.md) e [`fonte-ru-cardapio.md`](fonte-ru-cardapio.md).
> Plano de monitoramento: [`plano-monitoramento-fontes.md`](plano-monitoramento-fontes.md).

---

## 1. Objetivo e escopo

O Cerradinho não produz dado próprio: tudo que a API expõe vem de páginas
institucionais que o time não controla. O risco central do projeto, portanto,
não é de implementação — é de fonte. Uma fonte que muda de layout, de URL ou de
formato quebra o produto inteiro sem que nenhum teste unitário acuse.

Este relatório verifica as duas fontes priorizadas no Release 1:

| Fonte | Requisitos dependentes | Responsável pelo scraper |
|---|---|---|
| SIGAA — consulta pública de turmas | RF01-RF05, RF17 | Vitor |
| RU — cardápio semanal | RF06, RF07, RF19 | Ítalo |

As demais fontes previstas no `REQUISITOS.md` (Eventos, Editais, CKAN de dados
abertos) ficam para o Release 2 e não foram verificadas aqui.

**Data da verificação:** 13/09/2026.

## 2. Método

1. Acesso manual às páginas e inspeção do HTML servido.
2. Identificação do formato real em que o dado é publicado.
3. Comparação entre a URL documentada no `REQUISITOS.md` e a URL efetivamente
   viva.
4. Leitura do código de scraping já escrito, para extrair as armadilhas que o
   time descobriu na prática.

Medições de latência e verificação de `robots.txt` estão previstas mas ainda não
foram executadas — ver seção 6.

## 3. Achados

### A1 — O cardápio do RU é publicado em PDF, não em HTML (severidade: alta)

A página do cardápio não contém o cardápio. Ela contém uma lista de links para
arquivos PDF, um por campus e por semana, hospedados no diretório de uploads do
WordPress:

```
https://ru.unb.br/wp-content/uploads/2026/09/Gama-Semana-04-14-9-a-20-9.pdf
https://ru.unb.br/wp-content/uploads/2026/09/Darcy-Ribeiro-Semana-03-7-9-a-13-9.pdf
```

O `REQUISITOS.md` atribui ao Ítalo a stack "FastAPI, BeautifulSoup, SQLAlchemy"
para RF06-RF07. BeautifulSoup resolve apenas a primeira metade do problema:
descobrir e listar os links. A extração do cardápio em si exige uma biblioteca
de PDF.

**Impacto:** o scraper de RU precisa de duas etapas distintas (descoberta de
links em HTML, extração de conteúdo em PDF) e de uma dependência que não estava
prevista no planejamento.

### A2 — A URL documentada está desatualizada e falha em silêncio (severidade: alta)

O `REQUISITOS.md` registra a fonte do cardápio como `ru.unb.br/cardapio`. Essa
página existe e responde normalmente, mas está congelada: em 13/09/2026 ela
ainda exibe a semana de 10/08 a 16/08, com a marcação "Atualizado em: 7/8/2026".

A página efetivamente mantida é `ru.unb.br/cardapio-refeitorio/`, que lista as
semanas de 07/09 e 14/09 para os cinco campi.

**Impacto:** um scraper apontado para a URL documentada coletaria dados de cinco
semanas atrás e retornaria HTTP 200 com HTML bem-formado. Nenhum health check de
disponibilidade detectaria isso. É o modo de falha mais perigoso do projeto —
dado errado servido com aparência de dado certo.

**Ação:** corrigir a tabela de fontes do `REQUISITOS.md` (ver seção 5).

### A3 — O PDF é extraível, mas o layout é tabular com células mescladas (severidade: média)

Boa notícia: os PDFs contêm texto real, não imagem escaneada. Não há necessidade
de OCR, o que reduz muito o custo de implementação.

Má notícia: o cardápio é uma tabela de cinco colunas (uma por dia útil) com
linhas por componente da refeição (salada, prato principal padrão,
ovolactovegetariano, vegetariano estrito, guarnição, sobremesa, bebida). Várias
células são mescladas horizontalmente — "Leite integral OU Bebida de soja" vale
a semana inteira; "Mix de doces OPÇÃO: Frutas" cobre um dia só.

Numa extração linear de texto, tudo isso vira uma sequência única, sem
indicação de qual dia cada valor cobre. Associar prato ao dia correto exige
extração **posicional**, usando as coordenadas de cada célula, e não leitura
sequencial.

**Impacto:** o parser de cardápio é substancialmente mais complexo do que um
parser de HTML tabular. Deve ser tratado como tarefa M/L, não S.

### A4 — O SIGAA exige sessão "aquecida" antes da busca (severidade: média)

Documentado pelo Vitor no próprio scraper e reproduzido aqui como risco de
fonte. O SIGAA é uma aplicação JSF que mantém um contador de views por sessão no
campo oculto `javax.faces.ViewState`. Uma sessão que começa direto na página de
busca é rejeitada com a mensagem de que a sessão não está mais ativa. A
navegação precisa passar pela home antes.

Além disso, a espera por `networkidle` nunca resolve, porque o Google Analytics
da página mantém a rede ocupada indefinidamente — é preciso usar
`domcontentloaded`.

**Impacto:** o scraper é sensível a mudanças de fluxo de navegação, não só de
layout. Uma alteração no SIGAA que mexa na sequência de páginas quebra a coleta
mesmo que os seletores continuem válidos.

### A5 — Existe host alternativo para a mesma consulta (severidade: baixa, é oportunidade)

A consulta pública de turmas responde tanto em `sigaa.unb.br` quanto em
`sig.unb.br`. Materiais de orientação da própria UnB circulam com o segundo
endereço.

**Impacto:** possível fallback automático caso um dos hosts fique indisponível.
Vale confirmar se ambos servem a mesma instância ou se um é apenas redirect,
antes de tratar como redundância real.

### A6 — Dependência de navegador headless no pipeline (severidade: média)

O scraper de disciplinas usa Playwright com Chromium. Isso significa que
qualquer ambiente que rode a coleta — máquina de desenvolvimento, container de
produção, runner de CI — precisa do binário do navegador instalado via
`playwright install`.

**Impacto:** aumenta o tempo de build e o tamanho da imagem. Reforça a decisão
de manter testes que acessem o SIGAA de verdade fora do pipeline de CI,
usando fixtures de HTML salvo para os testes de parser.

## 4. Matriz de risco

| ID | Risco | Probabilidade | Impacto | Severidade |
|---|---|---|---|---|
| A1 | Cardápio em PDF exige stack não prevista | Certo (já ocorreu) | Alto | **Alta** |
| A2 | URL documentada serve dado velho sem erro | Certo (já ocorreu) | Alto | **Alta** |
| A3 | Layout tabular com células mescladas | Certo (já ocorreu) | Médio | **Média** |
| A4 | Fluxo de sessão do SIGAA quebra a coleta | Média | Alto | **Média** |
| A5 | Indisponibilidade de um host do SIGAA | Baixa | Alto | **Baixa** |
| A6 | Navegador headless indisponível no ambiente | Baixa | Médio | **Baixa** |
| A7 | Mudança de layout entre semestres | Média | Alto | **Média** |
| A8 | Bloqueio por volume de requisições | Baixa | Alto | **Média** |

A7 e A8 não foram observados nesta verificação; entram como risco projetado,
por analogia com o comportamento típico de sistemas institucionais.

## 5. Mitigações propostas

Ligadas ao RNF05 (resiliência) e ao RNF03 (observabilidade).

| Risco | Mitigação | Requisito |
|---|---|---|
| A1 | Adotar biblioteca de extração de PDF com suporte posicional; separar descoberta de links e extração em dois módulos | RF06 |
| A2 | Corrigir URL no `REQUISITOS.md`; adicionar validação de frescor (rejeitar cardápio cuja semana não contenha a data atual) | RNF05 |
| A2 | Monitorar conteúdo, não só status HTTP — ver plano de monitoramento | RNF03 |
| A3 | Fixture de PDF real no repositório para teste de parser sem rede | RNF09 |
| A4 | Manter a navegação pela home; testes de sabotagem simulando sessão expirada | RNF05, RNF09 |
| A5 | Confirmar equivalência dos hosts e, se confirmada, implementar fallback | RNF05 |
| A6 | Testes de parser sobre fixtures; integração real fora do CI | RNF08 |
| A7 | Versionar fixtures por semestre; alerta quando seletor não encontra elemento esperado | RNF05 |
| A8 | Throttling entre requisições, já previsto no RF01 | RF01 |

**Princípio geral:** o scraper deve falhar alto e cedo. É preferível uma
exceção explícita a um registro vazio persistido no banco. Todo parser deve
validar que encontrou o que esperava encontrar, e não apenas que a requisição
retornou 200.

## 6. Pendências desta verificação

Itens levantados mas não concluídos nesta sprint:

- [ ] Medir latência e variabilidade de resposta das duas fontes ao longo de uma
      semana (ver `plano-monitoramento-fontes.md`, seção de coleta manual)
- [ ] Verificar `robots.txt` de `ru.unb.br` e `sigaa.unb.br`
- [ ] Confirmar se `sig.unb.br` e `sigaa.unb.br` são instâncias distintas
- [ ] Verificar se o padrão de nome dos PDFs do RU é estável o bastante para
      construção de URL, ou se a descoberta por link é obrigatória
- [ ] Levantar as fontes do Release 2 (Eventos, Editais, CKAN)

## 7. Correções necessárias no REQUISITOS.md

Proposta de alteração na tabela da seção 2:

| Domínio | De | Para |
|---|---|---|
| Cardápio RU | `ru.unb.br/cardapio` — Aberto, sem login | `ru.unb.br/cardapio-refeitorio` — PDF semanal por campus; a URL `/cardapio` está desatualizada |

Alteração enviada em commit separado, para manter rastreável a origem da
correção.
