# SpecLore Foundations

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

SpecLore is a **definition**. It chooses and **freezes** the structures that humans, agents,
and tools use to work from the same source. It is prescriptive: it says what a structure *is*
and what an artifact **MUST** contain — not how mature an implementation happens to be.

The actors and their needs below frame *why* each structure exists; the domains then define
the structures themselves.

## 1. Actors

1. **The pilot** — the human (also called the *requester*): a user of prompts and the
   bottleneck of the process. The pilot MUST be able to understand the state of the work and
   make decisions easily and quickly.
2. **The agents** — the AI workers. They need clear, non-contradictory instructions and a
   frame that keeps them from deviating. They usually work several at once, so they need to
   share information and coordinate their cadence.
3. **The tool** — no longer a chat interface but a project manager. It orchestrates the
   agents and lets the pilot follow and steer the work.

## 2. Needs

| Actor  | Core needs |
| ------ | ---------- |
| Pilot  | Instruct the system and consult its state through structure a program can render **interactively** — not a wall of prose. |
| Agents | A structured instruction format; a **common** structure for skills / agents across runtimes; their own memory and messaging; collision-free concurrent work. |
| Tool   | A defined folder layout, frontmatter, and Markdown formatting types; technical **JSON** to exchange state and guarantee properties prose cannot (e.g. **atomicity**). |

## 3. Principles

### No redundancy — one home per fact

Information MUST NOT be duplicated. Each piece of information lives in **exactly one place**,
and every stored piece must **justify its reason to exist**. A second authoritative copy is a
source of drift and MUST be avoided.

Where fast access needs a second representation, it MUST be a **derived index or cache** —
clearly non-authoritative, rebuildable from the source, and never treated as truth on
conflict. A derived structure is allowed only when it earns its place (it answers a question
the source cannot answer cheaply).

This principle drives concrete choices across the corpus: a document's metadata lives only in
its frontmatter — no sidecar ([Interactive documents](../documents/interactive-documents.md)); and an
entity's location is materialized in a single derived index, not duplicated across a hashmap
*and* a store ([References](../substrate/references.md)).

### An open framework, not a fixed structure

SpecLore fixes **invariants and artifact contracts**; a project's classification and choice
of notions remain **open**, so it fits each team's organization. Once agents understand it, they
lay the structure **with the operator** and evolve it — that is the whole point: give the
structures and tools that let each context answer for itself. Concretely:

- the **operator** co-builds according to their needs;
- the **tools** guarantee the system's coherence, agnostically;
- an **IDE or tracking system** can be plugged in and adapt, just as agnostically;
- the **agents** build and follow a *bounded* structure;
- **agents of any model** can work together.

## 4. Domains

The needs are met by five domains. Each **defines and freezes** a set of structures.

| Domain | Primary actors | What it defines |
| ------ | -------------- | --------------- |
| [Interactive documents](../documents/interactive-documents.md) | Pilot | The structured Markdown a tool can render and the pilot can act on. |
| [Agentic layer](../agents/agent-instructions.md) | Agents, Tool | The agent↔system interface: agents, skills, prompts, workflows, and hooks. |
| [Agent collaboration](../agents/agent-collaboration.md) | Agents | The structure of agent memory and inter-agent messages. |
| [Concurrent work](../agents/concurrent-work.md) | Agents, Tool | The workspace / branch / merge structures for concurrent editing. |
| [Tool substrate](../substrate/tool-substrate.md) | Tool | The folder layout, frontmatter contract, and companion-JSON conventions. |

## 5. How each domain is written

Every domain document follows the same shape:

- **Structures defined here** — the named structures the domain freezes.
- One section per structure — prose definition, the **frozen shape** (fields / schema /
  example), and normative **requirements**.
- **Related** — the schemas, conformance criteria, and examples that back it.

## 6. Requirement conventions

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative
requirement levels (RFC 2119 / RFC 8174). A conforming artifact is one that satisfies the
MUST-level requirements of the structures it uses and validates against the corresponding
[schemas](../../schemas/).

## 7. Glossary

| Term | Meaning |
| --- | --- |
| Pilot / operator | Human who directs the project and makes decisions. |
| Agent | AI worker acting under instructions; its runtime is outside core. |
| Tool | Consumer that reads, validates or mutates SpecLore artifacts. |
| Profile | Named, versioned set of normative requirements. |
| Document | An authored Markdown entity with YAML frontmatter. |
| Descriptor | README representing a structural folder, not a second entity. |
| Frontmatter | The file's authoritative metadata mapping. |
| GUID | Stable UUID v4 identity, independent of location. |
| Relation | Declared forward edge; its inverse is derived in the reference index. |
| Atomic mutation | Change whose participating readers observe all-old or all-new state. |
| Skill, workflow, memory, workspace | Deferred domain concepts; see their informative drafts. |
