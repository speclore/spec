# Entities & references — the relational layer

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

**Part of:** [Tool substrate](tool-substrate.md)
**Primary actors:** Tool, Agents, Pilot
**Needs addressed:** relations that survive moves and renames; reciprocity that stays
consistent; the ability to evolve references without leaving orphans or incoherence.

SpecLore is a **relational system**, in the spirit of a database. Two entities are linked by a
relation that has a **cardinality** — one-to-one, one-to-many, or many-to-many — and every
relation is **reciprocal**: it exists on both sides at once.

## 1. Entities are immutable — the GUID

An **entity** is a document (a Markdown file) or a **structural folder**. An entity is
*immutable in identity*: whether it is moved or renamed, it remains the same entity. Identity
is carried by a **GUID**, which references a path:

- A document carries its `guid` in its **frontmatter**; a structural folder carries it in its
  **descriptor** (its `README.md` frontmatter — see [Folder tree](folder-tree.md)).
- The `guid` is the stable handle; the **path** is a mutable attribute of the entity.

> This immutability can only hold if allocation and manipulation of a node go through the
> **system**. That is hard to guarantee against out-of-band edits — which is exactly why the
> **scan** and **watch** operations (§7) exist: to reconcile reality back to the model.

## 2. Resolving a guid → path

The mapping **`guid` → `path`** is materialized in the `_refs` store (§3) — each record
carries a `path` — and **nowhere else**. Per the [no-redundancy principle](../foundations/foundations.md#3-principles)
we keep **one** materialization: to resolve a guid, compute its shard location directly and
read that single record. One disk read, no scan.

A runtime **MAY** cache `guid → path` in memory for repeated lookups. That cache is
**derived, non-authoritative, and rebuilt from `_refs`** — never persisted as a second index.

**Why not also keep a persistent global hashmap?** It would be a second derived copy of the
same mapping: pure drift risk (hashmap vs `_refs`) for no gain. A per-guid lookup is already a
direct O(1) read; the only thing a hashmap accelerates — steady-state random lookups — the
in-memory cache already covers, without persistence. And a **scan** must read every entity
regardless, so a persistent index saves nothing there either. For ~20k entities and dozens of
checks, direct reads (or a single cache build) are cheap. The authoritative facts live once —
`guid` in the document frontmatter or the folder descriptor, `path` in the filesystem — and
`_refs` is the one derived index over them.

Maintenance rules, applied per entity during a **scan** (the authoritative side always wins):

- If the entity **declares a `guid`** → verify its `_refs` record and **correct the path**.
- If the entity **has no `guid`** → **create** one and register its record.
- If a **`_refs` record points at a path that no longer exists** → **remove** the record.

## 3. The `_refs` store

The project MUST contain a `_refs` **application folder** (prefixed `_`, per A5). It is the
**one derived index** (§2): one JSON record per entity, holding the entity's `path` and its
**reciprocal** references. It is rebuildable in full by a scan.

**GUID format.** A guid is a **UUID v4** (hexadecimal).

**Sharding.** Records are sharded across **two levels**, by the **first two** hex characters
then the **next two**:

```
guid "1f2e3d4c-…"  →  _refs/1f/2e/1f2e3d4c-….json
```

This gives **256 × 256 = 65 536** leaf folders, and at ~256 records per leaf about **16.7M**
entities (256³) — a *soft* ceiling, since a folder holding ~1000 files is not a problem. The
256-way fan-out is the bounded-listing rule for `_refs`; [A3](folder-tree.md#a3--a-listing-must-not-exceed-255-sub-folders)'s
255 governs *authored* content folders, not this machine-managed shard.

**Record content — reciprocity.** A record lists, per relation property, the guids on the
**other side** of the relation. Example — *alice references bob as a friend* (`ami`);
`alice`/`bob` stand in for real UUIDs:

```json
// _refs/<shard>/<bob-guid>.json
{
  "guid": "<bob-guid>",
  "path": "project/people/0007-bob/bob.md",
  "refs": { "ami": ["<alice-guid>"] }
}
```

The forward declaration (`alice.ami = [bob]`) lives **once**, in alice's frontmatter; the
record above is the maintained **reverse** side — not a duplicate of the fact, but the
reverse index needed for cascade. So mutations resolve deterministically:

- **Delete `alice`** → remove `alice` from bob's `ami` property.
- **Delete `bob`** → empty the `ami` property in `alice`.

Then bob's `_refs` record is removed and any cache invalidated.

## 4. Cardinality & reciprocity

Every relation declares its **cardinality** (1:1, 1:N, N:N) and its **reciprocal** side, so
the system maintains both ends together:

- **1:1** — each side holds at most one guid.
- **1:N** — one side holds many, the other holds one (e.g. `children` ↔ `parent`).
- **N:N** — both sides hold many (e.g. `ami` ↔ `ami`, symmetric).

*(The catalog of relation types and their exact declaration is to be fixed.)*

## 5. Reference strength

A reference has one of three strengths, by how it points at its target:

| Strength     | Points via                      | Survives move/rename? |
| ------------ | ------------------------------- | --------------------- |
| **Strong**   | a **guid** — `ref://<guid>`     | yes                   |
| **Relative** | a **relative path**             | only within its subtree |
| **Weak**     | an **absolute path**            | no                    |

**The `ref://` protocol.** An internal link — from one entity to another — MUST be written as
`ref://<guid>`, not as a path. The guid resolves to the target's current location through the
`_refs` store (§2), so the link keeps pointing at the same entity across any move or rename.
Links to things *outside* the system (a web URL) keep their normal scheme (`https://…`).

Only **strong** references are durable. The **scan** exists in part to find **relative** and
**weak** references (path-based links) and **rewrite them to strong** `ref://<guid>` links.

## 6. Mutations go through the system

Allocating an entity and assigning its properties/relations **SHOULD** go through a system
tool rather than direct hand-editing. Direct edits cannot, on their own, keep the `_refs`
index and reciprocity coherent. When they happen anyway, **scan** and **watch** (§7)
reconcile them.

## 7. System operations

Coherence is guaranteed not by hope but by tooling, of four natures:

1. **AI tool.** An interface agents call to create nodes and set properties/relations —
   simplifying management and giving the agent **introspection** into the graph.
2. **Scan.** A batch pass that (re)builds the `_refs` index (paths and reciprocal edges),
   assigns missing guids, prunes stale records, and promotes relative/weak references to
   strong. Also the way to **import an existing folder**.
3. **Watch.** A live process that reacts to manual manipulations (by human or agent) in real
   time, keeping `_refs` consistent as files change.
4. **Quality & coherence analyzer.** A validator — e.g. to **gate commits** — that reports
   dangling references, non-strong references, and reciprocity breaks.

Their shared purpose is to make an information system simple to manage and **coherent by
construction**, so that references can evolve without creating omissions or inconsistencies.

## Related

- Schemas: [`../schemas/`](../../schemas/)
- Conformance: [`../conformance/`](../../conformance/)
- Examples: [`../examples/`](../../examples/)
