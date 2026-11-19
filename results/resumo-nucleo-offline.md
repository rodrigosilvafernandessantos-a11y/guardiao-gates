# Resumo revisado do núcleo offline — item 3

Registro da rodada inicial, preservado. A avaliação posterior dos 56 casos está no [resumo do item 4](resumo-suite-offline.md).

Data: 18/11/2026. Rodada de referência: `offline-20261118T211245Z-adac398e`.

O pesquisador autorizou a construção offline em 18/11/2026. Esta rodada executou apenas os três fluxos iniciais previstos no roadmap, com chamadas predefinidas e sinais fixos. Não houve chamada ao JEV da Typesafe, geração de resposta por modelo ou ação externa real.

| Caso | Decisão inicial | Estado final | Chamadas antes da aprovação | Invocações totais | Coincide com referência |
|---|---|---|---:|---:|---|
| T01 | PERMITIR | EXECUTADO | não aplicável | 1 | sim |
| T07 | BLOQUEAR | BLOQUEADO | não aplicável | 0 | sim |
| T12 | ESCALAR | EXECUTADO | 0 | 1 | sim |

Os três resultados coincidem com decisão, estado final e contagem esperados. Foram registradas três propostas/tentativas, duas invocações, uma leitura confirmada e um efeito externo simulado confirmado. T07 teve zero invocações de preço.

As 32 verificações automatizadas passaram: nove de materialização, sete de contrato e 16 do núcleo inicial. Incluem bloqueio de acesso direto às ferramentas, aprovação pelo papel específico, ausência de chamada antes da aprovação, preservação do conteúdo exato, alçadas conjuntas e exportação com abertura de sockets bloqueada. São verificações do software e não sessões com modelo.

## Evidências locais

- [Relatório da rodada](offline-20261118T211245Z-adac398e/relatorio.md).
- [Manifesto, ambiente e hashes](offline-20261118T211245Z-adac398e/manifesto.json).
- [Eventos e aprovações](offline-20261118T211245Z-adac398e/eventos.jsonl).
- [Casos observados](offline-20261118T211245Z-adac398e/casos-observados.csv).
- [Recibos dos mocks](offline-20261118T211245Z-adac398e/recibos.json).
- [Métricas](offline-20261118T211245Z-adac398e/metricas.json).

As subpastas de execução não são versionadas. O comando `python3 scripts/executar_nucleo_offline.py` regenera uma nova rodada com as mesmas condições e novos identificadores. Este resumo é preservado como registro revisado; os arquivos locais e seus hashes identificam a evidência da rodada indicada.

## Limites

A suíte de 56 casos, a concorrência e as falhas avançadas serão completadas e avaliadas no item 4. Não houve medição de utilidade do modelo, produtividade B0/B1 ou validação humana de domínio. O notebook principal ainda não foi criado. O controle básico de e-mail só libera o template processual conhecido; textos não reconhecidos permanecem em revisão.

Guia: [núcleo offline](../docs/especificacao/nucleo-offline.md).
