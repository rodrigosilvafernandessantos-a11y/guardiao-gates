# Dados do projeto

## Datasets originais

| Pasta | Material | Papel no piloto |
|---|---|---|
| [raw/cuad/](raw/cuad/) | contratos e anotações CUAD | referência de leitura e adaptação; não fornece autorização brasileira |
| [raw/indirect-prompt-injection/](raw/indirect-prompt-injection/) | casos de injeção indireta | referência de mecanismos de ataque |
| [raw/technology-ma/](raw/technology-ma/) | tabelas históricas de aquisições | apoio opcional; não define aprovação regulatória |

Os três diretórios contêm cópias integrais dos arquivos recebidos, inclusive `original.zip`, preservando os nomes internos e excluindo apenas arquivos de sistema. As fontes de coleta e seus hashes estão no [catálogo atual](provenance/catalogo-datasets.json). A documentação da seleção anterior está preservada no [histórico](../docs/historico/catalogo-datasets-anterior.md).

## Materiais autorais do piloto

- [Documentos sintéticos D01–D07](../docs/especificacao/documentos-do-piloto.md).
- [Vinte variantes dos dez pares de ataque](../docs/avaliacao/ataques-adaptados.md).
- [Casos e resultados esperados](../docs/avaliacao/casos-e-resultados-esperados.md).
- [Baseline sintética](../docs/avaliacao/baseline-sintetica.md).

O conteúdo foi exportado para [fixtures/](fixtures/README.md) e [cases/](cases/README.md): sete documentos-base, vinte variantes, dez estados e 56 casos carregáveis, com oráculos separados e hashes. O guia de casos explica os formatos, o carregamento e as pendências. Os 56 casos já têm [evidências de execução offline](../results/resumo-suite-offline.md), com chamadas predefinidas e sinais fixos. Não houve execução com modelo ou geração de amostras B0.

## Restauração e versionamento

`data/raw/` permanece local e fora do versionamento Git. Em outro computador, obter cada dataset pela origem do catálogo, manter o ZIP e verificar SHA-256 antes de extrair na pasta correspondente. Os nomes antigos nos manifestos originais são mapeados no catálogo atual. Uma clonagem sem restauração não basta para obter os corpora completos.

As licenças declaradas dos corpora e suas atribuições foram preservadas. Não há licença geral nova aplicada aos materiais de terceiros. Não importar credenciais, gravações de entrevistas ou documentos empresariais privados para estas pastas.

[Índice da documentação](../docs/README.md)
