# Changelog

## 0.1.0-core — Unreleased

### Added

- Bounded normative core, ten traceable requirement groups and prioritized release backlog.
- Five versioned schemas: base, document, folder, reference record and diagnostic report.
- Complete project example, positive/negative fixtures, read-only validator and CI.
- Black-box tool acceptance scenarios for preservation, concurrency, deletion and recovery.
- Governance, compatibility policy and release criteria.

### Clarified from the initial unpublished drafts

- Required GUID, author and creation timestamp; one authoritative title location.
- Structural descriptors use YAML-frontmatter README; technical stores use JSON.
- Relation definitions live at the root; inverse edges are derived.
- No-op round trips preserve bytes, including hard-break spaces and ordered-list starts.
  Global canonical formatting is deferred.
- Scan diagnoses by default; repair is an explicit atomic mutation with stale-state checks.
- The example is the conformance target. The editorial corpus, agent drafts and their old
  schemas do not expand core requirements.

The original bedrock was unpublished. No production runtime or integration is certified here.
