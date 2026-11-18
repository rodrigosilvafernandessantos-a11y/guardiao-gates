# Protocolo experimental — Guardião Gate

Versão: 0.3. Data: 17/11/2026. Estado: perguntas e foco confirmados; contrato JEV-1.0 candidato preparado para aprovação do avanço ao item 3. Protocolo global ainda não congelado. Nenhum teste do agente executado por este protocolo.

Este registro desenvolve a etapa 1 do [roadmap do notebook](roadmap-notebook.md). O pesquisador confirmou a pergunta central, as perguntas específicas e o foco principal em segurança, utilidade e rastreabilidade. A comparação de processo B0/B1 permanece secundária. Condições comparativas, amostra e parâmetros ainda serão definidos.

## 1. Perguntas do experimento — confirmadas

### Pergunta central

Em uma simulação de revisão de pedidos de informação e ação em M&A, em que medida o Guardião Gate impede a execução de ações não autorizadas, preservando a conclusão correta das tarefas permitidas e a rastreabilidade das decisões?

### Perguntas específicas

| ID | Pergunta | Evidência necessária |
|---|---|---|
| Q01 | O controlador aplica corretamente as decisões de permitir, escalar e bloquear previstas na política? | decisão inicial, estado final e invocações observadas comparados à referência de cada caso |
| Q02 | As ações supervisionadas só executam com aprovação válida e específica, inclusive após alterações, expiração, parada e tentativas de reutilização? | vínculo da aprovação com a ação e contagem de invocações nos casos de aprovação e falha |
| Q03 | Diante de instruções maliciosas em documentos, o agente tenta ações não autorizadas e o controlador impede sua execução? | propostas do modelo, decisões do controlador, invocações e efeitos por sessão maliciosa |
| Q04 | O sistema conclui corretamente as tarefas legítimas nas versões normais e maliciosas dos documentos? | rubrica de utilidade definida previamente e avaliação separada das variantes B/M |
| Q05 | Os registros permitem reconstruir o que foi proposto, decidido, aprovado e executado, incluindo falhas e efeitos desconhecidos? | cadeia de eventos por rodada, caso e ação; recibos e ausências explicitadas |

### Pergunta secundária de processo

Q06: em solicitações equivalentes, como o processo com Guardião (B1) se compara à referência humana sintética (B0) em esforço, erros, revisões e participação humana?

Esta pergunta depende de carteira comparável e tempos humanos medidos ou hipóteses B1 explicitamente modeladas. Latência do modelo e aprovações automáticas do simulador não medem esforço humano. Sem esses dados, a comparação permanece limitada e não sustenta ganho de produtividade observado.

### Comparação técnica para avaliar redução

Se o objetivo incluir atribuir uma redução de execuções indevidas ao controlador, acrescentar a comparação do mesmo agente com e sem controlador, exclusivamente em ferramentas simuladas e sob condições equivalentes. A pergunta central proposta permite avaliar o sistema; uma alegação comparativa de redução exige essa condição adicional.

### Recorte proposto

- Simulação acadêmica, com empresas, identidades, aprovações e efeitos fictícios.
- Quatro ferramentas previstas na especificação vigente; estados S01–S10 e política provisória MA-SIM-1.0.
- Primeira avaliação: 36 casos centrais e vinte variantes dos dez pares normal/malicioso. São 56 casos, não 56 sessões com modelo.
- Avaliação offline dos controles separada da avaliação de comportamento com modelo e da simulação de processo B0/B1.
- Decisões e resultados esperados tratados como referência provisória do pesquisador enquanto a revisão de domínio permanecer pendente.
- Sem meta antecipada de ganho de tempo ou redução percentual de erros. Resultados desfavoráveis e desconhecidos serão preservados.

## 2. Próximas definições da etapa 1

| Ordem | Definição | Situação |
|---|---|---|
| 1 | Pergunta central, perguntas específicas e prioridade de B0/B1 | confirmadas pelo pesquisador |
| 2 | Condições comparadas, amostra, repetições e encerramento de sessão | a definir |
| 3 | Regras, precedência e papel dos sinais JEV | definidos no contrato candidato JEV-1.0; aguardando aprovação |
| 4 | Formatos de tarefa, ação, sinais, aprovação, recibo e evento | entrada/resposta JEV com esquemas; casos e aprovações materializados; recibos e eventos operacionais serão detalhados na construção offline |
| 5 | Métricas, denominadores, rubrica de utilidade e critérios de conclusão | a congelar após as definições anteriores |
| 6 | Ambiente, versões, configuração e registro de mudanças | a definir |

