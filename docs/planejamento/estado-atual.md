# Estado atual e pendências

Data: 18/11/2026. Este registro inclui a materialização dos dados e a execução inicial do núcleo offline de `guardiao-gate`. Não houve execução com modelo nem avaliação completa do piloto.

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
| Política | MA-SIM-1.0, papéis e quatro ferramentas simuladas | controlador básico implementado; controles avançados serão completados no item 4 |
| Estados | S01–S10 | materializados em JSON, incluindo estados excepcional e inválido |
| Documentos | D01–D07 | corpos separados, D07 restrito, catálogo com hashes |
| Ataques | dez pares normal/malicioso | vinte entradas materializadas e escopos separados |
| Testes | 36 centrais + vinte pareados | três fluxos iniciais executados (T01/T07/T12); suíte completa ainda não executada |
| Revisão | procedimento e formulário | avaliação humana qualificada pendente |

## Próxima etapa técnica

O [roadmap do notebook](roadmap-notebook.md), elaborado em 17/11/2026, organiza as atividades abaixo em entregas e critérios de avanço. O item 3 foi autorizado pelo pesquisador e implementado; seu escopo é o dos três fluxos iniciais, com resultados isolados por rodada.

- Avançar ao item 4: completar controles e executar a suíte determinística de 56 casos, incluindo concorrência, histórico, mudanças e falhas. O contrato JEV-1.0 está aceito para uso offline.
- Manter os dados materializados e seus oráculos separados; conferir hashes pelo [guia dos casos](../../data/cases/README.md).
- Preservar o [núcleo offline implementado](../especificacao/nucleo-offline.md) e suas evidências, ampliando os cenários de forma explícita.
- Reconstruir o notebook após definir essa separação; nenhum notebook foi criado agora.
- Executar os testes determinísticos e só depois avaliar o comportamento com modelo.
- Gerar os dados de B0 e definir uma comparação de esforço com unidades e casos equivalentes.

## Materialização concluída

Os textos foram exportados sem respostas de referência no corpo, com pares B/M construídos deterministicamente. Estados, atores, regras, ações canônicas, aprovações e condições de falha foram convertidos em arquivos carregáveis. A configuração B0 foi exportada, mas suas amostras não foram geradas. Há um carregador e verificações de integridade, isolamento e fidelidade à fonte; essas verificações não são execuções dos 56 casos do experimento.

O contrato JEV-1.0 define entrada, resposta e quatro perfis offline completos. Criticidade e confiança ficam apenas nos registros; os limiares de revisão são escolhas sintéticas identificadas. A configuração registra a autorização explícita do pesquisador em 18/11/2026 para iniciar o item 3, agora implementado. A aprovação das perguntas do protocolo não resolve automaticamente as demais decisões metodológicas nem substitui revisão de domínio.

## Núcleo offline implementado

O item 3 contém as quatro ferramentas, o fluxo permitir/escalar/bloquear, aprovação simulada específica, relógio virtual e exportação por rodada. T01 executou uma leitura, T07 bloqueou a solicitação de preço e T12 executou um envio simulado após aprovação, com zero chamadas antes dela. As 32 verificações automatizadas de dados, contrato e núcleo passaram. A avaliação completa permanece no item 4.

## Decisões humanas pendentes

- Confirmar com o orientador o uso de pesquisa documental e baseline sintética.
- Realizar revisão de domínio antes de apresentar política e resultados esperados como validados.
- Definir participantes, patrocinador e coleta real caso a entrega inclua aplicação empresarial.

O roadmap em Word é preservado como plano anterior à reconstrução. Suas referências ao notebook antigo devem ser lidas no contexto do [histórico](../historico/referencia-do-prototipo.md).

[Índice](../README.md)
