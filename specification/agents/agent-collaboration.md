# Domain — Agent collaboration

> Design draft — informative for `0.1.0-core`. The [core contract](../core/core.md)
> is the release authority; requirements below apply only to future profiles once stabilized.

**Primary actors:** Agents
**Needs addressed:** agents must **remember** across sessions, **communicate** with one
another, and **coordinate** who does what and when.

## Purpose

Several agents working together need more than instructions: they need to remember what they
learn, to exchange information, and to pace their work. This domain defines the structures for
**memory**, **communication** (two modes), and **cadence**.

## Structures defined here

- **Memory** — cross-session learning: what an agent records, where, how it is reached, and
  how it compiles back into a prompt.
- **Communication** — two modes: **conversation** (direct) and **message** (asynchronous).
- **Cadence** — parallelism, the **queue** of jobs, and **sessions**.

---

## Memory

**Purpose.** Memory is a **cross-session** store: it holds what an agent *learns* so it is
reusable in later sessions, beyond any single run's context.

### What goes in it — learning, not the base prompt

The base behaviour and mission are carried by the **prompt** and instructions
([Agentic layer](agent-instructions.md)). Memory holds the **additive** part — what a session
*produces* that the initial prompt did not foresee. Its kinds:

| kind | what it captures |
| ---- | ---------------- |
| `rule` | **A reasoning** — the most valuable kind (see below). |
| `decision` | A choice made in a session. |
| `case` | A specific situation encountered, not anticipated. |
| `preference` | A standing preference of the operator/team. |
| `glossary` | A shared term/definition. |
| `fact` | A durable fact worth keeping. |

**Why `rule` matters most.** When the agent asks the operator and, instead of *ruling on the
case*, the operator explains **how to decide**, the answer is no longer a decision — it is a
**reasoning**. A reasoning **generalizes**: it becomes an engine the agent applies to future,
unseen cases. Rules are therefore the kind most worth compiling back into prompts — this is how
an agent genuinely learns rather than memorizing outcomes.

### Memory is transient — promote, don't hoard

