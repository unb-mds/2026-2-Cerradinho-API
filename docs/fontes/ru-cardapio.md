# Ficha da fonte: RU — cardápio semanal

> Ficha técnica de fonte de dado. Contexto e matriz de risco em
> [`relatorio-de-risco.md`](relatorio-de-risco.md).
> Verificada em 13/09/2026. URLs revistas em 27/10/2026.

## 1. Identificação

| Campo | Valor |
|---|---|
| Sistema | Site do Restaurante Universitário (WordPress + Elementor) |
| URLs | `https://ru.unb.br/cardapio/` e `https://ru.unb.br/cardapio-refeitorio/`, consultadas nessa ordem (ver seção 3) |
| Autenticação | Nenhuma |
| Formato do dado | **PDF**, um arquivo por campus e por semana |
| Formato da listagem | HTML estático |
| Requisitos atendidos | RF06, RF07, RF19 |

## 2. Como o dado é obtido

Processo em duas etapas, com tecnologias diferentes em cada uma.

**Etapa 1 — descoberta (HTML).** A página `cardapio-refeitorio` lista os PDFs
disponíveis, agrupados por campus (a página `cardapio` traz só o Darcy Ribeiro), com o intervalo de datas no texto do link:

```
### Cardápio Darcy Ribeiro
ISM – 7/9/2026 A 13/9/2026   → .../2026/09/Darcy-Ribeiro-Semana-03-7-9-a-13-9.pdf
ISM – 14/9/2026 A 20/9/2026  → .../2026/09/Darcy-Ribeiro-Semana-04-14-9-a-20-9.pdf
```

Campi publicados: Darcy Ribeiro, Ceilândia, Gama, Planaltina e Fazenda Água
Limpa. O Restaurante Executivo tem página própria.

Tipicamente há duas semanas disponíveis ao mesmo tempo: a corrente e a seguinte.
Isso é útil para o RF19 (cardápio semanal) e permite antecipar a coleta.

**Etapa 2 — extração (PDF).** Cada arquivo traz três blocos — café da manhã,
almoço e jantar — e cada bloco é uma tabela com cinco colunas, uma por dia útil
(2ª a 6ª feira), com a data no cabeçalho da coluna.

Linhas encontradas no bloco de almoço: salada 1, salada 2, molho para salada,
prato principal padrão, prato principal ovolactovegetariano, prato principal
vegetariano estrito, guarnição, acompanhamentos, sobremesa, bebida.

O bloco de jantar substitui guarnição por sopa e torrada. O de café da manhã tem
estrutura própria: bebidas, panificação, opção extra, gordura, complemento
(padrão / ovolacto / vegetariano estrito) e fruta.

Há ainda uma legenda de alérgenos no topo de cada página (cogumelo, leite e
derivados, mel, pimenta, soja, trigo/glúten, amendoim, oleaginosa, ovo, suíno),
associada às preparações por ícones. **Os ícones não sobrevivem à extração de
texto** — se o RF06 precisar dessa informação, será necessário tratar a camada
gráfica do PDF, o que aumenta bastante o escopo.

## 3. Risco A2 — a URL documentada serve dado velho

O `REQUISITOS.md` registra `ru.unb.br/cardapio`. Essa página existe e responde
HTTP 200 com HTML bem-formado, mas está congelada: em 13/09/2026 ainda exibe a
semana de 10/08 a 16/08, marcada como "Atualizado em: 7/8/2026".

Aparentemente o site migrou a publicação para a página agregadora
`cardapio-refeitorio`, mantendo as páginas por campus como legado — a de Darcy
Ribeiro deixou de ser atualizada. Há ainda um link no rodapé institucional
apontando para `ru.unb.br/index.php/cardapio`, remanescente da versão anterior
do site (Joomla).

**Por que isso é grave:** nenhum monitor de disponibilidade detectaria a falha.
A página responde, o HTML é válido, o parser encontraria um link de PDF e o PDF
existiria. O resultado seria um cardápio de cinco semanas atrás servido como
cardápio do dia.

**Mitigação obrigatória:** validar frescor no scraper. O intervalo de datas
extraído do link ou do PDF precisa conter a data corrente; se não contiver,
levantar exceção em vez de persistir.

**Atualização de 27/10/2026.** O problema se inverteu. Na semana de 19/10 a
25/10 o RU reorganizou o site com uma página por campus (`cardapio`,
`cardapio-gama`, `cardapio-ceilandia` e `cardapio-planaltina`), e a
`cardapio-refeitorio` ficou parada na semana de 12/10, o que fez a coleta
falhar. Na semana seguinte as duas voltaram a ter o PDF novo. Como não dá para
saber qual página o RU vai manter, o scraper consulta `cardapio` e depois
`cardapio-refeitorio` e usa a primeira que tiver a semana atual. Se nenhuma
tiver, a coleta falha com `ErroFonteIndisponivel`, que fica registrada no log
de execução (RF16).

## 4. Riscos

| ID | Risco | Severidade | Mitigação |
|---|---|---|---|
| A1 | Formato PDF exige stack não prevista no planejamento | Alta | Adotar extração de PDF com suporte posicional |
| A2 | Página parada serve dado velho sem erro | Alta | Consultar as duas páginas e validar o frescor |
| A3 | Tabela com células mescladas impede leitura sequencial | Média | Extração posicional por coordenadas |
| — | Ícones de alérgeno não sobrevivem à extração de texto | Média | Definir se estão no escopo do RF06 |
| — | Padrão de nome do PDF pode não ser estável | Média | Descobrir o link pela página, nunca construir a URL |
| — | Cardápio muda sem aviso prévio (declarado pelo próprio RU) | Baixa | Recoleta diária; tratar como dado indicativo |

Sobre o penúltimo item: os nomes seguem um padrão aparente
(`Campus-Semana-NN-D-M-a-D-M.pdf`), mas o número da semana é sequencial dentro
do contrato e a grafia do campus varia ("Darcy-Ribeiro", "Fazenda"). Construir a
URL a partir da data seria frágil. A descoberta pelo HTML é o caminho correto.

## 5. Janela de coleta recomendada

Publicação semanal, com a semana seguinte disponível com alguns dias de
antecedência. Coleta diária é suficiente e cobre o caso de substituição de um
PDF já publicado.

Vale registrar o hash do PDF coletado: se o arquivo mudar sem que a URL mude, é
sinal de correção de cardápio, e o histórico do RF07 precisa refletir isso.

## 6. Pendências

- [x] Escolher e testar a biblioteca de extração de PDF (pdfplumber, [ADR 0002](../adr/0002-ferramentas-de-scraping.md))
- [x] Salvar PDFs como fixture no repositório, para teste de parser sem rede (cinco semanas em `backend/tests/scrapers/fixtures/`)
- [ ] Definir com o PO se os ícones de alérgeno entram no escopo do RF06
- [ ] Verificar `robots.txt` do domínio
- [ ] Confirmar se os cinco campi seguem exatamente a mesma estrutura de tabela
