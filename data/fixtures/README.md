# Entradas do piloto

Materializados **sete documentos-base D01–D07 e vinte variantes P01-B/P01-M a P10-B/P10-M**, exportados das especificações vigentes.

- `documentos/`: D01–D06, textos de negócio liberados para leitura interna conforme a política.
- `restritos/`: D07; leitura fora do contexto comum, mediada pelo futuro controlador.
- `pares/`: dez variantes normais e dez maliciosas. Cada sessão libera somente seu arquivo escolhido.
- `manifesto.json`: IDs, versões, caminhos, classificação, fontes, transformações, atribuição e SHA-256. É metadado do executor, não contexto do agente.

As fixtures excluem títulos de organização, linhas de metadados e respostas de referência. Mantêm o corpo de negócio exato em UTF-8/LF, sem quebra de linha terminal. B é byte a byte igual ao corpo do documento-base; M é o mesmo corpo, duas quebras LF e o payload exato, sem orientação ao avaliador.

As referências de resposta estão em [cases/oraculos/](../cases/oraculos/), fora das entradas. Consulte o [guia de carregamento e validação](../cases/README.md). O carregador verifica hashes e permite leitura apenas dos IDs explicitamente liberados pelo chamador confiável; não é implementação completa de controle de autorização.

Fontes: [documentos do piloto](../../docs/especificacao/documentos-do-piloto.md), seções 8 e 13; [ataques adaptados](../../docs/avaliacao/ataques-adaptados.md), seção 11. D01–D03 usam referências conceituais do CUAD/The Atticus Project. Os payloads adaptados atribuem NVIDIA Corporation, CC BY 4.0, com origem e alterações registradas no manifesto. Os originais e seus avisos não foram modificados.

Todos os valores e atores do piloto são fictícios. Nenhum teste do agente foi executado nesta materialização; integridade dos arquivos não valida a política de domínio.
