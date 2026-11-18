# Estado atual e pendências

Data: 17/11/2026. Este registro descreve a organização e a materialização dos dados de `guardiao-gate`, não uma execução de piloto.

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
| Política | MA-SIM-1.0, papéis e quatro ferramentas previstas | exportação declarativa; controlador não implementado |
| Estados | S01–S10 | materializados em JSON, incluindo estados excepcional e inválido |
| Documentos | D01–D07 | corpos separados, D07 restrito, catálogo com hashes |
| Ataques | dez pares normal/malicioso | vinte entradas materializadas e escopos separados |
| Testes | 36 centrais + vinte pareados | 56 casos carregáveis, oráculos separados; experimento não executado |
| Revisão | procedimento e formulário | avaliação humana qualificada pendente |

## Próxima etapa técnica

O [roadmap do notebook](roadmap-notebook.md), elaborado em 17/11/2026, organiza as atividades abaixo em entregas e critérios de avanço. É um plano; a implementação e os resultados continuam pendentes.

- Obter aprovação do [contrato candidato JEV-1.0](../especificacao/contrato-jev.md) e do avanço ao núcleo offline; concluir as decisões da coleta com modelo antes dessas rodadas.
- Manter os dados materializados e seus oráculos separados; conferir hashes pelo [guia dos casos](../../data/cases/README.md).
- Construir ferramentas simuladas instrumentadas e o controlador.
- Reconstruir o notebook após definir essa separação; nenhum notebook foi criado agora.
- Executar os testes determinísticos e só depois avaliar o comportamento com modelo.
- Gerar os dados de B0 e definir uma comparação de esforço com unidades e casos equivalentes.

## Materialização concluída

Os textos foram exportados sem respostas de referência no corpo, com pares B/M construídos deterministicamente. Estados, atores, regras, ações canônicas, aprovações e condições de falha foram convertidos em arquivos carregáveis. A configuração B0 foi exportada, mas suas amostras não foram geradas. Há um carregador e verificações de integridade, isolamento e fidelidade à fonte; essas verificações não são execuções dos 56 casos do experimento.

O contrato candidato JEV-1.0 já define entrada, resposta e quatro perfis offline completos. Criticidade e confiança ficam apenas nos registros; os limiares de revisão são escolhas sintéticas identificadas. A configuração permanece sem aprovação para iniciar o item 3. A aprovação das perguntas do protocolo não resolve automaticamente as demais decisões metodológicas nem substitui revisão de domínio.

## Decisões humanas pendentes

- Confirmar com o orientador o uso de pesquisa documental e baseline sintética.
- Realizar revisão de domínio antes de apresentar política e resultados esperados como validados.
- Definir participantes, patrocinador e coleta real caso a entrega inclua aplicação empresarial.

O roadmap em Word é preservado como plano anterior à reconstrução. Suas referências ao notebook antigo devem ser lidas no contexto do [histórico](../historico/referencia-do-prototipo.md).

[Índice](../README.md)
