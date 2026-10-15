#!/usr/bin/env python3
"""Devcraft's PreToolUse guard, one script for both vendors.

Claude Code runs it from the seat settings file; Codex runs it from the Codex
seat home's `hooks.json`, hash-trusted. It reads the tool call on stdin, judges
it against the pass's seat context (`$DEVCRAFT_CONTEXT`, see `policy.py`), and
blocks with exit code 2 and a reason on stderr. It allows by exiting 0 silently.

It sits on top of the sandbox and the permission deny rules, never instead of
them: those are the wall, and this adds what they cannot see (which seat is
running, a path after `~` and links are resolved, a wrapped `sh -c`, a
plan-named exception). It fails closed: no context, a context it cannot read,
a missing machine-local list or a command it cannot parse is a refusal.

Every decision is appended to the pass's guard log, so a seat run that left no
lines there is a guard that never loaded.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

import policy  # noqa: E402
from policy import Context, ContextError  # noqa: E402
import shellparse  # noqa: E402

SAFE_SINKS = ("/dev/null", "/dev/stdout", "/dev/stderr", "/dev/tty", "/dev/fd/1", "/dev/fd/2")

DENY_ALWAYS = {
    "sudo", "su", "doas", "brew", "pipx", "at", "batch", "csrutil", "spctl", "tccutil", "osascript",
    "security", "dscl", "chsh", "passwd", "shutdown", "reboot", "halt", "kextload", "softwareupdate", "mas",
    "twine", "vercel", "netlify", "fly", "flyctl", "firebase", "wrangler", "terraform", "kubectl", "helm",
    "aws", "gcloud", "az", "heroku", "systemctl", "visudo", "ssh", "scp", "sftp", "ssh-add", "ssh-keygen",
}
READ_ONLY_SUBS = {
    "launchctl": {"list", "print", "print-disabled", "blame", "version", "help", "error"},
    "defaults": {"read", "read-type", "domains", "find", "help"},
    "diskutil": {"list", "info"},
}
PACKAGE_MANAGERS = {
    "npm": {"install", "i", "ci", "add", "uninstall", "remove", "rm", "un", "update", "up", "upgrade", "link", "dedupe", "prune", "audit", "publish", "unpublish", "exec", "x", "init", "pkg"},
    "pnpm": {"install", "i", "add", "remove", "rm", "uninstall", "update", "up", "upgrade", "link", "dedupe", "prune", "publish", "dlx", "import", "patch"},
    "yarn": {"install", "add", "remove", "upgrade", "up", "dedupe", "link", "publish", "dlx", "npm"},
    "bun": {"install", "i", "add", "remove", "rm", "update", "upgrade", "link", "publish", "pm", "x"},
    "pip": {"install", "uninstall", "download", "wheel"},
    "uv": {"add", "remove", "lock", "sync", "pip", "tool", "publish", "self", "python", "venv", "export"},
    "poetry": {"add", "remove", "lock", "install", "update", "publish", "self", "sync"},
    "pipenv": {"install", "uninstall", "lock", "update", "sync", "upgrade"},
    "cargo": {"add", "remove", "update", "install", "publish", "uninstall", "generate-lockfile"},
    "go": {"get", "install", "mod"},
    "gem": {"install", "uninstall", "update", "push"},
    "bundle": {"add", "install", "update", "remove", "lock"},
    "composer": {"require", "remove", "update", "install"},
    "conda": {"install", "remove", "update", "create"},
    "mamba": {"install", "remove", "update", "create"},
}
TEST_RUNNERS = {"jest", "vitest", "playwright", "test", "tests", "snapshot", "snapshots"}
GIT_READ = {
    "status", "diff", "log", "show", "rev-parse", "ls-files", "ls-tree", "cat-file", "blame", "grep",
    "describe", "shortlog", "merge-base", "for-each-ref", "name-rev", "show-ref", "version", "help",
    "check-ignore", "check-attr", "count-objects", "var", "rev-list", "whatchanged", "diff-tree", "diff-files", "diff-index",
}
GIT_WRITE_SEATS = {"verifier", "release-reliability"}
GIT_CONFIG_KEYS = re.compile(r"^(core\.(hookspath|sshcommand|fsmonitor|pager|editor|askpass)|credential|user\.|gpg|commit\.gpgsign|tag\.gpgsign|url\.|http\.|include|alias\.|safe\.|protocol\.|remote\.)", re.I)
GIT_SUB_GLOBAL_WITH_ARG = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path", "--config-env"}


# --- reading the tool call -------------------------------------------------

def normalize(event: dict) -> Tuple[str, dict, str]:
    """(tool, input, cwd) from either vendor's PreToolUse payload."""
    tool = event.get("tool_name") or event.get("tool") or ""
    tin = event.get("tool_input")
    if tin is None:
        tin = event.get("input", {})
    if isinstance(tin, str):
        try:
            tin = json.loads(tin)
        except ValueError:
            tin = {"command": tin}
    cwd = event.get("cwd") or os.getcwd()
    return tool, tin if isinstance(tin, dict) else {}, cwd


