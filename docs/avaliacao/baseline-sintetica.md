---
title: Baseline simulada do processo atual — Guardião de Gates de M&A
language: pt-BR
version: '1.0'
research_date: '2026-11-17'
status: pesquisa_documental_e_modelagem_sintetica
process_condition: B0_processo_humano_de_referencia
empirical_company_baseline: false
units: minutos_pessoa_por_solicitacao
---

# Baseline simulada do processo atual em M&A

## 1. Resumo e instruções ao agente

Este documento entrega uma baseline numérica utilizável em simulação acadêmica para o projeto **Guardião de Gates de M&A**, do IBMEC. Abrange tempo por tarefa, erros, revisões e intervenções humanas na análise de solicitações de informação ou ação entre comprador e empresa alvo antes do fechamento.

**A baseline é sintética, informada por pesquisa documental; não é uma medição empresarial.** Há evidência quantitativa para a ordem de grandeza da revisão documental. A decomposição das tarefas, as taxas de erro por solicitação, a frequência de retrabalho e a quantidade de intervenções são hipóteses de modelagem, pois as fontes examinadas não medem diretamente esse fluxo.

Valores centrais esperados sob as premissas deste documento:

| Indicador | Baseline central sintética | Denominador/unidade |
|---|---:|---|
| Esforço sem especialista e sem retrabalho | 57,90 | minutos pessoa/solicitação |
| Esforço completo, com especialista e retrabalho | **75,81** | minutos pessoa/solicitação |
| Solicitações com erro inicial | **11,80%** | todas as solicitações simuladas |
| Solicitações com erro residual após controles | **3,55%** | todas as solicitações simuladas |
| Solicitações com pelo menos uma rodada adicional | **17,50%** | todas as solicitações simuladas |
| Rodadas adicionais | **0,21975** | rodadas/solicitação |
| Revisões, incluindo controle inicial e especialista | **1,52975** | eventos de revisão/solicitação |
| Participações humanas operacionais | **3,74950** | eventos humanos distintos/solicitação |
| Solicitações com participação humana | **100%** | processo B0 humano |
| Solicitações com especialista | **31%** | todas as solicitações simuladas |

Esses valores são **expectativas matemáticas**, calculadas dos parâmetros abaixo; não são resultados de uma execução Monte Carlo nem médias publicadas. Uma rodada finita pode apresentar outros valores.

### Regras obrigatórias de utilização

1. Identificar tabelas e gráficos como “simulação acadêmica com parâmetros sintéticos informados por literatura”.
2. Preservar `origem_dado=sintetico`, versão, semente, cenário e fontes de referência nos resultados.
3. Não converter F1 em taxa de solicitações erradas. Não usar erros de IA como erros humanos.
4. Não usar a baseline técnica JEV versus LLM dos notebooks como B0 empresarial.
5. Não preencher automaticamente o desempenho do Guardião com reduções de tempo de fornecedores. B1 deve ser medido no protótipo ou receber hipóteses próprias explicitamente identificadas.
6. Manter aprovação humana e restrições da política nas duas condições quando exigidas pelo caso. Menor participação humana não significa, isoladamente, melhor resultado.
7. Não apresentar o processo reconstruído como rotina observada de uma empresa, nem afirmar que houve entrevistas próprias.

## 2. Recorte extraído dos arquivos do projeto

Foram consultados os documentos locais:

- [visao-geral-do-projeto.docx](../visao-geral/visao-geral-do-projeto.docx);
- [diagnostico-da-referencia.docx](../historico/diagnostico-da-referencia.docx);
- [problema-e-tarefa.md](../pesquisa/problema-e-tarefa.md);
- [baseline-sintetica.md](baseline-sintetica.md).

O material existente descreve quatro ferramentas simuladas: leitura de documento, solicitação de preços, proposta de migração e envio de e-mail. O diagnóstico aponta ausência de uma baseline empresarial observada. A pesquisa anterior oferece referências e protocolo de coleta, mas deixa os parâmetros a medir. Este documento **complementa** essa pesquisa para atender ao uso em simulação autorizado pelo pesquisador; não substitui os documentos anteriores.

**Unidade:** uma solicitação identificada, com documento ou dado, finalidade, destinatário, fase e ação pretendida. Uma solicitação pode receber negativa; negativa corretamente registrada é desfecho válido.

**Início:** recebimento do pedido. **Fim:** decisão e desfecho registrados, com execução simulada quando autorizada ou comunicação de negativa. Cada pedido tem uma ação principal; pedidos com várias ações devem ser divididos e correlacionados.

**B0:** processo de referência executado por pessoas, com ferramentas convencionais de consulta, comunicação e registro. Isso é uma escolha experimental, não evidência de que a organização real não usa IA.

Não estão incluídos negociação do preço da aquisição, revisão integral de todos os contratos de uma operação, elaboração de notificação regulatória nem implementação efetiva de migração. Um pedido de migração pode terminar em impedimento. Não se contabilizam horas de migração como esforço de triagem.

## 3. Pesquisa na internet: método e evidências

### 3.1 Método e critérios

Pesquisa exploratória consultada em **17/11/2026**, em português e inglês, com buscas sobre tempo de revisão de contratos, desempenho humano, solicitações de due diligence, clean teams, revisão e supervisão. Foram examinados relatórios originais, artigos, preprints, órgãos públicos e universidade; referências dos arquivos locais foram reabertas para verificação.

Exemplos de consultas: `human contract review time accuracy LawGeex 2018`, `Better Call GPT 43.46 56.17`, `due diligence information requests manual review clean team revisions time study M&A`, `site.ftc.gov Avoiding antitrust pitfalls review`, além de navegação direta às fontes abaixo.

Critérios: relação com pelo menos uma dimensão solicitada; unidade de medida identificável; fonte original ou institucional; distinção entre estudo quantitativo e orientação de processo. Não é revisão sistemática nem busca exaustiva. Não se encontrou, nas fontes examinadas, uma base que reúna os quatro indicadores para a mesma tarefa do projeto.

### 3.2 Evidências quantitativas e sua transferência