Memory is a **transient** state, not a store to accumulate in. If a piece of information is
important enough to keep, it belongs in the **prompt** or the **specs** — and moving memory
items to their right place is **daily work**. Memory is explicitly **not a RAG**: it is a
short-lived learning buffer that *feeds* that promotion, not a queryable knowledge base. This
is why memory is a [non-versioned system store](#system-folders): the durable home of a
learning is the prompt or the specs, not memory itself.

### Runtime-independent location & access

Memory MUST NOT live in an agent runtime's private store. It lives in a **canonical SpecLore
system store** (see [System folders](#system-folders)), so that **a model or a system can be
swapped and still reach the same memory**. Agents MUST reach it through an **abstraction — a
tool or MCP server** ([the AI tool](../substrate/references.md#7-system-operations)), never through
hardcoded paths. Where a runtime ships its own native memory, SpecLore's tool/MCP **invites the
agent to use SpecLore memory instead**. Interchangeability is the goal.

### A memory entry

*(First draft.)* A memory entry is a **Markdown file with frontmatter** (an entity — guid,
frontmatter, body). Proposed frontmatter: `guid`, `type: memory`, `kind` (above), `scope`
(agent-private or project-shared), `tags`, `created`/`author`, `relations`. The body carries the
learned content.

### Memory → system prompt

A selection of entries (via [selectors](../foundations/selectors.md)) is **compiled** into a system prompt and
injected as additive behaviour. **When** this happens is an open architecture choice: at **end
of session**, or on a **temporal trigger** (e.g. nightly — accepting that a learning captured
at night is only restored the next day). Either way it is naturally driven by a
[hook / event](agent-orchestration.md) (`session-end`, a scheduled event).

Per the [no-redundancy principle](../foundations/foundations.md#3-principles), memory is the **single home** of
a learned fact; the compiled prompt is a **derived** view, never a second source of truth.

---

## Communication — two modes

Agents communicate in two distinct modes, and the difference matters:

### Conversation (direct, synchronous)

One agent **invokes** another inline to ask a question or hand off a point. It is **fast** and
lets the caller **continue their current session**.

Example: Alice (developer) needs Bob (product owner) to validate a point left uninstructed in
the specs before she builds it. She states what she is working on and what must be decided.

- If Bob has **free capacity** (see [Cadence](#cadence)) and it is a **simple decision**, the
  invocation becomes a **job** he works on **directly**; his output is **automatically returned
  to Alice** as the reply, and she carries on. (This is the short-circuit: an available agent
  works the request now.)
- If Bob has **no free capacity**, the system answers Alice **synchronously** that Bob is
  **busy — send a message** — *without soliciting Bob* (no job is created for him). The same
  applies when the question needs **spec rework** or an **operator decision**: it cannot be
  answered inline.

Either way, when Bob answers, his **session is stopped and summarized** — that summary *is* the
reply returned to Alice.

### Message (asynchronous)

A mailbox system, email-like. It is **slower**, gives a **quality-guaranteed** answer, and
**requires a new session** to resume the work once the reply arrives.

**The mailbox (folders).** The root marks a *messaging* store; under it, one folder per agent,
each with `sent`, `inbox`, and `trash`. The **`inbox` is FILO**. A mailbox belongs to its
agent, who reads a message when **ready** (see [Cadence](#cadence)).

**Threads (guid-based).** Threading works like email, keyed by **guid**. The flow:

1. Alice sends Bob a message (a file in her `sent`, arriving in Bob's `inbox`).
2. Bob reads it → the message moves to his **`trash`** (consumed to handle Alice's request).
3. If Bob replies in his session, the reply is a **new thread** keyed by **Bob's** message guid
   (a file in his `sent`), carrying a **`reply-to`** with **Alice's** thread guid.
4. When Alice reads Bob's reply, `reply-to` gives her back her **original request** — so she can
   **reload her context**.

**Message structure.** A message is a **Markdown document** (frontmatter + body), frozen by
[`message.schema.json`](../../schemas/message.schema.json). Frontmatter: `guid` (identity **and**
thread anchor), `type: message`, `from` (ref), `to` (ref or ref list), `subject`, optional
`reply-to` (ref — the message being replied to, which chains the thread), `sent`. The **body**
is the message content. A message's **folder** (`inbox` / `sent` / `trash`) *is* its state —
there is no status field.

> The original **request message** is kept **verbatim** — never summarized. Via `reply-to` the
> requester reloads full context in a fresh session, which avoids context overload across
> many-turn exchanges. (A *working session*, by contrast, is stopped and summarized when the
> agent answers — see [From job to session and task](#from-job-to-session-and-task).)

### Choosing a mode

| | Conversation (direct) | Message (async) |
| --- | --- | --- |
| Speed | Fast | Slower |
| Session | Continues the current one | Needs a **new** session to resume |
| Answer | Quick | Quality-guaranteed |
| Use when | Simple, answerable now | Needs work/decisions, or the callee is busy |

---

## Cadence

### Parallelism — an agent property

An agent can process **several jobs in parallel**. **How many** is a **property of the agent**:
more parallelism means more token consumption, so it is left to the **operator's discretion**
(alongside the chosen model, API key, or default effort).

Capacity works in **slots**: while a slot is free the agent is *ready* and pulls the next job
from its queue; when a job **finishes**, its slot frees and the agent takes the next one.
"Being ready" is simply "having a free slot".

### The queue

Each agent has a **queue** — a `queue` folder, with a per-agent sub-folder of `jobs`, where a
**job is a JSON file**:

```
queue/<agent>/<job>.json
```

**Everything becomes a job.** A conversation, a message, a solicitation from a
[hook or workflow](agent-orchestration.md), or a prompt from the operator — all end up
producing a **job** the agent processes. (The one exception is a direct conversation to an
agent with no free capacity: it is bounced synchronously as "busy — send a message" and no job
is created.)

**Job structure.** A job is **technical JSON**, frozen by [`job.schema.json`](../../schemas/job.schema.json).
Key fields: `guid`; `agent` (ref — the owner); `source` (`{ origin: conversation | message |
hook | workflow | prompt, ref? }` — what produced it); `request` (the ask); `status`
(`queued` | `running` | `done` | `failed` | `cancelled`); `created`; optional `priority` and
`by`; and, once running, `session` and `task` (refs).

### From job to session and task

A job the agent takes up needs a **dedicated session** to run, and is tracked by a **task** —
which follows its progress and marks the agent **occupied** on it (a task is the same notion as
in [Project management](../project-management/project-management.md)). When the agent **answers**, its session is
**stopped and summarized**; that summary is the outcome (e.g. the reply to a message).

### Sessions

A running job is bound to a **session**, stored append-only as a single **JSONL** file — one
sub-folder per agent, one file per session:

```
sessions/<agent>/<session-guid>.jsonl
```

Each line is one record, discriminated by `kind`:

- **`header`** (first line) — `guid`, `agent` (ref), `job` (ref), `started`, optional `model`.
- **`event`** (many) — a timestamped entry of the run: a `turn`, a `tool` call, a `message`, a
  `note`. Payloads are open.
- **`summary`** (last line, written when the session is **stopped**) — `ended`, `status`
  (`stopped` | `failed`), and the `outcome` (what the session produced, e.g. the reply returned
  to a caller). This is the summary referenced by [Conversation](#conversation-direct-synchronous)
  and [Message](#message-asynchronous).

Records are frozen by [`session.schema.json`](../../schemas/session.schema.json). A session is
append-only and, being a [system folder](#system-folders), **not versioned**.

### System folders

`queue`, `messaging`, `memory`, and `sessions` are **system folders**: they are runtime state
that evolves continuously and is **not versioned** (kept out of source control). They are
application folders ([prefixed `_`, per A5](../substrate/folder-tree.md#a5--application-folders-are-prefixed-with-_)),
reached through the tool/MCP abstraction rather than by path.

---

## Related

- Agentic definitions & orchestration: [Agentic layer](agent-instructions.md), [Agent orchestration](agent-orchestration.md)
- Selectors: [Selectors](../foundations/selectors.md)
- Schemas: [`../schemas/`](../../schemas/)
- Conformance: [`../conformance/`](../../conformance/)
- Examples: [`../examples/`](../../examples/)
