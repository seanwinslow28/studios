---
lane: releasing
seat: release-reliability
updated: 2026-10-11
---
# Lane manifest — Release & Reliability

Mandatory first read for the [Release & Reliability seat](../bench/release-reliability.md).
Entries are title + pointer + one-line when-to-read — shelf labels, never the books: the
content lives in the private corpus (`../corpus/`, gitignored), so pointers resolve only on
a machine that has it (`manifest-only` grounding otherwise, per the seat preamble). Follow
only the pointers relevant to the release in hand. Seats stop at `## Reading path`; that
section is the owner's.

This is the deepest free shelf on the bench: two SRE books, a free observability book, the
Builders' Library and PagerDuty's docs all write for this seat first. The sections follow
the release plan's own order, from what changes in the running world to Sean's go-live
step, then the seat's audit of the test record.

## Release surface and preconditions

- **The twelve, in one line each** — [`twelve-factor.md`](../corpus/canon/twelve-factor.md) — listing what changes in the running world: config, jobs, backing services, secret names.
- **Backing services, dev/prod parity, admin processes** — [`twelve-factor.md`](../corpus/canon/twelve-factor.md) — environment notes and one-off admin steps.
- **Release engineering** — [`sre-book.md`](../corpus/canon/sre-book.md) — build provenance, branching and config rollout in the plan.
- **Reliable launches and the launch checklist** — [`sre-book.md`](../corpus/canon/sre-book.md) — checking the plan covers each launch area before go-live.
- **Configuration design and best practices** — [`sre-workbook.md`](../corpus/canon/sre-workbook.md) — a release changes config.
- **A02:2025 Security Misconfiguration** — [`owasp-top-10-2025.md`](../corpus/canon/owasp-top-10-2025.md) — the go-live checklist's configuration items.

## Migration plan

- **Parallel Change, aka expand and contract** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — sequencing a migration so every step is releasable and reversible.
- **Ensuring rollback safety during deployments** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — a data format, wire protocol or persisted state changes.
- **Data integrity** — [`sre-book.md`](../corpus/canon/sre-book.md) — anything that deletes or rewrites data; the backup before it.
- **Deprecation and migration** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — writing how the old path is retired.
- **Data processing pipelines** — [`sre-workbook.md`](../corpus/canon/sre-workbook.md) — a batch job, ETL or overnight agent that transforms data.

## Rollout

- **Canarying releases** — [`sre-workbook.md`](../corpus/canon/sre-workbook.md) — writing the solo-scale canary (dry run, log-only shadow, live) and its automatic stop.
- **Automating safe, hands-off deployments** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — stages, bake times, rollback triggers.
- **Validating a change in production: the crossing-over flywheel** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — post-deploy verification and rollback triggers.
- **Design for a changing landscape: how to roll out changes (ch7)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — sequencing a rollout, or a dependency or security patch.
- **Feature Toggles** — [`martinfowler-articles.md`](../corpus/canon/martinfowler-articles.md) — choosing the flag type and writing its removal as release follow-up.
- **Working in small batches** — [`dora.md`](../corpus/canon/dora.md) — keeping a release small.
- **Release branches and releasing from trunk** — [`trunk-based-development.md`](../corpus/canon/trunk-based-development.md) — the hotfix path, and whether a release branch is needed.
- **Continuous delivery and release** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — phasing and flags in the rollout.

## Failure modes

- **Cascading failures and overload** — [`sre-book.md`](../corpus/canon/sre-book.md) — naming how the change fails under load and what stops the spread.
- **Design for resilience (ch8)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — degradation and failover parts of the runbook.
- **Mitigating denial of service, solo scale (ch10)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — a public endpoint, webhook receiver, or agent that calls an API in a loop.
- **Avoiding insurmountable queue backlogs** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — backlog alarms for a queue agents drain.
- **A10:2025 Mishandling of Exceptional Conditions** — [`owasp-top-10-2025.md`](../corpus/canon/owasp-top-10-2025.md) — rollback and partial-failure behaviour.

## Rollback and kill drill

