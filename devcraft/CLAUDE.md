# CLAUDE.md — Devcraft

**Devcraft — a software engineering studio.**

The third -craft team, built on the [craftwork](../craftwork/README.md) recipe: a four-seat bench that plans, tests, builds and releases code in Sean's own repos, and explains every material choice (why A over B, briefly, and what it leaned on from the canon). The machinery is public; the brain is private.

**Not voice-bearing.** Devcraft ships code, plans, tests and run records. Public prose that will be read as Sean (READMEs, launch notes) is drafted plain and routed to the voice skills as follow-on work.

## Status

Scaffold only. The studio is being built along the [Devcraft build map](https://github.com/seanwinslow28/SWCB/issues/100), on the brain's private tracker, which holds the ratified decisions and the open tickets. Nothing in this folder is final until its owning ticket closes.

## Layout

| Path | Lane | What lives here |
|---|---|---|
| `bench/` | public | Four seat definitions: Build Planner, Builder, Verifier, Release & Reliability. Placeholder until its map ticket closes |
| `templates/` | public | One artifact template per seat (build plan, test suite and run record, code change and change note, release plan and runbook), the gate schedule and its attack lists, and Devcraft's return templates. Placeholder until its map ticket closes |
| `lanes/` | public | Four lane manifests: topic-organized tables of contents (title + pointer + one-line when-to-read) into the private corpus, doubling as reading paths. Shelf labels, never the books. Placeholder until its map ticket closes |
| `trace/` | public | Devcraft's side of the shared trace kit ([craftwork/trace/](../craftwork/trace/README.md)): `studio.py`, the profile the kit reads, and `taxonomy.md`, empty until Devcraft's own labels earn a seat failure mode |
| `corpus/` | **private — gitignored** | Two-layer reference corpus: free-canon distillates + book-to-skill ingests |
| `ledger/` | **private — gitignored** | The decision ledger, a clone of its own private repo, accreting per engagement. Engagements are `dc-eng-NNN`, entries `dc-eng-NNN.dNN` |
| `books/` | **private — gitignored** | Guard directory only: purchased ebooks live at `~/Books/devcraft/`, outside the repo. Nothing should ever sit here |
| shared law | public | [`../craftwork/`](../craftwork/README.md): what every -craft team inherits, one copy |
| master skill | public | `.claude/skills/devcraft/`, per the house rule. A placeholder until the map's master-skill tickets write it |

## Inherited law

Devcraft runs on all of [craftwork/law.md](../craftwork/law.md) and adds to it only where its own rules below say so.

- **Name the canon:** [craftwork § Name the canon](../craftwork/law.md#name-the-canon).
- **The audit shape and the three-seat floor:** [craftwork § The audit shape](../craftwork/law.md#the-audit-shape-and-the-three-seat-floor).
- **D+14:** [craftwork § Standing success measure](../craftwork/law.md#standing-success-measure).
- **Availability ladder:** [craftwork § Availability ladder](../craftwork/law.md#availability-ladder).
- **Self-targeted engagements:** [craftwork § Self-targeted modifier](../craftwork/law.md#self-targeted-modifier).
- **Model delegation:** [craftwork § Model delegation](../craftwork/law.md#model-delegation).
- **The alias probe at Route:** [craftwork § The alias probe at Route](../craftwork/law.md#the-alias-probe-at-route).
- **Checks converge:** [craftwork § Checks converge](../craftwork/law.md#checks-converge-and-the-ladder-has-brakes).
- **Handoffs:** [the handoff contract](../craftwork/handoff-contract.md), and the sender's binding for each pair.

## Non-negotiable rules

1. **Public machinery, private brain.** `corpus/`, `ledger/` and `books/` are local-only via the PRIVATE LAYER block in the root `.gitignore`. Never `git add` them, never weaken those rules, and never let book-derived text, ledger detail, or the name of an employer, a client or a startup land in a tracked file or an issue. Assume every tracked file in this folder is read by a recruiter. `ledger/` is its own git repo backed up to a **private** remote (`seanwinslow28/devcraft-ledger`): any session that writes to it commits and pushes there before ending (`git -C devcraft/ledger push`), never to this repo.
2. **Graceful degradation.** On a machine where the private lanes are absent (a fresh clone, an employer machine), seats say so plainly and continue on tracked knowledge. They never fabricate citations into a corpus they cannot read.
3. **How, never what.** Devcraft owns how code is built, never what is built or the architecture. Work arrives three ways: a Productcraft execution breakdown, a Systemcraft design with its open implementation holds, or Sean's direct ask. Product and architecture calls are routed upstream, never decided here.
4. **The boundary rule.** The Builder never edits a test. The Verifier never edits source. Release & Reliability never edits application source or tests; migration code is source, so the Builder writes it to Release's migration plan and the Verifier tests it. No seat certifies its own work done.
5. **Claude plans, Codex codes.** The Builder runs on Codex; the Build Planner, the Verifier and Release & Reliability run on Claude, so code and its tests always come from different vendors. Every seat's `model:` line is a ruled row of [the runtime registry](../craftwork/templates/runtime-registry.md). Every Codex pass pins `--model gpt-5.6-sol` with its effort spelled out, never the config default and never `ultra`.
6. **Audits run fresh, in one closed cycle, and two gates hold a full build.** Planner → Builder → Release → Verifier → Planner, the arrow reading "audits". The plan gate runs after the Verifier's audit of the build plan and before any code; its anchor is the build plan. The release gate runs before merge and attacks the change, the test record and the release plan together; its anchor is the release plan. A gate runs on the vendor that did not last write its anchor. A small direct ask takes only the release gate, and only when it touches live data, a migration, or anything that runs unattended. When Systemcraft's Gate 3 waits on a build, the release gate runs first and feeds it, never replacing it.
7. **Security is a duty, not a seat.** It is a required section of the build plan, security tests from the Verifier, a fixed attack list at the release gate, and secret and dependency hooks. A plan that rates its surface high gets one extra security pass, run as a protocol. The seat question reopens only if the release gate raises a P0 security finding the plan did not foresee.
8. **Main is Sean's.** All work happens on a branch in its own worktree. Nothing merges to main without Sean's dated yes, and seat sessions hold no merge credentials.
9. **The never-do list** is being worded on the build map's never-do ticket, which also rules which items a hook enforces and which a seat contract states. It lands here in full when that ticket closes.
