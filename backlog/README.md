# Release backlog

This is the delivery backlog of the specification, separate from the normative corpus.
Status is evidenced by files and the release check command, not by implementation claims.

## 0.1.0-core

| ID | Priority | Deliverable / acceptance | Depends on | Status |
| --- | --- | --- | --- | --- |
| CORE-01 | P0 | Freeze the core boundary, authority order and explicit deferred capabilities. | — | done — [C01](../specification/core/core.md) |
| CORE-02 | P0 | One document/descriptor contract; required identity, author, timestamps and extension rules agree with schemas. | CORE-01 | done — [schemas](../schemas/README.md) |
| CORE-03 | P0 | Define Markdown preservation, structural role markers, links and diagnostic behavior with edge cases. | CORE-02 | done — [C03/C04/C06](../specification/core/core.md) |
| CORE-04 | P0 | Freeze folder classification, identity, reference catalog, cardinality and reverse index. | CORE-02 | done — [C05–C08](../specification/core/core.md) |
| CORE-05 | P0 | Define atomic mutation, conflict, scan and recovery obligations without choosing a runtime. | CORE-04 | done — [C09 scenarios](../conformance/fixtures/operations.json) |
| CORE-06 | P0 | Supply valid/invalid fixtures, a complete example and repeatable validation with CI. | CORE-03, CORE-05 | done — [conformance](../conformance/README.md) |
| CORE-07 | P1 | Reconcile older drafts, define governance/versioning, record changes and release criteria. | CORE-01 | done — [governance](../governance.md) |
| CORE-08 | P0 | Run the release checks and record evidence and limits; prepare the release handoff. | CORE-06, CORE-07 | done — [evidence](release-0.1.0-core.md) |

The target is a releasable **specification package** named `0.1.0-core`. Building a parser,
MCP server, watcher or IDE is a separate project. Tagging and publishing are release actions,
separate from completing this backlog.

Publication follow-up: review the prepared diff, commit, tag and publish the chosen release
content. This has not been performed. The eight completed items concern the specification
package; runtime implementation and certification remain NEXT-08.

## Following increments (outside core)

| ID | Deliverable / decision still required | Depends on |
| --- | --- | --- |
| NEXT-01 | Typed task/feature/story/bug/decision schemas, section binding, statuses and extension registry. | CORE-02, CORE-03 |
| NEXT-02 | Semantic DOM, progress semantics, stable node addressing and a complete selector grammar/tester. | CORE-03 |
| NEXT-03 | Agent/skill/prompt schemas and deterministic global → project → subtree instruction precedence. | CORE-02 |
| NEXT-04 | Workflow execution state, hook/event schemas, retry, cancellation and loop prevention. | NEXT-02, NEXT-03 |
| NEXT-05 | Memory schema, retention/promotion and compilation timing (session end vs scheduled). | NEXT-03, NEXT-04 |
| NEXT-06 | Message ownership/delivery, queue fairness, job/session lifecycle and crash recovery. | CORE-05, NEXT-03 |
| NEXT-07 | Workspace/branch/merge contracts, access enforcement and conflict representation. | CORE-05 |
| NEXT-08 | Runtime adapters, parser/editor, watcher and independent implementation conformance. | CORE-06 |
| NEXT-09 | Migrate the editorial corpus to a conformant project once publication tooling supports GUID links. | CORE-06 |

Each following item requires its own scope, schema, positive/negative examples and acceptance
criteria before becoming normative. Existing agent and project-management drafts are retained
as design input; their MUST statements do not expand the core profile.