- **Build, release, run — and rollback (factor V)** — [`twelve-factor.md`](../corpus/canon/twelve-factor.md) — writing the rollback section.
- **Design for recovery: rollouts, rollbacks, known state (ch9)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — the way back to a known good state.
- **Emergency response: lessons from real breakages** — [`sre-book.md`](../corpus/canon/sre-book.md) — testing that rollback works, before a "low risk" change goes out.
- **Version control and rollback** — [`dora.md`](../corpus/canon/dora.md) — the rollback mechanism, and what must be committed.
- **Reset demystified: the three trees** and **Recovery: reflog and fsck** — [`pro-git-and-worktree.md`](../corpus/canon/pro-git-and-worktree.md) — git steps in a rollback runbook.
- **Safe defaults and reversibility** — [`testing-on-the-toilet.md`](../corpus/canon/testing-on-the-toilet.md) — writing scripts and migration commands that fail safe.
- **Disposability: startup, shutdown, idempotent jobs (factor IX)** — [`twelve-factor.md`](../corpus/canon/twelve-factor.md) — a job that re-runs unattended must be safe to run twice.

## Monitoring and alerts

- **Monitoring: symptoms, causes and the four golden signals** — [`sre-book.md`](../corpus/canon/sre-book.md) — the runbook's "how we know it is healthy" and alert sections.
- **SLIs, SLOs and SLAs** — [`sre-book.md`](../corpus/canon/sre-book.md) — stating what "healthy after go-live" means.
- **Implementing SLOs** and **Alerting on SLOs** — [`sre-workbook.md`](../corpus/canon/sre-workbook.md) — a health definition, an error budget policy and burn-rate alert rules.
- **SLOs and helpful alerts** and **Error budgets and burn alerts: the mechanics** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — what pages, and is the budget healthy enough to ship.
- **Release-time signals: build info, the after-deploy questions, runbooks** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — tying a regression to a release.
- **Instrumenting distributed systems for operational visibility** — [`aws-builders-library.md`](../corpus/canon/aws-builders-library.md) — the runbook's "how to tell it is working" steps.
- **Alerting principles** — [`pagerduty-incident-response.md`](../corpus/canon/pagerduty-incident-response.md) — deciding what wakes Sean.
- **Being on-call** and **On-call and pager load** — [`sre-book.md`](../corpus/canon/sre-book.md), [`sre-workbook.md`](../corpus/canon/sre-workbook.md) — what wakes a human versus waits for the morning log.
- **A09:2025 Security Logging and Alerting Failures** — [`owasp-top-10-2025.md`](../corpus/canon/owasp-top-10-2025.md) — security alert definitions.
- **Logs (factor XI)** — [`twelve-factor.md`](../corpus/canon/twelve-factor.md) — where to look when it breaks.

## Runbook and incidents

- **Severity levels and "is this an incident?"** and **During an incident** — [`pagerduty-incident-response.md`](../corpus/canon/pagerduty-incident-response.md) — the runbook's severity table and first-response steps.
- **Roles (and what a solo developer keeps)** — [`pagerduty-incident-response.md`](../corpus/canon/pagerduty-incident-response.md) — which hats the runbook asks Sean to wear.
- **Managing incidents** — [`sre-book.md`](../corpus/canon/sre-book.md) — the incident section and the go-live watch plan.
- **The core analysis loop and AI in investigations** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — triage after a failed release.
- **Effective troubleshooting** — [`sre-book.md`](../corpus/canon/sre-book.md) — a post-release check fails.
- **Crisis management (ch17)** and **Recovery and aftermath (ch18)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — a security incident is suspected; recovery checklists.
- **After an incident and the postmortem process**, **Postmortem template shape** and **Blameless culture and language** — [`pagerduty-incident-response.md`](../corpus/canon/pagerduty-incident-response.md) — writing the postmortem after a rollback.
- **Postmortem culture** — [`sre-book.md`](../corpus/canon/sre-book.md) — after any rollback or failed release.
- **On-call and incident anti-patterns** — [`pagerduty-incident-response.md`](../corpus/canon/pagerduty-incident-response.md) — handoff notes and escalation rules.
- **Headless / non-interactive runs** — [`claude-code-docs.md`](../corpus/canon/claude-code-docs.md) — a runbook for an unattended Claude agent.
- **Non-interactive runs: `codex exec`** — [`codex-docs.md`](../corpus/canon/codex-docs.md) — a runbook or job for an unattended Codex run.

