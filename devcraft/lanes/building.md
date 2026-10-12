---
lane: building
seat: builder
updated: 2026-10-11
---
# Lane manifest — Builder

Mandatory first read for the [Builder](../bench/builder.md). Entries are title + pointer +
one-line when-to-read — shelf labels, never the books: the content lives in the private
corpus (`../corpus/`, gitignored), so pointers resolve only on a machine that has it
(`manifest-only` grounding otherwise, per the seat preamble). Follow only the pointers
relevant to the slice in hand. Seats stop at `## Reading path`; that section is the owner's.

This shelf is about the how of a slice: small behaviour-preserving moves, code the
Verifier's suite can reach through its seams, safe handling of everything that comes in
from outside, and commits that read and roll back cleanly. Nothing here is about editing a
test: test files are the Verifier's.

## Small steps and named moves

- **Refactoring catalog** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — naming the refactoring in a commit or a preparatory step, so the Planner's audit can check the move.
- **Branch By Abstraction** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — replacing a library, framework or backend in gradual, always-green steps.
- **Parallel Change, aka expand and contract** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — changing a signature, payload or schema that other code depends on.
- **Feature Toggles** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — implementing a flag the plan asks for, with its removal in mind.
- **Continuous Integration** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — landing work in small integrated steps with the suite runnable at every commit group.

## Code the suite can reach

- **Testable code (for the Builder)** — [`testing-on-the-toilet.md`](../corpus/canon/testing-on-the-toilet.md) — structuring code so the Verifier's tests reach it through the plan's seams, never through hooks added for tests.
- **Design for understandability (ch6)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — choosing types and interfaces that make invariants hard to break.
- **Writing code: safe by construction (ch12)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — picking the library or pattern that rules a bug class out instead of guarding against it.
- **Configuration design and best practices** — [`sre-workbook.md`](../corpus/canon/sre-workbook.md) — implementing config defaults and validation.

## Calls that fail

- **Timeouts, retries and backoff with jitter** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — writing any network or subprocess call the plan specifies.
- **Cascading failures and overload** — [`sre-book.md`](../corpus/canon/sre-book.md) — applying the named retry and backoff patterns without amplifying load.
- **Managing load** — [`sre-workbook.md`](../corpus/canon/sre-workbook.md) — code that scales or calls a rate-limited service.
- **A10:2025 Mishandling of Exceptional Conditions** — [`owasp-top-10-2025.md`](../corpus/canon/owasp-top-10-2025.md) — writing error paths: fail closed, never half-done.

## Handling outside input safely

- **Part 1: Index by task** — [`owasp-cheat-sheets.md`](../corpus/canon/owasp-cheat-sheets.md) — the slice touches an area the plan's security section names; find its sheet.
- **Part 2: Distilled checklists for the twelve most relevant sheets** — [`owasp-cheat-sheets.md`](../corpus/canon/owasp-cheat-sheets.md) — any subprocess call, hook payload, CLI argument, JSON body, fetch tool, MCP server code or secret handling.
- **A05:2025 Injection** — [`owasp-top-10-2025.md`](../corpus/canon/owasp-top-10-2025.md) — code that builds a query, a shell command, a template or HTML.
- **The 2025 list, with a Verifier test per entry** — [`cwe-top-25.md`](../corpus/canon/cwe-top-25.md) — checking a slice against the weakness classes the plan lists.
- **PW: Produce Well-Secured Software** — [`nist-ssdf.md`](../corpus/canon/nist-ssdf.md) — naming the secure-coding practice a decision follows in the change note.
- **Concise Guide for Developing More Secure Software** — [`openssf-guides.md`](../corpus/canon/openssf-guides.md) — a slice adds a dependency or touches build tooling.

## Instrumentation the plan asks for

- **Instrumentation and the wide event** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — deciding what to emit and how to shape it.
- **OpenTelemetry: spans, layering, naming, schemas** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — writing instrumentation with OpenTelemetry.
- **Release-time signals: build info, the after-deploy questions, runbooks** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — emitting the fields Release's runbook reads.
- **Sampling** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — a harness emits a lot.
- **Observing LLM apps and agent harnesses** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — code that calls a model.

## Commit groups and the change note

