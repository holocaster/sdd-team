# sdd-team

Workflow portátil de desenvolvimento guiado por especificações (SDD), com discovery interativo e agentes isolados para planejamento, implementação e revisão. O filesystem e o Git guardam o estado; cada agente começa com contexto fresco.

## Pré-requisitos

- Git, árvore limpa e um branch de feature no projeto alvo.
- Um CLI com skills e agentes isolados: Claude Code, Codex ou opencode.
- Bash para executar o bootstrap atual.
- Gitleaks para a varredura obrigatória de credenciais; checks essenciais indisponíveis ou incompletos bloqueiam a revisão.
- Skills externas `grilling`, `domain-modeling` e `tdd`, com suas dependências e referências, disponíveis no CLI escolhido.
- Node.js e npm se usar a instalação de skills via `npx`.

## Instalação

### Skills

Clone o repositório e instale as skills:

```bash
git clone https://github.com/holocaster/sdd-team.git
cd sdd-team
npx skills add . --skill '*' --agent claude-code codex opencode --global
```

Quando as mudanças estiverem disponíveis no GitHub, o mesmo catálogo pode ser instalado com `npx skills add holocaster/sdd-team`. Selecione apenas os CLIs desejados com `--agent`; omita `--global` para instalar no projeto alvo.

As dependências externas vêm de [mattpocock/skills](https://github.com/mattpocock/skills). Elas não estão incluídas neste repositório. Instale `grilling`, `domain-modeling` e `tdd`, incluindo as referências e dependências usadas por elas, como `codebase-design`.

### Agentes

A instalação de skills não registra os agentes. Registre também `sdd-planner`, `sdd-implementer` e `sdd-reviewer` no CLI escolhido:

| CLI | Fonte dos perfis | Registro |
|---|---|---|
| Claude Code | `.claude/agents/sdd-*.md` | `.claude/agents/` no projeto ou `~/.claude/agents/` global |
| opencode | `.opencode/agents/sdd-*.md` | `.opencode/agents/` no projeto ou `~/.config/opencode/agents/` global |
| Codex | `.claude/agents/sdd-*.md` como contrato canônico | Configuração dos papéis no Codex, com instruções para ler os perfis no caminho instalado |

Use cópias ou symlinks para os perfis Markdown. A configuração de papéis do Codex precisa ser criada separadamente; este repositório ainda não fornece um instalador automatizado de agentes. Preserve os nomes, os contratos e a revisão independente.

### Inicialização do projeto alvo

Depois de instalar skills e agentes, execute o `bootstrap.sh` incluído em `sdd-main`, na raiz do projeto alvo, uma vez:

```bash
bash ~/.claude/skills/sdd-main/bootstrap.sh
# ou, para uma instalação global no Codex
bash ~/.codex/skills/sdd-main/bootstrap.sh
```

Para outros caminhos de instalação, use o `bootstrap.sh` da skill instalada. Ele cria apenas `.ai/PROJECT_STATE.md`, `docs/`, `tickets/` e um stub de `docs/CONTEXT.md`, preservando as configurações de permissões existentes. Permissões são configuradas separadamente no CLI escolhido.

## Papéis e skills

| Papel | Responsabilidade | Skills deste repositório |
|---|---|---|
| Main | Único contato com o usuário; discovery, estado e encaminhamento | `sdd-main`, `sdd-grill-with-docs` no discovery |
| Planner | Formaliza o brief em spec, tickets e ADRs | `sdd-to-spec`, `sdd-to-tickets`; `sdd-codebase-design` quando necessário |
| Implementer | Implementa um ticket ou Batch e commita código e testes | `sdd-implement`, com a skill externa `tdd` |
| Reviewer | Revisa independentemente o range exato do ticket ou Batch | `sdd-security-review` em BRANCH, `sdd-code-review`; `sdd-diagnosing-bugs` quando necessário |

Planner, Implementer e Reviewer rodam em sessões novas, sem herdar a conversa do Main, e recebem objetivos, referências e restrições necessárias. Não falam com o usuário. Uma skill ou agente necessário ausente é um bloqueio, não autorização para simular o papel.

## Fluxo

1. **Dimensionamento:** Main escolhe o caminho rápido para um único slice vertical, sem ambiguidade nem nova decisão transversal. Escreve um ticket com critérios autossuficientes e segue para implementação, sem brief ou Planner.
2. **Discovery, no caminho completo:** Main resolve as questões com o usuário, mantém glossário e decisões atuais em `docs/CONTEXT.md` e escreve `docs/briefs/<NNNN-slug>.md`.
3. **Planejamento:** Planner produz a spec, os tickets e ADRs. Questões de produto ou escopo voltam ao usuário pelo Main.
4. **Implementação serial:** Implementer trabalha um ticket ou Batch elegível. Uma cadeia linear vira Batch quando os critérios combinados cabem em uma sessão e nenhum membro exige revisão isolada. Reporta `base_sha` na primeira rodada e `head_sha` ao terminar; `base_sha` é imutável nas correções.
5. **Revisão:** Main confirma a entrega concluída e commitada e a árvore limpa antes de delegar. Reviewer usa exatamente `base_sha..head_sha`. Executa segurança em BRANCH primeiro, incluindo credenciais dos commits intermediários, testes e documentação. Standards + Spec reutiliza o contexto sanitizado. Regressões comprovadamente introduzidas, vazamentos confirmados e vulnerabilidades aceitas no range impedem aprovação, mesmo sem critério explícito.
6. **Correção ou conclusão:** Main persiste a revisão. Em `changes_requested`, reenvia o mesmo ticket ou Batch com a base original e os findings. Em `approved`, marca todos os tickets do run como `done` e seus critérios como `[x]`. Ao terceiro `changes_requested` sem aprovação, escala ao usuário.

Antes de delegar, Main confirma a autorização para os commits necessários e a capacidade de escrita na árvore e nos metadados Git, concluindo os checkpoints pendentes. Autorizações existentes são reutilizadas. Cada autor commita seus artefatos antes do handoff, mantendo a árvore limpa. Main persiste estado e revisões; Planner commita spec, tickets e ADRs; Implementer commita código e testes; Reviewer não commita. O Main continua até concluir os tickets e só interrompe por questões ou bloqueios definidos em `sdd-main`.

Na retomada, commits de estado do Main preservam o `head_sha` da implementação e uma revisão ainda válida. Trabalho local de origem incerta é preservado e reportado ao usuário; a limpeza de agentes se limita aos próprios artefatos identificados.

`FULL HISTORY` é uma auditoria separada de credenciais, somente por pedido explícito ao Main. Não roda no loop de tickets. Os contratos detalhados, rotas e regras de cold resume estão na [skill `sdd-main`](.claude/skills/sdd-main/SKILL.md).

## Artefatos no projeto alvo

```text
.ai/PROJECT_STATE.md          estado mínimo e ponteiros para os artefatos
docs/CONTEXT.md               glossário e decisões atuais do projeto
docs/briefs/<NNNN-slug>.md    brief da feature, no caminho completo
docs/specs/<NNNN-slug>.md     spec da feature, no caminho completo
docs/adrs/                   decisões arquiteturais, com numeração própria
tickets/<NNNN-slug>/         index.md, tickets e registros *.review.md
```

O id `NNNN-slug` identifica a mesma feature no brief, na spec e nos tickets. `index.md` é a fonte de status dos tickets; `PROJECT_STATE.md` mantém apenas o ponto de retomada. Este repositório distribui o workflow e não mantém esses artefatos para si.

## Desenvolvimento e referências

Os perfis `.claude/agents/` e as skills `.claude/skills/` são canônicos. Depois de alterar um perfil, regenere a cópia opencode:

```bash
.opencode/sync-agents.sh
```

Contribuidores podem usar symlinks para consumir este checkout; nesse caso, mudanças têm efeito imediato nos projetos ligados. Instalações por cópia precisam ser atualizadas.

Execute os checks dos scripts com Python 3, Bash e Git:

```bash
python3 -B -m unittest discover -s tests -v
```

A suíte verifica bootstrap, preservação de arquivos e sincronização dos perfis; o CI executa o mesmo comando em pushes e pull requests. Os [cenários manuais do workflow](docs/WORKFLOW-CHECKS.md) cobrem preservação de trabalho local, retomada e escopo de regressões.

Consulte [AGENTS.md](AGENTS.md) para manutenção e [SYNC.md](.claude/skills/SYNC.md) para a origem e as diferenças dos forks de Matt Pocock. A [revisão upstream de 2026-10-02](docs/archive/upstream-skills-review-2026-10-02.md) é pesquisa histórica, não instrução de instalação.

### Ponytail, opcional

Ponytail é um plugin externo, não uma dependência do SDD nem parte desta distribuição. Para usá-lo, instale o plugin e configure seus hooks no harness escolhido. Na integração Claude Code por hooks, o escopo recomendado é `PONYTAIL_SUBAGENT_MATCHER=implementer`, mantendo Planner e Reviewer independentes dessa política. Quando o hook já injeta as instruções, uma invocação adicional da skill é desnecessária.

## Contribuição e segurança

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) para desenvolver e enviar pull requests.
Relate vulnerabilidades conforme [SECURITY.md](SECURITY.md).

## Licença

[MIT](LICENSE). Materiais adaptados preservam os avisos em
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
