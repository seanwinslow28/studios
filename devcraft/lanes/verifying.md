---
lane: verifying
seat: verifier
updated: 2026-10-11
---
# Lane manifest — Verifier

Mandatory first read for the [Verifier](../bench/verifier.md). Entries are title + pointer +
one-line when-to-read — shelf labels, never the books: the content lives in the private
corpus (`../corpus/`, gitignored), so pointers resolve only on a machine that has it
(`manifest-only` grounding otherwise, per the seat preamble). Follow only the pointers
relevant to the criteria in hand. Seats stop at `## Reading path`; that section is the
owner's.

This seat audits the build plan, then writes the whole suite from the plan, blind to the
code, and records it failing before any code exists. The shelf follows that order: judging
a plan, deciding what to test and at what level, writing tests that survive refactoring,
the security tests the plan's triggers call for, and judging Release's drill and the test
record's own trustworthiness. Nothing here is about editing source: that is the Builder's.

## Audit duty: the build plan

- **What to look for: the review checklist** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — the plan audit: design, complexity, test strategy.
- **The standard: approve once it definitely improves code health** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — the bar to name in the audit's verdict.
- **Writing findings: review comments** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — writing a finding the Planner must act on.
- **The framing: time, scale, trade-offs, Hyrum's Law** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — judging whether the plan's rigour fits the code's expected life.
- **Short-lived feature branches: the rules** and **Anti-patterns** — [`trunk-based-development.md`](../corpus/canon/trunk-based-development.md) — is the branch plan really short-lived; a quick reject list.
- **A06:2025 Insecure Design** and **How to use the list at Devcraft scale** — [`owasp-top-10-2025.md`](../corpus/canon/owasp-top-10-2025.md) — checking each of the seven triggers against the plan, and that the security section covers the risks the change actually touches.
- **Tailoring and "documented security decisions"** and **The three levels** — [`owasp-asvs-5.md`](../corpus/canon/owasp-asvs-5.md) — are the plan's security decisions written down, and is a target level stated.
- **Security-Focused Guide for AI Code Assistant Instructions** — [`openssf-guides.md`](../corpus/canon/openssf-guides.md) — checking the plan does not rely on the Builder being careful.
- **Part 1: Index by task** — [`owasp-cheat-sheets.md`](../corpus/canon/owasp-cheat-sheets.md) — does the plan cite the right sheet for its surface.
- **Config and secrets (factor III)** — [`twelve-factor.md`](../corpus/canon/twelve-factor.md) — a plan-audit check on where secrets live.

## Deciding what to test, and at what level

- **Test strategy: size, scope, flakiness, the pyramid** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — mapping each acceptance criterion to a test size and scope.
- **The Practical Test Pyramid** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — deciding which level each test belongs at.
- **Larger tests: fidelity, configuration, and risk-driven test plans** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — a criterion needs an integration or end-to-end test.
- **Deciding what to test, and how much** — [`testing-on-the-toilet.md`](../corpus/canon/testing-on-the-toilet.md) — the criterion → test map is drafted and needs priorities.
- **Test automation** — [`dora.md`](../corpus/canon/dora.md) — the test-strategy view from delivery research.
- **What AI adoption does to delivery (2025 report)** — [`dora.md`](../corpus/canon/dora.md) — deciding how much independent testing an agent-built change needs.
- **Testing code: unit, integration, fuzzing, static analysis (ch13)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — choosing test methods beyond example tests.
- **Testing for reliability** — [`sre-book.md`](../corpus/canon/sre-book.md) — choosing which production checks to add.

## Writing tests that survive refactoring

- **Test behaviour, not implementation** — [`testing-on-the-toilet.md`](../corpus/canon/testing-on-the-toilet.md) — writing every test blind to the code, against what the plan says it does.
- **Writing unit tests that stay useful** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — writing tests, and judging later whether a change that forces edits to old tests is explained.
- **Test doubles: prefer real, then fake, then mock** — [`testing-on-the-toilet.md`](../corpus/canon/testing-on-the-toilet.md) — choosing what stands in for a dependency.
- **Test doubles: real first, fake second, stub sparingly** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — the same rule, with the seams the plan names (clock, filesystem, HTTP client, model client).
- **Readable tests: DAMP, focused, cause next to effect** — [`testing-on-the-toilet.md`](../corpus/canon/testing-on-the-toilet.md) — writing a test someone can read at a release gate.
- **Assertions and failure messages** — [`testing-on-the-toilet.md`](../corpus/canon/testing-on-the-toilet.md) — making a red test diagnosable.
- **Flaky tests** — [`testing-on-the-toilet.md`](../corpus/canon/testing-on-the-toilet.md) — any test that touches time, files, threads or shared state.
- **Safe defaults and reversibility** — [`testing-on-the-toilet.md`](../corpus/canon/testing-on-the-toilet.md) — adding a test for the safe default.
- **Refactoring catalog** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — recognising a pure refactor, where tests should not change.

