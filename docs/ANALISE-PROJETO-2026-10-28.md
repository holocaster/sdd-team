# Análise do projeto sdd-team

Data: 2026-10-28. Referência analisada: commit `1aaa265`.

Este relatório preserva o diagnóstico do commit de referência; as linhas citadas
nas evidências correspondem àquela versão. A tabela e o registro de correções
abaixo indicam o estado após as correções de 2026-10-29.
A reverificação dos itens 4, 5 e 6 nessa data usou o commit `3aac7e0`, antes
das correções adicionais dos itens 4, 5 e 6 registradas abaixo.
A verificação final partiu de `432951e` e inclui a correção do template descrita
no item 6 do registro de correções.

O cenário considerado é o documentado pelo projeto: um Main coordenando agentes
isolados, com implementação serial em uma única árvore Git. A análise abrangeu
README, instruções do repositório, perfis canônicos e gerados, skills, scripts
e o handoff de instalação.

A estrutura de papéis, revisão independente, ranges explícitos e artefatos
versionados é uma boa base. Os pontos abaixo concentram os riscos encontrados.

| Item | Prioridade sugerida | Natureza da evidência | Status em 2026-10-29 |
|---|---|---|---|
| 1. Limpeza pode apagar trabalho local | Alta | Efeito dos comandos reproduzido em repositório temporário | Corrigido nas instruções |
| 2. Retomada confunde implementação e estado | Alta | Contradição entre as regras documentadas | Corrigido nas instruções |
| 3. Escopo pode excluir regressões introduzidas | Alta | Ambiguidade do contrato de revisão | Corrigido nas instruções |
| 4. Bootstrap cria regra ampla de shell sem escolha própria | Alta antes de distribuição pública | Comportamento reproduzido e coberto por teste de regressão | Corrigido: bootstrap apenas de artefatos |
| 5. Ausência de checks automatizados versionados | Média | Suíte executável em fixtures temporárias e CI aprovado | Checks dos scripts implementados; avaliação completa do workflow com agentes pendente |
| 6. Template incentiva especificações extensas | Baixa | Exigência textual removida; síntese de specs avaliada em dois casos | Corrigido nas instruções; sem medição comparativa de custo ou tempo |

## Correções realizadas em 2026-10-29

Implementadas pelo Codex após autorização do usuário:

1. **Preservação de trabalho local:** removidas as receitas de limpeza global do
   [Main](../.claude/skills/sdd-main/SKILL.md) e do
   [Reviewer](../.claude/agents/sdd-reviewer.md). Reviewer e
   [Implementer](../.claude/agents/sdd-implementer.md) limpam somente alterações
   próprias identificadas, por caminhos explícitos. Trabalho staged, preexistente
   ou de origem incerta é preservado e reportado; nenhuma nova delegação ocorre
   com a árvore suja.
2. **Retomada:** Main distingue commits de implementação de commits de estado,
   preserva `base_sha`, mantém `head_sha` no último commit verificado do
   Implementer e reutiliza revisões cujo ticket e range ainda correspondam.
   Uma nova implementação invalida a revisão anterior sem zerar `review_round`;
   encaminhar uma revisão persistida não incrementa novamente o contador.
3. **Regressões:** Reviewer e Main mantêm regressões comprovadamente introduzidas
   no range dentro do loop de correção, mesmo sem critério explícito. Elas são
   bloqueantes; defeitos preexistentes e requisitos futuros fora do escopo seguem
   encaminhamento separado. Mudanças exigidas pela spec não são tratadas como
   regressões apenas por alterarem o comportamento anterior.
4. **Bootstrap sem concessão de permissões:** removidas a criação de `.claude/`
   e a escrita automática de `Task` e `Bash(*)`. A inicialização cria apenas os
   artefatos SDD e preserva configurações existentes, inclusive as criadas pela
   versão anterior. O Main, o README e o handoff foram alinhados. O opt-in de
   autonomia por cliente continua como trabalho futuro, separado do bootstrap.
