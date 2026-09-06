# Document types

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

**Part of:** [Interactive documents](interactive-documents.md)
**Builds on:** [Folder tree](../substrate/folder-tree.md) (Q1–Q4 form), [References](../substrate/references.md),
[Project management](../project-management/project-management.md) (the notions)

A document's frontmatter `type` fixes its expected structure: which **frontmatter properties**
it carries (placed by [Q1–Q3](interactive-documents.md#frontmatter-or-body)), which
**header-region blocks** it holds, and which **body sections** it expects. Types are an
**extensible palette** — below is a first proposal for project tracking; every type extends a
common **base**.

> These are *Markdown document* types (notional leaves). Grouping entities that carry a list —
> a **sprint**, a **milestone**, a `tasks`/`features` collection — are **structural folders**
> described by their descriptor (a `README.md`, see [Folder tree](../substrate/folder-tree.md)), not by a
document type.

## Base document

Every document type includes these.

**Frontmatter**

| Property | Q → home | Notes |
| -------- | -------- | ----- |
| `guid` | Q1 → frontmatter | Stable identity ([References](../substrate/references.md)). Required. |
| `type` | Q2 → frontmatter | The document type. Required. |
| `author` | Q1 → frontmatter | Creator. Required. |
| `created` | Q1 → frontmatter | Creation timestamp. Required. |
| `status` | Q2 → frontmatter | Workflow state. |
| `tags` | Q2 → frontmatter | Free classification. |
| `version` | Q3 → frontmatter | Current version (scalar). |
| `relations` | Q3 → frontmatter | Typed references to other entities. |

**Header region** — `versions[]`: the change-tracking table `version | author | date | comment`
(optional; a body-backed property, [conflict policy](interactive-documents.md#conflict-policy-fallback-and-alerts) applies).

**Body** — `# Title`, then type-specific sections.

The per-type sections below list only what the type **adds** to this base.

## `task`

- **Frontmatter (+):** `priority`, `estimate`, `assignee`; `relations`: `parent` (for a
  subtask), `blocks` / `blocked-by`, sprint membership (by reference).
- **Body:** a short description; an **acceptance checklist** (task list); optional notes.
- **Form note:** a one-line task with a checkbox belongs *inside* its parent document
  ([Q4](../substrate/folder-tree.md#choosing-a-form-referential-document-or-folder)); it becomes its own
  `task` document once it carries real content.

## `feature`

- **Home:** the classification tree `features/domain-XXX/epic-XXX/` (its single primary home).
- **Frontmatter (+):** `status` (proposed / building / shipped); `relations`: stories,
  dependencies.
- **Body:** description; **scope**; **acceptance criteria** (task list); links to related
  stories/tasks.
- **Form note:** a `feature` becomes a folder if it grows sub-parts (its own tasks, criteria
  lists); otherwise a single `feature.md`.

## `user-story`

- **Frontmatter (+):** `estimate`; `relations`: parent `epic`/`feature`, sprint membership.
- **Body:** the story statement (*as a … I want … so that …*); **acceptance criteria** (task
  list); notes.

## `bug`

- **Frontmatter (+):** `severity`, `priority`, `assignee`; `relations`: affected
  `feature`/`component`, `duplicate-of`.
- **Body:** **reproduction** steps; expected vs actual; environment; a fix **checklist**.

## `decision` (ADR)

- **Frontmatter (+):** `status` (proposed / accepted / superseded); `relations`: `supersedes`
  / `superseded-by`, affected entities.
- **Body:** **Context**; **Decision**; **Consequences** — the classic ADR shape.

## Extending the palette

A new type is defined the same way: pick its frontmatter properties with Q1–Q3, declare its
header-region blocks and their roles, and fix its body sections. Its structure is validated by
[`../schemas/`](../../schemas/) and demonstrated in [`../examples/`](../../examples/).

## Related

- Schemas: [`../schemas/`](../../schemas/)
- Conformance: [`../conformance/`](../../conformance/)
- Examples: [`../examples/`](../../examples/)
