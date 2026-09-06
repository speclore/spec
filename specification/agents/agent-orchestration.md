# Agent orchestration — workflows & hooks

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

**Part of:** [Agentic layer](agent-instructions.md)
**Primary actors:** Agents, Tool
**Needs addressed:** drive multi-step agent work deterministically, and **bind system events
to agentic actions** — the two ways the system and the agents act on each other.

Orchestration is the active side of the agentic layer. A **workflow** is *proactive* (an
ordered plan the system runs); a **hook** is *reactive* (the system reacts to an event by
running something). Both reference definitions ([agents, skills, prompts](agent-instructions.md))
by `ref://<guid>`, never by name, and both target work through [selectors](../foundations/selectors.md).

### The event bus — workflows and hooks compose

Events are a shared bus. **Emitters** — system operations ([scan/watch/commit](../substrate/references.md#7-system-operations)),
agents, and **workflows** — raise events; **hooks** listen and run actions. So the two compose
both ways: a **hook** can run a **workflow**, and a **workflow** can, by emitting an event,
**trigger a hook**. Every listen and every emit is scoped by an [event selector](../foundations/selectors.md#event-selectors)
so nothing fires on "everything".

## `workflow`

An ordered set of steps over agentic definitions.

*(First draft.)*
- **Frontmatter:** `guid`, `type: workflow`, `name`, `description`, optional `trigger` (an
  [event selector](../foundations/selectors.md#event-selectors)), `inputs`.
- **Body — steps:** a list (the [DOM item model](../documents/interactive-documents.md#the-document-object-model)
  applies — each step is an item, so `progress` rolls up). Each step carries:
  - a **target** — a `ref://<guid>` of the `agent` / `skill` it runs, or a
    [selector](../foundations/selectors.md) when it acts over a matched set;
  - its **inputs**;
  - **control flow** — sequence (default), parallel, or a condition.
- **Form:** a Markdown document; a folder if it grows sub-parts.

Because steps are items, a workflow doubles as its own **progress view** — a running workflow
reports completion the same way a task list does.

## `hook`

An **event → action** binding: the reactive link between the system and the agents.

*(First draft.)*
- **Frontmatter:** `guid`, `type: hook`, `event`, `action`, `enabled`.
  - **`event`** — an [event selector](../foundations/selectors.md#event-selectors): an event **kind**
    (`created`, `updated`, `deleted`, `moved`, `reference-broken`, `commit`, `scan`, `message`,
    …) narrowed by an entity/node selector — e.g. `updated` where `type = feature` and
    `property = status`, **not** a bare "changed". This is what makes a hook precise.
  - **`action`** — what runs: a `ref://<guid>` to a `skill` / `workflow`.
- **Body:** conditions and notes.

Hooks are what let the system stay coherent *automatically* — e.g. on a broken reference,
trigger a fixing workflow; on a commit, run the quality analyzer; on an entity created in a
subtree, notify an agent.

## Related

- Definitions: [Agentic layer](agent-instructions.md)
- Collaboration: [Agent collaboration](agent-collaboration.md)
- Schemas: [`../schemas/`](../../schemas/)
- Conformance: [`../conformance/`](../../conformance/)
- Examples: [`../examples/`](../../examples/)