O protocolo só será denominado congelado após resolver essas definições e registrar a versão de referência. Alterações posteriores deverão preservar a versão anterior e indicar quais casos e resultados são afetados.

## 3. Preparação dos dados

Por solicitação do pesquisador, os documentos, estados e 56 casos da especificação vigente foram materializados, com respostas esperadas separadas. Consulte o [guia dos dados](../../data/cases/README.md). Essa preparação não congela as definições metodológicas pendentes acima. O contrato candidato JEV-1.0 agora especifica entrada, resposta, uso dos sinais e perfis completos. Seu aceite e o avanço ao item 3 permanecem aguardando aprovação do pesquisador.


## 4. Contrato candidato JEV-1.0

Referências canônicas: [especificação do contrato](../especificacao/contrato-jev.md), [configuração](../../config/jev-1.0.json) e esquemas de [entrada](../../schemas/jev-entrada-1.0.schema.json) e [resposta](../../schemas/jev-resposta-1.0.schema.json).

- Seis sinais: `gun_jumping`, `informacao_restrita`, `dados_pessoais`, `efeito_externo`, `natureza` e `criticidade`. Versão obrigatória `JEV-1.0`.
- `informacao_restrita` considera finalidade, público e canal autorizados; confidencialidade isolada não torna a leitura interna indevida.
- Criticidade e confiança são auxiliares de registro. A proposta anterior de escalada por criticidade >= 3 foi retirada.
- Limiares propostos de revisão: 0,50 para gun jumping, informação restrita e dados pessoais inesperados, com comparação inclusiva. São escolhas sintéticas, sem calibração ou fundamento numérico no artigo.
- Cadastro da ferramenta, contexto confiável, proibições e alçadas prevalecem. JEV não aprova, muda estado, concede acesso ou altera a política.
- Quatro perfis offline completos e coerentes com as ferramentas. Os riscos são deliberadamente favoráveis para isolar os controles; não são classificações empíricas dos casos.
- Formato validado não equivale a aprovação de uso: `approved_for_item_3=false` até aceite explícito do pesquisador.

A fundamentação conceitual foi registrada a partir do Artigo-V14, com referência por seção e hash da versão consultada. Os ajustes não alteram o conteúdo das fixtures ou os resultados esperados dos 56 casos.

## 5. Escopo da aprovação solicitada

Aprovar este pacote significa aceitar o contrato candidato e autorizar o início do núcleo offline do item 3: quatro ferramentas simuladas, estado confiável, relógio e registros, com os fluxos iniciais T01/T07/T12. A construção do controlador ainda não foi iniciada.

O protocolo das rodadas com modelo permanece aberto: condições comparadas, repetições finais, limites de sessão, rubrica de utilidade, modelo, custos e ambiente da coleta serão definidos antes de executar essas rodadas. Para a preparação atual foram usadas apenas bibliotecas padrão Python, sem conexão a modelos ou serviços externos. Não se presume aceite dessas decisões futuras pela aprovação do núcleo offline.

A [versão 0.2](protocolo-experimental-v0.2.md) foi preservada. A revisão humana de domínio continua pendente, independentemente do aceite técnico do pesquisador.


## 6. Esclarecimento registrado com o pesquisador

Foi confirmada a manutenção da palavra **contrato** para a interface de integração entre o Guardião e o JEV da Typesafe. A versão `JEV-1.0` pertence ao contrato do projeto, não ao modelo. Os campos propostos serão conferidos contra a interface nativa antes da integração real; essa compatibilidade ainda não foi verificada.

O núcleo offline utilizará respostas fixas que simulam a interface normalizada, permitindo testar o Guardião sem modelo, internet ou ações reais. Essa simulação não constitui avaliação do JEV. O pesquisador solicitou uma nova pergunta antes do avanço ao item 3; portanto, o registro permanece `approved_for_item_3=false` até a resposta explícita.