def command_text(tin: dict) -> Optional[str]:
    cmd = tin.get("command", tin.get("cmd"))
    if isinstance(cmd, list):
        # Codex sends argv; `bash -lc <script>` is the usual shape.
        if len(cmd) >= 3 and os.path.basename(cmd[0]) in shellparse.SHELLS and cmd[1] in ("-c", "-lc", "-ic"):
            return cmd[2]
        import shlex
        return " ".join(shlex.quote(c) for c in cmd)
    return cmd if isinstance(cmd, str) else None


PATCH_PATH = re.compile(r"^\*\*\* (Add File|Update File|Delete File|Move to): (.+)$", re.M)


def patch_paths(text: str) -> List[Tuple[str, str]]:
    return [(m.group(1), m.group(2).strip()) for m in PATCH_PATH.finditer(text)]


# --- judging -----------------------------------------------------------------

class Verdict(Exception):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def deny(reason: str) -> None:
    raise Verdict(reason)


def resolve(arg: str, cwd: Optional[str], scratch: str = "") -> Optional[str]:
    """An argument as an absolute path, or None when it cannot be resolved."""
    a = arg.replace("${HOME}", "~").replace("$HOME", "~")
    if scratch:  # the launcher sets it to the pass's scratch folder (SWCB #148)
        a = re.sub(r"\$(\{DEVCRAFT_SCRATCH\}|DEVCRAFT_SCRATCH(?![A-Za-z0-9_]))", lambda _: scratch, a)
    if "$" in a or "`" in a:
        return None
    if a.startswith("~"):
        return policy.real(a)
    if os.path.isabs(a):
        return policy.real(a)
    if cwd is None:
        return None
    return policy.real(os.path.join(cwd, a))


def check_write(ctx: Context, arg: str, cwd: Optional[str], creating: bool = False) -> None:
    if arg in SAFE_SINKS:
        return
    p = resolve(arg, cwd, ctx.scratch)
    if p is None:
        deny(f"cannot resolve the write target {arg!r}; name it plainly (never-do 7)")
    why = ctx.write_verdict(p, creating=creating)
    if why:
        deny(why)


def check_read(ctx: Context, arg: str, cwd: Optional[str]) -> None:
    p = resolve(arg, cwd, ctx.scratch)
    if p is None:
        return
    why = ctx.read_verdict(p)
    if why:
        deny(why)


def operands(argv: List[str], skip_first: int = 1, with_value: Iterable[str] = ()) -> List[str]:
    out, i, opts_done = [], skip_first, False
    with_value = set(with_value)
    while i < len(argv):
        a = argv[i]
        if not opts_done and a == "--":
            opts_done = True
        elif not opts_done and a.startswith("-") and a != "-":
            if a in with_value:
                i += 1
        else:
            out.append(a)
        i += 1
    return out


