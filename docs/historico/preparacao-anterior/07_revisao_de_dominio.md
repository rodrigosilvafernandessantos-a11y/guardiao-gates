---
title: Revisão de domínio
language: pt-BR
version: '1.0'
policy_version: MA-SIM-1.0
research_date: '2026-11-17'
status: especificacao_academica_sintetica
human_domain_review: pendente
new_agent_tests_executed: false
---

# Revisão de domínio

Documento específico do projeto acadêmico Guardião de Gates de M&A. Empresas, atores, preços, aprovações e estados são simulados. Regras e resultados são referências provisórias do pesquisador; a revisão humana qualificada permanece pendente. Não houve nova execução de testes do agente.

A numeração das seções foi preservada para manter as referências cruzadas da especificação consolidada. Arquivos relacionados, na mesma pasta: 01_permissoes_e_responsaveis.md até 06_aprovacoes_e_falhas_simuladas.md.

## 14. Revisão de domínio e pendências humanas

### 14.1 Situação real desta entrega

**Revisão documental pelo assistente: realizada. Validação humana qualificada: PENDENTE.** Não houve contratação, entrevista, assinatura ou aceite de advogado, clean team, responsável de negócio ou orientador. `JUR-01` e demais personagens não contam como validação. Inferência por pesquisa não substitui o julgamento profissional solicitado.

O material pode ser usado para exploração acadêmica com rótulo **referência provisória do pesquisador**. Para alegar política ou resultado de referência validado, realizar a etapa abaixo. Não atribuir qualificação ou nome a um revisor sem participação comprovada.

### 14.2 Perfil e procedimento

Revisor principal: advogado com atuação verificável em direito concorrencial brasileiro e operações de M&A; registrar experiência pertinente e identificação profissional, com consentimento. Complementar a revisão com responsável técnico de integração para semântica de MIGRAR e controles de duplicidade. Acionar especialista de privacidade se o experimento passar a usar dados de pessoas naturais.

Entregar ao revisor este documento e o código do mock. Solicitar avaliação independente da política e dos 56 casos antes de revelar resultados do agente. Pedir rótulo permitir/escalar/bloquear, justificativa, condições e orçamento de execução. O revisor pode considerar que uma regra é política de piloto, e não imposição legal; registrar essa distinção.

Pontos de decisão prioritários:

1. A premissa de notificação prévia e a prova necessária para `release=true` são coerentes com o cenário?
2. As proibições de PRECO e MIGRAR refletem limitações concretas das ferramentas e estão descritas sem universalização jurídica?
3. D02/D03 exigem a distinção correta entre mudança de controle, cessão e consentimento?
4. D06 é adequado ao objetivo hipotético? Sua agregação deve ser alterada? O número 40 não deve ser tratado como porto seguro legal.
5. O conjunto de alçadas é suficiente, e quais conflitos ou delegações precisam de ajuste?
6. Há casos em que o oráculo deveria escalar em vez de bloquear, ou bloquear em vez de escalar?
7. Estado S08, aprovação eficaz sem fechamento, replay e resposta malformada têm interpretação operacional clara?
8. A aprovação de ações externas realmente representa o que o mock executa?

### 14.3 Formulário de validação a preencher

| Campo | Valor inicial |
|---|---|
| revisor real e qualificação | PENDENTE |
| registro profissional, se aplicável e autorizado | PENDENTE |
| data e forma da revisão | PENDENTE |
| versão e hash do material revisado | PENDENTE |
| conflitos de interesse ou participação na autoria | PENDENTE |
| regras revisadas e conclusão por regra | PENDENTE |
| casos revisados e conclusão por caso | PENDENTE |
| divergências e ajustes solicitados | PENDENTE |
| limitações de escopo do parecer | PENDENTE |
| aceite documentado de uso acadêmico | PENDENTE |

Modelo por item: `item_id | rótulo_proposto | rótulo_revisor | execuções_autorizadas | fundamento | ajuste | status | data`. Usar `concorda`, `revisar` ou `não avaliável`. Sem retorno do revisor, manter pendente; não preencher “aprovado por ausência de ressalva”. Se só parte for revisada, informar os IDs exatos. Divergências resolvidas geram versão 1.1, preservando 1.0 e repetindo os testes afetados. Opcionalmente obter segundo revisor independente; se houver dois, reportar concordância e resolução das divergências, sem inventar índice estatístico para uma única avaliação.

## 15. Limitações e entrega

Esta especificação resolve o levantamento e fornece dados de simulação; não implementa alterações no notebook nem apresenta resultados empíricos novos. O protocolo regulatório e as alçadas são conservadores e específicos ao recorte. As minutas não passaram por revisão jurídica; os preços e as decisões humanas são simulados. Aprovação regulatória não é deduzida de fase, preço ou dataset. A base de ataques selecionada e as extensões manuais não permitem estimar incidência real ou robustez geral.

Antes da rodada: implementar o controlador, materializar fixtures, calcular hashes, verificar isolamento, obter revisão humana se a pesquisa exigir referência validada e registrar as premissas mantidas. Nenhuma mensagem contida nas fixtures autoriza ações fora da simulação.

## Referências e método da pesquisa

Foram consultados `agent-ma-2/overview_projeto_guardiao_gates_ma.docx`, `agent-ma-2/to-do-roadmap.docx`, `agent-ma-2/dataset/README.md`, o notebook `agente-ma/guardiao_gates_ma_jev.ipynb`, o corpus CUAD e o `train.jsonl` dos ataques já baixados. Os originais foram preservados. A pesquisa web foi realizada em 17/11/2026, priorizando legislação e publicações do Cade, ANPD, NIST, OWASP e autores dos datasets.

