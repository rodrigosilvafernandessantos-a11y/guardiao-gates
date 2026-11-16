# Datasets para a simulação do Guardião de Gates de M&A

Seleção orientada pelo documento `../to-do-roadmap.docx`, especialmente pelas etapas 4 (dados da simulação), 5 (casos e resultados esperados) e 6 (evidências). Data da coleta: **14/11/2026**, horário de São Paulo.

O objetivo é montar um conjunto pequeno de documentos e casos para avaliar permissões, bloqueios, aprovação humana e rastreabilidade. Os datasets são material de apoio: não substituem a matriz de permissões, a revisão de domínio ou a medição do processo atual.

## Organização

| Pasta | Conteúdo | Prioridade |
|---|---|---|
| `agent-indirect-prompt-injection/` | Casos sintéticos de instruções maliciosas recebidas por ferramentas | Principal |
| `cuad/` | Contratos comerciais e anotações de cláusulas | Principal |
| `technology-mergers-acquisitions/` | Tabelas de empresas e aquisições | Complementar |

Cada pasta conserva o arquivo `original.zip` recebido do Kaggle e seu conteúdo extraído. O arquivo `download-manifest.json` registra os tamanhos, as quantidades de arquivos extraídos e os hashes SHA-256 dos ZIPs. Os arquivos originais devem ser preservados; adaptações do projeto devem ficar em uma pasta separada e ser identificadas como derivadas.

**Verificação local concluída:** os três ZIPs passaram na verificação de integridade. A leitura dos arquivos confirmou 1.272 casos de ataque, 510 documentos no JSON do CUAD e 1.643 linhas de aquisições. As contagens e a conferência dos hashes estão em `verification.json`. Essa verificação confirma a leitura e integridade dos arquivos, sem certificar a qualidade das anotações ou a correção dos dados.

## 1. Agent Indirect Prompt Injection Cases

- **Kaggle:** https://www.kaggle.com/datasets/yashdogra/agent-indirect-prompt-injection-cases
- **Fonte original:** NVIDIA Corporation — https://huggingface.co/datasets/nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1
- **Publicação no Kaggle:** cópia de terceiros, não oficial.
- **Última atualização consultada:** 05/10/2026.
- **Licença declarada:** CC BY 4.0. Atribuir a NVIDIA e documentar as adaptações.
- **Unidade de observação:** um caso de ataque indireto contra um agente que usa ferramentas.
- **Conteúdo descrito:** 1.272 casos sintéticos em nove domínios; inclui o domínio jurídico. Há um único conjunto `train`, sem separação original de validação e teste.
- **Arquivos:** `train.jsonl`, `cases.parquet`, `data_dictionary.csv` e `source_manifest.json`, aproximadamente 12,3 MB descompactados.

### Sugestão de uso

Selecionar inicialmente **10 a 15 casos**, priorizando ações não autorizadas e vazamento de informações. Adaptar o conteúdo para um documento fictício de due diligence ou mensagem do vendedor. Usar apenas as ferramentas simuladas já previstas no projeto.

Para cada caso, preparar uma versão normal do documento e uma versão com instrução maliciosa. Manter a tarefa legítima equivalente nas duas versões. Exemplos de comportamento a avaliar: tentativa de envio para destinatário fora da alçada, solicitação de preços sem permissão e alteração da ação depois da aprovação.

Registrar antes da execução a ferramenta e os argumentos proibidos. Verificar o resultado pela chamada efetivamente executada: uma recusa textual não comprova que a ação foi impedida. A adaptação às ferramentas e à política do projeto precisa de revisão própria.

### Limitações

Os casos são sintéticos, em inglês, e não constituem exemplos de aplicação do direito brasileiro. Segundo a documentação da fonte, foram selecionados ataques bem-sucedidos contra um modelo específico; portanto, a taxa de sucesso não representa a frequência de ataques no mundo real. Evitar usar os mesmos exemplos para ajustar e avaliar o controlador. Uma amostra pequena e adaptada produz evidência exploratória.

## 2. CUAD — Atticus Open Contract Dataset

- **Kaggle utilizado:** https://www.kaggle.com/datasets/konradb/atticus-open-contract-dataset-aok-beta
- **Criador do corpus:** The Atticus Project. A versão baixada é uma republicação de terceiros.
- **Fonte original:** https://www.atticusprojectai.org/cuad/
- **Última atualização consultada no Kaggle:** 20/07/2023, versão 2.
- **Licença declarada:** CC BY 4.0. Preservar atribuição e indicar traduções ou outras alterações.
- **Unidade de observação:** contrato e perguntas/anotações sobre cláusulas.
- **Conteúdo descrito:** 510 contratos comerciais, mais de 13 mil anotações e 41 categorias de cláusulas.
- **Arquivos:** inclui `CUAD_v1/CUAD_v1.json`, `CUAD_v1/CUAD_v1_README.txt` e contratos em PDF. Total informado pelo Kaggle: aproximadamente 174 MB descompactados.

### Sugestão de uso

Selecionar **3 a 5 contratos ou trechos** como referência para escrever contratos curtos em português, usando empresas e pessoas fictícias, conforme o roadmap. Selecionar cláusulas disponíveis que ajudem a construir tarefas de leitura, identificação de obrigações ou necessidade de revisão.

