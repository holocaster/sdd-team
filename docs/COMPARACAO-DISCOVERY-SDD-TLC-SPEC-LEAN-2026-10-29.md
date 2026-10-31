# Discovery do SDD versus tlc-spec-lean

Análise: 29/10/2026. Interpretei `tcl-spec-lean` como `tlc-spec-lean`.

**Recomendação: incorporar a técnica de descoberta do PLAN ao SDD, preservando `domain-modeling` e o Planner. Não substituir `sdd-grill-with-docs` pela skill TLC inteira.** O PLAN combina discovery e desenho da solução; a TLC inteira também substitui tickets, implementação, revisão e estado. São mudanças de alcance diferente. [SDD:64–79](../.claude/skills/sdd-main/SKILL.md), TLC:173–198 (`tlc-spec-lean/SKILL.md`).

## Escopo e fontes

Comparei as fontes canônicas deste repositório no commit `d8154358f2d6a3fc2d91a05d3641cede6563fccf` com a instalação local da TLC, declarada como **1.0.0**. Li `SKILL.md`, as cinco referências PLAN/CHECKS/BUILD/VERIFY/MEMORY, os validadores e os exemplos. O SHA-256 de `tlc-spec-lean/SKILL.md` nesta coleta é `56db00c3b8c5e76c41f05aeddf1ba1c21be420f4afee48a5695c693a7391a50f`. A versão declarada não identifica, sozinha, alterações posteriores nas referências. Metadados TLC:1–12 (`tlc-spec-lean/SKILL.md`).

Esta é uma análise estática de contratos, não uma execução dos workflows ou benchmark. Não alterei skills, perfis nem configuração. Os links do repositório são relativos. As fontes externas são identificadas por skill e arquivo, sem caminhos pessoais; a instalação analisada não acompanha este relatório. Os números indicados nas referências identificam as linhas consultadas.

## Três mudanças possíveis

| Opção | O que muda | Avaliação |
|---|---|---|
| Usar a elicitação do PLAN no discovery | Perguntas, levantamento de superfícies, requisitos implícitos e registro de hipóteses; saída continua sendo brief + CONTEXT | Melhor primeira experiência; precisa de um adaptador de escopo e artefatos |
| Usar o PLAN completo como substituto | Main também produz critérios e desenho técnico em `plan.md`, antes de continuar no SDD | Sobrepõe responsabilidades e documentos do Planner |
| Adotar TLC inteira | PLAN → CHECKS → BUILD → VERIFY, com obrigações em lugar da decomposição em tickets | É uma alternativa ao workflow, não uma troca de discovery |

Essa separação decorre do contrato do Main, que escreve um brief curto e não escreve specs/ADRs no caminho completo, e do PLAN, que já inclui fluxo, entidades, interface e decisões difíceis de reverter. [SDD:29–38 e 151–154](../.claude/skills/sdd-main/SKILL.md), PLAN:198–305 (`tlc-spec-lean/references/plan.md`).

## Como o discovery funciona hoje

O nome exato no SDD é **`sdd-grill-with-docs`**, um adaptador que chama `grilling` e depois `domain-modeling`. Ele direciona glossário e decisões atuais para `docs/CONTEXT.md`; propostas de ADR ficam no brief, e o Planner escreve os ADRs depois. Main estabiliza e commita brief + CONTEXT antes do handoff. [Adaptador:6–10](../.claude/skills/sdd-grill-with-docs/SKILL.md), [SDD:64–79](../.claude/skills/sdd-main/SKILL.md).

A versão instalada de `grilling` percorre uma árvore de decisões: pergunta toda a fronteira cujos pré-requisitos já foram resolvidos, recomenda respostas e espera a rodada seguinte. Fatos são investigados pelo agente; decisões pertencem ao usuário. Termina quando não há decisões silenciosamente assumidas e o usuário confirma o entendimento. Grilling:6–30 (`grilling/SKILL.md`).