5. **Checks automatizados mínimos:** adicionada a
   [suíte de scripts](../tests/test_scripts.py), com sete testes usando somente
   a biblioteca padrão do Python, Bash e Git. Ela cobre artefatos e estado inicial,
   ausência de novas permissões, preservação de arquivos, idempotência, sintaxe,
   alinhamento dos perfis gerados e atualização de suas descrições e corpos,
   incluindo a restrição de edição do Reviewer. O
   [CI](../.github/workflows/checks.yml) executa a mesma suíte em pushes e pull requests.
6. **Spec proporcional ao escopo:** o
   [template](../.claude/skills/sdd-to-spec/SKILL.md) agora pede histórias distintas,
   rastreáveis ao brief e proporcionais à feature, cobrindo todos os comportamentos
   e restrições acordados. Remove a exigência de extensão e orienta consolidar
   duplicações sem inventar requisitos. A divergência intencional foi registrada
   em [SYNC.md](../.claude/skills/SYNC.md).

Os perfis OpenCode foram regenerados nas correções dos itens 1–3 e o README foi
atualizado. Os [cenários de validação](WORKFLOW-CHECKS.md) registram os estados
iniciais e os resultados esperados para limpeza, retomada, escopo de regressões
e síntese de specs pequenas e maiores.

Validação realizada: limpeza seletiva em repositório temporário, preservando
conteúdo local, conteúdo staged e notas não rastreadas; históricos Git temporários
para tickets e Batches com checkpoints, revisões e correções; conferência manual
das rotas do contrato; sincronização dos perfis, links locais, sintaxe dos scripts
e `git diff --check`.

