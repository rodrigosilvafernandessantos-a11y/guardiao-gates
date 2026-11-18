# Guardião Gate

Projeto acadêmico IBMEC sobre controle de ações, riscos e responsabilidades de agentes de IA no contexto de fusões e aquisições.

**Estado em 17/11/2026:** documentos, estados e 56 casos materializados, com carregador e verificações de integridade dos dados. O notebook, o agente e o controlador ainda serão construídos. Não há nova execução do experimento nem resultados do agente.

## Comece por aqui

1. [Visão geral do projeto](docs/visao-geral/visao-geral-do-projeto.docx).
2. [Estado atual, decisões e pendências](docs/planejamento/estado-atual.md).
3. [Índice completo da documentação](docs/README.md).
4. [Catálogo de dados e proveniência](data/README.md).
5. [Organização e regras de nomes](docs/organizacao/estrutura-e-convencoes.md).
6. [Roadmap de construção do notebook experimental](docs/planejamento/roadmap-notebook.md).

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
│   ├── fixtures/        documentos e variantes, com manifesto de integridade
│   └── cases/           casos, configurações e oráculos separados
├── scripts/             materialização e validação dos dados
├── src/guardiao_gate/   carregador de dados; controlador ainda pendente
├── tests/               verificações da preparação dos dados
├── notebooks/           reservado para reconstrução futura
└── results/             reservado para novas execuções
```

## Limites desta etapa

- Os sete documentos D01–D07, dez estados e 56 casos foram exportados para arquivos carregáveis. Consulte o [guia de uso e validação](data/cases/README.md).
- O [contrato candidato JEV-1.0](docs/especificacao/contrato-jev.md) tem esquemas e perfis offline completos. O início do núcleo offline aguarda aprovação do pesquisador; nenhum controlador ou experimento foi executado.
- A política MA-SIM-1.0 é uma referência provisória; a validação humana qualificada permanece pendente.
- As entrevistas são públicas/documentais; a baseline é sintética, não medição empresarial.
- Os documentos Word e PowerPoint foram copiados integralmente, sem revisão de conteúdo. O estado atual desta página e do planejamento prevalece sobre descrições da implementação anterior.
- O notebook antigo não foi importado. Referências antigas foram contextualizadas no [histórico](docs/historico/referencia-do-prototipo.md).

## Dados e Git

Os datasets originais estão disponíveis em `data/raw/`, mas suas subpastas estão excluídas do versionamento para evitar arquivos volumosos. Um clone Git isolado não contém esses dados. Consulte o [catálogo de proveniência](data/provenance/catalogo-datasets.json) e o [guia dos dados](data/README.md) para fontes e conferência de hashes.

Nenhuma credencial, ambiente Python ou arquivo temporário do Word foi importado. Não foi definida licença geral para o projeto; os datasets mantêm seus avisos próprios. Não há repositório remoto configurado.

[Inventário da organização](docs/organizacao/inventario-migracao.csv)