## Failure behaviour

- **Timeouts, retries and backoff with jitter** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — testing timeout and retry behaviour.
- **Making retries safe with idempotent APIs** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — writing the "same request twice" test.
- **Cascading failures and overload** — [`sre-book.md`](../corpus/canon/sre-book.md) — writing failure-injection tests.
- **Using load shedding to avoid overload** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — designing a load test.
- **Disposability: startup, shutdown, idempotent jobs (factor IX)** — [`twelve-factor.md`](../corpus/canon/twelve-factor.md) — shutdown and retry tests for a job.
- **Data processing pipelines** — [`sre-workbook.md`](../corpus/canon/sre-workbook.md) — golden-data tests for a batch job or overnight agent.

## Security tests

- **The 2025 list, with a Verifier test per entry** — [`cwe-top-25.md`](../corpus/canon/cwe-top-25.md) — writing a security test per weakness class the plan lists, and labelling findings.
- **Using ASVS to write tests** and **Chapter guide with the L1 requirements** — [`owasp-asvs-5.md`](../corpus/canon/owasp-asvs-5.md) — turning each requirement ID in the plan into a test.
- **Citing requirements: the ID scheme** — [`owasp-asvs-5.md`](../corpus/canon/owasp-asvs-5.md) — naming a test after the requirement it checks.
- **Agentic Top 10 (2026)** and **LLM Top 10 (2025)** — [`owasp-llm-agentic-top-10.md`](../corpus/canon/owasp-llm-agentic-top-10.md) — one test per agentic item at minimum, for an agent that reads outside text and acts.
- **Part 2: Distilled checklists for the twelve most relevant sheets** — [`owasp-cheat-sheets.md`](../corpus/canon/owasp-cheat-sheets.md) — the abuse-case matrix as a ready test list; argument-injection, SSRF, MCP rug-pull and negative input tests.
- **The 12 categories at a glance** and **Per-category guide: what to test, how, and what automates** — [`owasp-wstg.md`](../corpus/canon/owasp-wstg.md) — choosing which categories a change touches and how each automates.
- **Citing tests: the ID scheme and versions** — [`owasp-wstg.md`](../corpus/canon/owasp-wstg.md) — naming security tests and findings.
- **A01:2025 Broken Access Control** and **A05:2025 Injection** — [`owasp-top-10-2025.md`](../corpus/canon/owasp-top-10-2025.md) — negative tests and input fuzzing.
- **Design for least privilege (ch5)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — testing that the change gets no more access than the plan says.

## Hooks, harnesses and agent code

- **Hooks: exit codes and output (the part tests should pin)** — [`claude-code-docs.md`](../corpus/canon/claude-code-docs.md) — each row is a hook test case.
- **Hooks: decision control by event** — [`claude-code-docs.md`](../corpus/canon/claude-code-docs.md) — asserting the right field at the right nesting level.
- **Execpolicy rules** — [`codex-docs.md`](../corpus/canon/codex-docs.md) — testing a Codex rule file.
- **Git hooks** — [`pro-git-and-worktree.md`](../corpus/canon/pro-git-and-worktree.md) — testing secret and dependency hooks.
- **Observing LLM apps and agent harnesses** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — evals for model-backed paths.
- **OpenTelemetry: spans, layering, naming, schemas** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — telemetry tests: the logs and spans the plan promised.

## UI tests

- **The core principle** and **Query priority** — [`testing-library-principles.md`](../corpus/canon/testing-library-principles.md) — finding and driving elements as a user would; the order is a reviewable rule.
- **Waiting without flakiness** and **Interacting like a user** — [`testing-library-principles.md`](../corpus/canon/testing-library-principles.md) — anything async, and writing interaction steps.

## Running the suite, and the run record

