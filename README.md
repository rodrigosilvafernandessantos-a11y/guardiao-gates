# Guardião Gate

Projeto acadêmico IBMEC sobre controle de ações, riscos e responsabilidades de agentes de IA no contexto de fusões e aquisições.

**Estado em 17/11/2026:** repositório documental e de dados. O notebook e o agente serão reconstruídos do zero. Não há notebook, implementação, teste executado ou resultado novo neste repositório.

## Comece por aqui

1. [Visão geral do projeto](docs/visao-geral/visao-geral-do-projeto.docx).
2. [Estado atual, decisões e pendências](docs/planejamento/estado-atual.md).
3. [Índice completo da documentação](docs/README.md).
4. [Catálogo de dados e proveniência](data/README.md).
5. [Organização e regras de nomes](docs/organizacao/estrutura-e-convencoes.md).

## Estrutura

```text
guardiao-gate/
├── README.md
├── docs/
│   ├── visao-geral/      apresentação do projeto
│   ├── planejamento/    roteiro e estado atual
│   ├── pesquisa/        problema e evidências documentais
│   ├── especificacao/   regras, estados e documentos do piloto
│   ├── avaliacao/       baseline, ataques e casos esperados
│   ├── governanca/      revisão humana de domínio
│   ├── tcc/             orientações acadêmicas
│   ├── organizacao/     convenções e inventário de migração
│   └── historico/       versões e documentos anteriores
├── data/
│   ├── raw/             cópias integrais dos datasets originais
│   ├── provenance/      fontes e hashes
│   ├── fixtures/        reservado para documentos de entrada separados
│   └── cases/           reservado para casos e configurações carregáveis
├── notebooks/           reservado para reconstrução futura
└── results/             reservado para novas execuções
```

## Limites desta etapa

- Os sete documentos D01–D07, dez estados e 56 casos estão **especificados em Markdown**, não materializados para execução.
- A política MA-SIM-1.0 é uma referência provisória; a validação humana qualificada permanece pendente.
- As entrevistas são públicas/documentais; a baseline é sintética, não medição empresarial.
- Os documentos Word e PowerPoint foram copiados integralmente, sem revisão de conteúdo. O estado atual desta página e do planejamento prevalece sobre descrições da implementação anterior.
- O notebook antigo não foi importado. Referências antigas foram contextualizadas no [histórico](docs/historico/referencia-do-prototipo.md).

## Dados e Git

Os datasets originais estão disponíveis em `data/raw/`, mas suas subpastas estão excluídas do versionamento para evitar arquivos volumosos. Um clone Git isolado não contém esses dados. Consulte o [catálogo de proveniência](data/provenance/catalogo-datasets.json) e o [guia dos dados](data/README.md) para fontes e conferência de hashes.

Nenhuma credencial, ambiente Python ou arquivo temporário do Word foi importado. Não foi definida licença geral para o projeto; os datasets mantêm seus avisos próprios. Não há repositório remoto configurado.

[Inventário da organização](docs/organizacao/inventario-migracao.csv)