O template corrigido passou no validador de skills e foi aplicado por duas sessões
isoladas de agentes Codex aos [briefs de avaliação](WORKFLOW-CHECKS.md#spec-synthesis),
em diretórios temporários. O caso pequeno produziu três histórias e o maior, seis.
A conferência contra os briefs confirmou cobertura dos requisitos, histórias
distintas e ausência de funcionalidades inventadas, incluindo o contrato de
inteiros grandes no caso pequeno e precedência de erros, preservação do estado
em falhas e isolamento das cópias no maior. As contagens são observações, não metas.
Foi uma execução por caso, apenas de síntese da spec, sem implementação ou
comparação com o template anterior; não demonstra economia de tokens ou tempo.

**Limite:** o workflow completo com agentes nos três CLIs ainda não foi executado.
Os cenários de retomada e regressões continuam manuais; a suíte automatiza os
comportamentos determinísticos dos scripts. Os sete testes passaram localmente,
incluindo o teste de permissões que falhava antes da correção. O job `scripts`
também passou no GitHub para `432951e`, conforme a
[execução 40919497987](https://github.com/holocaster/sdd-team/actions/runs/40919497987),
concluída em 2026-10-29. Isso valida aquele commit, não alterações locais posteriores.

## Reverificação anterior às correções dos itens 4, 5 e 6

Referência: `3aac7e0`, em 2026-10-29. Esta seção preserva os resultados anteriores
às correções adicionais; o estado atual está na tabela e no registro acima.

### Item 4: confirmado, com limite sobre a aplicação das permissões

O [bootstrap](../.claude/skills/sdd-main/bootstrap.sh), linhas 49–57 naquela versão,
criava `permissions.allow` com `Task` e `Bash(*)` quando o arquivo compartilhado
não existia. O script não lia consentimento nem identificava o cliente ativo.

As reproduções em repositórios Git temporários confirmaram:

- Inicialização com stdin fechado e sem argumento de consentimento: criou os
  artefatos e a regra ampla, sem perguntar.
- Configuração compartilhada existente com `deny`, configuração local, estado e
  contexto preexistentes: preservou todos os bytes após duas execuções.
- Somente `.claude/settings.local.json` existente com `deny`: preservou o arquivo,
  mas criou também `.claude/settings.json` com a regra ampla. Nova execução
  preservou os caminhos e bytes de todos os arquivos da fixture.

A [documentação atual de permissões do Claude Code](https://code.claude.com/docs/en/permissions)
confirma que `Bash(*)` corresponde a todos os comandos Bash, mas regras `deny` e
`ask` precedem `allow`, e políticas gerenciadas podem restringir sua aplicação.
Ela também condiciona regras `allow` do arquivo compartilhado à confiança no
workspace. O [sandbox é uma camada separada](https://code.claude.com/docs/en/sandboxing#how-sandboxing-relates-to-permissions-and-permission-modes).
Portanto, o teste comprova a escrita da regra sem escolha no bootstrap; não
comprova execução irrestrita ou ausência de confirmação no cliente.

O repositório não fixa uma versão do Claude Code. Não foi executada uma sessão
desse cliente para testar confiança, carregamento das regras ou restrições
efetivas. A recomendação foi separar artefatos de permissões opcionais;
as decisões do opt-in descrito no [handoff](HANDOFF-NPX-INSTALLATION.md) permanecem abertas.

### Item 5: confirmado; cenários manuais não encerram a pendência

O inventário daquele commit continha **32 arquivos rastreados**, incluindo os
[cenários de aceitação](WORKFLOW-CHECKS.md), explicitamente manuais. Não havia suíte
automatizada, runner de testes ou configuração de CI versionados naquele commit.

Passaram `bash -n` nos dois scripts e a regeneração dos três perfis OpenCode em
cópia temporária, com resultado idêntico byte a byte aos arquivos rastreados.
Os testes de bootstrap acima também passaram. Esses checks foram executados nesta
verificação; ainda estavam ausentes como testes reutilizáveis no repositório.

O passo mínimo recomendado foi versionar checks dos scripts e da sincronização,
sem introduzir um motor de workflow. Os cenários de retomada documentam resultados
esperados, mas testar uma implementação paralela dessas regras não provaria que
os agentes seguem o Markdown. Essa avaliação continua separada e pendente.

### Item 6: redação confirmada; impacto continua não medido

O [template](../.claude/skills/sdd-to-spec/SKILL.md), linhas 30 e 38, ainda exigia
uma lista `LONG` e `extremely extensive`. O
[caminho rápido](../.claude/skills/sdd-main/SKILL.md) evita a spec em mudanças
elegíveis, e o [Planner](../.claude/agents/sdd-planner.md) proíbe inventar
requisitos. Essas regras limitam o risco; uma feature pequena que exija decisão
transversal, porém, continua seguindo o template completo.

Naquela verificação, mantive o item como melhoria de redação de baixa prioridade: pedir cobertura
do escopo acordado, proporcional à feature. Não houve comparação de specs geradas
para features pequenas e grandes; não há evidência nova de aumento de tokens,
tickets ou tempo. O problema comprovado é a exigência textual de extensão, e não
uma expansão de escopo observada em execução.

## 1. Limpeza automática pode apagar trabalho local

### Evidências

- [sdd-main, seção Cold resume](../.claude/skills/sdd-main/SKILL.md), linha 122:
  determina executar `git checkout -- . && git clean -fd` ao encontrar a árvore
  suja, antes de qualquer outra ação.
- [sdd-main, fase Review](../.claude/skills/sdd-main/SKILL.md), linha 100:
  repete a limpeza global quando o Reviewer relata alterações deixadas por checks.
- [Perfil do Reviewer](../.claude/agents/sdd-reviewer.md), linha 41:
  também orienta restaurar arquivos e limpar os não rastreados dessa forma.

### Cenário e resultado observado

A reprodução foi executada exclusivamente em um repositório temporário:

1. Um arquivo foi adicionado ao índice com conteúdo conhecido.
2. Seu conteúdo na árvore de trabalho foi alterado, sem adicionar a alteração.
3. Foi criado outro arquivo, não rastreado, representando notas do usuário.
4. Foram executados os dois comandos prescritos.
5. O primeiro arquivo voltou ao conteúdo do índice; o arquivo de notas foi excluído.

Não foi necessário criar commits. O teste confirmou o efeito destrutivo dos
comandos; não foi uma execução completa do workflow por um agente.

### Por que considero um problema

Uma sessão retomada pode encontrar tanto trabalho inacabado do agente quanto
alterações feitas pelo usuário entre sessões. A regra presume uma origem sem
verificá-la. Esses comandos não distinguem arquivos temporários de trabalho útil.

A perda pode afetar alterações sem cópia em commits. Além disso,
`git checkout -- .` restaura a partir do índice, não garante uma restauração ao
commit inicial quando existem alterações staged. Portanto, a receita também não
garante, em todos os estados, a árvore limpa que o contrato exige.

### Direção mínima de correção

Identificar o que foi produzido pelo check ou agente e limpar apenas esses
artefatos. Preservar alterações de origem desconhecida e encaminhar a situação ao
usuário quando não for possível prosseguir sem descartá-las.

### O que validar

- Alterações do usuário e arquivos não rastreados sobrevivem à retomada.
- Arquivos temporários identificados podem ser removidos sem limpeza global.
- Alterações staged não são confundidas com uma árvore restaurada ao commit.

## 2. Retomada usa uma comparação incompatível com os checkpoints

### Evidências

Na [skill sdd-main](../.claude/skills/sdd-main/SKILL.md):

- Linha 80: `head_sha` identifica o último commit do Implementer; `HEAD` pode
  estar adiante dele devido a commits de estado do Main.
- Linha 91: Main deve salvar `base_sha` e `head_sha` e commitar esse estado.
- Linha 100: o resultado da revisão também é persistido em um novo commit.
- Linha 125: a diferença entre `head_sha` e a ponta do branch aparece como sinal
  de implementação ainda não registrada; a ação é salvar `HEAD` como `head_sha`.
- Linhas 126–127: o encaminhamento normal da revisão persistida exige que
  `head_sha` esteja na ponta do branch.

### Cenário que expõe a contradição

Considere uma sequência normal, sem nova implementação após a revisão:

```text
C -> I -> S -> R

C: checkpoint que ativa o ticket
I: commit da implementação
S: Main persiste head_sha = I
R: Main persiste a revisão changes_requested
```

Ao retomar depois de `R`, o estado válido contém:

```yaml
active_ticket: 01
head_sha: I
review: tickets/0001-exemplo/01-exemplo.review.md
review_round: 1
```

`HEAD` é `R`, e não `I`. A condição de igualdade da linha 127 não se sustenta,
apesar de o resultado da revisão estar corretamente persistido. A regra da linha
125 pode ser interpretada como aplicável, pois há commits do Implementer depois
do checkpoint e `head_sha` é diferente da ponta.

### Por que considero um problema

O estado produzido pelo fluxo normal não satisfaz as condições documentadas para
sua própria retomada. Uma leitura literal pode substituir `head_sha` por um commit
do Main e repetir a revisão, em vez de encaminhar a correção já solicitada.

Essa substituição também faz o `reviewed_range` persistido deixar de corresponder
ao range ativo. O Main exige essa correspondência antes de reutilizar a revisão.

O defeito identificado é uma contradição de especificação. Não foi demonstrado
que todos os modelos ou CLIs seguirão a interpretação incorreta; um agente pode
inferir a intenção e contornar a redação. Essa inferência não é uma garantia de
recuperação confiável.

### Direção mínima de correção

Reconhecer checkpoints do Main como parte normal do histórico. Reutilizar uma
revisão cujo ticket e range continuem válidos e só atualizar `head_sha` quando
houver evidência de nova implementação ainda não registrada.

### O que validar

- Retomada após o commit do Implementer, antes de Main persistir os SHAs.
- Retomada depois do checkpoint que persiste os SHAs.
- Retomada após revisão `changes_requested`, `blocked` e `approved`.
- Retomada após uma correção, preservando o `base_sha` original.
- Commits exclusivamente de estado não provocam nova revisão por si só.

## 3. Regra de escopo pode excluir regressões introduzidas pelo ticket

### Evidências

- [Perfil do Reviewer](../.claude/agents/sdd-reviewer.md), linha 54:
  classifica regressões como `blocking`.
- No mesmo perfil, linha 60: vulnerabilidades e vazamentos introduzidos permanecem
  em escopo mesmo sem critério explícito de segurança.
- No mesmo perfil, linha 62: para outros defeitos, determina que findings fora dos
  critérios de aceitação não alterem o veredito.
- [sdd-main](../.claude/skills/sdd-main/SKILL.md), linhas 106–112:
  reforça o encaminhamento separado dos defeitos fora dos critérios.

### Cenário para análise

Um ticket pede suporte a um novo formato de entrada. A implementação altera um
parser compartilhado: o novo formato funciona, mas um formato anteriormente
suportado passa a produzir resultado incorreto. Os critérios do ticket mencionam
somente o novo formato.

Essa quebra foi introduzida pelo ticket, mas está fora da descrição literal dos
critérios. A redação atual permite tratá-la como não bloqueante, embora também
classifique regressões como bloqueantes.

### Por que considero um problema

Existem duas perguntas diferentes: se o defeito pertence aos requisitos novos e
se foi causado pela mudança. Proteger o ticket de bugs preexistentes é adequado.
Aplicar a mesma exclusão a uma regressão introduzida enfraquece a revisão.

Os exemplos do contrato citam defeitos preexistentes e trabalho de outros tickets,
o que sugere uma intenção mais restrita. A condição escrita é mais ampla que esses
exemplos. Este item é uma ambiguidade contratual, não uma regressão real encontrada
em um projeto consumidor nem uma aprovação incorreta reproduzida com agentes.

### Direção mínima de correção

Explicitar que regressões demonstráveis introduzidas pelo range são relevantes
para o veredito, mesmo sem critério específico. Manter o encaminhamento separado
para defeitos preexistentes ou comportamentos futuros ainda não exigidos.

### O que validar

Comparar três casos: defeito preexistente, requisito futuro de outro ticket e
regressão introduzida pela implementação atual. Apenas estar fora dos critérios
não deve tornar os três casos equivalentes.

## 4. Bootstrap cria permissões amplas sem escolha explícita

### Evidências

- [bootstrap.sh](../.claude/skills/sdd-main/bootstrap.sh), linhas 49–56:
  quando `.claude/settings.json` não existe, cria uma configuração com
  `"allow": ["Task", "Bash(*)"]`.
- [sdd-main, pré-requisitos](../.claude/skills/sdd-main/SKILL.md): orienta executar
  o bootstrap quando `.ai/PROJECT_STATE.md` estiver ausente.
- [Handoff de instalação](HANDOFF-NPX-INSTALLATION.md), linhas 38–49:
  registra como requisito futuro uma escolha explícita antes de configurar
  autonomia, além da identificação do cliente ativo.

### Resultado observado

Executei o bootstrap em um repositório Git temporário, sem configuração Claude
prévia. O arquivo foi criado com exatamente `Task` e `Bash(*)` na lista de
permissões, sem pergunta ou parâmetro de consentimento.

Também confirmei que uma segunda execução preserva os bytes de uma configuração
existente. Não foi observado sobrescrever configurações já presentes.

### Por que considero um problema

Inicializar os artefatos do workflow também passa a configurar aprovação ampla de
comandos shell no Claude Code. Um usuário interessado apenas na estrutura SDD pode
não pretender conceder essa autonomia. A configuração também é criada quando o
mesmo script é usado para inicializar um projeto de outro CLI.

Isso não significa que o script remova todas as restrições de sandbox ou políticas
gerenciadas. O comportamento comprovado é a criação da regra ampla de aprovação.

É uma pendência de produto já reconhecida no handoff, cuja implementação foi
explicitamente adiada. Não é uma regressão recém-descoberta nem prova de que o
bootstrap atual descumpre sua descrição no README.

### Direção mínima de correção

Separar a criação dos artefatos da configuração opcional de permissões. A segunda
etapa deve depender de escolha explícita e do cliente correto, preservando as
restrições existentes. As decisões abertas do handoff ainda precisam ser resolvidas.

### O que validar

Inicialização sem consentimento não altera permissões. Consentimento positivo
atinge somente o cliente selecionado. Configurações existentes são preservadas e
execuções repetidas não ampliam a autorização anterior.

## 5. Garantias centrais não têm checks automatizados versionados

### Evidências

O inventário com `git ls-files` encontrou 30 arquivos rastreados no momento da
análise. Não foram encontrados testes automatizados ou configuração de CI
versionados. Os dois scripts executáveis distribuídos são
[bootstrap.sh](../.claude/skills/sdd-main/bootstrap.sh) e
[sync-agents.sh](../.opencode/sync-agents.sh).

### Por que considero um problema

Os contratos de estado, os perfis gerados e as permissões são comportamento do
produto. Uma alteração pequena nesses arquivos pode comprometer retomada ou
isolamento sem produzir erro de sintaxe.

Os checks manuais desta análise passaram, mas não são uma proteção persistente
para mudanças futuras. O problema de retomada do item 2 demonstra um cenário
concreto que uma verificação dos estados esperados deveria cobrir.

A ausência no repositório não prova que o autor nunca realizou testes manuais ou
que não existam verificações externas. O achado se limita à proteção versionada e
reproduzível disponível aos contribuidores.

### Direção mínima de correção

Adicionar poucos checks para inicialização, preservação de arquivos existentes,
geração dos perfis e estados de retomada. Os scripts podem ser testados em
diretórios temporários. Os cenários do workflow devem ter estado inicial e rota
esperada explícitos; não basta verificar que uma frase existe no Markdown.

Não há evidência de necessidade de um novo framework ou de um motor de workflow.
Testar scripts e contratos também não comprova, sozinho, adesão de um modelo às
instruções: a execução com agentes exige avaliação separada.

## 6. Template incentiva volume de especificação sem critério proporcional

### Evidência

O [template sdd-to-spec](../.claude/skills/sdd-to-spec/SKILL.md), linhas 30 e 38,
exige uma lista longa e extremamente extensa de histórias, independentemente do
tamanho da feature que seguir o caminho completo.

### Por que considero um problema

O caminho completo pode ser necessário para uma mudança pequena com uma decisão
arquitetural. Nesse caso, a exigência de extensão pode incentivar histórias
redundantes ou inferidas além do brief, aumentando o material a revisar e os
critérios que o Planner precisa mapear para tickets.

Este é um risco sugerido pela instrução, não um efeito medido. Não foram analisadas
features consumidoras que demonstrem aumento de tokens, escopo ou tempo de execução.
Por isso, este item tem prioridade inferior aos problemas de integridade e estado.

### Direção mínima de melhoria

Pedir cobertura completa do comportamento acordado, com quantidade de histórias
proporcional à feature, em vez de exigir uma lista extensa por definição.

### O que validar

Avaliar uma feature pequena e outra maior pelo mesmo template. Verificar cobertura
dos requisitos, ausência de escopo inventado e utilidade de cada história, sem usar
o tamanho do documento como medida de qualidade.

## Verificações realizadas e limites

Passaram na análise:

- `bash -n` nos dois scripts.
- Bootstrap em repositório temporário, incluindo preservação dos arquivos
  existentes em execução repetida.
- Geração dos perfis OpenCode em cópia temporária, com resultado idêntico aos
  arquivos rastreados.
- Resolução dos links Markdown locais fora de `docs/archive/`.
- `git diff --check`.

A consulta ao Context7 apresentou documentação tanto do esquema antigo quanto do
V2 do OpenCode. A conferência com a
[documentação oficial V2 de agentes](https://opencode.ai/v2/docs/agents) confirmou
que `permissions` com regras `action`, `resource` e `effect` é válido nesse
formato. Portanto, essa sintaxe não foi registrada como defeito. Isso não comprova
compatibilidade com todas as versões do CLI.

Não foram executados o workflow completo nos três CLIs, uma instalação pública
em ambiente limpo, uma auditoria completa de credenciais ou benchmarks de custo e
tempo. O efeito da limpeza e o comportamento do bootstrap foram reproduzidos; os
problemas de retomada e escopo foram estabelecidos pela leitura dos contratos.

Os itens 1, 2 e 3 foram corrigidos nas instruções; o item 4 foi resolvido com
bootstrap apenas de artefatos, e o item 5 recebeu checks executáveis e CI.
O item 6 foi corrigido no template. O CI já passou para `432951e`.
Permanecem pendentes a validação completa do workflow com agentes nos três CLIs
e, como trabalho futuro separado, o instalador e o opt-in de permissões por cliente
descritos no handoff. Não foi medido ganho de custo ou tempo do novo template.