- **Stashing and cleaning** — [`pro-git-and-worktree.md`](../corpus/canon/pro-git-and-worktree.md) — resetting a working tree between test runs.
- **Bisect and blame** — [`pro-git-and-worktree.md`](../corpus/canon/pro-git-and-worktree.md) — hunting a regression.
- **Effective troubleshooting** — [`sre-book.md`](../corpus/canon/sre-book.md) — diagnosing a failing test before reporting it.
- **Observability for CI/CD** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — flake triage.
- **Continuous integration: what runs when** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — deciding which tests run on every commit.

## Book layer

The Verifier's primary book is ingested; the other three each earn a pointer row.

- **Khorikov, *Unit Testing* — cheatsheet** — [`books/unit-testing/cheatsheet.md`](../corpus/books/unit-testing/cheatsheet.md) — first, on any test or test diff: the four pillars, mock and stub rules, smells, and the table of test changes that weaken a check against those that strengthen it.
- **Khorikov, *Unit Testing* — ch. 1–4** — [`books/unit-testing/`](../corpus/books/unit-testing/) — what a unit test is, how one is laid out, and scoring a test's value.
- **Khorikov, *Unit Testing* — ch. 5, 9** — [`books/unit-testing/`](../corpus/books/unit-testing/) — deciding what to mock, and keeping tests from breaking on refactors.
- **Khorikov, *Unit Testing* — ch. 6, 7** — [`books/unit-testing/`](../corpus/books/unit-testing/) — choosing output, state or communication style, and telling the plan which code shape makes tests valuable.
- **Khorikov, *Unit Testing* — ch. 8, 10** — [`books/unit-testing/`](../corpus/books/unit-testing/) — integration tests and tests against a real database.
- **Khorikov, *Unit Testing* — ch. 11** — [`books/unit-testing/`](../corpus/books/unit-testing/) — a test reaches into private state, leaks domain knowledge, or mocks a concrete class.
- **Ousterhout, *A Philosophy of Software Design* — ch. 1, 4, 5, 7, 9, 11, 13–15, 18–20** — [`books/a-philosophy-of-software-design/`](../corpus/books/a-philosophy-of-software-design/) — auditing a plan for red flags, and reviewing docs and names that changed with the code.
- **Fowler, *Refactoring* — ch. 1, 2, 4** — [`books/refactoring/`](../corpus/books/refactoring/) — what self-testing code needs, and the seat notes in the catalog that mark test changes as handed over.
- **Nygard, *Release It!* — ch. 2–5, 11, 12, 14, 15, 17** — [`books/release-it/`](../corpus/books/release-it/) — test harnesses, contract tests, load-test realism, fuzzing and fault injection.

Read the corpus honestly: every figure was lost in capture, and chapters 4 to 8 lean on them
most, so their tables are rebuilt from flattened text. The examples are C# and .NET tooling
of 2019–20; carry the idea, not the API. Thirteen source defects are flagged in place,
mostly listings that disagree with their own text, and one attribution rests on a writer's
outside knowledge and is marked unverified.

## Reading path

Corpus states are as of the `updated:` date in the header.

| # | Title | Read this when | Format | Audio | Corpus |
|---|---|---|---|---|---|
| 1 | Khorikov, *Unit Testing Principles, Practices, and Patterns* (2020) | first on this path — the four pillars are the judgment every test on the bench is held to | PDF | Nate Colitto · about 7:18 (not checked) | ingested |
| 2 | Winters, Manshreck & Wright, *Software Engineering at Google* | — read on the planning path; its testing chapters are this lane's second read | | | |
| 3 | Fowler, *Refactoring* | — read on the building path | | | |
| 4 | Ousterhout, *A Philosophy of Software Design* | — read on the planning path | | | |
| 5 | Nygard, *Release It!* | — read on the releasing path | | | |

### Next

- Feathers, *Working Effectively with Legacy Code* (2004) — pinning existing behaviour with tests before code changes. It sits here, not on the building shelf, because the Builder never edits a test. InformIT sells it DRM-free.
- Aniche, *Effective Software Testing* (2022) — the book brief's runner-up: deriving cases from a spec with partitions and boundaries, which suits tests written first. Could pair with the pick later.
- Meszaros, *xUnit Test Patterns* (2007) — a large reference catalog of test smells; a reference shelf, not a read.
