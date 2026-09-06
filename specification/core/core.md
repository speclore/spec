# Core contract — 0.1.0-core

## 1. Boundary and authority (C01)

The exact profile identifier is `0.1.0-core`. A conformant project MUST declare it as
`speclore` in its root descriptor. This document and the five core schemas listed in
[schemas](../../schemas/README.md) define the profile. Prose defines cross-file and behavior
rules; schemas define field shapes. Both MUST hold. A disagreement is a specification defect,
not permission to select the weaker rule. Fixtures illustrate these rules and cannot override
them. Older domain drafts and worked product-management catalogs are informative for core.

Core has one artifact profile, covering a complete project snapshot. Tools may additionally
claim read support or mutation support; these claims MUST name their capabilities and tested
version. Passing a frontmatter schema alone is not project or tool conformance.

Core does not require a semantic DOM, node editing, selectors, task-specific sections, agents,
skills, workflows, hooks, memory, messaging, scheduling, workspaces or merges. Their follow-up
work is tracked in the [backlog](../../backlog/README.md). A conforming core tool preserves
extension data but need not interpret it. No particular runtime, database, Git layout or UI is
required. This package specifies tools' behavior without shipping those production tools.

## 2. Documents and frontmatter (C02)

Every authored `.md` file inside a project is a document, except a structural descriptor,
which represents its folder. Metadata MUST live in that file's YAML frontmatter. Sidecars
MUST NOT serve as a second authoritative metadata source. Non-Markdown assets are not entities.

Files MUST be UTF-8 without BOM, use LF, start with `---` followed by LF, close the frontmatter
with an unindented `---` line, and end with LF. The frontmatter MUST be a block YAML mapping
with unique string keys and JSON-compatible values. Explicit YAML tags, anchors, aliases,
merge keys, non-finite numbers, multiple YAML documents and top-level JSON/flow mappings are
invalid. Scalars follow JSON typing: only `true`, `false`, `null` and JSON numbers resolve as
non-strings; dates and words such as `yes` remain strings. Strings may be quoted. YAML parser
implementations MUST NOT silently discard duplicate keys.

Required common fields: `guid` (lowercase UUID v4), `type`, non-empty `author` and `created`
(RFC 3339 date-time with timezone). Optional fields: `status`, unique string `tags`, string
`version`, and `relations`. A document's title lives only in its body. Descriptors instead
carry `title` in frontmatter; their body is optional narrative, not another title authority.

The core document type is `document`. Custom types MUST use `x-<name>`; custom metadata keys
MUST use `x-<name>`, with `<name>` matching `[a-z][a-z0-9-]*`. Unknown unprefixed keys are
invalid. Extensions MUST NOT redefine core fields, grant permissions or change core validity.
Core records no per-task workflow meaning for `status`; structured task types are deferred.

## 3. Markdown and preservation (C03)

The body is CommonMark 0.31.2 plus GFM tables, task lists, strikethrough and autolinks.
HTML, images, blockquotes and fenced payloads are content, not executable instructions.
Only top-level Markdown constructs participate in title/role detection. A content document
MUST have exactly one top-level level-one heading; no substantive content precedes it except
the optional versions block. A descriptor MAY have an empty body.

Core's canonical envelope uses the YAML subset above and LF. It deliberately allows multiple
equivalent body spellings. A read/serialize round trip with no edit MUST preserve the whole
valid input byte-for-byte, including comments, hard-break spaces, ordered-list start values,
fence lengths, YAML quotes and unknown content. After an edit, only the targeted ranges and
necessary adjacent delimiters MAY change; unrelated content MUST remain intact. Global
normalization is a separate, explicit operation and is not a condition of core conformance.

This supersedes the draft's lossy whitespace and list-renumbering canonicalizer. Stripping
two trailing spaces changes a hard break; resetting `7.` changes a list's value; fixed triple
backticks can close a payload early. The core contract makes preservation testable without
requiring a new Markdown formatter. Typed DOM projections and node mutation APIs are deferred.

## 4. Structural role and diagnostics (C04)

