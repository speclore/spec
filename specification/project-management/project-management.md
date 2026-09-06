# Project management — the notion toolbox

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

**Builds on:** [Folder tree](../substrate/folder-tree.md), [Interactive documents](../documents/interactive-documents.md)
**Primary actors:** Pilot, Agents, Tool

SpecLore is a **toolbox, not a methodology**. This document catalogs the *notions* of software
project management as an **extensible palette**. A method — Scrum, Kanban, Waterfall, SAFe,
XP — is a *selection and arrangement* of these notions; SpecLore imposes none, and a project
uses only the notions it needs.

## The three layers — do not confuse them

Evaluating the domain, the single most important finding is that project-management concepts
fall into three layers that must be modeled differently:

1. **Notions (stored).** Concrete units — a feature, a task, a bug, a decision — each with
   exactly **one primary home** in a *single* classification tree (A1). The classifying levels
   of that tree (e.g. `domain/`, `epic/`) are **classification folders**, chosen to keep the
   tree balanced (see [Choosing a form](../substrate/folder-tree.md#choosing-a-form-referential-document-or-folder)
   and [A well-balanced tree](../substrate/folder-tree.md#a-well-balanced-tree)). A notion's place in that
   hierarchy *is* its primary categorization — no reference needed for it.
2. **Relations (secondary grouping & links).** Everything *else* a notion belongs to — a
   sprint, a milestone, a backlog position, a dependency — is a **reference**, never a second
   folder home. A feature stays in its home while a sprint *references* it, and the same
   feature can sit in several sprints over its life. The mechanism — guid entities, cardinality
   (1:1 / 1:N / N:N), reciprocity, and reference strength — is defined in
   [References](../substrate/references.md).
3. **Views (rendered).** Board, roadmap, gantt, burndown, dependency graph — **computed** by
   the tool over notions + relations. Renderings, not stored folders.

> Rule of thumb: a notion's **one** home is a folder in the classification tree; **every other
> membership** is a reference; a **display** is a view.

### Primary home vs secondary grouping — features, sprints, milestones

Take **features**. Intuitively one makes `features/` then a sub-folder per feature — fine until
a long-lived project passes 500 features and breaks the
[255 ceiling](../substrate/folder-tree.md#a3--a-listing-must-not-exceed-255-sub-folders). That is the signal
to add classifying levels: `features/epic-XXX/feat-XXX/`, and on a complex product (an ERP)
`features/domain-XXX/epic-XXX/feat-XXX/`. **Epic and domain are classification folders** — the
feature's single home.

A **sprint** or **milestone** is a *secondary grouping*. It has its own properties (status, due
date) and its own evolving content (task breakdown, tracking, what was delivered), so by
[Q1–Q2](../substrate/folder-tree.md#choosing-a-form-referential-document-or-folder) it is a **folder with a
descriptor** — for example:

```
milestones/ M0-BEDROCK/ S1/     # S1 is a sprint inside milestone M0-BEDROCK
```

S1's descriptor (its `README.md`) lists the **feature references** it embarks (guids), not copies of the
features. Because a sprint lives — a feature may be partially implemented, broken into tasks,
tracked, delivered — the sprint owns *that* content itself while the features stay in their home
tree. This is why a sprint is legitimately a folder, yet never *contains* the features.

A **backlog** that is only an ordered list of features with no properties of its own is, by
[Q1](../substrate/folder-tree.md#choosing-a-form-referential-document-or-folder), a **JSON referential** (an
ordered list of references); give it properties and it becomes a folder or a Markdown instead.

## Notion catalog

Legend: **◆ item** (authored leaf) · **▚ grouping** (leaf + membership by reference) ·
**◷ cadence** (time-boxed grouping) · **✎ knowledge** (reference document). Notions you named
are marked ★; the rest are the gaps this evaluation surfaced.

### A. Product & intent — the *why / what*

| Notion | Kind | Note |
| ------ | ---- | ---- |
| vision | ✎ | The product's north star. |
| objective / OKR | ✎ | Measurable goals work rolls up to. |
| roadmap | view/✎ | Time-ordered intent (rendered from milestones/releases). |
| theme / initiative | ▚ | Large grouping above epics (SAFe). |
| epic | classification | Usually a **classification folder** — a feature's home level. |
| feature ★ | ◆/▚ | A shippable capability; may group stories. |
| user story ★ | ◆ | User-centric increment of value. |
| requirement | ◆ | Functional / non-functional; classic for Waterfall. |
| use case | ◆ | Actor–goal interaction. |
| acceptance criteria | (attr/◆) | Conditions of done — usually inside a story. |
| persona | ✎ | Who we build for. |
| hypothesis / experiment | ◆ | Discovery, lean/data-driven work. |

### B. Planning & cadence — the *when*

| Notion | Kind | Note |
| ------ | ---- | ---- |
| milestone | ▚ | A dated checkpoint. |
| phase / stage | ▚ | Waterfall/stage-gate sequencing. |
| release ★ | ▚ | A delivered set of changes; pairs with the changelog. |
| version | (attr) | Usually a property of a release/artifact. |
| sprint / iteration ★ | ◷ | Time-box + membership by reference. |
| increment | ▚ | The sum shippable at a cadence end (Scrum). |
| backlog ★ | view/list | **Ordered selection** of items — not a folder. |
| ceremony / event | ◷ | Planning, review, retro, standup. |
| estimate / story points | (attr) | Sizing property on items. |
| capacity / velocity | (metric) | Planning inputs, derived. |
| dependency | relation | Reference between items (blocks / blocked-by). |

### C. Execution & work items — the *do*

| Notion | Kind | Note |
| ------ | ---- | ---- |
| task | ◆ | Unit of work. |
| subtask | ◆/relation | A task referencing its parent. |
| issue ★ | ◆ | Generic tracked item (tracker-style). |
| bug / defect | ◆ | Adds severity/reproduction. |
| request / change request ★ | ◆ | Inbound ask (feature request, CR). |
| chore | ◆ | Maintenance work, no user value. |
| spike | ◆ | Time-boxed research task. |
| blocker / impediment | ◆/relation | What stops work (Scrum impediment). |

### D. Decisions, risk & knowledge — *RAID + governance*

| Notion | Kind | Note |
| ------ | ---- | ---- |
| decision / ADR | ✎ | Architecture/other decision records. |
| risk | ◆ | Probability × impact (the **R** of RAID). |
| assumption | ◆ | Believed-true, to validate (**A**). |
| constraint | ◆ | Fixed limit on the work. |
| meeting / notes | ✎ | Minutes and outcomes. |
| action item | ◆ | Follow-up owned by someone. |
| retrospective / lesson | ✎ | What to keep/change. |
| glossary / term | ✎ | Shared vocabulary. |
| convention / policy | ✎ | Team rules, definition of done. |
| document / spec / RFC | ✎ | Design and specification artifacts. |
| status report / update | ✎ | Periodic state for the pilot. |

### E. People & organization

| Notion | Kind | Note |
| ------ | ---- | ---- |
| team | ✎/▚ | Who does the work. |
| role / responsibility | (attr) | RACI; often a property. |
| stakeholder | ✎ | Interested/affected party. |
| member / contributor | ✎ | An individual (human or agent). |
| ownership / assignment | (attr) | Who owns an item — a property. |

### F. Quality, delivery & operations

| Notion | Kind | Note |
| ------ | ---- | ---- |
| test / test case / plan | ◆ | Verification units. |
| review / QA | ◆/relation | Gate on an item. |
| environment | ✎ | dev / staging / prod. |
| deployment | ◆ | A delivery act, tied to a release. |
| incident / postmortem | ◆/✎ | Ops failure + analysis. |
| SLO / SLA | ✎ | Operational targets. |
| metric / KPI | (metric) | Derived measures. |
| changelog | list/✎ | The record of shipped change. |

## Attributes (frontmatter, cross-cutting)

These are **not** notions — they are properties carried in a leaf's frontmatter, shared
across many notions: `status` (workflow state), `priority`, `severity`, `labels`/`tags`,
`estimate`, `assignee`/`owner`, `reporter`, `dates` (created / updated / start / due),
`relations` (parent, blocks, relates-to, duplicate-of), `version`.

## Mapping to folder usages

- Each **item** notion becomes a **collection** structural folder (`usage` = the notion,
  e.g. `userstories`, `bugs`, `tasks`), holding one notional leaf per item.
- **Grouping / cadence** notions are also leaves (an epic, a sprint, a release each have
  their own document — goal, dates, notes) but their *membership* is expressed by references
  from the items, not by nesting.
- **Views** are produced by the tool and stored nowhere (or cached under a `_` application
  folder).

The recognized `usage` set in [Folder tree](../substrate/folder-tree.md) is therefore this catalog,
extensible per project.

## Methods as compositions (illustrative)

- **Scrum** — product `backlog` (list) of `user story` + `bug`; `epic`; `sprint` (cadence) →
  `increment`; `release`; ceremonies; `velocity`.
- **Kanban** — a `board` view over `issue`/`task`; WIP limit (policy); continuous flow; no
  sprint.
- **Waterfall** — `phase`s; `requirement`s; `milestone`s; a `gantt` view; `change request`s.
- **SAFe** — `theme`/`initiative` → `epic` → `feature` → `story`; program increment (cadence).

Each method draws from the same palette; SpecLore stores the notions and relations, the tool
renders the method's views.

## Related

- Schemas: [`../schemas/`](../../schemas/)
- Conformance: [`../conformance/`](../../conformance/)
- Examples: [`../examples/`](../../examples/)
