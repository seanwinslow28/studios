---
lane: planning
seat: build-planner
updated: 2026-10-11
---
# Lane manifest — Build Planner

Mandatory first read for the [Build Planner](../bench/build-planner.md). Entries are title +
pointer + one-line when-to-read — shelf labels, never the books: the content lives in the
private corpus (`../corpus/`, gitignored), so pointers resolve only on a machine that has it
(`manifest-only` grounding otherwise, per the seat preamble). Follow only the pointers
relevant to the plan in hand. Seats stop at `## Reading path`; that section is the owner's.

The free layer is wide here because the build plan touches every other seat's work: it names
the slices, the seams the Verifier tests through, the security surface, and the ops paths
Release will own. Architecture calls are not on this shelf; they route upstream.

## Sizing and slicing the build

- **The framing: time, scale, trade-offs, Hyrum's Law** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — deciding how much engineering a change deserves, before the scope section is written.
- **Working in small batches** — [`dora.md`](../corpus/canon/dora.md) — cutting the approach into slices, and when a slice looks too big to land green on its own.
- **Small changes (author's guide)** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — sizing slices so each commit group reads and rolls back on its own.
- **Code review: what to check, how big, how described** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — a slice is heading past a reviewable size.
- **Large-scale changes (repo-wide refactors and migrations)** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — the plan is a rename, API migration or upgrade across many files, and may need splitting into consecutive builds.
- **Simplicity** — [`sre-book.md`](../corpus/canon/sre-book.md) — choosing between approaches, or cutting scope nobody asked for.

## Approach and known structures

- **Chapters worth a planner's time** — [`aosa.md`](../corpus/canon/aosa.md) — looking for a proven structure to follow in the approach section (architecture-sized calls still route upstream).
- **Branch By Abstraction** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — the plan replaces a library, backend or module others depend on, in always-green steps.
- **Branch by abstraction** — [`trunk-based-development.md`](../corpus/canon/trunk-based-development.md) — the same move seen from the branching side, when the rollout section has to say how the replacement lands.
- **Feature Toggles** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — a change must ship dark; choosing the flag type and writing its removal date into the plan.
- **Deprecation and migration** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — a change replaces an old path and the plan must say how the old one goes away.
- **Loosely coupled architecture** — [`dora.md`](../corpus/canon/dora.md) — noting a coupling risk in Reversibility and risks (the call itself routes upstream).

## Interfaces, data and config

- **Ensuring rollback safety during deployments** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — the change touches a data format, wire protocol or persisted state; flag the ops paths for Release.
- **Making retries safe with idempotent APIs** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — any operation that creates something or has side effects and may run twice (file writes, ticket creation, commits, API posts).
- **Configuration design and best practices** — [`sre-workbook.md`](../corpus/canon/sre-workbook.md) — the change adds config options; name the defaults and validation the Builder must write.
- **The twelve, in one line each** — [`twelve-factor.md`](../corpus/canon/twelve-factor.md) — a checklist when the plan introduces config, a service dependency, a background job or a deploy step.
- **Stateless processes (factor VI)** — [`twelve-factor.md`](../corpus/canon/twelve-factor.md) — the plan stores anything between runs.
- **Semantic Versioning 2.0.0: what the number promises** — [`commit-version-changelog-conventions.md`](../corpus/canon/commit-version-changelog-conventions.md) — deciding whether a change is breaking.

## Failure handling and load

- **Timeouts, retries and backoff with jitter** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — specifying any network or subprocess call: model providers, webhooks, hooks that shell out.
- **Avoiding fallback in distributed systems** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — the design says "if X fails, try Y instead".
- **Cascading failures and overload** — [`sre-book.md`](../corpus/canon/sre-book.md) — writing the failure-handling part of the approach (retries, timeouts, backoff).
- **Avoiding insurmountable queue backlogs** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — any queue, inbox or ticket folder that agents drain.
- **Using load shedding to avoid overload** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — any server or queue consumer.
- **Managing load** — [`sre-workbook.md`](../corpus/canon/sre-workbook.md) — anything that scales or calls rate-limited services.
- **Design for resilience (ch8)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — deciding what the change does when a dependency fails.

## Test seams and test strategy

- **Test strategy: size, scope, flakiness, the pyramid** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — writing the test approach the Verifier will audit and then write to.
- **Test doubles: real first, fake second, stub sparingly** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — naming the seams the Builder must leave (injectable clock, filesystem, HTTP client, model client).
- **Testable code (for the Builder)** — [`testing-on-the-toilet.md`](../corpus/canon/testing-on-the-toilet.md) — naming the code shape in the plan so the Verifier can test without reading source.
- **Deciding what to test, and how much** — [`testing-on-the-toilet.md`](../corpus/canon/testing-on-the-toilet.md) — the acceptance criteria are written and the test seams section needs priorities.
- **The Practical Test Pyramid** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — deciding which level each criterion is tested at.
- **Larger tests: fidelity, configuration, and risk-driven test plans** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — a criterion needs an integration or end-to-end test.
- **The core principle** — [`testing-library-principles.md`](../corpus/canon/testing-library-principles.md) — the plan touches a UI.

## Security & privacy surface

Rate the surface against the seven triggers first; these entries help write the section once rated.

- **The adversary mindset (ch2)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — opening the security section: who would attack this, and how.
- **Read this first: three principles that run through both lists** — [`owasp-llm-agentic-top-10.md`](../corpus/canon/owasp-llm-agentic-top-10.md) — any plan for a hook, agent harness or model call (trigger 6).
- **Agentic Top 10 (2026)** — [`owasp-llm-agentic-top-10.md`](../corpus/canon/owasp-llm-agentic-top-10.md) — the threat list for an agent that reads outside text and can act.
- **LLM Top 10 (2025)** — [`owasp-llm-agentic-top-10.md`](../corpus/canon/owasp-llm-agentic-top-10.md) — a model is a component of the change.
- **Part 1: Index by task** — [`owasp-cheat-sheets.md`](../corpus/canon/owasp-cheat-sheets.md) — picking the one or two sheets that match the change, to cite in the section.
- **Part 2: Distilled checklists for the twelve most relevant sheets** — [`owasp-cheat-sheets.md`](../corpus/canon/owasp-cheat-sheets.md) — tool scoping and cost limits, secrets, MCP servers, subprocess calls, outbound fetches.
- **How to use the list at Devcraft scale** — [`owasp-top-10-2025.md`](../corpus/canon/owasp-top-10-2025.md) — naming which web-risk classes the change touches.
- **Chapter guide with the L1 requirements** and **A starter L1+ profile for Devcraft repos** — [`owasp-asvs-5.md`](../corpus/canon/owasp-asvs-5.md) — picking requirement IDs the Verifier will turn into tests.
- **The 2025 list, with a Verifier test per entry** — [`cwe-top-25.md`](../corpus/canon/cwe-top-25.md) — listing the weakness classes a change touches.
- **PW: Produce Well-Secured Software** and **What 800-218A adds for AI** — [`nist-ssdf.md`](../corpus/canon/nist-ssdf.md) — naming the secure-development practice a plan section follows; the AI addendum when prompts, model calls or model files change.
- **Security-Focused Guide for AI Code Assistant Instructions** — [`openssf-guides.md`](../corpus/canon/openssf-guides.md) — writing the plan's guidance to the Builder, so nothing relies on the agent being careful.
- **Design for least privilege (ch5)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — stating what access the change needs.
- **Config and secrets (factor III)** — [`twelve-factor.md`](../corpus/canon/twelve-factor.md) — where each secret lives and how it reaches the code.
- **Dependency management** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — the plan proposes any new dependency.

## Agent harnesses, hooks and seat runs

- **Hooks: the contract a hook script must honour** and **Hooks: decision control by event** — [`claude-code-docs.md`](../corpus/canon/claude-code-docs.md) — specifying any Claude Code hook, and choosing which event enforces the rule.
- **Permission rules**, **Permission modes and settings precedence** and **Sandboxing** — [`claude-code-docs.md`](../corpus/canon/claude-code-docs.md) — the security section of an unattended Claude agent: what is OS-enforced and what is advisory.
- **Sandbox mode and approval policy** and **Execpolicy rules** — [`codex-docs.md`](../corpus/canon/codex-docs.md) — deciding what the Builder may run, sandboxed and not.
- **Prompting and best practices for the Builder** — [`codex-docs.md`](../corpus/canon/codex-docs.md) — writing the plan as a hand-off a Codex Builder can follow without the drafting conversation.
- **Model selection and reasoning effort** — [`codex-docs.md`](../corpus/canon/codex-docs.md) — the plan's budget line.
- **The DORA AI Capabilities Model (the seven, confirmed)** — [`dora.md`](../corpus/canon/dora.md) — planning work on an agent harness, or deciding what context agents get.
- **Observing LLM apps and agent harnesses** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — any harness that calls a model.

## Observability and rollout in the plan

- **Instrumenting distributed systems for operational visibility** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — writing what the change must log and measure.
- **Instrumentation and the wide event** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — the plan's telemetry spec.
- **Observability-driven development** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — every plan's verification thinking, beyond the test suite.
- **Monitoring with purpose** — [`sre-workbook.md`](../corpus/canon/sre-workbook.md) — specifying instrumentation Release will alert on.
- **The model in brief** and **Short-lived feature branches: the rules** — [`trunk-based-development.md`](../corpus/canon/trunk-based-development.md) — how the work is cut into branches and lands.
- **Embracing risk and error budgets** — [`sre-book.md`](../corpus/canon/sre-book.md) — deciding how much test and rollout ceremony a change deserves.
- **Eliminating toil** — [`sre-book.md`](../corpus/canon/sre-book.md) — deciding whether a recurring manual step is worth automating in this build.

## Audit duty: the code change and change note

- **What to look for: the review checklist** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — reading the Builder's diff against the plan.
- **The standard: approve once it definitely improves code health** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — the bar to name in the audit's verdict.
- **Writing findings: review comments** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — writing a finding the Builder must act on.
- **Navigating a change: order of attack** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — the diff spans many files.
- **Refactoring catalog** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — checking that a move the change note names is the move the diff made.

## Book layer

The Planner's primary book is ingested; the other three each earn a pointer row.

- **Ousterhout, *A Philosophy of Software Design* — cheatsheet** — [`books/a-philosophy-of-software-design/cheatsheet.md`](../corpus/books/a-philosophy-of-software-design/cheatsheet.md) — reviewing a draft plan before it leaves the seat: the red flags as a checklist.
- **Ousterhout, *A Philosophy of Software Design* — ch. 1–5** — [`books/a-philosophy-of-software-design/`](../corpus/books/a-philosophy-of-software-design/) — judging how much complexity an approach leaks: module depth, information hiding.
- **Ousterhout, *A Philosophy of Software Design* — ch. 6–10** — [`books/a-philosophy-of-software-design/`](../corpus/books/a-philosophy-of-software-design/) — shaping an interface or layer the slices create, or deciding where error handling lives.
- **Ousterhout, *A Philosophy of Software Design* — ch. 11, 15** — [`books/a-philosophy-of-software-design/`](../corpus/books/a-philosophy-of-software-design/) — weighing two approaches before choosing, and writing interface specs before code.
- **Ousterhout, *A Philosophy of Software Design* — ch. 19, 20** — [`books/a-philosophy-of-software-design/`](../corpus/books/a-philosophy-of-software-design/) — a plan leans on a current trend, or has a latency budget.
- **Fowler, *Refactoring* — ch. 2, 3** — [`books/refactoring/`](../corpus/books/refactoring/) — scheduling preparatory refactoring as its own slice, or reading smells as signals of scope.
- **Khorikov, *Unit Testing* — ch. 1, 2, 4, 6–8, 10** — [`books/unit-testing/`](../corpus/books/unit-testing/) — writing test seams: the test mix, a functional core, which dependencies to mock, the humble-object split, migrations.
- **Nygard, *Release It!* — ch. 1, 5, 7, 9, 13, 14, 16** — [`books/release-it/`](../corpus/books/release-it/) — life-cycle cost, the deploy target, and sequencing a big change as small releases.

Read the corpus honestly: the ingest is the **first edition** (v1.01, 2018), not the 2nd
edition (2021) the book brief ruled, so nothing the 2nd edition revised is covered. About
sixteen figures were lost in capture, several of them code listings, and the chapter 2
formula is rebuilt from the prose. Three source slips are flagged in place, among them redo
named where undo is meant in chapter 9. The book reflects the 2018 agile and TDD debate.

## Reading path

Corpus states are as of the `updated:` date in the header.

| # | Title | Read this when | Format | Audio | Corpus |
|---|---|---|---|---|---|
| 1 | Ousterhout, *A Philosophy of Software Design* (1st ed. 2018) | first on this path — short, and the checklist this seat judges every plan against | PDF | — none found | ingested |
| 2 | Winters, Manshreck & Wright, *Software Engineering at Google* (2020) | before your first full build — free, and the widest view of the craft in the set | web (free) | — | distilled |
| 3 | Fowler, *Refactoring* | — read on the building path | | | |
| 4 | Khorikov, *Unit Testing* | — read on the verifying path | | | |
| 5 | Nygard, *Release It!* | — read on the releasing path | | | |

### Next

- Thomas & Hunt, *The Pragmatic Programmer* (20th anniv. ed.) — the book brief's runner-up: broad working habits rather than a plan checklist. Ingested only from a licensed copy (pragprog sells it without restrictive DRM).
- Ousterhout, *A Philosophy of Software Design* (2nd ed. 2021) — the edition the brief ruled; buying it means re-running the same ingest into the same folder.
