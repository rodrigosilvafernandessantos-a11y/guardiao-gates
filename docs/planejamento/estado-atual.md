# Estado atual e pendências

Data: 19/11/2026. Este registro inclui dados, controles, avaliação dos 56 casos offline e integração ao notebook reproduzível. Não houve execução com modelo ou aplicação empresarial.

## Decisões de organização

1. A nova implementação será reconstruída do zero.
2. O notebook anterior fica fora deste repositório; não é base operacional nem prova dos novos controles.
3. Os arquivos de origem foram preservados nas pastas anteriores; este repositório recebeu cópias.
4. Os materiais atuais foram divididos entre pesquisa, especificação, avaliação e governança.
5. Os dados brutos permanecem separados das adaptações e dos resultados.

## O que já está documentado

| Área | Disponível | Situação |
|---|---|---|
| Problema | tarefa de revisão de pedidos no contexto de M&A | recorte acadêmico fundamentado documentalmente |
| Evidências | entrevistas públicas e fontes complementares | não são entrevistas próprias |
| Baseline | hipóteses, configuração e fórmulas B0 | sintética; geração ainda pendente |
| Política | MA-SIM-1.0, papéis e quatro ferramentas simuladas | controles avançados offline implementados e avaliados na suíte conhecida |
| Estados | S01–S10 | materializados em JSON, incluindo estados excepcional e inválido |
| Documentos | D01–D07 | corpos separados, D07 restrito, catálogo com hashes |
| Ataques | dez pares normal/malicioso | vinte entradas materializadas e escopos separados |
| Testes | 36 centrais + vinte pareados | 56/56 casos coincidentes na avaliação offline; detalhes no resumo da suíte |
| Revisão | procedimento e formulário | avaliação humana qualificada pendente |

## Próxima etapa técnica

O [roadmap do notebook](roadmap-notebook.md), elaborado em 17/11/2026, organiza as atividades abaixo em entregas e critérios de avanço. Os itens 3 e 4 foram autorizados e implementados; a suíte completa está avaliada no escopo offline, com resultados isolados por rodada.

- Definir e integrar o agente e o JEV reais no item 6, fixando versões, perguntas configuradas, limites de sessão e orçamento antes da coleta. O contrato normalizado continua aceito para uso offline.
- Manter os dados materializados e seus oráculos separados; conferir hashes pelo [guia dos casos](../../data/cases/README.md).
- Preservar o [núcleo offline implementado](../especificacao/nucleo-offline.md) e suas evidências, ampliando os cenários de forma explícita.
- Preservar o notebook e as evidências de reprodução, mantendo a separação entre células, controles e dados.
- Preservar a execução completa dos 56 casos e definir o desenho final antes de avaliar comportamento com modelo.
- Gerar os dados de B0 e definir uma comparação de esforço com unidades e casos equivalentes.

## Materialização concluída

Os textos foram exportados sem respostas de referência no corpo, com pares B/M construídos deterministicamente. Estados, atores, regras, ações canônicas, aprovações e condições de falha foram convertidos em arquivos carregáveis. A configuração B0 foi exportada, mas suas amostras não foram geradas. Há um carregador e verificações de integridade, isolamento e fidelidade à fonte; essas verificações não são execuções dos 56 casos do experimento.

O contrato JEV-1.0 define entrada, resposta e quatro perfis offline completos. Criticidade e confiança ficam apenas nos registros; os limiares de revisão são escolhas sintéticas identificadas. A configuração registra a autorização explícita do pesquisador em 18/11/2026 para iniciar o item 3, agora implementado. A aprovação das perguntas do protocolo não resolve automaticamente as demais decisões metodológicas nem substitui revisão de domínio.

## Núcleo offline implementado

O item 3 contém as quatro ferramentas, o fluxo permitir/escalar/bloquear, aprovação simulada específica, relógio virtual e exportação por rodada. Os primeiros fluxos T01/T07/T12 foram preservados. O item 4 ampliou os controles para os 56 casos, todos coincidentes com os oráculos de decisão, estado final e contagem. As 52 verificações automatizadas passaram. T31/T32 preservam efeitos desconhecidos, T30 explicita falha de auditoria e T33 tem uma invocação entre duas requisições concorrentes. Consulte o [resumo da suíte](../../results/resumo-suite-offline.md).

## Notebook reproduzível

O notebook principal está em `notebooks/experimento-guardiao-gate.ipynb`. Ele confere ambiente e hashes, executa os 56 casos, apresenta resultados e divergências e publica análise sem sobrescrever a rodada original. O executor em kernel novo preserva a cópia executada; a fonte fica limpa. Duas sessões novas, iniciadas na raiz e em notebooks/, concluíram as 12 células de código e reproduziram os 56 casos, com mesmas entradas, código, ambiente, parâmetros e resultados. As 62 verificações automatizadas passaram. Consulte o [guia](../especificacao/notebook-reproduzivel.md) e o [resumo da validação](../../results/resumo-notebook-reproduzivel.md).

## Decisões humanas pendentes

- Confirmar com o orientador o uso de pesquisa documental e baseline sintética.
- Realizar revisão de domínio antes de apresentar política e resultados esperados como validados.
- Definir participantes, patrocinador e coleta real caso a entrega inclua aplicação empresarial.

O roadmap em Word é preservado como plano anterior à reconstrução. Suas referências ao notebook antigo devem ser lidas no contexto do [histórico](../historico/referencia-do-prototipo.md).

[Índice](../README.md)
