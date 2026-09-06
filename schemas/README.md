# Schemas

The normative **0.1.0-core** schemas use draft 2020-12 and versioned identifiers.
The [core contract](../specification/core/core.md) adds cross-file and behavioral rules.

| Core schema | Validates |
| --- | --- |
| [core/base.schema.json](core/base.schema.json) | Required GUID, type, author, created; shared optional metadata and extensions. |
| [core/document.schema.json](core/document.schema.json) | Document frontmatter; unknown unprefixed keys and duplicate title authority are rejected. |
| [core/folder.schema.json](core/folder.schema.json) | Structural descriptor, title, kind, usage, root catalog/profile and collection index. |
| [core/refs.schema.json](core/refs.schema.json) | A derived reference record. |
| [core/diagnostic.schema.json](core/diagnostic.schema.json) | Derived report and error/valid consistency. |

Base is shared, not a complete artifact validator. Select document or folder, assert date-time
formats, reject duplicate YAML/JSON keys, and apply cross-file checks. YAML follows the core
JSON-compatible scalar rules.

See [validation instructions](../conformance/README.md). Schema IDs resolve locally; HTTPS
identities do not imply that a public website serves them.

## Experimental schemas

The older top-level document.base, agent, message, job and session schemas accompany the
agent-domain drafts. Their unversioned IDs and looser shapes are **not core authority** and
MUST NOT establish core conformance. Their stabilization remains in the
[following backlog](../backlog/README.md).