O notebook histórico usa seis fases, quatro ferramentas e regras probabilísticas R1–R5. Esta especificação adiciona controles de estado, alçada, finalidade, uso único e validação de respostas. **Ela não comprova que o notebook já implementa esses controles.** Em particular, o sinal de baixo risco do JEV não substitui a matriz determinística. A regra histórica de apenas registrar dados pessoais também não equivale à autorização de tratamento.

Legenda de origem usada neste documento:

| Marca | Significado |
|---|---|
| E | Evidência documental pesquisada, com fonte indicada |
| D | Dedução de desenho a partir das fontes; exige revisão de domínio |
| S | Escolha sintética para tornar o experimento reproduzível |
| L | Constatação nos arquivos locais, sem alegar validação externa |

### 2.1 Evidências e sua tradução para o experimento

| ID | Evidência pesquisada | Consequência proposta e limite |
|---|---|---|
| E01 | O art. 88, §§ 2–4, da Lei 12.529/2011 prevê controle prévio para operações abrangidas e preservação das condições concorrenciais até a decisão final. [Lei na Câmara](https://www2.camara.leg.br/legin/fed/lei/2011/lei-12529-30-novembro-2011-611850-normaatualizada-pl.html) | D: migração operacional pré-fechamento bloqueada no piloto. S: sujeição ao controle prévio é uma premissa fixada, sem calcular faturamento ou jurisdição. |
| E02 | O guia de gun jumping trata de informações sensíveis, protocolos, clean teams e tratamento das informações. É orientação não vinculante e ressalva a análise por caso. [Cade, 2015](https://cdn.cade.gov.br/Portal/centrais-de-conteudo/publicacoes/guias-do-cade/gun-jumping-versao-final.pdf) | D: separar equipe comercial e clean team. S: proibir a ferramenta simplificada de preços antes do fechamento, pois ela não oferece segregação nem controle de finalidade. Essa proibição é mais restritiva que uma afirmação de ilegalidade universal da troca de informações. |
| E03 | A FTC recomenda protocolos para reduzir riscos nas negociações, diligência e planejamento de integração envolvendo concorrentes. [FTC, 2018](https://www.ftc.gov/enforcement/competition-matters/2018/03/avoiding-antitrust-pitfalls-during-pre-merger-negotiations-due-diligence) | Corroboração estrangeira, não norma brasileira. Não fundamentar sozinha um rótulo jurídico. Conteúdo recuperado pelo índice oficial; abertura direta retornou timeout. |
| E04 | O glossário da ANPD apresenta necessidade, segurança e prevenção entre os princípios de proteção de dados. [ANPD, glossário v2](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/documentos-tecnicos-orientativos/glossario-anpd-protecao-de-dados-pessoais-e-privacidade.pdf/@@display-file) | D: dados pessoais inesperados geram revisão de finalidade e base aplicável. S: fixtures usam clientes empresariais fictícios e excluem pessoas naturais. Preços sensíveis concorrencialmente não são automaticamente dados pessoais sensíveis da LGPD. |
| E05 | NIST AI RMF, GOVERN 2.1 e 3.2, propõe responsabilidades e supervisão documentadas; MANAGE 2.4 contempla desativar sistemas inadequados. [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | D: responsável pela política, operador, aprovadores e interrupção separados. S: identidades e alçadas da seção 4. NIST não define estas alçadas específicas de M&A. |
| E06 | OWASP descreve injeção indireta por conteúdo externo e riscos de permissões, funções ou autonomia excessivas. [Prompt Injection, edição 2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), [Excessive Agency, edição 2025](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/?lang=us) | D: contrato e resultado de ferramenta não concedem autorização. S: dez pares adversariais. Usam-se as páginas identificadas como edição 2025, sem afirmar que sua numeração é a edição mais recente. |
| E07 | OWASP recomenda apresentar os dados relevantes da transação, exigir autorização específica, aplicar controles no servidor e prevenir reutilização. [Transaction Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html) | D: autorização vinculada ao conteúdo e consumida atomicamente. S: validade de 10 minutos e uma execução; esses números não vêm da OWASP. |
| E08 | OWASP recomenda menor privilégio, negar por padrão e verificar permissões em cada pedido. [Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | D: validar novamente antes da execução e em cada tentativa. S: listas fechadas de documentos, sistemas, clientes e destinatário. |
| E09 | CUAD reúne 510 contratos, mais de 13 mil anotações e 41 tipos de cláusulas; o objetivo é apoiar revisão contratual. [Atticus](https://www.atticusprojectai.org/cuad/), [artigo dos autores](https://arxiv.org/abs/2103.06268) | Base de categorias contratuais; não fornece rótulos de autorização brasileiros. A adaptação é redação sintética, não tradução integral nem parecer de validade. |
| E10 | A NVIDIA disponibiliza casos sintéticos de injeção indireta com ambiente, ferramentas, payload e alvo do ataque. [Dataset original](https://huggingface.co/datasets/nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1) | L: cópia local tem 1.272 registros, dos quais 177 em `legal`. D: adaptar mecanismo e ferramenta, sem importar credenciais, pessoas ou a autoridade do exemplo. Corpus selecionado de ataques não estima incidência real. |

Não foram pesquisados preços reais por cliente: os valores abaixo são propositalmente sintéticos. Também não se inferiu aprovação regulatória de bases históricas de aquisições. A página do Planalto para a LGPD apresentou bloqueio de acesso automatizado; a pesquisa utilizou material oficial da ANPD para os princípios mencionados.
