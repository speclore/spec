# Domain — Tool substrate

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

**Primary actors:** Tool
**Needs addressed:** Tools need a formal structure to function: a defined folder layout,
frontmatter, and Markdown formatting types, alongside companion **JSON** that lets the tool
communicate with agents and guarantee properties prose cannot — such as the **atomicity** of
an operation (e.g. an increment).

## Purpose

This domain defines and freezes the substrate every other domain sits on: the on-disk
conventions a tool depends on, and the JSON layer that carries state and guarantees. Markdown
holds what humans read; JSON holds what must be exact.

## Structures defined here

- **Folder layout** — the canonical on-disk structure.
- **Frontmatter contract** — the metadata every document carries.
- **Formatting-type registry** — the recognized Markdown constructs and their meaning.
- **Technical JSON** — the conventions for folder metadata and structured state exchange.
- **Relational layer** — entity guids and reciprocal references (see [References](references.md)).
- **Atomic operation** — how operations that must not tear are represented.

## Folder layout

Defined in its own document: **[Folder tree](folder-tree.md)**. It fixes the two purposes of
folders (navigation and partitioning) and the axioms that govern them (folder functions,
README-only structural roots, the 255-folder ceiling, single-level notional sub-folders, and
`_`-prefixed application folders).

## Frontmatter contract

*(Definition to be fixed.)* The metadata contract shared by all documents (cross-references
the frontmatter defined in [Interactive documents](../documents/interactive-documents.md)).

## Formatting-type registry

The recognized body constructs and their **canonical Markdown representation** are defined in
[Document parsing & serialization](../documents/document-parsing.md#4-canonical-form) (the canonical form)
and [Interactive documents](../documents/interactive-documents.md#the-structured-document--lossless-round-trip)
(the construct vocabulary).

## Technical JSON

*(Definition to be fixed; JSON conventions are detailed later.)* JSON here carries
**technical state** — folder metadata and state exchanged between tool and agents. It is
**never** a sidecar for a Markdown document: a document's properties live in its frontmatter
(see [Interactive documents](../documents/interactive-documents.md)). The `_refs` store (see
[References](references.md)) is the first example of technical JSON — a structural folder's
[descriptor](folder-tree.md#the-structural-folder-descriptor), by contrast, is a `README.md`,
not JSON.

## The relational layer

Entities (documents and structural folders) are identified by a stable **`guid`** and linked
by reciprocal **relations**, resolved through the `_refs` store. This is defined in its own
document: **[References](references.md)**.

## Atomic operation

*(Definition to be fixed.)* How an operation that must be atomic (e.g. an increment) is
represented in JSON so no consumer observes a torn state. Chief examples: incrementing a
structural folder's descriptor `index` to mint a new sub-folder ID, and updating a `_refs`
record (see [References](references.md)) without leaving a torn edge.

## Related

- Schemas: [`../schemas/`](../../schemas/)
- Conformance: [`../conformance/`](../../conformance/)
- Examples: [`../examples/`](../../examples/)
