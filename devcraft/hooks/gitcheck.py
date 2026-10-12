#!/usr/bin/env python3
"""Devcraft's git hooks: pre-commit, commit-msg and pre-push, for a build worktree.

`seat.py worktree` points the build worktree's own `core.hooksPath` (a
per-worktree setting) at `git/` beside this file, so these run for that
worktree only and never for Sean's own checkout. Every refusal names the rule.

- **pre-commit:** the staged change has no secret (gitleaks, by full path), no
  name from the machine's list (never-do 11), and, when a seat is committing,
  only paths that seat may write (never-do 4, 14).
- **commit-msg:** the message carries no name from the list; a seat's commit gets a
  `Devcraft-Seat: <seat>` trailer from its context, which the diff check reads.
- **pre-push:** no seat pushes; only to Sean's own remotes (never-do 1); never to
  the default branch, whose merge runs in Sean's own checkout after his dated
  yes (never-do 3); no branch deletes; a force-push only to the build's own
  branch and never once a release-gate record exists (never-do 7); no name from
  the list in anything pushed (never-do 11); then the diff check
  (`devcraft/diffcheck/`) over the engagement's range, whose exit 2 refuses.

Fails closed: a missing tool or list refuses the commit or push.
"""
from __future__ import annotations

import glob
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import policy  # noqa: E402

ZERO = "0" * 40
GITLEAKS = [os.environ.get("DEVCRAFT_GITLEAKS", ""), "/opt/homebrew/bin/gitleaks", "/usr/local/bin/gitleaks"]
DIFFCHECK = Path(__file__).resolve().parents[1] / "diffcheck" / "diffcheck.py"


class Refuse(Exception):
    pass


def git(*args: str, check: bool = True) -> str:
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise Refuse(f"git {' '.join(args[:2])} failed: {r.stderr.strip()[:200]}")
    return r.stdout


def name_hits(text: str, label: str) -> List[str]:
    """Where a listed name appears. The name itself is never printed."""
    hits = []
    pats = [re.compile(r"(?<![A-Za-z0-9])" + re.escape(n) + r"(?![A-Za-z0-9])", re.I) for n in policy.names()]
    for i, line in enumerate(text.splitlines(), 1):
        if any(p.search(line) for p in pats):
            hits.append(f"{label}:{i}")
    return hits


def added_lines_by_file(diff: str) -> str:
    """Only what the change adds: file headers and + lines."""
    keep = []
    for line in diff.splitlines():
        if line.startswith("+++ ") or (line.startswith("+") and not line.startswith("+++")):
            keep.append(line)
        elif line.startswith("diff --git"):
            keep.append(line)
    return "\n".join(keep)


def seat_context() -> Optional[policy.Context]:
    if not os.environ.get("DEVCRAFT_CONTEXT"):
        return None
    return policy.Context.from_env()


def gitleaks() -> str:
    for g in GITLEAKS:
        if g and os.access(g, os.X_OK):
            return g
    raise Refuse("gitleaks is not installed at a known full path; the secret scan cannot run")


