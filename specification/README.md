---
usage: corpus
title: The SpecLore Specification
---

# The SpecLore Specification (corpus)

This directory **is** the specification. It is a *corpus* — split by theme into sub-folders —
not a single monolithic document. This is editorial publication content: its historical
frontmatter sketches descriptors but does not claim core conformance. The tested dogfooding
target is the [example project](../examples/core-project/README.md).

## Start with the released scope

The [0.1.0-core contract](core/core.md) and its versioned schemas are the normative release
candidate. See [conformance](../conformance/README.md) for verification and the
[backlog](../backlog/README.md) for subsequent work. The domain documents below are informative
design drafts and may contain proposals superseded by the core contract.

## What this corpus is (and isn't)

SpecLore **defines and freezes structures**: how to organize folders, frontmatter, Markdown
formatting, and technical JSON so that specifications serve humans, agents, and tools alike.
It is **prescriptive** — it fixes structures and states requirements (MUST / SHOULD). It is
**not** an audit or maturity model, and **not** a reference implementation.

## Reading order

1. **`foundations/`** — the socle.
   - [foundations.md](foundations/foundations.md) — actors, needs, principles, requirement conventions.
   - [selectors.md](foundations/selectors.md) — the cross-cutting selector language (CSS-like) for entities, nodes, and events.
2. **`documents/`** — the interactive-document domain.
   - [interactive-documents.md](documents/interactive-documents.md) — structured Markdown the pilot can render and act on.
   - [document-parsing.md](documents/document-parsing.md) — the parse/serialize engine: two linked representations, "lossless", and the canonical form.
   - [document-types.md](documents/document-types.md) — per-type document structures (base, task, feature, story, bug, decision).
3. **`substrate/`** — the tool substrate.
   - [tool-substrate.md](substrate/tool-substrate.md) — folder layout, frontmatter, formatting types, and JSON guarantees.
   - [folder-tree.md](substrate/folder-tree.md) — the folder-tree axioms (navigation & partitioning), the descriptor, and classification/balance.
   - [references.md](substrate/references.md) — the relational layer: entity guids, the `_refs` store, cardinality, reciprocity, and reference strength.
4. **`agents/`** — the agentic layer.
   - [agent-instructions.md](agents/agent-instructions.md) — definitions: agent, skill (with invocation), prompt.
   - [agent-orchestration.md](agents/agent-orchestration.md) — workflows and hooks: the active link between agents and the system.
   - [agent-collaboration.md](agents/agent-collaboration.md) — memory, communication (conversation vs message), and cadence.
   - [concurrent-work.md](agents/concurrent-work.md) — workspaces, branches, and merges for concurrent editing.
5. **`project-management/`** — the toolbox.
   - [project-management.md](project-management/project-management.md) — the notions of project management (an extensible palette any method composes).

Each document links to the [`../schemas/`](../schemas/) that validate its JSON, the
[`../conformance/`](../conformance/) criteria that test it, and the
[`../examples/`](../examples/) that demonstrate it.
