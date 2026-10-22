# Lane manifests

One file per lane, four lanes, one seat each. A lane manifest is the first thing its seat
reads on every invocation, and it is two documents in one file, on Productcraft's schema
([its lanes README](../../productcraft/lanes/README.md)).

The upper half is **shelf labels** for the seat: a title, a pointer into the private corpus,
and a one-line note saying when the pointer is worth following. Never the books themselves:
the content lives in `../corpus/`, which is gitignored, so on a machine without it the
pointers do not resolve and the pass's grounding is written `manifest-only` instead of pretending
otherwise ([seat preamble](../templates/seat-preamble.md); rule 2 of
[`../CLAUDE.md`](../CLAUDE.md)). The lower half, from `## Reading path` down, is Sean's: an
ordered table of what to read and in what situation, plus a `### Next` shelf of titles the
lane holds in reserve. Seats stop at that heading; the reading path is the owner's.

The upper half has two layers. The **free-canon sections**, grouped by the parts of the
seat's own artifact and ending with its audit duty, point at the distillates in
`../corpus/canon/`. The **`## Book layer`** points at the four book ingests in
`../corpus/books/`, by chapter number and in the manifest's own words. A topic with no
pointer goes in the artifact header's `thin_lane:`, which is how a lane learns what it is
missing.

Three rules keep the halves from drifting. A book's format, audio and corpus facts, and the
account of what its capture lost, are stated on exactly one lane, its primary, and any other
lane that needs its chapters carries a pointer row instead; a free book in a reading path
follows the same rule. Listen-only titles appear only in a reading path, never as a shelf
label, so no seat can name a book it cannot read; Devcraft has none yet. And *Working
Effectively with Legacy Code* sits on the Verifier's Next shelf, not the Builder's, because
the Builder never edits a test (the boundary rule). Toolbelts live in the seat file, not
here.

## Studio reading order

No opening listen yet. The lanes, in pipeline order (the seat number, as on
[the bench](../bench/README.md)):

| # | Lane | Seat | Primary book | Manifest |
|---|---|---|---|---|
| 1 | Planning | [Build Planner](../bench/build-planner.md) | Ousterhout, *A Philosophy of Software Design* | [planning.md](planning.md) |
| 2 | Building | [Builder](../bench/builder.md) | Fowler, *Refactoring* (2nd ed.) | [building.md](building.md) |
| 3 | Verifying | [Verifier](../bench/verifier.md) | Khorikov, *Unit Testing Principles, Practices, and Patterns* | [verifying.md](verifying.md) |
| 4 | Releasing | [Release & Reliability](../bench/release-reliability.md) | Nygard, *Release It!* (2nd ed.) | [releasing.md](releasing.md) |

Pipeline order lives in the seat number, never the filename, so reordering the bench never
renames a manifest. The gates (plan, release, security pass) are protocols, not seats, and
read no manifest: they work from their anchors and [the gate
schedule](../templates/gate-schedule.md).

In a reading path's Corpus column, `ingested` means a book-to-skill ingest under
`../corpus/books/`, and `distilled` a free-canon distillate under `../corpus/canon/`.
