# Governance

## Responsibilities and decisions

The repository owner is the initial maintainer and release authority. Contributors propose
changes; editors maintain prose/schema/example consistency; reviewers assess normative impact
and test evidence. One person may hold several roles. Adding maintainers requires a recorded
owner decision naming their scope.

A normative proposal records the problem, affected profile/requirement IDs, compatibility
impact, proposed contract and acceptance cases in a pull request or repository decision.
A maintainer explicitly accepts it before release. When no other maintainer is available,
the author records self-review. Unresolved normative objections prevent releasing that change;
the owner decides after recording alternatives and rationale. Silence is not acceptance.
Editorial fixes need a diff and passing checks.

## Change process

1. Record the proposal and target version in the backlog.
2. Update normative prose, schemas, criteria and fixtures together.
3. Run release checks and identify runtime verification limits.
4. Record behavior and compatibility impact in the changelog.
5. The maintainer reviews the exact diff, commits the release content and tags that commit.
   Publication uses immutable tagged content; corrections require a new version.

## Compatibility and versioning

The requested name **0.1.0-core** is a SemVer prerelease of 0.1.0; core identifies the bounded
profile. Further candidates use 0.1.0-core.1, .2, etc. Published tags and schema IDs cannot
be replaced with different content.

Changing accepted artifact shapes, required fields, relation meaning or tool guarantees is
breaking: before 1.0 it requires a new minor version and migration notes; at/after 1.0 it
requires a major version. Compatible optional additions use a minor version. Patches fix
editorial/validator defects without intentionally changing the normative valid set.
Changed schemas receive new versioned IDs. Unknown profiles are rejected, not guessed.

## Core release gates

- [Core contract](specification/core/core.md) has no unresolved normative placeholders.
- Five core schemas, positive/negative fixtures and the example agree.
- The release check command and example validator pass.
- Deferred work is tracked; runtime certification is not implied.
- [Release evidence](backlog/release-0.1.0-core.md) records results and limitations.
- A maintainer reviews, commits and tags the exact content for publication.

Preparing the release package does not itself create a Git tag or publish an artifact.