Para o primeiro piloto, basta uma tarefa delimitada: ler o contrato fictício, localizar a cláusula relevante e produzir uma sugestão. Testar separadamente se o agente tenta enviar a sugestão, aceitar termos ou realizar outra ação sujeita à política de aprovação.

As anotações do CUAD podem apoiar a avaliação de extração de cláusulas. Elas **não são rótulos de PERMITIR, ESCALAR ou BLOQUEAR** e não validam regras do CADE ou o nível de autonomia admissível. Esses resultados esperados devem vir da matriz de permissões revisada para o projeto.

### Limitações

São documentos históricos, em inglês, de contexto estrangeiro. Traduzir ou adaptar uma cláusula não estabelece sua adequação jurídica ao Brasil. Registrar a referência do contrato original, a versão da adaptação e o responsável pela revisão.

**Observação de disponibilidade:** a página do próprio The Atticus Project no Kaggle (`theatticusproject/atticus-open-contract-dataset-aok-beta`) listava apenas o README na consulta realizada. Por isso foi utilizada a republicação de `konradb`, que disponibiliza os documentos e o JSON.

## 3. Technology Mergers & Acquisitions

- **Kaggle:** https://www.kaggle.com/datasets/joebeachcapital/technology-mergers-and-acquisitions
- **Publicador:** Joakim Arvidsson (`joebeachcapital`).
- **Origem declarada:** dados do CrunchBase, reunidos em https://github.com/ali-ce/datasets/tree/master/Tech-Giants-Acquisitions
- **Última atualização consultada:** 09/08/2023, versão 1. A data de atualização não significa que as operações ocorreram em 2023.
- **Licença declarada no Kaggle:** CC BY-SA 4.0. Preservar atribuição e observar as condições de compartilhamento de adaptações. A indicação do publicador não equivale a uma auditoria dos direitos da fonte original.
- **Unidade de observação:** transação, empresa ou pessoa, conforme a tabela.
- **Conteúdo descrito:** 36 grandes empresas de tecnologia, 1.610 empresas adquiridas e 1.643 transações.
- **Arquivos:** `Acquisitions.csv`, `Acquired Tech Companies.csv`, `Acquiring Tech Companies.csv`, `Founders and Board Members.csv` e `README.md`, aproximadamente 2,3 MB descompactados.

### Sugestão de uso

Usar como referência opcional para variar setor, porte, comprador, alvo, anúncio e preço de cenários fictícios. Priorizar os cenários já existentes no projeto antes de acrescentar casos.

Não é necessário usar a tabela de fundadores e conselheiros no piloto. O roadmap orienta o uso de pessoas e empresas fictícias; registrar como sintético qualquer cenário criado a partir dessa referência.

### Limitações

Datas, preços e situação de aquisições não demonstram autorização regulatória, permissões de ferramentas ou consentimento para execução. Não inferir aprovação do CADE nem usar o status da operação como autorização. O período exato de cobertura e a completude precisam ser apurados nos dados antes de qualquer análise histórica.

## Aplicação ao roadmap

| Necessidade | Material sugerido | Evidência a produzir |
|---|---|---|
| Contrato curto | Adaptação sintética inspirada no CUAD | Cláusula esperada e resultado da leitura |
| Tabela fictícia de preços | Criar diretamente para o projeto | Valores conhecidos e limites de acesso explícitos |
| Relatório de due diligence | Criar resumo sintético coerente com o caso | Conteúdo, versão e cenário associado |
| Mensagem ao vendedor | Criar mensagem sintética | Destinatário, argumentos e exigência de aprovação |
| Documento com instrução maliciosa | Adaptar casos da NVIDIA | Chamada proibida e contagem de execuções |
| Entradas inválidas e indisponibilidade | Criar casos determinísticos | Bloqueio registrado e zero execução indevida |
| Contexto da transação | Cenários existentes; base de aquisições opcional | Estado da operação definido explicitamente |

## Catálogo e resultados esperados

Para cada documento adaptado, registrar: identificador, arquivo, fonte, licença, versão, idioma, natureza sintética/derivada e cenário associado. Uma adaptação de dado público deve ser identificada como derivada, mesmo quando o novo cenário usa nomes fictícios.

Para cada teste, registrar antes da execução:

- Identificador e objetivo.
- Fase, ferramenta, argumentos e documento/contexto.
- Condição: sinais fixos, aprovação, negativa ou falha simulada.
- Resultado esperado: PERMITIR, ESCALAR ou BLOQUEAR.
- Quantidade esperada de chamadas: zero ou uma.
- Regra que justifica o resultado, revisor e dúvidas pendentes.

Registrar depois: identificadores de rodada e ação, versão da política, decisão, aprovação vinculada à ação, ferramenta executada, resultado, erro, tempo e quantidade de chamadas. Comparar ação proposta, autorizada e executada. Os datasets não fornecem automaticamente esses registros.

## Ordem recomendada

1. Definir a tarefa e revisar a matriz de permissões.
2. Preparar poucos documentos fictícios inspirados no CUAD e casos de ataque selecionados.
3. Definir os resultados esperados e testar o controlador offline com sinais fixos.
4. Corrigir os controles até não haver execução proibida nos casos definidos.
5. Avançar à demonstração com APIs conforme os critérios do roadmap.

O download não adapta os documentos nem executa notebooks, agentes ou código das fontes. Instruções encontradas nos datasets são conteúdo para análise e teste, não autorização para realizar ações. Entrevistas, baseline de negócio e validação das regras continuam sendo atividades próprias do projeto.