def write_targets(argv: List[str]) -> List[str]:
    """The paths a file-changing command would write, delete or move."""
    name = os.path.basename(argv[0])
    if name in ("rm", "rmdir", "unlink", "shred", "srm", "touch", "mkdir", "tee", "mv", "trash"):
        return operands(argv)
    if name in ("cp", "install", "ln", "rsync", "ditto", "gcp"):
        if "-t" in argv:
            return [argv[argv.index("-t") + 1]]
        ops = operands(argv, with_value=("-m", "-o", "-g", "-e", "--exclude", "--include"))
        return ops[-1:] if len(ops) >= 2 else ops
    if name in ("chmod", "chown", "chgrp", "chflags", "xattr", "setfacl"):
        ops = operands(argv, with_value=("-w", "-d"))
        return ops[1:]
    if name == "truncate":
        return operands(argv, with_value=("-s", "-r"))
    if name == "dd":
        return [a[3:] for a in argv[1:] if a.startswith("of=")]
    if name in ("sed", "gsed") and any(a == "-i" or a.startswith("-i") or a.startswith("--in-place") for a in argv[1:]):
        ops = operands(argv, with_value=("-e", "-f"))
        has_script_flag = any(a in ("-e", "-f") for a in argv)
        return ops if has_script_flag else ops[1:]
    if name == "perl" and any(re.match(r"^-\w*i", a) for a in argv[1:]):
        ops = operands(argv, with_value=("-e", "-E", "-M", "-I"))
        has_e = any(a in ("-e", "-E") or re.match(r"^-\w*[eE]$", a) for a in argv[1:])
        return ops if has_e else ops[1:]
    if name in ("find", "fd"):
        expr = argv[1:]
        if any(a in ("-delete", "-exec", "-execdir", "-ok", "-okdir", "--exec", "-x", "-X") for a in expr):
            roots = []
            for a in expr:
                if a.startswith("-") or a in ("(", "!"):
                    break
                roots.append(a)
            return roots or ["."]
    if name in ("tar", "bsdtar", "gtar"):
        return tar_targets(argv[1:])
    return []


def tar_targets(args: List[str]) -> List[str]:
    """Where tar writes: each -C folder (or the current one) when it extracts, the -f file when it
    creates or appends. A bundle's value letters (f, C) take the next arguments in order, old style too."""
    modes, dirs, files = set(), [], []
    long_modes = {"extract": "x", "get": "x", "create": "c", "append": "r", "update": "u"}
    i = 0
    while i < len(args):
        a = args[i]
        if a.startswith("--"):
            key, eq, val = a[2:].partition("=")
            if key in long_modes:
                modes.add(long_modes[key])
            elif key in ("directory", "file"):
                if not eq and i + 1 < len(args):
                    i += 1
                    val = args[i]
                (dirs if key == "directory" else files).append(val)
        elif (a.startswith("-") and len(a) > 1) or (i == 0 and a):
            for ch in a.lstrip("-"):
                modes.add(ch)
                if ch in "fC" and i + 1 < len(args):
                    i += 1
                    (dirs if ch == "C" else files).append(args[i])
        i += 1
    if "x" in modes:
        return dirs or ["."]
    if modes & {"c", "r", "u"}:
        return [f for f in files if f != "-"]
    return []


