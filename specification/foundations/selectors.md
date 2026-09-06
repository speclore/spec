# Selectors

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

**Cross-cutting** — used by [Agent orchestration](../agents/agent-orchestration.md) (hooks & workflows),
[References](../substrate/references.md) and [Project management](../project-management/project-management.md) (views), and
[Document parsing](../documents/document-parsing.md) (node addressing).
**Primary actors:** Tool, Agents

A **selector** is a **CSS-like** matcher over the entity tree — and, extending inward, over a
document's DOM. It reuses CSS mechanics so it is familiar, expressive, and open-ended. It
answers "`changed` is too broad": wherever something would act on everything, it carries a
selector and acts on a precise set.

## The mapping to CSS

| SpecLore | CSS analogue | Matches |
| -------- | ------------ | ------- |
| `#<guid>` | `#id` | one entity by **identity** (guid). |
| `.<kind>` | `.class` | entities by **kind** — a folder's `usage`, a document's `type`. |
| `<name>` | tag | entities by **name** (a path segment). |
| `*` | `*` | any entity (universal). |
| `[prop op value]` | attribute | a **property filter** — over a folder's descriptor or a document's frontmatter. Operators: `=`, `!=`, `>`, `<`, `>=`, `<=`, … |
| ` ` (space) | descendant | anywhere below. |
| `>` | child | a direct child. |

Compounds with no space **intersect** (`.feature[priority>1]` = kind `feature` **and**
`priority > 1`); `,` **unions**.

## Worked example

```
.project > milestones > *[state=planned] .feature[priority>1]
```

reads: any entity of kind **project**, with a direct child **milestones**, whose direct child
is **any** entity with `state = planned`, which **contains** (at any depth) an entity of kind
**feature** with `priority > 1`.

## What it ranges over

- **Entity level** — folders and documents; the tree is the [folder tree](../substrate/folder-tree.md), so
  combinators (`>`, descendant) express containment.
- **Node level** — the same language descends into a document's [DOM](../documents/interactive-documents.md#the-document-object-model):
  sections and items are elements too (e.g. `.task .item[isDone=false]`). This is the **node
  addressing** the parser layer needs.
- **Relations** — non-tree links (a feature's sprint, a dependency) are matched by property
  filters over relation properties, whose values are guids, resolved through `_refs`
  ([References](../substrate/references.md)).

## Two operations the tooling MUST support

1. **Query** — run a selector to **retrieve the matching set** (scan / collect).
2. **Check** — test whether **a given entity matches** a selector (validation).

Both are required. They are the **feedback loop agents need when authoring rules** (hook
events, workflow triggers, views): an agent writes a selector and immediately sees the list it
returns, or whether a specific element matches — so a rule can be verified before it is relied
on.

## Event selectors

An **event selector** is an event **kind** applied to the entities a selector matches:

- **kinds:** `created`, `updated`, `deleted`, `moved`, `reference-broken`, `commit`, `scan`,
  `message` (extensible).
- **narrowing:** for `updated`, name the changed **property** or relation — e.g. an `updated`
  event on `.feature[state]` fires only when a feature's `state` changes, not on any change.

## Scope of this document

SpecLore fixes the **model** (CSS-like `#id` / `.class` / tag / `[attr]` / combinators) and the
**two operations**. The precise grammar reuses CSS conventions; the selector **tester** is a
tooling requirement, not an engine re-invented here.

## Related

- Schemas: [`../schemas/`](../../schemas/)
- Conformance: [`../conformance/`](../../conformance/)
- Examples: [`../examples/`](../../examples/)