## Secure deployment

- **Deploying code: the supply chain (ch14)** — [`building-secure-reliable-systems.md`](../corpus/canon/building-secure-reliable-systems.md) — checking that what ships is what was reviewed and tested.
- **Tracks and levels at a glance** and **What a solo developer can realistically reach** — [`slsa.md`](../corpus/canon/slsa.md) — stating the release's target integrity level.
- **What provenance is, and what has to be in it** — [`slsa.md`](../corpus/canon/slsa.md) — the plan's integrity section.
- **PS: Protect the Software** and **RV: Respond to Vulnerabilities** — [`nist-ssdf.md`](../corpus/canon/nist-ssdf.md) — release integrity, and the advisory and rollback path.
- **What 800-218A adds for AI** — [`nist-ssdf.md`](../corpus/canon/nist-ssdf.md) — AI-specific rollback criteria.
- **Part 2: Distilled checklists** — [`owasp-cheat-sheets.md`](../corpus/canon/owasp-cheat-sheets.md) — kill switch and rollback for an agent, secret rotation, deploy gates.
- **Permission rules**, **Permission modes and settings precedence** and **Sandboxing** — [`claude-code-docs.md`](../corpus/canon/claude-code-docs.md) — checking a runbook's flags match what the plan allowed.
- **Sandbox mode and approval policy**, **Config layers, profiles and CODEX_HOME** and **Model selection and reasoning effort** — [`codex-docs.md`](../corpus/canon/codex-docs.md) — a reproducible, pinned run command.
- **Dependency management** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — upgrade and pinning policy.

## Go-live, versions and release notes

- **Semantic Versioning 2.0.0** and **Keep a Changelog 1.1.0** — [`commit-version-changelog-conventions.md`](../corpus/canon/commit-version-changelog-conventions.md) — choosing the version and writing release notes.
- **How the three fit together (Devcraft release flow)** — [`commit-version-changelog-conventions.md`](../corpus/canon/commit-version-changelog-conventions.md) — from commit messages to version bump to changelog.
- **Signing, tagging and naming releases** — [`pro-git-and-worktree.md`](../corpus/canon/pro-git-and-worktree.md) — the go-live step's tag.
- **Worktrees (git-worktree)** — [`pro-git-and-worktree.md`](../corpus/canon/pro-git-and-worktree.md) — cleanup and per-worktree state after the build.
- **Emergencies** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — a hotfix wants to skip normal review.

## Delivery health and the bench

- **The delivery metrics (five, in two groups)** — [`dora.md`](../corpus/canon/dora.md) — choosing what the release record tracks per repo.
- **Measuring AI-assisted work** — [`dora.md`](../corpus/canon/dora.md) — what the release record adds for an agent-built change.
- **The platform: quality internal platforms, at bench scale** — [`dora.md`](../corpus/canon/dora.md) — a change to the bench's own hooks, gate scripts or CI.
- **Eliminating toil** — [`sre-book.md`](../corpus/canon/sre-book.md) — a runbook step is done by hand every release.
- **Observability for CI/CD** — [`observability-engineering.md`](../corpus/canon/observability-engineering.md) — pipeline health in release readiness.

## Audit duty: the test suite and run record

- **Writing unit tests that stay useful** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — is the test record trustworthy.
- **Larger tests: fidelity, configuration, and risk-driven test plans** — [`software-engineering-at-google.md`](../corpus/canon/software-engineering-at-google.md) — do config, smoke and production-like checks cover the release surface.
- **Testing for reliability** — [`sre-book.md`](../corpus/canon/sre-book.md) — does the suite exercise the failure modes the release plan names.
- **CI in the TBD sense** — [`trunk-based-development.md`](../corpus/canon/trunk-based-development.md) — what "green" means before merge.
- **Flaky tests** — [`testing-on-the-toilet.md`](../corpus/canon/testing-on-the-toilet.md) — a red run that passes on retry.
- **Writing findings: review comments** — [`google-code-review-guide.md`](../corpus/canon/google-code-review-guide.md) — writing a finding the Verifier must act on.

