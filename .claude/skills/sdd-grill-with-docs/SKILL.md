---
name: sdd-grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADRs and glossary) as we go. Use during SDD discovery, driven by sdd-main in the orchestrator session. Ungated copy of grill-with-docs so it is reachable from the SDD workflow.
---

Call the Skill tool for "grilling", then for "domain-modeling" with this SDD artifact contract. It overrides the dependency's default paths and file layout, including those in its referenced formats:

- Read and write glossary terms in the glossary section of `docs/CONTEXT.md` wherever upstream names `GLOSSARY.md` or `CONTEXT.md`. Apply the glossary format to that section and preserve the rest of the file, including current cross-cutting decisions.
- Read existing ADRs from `docs/adrs/` wherever upstream names `docs/adr/`.
- During discovery, capture settled decisions in `docs/CONTEXT.md` and ADR proposals in the feature brief. The `sdd-planner` writes the ADRs in `docs/adrs/` after discovery.