Core recognizes one optional body-backed property, `versions`, marked by the exact standalone
HTML comment `<!-- speclore:versions -->`, followed by one blank line and a GFM table before
the document title (or at the start of a descriptor body). Its columns, in order, MUST be
`version | author | date | comment`. Each row has four cells; version and author are non-empty,
date is an RFC 3339 date-time, and comment may be empty. Cell values are plain text; table
escaping uses GFM rules. No second frontmatter `versions` field is allowed. `version`, when
present, is the current scalar and is not inferred from historical rows.

A duplicate or misplaced marker, malformed table or invalid metadata makes the artifact
non-conformant. A reader MUST preserve its input, emit a diagnostic and MAY show the first
valid marked block as a fallback. It MUST NOT merge or delete conflicting blocks. An ordinary
unmarked table is ordinary content, even when its columns resemble the versions table.

A diagnostic report follows `diagnostic.schema.json`: profile, `valid` and an array of
`code`, `severity`, project-relative `path`, `message`, optional one-based `line` and `guid`.
`valid` MUST be false exactly when any diagnostic has severity `error`. Diagnostics are
derived output, never mandatory stored document properties. Stable codes are the C identifiers
in this contract; warnings do not make a snapshot invalid.

## 5. Folder tree (C05)

A project root MUST have a `README.md` structural descriptor with `type: folder`,
`usage: project`, `kind: composite`, and the profile identifier. Every structural folder MUST
have exactly that descriptor at its root and no other files. It MAY have application folders.
Its `guid` identifies the folder; the descriptor is not a second entity. The descriptor's
`title` is required. `usage` is a non-empty lowercase name; it describes user-chosen semantics.

`kind: composite` holds structural children; `kind: collection` holds notional children.
Notional folders have no `type: folder` descriptor: their Markdown files are document entities.
They MAY hold assets and at most one level of thematic child folders, with no deeper authored
folders. A notional `README.md`, if present, is an ordinary document. Application folders start
with `_` and are excluded from authored width/depth rules and entity scanning. Their contents
have only the explicitly applicable technical contract (`_refs` below).

An authored folder MUST have at most 255 immediate authored child folders. Application
folders do not count. The 5–15 navigation guidance in the draft is advisory. Files and folders
MUST NOT be symlinks; names MUST NOT start with `.` or contain backslashes or ASCII control characters. Paths are
case-sensitive and relative to the declared project root, without `.` or `..` components.
A case-insensitive host SHOULD diagnose colliding names before import.
Root `.git` and `.gitignore` are administrative exceptions, outside the project artifact;
they are ignored during snapshot validation.

An optional descriptor `index` is a nonnegative integer used only on collections. If it is
used for numeric child names, it is the highest reserved ID, never a child count. Allocation
increments it monotonically in the same mutation as creating the child; gaps are allowed,
reuse is forbidden. Without `index`, naming is user-defined. Reclassification preserves GUIDs.
Numeric child names have the shape `<digits>-<label>`; their numeric values MUST be unique
within the collection and fall within `1..index` when the descriptor has an index.

## 6. Identity and links (C06)

Each entity MUST have a project-unique lowercase UUID v4. Moves and renames preserve it;
copies intended as new entities MUST receive new GUIDs. A scan encountering duplicates MUST
report a conflict and MUST NOT guess which copy is authoritative.

An actual Markdown link to another entity MUST use `ref://<guid>` with no fragment or query.
It MUST resolve within this project. Cross-project entity references are deferred. Local
`#anchor` links are permitted, as are relative links to existing non-entity assets within the
root and external `https`, `http` and `mailto` links. Absolute filesystem paths, entity paths,
unsupported URI schemes and escaping the root are invalid. Readers MUST NOT execute URLs or
raw HTML merely because parsing accepted the content. Code spans, fences and raw HTML are
opaque: text resembling a reference there is not a graph edge. Images use asset/external URLs,
not entity references. Link definitions count only when used by an actual Markdown link.

## 7. Relation definitions and authority (C07)

