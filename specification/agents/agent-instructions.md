# Domain — Agentic layer

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

**Primary actors:** Agents, Tool
**Needs addressed:** agents need clear, non-contradictory instructions and a **common**,
cross-runtime structure for what they are, what they can do, and how the system drives them.

This domain is the **interface between the agents and the system**. `AGENTS.md` is a good
precedent, but there is no shared structure for the artifacts that steer agents. SpecLore
defines that structure so the same artifacts work across runtimes (Claude, Codex, others) and
agents receive one coherent set of instructions.

## The catalog

Agentic elements fall into three families:

| Family | Element | What it is |
| ------ | ------- | ---------- |
| **Definition** (what an agent *is* / *can do*) | `agent` | A role: identity, tools, constraints, base instructions. |
| | `skill` | A reusable capability, invoked **autonomously or on explicit request** (a *command* is just a skill with explicit invocation). |
| | `prompt` | A reusable, parameterized prompt template. |
| **Orchestration** (how work is *driven* & *bound* to the system) | `workflow` | An ordered set of steps over agents and skills. |
| | `hook` | An event → action binding (the reactive link to the system). |
| **Collaboration** (how agents *share*) | memory, message, cadence | See [Agent collaboration](agent-collaboration.md). |

Definitions and the instruction file are specified below; orchestration in
[Agent orchestration](agent-orchestration.md); collaboration in
[Agent collaboration](agent-collaboration.md).

### Invocation intent — one artifact, two modes

A `skill` **is** a command and vice-versa: a single artifact, distinguished by an `invocation`
property (not by shape):

- **`invocation: auto`** — the agent loads the skill the moment it judges it relevant. It
  *structures a démarche* — e.g. while writing a document, the agent recognises on its own that
  a structuring skill applies.
- **`invocation: explicit`** — the skill runs **only on an explicit request** (natural language
  is fine, but it must be an explicit demand); it is never triggered by the agent's own
  conclusion. This is what used to be called a *command*.

Example: an analysis loads an `auto` skill that *identifies* features to create. The
`create-feature` skill (`invocation: explicit`) does **not** run — even if the agent concludes
features should be created. Intent, not inference, invokes an explicit skill.

## Where they live

The agentic definitions live under an `agents/` folder, one **structural collection** per kind
(a `usage`, declared in its descriptor — see [Folder tree](../substrate/folder-tree.md)). They are authored
content, **not** `_`-application folders:

```
agents/roles/      # agent definitions
agents/skills/     # skills (a command = a skill with invocation: explicit)
agents/prompts/    # prompts
agents/workflows/  # workflows
agents/hooks/      # hooks
```

(`roles`, `skills` are confirmed; `prompts`, `workflows`, `hooks` follow the same pattern.)

An element MAY be **global** (reusable across projects) or **project-scoped**. Every element is
an **entity** with a `guid`, so agents, workflows, and hooks reference each other by
`ref://<guid>` ([References](../substrate/references.md)) — never by name or path.

> **Cross-runtime.** SpecLore fixes the *canonical structure* of these artifacts. A given
> runtime maps its native locations (`.claude/`, `AGENTS.md`, …) onto it; that mapping is an
> adapter, i.e. implementation, and is out of scope as *normative* text.

### Runtime support & mapping

*(Informative.)* How the definitions land on real runtimes today (context, not a normative
rule):

- **Skills are a near-standard.** Both **Claude Code** and **OpenAI Codex** support
  **`SKILL.md`** — YAML frontmatter (*when* to use) + Markdown (*how*), in a folder with
  optional resources, loaded on demand (progressive disclosure) and **model-invoked**.
  SpecLore's `skill` maps to it directly — align with `SKILL.md` rather than diverge.
- **Commands are skills.** Claude's flat `.claude/commands/*.md` and Codex's custom prompts are
  **deprecated in favour of skills**; explicit-only invocation is expressed by **invocation
  controls in the skill frontmatter**. SpecLore matches this directly: one `skill` artifact with
  an `invocation` field (`auto` / `explicit`), a *command* being a skill with
  `invocation: explicit`.
