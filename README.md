# SpecLore

**A specification for writing specifications — a quality standard for how humans, agents, and
tools work from the same structured source.**

## The pitch

Software is now built by a few humans directing many AI agents through a tool. That
arrangement has three actors, and plain prompts and plain Markdown fail all three:

- **The pilot** — the human — is the bottleneck. Every decision routes through one person who
  must grasp the state of the work and act fast. Markdown reads fine but can't drive an
  interactive interface.
- **The agents** drift. Without a shared, structured frame they get contradictory
  instructions, lose track of each other, and collide editing the same files.
- **The tool** has outgrown the chat window. It's becoming a project manager that
  orchestrates agents and lets the pilot follow along — a role plain text can't support.

SpecLore gives the three a common substrate: **Markdown a program can parse and render
interactively**, and **JSON that lets tools and agents exchange state reliably** (structured
instructions, memory, messaging, and guarantees like atomic operations).

## What this repository defines

A **specification corpus** that **defines and freezes concrete structures** — folder layout,
frontmatter, Markdown formatting types, and technical JSON — shared by humans, agents, and
tools. It is **prescriptive** (it fixes structures and states MUST / SHOULD requirements),
**not** an audit or maturity model, and **not** a reference implementation.

The frozen `0.1.0-core` contract is in [`specification/core/`](specification/core/).
The other domain documents preserve the broader design and follow-up work.

## Repository structure

| Path                        | Purpose                                                              |
| --------------------------- | ------------------------------------------------------------------- |
| `specification/`            | The specification corpus, split by theme (start at its README).     |
| `specification/foundations/` | The socle: actors, needs, principles, and requirement conventions. |
| `schemas/`                  | JSON Schemas that define and validate the machine-readable JSON.     |
| `conformance/`              | Conformance criteria and fixtures a spec must satisfy.              |
| `examples/`                 | Worked examples of SpecLore-conformant specifications.              |
| `governance.md`             | How SpecLore is maintained and how changes are proposed.           |
| `changelog.md`              | The record of changes, by version.                                 |
| `backlog/`                  | Core release work, acceptance evidence and following increments.    |
| `LICENSE`                   | MIT.                                                                |

## Status

**0.1.0-core — release candidate, not yet published.** Documents, folder descriptors, GUIDs,
relations and reference-index contracts have a bounded normative profile, versioned schemas
and executable snapshot fixtures. Agent orchestration, memory and concurrent editing remain
experimental. See the [backlog](backlog/README.md), [release evidence](backlog/release-0.1.0-core.md)
and [validation instructions](conformance/README.md).

## License

[MIT](LICENSE) © 2026 SpecLore
