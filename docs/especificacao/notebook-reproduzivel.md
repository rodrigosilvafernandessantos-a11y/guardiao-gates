# Notebook reproduzível — item 5

Data: 19/11/2026. Notebook: [experimento-guardiao-gate.ipynb](../../notebooks/experimento-guardiao-gate.ipynb). Escopo autorizado: organizar e executar preparação, suíte offline e análise, preservando cada rodada. Não inclui JEV real, outro modelo ou simulação B0/B1.

## Sequência de uso

1. Abrir a cópia completa do repositório, com as fixtures e configurações versionadas. Os corpora volumosos em `data/raw/` não são necessários ao notebook offline.
2. Usar Python 3.12, com referência validada em 3.12.8/macOS. Os pacotes estão fixados em [requirements-notebook.txt](../../requirements-notebook.txt). O conjunto usa IPython que exige Python 3.11 ou superior.
3. Selecionar no editor o ambiente que contém essas dependências. Salvar o notebook, reiniciar o kernel e executar todas as células em ordem.
4. Consultar a pasta de rodada e a análise exibidas ao final. Repetir o procedimento cria outra rodada, sem sobrescrever as anteriores.

Para criar um ambiente local, se necessário:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-notebook.txt
```

A instalação inicial pode exigir internet; nenhuma instalação é executada automaticamente por uma célula. As versões foram obtidas e verificadas no ambiente local disponível. Outros sistemas e versões de Python precisam de validação própria; não se presume equivalência entre plataformas.

## Executar sem editor

Na raiz, com o ambiente ativado:

```sh
python scripts/executar_notebook.py
```

O comando abre um **kernel Jupyter novo**, executa as células reais em ordem e preserva as saídas. Não usa um laço de `exec` como substituto do kernel. A comunicação é IPC local, sem conexão a serviço externo, com arquivos temporários isolados; configurações pessoais do IPython não são utilizadas.

Para verificar a localização da raiz em outra posição de trabalho do kernel:

```sh
python scripts/executar_notebook.py --kernel-cwd root
python scripts/executar_notebook.py --kernel-cwd notebooks
```

O executor é especializado neste notebook do projeto, em Unix/macOS. Um editor compatível com Jupyter pode ser usado para interação; não foi instalado ou escolhido um editor específico. A fonte versionada fica sem outputs; a cópia com resultados é salva dentro da rodada.

## Conteúdo das 12 etapas

| Etapa | Conteúdo |
|---|---|
| 1 | localização da raiz e importação dos componentes |
| 2 | modo explícito, versões do ambiente e configuração |
| 3 | inventário e integridade dos dados |
| 4 | ferramentas, estados e responsabilidades |
| 5 | execução completa dos 56 casos |
| 6 | leitura dos resultados preservados e indicadores |
| 7 | tabela dos 36 casos centrais |
| 8 | tabelas dos vinte pareados e sondagens |
| 9 | falhas esperadas e efeitos desconhecidos |
| 10 | divergências e prontidão técnica local |
| 11 | situação das etapas futuras com modelo e B0/B1 |
| 12 | exportação da análise e links para os registros |

O arquivo tem 25 células: 13 de explicação e 12 de código. O notebook chama os componentes existentes, sem duplicar regras, alçadas ou respostas esperadas nas células.

## Preparação antes de criar uma rodada

O padrão é `MODO="offline"` e `USAR_MODELO=False`. Ativar modelo nesta entrega gera erro explícito antes da coleta. Não há endpoint, credencial ou cliente de modelo embutido.

A preparação valida versões dos pacotes, versão mínima de Python, caminhos, hashes e inventário. A conferência estrita de dependências é o padrão. As versões observadas e os parâmetros efetivos entram no contexto da execução, sem copiar variáveis de ambiente ou credenciais.

O caminho da raiz é descoberto a partir do diretório de trabalho; não contém caminhos absolutos deste computador. `GUARDIAO_PROJECT_ROOT` é uma opção explícita para outra cópia completa. As saídas ficam em `results/` ou em suas subpastas. Arquivos de entrada alterados ou ausentes não são regenerados silenciosamente pelo notebook.

O kernel recebe os contratos e fixtures pelos carregadores existentes. D07 não é exibido na inspeção comum, e as entradas de avaliação não são transformadas em contexto de um agente.

## Preservação por rodada

O executor da suíte mantém seu manifesto e todos os registros do item 4. Quando chamado pelo notebook, inclui também:

- `contexto-execucao.json`: modo, parâmetros, inventário, ambiente, versões e hashes de preparação.
- `notebook-fonte.ipynb`: cópia da fonte salva no disco no início da rodada, vinculada por SHA-256.
- Hashes da configuração do notebook, dependências e executor.

A análise gera uma subpasta `analise-notebook/`, com `analise.md`, `analise.json` e `manifesto-analise.json`. O manifesto da rodada original não é reescrito para incluir análises posteriores; cada análise aponta para seu hash. Reexecutar somente a célula de publicação não sobrescreve a análise existente: para nova rodada, reiniciar e executar tudo.

Pelo comando de execução em kernel novo, a mesma subpasta recebe `notebook.executado.ipynb` e `execucao-jupyter.json`, que registra a fonte, o notebook executado, os manifestos e o número de células concluídas. O arquivo-fonte do repositório continua limpo. Em execução interativa, os registros e a análise são automáticos, mas o salvamento do notebook com outputs depende do editor.

Caso uma célula falhe, o executor preserva `notebook-parcial.ipynb` e um registro de erro em uma pasta exclusiva `notebook-falhou-*`, sem eliminar uma rodada que já tenha sido gerada. Divergências de casos são diferentes de erro de célula: a suíte conclui a coleta e o notebook publica a análise desfavorável; o executor retorna status de divergência ao final.

A validação de desenvolvimento encontrou um erro de formatação numa célula de análise. A rodada e a cópia parcial foram mantidas; o problema foi corrigido, e a sintaxe de todas as células passou a ser verificada antes de iniciar um kernel.

## Reproduzir resultados, sem exigir bytes idênticos

Cada rodada recebe identificadores e timestamps novos; T33 pode trocar a ordem do vencedor e os IDs de threads. Esses campos não são utilizados como prova de alteração de comportamento.

A comparação verifica entradas, código, parâmetros, ambiente registrado, métricas e resultados por caso, tratando T33 como conjunto de desfechos. Não remove diferenças de estado, contagem, efeitos desconhecidos, critérios ou respostas internas. Os hashes da rodada original continuam íntegros e não são normalizados ou reescritos.

O helper `compare_runs` gera uma comparação explícita. Repetir estes casos conhecidos não mede variabilidade ou generalização de um modelo, pois nenhum modelo está presente. A versão de Python, os pacotes e a configuração ficam registrados; os pacotes internos de decisão continuam usando apenas a biblioteca padrão.

## Limites científicos

- A rubrica dos pares verifica extração e critérios fixos, não utilidade de modelo.
- As 26 sondagens pertencem aos vinte casos; não são novas sessões ou ataques espontaneamente seguidos.
- T31/T32 conservam `null`; T30 conserva a falha da trilha normal. Não tratar sucesso do teste como ausência de falha operacional simulada.
- Não são produzidos ganhos de produtividade, resultados B0/B1 ou conclusões de calibração jurídica.
- A coleta com modelo, sua configuração final e a revisão humana de domínio continuam pendentes.

Ver [resumo da validação do notebook](../../results/resumo-notebook-reproduzivel.md) e [protocolo atual](../planejamento/protocolo-experimental.md).