The root descriptor's optional `relation-types` array declares relation definitions:
`name`, `inverse`, `cardinality` (`1:1`, `1:N`, `N:N`) and `on-delete` (`restrict` or `detach`).
The catalog belongs only to the root. Names and inverse names MUST be unique across the
catalog, except `name == inverse` is allowed only for symmetric `N:N`. `links` is reserved
for body-link backlinks and MUST NOT be a relation name or inverse.

Only `name` is authored in a source entity's `relations`; its value is a strong ref for
`1:1`, a unique array of strong refs for `1:N` or `N:N`. `1:1` limits outgoing and incoming
edges to one. `1:N` permits many outgoing edges but at most one source per target. `N:N`
permits both. Absence means no edges; null and duplicate array members are invalid. An
undeclared relation name is invalid. Self-relations are forbidden.

The inverse is derived in `_refs`, not authored a second time. For symmetric relations either
endpoint may declare the edge, but authoring it at both endpoints is invalid duplication.
The derived index uses the inverse name at the receiving endpoint; bidirectional traversal
combines authored outgoing edges and indexed incoming edges. A body link adds only a `links`
backlink, never an inferred typed relation. Distinct body/typed links to the same target are
allowed because they carry different meaning.

## 8. Reference index (C08)

`_refs` is required in a conformant snapshot and contains exactly one JSON record per entity,
at `_refs/<first-two-guid-hex>/<next-two-guid-hex>/<guid>.json`. Its only fields are `guid`,
`path`, `refs`. A document path is relative to the project root. A folder path names the
folder, with the root represented by the empty string. `refs` maps inverse names (or `links`)
to sorted, unique arrays of source GUIDs, omitting empty arrays. A record without backlinks
has `refs: {}`. JSON uses UTF-8/LF, unique keys and finite JSON values. Object-key order is
not significant. No hidden records or stale records are permitted in `_refs`.

The index MUST equal a full derivation from authored entities and actual Markdown links.
Filesystem locations and frontmatter are authoritative. `_refs` is rebuildable and SHOULD
be excluded from source control in operational projects; checked-in fixture indexes are
snapshots for demonstration. Omitting the index from an export requires rebuilding before
claiming snapshot conformance. In-memory caches are allowed; a second persistent GUID index
is not part of the profile.

## 9. Mutation, scan and recovery (C09)

These are normative obligations of a tool claiming **mutation support**, not requirements
to implement that tool in this specification repository.

- Reads participating in a mutation MUST observe either the complete previous generation or
  the complete committed generation, never a mixture of metadata, child allocation and index.
- A mutation MUST check that its input generation is still current. A stale edit is rejected
  as a conflict; there is no silent last-writer-wins. Locks, transactions or compare-and-swap
  are implementation choices. Merely encoding an operation in JSON guarantees nothing.
- After interruption, recovery MUST expose either the old or the new complete state before
  accepting another mutation. Partially updated `_refs` cannot be treated as valid. Watchers
  coalesce their own writes and publish results only after the commit boundary.
- Deletion MUST inspect incoming body and typed references first. Body links always restrict
  deletion. Typed `restrict` edges reject deletion. With only `detach` incoming edges, removal
  of those forward declarations, outgoing backlinks and the entity/index record is atomic.
  Deleting a subtree applies the same check to outside references to every contained entity.
- Read-only validation never repairs. A scan defaults to diagnosis and a proposed repair.
  Applying repair is an explicit mutation: assign missing GUIDs, rewrite unambiguous entity
  paths and rebuild the index together. Duplicate GUIDs, ambiguous targets, invalid YAML and
  unresolved references stop repair; the source is not silently rewritten or pruned.

The black-box scenarios in [operation fixtures](../../conformance/fixtures/operations.json)
specify inputs, actions and observable outcomes. A tool's conformance report MUST supply
evidence for them; passing the static validator alone does not establish mutation support.

## 10. Release and extensions (C10)

The normative profile is immutable within a published release. The schemas' `$id` values
include `0.1.0-core`; resolution in the test harness is local and never fetches the network.
The release package includes the contract, schemas, criteria, fixtures, example, validation
command and changelog. Full release gates and compatibility rules are in
[governance](../../governance.md). Next increments may add separate profiles; no deferred
capability is implied by the term core.