`domain-modeling` acrescenta uma disciplina própria: confronta termos com o glossário, explora cenários de domínio e divergências entre fala e código, registra termos imediatamente e reserva ADRs para decisões relevantes com alternativas reais. Isso vai além de fazer perguntas até esclarecer o escopo. Domain modeling:8 e 46–74 (`domain-modeling/SKILL.md`).

## Diferenças no discovery

| Aspecto | SDD atual | PLAN da TLC |
|---|---|---|
| Forma das perguntas | Árvore de decisões; toda a fronteira independente por rodada | Opções concretas com recomendação; até duas perguntas independentes, uma se dependentes |
| Incerteza | Decisões com o usuário; nenhuma hipótese silenciosa ao encerrar | Defaults seguros podem seguir registrados; `Confirmed? y/n` distingue confirmação de escolha do agente |
| Busca de lacunas | Entrevista orientada pela árvore e cenários de domínio | Enumeração fixa das superfícies e nove dimensões, com `n/a` justificado |
| Critérios | Discovery entrega brief; Planner formaliza spec e tickets | Critérios EARS mensuráveis e IDs de requisito já no PLAN |
| Domínio | Glossário durável compartilhado em CONTEXT + decisões/ADRs | `Impact` registra termos novos, mudanças de significado e consumidores afetados; `Relations` registra entidades e cardinalidade |
| Arquitetura | Planner decide interfaces, pontos de teste e implementação | PLAN apresenta Flow, Relations, Surface e Landing; alternativas arquiteturais ainda abertas precisam ser resolvidas antes |
| Fechamento | Entendimento confirmado e brief estável antes do Planner | Validação do plano e revisão humana antes de escrever checks |

Fontes da tabela: Grilling:6–30 (`grilling/SKILL.md`), [SDD:64–81](../.claude/skills/sdd-main/SKILL.md), [Spec:10–16 e 40–62](../.claude/skills/sdd-to-spec/SKILL.md), PLAN:31–98 (`tlc-spec-lean/references/plan.md`), PLAN:100–196 (`tlc-spec-lean/references/plan.md`), PLAN:239–305 (`tlc-spec-lean/references/plan.md`), PLAN:494–505 (`tlc-spec-lean/references/plan.md`).

O ganho mais concreto de estrutura está nas **enumerações**. Uma API obriga a percorrer formato de resposta/erro, autorização, versionamento e rate limit. Uma tela exige estados vazio/loading/erro/não autorizado, organização e confirmação destrutiva. Cada item precisa virar critério, comportamento existente ou `n/a` com motivo. Não é uma autorização para acrescentar capacidades. PLAN:100–127 (`tlc-spec-lean/references/plan.md`).

As nove dimensões cobrem validação, falha parcial, idempotência, autorização, concorrência, ciclo de dados, dependências externas, transições de estado e observabilidade. São percorridas no PLAN, mas seu registro final, `Swept`, fica em CHECKS porque referencia números de checks. **Importar apenas discovery exige adaptar esse registro**; o PLAN isolado não entrega o mecanismo completo. PLAN:165–196 (`tlc-spec-lean/references/plan.md`).

EARS distingue invariantes, eventos, estados, capacidades opcionais e falhas, com um requisito e resultado concreto por critério. Por exemplo, “tratar timeout corretamente” precisa virar um comportamento observável; a TLC separa metas estatísticas de serviço de critérios decidíveis numa execução. Isso melhora a forma de especificar, mas não garante que o requisito escolhido esteja correto. PLAN:129–163 (`tlc-spec-lean/references/plan.md`).

Há dois custos possíveis. Limitar perguntas por turno pode diminuir a carga de cada resposta e aumentar o número de rodadas quando a fronteira é grande. E completar o desenho técnico durante discovery pode aumentar o trabalho do Main e duplicar a exploração posterior do Planner. São inferências do desenho, não resultados medidos. Grilling:8–28 (`grilling/SKILL.md`), PLAN:79–98 (`tlc-spec-lean/references/plan.md`), [Planner:29–33](../.claude/agents/sdd-planner.md).

## O que pertence à TLC inteira, não ao discovery

### Obrigações e evidência