def judge_git(ctx: Context, argv: List[str], cwd: Optional[str]) -> None:
    i = 1
    while i < len(argv) and argv[i].startswith("-"):
        flag = argv[i]
        if flag in ("--git-dir", "--work-tree") or flag.startswith(("--git-dir=", "--work-tree=")):
            deny("git --git-dir/--work-tree reach outside the build's worktree (never-do 7)")
        if flag == "-c" and i + 1 < len(argv) and GIT_CONFIG_KEYS.match(argv[i + 1]):
            deny(f"git -c {argv[i + 1].split('=')[0]} changes a control for one call (never-do 6, 14)")
        if flag == "-C" and i + 1 < len(argv):
            cwd = resolve(argv[i + 1], cwd)
        i += 2 if flag in GIT_SUB_GLOBAL_WITH_ARG else 1
    if i >= len(argv):
        return
    sub, rest = argv[i], argv[i + 1:]
    if sub in GIT_READ:
        return
    if sub == "archive":  # reads a commit; its one write is -o, which lands where the seat may write (SWCB #148)
        if any(a.startswith(("--remote", "--exec")) for a in rest):
            deny("git archive --remote or --exec reaches a remote or runs a command (never-do 1, 7)")
        for j, a in enumerate(rest):
            if a in ("-o", "--output") and j + 1 < len(rest):
                check_write(ctx, rest[j + 1], cwd, creating=True)
            elif a.startswith("--output="):
                check_write(ctx, a.split("=", 1)[1], cwd, creating=True)
            elif a.startswith("-o") and len(a) > 2:
                check_write(ctx, a[2:], cwd, creating=True)
        return
    if sub == "branch":
        if any(a in ("-d", "-D", "--delete", "-m", "-M", "--move", "-c", "-C", "--copy", "-f", "--force", "-u", "--set-upstream-to", "--unset-upstream", "--edit-description") for a in rest) or [a for a in rest if not a.startswith("-")]:
            deny("creating, moving or deleting branches is the coordinator's (never-do 7)")
        return
    if sub == "tag":
        if [a for a in rest if not a.startswith("-")] or any(a in ("-d", "--delete", "-a", "-s", "-f") for a in rest):
            deny("tags are the coordinator's")
        return
    if sub == "stash":
        if rest and rest[0] not in ("list", "show"):
            deny("the stash is shared by every worktree; only `git stash list` and `show` (never-do 7)")
        if not rest:
            deny("the stash is shared by every worktree (never-do 7)")
        return
    if sub == "worktree":
        if rest[:1] != ["list"]:
            deny("worktrees are the coordinator's (never-do 7)")
        return
    if sub == "config":
        if any(a in ("--get", "--get-all", "--get-regexp", "--list", "-l", "get", "list") for a in rest):
            if not any(a in ("--unset", "--unset-all", "--add", "--replace-all", "--edit", "-e", "set", "unset") for a in rest):
                return
        deny("git config is a control (never-do 6, 14)")
    if sub == "remote":
        if not rest or rest[0] in ("-v", "--verbose", "show", "get-url"):
            return
        deny("remotes are the coordinator's (never-do 1)")
    if sub == "reflog":
        if not rest or rest[0] in ("show", "list") or not rest[0] in ("expire", "delete", "drop"):
            return
        deny("reflog edits rewrite history (never-do 17)")
    if sub in ("push", "send-pack", "request-pull", "send-email"):
        deny("seats never push; the coordinator does (never-do 1, 3)")
    if ctx.seat not in GIT_WRITE_SEATS:
        deny(f"git {sub} changes the repo; the {ctx.seat} has no git write (bench, toolbelt)")
    # The Verifier and Release commit their own paths.
    if sub in ("add", "rm", "mv", "restore", "checkout"):
        if sub in ("checkout",) and "--" not in rest:
            deny("switching branches is the coordinator's; `git checkout -- <path>` only")
        paths = rest[rest.index("--") + 1:] if "--" in rest else operands(["git"] + rest, with_value=("-s", "--source", "--pathspec-from-file"))
        if any(a in ("-A", "--all", ".", ":/", "-u", "--update") for a in rest) or not paths:
            deny(f"git {sub} takes named paths only (AGENTS.md: stage named paths)")
        for p in paths:
            check_write(ctx, p, cwd)
        return
    if sub == "commit":
        flags = [a for a in rest if re.fullmatch(r"-[A-Za-z]+", a)]
        if "--no-verify" in rest or any("n" in f for f in flags):
            deny("commits run the pre-commit check; never --no-verify (never-do 5)")
        if "--all" in rest or any("a" in f for f in flags):
            deny("commit named, staged paths only; never -a (AGENTS.md)")
        return
    deny(f"git {sub} is the coordinator's")


