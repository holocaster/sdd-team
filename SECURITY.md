# Política de segurança

## Código suportado

Reproduza problemas na revisão mais recente da branch padrão. Revisões antigas
não têm garantia de correções de segurança. Os relatos são tratados conforme a
disponibilidade do mantenedor, sem prazo de resposta garantido.

## Relatar uma vulnerabilidade

Compartilhe detalhes de vulnerabilidades, credenciais e provas de conceito por
um canal privado.

Se o relato privado do GitHub estiver habilitado, use
[Report a vulnerability](https://github.com/holocaster/sdd-team/security/advisories/new).
Caso contrário, abra uma [issue](https://github.com/holocaster/sdd-team/issues)
com o título `Security contact request`, solicitando um canal privado sem
descrever a vulnerabilidade. Envie os detalhes depois que o canal for definido.

Inclua no relato privado:

- Commit afetado, sistema operacional, CLI e versão.
- Skills, perfis e permissões relevantes, sem credenciais.
- Passos de reprodução ou um exemplo mínimo em um repositório descartável.
- Comportamento esperado, resultado observado e impacto possível.

Combine a divulgação pública com o mantenedor durante a avaliação e correção.
Use dados sintéticos e remova segredos de logs, diffs e artefatos anexados.

## Limites de segurança do workflow

- Skills e perfis são instruções para agentes. Isolamento de sessões e papéis
  não fornece isolamento de processos; acesso a arquivos, comandos e rede
  depende das permissões e do sandbox do CLI utilizado.
- O workflow prevê escrita de arquivos e commits locais. Configure permissões
  e autorizações no CLI antes de executá-lo. O `bootstrap.sh` cria a estrutura
  de artefatos e preserva as configurações de permissões existentes.
- Conteúdo do projeto e resultados de ferramentas podem ser enviados ao
  provedor de modelos configurado. Briefs, specs, tickets e revisões são
  persistidos em arquivos e commits; revise-os antes de compartilhá-los.
- A revisão obrigatória em modo `BRANCH` cobre o range da implementação,
  incluindo credenciais nos commits intermediários. `FULL HISTORY` é uma
  auditoria separada, solicitada explicitamente; preparar documentação pública
  não executa essa auditoria.
- Aprovação de um agente ou ausência de findings não garante ausência de
  vulnerabilidades ou segredos. A suíte de scripts também não valida decisões
  dos modelos nem substitui a revisão do conteúdo a publicar.

Veja os [pré-requisitos](README.md#pré-requisitos) e os
[contratos do workflow](.claude/skills/sdd-main/SKILL.md) para a configuração.
