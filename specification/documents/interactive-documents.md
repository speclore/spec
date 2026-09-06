# Domain — Interactive documents

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

**Primary actors:** Pilot
**Needs addressed:** The pilot must instruct the system and consult its state through
structure a program can parse and **render interactively**, rather than reading raw prose.

## Purpose

This domain defines the structured Markdown format a SpecLore document uses. A document must
be readable as plain text yet parseable into a **structured object** — so a tool can render it
as interface, and edit it without losing anything.

## Anatomy of a document

A document has two parts:

- **Frontmatter** — identification and meta properties.
- **Content** — the body: an optional header region, a title, and sections.

```
---
frontmatter            # identity + meta properties
---

<header region>        # structural blocks (e.g. a versions table) — before the title

# Title

## Section …           # content
```

## The self-contained rule

A SpecLore document declares **all of its properties in itself** — its frontmatter or its own
body. Using a companion or sidecar JSON to complement a document is **forbidden** (MUST NOT):
a document is one file, so it can be **moved, copied, or renamed as a unit** without losing
metadata.

> This is distinct from a structural folder's **descriptor** (its `README.md`, see
> [Folder tree](../substrate/folder-tree.md)), which describes the *folder*, not a content document.

## Frontmatter or body?

Where a property lives is decided by three questions:

**Q1 — Is it an immutable datum identifying the document?**
- **Yes** → **frontmatter** (e.g. `guid`, `author`, creation date, `reference`).
- **No** (it evolves — title, status, classification) → **Q2**.

**Q2 — Does the property classify the document?**
- **Yes** → **frontmatter** (e.g. `tags`, `status`, `type`).
- **No** → **Q3**.

**Q3 — Is it a structuring property of the simple system?**
- **Yes** → **frontmatter** (e.g. `relations`, `link`, `version`).
- **No** → the **body** (e.g. change tracking, a list of points to validate).

## The structured document — lossless round-trip

Markdown is already structured. SpecLore treats a conforming document as a **structured
object**: it can be **parsed** from the file, interpreted or rendered, **modified in memory**,
and **serialized back with no loss** of content or formatting. The object and its
serialization are linked — evolving the data evolves the serialization, and vice-versa.

> **Requirement.** A conforming parser MUST round-trip a spec-formatted document: read it into
> its object, write it back, and lose nothing. This is what makes deterministic identification
> (below) and the conflict policy non-negotiable.

The mechanics — the grammar baseline, the precise definition of "lossless", and the canonical
serialization form — are defined in [Document parsing & serialization](document-parsing.md).

Recognized body constructs (the vocabulary a parser understands):

| Construct | Role |
| --------- | ---- |
| Headings | Title, sections, sub-sections. |
| Tables | Columns = properties, rows = entries/values. |
| Lists | Classic bullet/ordered lists. |
| Task lists | Checkable items (done / not done). |
| References / links | Pointers to other entities (`ref://<guid>`) or external URLs. |
| Typed blocks | Structured, typed content — `code`, `mermaid`. |

A **body-backed property** maps to a construct. Example: the document exposes `versions[]`,
serialized as a table (`version | author | date | comment`) in the header region; adding an
entry adds a row.

**Internal links use `ref://<guid>`.** A link to another entity MUST point via its guid
(`ref://<guid>`), never a relative path, so it survives moves and renames; only external links
keep a normal URL scheme. See [References](../substrate/references.md#5-reference-strength).

## The document object model

A parsed document is a **tree** — a DOM — mirroring the document's structure: sections nest as
nodes, and structural constructs (task lists, tables) are their leaves. The parser extracts
named top-level elements — currently **`title`**, **`versions`**, and **`tasks`**
(extensible).

### The item — a uniform, recursive node

Every node in the tree is an **item** with the same shape:

| Field | Meaning |
| ----- | ------- |
| `parent` | The parent node. |
| `title` | The item's label. |
| `description` | Its descriptive text. |
| `isDone` | Whether it is complete. |
| `items` | Its child items (the sub-tree). |
| `progress` | If `items` is non-empty, the children's `progress` averaged (a simple, unweighted mean for now); otherwise `isDone ? 1 : 0`. |

Because the shape is uniform, sections, lists, and individual entries are all items, and
`progress` rolls up the tree automatically.

### Task lists

A checkbox list:

```
- [x] todo 1 : description
- [ ] todo 2
```

Each line is an item: `isDone` comes from `[x]` / `[ ]`, `title` is the text before the
**first** `:`, `description` the text after that first `:` (optional — a `:` inside the title
does not split again), nested checkboxes become `items`, and `progress` follows the rule
above.

Within a section, the **parent is the section**: the list-level item takes the **parent's
title** (the section heading), its **description** is the paragraph before the list, and its
**items** are the checkbox lines.

### Tables

A table is handled the same way — an **array of structured items** exposed under `items`
(columns are the item's properties, each row an item). `versions` is exactly this: a table
whose rows are items.

## Identifying a structural block — position & role, not duck typing

Identifying a block by its *shape alone* (duck typing) is **rejected**: a block may have the
shape yet be meant for another purpose. Duck typing is lenient but error-prone, and a
framework that guarantees results cannot rely on it. A structural block is identified by a
**defined, unequivocal role** and a **respected structure**, anchored by **position**:

- Structural blocks live in the **header region** — **before** the `# Title` and the content
  sections. Position is the primary identifying condition.
- Because the location is defined, **creating** a missing block is simple: inject it at its
  defined place.

*(The exact per-block role marker is to be fixed; it must make the role unequivocal, not
inferred from shape.)*

## Conflict policy: fallback and alerts

When a block expected once appears several times (e.g. one versions table expected, three
found), SpecLore does **not**:

- **refuse parsing** — that degrades everything (though the validation **lint** MAY refuse the
  *format*);
- **merge** — exposing all in one property loses formatting, and writing back would collapse
  three tables into one (**forbidden**);
- **empty the property** — that loses information.

Instead it **falls back to displaying** the information (e.g. the first block) **and raises an
alert on the document**. Rationale: the pilot, short on time, still sees data; the agents are
notified by the **lint** and can fix or escalate — driven by the lint result, not by missing
data. Alerts are **derived** (surfaced by the parser/analyzer at render time), not stored.

**This policy applies to every structural part.**

## Related

- Document type structures: [Document types](document-types.md)
- Schemas: [`../schemas/`](../../schemas/)
- Conformance: [`../conformance/`](../../conformance/)
- Examples: [`../examples/`](../../examples/)
