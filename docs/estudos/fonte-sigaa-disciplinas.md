# Ficha da fonte: SIGAA — consulta pública de turmas

> Ficha técnica de fonte de dado. Contexto e matriz de risco em
> [`relatorio-risco-fontes.md`](relatorio-risco-fontes.md).
> Verificada em 13/09/2026.

## 1. Identificação

| Campo | Valor |
|---|---|
| Sistema | SIGAA (Sistema Integrado de Gestão de Atividades Acadêmicas) |
| URL de entrada | `https://sigaa.unb.br/sigaa/public/` |
| URL da consulta | `https://sigaa.unb.br/sigaa/public/turmas/listar.jsf?aba=p-ensino` |
| Host alternativo | `https://sig.unb.br/sigaa/public/turmas/listar.jsf` |
| Autenticação | Nenhuma — consulta pública |
| Tecnologia | JavaServer Faces (JSF), com postback e `ViewState` |
| Formato do dado | HTML renderizado no servidor |
| Requisitos atendidos | RF01, RF02, RF03, RF04, RF05, RF17 |

## 2. Como o dado é obtido

A página serve um formulário com quatro campos obrigatórios:

| Campo | Seletor | Valores |
|---|---|---|
| Nível de ensino | `formTurma:inputNivel` | `G` (graduação), `F`, `L`, `R`, `S`, `E` (mestrado), `D` (doutorado) |
| Unidade | `formTurma:inputDepto` | Código numérico do departamento (ex.: `673` = Campus UnB Gama / FCTE) |
| Ano | `formTurma:inputAno` | Ano letivo com quatro dígitos |
| Período | `formTurma:inputPeriodo` | Período do ano letivo |

O envio é feito pelo botão `input[type="submit"][value="Buscar"]`. O resultado
volta na mesma página, como postback.

A lista de unidades disponíveis pode ser lida do próprio HTML do formulário, sem
executar nenhuma busca — o `select` de unidade já traz todas as opções. Isso
permite descobrir dinamicamente os códigos de departamento em vez de mantê-los
fixos no código.

## 3. Por que Playwright e não requisição HTTP simples

Três motivos, em ordem de importância:

1. **Sessão com estado.** O JSF mantém um `ViewState` por sessão. Reproduzir o
   postback via requisição HTTP exigiria extrair e reenviar esse token a cada
   passo, além de gerenciar cookies de sessão manualmente.
2. **Aquecimento de sessão.** Ver risco A4 abaixo.
3. **Superfície de manutenção.** Um erro de token gera a mesma mensagem genérica
   de sessão expirada que um erro de fluxo, o que torna a depuração cara.

## 4. Armadilhas conhecidas

### 4.1 Sessão precisa ser aquecida

Uma sessão que nasce direto na página de busca é rejeitada. O contador de views
do JSF (`javax.faces.ViewState`, valores como `j_id1`, `j_id6`) começa baixo
demais, e o botão Buscar responde com erro de sessão inativa.

**Solução adotada:** visitar `sigaa.unb.br/sigaa/public/` antes de navegar para
a página de busca.

### 4.2 `networkidle` nunca resolve

O Google Analytics embutido na página mantém requisições em curso
indefinidamente. Esperar por rede ociosa trava o scraper.

**Solução adotada:** esperar por `domcontentloaded`.

### 4.3 Mensagem de erro vem com escape Unicode

O SIGAA grava a mensagem de sessão expirada com escape (`n\u00e3o` em vez de
`não`). Uma comparação por string acentuada nunca casa.

**Solução adotada:** comparar por trecho sem acento (`mais ativa`) ou por
`viewexpired`.

## 5. Riscos

| ID | Risco | Severidade | Mitigação |
|---|---|---|---|
| A4 | Mudança no fluxo de navegação quebra a coleta mesmo com seletores válidos | Média | Testes de sabotagem simulando sessão expirada |
| A5 | Indisponibilidade do host | Baixa | Avaliar `sig.unb.br` como fallback |
| A6 | Dependência de Chromium headless no ambiente | Baixa | Testes de parser sobre fixtures de HTML |
| A7 | Mudança de layout entre semestres | Média | Versionar fixtures; alertar quando seletor não encontra elemento |
| A8 | Bloqueio por volume de requisições | Média | Throttling entre unidades, já previsto no RF01 |

Os seletores usados (`formTurma:inputNivel` e afins) são baseados em atributos
`name` gerados pelo JSF a partir da estrutura do formulário. São mais estáveis
que seletores posicionais, mas mudam se a UnB atualizar a versão do SIGAA e o
formulário for reestruturado.

## 6. Janela de coleta recomendada

A oferta de turmas muda com baixa frequência fora dos períodos de matrícula e
ajuste. Uma coleta diária é suficiente para o Release 1, preferencialmente em
horário de baixa demanda, para não competir com estudantes durante matrícula.

Durante o período de ajuste de matrícula a oferta muda várias vezes ao dia — vale
avaliar coleta mais frequente nessas janelas específicas, se isso não implicar
carga significativa sobre o servidor da UnB.

## 7. Pendências

- [ ] Medir latência típica da busca completa por unidade
- [ ] Confirmar se `sig.unb.br` e `sigaa.unb.br` são a mesma instância
- [ ] Verificar `robots.txt` do domínio
- [ ] Levantar o número total de unidades, para dimensionar o tempo de uma coleta completa