def judge_gh(argv: List[str]) -> None:
    rest = [a for a in argv[1:]]
    if not rest:
        return
    sub = rest[0]
    action = rest[1] if len(rest) > 1 else ""
    ok = {
        "issue": {"view", "list", "status"}, "pr": {"view", "list", "diff", "checks", "status"},
        "repo": {"view"}, "run": {"view", "list"}, "release": {"view", "list"}, "search": None,
        "help": None, "version": None, "--version": None,
    }
    if sub == "api":
        method = None
        for j, a in enumerate(rest):
            if a in ("-X", "--method") and j + 1 < len(rest):
                method = rest[j + 1].upper()
            elif a.startswith("--method="):
                method = a.split("=", 1)[1].upper()
        if (method and method != "GET") or any(a in ("-f", "-F", "--field", "--raw-field", "--input") or a.startswith(("--field=", "--raw-field=", "--input=")) for a in rest):
            deny("gh api writes; seats only read (never-do 1)")
        return
    if sub in ok and (ok[sub] is None or action in ok[sub]):
        return
    deny(f"gh {sub} {action}".strip() + " acts on GitHub; seats only read (never-do 1, 8)")


def scripts_off(name: str, argv: List[str]) -> bool:
    args = argv[1:]
    if name in ("npm", "pnpm", "yarn", "bun"):
        return "--ignore-scripts" in args
    if name in ("pip", "pip3"):
        return any(a in ("--only-binary=:all:",) for a in args) or any(
            a == "--only-binary" and j + 1 < len(args) and args[j + 1] == ":all:" for j, a in enumerate(args))
    if name == "uv":
        return "--no-build" in args
    return False


def judge_packages(ctx: Context, name: str, argv: List[str]) -> None:
    if name in ("pip3",) or re.fullmatch(r"pip3(\.\d+)?", name):
        name = "pip"
    if name in ("python", "python3") or re.fullmatch(r"python3(\.\d+)?", name):
        if len(argv) > 2 and argv[1] == "-m" and argv[2] in ("pip", "pipx", "ensurepip"):
            if argv[2] != "pip":
                deny(f"python -m {argv[2]} installs globally (never-do 16)")
            argv, name = ["pip"] + argv[3:], "pip"
        else:
            return
    subs = PACKAGE_MANAGERS.get(name)
    if subs is None:
        return
    args = argv[1:]
    if name in ("npm", "pnpm", "yarn", "bun") and any(a in ("-g", "--global", "--location=global") for a in args):
        deny(f"{name} global installs are never allowed (never-do 16)")
    if name == "yarn" and args[:1] == ["global"]:
        deny("yarn global is never allowed (never-do 16)")
    verbs = [a for a in args if not a.startswith("-")]
    verb = verbs[0] if verbs else ("install" if name in ("yarn", "bun", "npm", "pnpm", "bundle") and not args else "")
    if name == "uv" and verb == "run":
        return
    if name == "uv" and verb == "pip" and len(verbs) > 1 and verbs[1] in ("list", "show", "freeze", "tree", "check"):
        return
    if name == "go" and verb == "mod" and len(verbs) > 1 and verbs[1] in ("graph", "why", "verify", "download"):
        return
    if verb not in subs:
        return
    if verb in ("publish", "unpublish", "push"):
        deny(f"{name} {verb} publishes; no seat publishes (never-do 1, 8)")
    if name == "uv" and verb in ("tool", "self", "python"):
        deny(f"uv {verb} changes global tools (never-do 16)")
    if name == "cargo" and verb == "install" or name == "go" and verb == "install":
        deny(f"{name} install puts a global tool on the machine (never-do 16)")
    if ctx.seat == "coordinator":
        if not scripts_off(name, argv):
            deny(f"{name} {verb} runs install scripts; add the scripts-off flag (npm-family --ignore-scripts, pip --only-binary=:all:, uv --no-build) (never-do 12)")
        return
    deny(f"{name} {verb} changes dependencies; the coordinator runs the installs the plan names (never-do 12)")