## Book layer

The seat's primary book is ingested; the other three each earn a pointer row.

- **Nygard, *Release It!* — cheatsheet** — [`books/release-it/cheatsheet.md`](../corpus/books/release-it/cheatsheet.md) — checking a release plan against each stability antipattern and its counter, and the decision rules for the release gate.
- **Nygard, *Release It!* — ch. 4, 5** — [`books/release-it/`](../corpus/books/release-it/) — naming the failure modes, and the patterns that contain them: timeouts, breakers, bulkheads.
- **Nygard, *Release It!* — ch. 13** — [`books/release-it/`](../corpus/books/release-it/) — deploy phases, and expand-then-contract for schema and data.
- **Nygard, *Release It!* — ch. 14** — [`books/release-it/`](../corpus/books/release-it/) — versioning an interface others call.
- **Nygard, *Release It!* — ch. 10, 11** — [`books/release-it/`](../corpus/books/release-it/) — the control plane, and security at deploy time.
- **Nygard, *Release It!* — ch. 17** — [`books/release-it/`](../corpus/books/release-it/) — drills and fault injection beyond the kill drill.
- **Nygard, *Release It!* — ch. 1–3, 6–9, 12, 15, 16** — [`books/release-it/`](../corpus/books/release-it/) — case studies, the production foundations, and adapting a system over time.
- **Ousterhout, *A Philosophy of Software Design* — ch. 8, 10, 17, 20** — [`books/a-philosophy-of-software-design/`](../corpus/books/a-philosophy-of-software-design/) — crash versus recover, config sprawl, consistency in CI, latency budgets.
- **Khorikov, *Unit Testing* — ch. 8–10** — [`books/unit-testing/`](../corpus/books/unit-testing/) — structured logging, fail-fast config, immutable migrations, fixing forward.
- **Fowler, *Refactoring* — ch. 2** — [`books/refactoring/`](../corpus/books/refactoring/) — published interfaces, parallel change, and integrating continuously instead of long branches.

Read the corpus honestly: ninety-six images were lost, so chapters 4, 16, 13 and 9 lean on prose; every code listing was split by
the extractor and is rebuilt and marked as rebuilt. Forty-five source defects are flagged in
place, among them arithmetic that does not reconcile and a pool count that differs between
chapters 2 and 3. The book is 2018: no service mesh, OpenTelemetry, SBOM or SLSA, a
release-candidate security top-10 from 2017, and a dependency-alert service that no longer
exists. The free layer above covers what it predates.

## Reading path

Corpus states are as of the `updated:` date in the header.

| # | Title | Read this when | Format | Audio | Corpus |
|---|---|---|---|---|---|
| 1 | Nygard, *Release It!* (2nd ed. 2018) | first on this path — failure, deployment and recovery in one book | EPUB | — none found | ingested |
| 2 | Majors, Fong-Jones, Miranda & Parker, *Observability Engineering* (2nd ed. 2026) | before writing your first monitoring and alert section — covers what *Release It!* predates | PDF (free) | — | distilled |
| 3 | Beyer, Jones, Petoff & Murphy, *Site Reliability Engineering* (2016) | when a release first needs an SLO or an incident section — free, read by chapter | web (free) | — | distilled |
| 4 | Ousterhout, *A Philosophy of Software Design* | — read on the planning path | | | |
| 5 | Khorikov, *Unit Testing* | — read on the verifying path | | | |
| 6 | Fowler, *Refactoring* | — read on the building path | | | |

### Next

- Humble & Farley, *Continuous Delivery* (2010) — the book brief's runner-up; deployment pipeline thinking, with 2010 tooling.
- Campbell & Majors, *Database Reliability Engineering* (2017) — migrations and backups, useful but dated.