| ID | Fonte e desenho | Evidência verificada | Aplicação e limite |
|---|---|---|---|
| E1 | [LawGeex, 2018, relatório original](https://images.law.com/contrib/content/uploads/documents/397/5408/lawgeex.pdf), pp. 6–9 e 14–15; 20 advogados, cinco NDAs | Humanos: média de 92 min para o lote; extremos de 51 e 156 min. Resultado humano médio de 85%, calculado por F-measure | Referência para leitura e identificação de questões. Estudo do fornecedor, documentos curtos e contexto estrangeiro; não cronometra aprovação de compartilhamento |
| E2 | [Martin et al., Better Call GPT, 2024, v1](https://arxiv.org/html/2401.16212v1), seções 3.3 e 4.2, tabelas 2–4; dez contratos de compras dos EUA/Nova Zelândia | Minutos/documento: sênior 43,46; júnior 56,17; LPO 201. Júnior: precisão 0,876, recall 0,845 e F1 0,860 na identificação | Apoia amplitude dos tempos e definição de qualidade. Preprint de autores da Onit; revisão contratual não equivale à autorização de pedido |
| E3 | [Whitehouse et al., Better Bill GPT, 2025, v1](https://arxiv.org/html/2504.02881v1), resumo e seção 4 | Revisão humana de faturas: 194–316 segundos por fatura; melhor grupo de advogados experientes com 72% de acerto na aprovação | Evidência de que microtarefas de conferência podem durar minutos e de que decisão humana admite divergência. Outro objeto e preprint da Onit; 28% de discordância não é taxa de erro de M&A |
| E4 | [Magesh et al., 2025, Journal of Empirical Legal Studies](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf), resumo, DOI 10.1111/jels.12413 | Avaliação de ferramentas de pesquisa jurídica com alucinações entre 17% e 33% | Justifica avaliar qualidade e verificação em B1. Mede ferramentas de IA, não pessoas nem compartilhamento de informação; não alimenta taxas de B0 |
| E5 | [Bayes Business School, 22/06/2024](https://www.bayes.citystgeorges.ac.uk/news-and-events/news/2024/june/cautious-m-and-a-investors-investing-in-extensive-due-diligence) | Mais de 900 transações anunciadas em 2013–2023; média de 203 dias entre abertura do VDR e anúncio, ante 124 na análise anterior; 30 entrevistas | Contexto de duração e dependências. Dados proprietários Intralinks; não são minutos de trabalho nem espera por solicitação |

**Derivação D1:** 92/5 = **18,4 min por NDA**, média aritmética do lote de E1. Não são tempos individuais observados. A referência inspira o valor central de 18 min da análise simples, mas arredondamento e transferência para a tarefa do projeto são escolhas de modelagem.

A análise moderada de 35 min fica entre a referência curta de D1 e os 43,46–56,17 min de revisão completa de E2. A análise complexa de 60 min aproxima-se dessa última ordem de grandeza e admite cauda superior. **Esses 35 e 60 min não foram publicados para pedidos de M&A**: pressupõem análise focalizada e complexidade crescente. O valor de 201 min não integra o cenário central por se referir a outro grupo e organização do trabalho.

### 3.3 Evidências sobre revisões e intervenções

| ID | Fonte original | O que sustenta | O que não fornece |
|---|---|---|---|
| E6 | [Hendrycks et al., CUAD, 2021, v2](https://arxiv.org/html/2103.06268v2), apêndice A.2 | 510 contratos, 41 categorias; treinamento de 70–100 h; anotação, busca de omissões, revisão por categoria e advogados, consenso e exame iterativo de sugestões adicionais | Frequência operacional de retrabalho ou minutos por revisão de pedido. Treinamento é preparação, não esforço recorrente |
| E7 | [Cade, Guia de consumação prévia, 2015](https://cdn.cade.gov.br/Portal/centrais-de-conteudo/publicacoes/guias-do-cade/gun-jumping-versao-final.pdf), seções 2.1–2.6 | No modelo descrito: segregação de equipes, classificação de informação, comunicações escritas e registro do fluxo | Número universal de aprovadores, taxa de erros ou duração de tarefa. Guia orientador; a aplicação depende do caso |
| E8 | [FTC, 20/03/2018](https://www.ftc.gov/enforcement/competition-matters/2018/03/avoiding-antitrust-pitfalls-during-pre-merger-negotiations-due-diligence) | Minimização de informações, clean teams, acesso restrito, agregação e exame jurídico de relatórios antes da disseminação | Percentual de pedidos escalados ou tempo de aprovação. Contexto dos EUA, usado como referência comparativa de processo |
| E9 | [NIST, AI RMF Playbook — Measure](https://airc.nist.gov/airmf-resources/playbook/measure/), Measure 2.8 | Documentar supervisão, intervenções que alteram resultados, erros, adjudicação e escaladas | Benchmark de produtividade. Fundamenta registro e avaliação, não taxas numéricas |
| E10 | [Bang et al., ContractScrub, 20/08/2026, v1](https://arxiv.org/html/2608.20204v1), resumo e seção 1 | Define revisão final de inconsistências como tarefa específica e apresenta benchmark construído por especialistas | Baseline humana de solicitações. Não transpor erros inseridos no benchmark para prevalência natural; autores ligados à Thomson Reuters e Imperial College |

As fontes sustentam a **existência e natureza** das verificações. Não sustentam empiricamente os percentuais de 5%, 60% ou 100% de especialista, nem as taxas de retrabalho escolhidas abaixo.

## 4. Proveniência e força dos parâmetros

| Código | Significado | Exemplo |
|---|---|---|
| PUBLICADO | Valor explicitamente encontrado na fonte, preservando sua unidade | 92 min para cinco NDAs |
| DERIVADO | Operação matemática sobre valor publicado | 18,4 min por NDA como média do lote |
| HIPOTESE | Escolha sintética compatível com a tarefa e motivada pela pesquisa | 18 min para análise de pedido simples; erro inicial de 8% |
| EXPECTATIVA | Cálculo analítico sobre hipóteses | 75,8115 min pessoa/solicitação |
| OBSERVADO_LOCAL | Medição futura no processo ou experimento | Não disponível nesta entrega |

**Todos os parâmetros das seções 5–9 são HIPOTESE, salvo resultados identificados como EXPECTATIVA.** A evidência de tempo é indireta; a confiança de transferência é baixa a moderada. A confiança nas taxas de erro, revisões, composição da carteira e filas é baixa, pois não há calibração local. Faixas de cenário não são intervalos estatísticos de confiança.

## 5. Carteira e tempo por tarefa

### 5.1 Classes sintéticas

| Classe | Peso | Exemplo | Regra de escopo |
|---|---:|---|---|
| simples | 60% | Pedido completo para leitura ou compartilhamento já previsto em política, com material curto | Análise focalizada e destinatário conhecido |
| moderada | 30% | Necessidade de conferir restrições, finalidade, destinatário ou preparar versão reduzida | Maior interpretação; possível especialista |
| complexa | 10% | Dados individualizados sensíveis, dúvida de alçada, pedido de integração ou conflito de contexto | Análise especializada e possibilidade de negativa |

Os pesos são premissas de uma carteira didática, não distribuição de mercado. Complexidade não determina se uma ação é proibida: a referência de decisão deve ser atribuída separadamente por caso.

### 5.2 Tempos centrais determinísticos

| Etapa | Responsável proposto | Simples | Moderada | Complexa | Motivação |
|---|---|---:|---:|---:|---|
| T1 Receber, identificar e registrar o pedido | Analista | 3 | 5 | 8 | Hipótese de conferência de campos e material |
| T2 Confirmar fase, versão e alçadas | Analista | 2 | 4 | 6 | Controle contextual inspirado no recorte local |
| T3 Ler e analisar conteúdo, finalidade e destinatário | Analista | 18 | 35 | 60 | Ordem de grandeza de D1/E2, adaptada |
| T4 Conferir análise e preparar encaminhamento | Revisor | 8 | 15 | 25 | Segunda verificação e eventual redução do conteúdo; E6–E8 |
| T5 Decidir e registrar autorização ou negativa | Revisor/aprovador | 5 | 8 | 12 | Decisão específica; tempo separado da conferência |
| T6 Executar envio autorizado ou comunicar negativa e arquivar | Operador | 4 | 6 | 9 | Conferência final de destinatário e evidência de desfecho |
| **Total sem especialista/retrabalho** | — | **40** | **73** | **120** | Soma de T1–T6 |

Unidade de todas as células numéricas: **minutos pessoa por solicitação da classe**. A T6 contém um encerramento padronizado nas duas rotas, sem assumir execução de ação proibida. Para volumes grandes, documentos extensos ou múltiplos anexos, criar outra classe ou tarefa; não extrapolar silenciosamente.

### 5.3 Distribuições de duração

Para Monte Carlo, cada T1–T6 usa uma triangular `(mínimo, moda, máximo) = (0,5t, t, 1,5t)`, em que `t` é o valor da tabela. Assim a média é `t`, preservando as contas centrais. Exemplo: T3 simples = Tri(9,18,27).

Triangular é uma escolha transparente quando faltam observações. Os limites são premissas de suporte da simulação, não mínimos/máximos observados em estudos. Tempos de etapas são independentes **condicionalmente à classe**, simplificação que deve ser declarada; a classe compartilhada já induz associação entre eles.

## 6. Especialistas, revisões e intervenções

### 6.1 Parâmetros complementares

| Parâmetro | Simples | Moderada | Complexa |
|---|---:|---:|---:|
| Probabilidade de especialista `s` | 0,05 | 0,60 | 1,00 |
| Tempo de especialista, Tri(min,moda,max) | (5,15,25) | (10,30,50) | (20,60,100) |
| Probabilidade de ≥1 rodada adicional `r` | 0,10 | 0,25 | 0,40 |
| Probabilidade de segunda rodada, dado retrabalho `b` | 0,10 | 0,25 | 0,50 |
| Esforço agregado de cada rodada, Tri(min,moda,max) | (6,12,24) | (12,24,42) | (20,40,75) |
| Média de esforço por rodada | 14 | 26 | 45 |

Especialista ocorre no máximo uma vez e complementa T4–T5, sem repetir integralmente a análise. O encaminhamento e registro da escalada estão incluídos nas tarefas normais; apenas a análise especializada adiciona tempo. O controle inicial é obrigatório em 100% dos pedidos neste processo experimental.

Uma rodada adicional significa devolução com alteração e nova conferência de versão. Há no máximo duas rodadas no modelo central. Retrabalho pode decorrer de erro detectado, incompletude do pedido ou alteração de escopo; revisão não é sinônimo de erro.

### 6.2 Contagem sem duplicação

- **Evento humano inicial 1:** participação do analista em T1–T3.
- **Evento humano inicial 2:** revisão e decisão em T4–T5, na mesma sessão.
- **Evento humano inicial 3:** encerramento operacional em T6.
- **Especialista:** mais um evento, quando acionado.
- **Cada rodada adicional:** dois eventos, um de ajuste e um de nova conferência. Dividir o tempo agregado da rodada igualmente entre esses eventos para o registro sintético; a divisão 50/50 também é hipótese.

Um evento pode ter vários rótulos, como revisão e aprovação, mas seu `evento_id` conta uma vez no total. Os três eventos iniciais podem envolver menos de três pessoas distintas; **evento não significa pessoa**. A contagem representa episódios operacionais e não cliques, comentários ou todas as pequenas ações.

Com `S∈{0,1}` indicando especialista e `R∈{0,1,2}` indicando rodadas:

```text
intervencoes_total = 3 + S + 2*R
revisoes_total = 1 + S + R
rodadas_adicionais = R
participou_humano = true
E[R | classe] = r*(1+b)
```

Para comparar B1, publicar tanto todos os eventos humanos operacionais quanto as intervenções no processamento iniciado pelo agente. Caso a definição de evento mude entre B0 e B1, a diferença perde comparabilidade.

## 7. Erros: definições e parâmetros

**Erro inicial:** pelo menos uma divergência material na análise/proposta anterior ao controle, frente à referência do caso. **Erro residual:** divergência que permanece no desfecho após os controles. Os denominadores são solicitações, não cláusulas nem anotações. O modelo central representa no máximo um indicador de erro material por pedido; não estima quantidade de erros por documento.

Categorias a registrar: conteúdo, decisão, autorização ou execução. O modelo numérico central **não atribui proporções a essas categorias**, nem presume que todo erro residual represente liberação ou execução indevida.

| Parâmetro | Simples | Moderada | Complexa |
|---|---:|---:|---:|
| Probabilidade de erro inicial `e` | 0,08 | 0,15 | 0,25 |
| Detecção/correção pelo conjunto de controles, dado erro `d` | 0,75 | 0,70 | 0,60 |
| Erro residual esperado `e*(1-d)` | 0,020 | 0,045 | 0,100 |

Os valores de `e` e `d` são **hipóteses sem benchmark diretamente transferível**. A literatura demonstra divergências de avaliação e necessidade de revisão, mas não identifica esses números. Escolheu-se aumentar a dificuldade do erro e reduzir sua detecção com a complexidade. O centro é um cenário didático; testar também erro menor e maior.

Não se utilizou `1−F1` de E1/E2. A discordância de aprovação de faturas de E3 também não foi transferida. E4 trata de alucinação de sistemas, portanto não informa `e` humano.

### 7.1 Coerência entre erro e retrabalho

Para impedir um modelo em que um erro é corrigido sem revisão nem esforço:

1. Sortear erro inicial `E ~ Bernoulli(e)`.
2. Sortear detecção `D = E AND Bernoulli(d)`.
3. Se `D=true`, iniciar uma rodada adicional obrigatória.
4. Se `D=false`, sortear outra causa de retrabalho com probabilidade `q=(r−e*d)/(1−e*d)`.
5. Se houver retrabalho, `R=1+Bernoulli(b)`; senão `R=0`.
6. Erro residual `F=E AND NOT D`.

Valores de `q`: simples **0,04255319**; moderada **0,16201117**; complexa **0,29411765**. Essa construção preserva `P(R≥1)=r`, garantindo `r≥e*d`. Ao mudar cenários, recalcular `q` e rejeitar combinações inválidas.

Detecção engloba o conjunto de controles, inclusive especialista quando houver; `d` não é uma capacidade incremental a somar à T4 ou ao especialista. Um erro detectado é corrigido na primeira rodada, por simplificação. A segunda pode tratar incompletude ou ajustes de escopo. O modelo central não introduz novos erros nas revisões; isso é uma premissa otimista, a testar em sensibilidade.

Falha técnica não é erro de julgamento: registrar separadamente. O B0 central não injeta falhas técnicas por falta de taxa local, sem alegar que tais falhas inexistam. Qualquer cenário com falhas precisa adicionar tempo de recuperação e intervenções.

## 8. Cálculos e baseline consolidada

Para classe `c`, sejam `T0` a soma das seis etapas, `s` a chance de especialista, `ts` sua duração média, `tr` a duração média da rodada:

```text
E[T | c] = T0 + s*ts + r*(1+b)*tr
E[intervencoes | c] = 3 + s + 2*r*(1+b)
E[revisoes | c] = 1 + s + r*(1+b)
E[erro_residual | c] = e*(1-d)
E[indicador] = soma_c peso_c * E[indicador | c]
```

| Indicador esperado | Simples | Moderada | Complexa | Carteira 60/30/10 |
|---|---:|---:|---:|---:|
| T0, min pessoa | 40 | 73 | 120 | 57,90 |
| Esforço de especialista, min pessoa | 0,75 | 18 | 60 | 11,85 |
| Esforço de retrabalho, min pessoa | 1,54 | 8,125 | 27 | 6,0615 |
| **Esforço completo, min pessoa** | **42,29** | **99,125** | **207** | **75,8115** |
| Probabilidade de retrabalho | 10% | 25% | 40% | 17,50% |
| Rodadas adicionais/pedido | 0,11 | 0,3125 | 0,60 | 0,21975 |
| Revisões/pedido | 1,16 | 1,9125 | 2,60 | 1,52975 |
| Eventos humanos/pedido | 3,27 | 4,225 | 5,20 | 3,74950 |
| Erro inicial | 8% | 15% | 25% | 11,80% |
| Erro residual | 2% | 4,5% | 10% | 3,55% |

Por exemplo, esforço moderado = `73 + 0,6*30 + 0,25*1,25*26 = 99,125 min pessoa`.

Para **1.000 solicitações**, expectativas: 1.263,525 horas pessoa, 118 pedidos com erro inicial, 35,5 com erro residual, 175 com retrabalho, 219,75 rodadas adicionais e 3.749,5 eventos humanos. Valores fracionários são médias teóricas sobre repetições, não contagens possíveis de uma execução isolada. O volume de 1.000 é apenas uma escala demonstrativa.

## 9. Espera e tempo decorrido — extensão opcional

O pedido central é esforço por tarefa. Se o simulador também precisar de prazo, usar uma extensão separada, inteiramente hipotética:

| Classe | Espera agregada por solicitação, Tri(min,moda,max), em minutos úteis | Espera média |
|---|---|---:|
| simples | (0,30,120) | 50 |
| moderada | (30,120,480) | 210 |
| complexa | (120,480,1440) | 680 |

As esperas representam filas por informação/aprovação no conjunto do pedido; sortear **uma vez**, sem adicionar novamente espera de especialista ou rodadas. A literatura E5 sustenta a existência de dependências, não esses valores. O cenário simples de prazo assume trabalho sequencial, um participante ativo de cada vez, sem sobreposição: `prazo_util_min = esforço_total_min + espera_agregada_min`.

Nessa extensão, espera média ponderada = **161 min úteis** e prazo médio = **236,8115 min úteis**. Não chamar de horas corridas ou SLA observado. Para datas, definir calendário de dias úteis, jornada e feriados; não transformar minutos úteis em timestamps corridos sem essa convenção. Em processos paralelos, construir uma linha do tempo de eventos: não somar esforço pessoa para obter duração.

## 10. Parâmetros legíveis por máquina

Este JSON é a configuração central completa do modelo. Os tempos T1–T6 geram triangulares pelo multiplicador declarado; `tri_*` segue a ordem mínimo, moda, máximo. Probabilidades usam escala 0–1.

```json
{
  "baseline_id": "B0_MA_SINTETICA_v1",
  "origem_dado": "sintetico_informado_por_literatura",
  "data_pesquisa": "2026-11-17",
  "unidade": "solicitacao",
  "unidade_tempo": "minuto_pessoa",
  "seed_sugerida": 20261117,
  "n_solicitacoes_sugerido": 1000,
  "repeticoes_sugeridas": 1000,
  "triangular_T1_T6_multiplicadores": [0.5, 1.0, 1.5],
  "eventos_humanos_iniciais": 3,
  "revisoes_iniciais": 1,
  "eventos_por_especialista": 1,
  "revisoes_por_especialista": 1,
  "eventos_por_rodada": 2,
  "revisoes_por_rodada": 1,
  "max_rodadas": 2,
  "fracao_tempo_rodada_ajuste": 0.5,
  "introduz_novos_erros": false,
  "injeta_falhas_tecnicas": false,
  "espera_opcional": true,
  "classes": {
    "simples": {
      "peso": 0.6,
      "T1_T6_centrais": [3, 2, 18, 8, 5, 4],
      "p_especialista": 0.05,
      "tri_especialista": [5, 15, 25],
      "p_retrabalho": 0.1,
      "p_segunda_rodada_dado_retrabalho": 0.1,
      "tri_rodada": [6, 12, 24],
      "p_erro_inicial": 0.08,
      "p_deteccao_dado_erro": 0.75,
      "tri_espera_util": [0, 30, 120]
    },
    "moderada": {
      "peso": 0.3,
      "T1_T6_centrais": [5, 4, 35, 15, 8, 6],
      "p_especialista": 0.6,
      "tri_especialista": [10, 30, 50],
      "p_retrabalho": 0.25,
      "p_segunda_rodada_dado_retrabalho": 0.25,
      "tri_rodada": [12, 24, 42],
      "p_erro_inicial": 0.15,
      "p_deteccao_dado_erro": 0.7,
      "tri_espera_util": [30, 120, 480]
    },
    "complexa": {
      "peso": 0.1,
      "T1_T6_centrais": [8, 6, 60, 25, 12, 9],
      "p_especialista": 1.0,
      "tri_especialista": [20, 60, 100],
      "p_retrabalho": 0.4,
      "p_segunda_rodada_dado_retrabalho": 0.5,
      "tri_rodada": [20, 40, 75],
      "p_erro_inicial": 0.25,
      "p_deteccao_dado_erro": 0.6,
      "tri_espera_util": [120, 480, 1440]
    }
  }
}
```

Semente, tamanho e repetições são sugestões de execução futura, não indicações de experimento já realizado. Fixar e registrar biblioteca e gerador aleatório; a mesma semente isoladamente não garante igualdade entre bibliotecas diferentes.

### 10.1 Sequência de geração

```text
Para cada pedido:
  sortear classe com pesos da configuração
  sortear T1...T6 pelas triangulares correspondentes
  sortear S ~ Bernoulli(p_especialista)
  sortear duração de especialista apenas se S=1
  sortear E e D e construir R conforme seção 7.1
  sortear uma duração por rodada adicional
  F = E e não D
  esforço = soma(T1...T6) + duração_especialista + soma(durações_rodadas)
  eventos = 3 + S + 2*R
  revisões = 1 + S + R
  opcionalmente sortear uma espera agregada
  registrar origem sintética, parâmetros e resultados
```

A referência de decisão do caso e a execução da ferramenta são camadas adicionais: o indicador agregado de erro não escolhe sozinho qual ação deveria ser permitida. Para medir liberação indevida, criar casos com `acao_permitida_referencia`, `aprovacao_exigida` e `acao_executada`, depois avaliar o resultado real do controlador.

## 11. Cenários e análise de sensibilidade

Usar “favorável” e “desfavorável” em relação ao **processo humano B0**, evitando construir artificialmente uma comparação favorável ao agente. As variações abaixo são hipóteses, não estimativas de mercado.

| Parâmetro | B0 favorável | Central | B0 desfavorável |
|---|---|---|---|
| Tempos de todas as atividades e rodadas | central × 0,75 | tabelas | central × 1,50 |
| `e`, por classe simples/moderada/complexa | 0,04 / 0,08 / 0,15 | 0,08 / 0,15 / 0,25 | 0,12 / 0,22 / 0,35 |
| `d`, por classe | 0,85 / 0,80 / 0,75 | 0,75 / 0,70 / 0,60 | 0,65 / 0,60 / 0,50 |
| `r`, por classe | 0,07 / 0,18 / 0,30 | 0,10 / 0,25 / 0,40 | 0,18 / 0,35 / 0,55 |
| Probabilidade de segunda rodada e especialista | central | central | central |
| Espera opcional | central × 0,50 | central | central × 2 |

Manter pesos da carteira ao comparar esses três cenários. Fazer uma análise separada para composição: carteira leve 80/15/5 e pesada 30/40/30. Também variar individualmente o tempo de análise, `e`, `d` e `r`, para identificar quais premissas dominam o resultado.

Sensibilidade adicional: após o controle, sortear introdução de novo erro em 1% e 3% dos pedidos que estavam corretos. Nesse modelo, `erro_final = F OR (NOT F AND Bernoulli(p_novo))`; taxa esperada = `p_F+(1−p_F)*p_novo`. Aplicar essa extensão simetricamente às revisões humanas de B0/B1 quando comparáveis e identificar o novo erro. Não somar probabilidades sem considerar a sobreposição.

Executar, se viável, 1.000 carteiras de 1.000 pedidos e reportar distribuição das médias, dos totais e das taxas. Percentis entre simulações descrevem **variabilidade sob premissas fixas**; não validam empiricamente essas premissas. Separar a variação dos pedidos da incerteza entre cenários.

## 12. Registros, métricas e comparação com B1

### 12.1 Estruturas mínimas

**Pedido:** `pedido_id`, `baseline_id`, `origem_dado`, `cenario`, `seed`, `classe`, `fase`, `acao`, `documento_id`, `versao`, `destinatario_papel`, `decisao_referencia`, `aprovacao_exigida`, `T1`...`T6`, `especialista_min`, `retrabalho_min`, `esforco_total_min`, `espera_util_min`, `erro_inicial`, `erro_detectado`, `erro_residual`, `rodadas`, `revisoes`, `intervencoes`, `estado_final`.

**Evento:** `evento_id`, `pedido_id`, `action_id`, `condicao`, `ator_id`, `papel`, `tipos`, `versao_antes`, `versao_depois`, `duracao_ativa_min`, `decisao`, `aprovacao_id`, `execucao_confirmada`. Só criar timestamps se houver calendário/linha do tempo explicitamente modelados.

**Avaliação de referência:** `pedido_id`, `criterio`, `rotulo_esperado`, `rotulo_observado`, `avaliador`, `origem_referencia`, `categoria_erro`, `gravidade`, `justificativa`. Parâmetros agregados de erro não substituem essa avaliação quando houver teste de casos.

Preservar valores ausentes: `null` significa desconhecido/não aplicável; zero significa ausência efetivamente definida ou observada no modelo. Contar por IDs, sem somar rótulos de um mesmo evento.

### 12.2 Indicadores

- Tempo: média, mediana e P90 de minutos pessoa por pedido; prazo separado, se modelado.
- Erro inicial e residual: pedidos com erro/total de pedidos avaliáveis; sempre divulgar numerador e denominador.
- Retrabalho: pedidos com `R≥1`/total; rodadas e minutos adicionais por pedido.
- Revisão: eventos de revisão por pedido e percentual de pedidos revisados.
- Participação humana: eventos e minutos pessoa por pedido, pessoas distintas em campo separado.
- Segurança: execuções proibidas/ações proibidas tentadas; liberações indevidas/ações proibidas avaliadas; impedimentos indevidos/ações permitidas avaliadas.
- Aprovação: ações supervisionadas executadas com aprovação específica válida anterior/ações supervisionadas executadas.
- Auditoria: tentativas com cadeia completa/tentativas iniciadas; falhas e pendências publicadas separadamente.

Se não houver denominador, reportar não aplicável. Uma taxa de erro residual de 3,55% não permite estimar execuções indevidas: são métricas diferentes.

### 12.3 Comparação justa

Usar as mesmas solicitações, documentos, classes, referências e regras em B0 e B1. Separar uma carteira representativa dos testes adversariais; a quantidade artificial de ataques não estima sua incidência empresarial. Incluir em B1 preparação operacional recorrente, revisão, aprovação, correção, falhas e recuperação. Custos únicos de preparação e desenvolvimento devem ficar separados do esforço recorrente.

Calcular `ganho_tempo = (T_B0−T_B1)/T_B0` e diferença de erros em pontos percentuais, sem presumir sinal positivo. Distinguir uma comparação inteiramente simulada de um protótipo medido contra B0 sintético. Ganho financeiro depende de volume e custo hora locais; não calcular multas evitadas a partir das taxas simuladas.

## 13. Limitações e calibração futura

1. Não houve observação de empresa, cronometragem local ou coleta de entrevistas nesta entrega.
2. Os estudos de tempo tratam de revisão contratual ou faturamento; idioma, extensão, jurisdição, especialidade e objeto diferem do fluxo proposto.
3. Há estudos de fornecedor e preprints; foram usados com identificação de seus interesses e escopo.
4. O processo atual é uma reconstrução para o experimento. O arranjo de papéis e o controle em todos os pedidos não são universais.
5. Taxas de erro, detecção, retrabalho, especialista e composição não foram estimadas de amostra; dependem das hipóteses declaradas.
6. O modelo central limita revisões a duas rodadas, admite correção bem-sucedida de erros detectados e não introduz novos erros nem falhas técnicas. Casos muito demorados e dependências entre avaliadores podem estar subrepresentados.
7. Os resultados não demonstram conformidade jurídica nem permitem aprovar ações reais. O guia do Cade é usado para caracterizar controles, sem transformar seu modelo em uma regra universal.

Para calibrar posteriormente, observar pedidos consecutivos com tempos ativos por papel, versões, controles, desfechos e referência independente. Como piloto de viabilidade, 30–50 pedidos podem revelar problemas de definição; não são amostra suficiente por si só para estimar erro raro. Substituir parâmetros por classe e registrar tamanho, período e incerteza da amostra, mantendo esta versão sintética para rastreabilidade.

## 14. Texto sugerido para a metodologia acadêmica

> Foi construída uma baseline sintética do processo de revisão de solicitações de informação e ação no pré-fechamento de operações de M&A. A pesquisa documental forneceu referências de ordem de grandeza para revisão de documentos e fundamentos para controles humanos. Na ausência de dados diretamente equivalentes à unidade de análise, foram explicitadas hipóteses de decomposição de tarefas, complexidade, erros, detecção e retrabalho. O cenário central resulta em esforço esperado de 75,81 minutos pessoa por solicitação, com 17,50% de solicitações submetidas a rodadas adicionais e 3,55% de erro residual sintético. Esses valores são parâmetros de experimentação e expectativas do modelo, não medições de uma organização nem evidência de ganho do agente. A robustez das conclusões será examinada por cenários e análise de sensibilidade.

## 15. Prompt estruturado que orientou a execução

**Role:** Pesquisador de processos e métodos quantitativos para um projeto acadêmico.

**Task:** Identificar nos arquivos do projeto o processo atual e pesquisar fontes públicas sobre tempo por tarefa, erros, revisões e intervenções humanas. Preservar contexto, unidade e limitações dos dados publicados. Quando faltarem medidas diretamente aplicáveis, propor parâmetros sintéticos, com premissas, cálculos e cenários explícitos, sem apresentá-los como observações reais.

**Format:** Documento Markdown em português para leitura por agente, com escopo, evidências rastreáveis, baseline por tarefa, definições operacionais, configuração legível por máquina, instruções de simulação, cenários, limitações e referências.

**Premissa resolvida pelo contexto:** a unidade do projeto é a solicitação de informação ou ação no pré-fechamento, e não a operação inteira de M&A.

## 16. Referências e localização dos dados

Todas as referências abaixo foram acessadas em **17/11/2026**. Os links das tabelas remetem aos mesmos documentos.

1. **LawGeex.** Comparing the Performance of Artificial Intelligence to Human Lawyers in the Review of Standard Business Contracts. Fevereiro de 2018. Relatório original do fornecedor, pp. 6–9 e 14–15. [PDF](https://images.law.com/contrib/content/uploads/documents/397/5408/lawgeex.pdf).
2. **Martin, L.; Whitehouse, N.; Yiu, S.; Catterson, L.; Perera, R.** Better Call GPT, Comparing Large Language Models Against Lawyers. 24/01/2024, arXiv:2401.16212v1. Seções 3.3 e 4.2; tabelas 2–4. [Artigo](https://arxiv.org/html/2401.16212v1).
3. **Whitehouse, N.; Lincoln, N.; Yiu, S.; Catterson, L.; Perera, R.** Better Bill GPT: Comparing Large Language Models against Legal Invoice Reviewers. 02/04/2025, arXiv:2504.02881v1. Resumo e seção 4. [Artigo](https://arxiv.org/html/2504.02881v1).
4. **Magesh, V. et al.** Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools. Journal of Empirical Legal Studies, 2025. DOI: 10.1111/jels.12413. Resumo e resultados. [PDF dos autores](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf).
5. **Bayes Business School.** Cautious M&A investors taking extra care with due diligence. 22/06/2024. Divulgação institucional de pesquisa com SS&C Intralinks. [Página](https://www.bayes.citystgeorges.ac.uk/news-and-events/news/2024/june/cautious-m-and-a-investors-investing-in-extensive-due-diligence).
6. **Hendrycks, D.; Burns, C.; Chen, A.; Ball, S.** CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review. 2021, arXiv:2103.06268v2. Apêndice A.2, Labeling Process Details. [Artigo](https://arxiv.org/html/2103.06268v2).
7. **Conselho Administrativo de Defesa Econômica.** Guia para análise da consumação prévia de atos de concentração econômica. 2015. Seções 2.1–2.6, pp. 10–13. [PDF oficial](https://cdn.cade.gov.br/Portal/centrais-de-conteudo/publicacoes/guias-do-cade/gun-jumping-versao-final.pdf).
8. **Federal Trade Commission.** Avoiding antitrust pitfalls during pre-merger negotiations and due diligence. 20/03/2018. Recomendações para partes divulgadoras e receptoras. [Página oficial](https://www.ftc.gov/enforcement/competition-matters/2018/03/avoiding-antitrust-pitfalls-during-pre-merger-negotiations-due-diligence). A abertura direta inicialmente falhou; o conteúdo foi recuperado pelo resultado indexado da própria FTC.
9. **National Institute of Standards and Technology.** AI RMF Playbook — Measure, especialmente Measure 2.8. Recurso institucional consultado na data da pesquisa. [Página oficial](https://airc.nist.gov/airmf-resources/playbook/measure/).
10. **Bang, Y.; Fielding, K.; Oliver, B.; Birke, B.; Seedat, N.; Bean, A. M.** ContractScrub: A benchmark for final review of legal contracts. 20/08/2026, arXiv:2608.20204v1. Resumo e seção 1. [Artigo](https://arxiv.org/html/2608.20204v1).

**Resultado desta entrega:** documento de pesquisa e especificação de baseline sintética pronto para orientar a geração de dados. A simulação e a avaliação do agente são etapas posteriores; nenhuma foi apresentada como já executada aqui.


---

# Anexo Pesquisa documental e protocolo de medição

O anexo abaixo preserva a pesquisa anterior de 15/11/2026. O corpo principal de 17/11/2026 define os parâmetros sintéticos para simulação; o anexo apresenta referências e um protocolo de medição futura. Nenhuma das partes comprova medição empresarial realizada.

# Baseline do processo atual em M&A

Tempo por tarefa, erros, revisões e intervenções humanas

Relatório de pesquisa e protocolo de medição
Guardião de Gates de M&A  |  Projeto final IBMEC
Data de corte e consulta das fontes 15 de novembro de 2026

### Síntese executiva

A pesquisa oferece referências externas úteis para planejar a medição, mas não estabelece os valores do processo empresarial do projeto. A baseline principal deve ser observada em solicitações de informação e de ação no pré fechamento, desde o recebimento até a decisão e o registro do desfecho. O tempo humano de análise, a espera por aprovação e o retrabalho precisam ser medidos separadamente.

O diagnóstico informa que as quatro ferramentas são simuladas e que ainda faltam evidências de processo e impacto empresarial. Seus resultados de classificadores não equivalem a erros humanos, duração de tarefas ou frequência de revisão em uma empresa. [D1]

| Dimensão | Evidência pública mais útil | Conclusão para o projeto |
| --- | --- | --- |
| Tempo por tarefa | 92 minutos por lote de cinco NDAs; 43,46 a 201 minutos por contrato em outro experimento. [1, 2] | Há ordens de grandeza para revisão documental, não um tempo padrão de autorização de pedidos. |
| Erros | F1, precisão e recall na revisão contratual; alucinações na pesquisa jurídica. [1, 2, 4] | Definir erro por decisão ou execução, com referência de domínio independente. |
| Revisões | Processos documentados de revisão especializada e consenso. [5, 7, 8] | Etapas de controle estão descritas; frequência e duração locais seguem a medir. |
| Intervenções humanas | Orientação para registrar supervisão e alterações de decisões. [9] | Contar participação humana por tipo, motivo, tempo e ação afetada. |

### Decisão recomendada

Usar a literatura como contexto e como apoio ao desenho da avaliação. Não preencher o processo atual com médias de estudos externos nem apresentar reduções publicitárias como ganhos do agente. O resultado empresarial permanecerá “a medir” até a coleta prevista nas seções 7 e 8.

## 1 Escopo e método da pesquisa

### Unidade de análise

Recorte proposto: revisão e encaminhamento de uma solicitação de informação ou ação entre comprador e empresa alvo antes do fechamento. Cada solicitação deve identificar operação, fase confirmada, finalidade, documento ou dado, destinatário e ação pretendida. Esse recorte é compatível com ler documento, solicitar preços, propor migração e enviar e-mail, as ferramentas simuladas descritas no diagnóstico. [D1]

Início: chegada do pedido com seu conteúdo original preservado. Fim: decisão e desfecho registrados, incluindo execução autorizada, negativa, cancelamento ou falha. Uma aprovação sem comprovação de envio não deve ser registrada como execução concluída. A rotina empresarial exata ainda depende de observação.

### Estratégia de busca e seleção

A busca exploratória, em português e inglês, combinou M&A, due diligence, contract review, time per document, accuracy, revisions, human oversight, clean team e baseline. Foram priorizados relatórios originais, artigos acadêmicos, autores dos estudos, universidades, Cade, FTC e NIST. Notícias de terceiros e agregadores serviram apenas à descoberta; não sustentam os principais valores do relatório.

Foram selecionadas 13 fontes externas publicadas ou disponíveis até a data de corte. Não se trata de revisão sistemática: não houve protocolo pré registrado, busca exaustiva em bases bibliométricas ou avaliação formal de risco de viés. A abrangência cobre os quatro indicadores solicitados e explicita a proximidade de cada evidência à tarefa do projeto.

| Tipo de evidência | Tratamento adotado |
| --- | --- |
| Experimento com humanos | Preservar tarefa, amostra, unidade, condição com ou sem IA e definição de qualidade. |
| Estudo de fornecedor | Identificar interesse comercial, tamanho do corpus e custos ou etapas não contabilizados. |
| Orientação institucional | Usar para desenhar controles e registros; não converter em taxa observada. |
| Pesquisa de opinião | Tratar percepção e expectativa como tais; não chamar de medição de produtividade. |
| Documento interno | Usar para delimitar o protótipo; números relatados no diagnóstico não foram recontados nesta pesquisa. |

### Quatro conceitos que não devem ser misturados

Tempo ativo é esforço de trabalho; tempo decorrido inclui filas e dependências. Erro é divergência comprovada da referência; revisão pode ser controle planejado. Intervenção é uma participação humana operacional; pode ser obrigatória e correta. Falha técnica é um desfecho operacional distinto de decisão errada.

## 2 Tempos de tarefas em estudos comparáveis

| Estudo e unidade | Condição humana | Condição com IA | Limite de comparação |
| --- | --- | --- | --- |
| LawGeex 2018<br>Lote de 5 NDAs [1] | 20 advogados; média 92 min; menor 51 e maior 156 min. | Motor de IA: 26 segundos para o lote. | Identificação de questões; não inclui todo o fluxo de aprovação e execução. |
| Onit 2024<br>Contrato de compras [2] | Sênior 43,46 min; júnior 56,17 min; LPO 201,00 min por documento. | GPT4-1106 4,70 min; GPT4-32k 2,11 min por documento. | 10 contratos dos EUA e Nova Zelândia; não representa M&A brasileiro. |
| Choi e colegas<br>Redação de contrato [3] | 69,72 min sem GPT-4. | 47,59 min com GPT-4. | Experimento com estudantes; tarefa de redação, não autorização de ação. |
| Choi e colegas<br>Memorando ao cliente [3] | 244,41 min sem GPT-4. | 215,69 min com GPT-4. | Ganho depende da tarefa; comparar condições assistidas exige contabilizar o humano. |

### Como interpretar os tempos

Na LawGeex, dividir 92 por cinco produz 18,4 minutos por NDA, cálculo derivado deste relatório. É uma média aritmética de lote, sem tempos individuais por documento; não deve virar estimativa para contratos de qualquer extensão. A avaliação foi promovida pelo fornecedor e usou cinco NDAs públicos do corpus Enron. [1]

O estudo da Onit é um preprint de autores vinculados à empresa. A referência foi construída por revisores seniores, com playbook e consenso majoritário. O contraste mede revisão automatizada e humana; o tempo do modelo não incorpora necessariamente toda a validação posterior ou implantação operacional. [2]

Choi, Monahan e Schwarcz publicaram o estudo em 2024; a versão integral consultada relata coleta em 2023, 60 participantes inicialmente recrutados e 59 concluintes. A tabela 2 informa redução de 32,1% na redação contratual e 11,8% no memorando. Os percentuais e diferenças reportados foram preservados, embora não coincidam exatamente com o cálculo entre médias arredondadas. [3]

### Aplicabilidade

Esses resultados justificam cronometrar separadamente leitura, análise, preparação de resposta, aprovação e registro. Não justificam prometer que um pedido será tratado em 18,4 minutos, nem que o agente reduzirá o esforço na mesma proporção. Complexidade, idioma, extensão, destinatário e alçada alteram a unidade de trabalho.

## 3 Erros e qualidade da decisão

| Fonte | Medida e resultado | Uso correto |
| --- | --- | --- |
| LawGeex [1] | F1 médio de 85% para humanos e 94% para IA, chamado de accuracy no relatório. | F1 combina precisão e recall; 1 − F1 não é taxa de tarefas erradas. |
| Onit [2] | Identificação: júnior F1 0,860; GPT4-1106 0,871. Localização: júnior 0,667; GPT4-1106 0,686. | Encontrar uma questão e localizar o trecho são resultados diferentes. |
| Choi e colegas [3] | Qualidade corrigida às cegas; melhoria pequena e inconsistente entre tarefas. | A economia de tempo não demonstra, por si, melhora de qualidade. |
| Magesh e colegas [4] | 202 consultas jurídicas; ferramentas especializadas ainda produziram informação falsa ou enganosa. | Medir correção e sustentação na fonte; não transpor a taxa para decisões de M&A. |

### Alucinações e avaliação independente

Na publicação de 2025 de Hallucination Free, Lexis+ AI e Ask Practical Law AI tiveram alucinações em mais de uma a cada seis consultas; Westlaw, em aproximadamente um terço. São sistemas e versões avaliados no estudo, não um diagnóstico dos produtos atuais. Uma segunda avaliação independente de 48 respostas obteve concordância de 85,4% e kappa de Cohen de 0,77. Esses números descrevem a confiabilidade da rotulagem, não a taxa de erros humanos do processo. [4]

### Taxonomia proposta para o projeto

| Categoria | Definição operacional proposta |
| --- | --- |
| Erro de decisão | Permitir ação proibida, impedir ação permitida ou dispensar aprovação exigida segundo a política validada. |
| Erro de conteúdo | Omitir informação necessária, citar documento errado ou descrever incorretamente a informação que será compartilhada. |
| Erro de autorização | Usar aprovação de outro pedido, de versão anterior ou de pessoa sem alçada. |
| Erro de execução | Enviar para destinatário errado, executar ação diferente ou repetir efeito sem autorização. |
| Falha operacional | Timeout, autenticação, auditoria indisponível ou erro de ferramenta; contabilizar separadamente. |

A referência de domínio deve registrar decisão esperada, justificativa, versão da política e revisor. Divergências entre revisores devem ser preservadas antes do consenso. Casos ambíguos podem receber rótulo inconclusivo; não forçar acerto ou erro para produzir um indicador.

## 4 Revisões e intervenções humanas

### O que está documentado publicamente

O CUAD reúne 510 contratos, mais de 13 mil anotações e 41 categorias. Estudantes receberam 70 a 100 horas de treinamento. O processo inclui anotação, busca de omissões, revisão por categoria, revisão por advogados e exame de trechos adicionais sugeridos por ferramenta. A etapa de revisão dos adicionais se repete até que todos ou quase todos sejam incorretos. Isso comprova uma rotina de controle; não fornece média de rodadas, taxa de correção ou minutos de revisão por contrato. [5]

O guia do Cade descreve, no modelo de clean team, solicitações e comunicações escritas, classificação da informação, segregação de funções e registro formal das trocas. Não define um número universal de aprovadores nem uma duração padrão. É orientação para reduzir riscos, a ser aplicada conforme o contexto e as regras vigentes. [7]

A FTC recomenda revisão pelo jurídico antes de disseminar a outras áreas relatórios com informação concorrencialmente sensível, além de acesso restrito, agregação e proteção de identidades. A fonte descreve salvaguardas; não mede o percentual de pedidos revisados ou o custo humano dessas revisões. [8]

O NIST recomenda medir e documentar supervisão, alterações de resultados pelos usuários, erros reportados e atividades de adjudicação. Essa orientação sustenta o registro das intervenções, sem oferecer um benchmark numérico para M&A. [9]

### Como contar sem duplicar

| Evento proposto | Regra de contagem |
| --- | --- |
| Revisão inicial | Primeira conferência humana do pedido ou da saída, mesmo sem alterações. |
| Rodada adicional | Nova avaliação após devolução, alteração relevante ou solicitação de ajuste. Contar por versão, não por comentário. |
| Intervenção de aprovação | Ato de aprovar ou negar ação específica; pode ocorrer sem revisão adicional. |
| Intervenção de correção | Mudança humana de conteúdo, classificação, destinatário ou decisão. |
| Escalada | Encaminhamento a outra alçada ou especialista; distinguir pedido de análise e resposta efetiva. |
| Resgate operacional | Ação humana para resolver falha técnica ou concluir tarefa interrompida. |

Um mesmo evento pode ser revisão e intervenção de aprovação. Preservar os dois atributos, mas contar seu identificador uma única vez no total de intervenções. Distinguir tarefa iniciada por humano de intervenção durante o processamento. Menos intervenções só é melhoria quando os controles necessários continuam atendidos.

## 5 Contexto de M&A e atualização das evidências

### Duração da operação não equivale ao tempo de uma tarefa

Bayes Business School e SS&C Intralinks analisaram mais de 900 transações globais anunciadas entre 2013 e 2023. A divulgação de 2024 informa média de 203 dias de due diligence, comparada com 124 dias na análise anterior, aumento reportado de 64%. A janela foi definida entre abertura do data room virtual e anúncio público, não até o fechamento. O estudo também incluiu 30 entrevistas. Trata-se de pesquisa com base proprietária, encomendada pela Intralinks; serve como contexto de complexidade e espera, não como esforço humano de um pedido. [6]

A WorldCC divulgou, em abril de 2025, médias de 2023 de 11,6 semanas para contratos domésticos de complexidade média e 13,7 semanas para internacionais. O artigo não informa a amostra específica nem decomposição de esforço. Esses tempos de ciclo contratual não permitem estimar quantidade de revisões, duração de leitura ou fila de aprovação em M&A. [10]

### Expectativa, percepção e experimento são evidências diferentes

O levantamento Future of Professionals de 2024 ouviu mais de 2.200 profissionais. A economia de quatro horas semanais em um ano e 12 horas em cinco anos aparece como previsão dos respondentes, não como economia cronometrada. Não será usada como baseline ou meta do protótipo. [11]

O relatório de 2026 se baseia em pesquisa com 1.816 profissionais, realizada em março e abril. Relata que 34% usam ferramentas de IA não sancionadas pela organização. É evidência de percepção e uso declarado, em várias profissões e países; não é taxa de intervenção, retrabalho ou erro em M&A. Para o levantamento local, reforça a necessidade de registrar as ferramentas que já são usadas hoje. [12]

Uma divulgação da Universidade de Minnesota em 2026 descreve experimento com aproximadamente 100 estudantes: a revisão com IA beneficiou alguns textos inicialmente fracos e prejudicou alguns inicialmente fortes. A notícia institucional não fornece minutos ou frequência desses efeitos; não foi usada como benchmark numérico. Sua contribuição é lembrar que revisão pode introduzir erros, além de removê-los. [13]

### Conclusão sobre a transferibilidade

A literatura examinada combina contratos, pesquisa jurídica, formação profissional, governança e operações de M&A. Não há uma única fonte com os quatro indicadores na mesma unidade de solicitação do projeto. Não seria metodologicamente válido combinar médias dessas populações em uma “baseline média de M&A”. A comparação principal deve usar a mesma tarefa, critérios e população local.

## 6 Indicadores para a baseline observada

As definições abaixo são propostas metodológicas deste relatório. Fixá-las antes da coleta e aplicá-las de forma idêntica ao processo atual e à condição assistida. Reportar sempre numerador, denominador, unidade e quantidade de dados ausentes.

| Indicador | Cálculo ou definição | Apresentação |
| --- | --- | --- |
| Tempo humano ativo | Soma dos intervalos de trabalho de cada pessoa no pedido, inclusive revisão, correção e registro. | Minutos pessoa por pedido; mediana, média, P25, P75 e P90. |
| Tempo decorrido | Instante de desfecho − instante de recebimento. | Horas corridas; reportar horário útil separadamente se usado. |
| Espera | Intervalos em que o pedido aguarda aprovação, insumo ou disponibilidade; medir no fluxo. | Horas por motivo. Não subtrair esforço de várias pessoas do tempo decorrido. |
| Pedidos com erro | Pedidos avaliáveis com ao menos um erro confirmado ÷ pedidos avaliáveis. | Percentual e contagens; discriminar gravidade e categoria. |
| Liberação indevida | Pedidos proibidos indevidamente liberados ÷ pedidos proibidos com referência válida. | Distinguir decisão de permitir e execução efetiva. |
| Execução indevida | Ações proibidas efetivamente executadas ÷ ações proibidas tentadas. | Identificar tentativa e efeito; não usar apenas texto do agente. |
| Falso impedimento | Pedidos permitidos impedidos ÷ pedidos permitidos com referência válida. | Contar escalada à parte; não confundir espera com bloqueio. |
| Revisão e retrabalho | Pedidos revisados ÷ concluídos; rodadas adicionais por pedido; minutos de correção. | Separar controle planejado, correção de erro e mudança de escopo. |
| Intervenções | Eventos humanos distintos e tempo associado durante o processamento. | Eventos por pedido e percentual com intervenção, por tipo. |
| Falhas e pendências | Tentativas com falha ÷ tentativas iniciadas; pedidos sem desfecho no corte. | Preservar falhas, cancelamentos e pendências em categorias próprias. |

### Indicadores de controle complementares

Aprovação válida: ações supervisionadas executadas com aprovação válida anterior ÷ ações supervisionadas executadas. Auditoria completa: tentativas com cadeia de eventos exigida ÷ tentativas iniciadas. Reportar “não aplicável” quando não houver denominador, em vez de atribuir 100%.

## 7 Protocolo de coleta e comparação

### Amostragem inicial proposta

Observar todos os pedidos elegíveis de uma janela previamente definida, por exemplo duas semanas úteis. Como ponto de partida operacional, buscar ao menos 30 pedidos e participação de três profissionais, se disponíveis. Esses números são propostas de viabilidade, não uma amostra estatisticamente suficiente. Se o volume for menor, publicar o total e ampliar a janela quando possível.

Incluir pedidos rotineiros, sensíveis, incompletos e escalados; registrar extensão do material, fase, ferramenta, área e necessidade de especialista. Não preencher artificialmente cotas de risco na coleta natural. Um banco adicional de casos críticos pode ser criado para testes, mas seus resultados devem ser publicados separadamente da frequência operacional.

### Execução da coleta

1. Validar com o dono do processo o recorte, papéis e regras; identificar controles e ferramentas já existentes. Selecionar os pedidos consecutivos e guardar também os motivos de exclusão.

2. Registrar o recebimento, trabalho ativo, pausas, encaminhamentos, versões, decisão, aprovação e desfecho. Preferir registros de sistema combinados com observação; quando houver estimativa retrospectiva, marcar sua origem.

3. Fazer revisão independente do resultado, sem expor ao avaliador a condição experimental quando viável. Dois revisores em todos os casos críticos e numa amostra dos demais permitem estimar concordância. Registrar divergência e resolução, sem apagar o rótulo inicial.

4. Fechar a coleta em data explícita. Pedidos ainda abertos são pendências; não atribuir tempo zero ou conclusão presumida. Registrar ausências de dados e distinguir falta de registro de inexistência de erro.

### Comparação com o agente

B0 é o processo atual com suas ferramentas habituais, que podem incluir automação. B1 é o mesmo processo com o Guardião, preservando responsabilidade e aprovações. Uma comparação técnica adicional pode opor agente com instruções e agente com controlador; ela não substitui B0.

Para casos históricos ou sintéticos, usar desenho pareado com casos equivalentes e ordem contrabalançada; evitar que a mesma pessoa memorize a resposta ao repetir o mesmo caso. Manter material, critérios e limites comparáveis. Registrar run_id, versão e falhas em ambas as condições. Efeitos externos permanecem simulados no teste do protótipo.

### Análise e critério de interpretação

Comparar esforço total e tempo decorrido separadamente. Informar diferença absoluta e relativa, distribuição e incerteza; em amostras pequenas, enfatizar contagens e descrição. Qualquer economia deve incluir correção, revisão e resgate operacional. Definir previamente com o responsável quais erros são críticos e qual perda de qualidade é aceitável; não derivar esse limite dos resultados observados.

## 8 Estrutura de registro e situação da baseline

### Três registros relacionados

| Registro | Campos mínimos propostos |
| --- | --- |
| Pedido<br>Uma linha por solicitação | pedido_id, operacao_id pseudonimizado, origem real ou sintética, condição B0 ou B1, fase confirmada, ação, versão do material, extensão, risco, recebimento, desfecho, estado final, referência da política. |
| Evento<br>Uma linha por participação ou ação | evento_id, pedido_id, action_id, run_id quando aplicável, ator pseudonimizado, papel, tipo, início e fim com fuso, pausa, motivo, versão antes e depois, decisão, autorização relacionada e resultado da execução. |
| Avaliação<br>Uma linha por critério e avaliador | pedido_id ou action_id, avaliador, critério, referência esperada, rótulo observado, categoria e gravidade do erro, evidência, avaliação inicial, consenso e justificativa da resolução. |

Exportação sugerida para a coleta futura: CSV UTF-8 para pedidos e avaliações; CSV ou JSONL para eventos. Usar datas ISO 8601 com fuso e unidades documentadas. Campos desconhecidos ficam vazios com motivo de ausência; zero só representa quantidade efetivamente observada igual a zero.

### Como reconstruir o trabalho

O identificador do evento evita duplicação entre revisão e aprovação. Intervalos sobrepostos de uma mesma pessoa devem ser conferidos para não duplicar esforço; o trabalho simultâneo de duas pessoas soma esforço de ambas. O histórico de versões permite separar correção de erro, alteração de escopo e mera formatação. O tempo de avaliação científica deve ser registrado fora do esforço operacional, salvo se corresponder a controle já existente na rotina.

| Campo da baseline empresarial | Situação após a pesquisa |
| --- | --- |
| Tempo ativo por pedido | A medir por observação; estudos externos não preenchem este campo. |
| Tempo em espera e tempo total | A medir nos registros de recebimento, encaminhamento e desfecho. |
| Erros humanos e execuções indevidas | A medir por avaliação independente e evidência do efeito. |
| Revisões e retrabalho | A medir por versão e motivo; sem taxa externa diretamente transferível. |
| Intervenções humanas | A medir por evento e papel; controles obrigatórios devem permanecer identificados. |
| Ganho e retorno financeiro do agente | Não estimados; dependem de B0, B1, volume e custos locais. |

### Uso no projeto final

Este relatório atende à fundamentação pública e prepara a coleta. A seção de resultados do TCC só deve apresentar baseline empresarial depois de observar pedidos reais ou de declarar explicitamente um experimento simulado. A lacuna apontada no diagnóstico permanece aberta até existir medição reproduzível do processo comparável. [D1]

## 9 Referências verificáveis

Todas as fontes externas foram consultadas em 15 de novembro de 2026. Os números entre colchetes no texto remetem aos itens abaixo. Links abrem a página ou o documento efetivamente consultado. Fontes sem taxa ou tempo explícito não receberam valores inferidos.

### 1 LawGeex

Comparing the Performance of Artificial Intelligence to Human Lawyers in the Review of Standard Business Contracts. Fevereiro de 2018. Relatório original, hospedado em Law.com. Ver pp. 6–9 e 14–16: desenho, contratos, cálculo de F1 e tempos. Estudo de fornecedor; cinco NDAs e 20 advogados.

[Abrir fonte original](https://images.law.com/contrib/content/uploads/documents/397/5408/lawgeex.pdf)

### 2 Martin, L.; Whitehouse, N.; Yiu, S.; Catterson, L.; Perera, R.

Better Call GPT Comparing Large Language Models Against Lawyers. 24 de janeiro de 2024. Preprint arXiv 2401.16212v1. Ver seções 3.3, 4.2 e tabelas 2–4. Autores vinculados à Onit; dez contratos de compras.

[Abrir fonte original](https://arxiv.org/html/2401.16212v1)

### 3 Choi, J. H.; Monahan, A. B.; Schwarcz, D.

Lawyering in the Age of Artificial Intelligence. Minnesota Law Review 109, 147, novembro de 2024. DOI 10.24926/265535.4225. Versão integral abaixo; tabela 2 na página interna 25, página 59 do PDF reunido.

[Abrir fonte original](https://scholarship.law.umn.edu/minnlrev/vol109/iss1/3/)

[Abrir versão integral consultada](https://coverage.memberclicks.net/assets/LawSymposium-2024-UofMinnesota/ACCC_2024InsLawSymp_MN_Papers_Nov15_0845_WhatIsAI_20241002.pdf)

### 4 Magesh, V. e colegas

Hallucination Free Assessing the Reliability of Leading AI Legal Research Tools. Journal of Empirical Legal Studies, 2025. Publicação integral no site de autor. Ver seções 4–6 e figura 4; não confundir com a divulgação preliminar de 2024. 202 consultas; revisão independente de 48 respostas.

[Abrir fonte original](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf)

### 5 Hendrycks, D. e colegas

CUAD An Expert Annotated NLP Dataset for Legal Contract Review. 2021. Artigo do dataset. Ver seção 3 e apêndice A.2, Labeling Process Details. O corpus e o treinamento não equivalem a uma medição do processo empresarial local.

[Abrir fonte original](https://arxiv.org/html/2103.06268v2)

### 6 Bayes Business School

Cautious M&A investors taking extra care with due diligence. 22 de junho de 2024. Divulgação da instituição pesquisadora sobre estudo com Intralinks; mais de 900 transações de 2013–2023 e 30 entrevistas. A duração vai da abertura do VDR ao anúncio.

[Abrir fonte original](https://www.bayes.citystgeorges.ac.uk/news-and-events/news/2024/june/cautious-m-and-a-investors-investing-in-extensive-due-diligence)

## 10 Referências institucionais e documentos do projeto

### 7 Conselho Administrativo de Defesa Econômica

Guia para análise da consumação prévia de atos de concentração econômica. 2015. Fonte oficial brasileira. Ver seções 2.1–2.6, especialmente pp. 10–13. Usada para caracterizar o processo de referência, não para estabelecer taxas ou aconselhar uma operação específica.

[Abrir fonte original](https://cdn.cade.gov.br/Portal/centrais-de-conteudo/publicacoes/guias-do-cade/gun-jumping-versao-final.pdf)

### 8 Federal Trade Commission

Avoiding antitrust pitfalls during pre merger negotiations and due diligence. 20 de março de 2018. Orientação oficial dos EUA. Ver recomendações para partes que recebem informação, revisão de relatórios e clean teams. Referência de controles; não substitui o contexto brasileiro.

[Abrir fonte original](https://www.ftc.gov/enforcement/competition-matters/2018/03/avoiding-antitrust-pitfalls-during-pre-merger-negotiations-due-diligence)

### 9 National Institute of Standards and Technology

AI RMF Playbook Measure. Página de referência consultada em 2026. Ver recomendações de medição e documentação de supervisão humana, alterações de resultados, erros e adjudicação. Orientação de governança, sem amostra ou benchmark empresarial.

[Abrir fonte original](https://airc.nist.gov/airmf-resources/playbook/measure/)

### 10 King, C.; World Commerce and Contracting

Navigating the fog of uncertainty. 10 de abril de 2025. Divulgação da associação sobre dados de 2023. Ver parágrafo com ciclos de 11,6 e 13,7 semanas. Amostra e decomposição dos tempos não explicitadas nessa página.

[Abrir fonte original](https://news.worldcc.com/news-from-worldcc/navigating-the-fog-of-uncertainty?hs_amp=true)

### 11 Thomson Reuters

AI set to save professionals 12 hours per week by 2029. 9 de julho de 2024. Comunicado original do Future of Professionals 2024; mais de 2.200 respondentes. Os tempos são previsões declaradas, não experimento cronometrado.

[Abrir fonte original](https://www.thomsonreuters.com/en/press-releases/2024/july/ai-set-to-save-professionals-12-hours-per-week-by-2029)

### 12 Thomson Reuters Institute

Future of Professionals Report 2026. 2026, coleta em março e abril. Ver Key findings e About this report. Pesquisa global com 1.816 profissionais de várias áreas. Uso não sancionado de IA é autorrelato; não mede erro ou intervenção por tarefa.

[Abrir fonte original](https://www.thomsonreuters.com/en/institute/future-of-professionals-2026/report)

### 13 University of Minnesota Law School

Research Insights AI and the Future of Human Legal Reasoning. Minnesota Law Magazine, Spring 2026. Divulgação institucional de experimento com cerca de 100 estudantes. Útil para discutir revisão e qualidade; não oferece tempo ou taxa de retrabalho para M&A.

[Abrir fonte original](https://law.umn.edu/magazine/spring-2026/research-insights-ai-and-future-human-legal-reasoning)

### D1 Diagnóstico executivo do projeto

../historico/diagnostico-da-referencia.docx, arquivo local consultado integralmente. Ver seções 1, 5 e 7: ferramentas simuladas, baseline empresarial a obter e métricas propostas. Os resultados históricos nele informados não foram recalculados neste levantamento.

### Documento complementar de delimitação

../pesquisa/problema-e-tarefa.md, no diretório dataset, consultado para contextualizar o recorte de revisão de solicitações de informação no pré fechamento. Seus links e casos não substituíram a verificação das fontes desta pesquisa.


## Contexto da reconstrução

As menções ao notebook ou ao protótipo histórico descrevem a referência anterior. A implementação de `guardiao-gate` será reconstruída do zero; este repositório contém somente documentação e dados nesta etapa. Consulte a [referência histórica](../historico/referencia-do-prototipo.md).


## Navegação do repositório

[Índice da documentação](../README.md) · [Estado atual e pendências](../planejamento/estado-atual.md)
