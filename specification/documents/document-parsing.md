# Document parsing & serialization

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

**Part of:** [Interactive documents](interactive-documents.md)
**Primary actors:** Tool, Agents
**Needs addressed:** turn a Markdown document into a structured object and back —
deterministically and without losing content. This is the engine the whole domain relies on.

## 1. Two linked representations

A conforming document has **two linked representations** — the serialized content on one side,
the data structure on the other:

- **The syntax tree (AST).** A complete tree of every Markdown block and inline node. It is
  1:1 with the text: nothing in the file is absent from the AST, and nothing in the AST is
  absent from the file. **This layer guarantees the round-trip.**
- **The semantic model.** The DOM of **items** (`title`, `versions`, `tasks`, … with the item
  shape from [Interactive documents](interactive-documents.md#the-document-object-model)). It
  is a **projection** over the AST, for interpretation, rendering, and editing.

They are linked: editing the semantic model **mutates the AST**, and the file is **always
serialized from the AST**. The semantic model never serializes on its own — so it may be a
convenient, deliberately partial *view*, while the AST stays complete and lossless.

## 2. Grammar baseline

Parsing follows **CommonMark**, plus a fixed **GFM** extension set: pipe **tables**, **task
list items**, **strikethrough**, and **autolinks**. Frontmatter is delimited (§4). Anything
outside this grammar is not treated as recognized structure — it is preserved as a **content
node** (§5), never dropped.

## 3. What "lossless" means

Byte-for-byte preservation is neither possible nor desirable: CommonMark has many equivalent
spellings (`*` vs `-` bullets, ATX vs setext headings, spacing, table padding). SpecLore
defines loss against the **object**, not the bytes:

1. **No content loss.** `parse` keeps every block, every inline, and every character of text
   **content**. Cosmetic *scaffolding* — bullet character, heading style, blank-line count,
   table padding — is **not** content.
2. **Canonical & idempotent.** A document is stored in **canonical form** (§4). Serializing
   the object yields canonical text, and `serialize(parse(x))` is **idempotent** — a second
   pass changes nothing.
3. **Round-trip identity.** For a canonical document, `parse` then `serialize` is the identity
   on bytes. For any document, it produces the canonical equivalent with the **same object**.

So the equivalence class is *"same object"*: all spellings that parse to the same AST are
equivalent, and canonicalization elects the single representative. **Ingesting** a hand-written
or imported document normalizes it to canonical form **once** — this is part of what
[scan and watch](../substrate/references.md#7-system-operations) do — after which edits produce stable,
minimal diffs.

> Consistent with the [conflict policy](interactive-documents.md#conflict-policy-fallback-and-alerts):
> canonicalization MAY rewrite *scaffolding*, but MUST NOT drop or merge *content* — three
> tables never become one.

## 4. Canonical form

The serializer emits exactly one spelling per construct:

| Aspect | Canonical rule |
| ------ | -------------- |
| Encoding / lines | UTF-8, LF endings, no trailing spaces, exactly one final newline. |
| Block spacing | Exactly one blank line between blocks; no leading blank line. |
| Headings | ATX (`#`…), one space after the hashes, no closing hashes. |
| Unordered / task lists | `-` marker; tasks as `- [ ] ` / `- [x] `. |
| Ordered lists | `1.` `2.` … renumbered sequentially from 1. |
| Emphasis | `*italic*`, `**bold**`; inline code with the fewest backticks needed. |
| Tables | GFM pipes, leading & trailing `\|`, one space of padding per cell (not width-aligned — stable diffs); alignment row `---` with `:` markers. |
| Links | `[label](target)`; internal links `[label](ref://<guid>)`. |
| Fenced blocks | ```` ``` ```` fences with the language/type info string (`code`, `mermaid`). |

**Frontmatter format.** The frontmatter is **YAML**, delimited by `---` at the very top of the
file. This is a **strict** rule: a JSON frontmatter is **invalid**. The `markdown + JSON`
split runs along a clean line — **YAML lives inside documents and folder descriptors**
(frontmatter), **JSON is for technical/system stores** (the `_refs` store, session/queue
state), and the two never mix.

## 5. Mapping constructs to the object

Every AST node has a place; recognized constructs also project into the semantic model.

| AST node | Semantic projection |
| -------- | ------------------- |
| Frontmatter | Document properties, placed by [Q1–Q3](interactive-documents.md#frontmatter-or-body). |
| Heading | Opens a **section** item; its text is the section `title`. |
| Paragraph before a list | The list item's `description`. |
| Task list | `items` with `isDone` (per the [item rules](interactive-documents.md#task-lists)). |
| Bullet / ordered list | `items` (without `isDone`). |
| Table | An array of items — one per row, columns as properties. |
| Link `ref://<guid>` | A strong [reference](../substrate/references.md#5-reference-strength). |
| Code / mermaid fence, blockquote, image, thematic break, raw HTML, stray paragraph | A **content node** — preserved verbatim in the AST, exposed read-only in the semantic model. |

The **content node** is the escape hatch that makes §3's "no content loss" hold: anything not
a recognized semantic construct is still a node, still round-tripped — just not projected into
item fields.

## 6. What this fixes, and what is next

**Fixed here:** lossless is now defined (§3), the canonical form is fixed (§4), the grammar
baseline is declared (§2), and every construct has a home via the AST + content nodes
(§1, §5).

**Next** (their own sections, once this is agreed):

- **Inline parsing depth** — how a `ref://<guid>` or emphasis *inside* prose is extracted vs.
  kept as text.
- **Typed-section binding** — mapping named sections (a `decision`'s *Context / Decision /
  Consequences*) to typed properties of a [document type](document-types.md).
- **Node addressing** — a selector/path to target one node for in-memory edits (the node-level
  case of [Selectors](../foundations/selectors.md)).
- **Alert & lint structure** — the shape of a derived alert and the lint report.

## Related

- Schemas: [`../schemas/`](../../schemas/)
- Conformance: [`../conformance/`](../../conformance/)
- Examples: [`../examples/`](../../examples/)
