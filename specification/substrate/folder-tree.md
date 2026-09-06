# Folder tree

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

**Part of:** [Tool substrate](tool-substrate.md)
**Primary actors:** Tool, Pilot, Agents
**Needs addressed:** a defined folder layout a tool can depend on, that also lets the pilot
navigate and lets access be partitioned.

## Purpose — why folders matter

Folders are not incidental packaging. They serve **two purposes at once**:

- **Navigation.** They sort content and make it easy to discover. A good tree is a table of
  contents you can walk.
- **Partitioning** (*cloisonnement*). A subtree is a natural unit of access: read or write
  **roles** can be granted per subtree. Who may write where follows the folder boundaries.

Because a folder carries both meanings simultaneously, its shape is not a matter of taste.
The axioms below keep navigation legible and partitioning meaningful.

## Axioms

### A1 — A folder has exactly one of three functions

Every folder is, by intent, one of:

1. **Structural** — it *holds a tree* (a listing of sub-folders). Its job is to organize.
2. **Notional** — it *carries a notion*. Its job is to hold the documents of one topic.
3. **Application** — it is *used by applications* (tools), not authored by hand.

The function is a deliberate choice, and it MUST be respected by the rules that follow.

### A2 — A structural folder carries only its README at its root

A structural folder MUST NOT contain **content documents** at its root. It MUST carry a single
**[descriptor](#the-structural-folder-descriptor)** — its **`README.md`**, whose frontmatter
carries the structured meta. Any documentation beyond the README's own body MUST be placed
inside a sub-folder — which forces that sub-folder into the *notional* role (A1).

*Rationale.* This keeps navigation simple, prevents a structural folder from silting up with
loose documents, and makes the structural/notional boundary explicit rather than accidental.

### A3 — A listing MUST NOT exceed 255 sub-folders

Any single folder listing MUST contain at most **255** sub-folders. Exceeding that ceiling is
the signal that **a categorization level is missing** — the contents need to be grouped one
level deeper, not piled flat. See [Tree scoring](#tree-scoring) for the graded thresholds
(ok → fail) and the balance guidance behind this ceiling.

### A4 — A notional folder has a single level of thematic sub-folders

A notional folder:

- MAY carry documents of **any type** (Markdown, JSON, assets) directly at its root.
- Its sub-folders are **thematic**, and there is **exactly one** level of them. A thematic
  sub-folder holds documents, not further sub-folders.

If a notional folder's thematic sub-folders would exceed the A3 ceiling, it has outgrown a
single notion: **promote it to a structural folder** whose children are categorized. A4 and
A3 meet here — depth is added by re-typing the folder, never by nesting a second thematic
level.

### A5 — Application folders are prefixed with `_`

A folder used by an application MUST be prefixed with an underscore (`_`). This:

- **avoids collision** with a thematic folder of the same name (`agents/` vs `_agents/`),
- makes application folders **immediately identifiable**,
- **sorts them first** in a listing, keeping tool-owned state out of the way of content.

Some application folders hold **runtime/system state** that evolves continuously — the
messaging, queue, memory, and session stores (see [Agent collaboration](../agents/agent-collaboration.md#system-folders)).
These are **not versioned** (kept out of source control).

## The structural-folder descriptor

A structural folder carries **no content documents** at its root (A2), but it still needs annex
information and a description. Both live in its **descriptor**: a single, **mandatory
`README.md`** at its root, whose **frontmatter** carries the structured meta and whose **body**
is the human description. SpecLore deliberately uses **one format per function** — the README is
the *only* descriptor (there is no `meta.json`). The body MAY be empty: a frontmatter-only
`README.md` is valid.

> **Dogfooding note.** By convention **every** folder — structural *and* notional — carries a
> `README.md`. It is *mandatory* for structural folders (this rule); for notional folders it is
> the same convention, and may be frontmatter-only.

The founding principle:

> A structural folder does **not** carry its function in its **name** — it carries it in its
> **`README.md`**. Folders may therefore be named however users are used to naming them (`adr/`
> or `decisions/`, `tasks/` or `backlog/`); the semantics come from the descriptor's `usage`.

### Keys

The `README.md` frontmatter (YAML) currently defines these keys. The set is **not exhaustive**
and MAY evolve with system needs.

| Key       | Meaning |
| --------- | ------- |
| `guid`    | The folder's stable identity as an entity (see [References](references.md)). |
| `created` | Creation timestamp. |
| `author`  | Who created it — a GitHub name, an agent, or a terminal profile. |
| `usage`   | The folder's **function** (authoritative — see [Usages](#structural-folder-usages)). |
| `index`   | An auto-incremented integer used to mint new sub-folder IDs **incrementally**. |

Example — the folder's `README.md`:

```markdown
---
guid: f3a9…
created: <timestamp>
author: <github-name | agent | terminal-profile>
usage: tasks
index: 2
---

# Tasks

The open work for this project…
```

A structural folder is an **entity**: its `guid` makes it referenceable and lets it be moved
or renamed without breaking relations (see [References](references.md)).

`index` is the atomic counter behind incremental sub-folders: creating a new task reads and
increments it, yielding `0001-…`, `0002-…`, and so on without collision.

## Structural folder usages

`usage` names what a structural folder is for. Two kinds of structural folder exist, by what
their sub-content is:

- **Composite** — its children are themselves *structural* folders.
- **Collection** — its children are *notional* leaves (one notion each).

Recognized usages for **project tracking** (a starter set — the full, extensible catalog of
project-management notions lives in [Project management](../project-management/project-management.md)):

| `usage`      | Kind       | Sub-content (the children)                     | `index` |
| ------------ | ---------- | ---------------------------------------------- | ------- |
| `project`    | Composite  | structural folders: `milestones`, `tasks`, `adr` (+ `_` app folders) | — |
| `milestones` | Collection | notional milestone leaves                      | optional |
| `tasks`      | Collection | notional task leaves (incremental IDs)         | yes |
| `adr`        | Collection | notional decision leaves (ADR, incremental IDs)| yes |

The **structural sub-contents** are thus fully described by the *kind*: a `project` holds
structure (other structural folders); a `tasks`/`adr`/`milestones` holds a collection of
notional leaves. A notional leaf carries one notion's documents (e.g. a single `task.md`
whose properties live in its frontmatter — no sidecar JSON) and follows A4.

## Choosing a form: referential, document, or folder

Deciding the physical form of a piece of information is a modeling act. SpecLore gives the
**questions**, not a frozen answer — the point is to provide tools to build a structure, not
to impose one.

**Q1 — Does the element have properties?**
- **No** → it lives as an entry in a **JSON referential** (a shared list file, e.g.
  `tags.json`). No folder, no document of its own.
- **Yes** → ask **Q2**.

**Q2 — Does the element contain a list of information?**
- **No** → it is a **Markdown document** (its properties in its frontmatter).
- **Yes** → it is a **folder**, and Q1's properties are carried by its **descriptor** (its
  `README.md` frontmatter).

When Q2 is **yes**, continue:

**Q3 — Can the element be divided into sub-parts?**
- **No** → nothing to add.
- **Yes** → add a **classification folder** (structural), with its own descriptor.

**Q4 — One Markdown, or a folder of several Markdowns?**
Both are valid: a single `tasks.md`, or a `tasks/` folder holding `{T01.md, T02.md, …}`.
- Prefer a **folder + list** when the content has meaningful textual properties, evolves, and
  grows (items get added over time).
- Prefer an **item inside a Markdown** when it is just a sentence with a done/undone checkbox —
  it belongs *inside* its parent document, not as its own file.

So a `sprint` or `backlog` that has properties (status, due date, …) is either a **folder**
(with its descriptor) or a **Markdown with frontmatter**. Beyond frontmatter, a Markdown may
also hold lists whose items carry properties or references (Markdown structure: to be fixed).

## A well-balanced tree

The tree must be not only correct (axioms) but **well-classified**. A good classification has
the **fewest levels possible**, with a **balanced number of records at each level**.

- **Ideal load: 5–15 records per folder** — enough to justify a level, few enough to scan.
- **Too sparse & deep is as bad as flat & huge.** 1–2 records nested three levels deep is
  poorly weighted; 50 records in one listing is hard to navigate. A **human** reads and walks
  the tree — excess depth *and* excess width both slow discovery and search.
- **Grow by adding a classification level, not by overflowing.** When a listing outgrows the
  balance band, insert an intermediate classification folder (each with its own descriptor).

Worked example — features in a long-lived project (2–3/day → 500+ features):

```
features/                              # flat: 500+ leaves — breaks A3, unnavigable
features/ epic-XXX/ feat-XXX/          # add an epic level
features/ domain-XXX/ epic-XXX/ feat-XXX/   # ERP-scale: add a domain level above epics
```

Each added level is chosen to keep every listing inside the balance band.

## Tree scoring

The same indications are **scoring criteria**, consumed by the quality & coherence analyzer
([References §7](references.md#7-system-operations)) to grade a tree and, for example, gate
commits.

**Records per folder (listing width):**

| Records in a listing | Score |
| -------------------- | ----- |
| ≤ 15                 | ok |
| 16 – 50              | warning |
| 51 – 100             | alert |
| 101 – 255            | danger |
| ≥ 256                | fail (breaches [A3](#a3--a-listing-must-not-exceed-255-sub-folders)) |

**Parent / child weighting (balance):** flag imbalance when a **parent has fewer than 5
children** while a **child holds more than 15 nodes** — the level is not distributing its
load, and should be rebalanced (remove a needless level, or split an overfull one).

## Proposed structure — project tracking

```
project/                     # STRUCTURAL · usage=project (composite)
├── README.md                #   descriptor: frontmatter (guid, usage, index…) + description
├── _refs/                   # APPLICATION (A5) — the reference store (see references.md)
├── _runtime/                # APPLICATION (A5) — tool-owned, sorted first
│
├── milestones/              # STRUCTURAL · usage=milestones (collection)
│   ├── README.md            #   descriptor
│   └── 2026-q3-launch/      # NOTIONAL leaf — one milestone
│       └── milestone.md     #   all properties in its frontmatter (+ assets if any)
│
├── tasks/                   # STRUCTURAL · usage=tasks (collection)
│   ├── README.md            #   descriptor; its `index` drives incremental IDs
│   ├── 0001-parser/         # NOTIONAL leaf — one task
│   │   └── task.md          #   properties in frontmatter — no sidecar JSON
│   └── 0002-schema/
│       └── task.md
│
└── adr/                     # STRUCTURAL · usage=adr (collection) — could be named decisions/
    ├── README.md            #   descriptor
    └── 0001-markdown-plus-json/   # NOTIONAL leaf — one decision
        └── decision.md
```

Each leaf is a **folder**, not a bare `.md`, because a structural collection root admits only
its descriptor (A2). The leaf folder is the notional home for its document(s); the document
carries its own properties in frontmatter (see [Interactive documents](../documents/interactive-documents.md)).

### Bad example — what A2 forbids

```
tasks/                       # ✗ a structural folder (it holds a listing) …
├── tasks.md                 # ✗ … with a content document at its root — violates A2
├── 0001-parser/
└── 0002-schema/
```

`tasks.md` is a **content document**, not the folder's descriptor, so it does not belong at a
structural root. A **`README.md`** (frontmatter + overview) in its place *is* the descriptor
and would be correct; any further content must move into a notional sub-folder.

### How the axioms show up here

- **A1 / three functions.** `project`, `milestones`, `tasks`, `adr` are structural;
  `_runtime/` is application; each `0001-…/` leaf is notional.
- **A2.** Every structural root carries only its **descriptor** — a `README.md` — no other
  content documents; those live only in notional leaves.
- **A3.** If `tasks/` would exceed 255 leaves, it is regrouped one level deeper (e.g.
  `tasks/<area>/…`), turning `tasks/` into a composite structural folder.
- **A4.** Each leaf holds its documents flat, with at most one level of thematic sub-folders.
- **A5.** `_runtime/` is tool-owned, obvious, and listed first.

### Partitioning it enables

The same boundaries define read/write **roles**:

| Subtree        | Pilot | Agents | Tool       |
| -------------- | ----- | ------ | ---------- |
| `_runtime/`    | read  | read   | read/write |
| `adr/`         | write | read   | read       |
| `milestones/`  | write | read   | read       |
| `tasks/`       | read  | write  | read       |

*(Illustrative — the role model is refined in [Concurrent work](../agents/concurrent-work.md).)*

## Related

- Schemas: [`../schemas/`](../../schemas/)
- Conformance: [`../conformance/`](../../conformance/)
- Examples: [`../examples/`](../../examples/)