- **Agents (roles)** map to native **subagents** (markdown + frontmatter).
- **APIs (Anthropic Messages, OpenAI) have no skill concept** — the primitives are **tool use /
  function calling** and **MCP** (Anthropic's protocol, since adopted by OpenAI and Google).
  Programmatic runtimes therefore reach SpecLore skills through an **MCP server** — the same
  abstraction as [the AI tool](../substrate/references.md#7-system-operations).

## Instruction file

*(First draft.)* The base file that steers an agent (the `AGENTS.md` role). Several may apply
at once; the structure MUST make **precedence deterministic** so guidance is never
contradictory — a defined order (e.g. scope: global → project → subtree) resolves conflicts.

## `agent`

An agent is a **Markdown document** (frontmatter + body) in `agents/roles/`. Its frontmatter is
frozen by [`agent.schema.json`](../../schemas/agent.schema.json), which extends the
[base document schema](../../schemas/document.base.schema.json).

**Frontmatter**

| Field | Type | Req. | Meaning |
| ----- | ---- | :--: | ------- |
| `guid` | uuid v4 | ✔ | Stable identity ([References](../substrate/references.md)). |
| `type` | `"agent"` | ✔ | Document type. |
| `name` | string | ✔ | The agent's name/label. |
| `role` | string | ✔ | Its role (e.g. `developer`, `product-owner`). |
| `description` | string | | One-line summary. |
| `model` | string | | Preferred model. |
| `effort` | `low`\|`medium`\|`high`\|`xhigh`\|`max` | | Default reasoning effort. |
| `parallelism` | integer ≥ 1 | | Max jobs run at once — the capacity slots of [Cadence](agent-collaboration.md#cadence). Operator-tunable (tokens). |
| `skills` | `ref://<guid>`[] | | Skills the agent may use. |
| `tools` | string[] | | Allowed native / MCP tools. |
| `constraints` | string[] | | Guardrails it MUST respect. |
| `scope` | `global`\|`project` | | Reuse scope. |
| `relations` | relations | | Typed refs to other entities. |
| `created` | date-time | | Creation timestamp. |
| `author` | string | | Creator (GitHub name, agent, or terminal profile). |

**Body** — the agent's base instructions / persona (its system-prompt-like content); MUST be
non-empty.

**Example**

```markdown
---
guid: 7c9e6a1b-3d2f-4a10-9b7c-2e5f8a1d4c60
type: agent
name: Alice
role: developer
model: claude-opus-5
parallelism: 3
skills:
  - ref://3f2a9c14-8b6d-4e21-a0f5-1c7b9d2e6a83
constraints:
  - Never modify specs without an explicit request.
scope: project
---

# Alice — Developer

You implement features from the backlog, one task at a time…
```

## `skill`  (a *command* is a skill with `invocation: explicit`)

*(First draft.)*
- **Frontmatter:** `guid`, `type: skill`, `name`, `description`, **`invocation`** (`auto` |
  `explicit`), `when-to-use` (the trigger, for `auto`), optional `args` (for `explicit`) and
  `inputs`.
- **Body:** the capability's instructions; may bundle resources → a folder.
- **Form & location:** a **Markdown file with frontmatter**, in `agents/skills/` — this is the
  `SKILL.md` shape (see [Runtime support](#runtime-support--mapping)).

## `prompt`

*(First draft.)*
- **Frontmatter:** `guid`, `type: prompt`, `name`, `description`, `parameters` (named
  variables).
- **Body:** the template text with placeholders for the parameters.

## Related

- Orchestration: [Agent orchestration](agent-orchestration.md)
- Collaboration: [Agent collaboration](agent-collaboration.md)
- Schemas: [`../schemas/`](../../schemas/)
- Conformance: [`../conformance/`](../../conformance/)
- Examples: [`../examples/`](../../examples/)
