# CLAUDE.md — Motioncraft

**Motioncraft — an animation and motion-design studio.**

The fourth -craft team, built on the [craftwork](../craftwork/README.md) recipe: a four-seat bench that takes a film from brief to delivered cut (story and staging, designed poses and look, the moving scene, then finishing and sound) and explains every material choice (why A over B, briefly, and what it leaned on from the canon). It owns every piece of moving visual storytelling Sean's projects need: 2D and 3D animation, motion graphics, kinetic typography, editing, and sound for its own films. The machinery is public; the brain is private.

**Not voice-bearing.** Motioncraft ships boards, animatics, designed frames, moving scenes, cuts and their check records. Every engagement runs in plain mode. Sean's sole approval of artistry is a rule of this studio (below), not a voice declaration, and the corpus has no layer of Sean's own work.

## Status

Scaffold only. The studio is being built along the [Motioncraft build map](https://github.com/seanwinslow28/SWCB/issues/184), on the brain's private tracker, which holds the ratified decisions and the open tickets. The bench, the audit cycle, the gates and each seat's model land on their own map tickets. Nothing in this folder is final until its owning ticket closes.

## Layout

| Path | Lane | What lives here |
|---|---|---|
| `bench/` | public | Four seat definitions: Visual Story Director, Art and Pose Designer, Animator, Finishing and Sound Designer, each owning one artifact, with its contract, write zone, audit duty, launch form, toolbelt and never-do lines |
| `templates/` | public | One artifact template per seat, the evidence-pack fields, the check record and gate findings, the gate schedule (story, appearance and motion gates) and its attack lists, and the two handoff files: the return to Scriptcraft (whose binding is Scriptcraft's to write) and the binding for Devcraft |
| `lanes/` | public | Four lane manifests: topic-organized tables of contents (title + pointer + one-line when-to-read) into the private corpus, doubling as reading paths. Shelf labels, never the books |
| `trace/` | public | Motioncraft's side of the shared trace kit ([craftwork/trace/](../craftwork/trace/README.md)): `studio.py`, the profile the kit reads, and `taxonomy.md`, empty until Motioncraft's own labels earn a seat failure mode |
| `corpus/` | **private — gitignored** | The technique guides (principle and tool guides kept separate) and any book-to-skill ingests |
| `ledger/` | **private — gitignored** | The decision ledger and the approvals ledger, a clone of its own private repo, accreting per engagement. Engagements are `mc-eng-NNN`, entries `mc-eng-NNN.dNN` |
| `books/` | **private — gitignored** | Guard directory only: purchased ebooks live at `~/Books/motioncraft/`, outside the repo. Nothing should ever sit here |
| production material | **private — never in this repo** | Sources, media, renders and approved frames live in the approved private production workspace and its companion media folder (SWCB #157), never here and never in the ledger |
| shared law | public | [`../craftwork/`](../craftwork/README.md): what every -craft team inherits, one copy |
| master skill | public | `.claude/skills/motioncraft/SKILL.md`, per the house rule, linked for Codex at `.agents/skills/motioncraft`. Designed and written on the map's master-skill tickets; until then the folder holds a placeholder and there is nothing to invoke |

## Inherited law

Motioncraft runs on all of [craftwork/law.md](../craftwork/law.md) and adds to it only where its own rules below say so.

- **Name the canon:** [craftwork § Name the canon](../craftwork/law.md#name-the-canon).
- **The audit shape and the three-seat floor:** [craftwork § The audit shape](../craftwork/law.md#the-audit-shape-and-the-three-seat-floor).
- **D+14:** [craftwork § Standing success measure](../craftwork/law.md#standing-success-measure).
- **Availability ladder:** [craftwork § Availability ladder](../craftwork/law.md#availability-ladder).
- **Self-targeted engagements:** [craftwork § Self-targeted modifier](../craftwork/law.md#self-targeted-modifier).
- **Model delegation:** [craftwork § Model delegation](../craftwork/law.md#model-delegation).
- **The alias probe at Route:** [craftwork § The alias probe at Route](../craftwork/law.md#the-alias-probe-at-route).
- **Checks converge:** [craftwork § Checks converge](../craftwork/law.md#checks-converge-and-the-ladder-has-brakes).
- **Handoffs:** [the handoff contract](../craftwork/handoff-contract.md), and the sender's binding for each pair: [Motioncraft's for Devcraft](templates/handoff-binding-devcraft.md), and Scriptcraft's once it exists, answered on [the Scriptcraft return](templates/handoff-return-scriptcraft.md).

## Non-negotiable rules

1. **Public machinery, private brain.** `corpus/`, `ledger/` and `books/` are local-only via the PRIVATE LAYER block in the root `.gitignore`. Never `git add` them, never weaken those rules, and never let book-derived text, ledger detail, production material, or the name of an employer, a client or a startup land in a tracked file or an issue. A guide names a canon title and an idea in the writer's own words, never the book's text. Assume every tracked file in this folder is read by a recruiter. `ledger/` is its own git repo backed up to a **private** remote (`seanwinslow28/motioncraft-ledger`): any session that writes to it commits and pushes there before ending (`git -C motioncraft/ledger push`), never to this repo.
2. **Graceful degradation.** On a machine where the private lanes are absent (a fresh clone, an employer machine), seats say so plainly and continue on tracked knowledge. They never fabricate citations into a corpus they cannot read.
3. **Sean alone approves artistry.** No seat, gate or check approves how a film looks, moves or sounds. Seats and gates find and recommend; Sean decides, and his decision is recorded in the approvals ledger with its date.
4. **How a film is made, never what.** Motioncraft owns the making: staging, design, timing, finishing and delivery. What the film is (its story, its words, its purpose) is Sean's, or arrives from the sender's brief. Words come from Scriptcraft once it exists, pipeline software goes to Devcraft, and standalone static design is Designcraft's. Art made to move or made for a film is Motioncraft's.
5. **One named operator per application, versions preserved.** Each shared application (an animation, compositing or edit tool, an image path) has one named seat operating it in an engagement. Every version a seat saves is kept, never overwritten, so any frame Sean saw can be found again.
6. **Every finding is one of three kinds.** A **technical fail** (a check that does not pass: frame rate, resolution, a dropped frame, a broken file), a **craft fail** pinned to frames and named in the glossary's words, or a **taste call** for Sean. A finding that is none of these is not a finding. Taste calls are never ruled by a seat or a gate.
7. **The never-do list.** Fourteen items on top of the inherited law. Each seat's contract states every item.

    1. Never approve artistry. Sean alone approves.
    2. Never let a seat's own report stand as evidence. Every motion claim ships its evidence pack: adjacent frames around every contact and transformation, plus full-speed playback.
    3. Never animate before the appearance gate on a full train, and never carry an approval across a material design change.
    4. One operator per shared application, versions preserved.
    5. Never lower the bar or widen a test to fit a limit. A limit reached triggers a review and a decision from Sean.
    6. Never upload media or run cloud generation outside the tool-specific intended-use approval.
    7. Never buy anything: [SWCB AGENTS.md § Unattended runs](https://github.com/seanwinslow28/SWCB/blob/main/AGENTS.md#unattended-runs), and every purchase waits for Sean's individual yes.
    8. Never pass a filter, a render, or a generated image or clip off as authored craft.
    9. Never compress or re-time the film to flatter a proof.
    10. Never ship words as final.
    11. Never let agent-written research become a skill or a policy: [SWCB AGENTS.md § Trust](https://github.com/seanwinslow28/SWCB/blob/main/AGENTS.md#trust).
    12. Never name the employer, or let day-job material in except as lessons Sean states himself: [SWCB AGENTS.md § Trust](https://github.com/seanwinslow28/SWCB/blob/main/AGENTS.md#trust).
    13. Never let a cloud-generated asset be the only copy. Download it to the companion media folder on creation.
    14. Never present a version to Sean without its id, its status and his prior note on it.
8. **The interim words rule.** Every on-screen or spoken word is Sean's until Scriptcraft exists, and then Sean's or Scriptcraft's, arriving locked on its binding: a placeholder is marked (`WP<n>`) and never shipped, and a word change goes back on [the return's line](templates/handoff-return-scriptcraft.md), never rewritten here.
