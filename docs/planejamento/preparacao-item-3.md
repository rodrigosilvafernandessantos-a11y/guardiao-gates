# Preparação para o item 3 — revisão do pesquisador

Registro de preparação de 17/11/2026, preservado como histórico. Atualização em 18/11/2026: o pesquisador autorizou o item 3, agora implementado. Veja o [núcleo offline](../especificacao/nucleo-offline.md) e o [protocolo atual](protocolo-experimental.md). As seções abaixo descrevem a proposta e verificações anteriores à autorização, não o estado atual.

## O que foi corrigido

| Ponto | Entrega para revisão |
|---|---|
| Contrato JEV indefinido | versão candidata JEV-1.0 com entrada, resposta e parâmetros em arquivos próprios |
| Sigilo confundido com dados pessoais | sinal `informacao_restrita` relativo à finalidade, público e canal autorizados |
| Criticidade sem fundamentação decisória | nota e confiança somente nos registros; retirada a escalada automática por nota >= 3 |
| Limiares sem origem explícita | revisão proposta a partir de 0,50 para gun jumping, informação restrita e dados pessoais inesperados; escolha sintética, não calibrada pelo artigo |
| Perfil offline incompleto | quatro respostas completas: leitura, e-mail, solicitação de preço e migração; efeito e natureza coerentes com a ferramenta |
| Formato aceitando respostas defeituosas | esquemas e validação estrita, com testes negativos |
| Situação documental desatualizada | protocolo v0.3 e guias indicam contrato definido, mas sem aprovação para iniciar o item 3 |

## Esclarecimento confirmado

O pesquisador confirmou o uso do termo **contrato** para a interface de integração do Guardião com o JEV da Typesafe. Os perfis offline simulam essa interface. A compatibilidade dos seis campos com a API nativa será verificada antes da integração real. Essa confirmação de terminologia não inicia o item 3: o pesquisador solicitou que o avanço seja perguntado explicitamente.

## Decisões submetidas à aprovação

1. Adotar JEV-1.0 como contrato candidato da construção offline, com seis sinais e versão obrigatória.
2. Usar os limiares propostos somente para tornar uma ação admissível mais restritiva. Proibições, acesso e alçadas permanecem determinados pela política.
3. Manter criticidade e confiança sem influência sobre decisões nesta versão.
4. Iniciar o item 3 após o aceite, usando exclusivamente ferramentas simuladas e respostas fixas do classificador, com T01/T07/T12 como primeiros fluxos completos.

O aceite do pesquisador será registrado no protocolo e em `config/jev-1.0.json`, seguido de regeneração dos dados e conferência. Até lá, `approved_for_item_3=false` permanece explícito. Esse campo registra uma decisão de projeto; não é uma credencial ou aprovação de ação de negócio.

## Evidência de preparação

- 16 verificações automatizadas passaram: nove de materialização e sete do contrato JEV.
- As verificações tratam de formato, integridade, isolamento, perfis e preservação dos casos especiais. Não medem desempenho do JEV ou eficácia do controlador ainda não implementado.
- A reexportação é determinística. Os textos de negócio e os oráculos centrais/pareados permanecem preservados.
- Os 56 casos continuam sem execução experimental. A configuração B0 continua sem amostras geradas.

## Definições antes das etapas posteriores

Condições com/sem controlador, quantidade final de sessões, limites da execução com modelo, rubrica de utilidade, modelo/provedor e orçamento serão congelados antes da coleta correspondente. O perfil humano real para revisão de domínio continua pendente; nenhuma aprovação técnica o substitui.

## Arquivos para revisar

- [Contrato JEV-1.0](../especificacao/contrato-jev.md): campos, significado dos sinais, critérios e limites.
- [Protocolo v0.3](protocolo-experimental-v0.3.md): foco confirmado, contrato candidato e escopo da aprovação.
- [Configuração JEV](../../config/jev-1.0.json): parâmetros canônicos e estado de aprovação.
- [Guia dos dados](../../data/cases/README.md): estrutura, carregamento e verificações.