Depois da confirmação do PLAN, CHECKS deriva afirmações observáveis com valor concreto e comando de prova específico. `Coverage` associa cada membro de conjuntos enumerados a checks; `Swept` mostra onde cada dimensão foi atendida. Cada status de uma rota, entidade e decisão difícil de reverter deve ter correspondência. CHECKS fica completo antes do código; por padrão não exige uma segunda parada de aprovação, salvo conflitos, expansão de escopo ou bloqueios definidos. CHECKS:11–50 (`tlc-spec-lean/references/checks.md`), CHECKS:58–88 (`tlc-spec-lean/references/checks.md`), CHECKS:228–253 (`tlc-spec-lean/references/checks.md`).

O SDD já tem rastreabilidade de requisitos para tickets, testes de comportamento, evidência no handoff e revisão independente de critérios. A diferença é a TLC tornar explícita a cadeia **critério → check → seletor de teste → asserção localizada**, incluindo membros de conjuntos. Não seria correto dizer que ela introduz revisão ou testes que o SDD não possui. [Planner:29–35](../.claude/agents/sdd-planner.md), [Spec:56–62](../.claude/skills/sdd-to-spec/SKILL.md), [Implementer:69–78](../.claude/agents/sdd-implementer.md), VERIFY:95–178 (`tlc-spec-lean/references/verify.md`).

Os perfis mudam a garantia pretendida:

| Perfil TLC | Trabalho do Verifier | Limite relevante |
|---|---|---|
| `light`, padrão | Roda provas no HEAD, confirma testes executados, localiza asserções, avalia nível/amostragem e relê `Swept existing` | Não recompõe Coverage nem injeta falhas |
| `standard` | Acrescenta recomposição independente de Coverage, julgamento de Test policy e injeção de falhas por superfície de asserção | Não faz a comparação de fontes vinculantes prevista no perfil `ui` |
| `ui` | Acrescenta comparação de fontes vinculantes e enumeração de conteúdo/composição por tela | Espaçamento, cor e peso tipográfico podem ficar explicitamente fora, enumerados por tela |

Fontes: TLC:69–112 (`tlc-spec-lean/SKILL.md`), VERIFY:35–93 (`tlc-spec-lean/references/verify.md`). A injeção ocorre em worktree temporária, com teto de cinco falhas e verificação de preservação da árvore real; é evidência amostrada, não prova exaustiva de correção. VERIFY:180–204 (`tlc-spec-lean/references/verify.md`).

Os scripts são guardas estruturais úteis, **não executores das provas nem confirmação automática de completude semântica**. `validate_checks.py` declara que lê o Markdown, e a qualidade da prova continua sendo julgamento. O gate final procura evidência `file:line` global e contradições nas tabelas; não comprova por si só a identidade do Verifier ou a execução dos testes. Há ainda uma diferença entre a descrição geral e o código: `self-verified` gera warning, que só reprova com `--strict`. CHECKS:234–241 (`tlc-spec-lean/references/checks.md`), Validador:15–16, 186–196 e 351–353 (`tlc-spec-lean/scripts/validate_verification.py`).

### Execução e governança

| Aspecto | SDD atual | TLC inteira |
|---|---|---|
| Artefatos | CONTEXT, brief, spec, ADRs, tickets e PROJECT_STATE | plan, checks, verification e STATE; reutiliza o registro de decisões existente |
| Unidade de execução | Ticket vertical ou Batch elegível; cadeia linear vira Batch por padrão | Checks agrupados em slices, sem decomposição em tarefas |
| Builders | Implementer isolado por ticket/Batch; execução serial | Um builder, salvo orçamento de leitura; divisão em slices completos e sequenciais |
| Revisão | Reviewer independente por ticket/Batch, base imutável e head explícito em `base_sha..head_sha` | Verifier independente ao terminar a feature, `<feature base>..HEAD`, com todos os checks |
| Desenho durante build | Implementer não muda requisitos/ADRs; contradição relevante volta ao Planner | Checks/provas fixos; Landing/Relations/Surface aditivos; Flow/Impact mantidos atuais; porta nova sem conflito pode ser decidida pelo builder |
| Segurança | BRANCH obrigatório antes de Standards + Spec, incluindo credenciais e regressões introduzidas | As referências analisadas não definem varredura equivalente obrigatória; verificar checks não a substitui |
| Papel indisponível | Bloqueia; não simula o papel | Prevê alternativa declarada de self-verification em nova sessão quando não existe mecanismo de subagente |
| Modelo sugerido | Maior capacidade em Planner/Reviewer, menor em Implementer | Alta capacidade em domínio central e escrita dos checks, rápida no mecânico, média/alta no Verifier |

