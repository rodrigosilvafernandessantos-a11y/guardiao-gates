# Estrutura e convenções

## Separação de responsabilidades

| Local | Conteúdo | Evitar |
|---|---|---|
| `docs/pesquisa/` | problema e evidências | apresentar hipótese como medição |
| `docs/especificacao/` | regras, estados e contrato do piloto | misturar resultados executados |
| `docs/avaliacao/` | baseline, ataques e referência dos testes | expor respostas esperadas ao agente |
| `docs/governanca/` | revisão e responsabilidades | presumir aprovação humana |
| `docs/historico/` | cópias de versões anteriores | carregar como fonte vigente do simulador |
| `data/raw/` | arquivos originais dos datasets | editar corpus ou usar dados restritos como contexto geral |
| `data/provenance/` | origem e integridade | apagar avisos de licença |
| `data/fixtures/` | futuras entradas separadas | colocar oráculos junto das entradas do agente |
| `data/cases/` | futuros casos, estados e configurações | credenciais ou resultados observados |
| `notebooks/` | futura interface de experimentação | concentrar todas as regras e responsabilidades |
| `results/` | futuras saídas por rodada | sobrescrever histórico ou misturar execuções |

## Nomes

- Pastas e documentos autorais usam nomes descritivos em minúsculas, sem espaços ou acentos e com hífen.
- Títulos internos permanecem em português com acentuação.
- Nomes e bytes dos arquivos dos datasets originais foram preservados dentro de cada subpasta.
- IDs D01, S01, T01 e P01-B/P01-M permanecem estáveis: mover arquivo não altera o significado do caso.
- Os blocos de JSON, textos contratuais e payloads dos Markdown foram preservados; somente referências de localização e navegação foram ajustadas.
- Os arquivos Word e PowerPoint foram copiados sem alteração; referências internas antigas são contexto histórico.

## Fonte vigente e duplicação

A leitura começa pelo [índice](../README.md). Os dez documentos atuais são a referência de trabalho. Algumas tabelas e minutas são repetidas nos documentos por contexto; essa repetição foi preservada nesta organização. Na futura implementação, cada entrada e cada oráculo deve ter uma fonte canônica separada.

Os manifestos terminados em `.original.json` conservam a informação da coleta anterior, inclusive nomes antigos de pastas. O catálogo atual informa o mapeamento para os caminhos novos. Não editar os manifestos originais para fingir que foram produzidos nesta organização.

## Rastreabilidade

O [inventário](inventario-migracao.csv) registra, por arquivo copiado, origem relativa à pasta Projeto Final, destino relativo a este repositório, tratamento e hashes SHA-256. Arquivos organizacionais novos não são apresentados como cópias de fontes anteriores.

O notebook antigo, requisitos e resultados de execuções anteriores não foram importados. Os diretórios das etapas anteriores permanecem preservados fora deste repositório.
