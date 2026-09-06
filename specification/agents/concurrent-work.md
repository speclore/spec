# Domain — Concurrent work

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

**Primary actors:** Agents, Tool
**Needs addressed:** Agents usually work in the same folder, which causes edit
**collisions**. A structured model of workspaces, branches, and merges formalizes concurrent
editing.

## Purpose

When several agents edit shared files, unstructured concurrency produces lost work and
conflicts. This domain defines and freezes a **workspace / branch / merge** model — borrowed
in spirit from version control — so that concurrent work is isolated and reconciled
deliberately.

## Structures defined here

- **Workspace** — the isolated area an agent works in.
- **Branch** — a divergent line of change.
- **Merge** — how divergent work is reconciled and conflicts are represented.

## Workspace

*(Definition to be fixed.)* The frozen structure of a workspace: what it contains, how it is
identified, and how it relates to the shared tree.

## Branch

*(Definition to be fixed.)* How a divergent line of change is represented and tracked.

## Merge

*(Definition to be fixed.)* How merges are requested and applied, and how conflicts are
represented so they are surfaced rather than silently overwritten.

## Related

- Schemas: [`../schemas/`](../../schemas/)
- Conformance: [`../conformance/`](../../conformance/)
- Examples: [`../examples/`](../../examples/)