- **Conventional Commits 1.0.0: the message grammar** — [`commit-version-changelog-conventions.md`](../corpus/canon/commit-version-changelog-conventions.md) — writing the message for each commit group in the change note's map (the coordinator makes the commit).
- **Change descriptions (author's guide)** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — writing the change note so it still matches the diff at the release gate.
- **Small changes (author's guide)** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — composing commit groups that each read and roll back on their own.
- **Handling reviewer comments (author's guide)** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — answering the Planner's audit or a gate finding.
- **The one rule about rewriting history** — [`pro-git-and-worktree.md`](../corpus/canon/pro-git-and-worktree.md) — before rebasing the build branch in its own worktree.
- **Worktrees (git-worktree)** — [`pro-git-and-worktree.md`](../corpus/canon/pro-git-and-worktree.md) — working in the build's worktree alongside other checkouts.
- **Version control and branches: trunk, One Version, flags** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — staying on a short-lived branch.

## The Codex run itself

- **AGENTS.md: discovery rules and what to put in it** — [`codex-docs.md`](../corpus/canon/codex-docs.md) — the target repo's `AGENTS.md` is this seat's standing instructions; read it as such.
- **Prompting and best practices for the Builder** — [`codex-docs.md`](../corpus/canon/codex-docs.md) — self-discipline on a long slice: plan, verify, stop.
- **Worktrees** — [`claude-code-docs.md`](../corpus/canon/claude-code-docs.md) — parallel sessions on one repo.

## Audit duty: the release plan and runbook

- **Parallel Change, aka expand and contract** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — checking the migration plan's order against the code you wrote.
- **Build, release, run — and rollback (factor V)** — [`twelve-factor.md`](../corpus/canon/twelve-factor.md) — checking the rollback really returns to the old build.
- **Release-time signals** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — checking that every signal the runbook reads is one the code actually emits.
- **The twelve, in one line each** — [`twelve-factor.md`](../corpus/canon/twelve-factor.md) — checking the release surface lists every config, job and secret name the diff touches.
- **Writing findings: review comments** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — writing a finding Release must act on.

## Book layer

The Builder's primary book is ingested; the other three each earn a pointer row.

- **Fowler, *Refactoring* — cheatsheet** — [`books/refactoring/cheatsheet.md`](../corpus/books/refactoring/cheatsheet.md) — a smell in the code you are about to change: the smell→cure map names the move.
- **Fowler, *Refactoring* — ch. 1, 2** — [`books/refactoring/`](../corpus/books/refactoring/) — the small-step loop, and wearing one hat at a time: refactor first, then change behaviour.
- **Fowler, *Refactoring* — ch. 3** — [`books/refactoring/`](../corpus/books/refactoring/) — reading the code for smells before choosing a move.
- **Fowler, *Refactoring* — ch. 5–12** — [`books/refactoring/`](../corpus/books/refactoring/) — applying a named move; find it by its name (or its 1st-edition alias) in the topic index.
- **Ousterhout, *A Philosophy of Software Design* — ch. 6, 8–10, 12–18** — [`books/a-philosophy-of-software-design/`](../corpus/books/a-philosophy-of-software-design/) — shaping an interface, pulling complexity down, comments and naming, keeping code obvious.
- **Khorikov, *Unit Testing* — ch. 3, 5–11** — [`books/unit-testing/`](../corpus/books/unit-testing/) — code shaped for testing: an observable-behaviour API, command-query separation, a pure decision core, adapters, and no hooks added for tests.
- **Nygard, *Release It!* — ch. 4, 5, 7, 8, 11, 13, 16** — [`books/release-it/`](../corpus/books/release-it/) — timeouts, circuit breakers, bounded pools, injection and secrets, health-check fields.

Read the corpus honestly: this is the weakest ingest. The capture lost **every ASCII minus
sign**, so minus operators, decrements and negative
numbers are gone; a lost sign that changes meaning is flagged in place. It also lost
strikethrough, so an "after" listing can still show lines the book deleted, every figure
(each catalog entry's before→after sketch) and long code lines past the margin. Chapter
10's voyage-rating arithmetic is marked unreliable: follow the sequence of moves, not the
numbers. Chapters 6, 7, 8, 11 and 12 are split into a/b files. The examples are
ES2015-era JavaScript.

## Reading path

Corpus states are as of the `updated:` date in the header.

| # | Title | Read this when | Format | Audio | Corpus |
|---|---|---|---|---|---|
| 1 | Fowler, *Refactoring* (2nd ed. 2018) | first on this path — chapters 1 to 3, then the catalog as a reference | PDF | — none found | ingested |
| 2 | Ousterhout, *A Philosophy of Software Design* | — read on the planning path | | | |
| 3 | Khorikov, *Unit Testing* | — read on the verifying path | | | |
| 4 | Nygard, *Release It!* | — read on the releasing path | | | |

### Next

- Beck, *Tidy First?* (2023) — the book brief's runner-up: separate tidying commits from behaviour commits. Short, with an audio edition (Stephen R. Thorne · 2:41); the DRM-free claim at ebooks.com is unverified.
- Fowler, *Refactoring* (the publisher's EPUB) — the same book, re-captured to recover the minus signs and figures; a re-run of the same ingest into the same folder.