Fontes: [SDD:19, 25–38, 85–111 e 178–180](../.claude/skills/sdd-main/SKILL.md), [Implementer:43–51](../.claude/agents/sdd-implementer.md), [Reviewer:25–41 e 62–66](../.claude/agents/sdd-reviewer.md), TLC:114–129 e 238–258 (`tlc-spec-lean/SKILL.md`), BUILD:9–68 (`tlc-spec-lean/references/build.md`), VERIFY:9–33 (`tlc-spec-lean/references/verify.md`).

O SDD já reduz etapas por fast path e Batch; não pressupõe um agente por arquivo. Seu fast path depende de um slice sem questão aberta ou nova decisão transversal. O escape TLC depende de aproximadamente menos de três arquivos sem porta irreversível e usa somente CHECKS com Intent. Uma contagem menor de documentos não equivale automaticamente a menor custo ou melhor adequação. [SDD:55–62 e 85–89](../.claude/skills/sdd-main/SKILL.md), TLC:127–129 (`tlc-spec-lean/SKILL.md`).

### Git, memória e retomada

O SDD exige artefatos commitados antes de cada handoff, valida a prontidão do range e persiste base, head, revisão e contador de rodadas. Sua retomada distingue commits de implementação e bookkeeping, preserva trabalho incerto e reaproveita uma revisão válida do range exato. [SDD:19–27, 97–105 e 123–136](../.claude/skills/sdd-main/SKILL.md).

A TLC também usa commits e evidência Git: fecha checks no mesmo commit, passa artefatos + diff ao builder seguinte, recupera-se de compaction e reconcilia STATE com branch/status/log/checks. Entretanto, as referências não detalham o mesmo protocolo de base/head por ticket e recuperação da revisão. Em troca, mantêm estado por checks e uma camada de lições originadas em falhas reais de verificação. BUILD:89–91 e 124–152 (`tlc-spec-lean/references/build.md`), MEMORY:55–80 (`tlc-spec-lean/references/memory.md`).

Não é preciso abrir um segundo registro de decisões: MEMORY manda reutilizar ADRs/log existentes. Também seria incorreto dizer que a TLC ignora domínio: `Impact` trata termos e consumidores. O que não aparece ali é o contrato específico do SDD de um glossário compartilhado em CONTEXT atualizado por `domain-modeling`. MEMORY:36–38 (`tlc-spec-lean/references/memory.md`), PLAN:293–305 (`tlc-spec-lean/references/plan.md`), [SDD:31](../.claude/skills/sdd-main/SKILL.md).

A autorização padrão de commits locais descrita pela TLC não supera instruções do usuário ou do projeto. TLC:66–67 (`tlc-spec-lean/SKILL.md`).

## Adaptação mínima recomendada

Esta é uma proposta, não uma mudança já realizada:

