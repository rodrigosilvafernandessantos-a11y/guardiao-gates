# Estado atual e pendências

Data: 17/11/2026. Este registro descreve a organização de `guardiao-gate`, não uma execução de piloto.

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
| Política | MA-SIM-1.0, papéis e quatro ferramentas previstas | especificação; não implementada neste repositório |
| Estados | S01–S10 | definidos em tabela |
| Documentos | D01–D07 | conteúdo completo na especificação |
| Ataques | dez pares normal/malicioso | vinte entradas especificadas |
| Testes | 36 centrais + vinte pareados | 56 casos especificados; não executados |
| Revisão | procedimento e formulário | avaliação humana qualificada pendente |

## Próxima etapa técnica

O [roadmap do notebook](roadmap-notebook.md), elaborado em 17/11/2026, organiza as atividades abaixo em entregas e critérios de avanço. É um plano; a implementação e os resultados continuam pendentes.

- Fixar uma versão executável da política e seus esquemas.
- Separar D01–D07 e as vinte variantes dos textos de orientação ao avaliador.
- Converter estados, papéis, aprovações e casos em arquivos carregáveis.
- Construir ferramentas simuladas instrumentadas e o controlador.
- Reconstruir o notebook após definir essa separação; nenhum notebook foi criado agora.
- Executar os testes determinísticos e só depois avaliar o comportamento com modelo.
- Gerar os dados de B0 e definir uma comparação de esforço com unidades e casos equivalentes.

## Decisões humanas pendentes

- Confirmar com o orientador o uso de pesquisa documental e baseline sintética.
- Realizar revisão de domínio antes de apresentar política e resultados esperados como validados.
- Definir participantes, patrocinador e coleta real caso a entrega inclua aplicação empresarial.

O roadmap em Word é preservado como plano anterior à reconstrução. Suas referências ao notebook antigo devem ser lidas no contexto do [histórico](../historico/referencia-do-prototipo.md).

[Índice](../README.md)
