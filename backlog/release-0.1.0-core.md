# 0.1.0-core release evidence

Prepared on 2026-09-06. Status: local release candidate; no tag or publication created.
This records release-package verification, not certification of a production runtime.

## Decisions closed

- Core authority is limited to the core contract and versioned core schemas.
- Author and timezone-qualified creation timestamp are required; document title lives in the
  body, structural-folder title in the descriptor.
- Generic documents and namespaced extensions form the initial palette. Typed task/agent
  schemas and semantic selectors are subsequent work.
- No-op serialization preserves bytes; global Markdown normalization is deferred to avoid
  changing hard breaks, numbered-list starts and opaque content.
- Forward relations are authored once; inverse references are derived. The root declares
  cardinality and deletion policy. Body links restrict deletion.
- Scan is diagnostic by default. Repairs and allocations have atomic visibility, conflict
  checks and recovery obligations; implementation choice is left to the consuming tool.

## Verification

Run from the repository root:

```sh
.venv-core/bin/python conformance/check_release.py
.venv-core/bin/python conformance/validate.py examples/core-project
git diff --check
```

Local environment: Python **3.12.14** in `.venv-core`, created using the desktop's bundled
Python because the host Python lacked ensurepip. Runtime dependencies are pinned in
`conformance/requirements.txt`.

Verified results:

- **9 release checks passed**, including **81 snapshot cases**: 18 valid and 63 invalid,
  each invalid case requiring its expected diagnostic code.
- All five core schemas and the five retained experimental schemas pass schema meta-validation.
- The four-entity example validates with no diagnostics. CLI validation leaves its bytes
  unchanged. CLI error exits and symlink rejection are covered.
- Date-time validation is active, including invalid dates and missing timezones; schema
  identifiers, index paths and report validity are also checked.
- Local publication link targets exist; no unresolved placeholders remain in the core contract.
- `git diff --check` and the whitespace scan of newly added core/tooling files pass.
- Dependency consistency check passes. No network lookup is performed during validation.

The nine operation/reader/editor scenarios were checked for complete inputs/actions/outcomes;
their runtime outcomes were **not executed**, because this repository supplies a specification
and snapshot test tooling, not a candidate runtime. In particular, static success proves no
serializer round trip or crash/atomicity guarantee.

## Publication handoff

The working tree already contained the unpublished corpus before this work. Its existing
content is preserved and the core additions are reviewable together. The maintainer's final
diff review, commit, tag and publication remain the release step. CI is configured but has
not been observed running remotely. No external parser, watcher or transactional tool has
been tested; the nine black-box scenarios document their acceptance obligations.