def pre_commit() -> None:
    r = subprocess.run([gitleaks(), "git", "--pre-commit", "--staged", "--redact", "--no-banner", "--exit-code", "1"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise Refuse("the secret scan found a secret in the staged change (never-do 6):\n" + (r.stdout + r.stderr).strip()[-1500:])
    diff = git("diff", "--cached", "--no-color", "-U0", "--no-ext-diff")
    hits = name_hits(added_lines_by_file(diff), "staged diff line")
    if hits:
        raise Refuse("a name from the machine's list is in the staged change (never-do 11): " + ", ".join(hits[:10]))
    ctx = seat_context()
    if ctx and ctx.seat != "coordinator":
        top = git("rev-parse", "--show-toplevel").strip()
        for path in git("diff", "--cached", "--name-only", "-z").split("\0"):
            if path:
                why = ctx.write_verdict(os.path.join(top, path))
                if why:
                    raise Refuse(f"the {ctx.seat} may not commit {path}: {why}")


SEAT_TRAILER = "Devcraft-Seat"


def commit_msg(path: str) -> None:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    hits = name_hits("\n".join(l for l in text.splitlines() if not l.startswith("#")), "commit message line")
    if hits:
        raise Refuse("a name from the machine's list is in the commit message (never-do 11): " + ", ".join(hits))
    # The seat trailer is what the diff check reads to attribute a commit after the fact. A seat
    # gets its own seat stamped from the context it cannot edit; a trailer naming another seat
    # is refused. The coordinator's commits carry none, or the one it writes for a Builder slice.
    ctx = seat_context()
    if ctx and ctx.seat != "coordinator":
        claimed = re.findall(r"^" + SEAT_TRAILER + r":\s*(\S+)\s*$", text, re.M)
        if any(c != ctx.seat for c in claimed):
            raise Refuse(f"the commit message names a seat other than the one committing ({ctx.seat}) (never-do 4)")
        if not claimed:
            subprocess.run(["git", "interpret-trailers", "--in-place", "--if-exists", "addIfDifferent",
                            "--trailer", f"{SEAT_TRAILER}: {ctx.seat}", path], check=True)


def owner_of(url: str) -> str:
    m = re.search(r"github\.com[:/]+([^/]+)/", url)
    return m.group(1).lower() if m else ""


def default_branch(remote: str) -> str:
    ref = git("symbolic-ref", "-q", f"refs/remotes/{remote}/HEAD", check=False).strip()
    if ref:
        return "refs/heads/" + ref.rsplit("/", 1)[-1]
    for b in ("main", "master"):
        if subprocess.run(["git", "show-ref", "--verify", "-q", f"refs/remotes/{remote}/{b}"]).returncode == 0:
            return f"refs/heads/{b}"
    return "refs/heads/main"


def release_gate_ran(engagement: str) -> bool:
    if not engagement:
        return False
    pats = ["trace/pass-*-release-gate-*.md", "audits/*release-gate*"]
    return any(glob.glob(os.path.join(engagement, p)) for p in pats)


def pre_push(remote: str, url: str, lines: List[str]) -> None:
    ctx = seat_context()
    if ctx and ctx.seat != "coordinator":
        raise Refuse(f"the {ctx.seat} never pushes; the coordinator does (never-do 1, 3)")
    owner = owner_of(url)
    if owner not in policy.OWNERS:
        raise Refuse(f"{url} is not one of Sean's repos (never-do 1)")
    default = default_branch(remote)
    own = "refs/heads/" + git("rev-parse", "--abbrev-ref", "HEAD").strip()
    engagement = os.environ.get("DEVCRAFT_ENGAGEMENT") or git("config", "--get", "devcraft.engagement", check=False).strip()
    for line in lines:
        parts = line.split()
        if len(parts) != 4:
            continue
        local_ref, local_sha, remote_ref, remote_sha = parts
        if remote_ref in (default, "refs/heads/main", "refs/heads/master"):
            raise Refuse(f"{remote_ref} is the default branch. Nothing reaches it from a build worktree: "
                         "after Sean's dated yes, the merge runs in his own checkout (never-do 3)")
        if local_sha == ZERO:
            raise Refuse(f"deleting {remote_ref} from a build worktree is not allowed (never-do 7)")
        forced = remote_sha != ZERO and subprocess.run(
            ["git", "merge-base", "--is-ancestor", remote_sha, local_sha], capture_output=True).returncode != 0
        if forced:
            if remote_ref != own:
                raise Refuse(f"a force-push to {remote_ref}, which is not this build's branch ({own}) (never-do 7)")
            if release_gate_ran(engagement):
                raise Refuse("the release gate has run on this branch; it is never force-pushed again (never-do 7)")
        rng = [f"{remote_sha}..{local_sha}"] if remote_sha != ZERO else [local_sha, "--not", f"--remotes={remote}"]
        text = git("log", "-p", "--no-color", "--format=%B", *rng)
        hits = name_hits(text, f"push to {remote_ref}, line")
        hits += name_hits(remote_ref, "branch name")
        if hits:
            raise Refuse("a name from the machine's list is in what this push sends (never-do 11): " + ", ".join(hits[:10]))
        diff_check(engagement, local_sha, remote_ref.rsplit("/", 1)[-1])


def diff_check(engagement: str, candidate: str, branch: str) -> None:
    """The check before every push: the diff check over the engagement's base..candidate, offline.

    Exit 2 (a default branch, an unnamed control edit) refuses the push. Findings
    are recorded in the engagement's evidence and the push proceeds; the release
    gate reads them. No engagement on the worktree: nothing to check against.
    """
    if not engagement:
        return
    top = git("rev-parse", "--show-toplevel").strip()
    r = subprocess.run([sys.executable, str(DIFFCHECK), "--worktree", top, "--engagement", engagement,
                        "--candidate", candidate, "--branch", branch, "--offline"], capture_output=True, text=True)
    sys.stderr.write(r.stdout)
    if r.returncode == 2:
        raise Refuse("the diff check refused this push: " + (r.stderr.strip() or r.stdout.strip().splitlines()[0] if r.stdout.strip() else ""))
    if r.returncode not in (0, 1):
        raise Refuse(f"the diff check could not run (exit {r.returncode}): {r.stderr.strip()[-300:]}")


def main(argv: List[str]) -> int:
    hook = os.path.basename(argv[0])
    args = argv[1:]
    if hook == "gitcheck.py":
        hook, args = args[0], args[1:]
    try:
        if hook == "pre-commit":
            pre_commit()
        elif hook == "commit-msg":
            commit_msg(args[0])
        elif hook == "pre-push":
            pre_push(args[0], args[1], sys.stdin.read().splitlines())
        else:
            raise Refuse(f"unknown hook {hook}")
    except (Refuse, policy.ContextError) as e:
        sys.stderr.write(f"Devcraft {hook}: refused. {e}\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