def judge_simple(ctx: Context, s: shellparse.Simple) -> None:
    for w in s.writes:
        check_write(ctx, w, s.cwd, creating=True)
    for r in s.reads:
        check_read(ctx, r, s.cwd)
    if ctx.seat in ("builder", "release-reliability"):
        for e in s.env:
            if policy.SNAPSHOT_ENV.match(e):
                deny("regenerating snapshots or golden files edits a test (never-do 4)")
    argv = s.argv
    if not argv:
        return
    name = os.path.basename(argv[0])
    # Anything that names a credential or an employer path.
    for a in argv[1:]:
        for piece in ([a] + a.split("=", 1)[1:]):
            if "/" in piece or piece.startswith((".", "~")):
                check_read(ctx, piece, s.cwd)
        for m in re.finditer(r"\$\{?([A-Za-z_][A-Za-z0-9_]*)", a):
            if policy.CREDENTIAL_VAR.search(m.group(1)):
                deny(f"${m.group(1)} looks like a credential; never print one (never-do 6)")
    if name in ("env", "printenv", "set", "export", "declare", "typeset") and (len(argv) == 1 or argv[1:] in (["-p"], ["-x"], ["-0"])):
        deny("printing the environment can print a credential (never-do 6)")
    if name in DENY_ALWAYS:
        deny(f"{name} is never run by a seat (never-do 1, 8, 16)")
    if name in READ_ONLY_SUBS:
        if len(argv) < 2 or argv[1] not in READ_ONLY_SUBS[name]:
            deny(f"{name} {' '.join(argv[1:2])} changes the machine; only reading is allowed (never-do 8, 16)")
    if name == "crontab" and argv[1:] != ["-l"]:
        deny("crontab switches on unattended work (never-do 8)")
    if name in ("scutil", "networksetup", "pmset", "systemsetup", "nvram"):
        if not any(a.startswith(("--get", "-get", "-list", "-g")) for a in argv[1:]):
            deny(f"{name} changes system settings (never-do 16)")
    if name == "git":
        judge_git(ctx, argv, s.cwd)
    if name == "gh":
        judge_gh(argv)
    if name in ("cargo",) and argv[1:3] in (["insta", "accept"], ["insta", "review"]) and ctx.seat in ("builder", "release-reliability"):
        deny("accepting snapshots edits a test (never-do 4)")
    if name in ("docker", "podman") and len(argv) > 1 and argv[1] in ("push", "login"):
        deny(f"{name} {argv[1]} publishes or signs in (never-do 1, 6, 8)")
    judge_packages(ctx, name, argv)
    if ctx.seat in ("builder", "release-reliability"):
        runner = name in TEST_RUNNERS or any(os.path.basename(a) in TEST_RUNNERS for a in argv[1:4])
        for a in argv[1:]:
            if policy.SNAPSHOT_FLAGS.match(a) and (a != "-u" or runner):
                deny("regenerating snapshots or golden files edits a test (never-do 4)")
    for t in write_targets(argv):
        check_write(ctx, t, s.cwd, creating=name in ("touch", "mkdir", "tee", "cp", "install", "ln", "tar", "bsdtar", "gtar"))
    if name in ("python", "python3", "node", "ruby", "perl", "deno", "bun") and ctx.read_only:
        pass  # a read-only pass's sandbox holds; nothing to see in the text


