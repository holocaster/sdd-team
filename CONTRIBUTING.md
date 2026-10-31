# Como contribuir

Relatos de bugs e pull requests focados são bem-vindos. Para vulnerabilidades,
siga [SECURITY.md](SECURITY.md) e compartilhe os detalhes por um canal privado.

## Ambiente de desenvolvimento

Faça um fork, clone o seu fork e entre na raiz do repositório. Para os checks
locais, são necessários Python 3, Bash e Git:

```bash
python3 -B -m unittest discover -s tests -v
```

Para exercitar os agentes, siga a [instalação no README](README.md#instalação),
incluindo os perfis, as skills externas e o Gitleaks. Use um repositório
descartável como projeto alvo; este repositório distribui o workflow e não
mantém `.ai/PROJECT_STATE.md` para si. Chamadas aos modelos seguem os custos
e as permissões do CLI configurado.

## Organização e fontes canônicas

- `.claude/skills/`: instruções do workflow e scripts distribuídos.
- `.claude/agents/`: contratos canônicos de Planner, Implementer e Reviewer.
- `.opencode/agents/`: perfis gerados a partir dos canônicos.
- `tests/test_scripts.py`: checks de bootstrap e sincronização.
- `docs/WORKFLOW-CHECKS.md`: cenários manuais para os contratos dos agentes.
- `docs/archive/`: pesquisa histórica.

Leia [AGENTS.md](AGENTS.md) antes de alterar contratos. `CLAUDE.md` é um symlink
para esse arquivo. Para mudanças nos forks de Matt Pocock, leia também
[SYNC.md](.claude/skills/SYNC.md); eles têm diferenças intencionais do upstream.

Se alterar o corpo ou a descrição de um perfil canônico, regenere os perfis:

```bash
.opencode/sync-agents.sh
```

Instalações por symlink consomem as alterações deste checkout imediatamente.

## Validação e pull requests

Trabalhe em passos pequenos. Antes de enviar um pull request, execute a suíte
acima, confira os links locais dos documentos alterados e rode:

```bash
git diff --check
```

Mudanças no comportamento dos agentes devem exercitar os cenários relevantes de
[WORKFLOW-CHECKS.md](docs/WORKFLOW-CHECKS.md). A suíte automatizada verifica scripts
e perfis gerados; ela não comprova que um modelo segue os contratos do workflow.
Para mudanças somente em documentação, verifique links e comandos; novos testes
são necessários quando houver comportamento novo que precise de cobertura.

Em bugs, informe o commit, sistema operacional, CLI e versão, skills instaladas,
passos para reproduzir e comportamento esperado e observado. Use exemplos
sintéticos e remova credenciais e dados privados de logs e artefatos.

Mantenha cada pull request focado, explique o problema e a mudança de
comportamento, liste os checks executados e atualize a documentação afetada.
Discuta mudanças amplas de contrato em uma issue antes de implementá-las.

## Licença

As contribuições são disponibilizadas sob a [licença MIT](LICENSE) do projeto.
Preserve os avisos de terceiros em [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
ao reutilizar ou adaptar material externo.
