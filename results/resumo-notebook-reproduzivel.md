# Resumo revisado — notebook reproduzível

Data local: 19/11/2026, America/Sao_Paulo. Os identificadores das rodadas usam UTC; por isso começam em 20/11/2026.

Notebook principal: [experimento-guardiao-gate.ipynb](../notebooks/experimento-guardiao-gate.ipynb).

O item 5 foi autorizado pelo pesquisador. O notebook organiza preparação, execução e análise em 12 etapas, com 25 células (13 de explicação e 12 de código), mantendo dados, regras e avaliação em componentes externos.

## Validação em sessões novas

| Execução | Diretório de trabalho do kernel | Células de código concluídas | Casos coincidentes |
|---|---|---:|---:|
| `suite-offline-20261120T002309Z-75f75d12` | `notebooks/` | 12/12 | 56/56 |
| `suite-offline-20261120T002310Z-f435bd4d` | raiz do projeto | 12/12 | 56/56 |

As duas execuções foram feitas em processos Jupyter novos, por IPC local, com Python 3.12.8 e 30 dependências conferidas nas versões fixadas. Não houve modelo, serviço de internet ou ação real. A instalação de pacotes não foi necessária neste ambiente; sua lista foi registrada em `requirements-notebook.txt`.

## Comparação de reprodução

| Critério | Coincide entre as rodadas |
|---|---|
| Entradas | sim |
| Código e configuração | sim |
| Ambiente registrado | sim |
| Parâmetros | sim |
| Resultados por caso | sim |
| Métricas | sim |

**Reprodução confirmada no ambiente validado.** Identificadores, timestamps, hashes vinculados à rodada e a ordem de vencedor/threads em T33 podem variar. Essas variações não removem diferenças de decisão, estado final, contagem, efeito desconhecido ou rubrica. Nenhum caso teve alteração de resultado entre as duas sessões.

A primeira tentativa de desenvolvimento encontrou um erro de formatação em uma célula de análise. Sua rodada e cópia parcial foram preservadas; a correção foi seguida de conferência de sintaxe de todas as células e das execuções finais acima. Não foi apagado o registro dessa tentativa.

## Artefatos

- [Comparação estruturada das duas sessões](comparacao-notebook-kernels-limpos.json).
- [Notebook executado — sessão a partir de notebooks/](suite-offline-20261120T002309Z-75f75d12/analise-notebook/notebook.executado.ipynb).
- [Notebook executado — sessão a partir da raiz](suite-offline-20261120T002310Z-f435bd4d/analise-notebook/notebook.executado.ipynb).
- [Análise da sessão de referência](suite-offline-20261120T002310Z-f435bd4d/analise-notebook/analise.md).
- [Manifesto da rodada](suite-offline-20261120T002310Z-f435bd4d/manifesto.json).
- [Registro de execução do kernel](suite-offline-20261120T002310Z-f435bd4d/analise-notebook/execucao-jupyter.json).
- [Casos observados](suite-offline-20261120T002310Z-f435bd4d/casos-observados.csv).
- [Registro parcial da tentativa de desenvolvimento](suite-offline-20261120T001545Z-338effd3/notebook-falhou-9f59d1e8c2cb/execucao-jupyter.json).

As fontes do notebook, a análise e a execução possuem registros de hash separados, ligados à mesma rodada. A análise não reescreve o manifesto dos casos já concluídos. O notebook-fonte permanece sem outputs antigos; as cópias executadas ficam nas pastas locais de resultados, que continuam fora do Git. Este resumo e a comparação estruturada são registros revisados que podem ser versionados.

## Verificações da implementação

As **62 verificações automatizadas** passaram: as 52 anteriores de dados, contratos e controles, mais dez de preparação e análise do notebook. Foram verificados modo offline, versões, alteração de fonte, preservação de rodadas, comparação semântica, efeitos desconhecidos, análise sem sobrescrita, hashes, escape de HTML e preservação de divergência injetada em teste.

A validação do notebook em kernel novo é adicional a essas verificações: executa as células reais, em vez de apenas compilar ou simular o código. As cópias finais têm contadores nativos de execução de 1 a 12 e nenhum output de erro.

## Como repetir

Com as dependências instaladas no ambiente selecionado:

```sh
python3 scripts/executar_notebook.py
```

Em um editor compatível, abrir a fonte, salvar, reiniciar o kernel e executar todas as células. Cada execução completa cria outra rodada. [Guia completo](../docs/especificacao/notebook-reproduzivel.md).

## Limites

O resultado cobre somente o modo offline, com sinais fixos e casos sintéticos conhecidos. A utilidade observada é de extração e critérios fixos, não de modelo. T31/T32 mantêm efeitos desconhecidos e T30 mantém a indisponibilidade da trilha normal. A revisão humana de domínio continua pendente. JEV real, comparação com/sem controlador com modelo e B0/B1 não foram executados.

O próximo item é definir e integrar o agente e o classificador reais, com parâmetros, limites e orçamento da coleta.