def judge(ctx: Context, tool: str, tin: dict, cwd: str) -> None:
    if ctx.seat == "coordinator":
        cmd = command_text(tin)
        if cmd:
            for s in shellparse.parse(cmd, cwd):
                if s.argv:
                    judge_packages(ctx, os.path.basename(s.argv[0]), s.argv)
        return
    text = tin.get("command") if isinstance(tin.get("command"), str) else tin.get("patch") or tin.get("input")
    if tool == "apply_patch" or (isinstance(text, str) and text.lstrip().startswith("*** Begin Patch")):
        found = patch_paths(text if isinstance(text, str) else json.dumps(tin))
        if not found:
            deny("the guard cannot find the files in this patch")
        for kind, path in found:
            check_write(ctx, path, cwd, creating=(kind == "Add File"))
        return
    cmd = command_text(tin)
    if cmd is not None:
        try:
            simples = shellparse.parse(cmd, cwd)
        except shellparse.Unparseable as e:
            deny(f"the guard cannot read this command ({e}); split it into plain steps")
        for s in simples:
            judge_simple(ctx, s)
        return
    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        path = tin.get("file_path") or tin.get("notebook_path") or ""
        if not path:
            deny("no file path in the edit")
        check_write(ctx, path, cwd, creating=(tool == "Write"))
        return
    if tool in ("Read", "Glob", "Grep", "LS", "NotebookRead"):
        for key in ("file_path", "path", "notebook_path"):
            if tin.get(key):
                check_read(ctx, tin[key], cwd)
        pat = tin.get("pattern", "")
        if tool == "Glob" and isinstance(pat, str) and (pat.startswith(("/", "~"))):
            check_read(ctx, pat.split("*")[0] or "/", cwd)
        return
    if tool in ("WebFetch", "WebSearch"):
        deny("seats have no web tools; network is the plan's allowlist only (never-do 15)")
    if tool.startswith("mcp__"):
        deny("seats run with no MCP servers (bench, launch forms)")
    # Skill and other read-only built-ins pass.


def log(ctx: Optional[Context], record: dict) -> None:
    target = ctx.log if ctx else os.environ.get("DEVCRAFT_GUARD_LOG", "")
    if not target:
        return
    try:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")
    except OSError:
        pass


def main(stdin: str) -> int:
    ctx = None
    record = {"t": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "seat": os.environ.get("DEVCRAFT_SEAT", "")}
    try:
        event = json.loads(stdin or "{}")
        if event.get("hook_event_name") == "SessionStart":
            # The proof the guard loaded, written before the seat's first call.
            record["decision"] = "session-start"
            try:
                ctx = Context.from_env()
                ctx.test_paths()
                policy.employer_paths()
                record["seat"] = ctx.seat
            except ContextError as e:
                record["decision"] = f"session-start, but the guard cannot run: {e}"
                sys.stderr.write(f"Devcraft guard: every tool call will be refused ({e}).\n")
            log(ctx, record)
            return 0
        tool, tin, cwd = normalize(event)
        record.update(tool=tool, vendor="codex" if "turn_id" in event or tool in ("shell", "apply_patch", "local_shell") else "claude")
        record["input"] = (command_text(tin) or tin.get("file_path") or tin.get("path") or "")[:400]
        ctx = Context.from_env()
        record["seat"] = ctx.seat
        judge(ctx, tool, tin, cwd)
    except Verdict as v:
        record.update(decision="deny", reason=v.reason)
        log(ctx, record)
        sys.stderr.write(f"Devcraft guard: {v.reason}\n")
        return 2
    except (ContextError, ValueError, KeyError) as e:
        record.update(decision="deny", reason=f"guard cannot run: {e}")
        log(ctx, record)
        sys.stderr.write(f"Devcraft guard: refused, the guard cannot run ({e}). Stop and report Blocked.\n")
        return 2
    record["decision"] = "allow"
    log(ctx, record)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.stdin.read()))
