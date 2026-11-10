# Shipping with a way back.

Read this before changing anything already running: a scheduled job, a Python install, a settings file. It's about changes you can take back, and knowing whether they worked.

## What a way back is.

A way back is a tested route to how things were, ready before the change lands. An undo written down but never run is a guess, and guesses fail at the worst moment: at night, with the change half done.

A good way back has three parts:

- **A copy of what was there.** The old job file, the old venv (a project's private Python folder), the old settings, kept untouched beside the new ones, never overwritten.
- **One short command that restores it,** run once on purpose before the real change, so you've seen it work.
- **A check that says it's restored,** the same check that tells you the change itself worked.

Amazon's engineers call this avoiding one-way doors. Ask of every step: if this is wrong an hour from now, what does going back cost? If "very little", go. If "we can't", split the step until each piece can be undone, or name it plainly as the one that can't, so Sean knows what he's accepting.

## Rollback or roll forward.

Rolling back means returning to the last version that worked. Rolling forward means fixing the fault and shipping a new version on top. When something breaks, roll back first and work out why afterwards. It's quick, it's been seen working, and it needs no clear thinking at 3 a.m.

Rolling forward is right only when going back is worse or impossible: the change already rewrote something the old version can't read, or the fix is one obvious line and the rollback is slow. That second case is a warning: the undo needs work.

Undoing gets hard when a change leaves something the old version can't cope with: a new log format, a renamed folder, a deleted file. The cure is to add before you remove, often called expand and contract. Put the new thing in beside the old, switch over, and clear the old away only once the new one has run cleanly for a while. Moving a scheduled job to a new Python works this way. Build the new venv next to the old one, point the job at it, and keep the old venv until the job has run a few nights in a row. Going back is then one edit and one reload.

## Show it before you do it.

Terraform, a tool for setting up servers from written settings, built a habit worth copying: plan, then apply. Before it touches anything, it lists exactly what it will create, change and delete, with a one-line total. You approve that plan, and only that plan runs. If the world moved since the plan was made, it refuses rather than guessing.

A small script can do the same: a preview that changes nothing and prints what it would do ("3 jobs to move, 1 already moved"), then an apply that does just that. Terraform's plan can also return 0 for no changes, 2 for changes waiting and 1 for an error, so a script can tell them apart.

A dry run must skip the risky part, not just the visible part. Cloudflare learned this in July 2019 (on the shelf). A new firewall rule went out in a mode that only logged what it would have blocked. It still took sites down worldwide for 27 minutes, because the expensive pattern matching ran either way. Logging instead of acting wasn't the safety. Not running the costly work would have been.

Plan-then-apply is a preview, not an undo. Terraform doesn't roll back an apply that fails halfway. The way back still needs its own plan.

## Small first, then everything.

A canary is a small, early dose of a change, watched closely before everything gets it. At Google's scale that's a slice of servers. At Devcraft's scale it's one job before all of them, one night before every night, one Mac before both.

What makes a canary worth having:

- **It runs the real thing.** One real job on one real night.
- **You decide in advance what you're watching.** Did it run, did it exit cleanly, did it write what it should. Decided beforehand, a bad result can't be talked away afterwards.
- **It lasts long enough to mean something.** A nightly job needs at least one night. A weekly one needs a week, or a run triggered by hand that does the full work.
- **It happens however small the change feels.** Google's SRE book tells of a settings change judged low risk, given a lighter rollout, that hit a rare path everywhere at once.

## Pin it, so an upgrade is a choice.

Pinning means fixing a version on purpose, so it changes only when you decide. Without it, upgrades arrive as side effects.

Justin Mayer's post "Homebrew Python is not for you" (on the shelf) lays out the chain. You upgrade some unrelated tool. It pulls in a newer Python. Homebrew's cleanup removes the old one. Every venv built on it now points at nothing, and a scheduled job using one fails with an error about a library that won't load. Nobody chose that upgrade.

uv's design (on the shelf, Sean's pick) shows the other way. uv installs Python into its own folder, where Homebrew never reaches. Venvs point at a folder named for the minor version (3.14), which points in turn at the newest bug-fix release (say 3.14.8). When uv installs a newer bug-fix release, it moves that one pointer and keeps the old copy, because something might still use it. It never jumps to a new minor version on its own, since 3.15 can change which packages work. That's pinning done well: small safe fixes follow by themselves, big changes wait for a decision, and nothing in use is deleted.

A lockfile, which records the exact version of every package, does the same for a project's parts. Upgrades happen on a day you pick, with the old version still there to go back to.

## Make it safe to run twice.

Unattended jobs get re-run: after a crash, after the Mac wakes, by hand to test. A job is safe when running it twice does no more than running it once. The word for that is idempotent.

The danger is the half-applied change. A script moves four of seven jobs, then fails. Now the system is in a state nobody designed or tested, and the undo may not fit it either. The defences:

- **Check before acting.** Each step asks "is this already done?" and skips if so.
- **Stage, then switch.** Build the new thing fully off to the side, check it, then flip one pointer. A failure before the flip leaves the old thing untouched.
- **Fail loudly and stop.** A failed step halts the run and names itself.

## Know that it ran.

A change is done when you've seen it work and you'll hear if it stops. For a scheduled job, that means answering four questions each morning without digging: did it run, did it succeed, how long did it take, and is anything filling up. In practice:

- **Logs that land where you'll look.** launchd, the scheduler built into macOS, throws away a job's output unless the job file names a place to write it.
- **Honest exit codes.** Zero only when the work really happened. "Ran fine, wrote nothing" is a failure and should say so.
- **An alarm for silence.** A job that never starts writes no error. To catch it, each good run leaves a timestamp, and a separate check complains when the timestamp is too old. Watching only for errors misses the job that didn't run at all.
- **A record of what changed.** Which version, which interpreter, when it switched. A week later, "what changed?" should take seconds to answer.

## How it goes wrong, and the fix.

- **Silent failure.** The job stopped and nothing said so. Fix: logs to a file, honest exit codes, and an alarm for a missing run.
- **An undo never tried.** It's written down and fails when needed. Fix: run the undo once, on purpose, before the change.
- **An undo too slow to use.** Cloudflare's usual way back meant rebuilding the whole rule set twice, so they reached for a blunt off switch instead. Fix: time the way back. If it's slower than the damage, make it faster.
- **A rescue that depends on the broken thing.** Cloudflare's own sign-in tool was down too. Fix: make sure the undo works while the changed thing is broken. For a Python move, going back must not need the new Python.
- **Half-applied changes.** Fix: stage, then switch, and make every step safe to repeat.
- **No record of what changed.** Fix: log each switch with the old and new values.
- **Clearing the old too soon.** Fix: keep it until the new one has run cleanly long enough to trust.

## Examples.

- **Cloudflare's 2019 outage** (`devcraft/research/cloudflare-2019-outage-rollback.md`): 25 minutes from rollout to the off switch, 2 to recover, then 45 more of checking in one city before switching the feature back on.
- **Terraform's plan, then apply** (`devcraft/research/terraform-plan-then-apply.md`): the preview that changes nothing, the one-line total, the stale plan refused.
- **uv's patch upgrades** (`devcraft/research/uv-python-patch-upgrades.md`) and **"Homebrew Python is not for you"** (`devcraft/research/homebrew-python-is-not-for-you.md`): the same problem, met by design and by accident.
