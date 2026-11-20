# Notebook do experimento

Arquivo principal: [experimento-guardiao-gate.ipynb](experimento-guardiao-gate.ipynb).

O notebook organiza preparação, execução dos 56 casos e análise em 12 etapas (25 células, sendo 12 de código). Usa os componentes externos; não duplica política, mocks ou respostas esperadas nas células. O modo padrão é offline, sem modelo ou ações reais.

## Rodar do início ao fim

1. Usar Python 3.12 (referência validada: 3.12.8/macOS) e instalar [requirements-notebook.txt](../requirements-notebook.txt) no ambiente selecionado pelo kernel.
2. Abrir o notebook na cópia completa do repositório, salvar, reiniciar o kernel e executar todas as células em ordem.
3. Abrir a pasta de resultados e a análise indicadas na última célula. Cada execução gera outra rodada.

Também é possível executar sem editor:

```sh
python3 scripts/executar_notebook.py
```

Esse comando deve ser chamado na raiz, com as dependências disponíveis. Ele cria um kernel Jupyter novo, executa as células e salva `notebook.executado.ipynb` dentro da rodada. A fonte versionada fica sem outputs. O executor usa IPC local e não chama serviços externos.

As versões das dependências, os parâmetros efetivos e hashes da fonte entram na execução. A instalação inicial pode exigir internet; nenhuma célula instala pacotes. No modo offline, os corpora grandes de `data/raw/` não são necessários.

[Guia completo](../docs/especificacao/notebook-reproduzivel.md) · [Validação de reprodução](../results/resumo-notebook-reproduzivel.md) · [Roadmap](../docs/planejamento/roadmap-notebook.md)