1. **Preservar a divisão de papéis.** Main usa a elicitação do PLAN para esclarecer problema, escopo, superfícies e dimensões. Sua saída continua sendo o brief curto; não cria `.specs/`, spec técnica ou tickets no caminho completo. Planner continua dono de spec, ADRs e tickets. [Limites atuais:151–154](../.claude/skills/sdd-main/SKILL.md).
2. **Manter `domain-modeling`.** Termos confirmados e decisões atuais entram em CONTEXT; propostas de ADR seguem no brief. Reaproveitar `Impact` como pergunta sobre termos/callers afetados, sem outro glossário. [Contrato atual:6–10](../.claude/skills/sdd-grill-with-docs/SKILL.md).
3. **Registrar lacunas sem duplicação.** No brief, guardar apenas requisitos descobertos, exclusões, hipóteses e pendências; usar as enumerações como roteiro. Se houver exigência de matriz auditável das nove dimensões, escolher um dono e um destino canônicos antes de adicioná-la. Não chamar esse recorte de PLAN TLC completo validado.
4. **Definir a fronteira de autonomia.** Defaults técnicos reversíveis e questões delegadas podem ser registrados. Questões materiais de produto/escopo continuam sendo resolvidas com o usuário; `Confirmed? n` não pode virar consentimento implícito. [SDD:69–73](../.claude/skills/sdd-main/SKILL.md), PLAN:86–98 (`tlc-spec-lean/references/plan.md`).
5. **Tratar provas como uma segunda experiência.** Se o objetivo for combater critérios esquecidos e testes fracos, adaptar CHECKS/Coverage/Swept para spec/tickets e Reviewer, preservando segurança BRANCH, TDD, range exato e handoffs commitados. Isso precisa de desenho próprio: não vem automaticamente da troca de entrevista.

O PLAN completo também seria viável com uma mudança maior de responsabilidades: Main elicita requisitos, Planner prepara o desenho e Main traz decisões materiais ao usuário. Porém isso exige definir quem aprova qual artefato e impedir uma spec paralela concorrente. Não é uma substituição textual de uma chamada de skill. [Planner:39–55](../.claude/agents/sdd-planner.md), PLAN:494–505 (`tlc-spec-lean/references/plan.md`).

## Como avaliar sem presumir ganhos

Uma comparação entre os workflows precisa de tarefas equivalentes e critérios definidos previamente. Mudanças no discovery devem ser avaliadas separadamente das mudanças de implementação e revisão.

Uma avaliação controlada pode comparar:

| Variante | Contrato mantido | Pergunta respondida |
|---|---|---|
| A: SDD atual | Fast path, Batch e revisões atuais | Referência |
| B: SDD + elicitação PLAN | Mesmos papéis, caminhos e revisão de A | O roteiro encontra mais lacunas com carga aceitável ao usuário? |
| C: B + provas/Coverage e verificação adaptadas | Mesmo escopo, segurança e autorização; perfil declarado | O mecanismo de obrigações reduz omissões e correções incompletas? |

Usar tarefas equivalentes: uma mudança pequena, uma feature ambígua, uma com múltiplos slices/contrato e uma mudança de domínio com dados existentes, por exemplo reservas e cancelamentos. Em A/B, manter idênticos Planner, Implementer, Reviewer, modelos, versões, base do repositório e ambiente; variar apenas a elicitação e repetir execuções. Testar TLC inteira separadamente seria uma quarta comparação de workflows, sem atribuir seus resultados apenas ao discovery.

Usar dados sintéticos e cobrir **caso original, variantes próximas e controles válidos**. Avaliar também retomada após interrupção e bloqueio antes do dispatch quando commits não forem possíveis. [Regra de irmãos do defeito:49](../.claude/agents/sdd-implementer.md).

Medir por feature entregue: omissões/ambiguidades do brief, questões materiais descobertas antes/depois do planejamento, requisitos inventados, rodadas e esforço do usuário, critérios sem prova, defeitos detectados/escapados, correções por classe de falha, interrupções, agentes reabertos, tempo e uso com cache separado. Comparar custos somente com cobrança/preços e tarefas equivalentes; registrar perfil de verificação e trabalho efetivamente executado. Uma aprovação textual ou um gate estrutural verde não é o desfecho de qualidade do experimento. Gate estrutural TLC:15–16 (`tlc-spec-lean/scripts/validate_verification.py`).

**Decisão sugerida:** experimentar B primeiro. Ela ataca a organização do discovery com menor alteração contratual. Se o problema prioritário for retrabalho de implementação/revisão, avaliar C em separado; adotar a TLC inteira só faz sentido como decisão consciente de substituir o workflow e manter explicitamente as garantias do SDD que o projeto ainda exige.
