#!/usr/bin/env python3
"""Set up the wall for one seat pass, on either vendor.

    seat.py context   --seat S --worktree W --engagement E --pass NN [--branch B]
                      [--test-path P]... [--ops-path P]... [--grant-read F]...
                      [--grant-control F]... [--host H]...      → <E>/trace/logs/pass-NN.context.json
    seat.py claude-settings <context.json>                      → <E>/trace/logs/pass-NN.settings.json
    seat.py codex-home [--home ~/.codex-devcraft]                → the Codex seat home, its hooks trusted
    seat.py codex-pass <context.json> [--home ...]              → <home>/<eng>-pass-NN.config.toml
    seat.py worktree <worktree> --engagement E                  → that worktree's own git hooks
    seat.py launch <context.json> --prompt-file F [--budget USD] [--run]
    seat.py check [--home ...]                                  → preflight; exit 1 on any gap

The coordinator runs these; no seat does. Every plan-named exception reaches a
pass only through `context`, whose flags the coordinator copies from the plan
gate's frozen "Exceptions on the record" table. Written on the Devcraft build
map's "Build the never-do hooks and sandbox config" ticket (2026-10-11), from
the two vendors' probes that day (see README.md).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
import policy  # noqa: E402

HOOKS = Path(__file__).resolve().parent
GUARD = HOOKS / "guard.py"
PYTHON = "/usr/bin/python3"
GUARD_COMMAND = f"{PYTHON} {GUARD}"
DEFAULT_HOME = Path(os.path.expanduser("~/.codex-devcraft"))
STUDIOS = HOOKS.parents[1]
KEEP_ENV = ("HOME", "USER", "LOGNAME", "PATH", "LANG", "LC_ALL", "TMPDIR", "TERM", "SHELL")
CODEX_FEATURES_OFF = (
    "apps", "plugins", "remote_plugin", "multi_agent", "memories", "browser_use", "computer_use",
    "in_app_browser", "image_generation", "goals", "skill_mcp_dependency_install", "shell_snapshot",
)


def die(msg: str) -> None:
    sys.stderr.write(f"seat.py: {msg}\n")
    sys.exit(1)


def toml_str(s: str) -> str:
    return json.dumps(s)  # a JSON string is a valid TOML basic string


# --- the context ---------------------------------------------------------------

def cmd_context(a) -> None:
    if a.seat not in policy.ALL_ROLES:
        die(f"unknown seat {a.seat}")
    eng = policy.real(a.engagement)
    data = {
        "seat": a.seat, "worktree": policy.real(a.worktree), "engagement": eng, "branch": a.branch or "",
        "pass": a.pass_id, "test_paths_add": a.test_path, "ops_paths": a.ops_path,
        "grants": {"read": [policy.real(p) for p in a.grant_read], "control": a.grant_control},
        "hosts": a.host, "read_only": a.seat in policy.GATES or a.read_only,
        "log": os.path.join(eng, "trace", "logs", "guard.jsonl"),
    }
    ctx = policy.Context(data)  # validates: no exception for AGENTS.md, CLAUDE.md or skills
    ctx.test_paths()  # a repo without the floor stops at Open
    out = Path(eng) / "trace" / "logs" / f"pass-{a.pass_id}.context.json"
    if out.exists():
        die(f"{out} exists; a pass's context is written once (never-do 17)")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(out)


def load(path: str) -> policy.Context:
    return policy.Context(json.loads(Path(path).read_text()), source=policy.real(path))


# --- shared path lists ------------------------------------------------------------

def credential_denies(ctx: policy.Context) -> List[str]:
    out = [p for p in policy.CREDENTIAL_PATHS if policy.real(p) not in ctx.grant_read]
    for root, dirs, files in os.walk(ctx.worktree):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".venv")]
        for f in files:
            p = os.path.join(root, f)
            if policy.is_credential(p, ctx.grant_read):
                out.append(p)
    return out


def complement(ctx: policy.Context, allowed: List[str], depth: int = 4) -> List[str]:
    """Worktree paths no `allowed` pattern can reach, as coarsely as possible.

    The sandbox cannot say "everything but the test paths", so this lists what
    lies outside them as it stands now; a file created later is the guard's.
    """
    out: List[str] = []

    def could_hold(rel_dir: str) -> bool:
        for pat in allowed:
            p = pat.strip().lstrip("./").rstrip("/")
            if "/" not in p or policy.matches(rel_dir, p):
                return True
            static = re.split(r"[*?\[]", p, 1)[0]
            if static.startswith(rel_dir + "/") or (rel_dir + "/").startswith(static.rsplit("/", 1)[0] + "/") and any(c in p for c in "*?["):
                return True
        return False

    def walk(rel: str, level: int) -> None:
        base = os.path.join(ctx.worktree, rel)
        for name in sorted(os.listdir(base)):
            r = os.path.join(rel, name) if rel else name
            if name == ".git" or policy.any_match(r, allowed):
                continue
            full = os.path.join(ctx.worktree, r)
            if os.path.isdir(full) and not os.path.islink(full):
                if could_hold(r) and level < depth:
                    walk(r, level + 1)
                elif not could_hold(r):
                    out.append(full)
            else:
                out.append(full)

    walk("", 0)
    return out


def common_git_dir(worktree: str) -> str:
    r = subprocess.run(["git", "-C", worktree, "rev-parse", "--path-format=absolute", "--git-common-dir"],
                       capture_output=True, text=True)
    return policy.real(r.stdout.strip()) if r.returncode == 0 else ""


def worktree_git_dir(worktree: str) -> str:
    r = subprocess.run(["git", "-C", worktree, "rev-parse", "--path-format=absolute", "--git-dir"],
                       capture_output=True, text=True)
    return policy.real(r.stdout.strip()) if r.returncode == 0 else ""


# --- Claude seats -----------------------------------------------------------------

def claude_settings(ctx: policy.Context) -> Dict:
    if ctx.seat not in policy.CLAUDE_SEATS:
        die(f"{ctx.seat} is not a Claude seat")
    emp = policy.employer_paths()
    creds = credential_denies(ctx)
    no_read = creds + emp + [str(Path(ctx.engagement) / "held-out")] * (ctx.seat != "verifier")
    no_read = [p for p in no_read if p]
    gitdir, wtgit = common_git_dir(ctx.worktree), worktree_git_dir(ctx.worktree)
    controls = [os.path.join(ctx.worktree, c.rstrip("/")) for c in ctx.controls()
                if not any(policy.matches(c, g) for g in ctx.grant_control)]
    git_controls = [os.path.join(gitdir, "hooks"), os.path.join(gitdir, "config"), os.path.join(wtgit, "config.worktree")] if gitdir else []
    eng = Path(ctx.engagement)
    records = [str(eng / "trace"), str(eng / "brief.md"), str(eng / "handoff"), str(eng / "index.md")]
    records += [str(p) for p in eng.glob("d[0-9]*.md")]
    records += [str(p) for p in (eng / "audits").glob("*")]
    refs = [str(STUDIOS / "devcraft" / "lanes"), str(STUDIOS / "devcraft" / "corpus")]
    no_write = controls + git_controls + records + refs
    if ctx.seat == "build-planner":
        no_write.append(ctx.worktree)
    elif ctx.seat == "verifier":
        no_write += complement(ctx, ctx.test_paths())
    elif ctx.seat == "release-reliability":
        tests = ctx.test_paths()
        no_write += complement(ctx, ctx.ops_paths)
        no_write += [os.path.join(ctx.worktree, t.rstrip("/")) for t in tests if not any(c in t for c in "*?[")]

    def rule(tool: str, p: str) -> List[str]:
        return [f"{tool}(/{p})", f"{tool}(/{p}/**)"] if os.path.isdir(p) or not os.path.exists(p) else [f"{tool}(/{p})"]

    deny: List[str] = []
    for p in no_read:
        deny += rule("Read", p)
    deny += [f"Read(//{ctx.worktree.lstrip('/')}/**/.env)", f"Read(//{ctx.worktree.lstrip('/')}/**/.env.local)"]
    for p in no_write:
        deny += rule("Edit", p)
    deny += [f"Edit(//{ctx.worktree.lstrip('/')}/**/{c})" for c in (".claude/**", ".codex/**", ".agents/**", "AGENTS.md", "CLAUDE.md")]
    deny += [f"Bash({c}:*)" for c in ("sudo", "git push", "brew", "pipx", "crontab", "launchctl load", "launchctl bootstrap",
                                       "launchctl enable", "gh workflow", "gh pr create", "gh issue create", "npm publish", "security")]
    deny += ["WebFetch", "WebSearch", "Task", "Agent"]
    allow_write = []
    if ctx.seat in ("verifier", "release-reliability") and gitdir:
        allow_write = [os.path.join(gitdir, "objects"), wtgit]
        branch = ctx.branch or ""
        if branch:
            allow_write += [os.path.join(gitdir, "refs", "heads", os.path.dirname(branch)) if "/" in branch else os.path.join(gitdir, "refs", "heads"),
                            os.path.join(gitdir, "logs", "refs", "heads", os.path.dirname(branch)) if "/" in branch else os.path.join(gitdir, "logs", "refs", "heads")]
    return {
        "permissions": {"deny": sorted(set(deny)), "defaultMode": "acceptEdits", "disableBypassPermissionsMode": "disable"},
        "sandbox": {
            "enabled": True, "failIfUnavailable": True, "autoAllowBashIfSandboxed": True,
            "allowUnsandboxedCommands": False, "excludedCommands": [],
            "filesystem": {"denyRead": sorted(set(no_read)), "allowWrite": allow_write,
                           "denyWrite": sorted(set(no_write + git_controls))},
            "network": {"allowedDomains": list(ctx.hosts), "strictAllowlist": True},
        },
        "hooks": {"PreToolUse": [{"matcher": "*", "hooks": [{"type": "command", "command": GUARD_COMMAND, "timeout": 15}]}],
                  "SessionStart": [{"hooks": [{"type": "command", "command": GUARD_COMMAND, "timeout": 15}]}]},
        "env": {"DEVCRAFT_CONTEXT": ctx.source},
        "disableAllHooks": False,
    }


def cmd_claude_settings(a) -> None:
    ctx = load(a.context)
    out = Path(a.context).with_name(Path(a.context).name.replace(".context.json", ".settings.json"))
    out.write_text(json.dumps(claude_settings(ctx), indent=2) + "\n")
    print(out)


# --- Codex seats --------------------------------------------------------------------

def hooks_json() -> Dict:
    return {"hooks": {"PreToolUse": [{"matcher": "Bash|apply_patch", "hooks": [
        {"type": "command", "command": GUARD_COMMAND, "timeout": 15}]}]}}


def snake(event: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", event).lower()


def hook_hash(event: str, group: Dict, h: Dict) -> str:
    """Codex's trust fingerprint for one hook (codex-rs hooks discovery, 0.146)."""
    norm = {"type": "command", "command": h["command"], "timeout": max(1, int(h.get("timeout", 600))),
            "async": bool(h.get("async", False))}
    if h.get("statusMessage") is not None:
        norm["statusMessage"] = h["statusMessage"]
    ident = {"event_name": snake(event), "hooks": [norm]}
    if group.get("matcher") is not None:
        ident["matcher"] = group["matcher"]
    blob = json.dumps(ident, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(blob.encode()).hexdigest()


def floor_profile(name: str, extends: str, deny: List[str]) -> List[str]:
    lines = [f"[permissions.{name}]", f'extends = "{extends}"', f"[permissions.{name}.filesystem]"]
    lines += [f'{toml_str(p)} = "deny"' for p in deny]
    lines += [f"[permissions.{name}.network]", "enabled = false", ""]
    return lines


def cmd_codex_home(a) -> None:
    home = Path(os.path.expanduser(a.home))
    home.mkdir(parents=True, exist_ok=True)
    os.chmod(home, 0o700)
    hj = home / "hooks.json"
    data = hooks_json()
    hj.write_text(json.dumps(data, indent=2) + "\n")
    deny = list(policy.CREDENTIAL_PATHS) + policy.employer_paths()
    lines = [
        "# Devcraft's Codex seat home. Written by devcraft/hooks/seat.py codex-home; rewrite it, never hand-edit.",
        "# A pass layers <eng>-pass-NN.config.toml on top with -p; with no layer a pass gets the read-only floor.",
        'default_permissions = "devcraft-floor"', "",
        "[features]", *[f"{f} = false" for f in CODEX_FEATURES_OFF], "",
        "[skills]", "include_instructions = false", "",
        "[shell_environment_policy]", 'inherit = "all"', "ignore_default_excludes = false",
        'exclude = ["*TOKEN*", "*KEY*", "*SECRET*", "*PASSWORD*", "*CREDENTIAL*", "GH_*", "GITHUB_*", "DEVCRAFT_CONTEXT"]', "",
        *floor_profile("devcraft-floor", ":read-only", deny),
        "[hooks.state]",
    ]
    for event, groups in data["hooks"].items():
        for gi, g in enumerate(groups):
            for hi, h in enumerate(g["hooks"]):
                lines += [f'[hooks.state.{toml_str(f"{hj}:{snake(event)}:{gi}:{hi}")}]',
                          f'trusted_hash = "{hook_hash(event, g, h)}"', "enabled = true"]
    (home / "config.toml").write_text("\n".join(lines) + "\n")
    print(home)
    if not (home / "auth.json").exists():
        print(f"Next, Sean signs this home in once: CODEX_HOME={home} codex login")


def codex_layer(ctx: policy.Context) -> List[str]:
    name = f"pass-{Path(ctx.source).name.split('.')[0].split('pass-')[-1]}"
    deny = credential_denies(ctx) + policy.employer_paths() + [os.path.join(ctx.engagement, "held-out")]
    rel_read: List[str] = []
    if ctx.seat == "builder":
        for c in ctx.controls():
            # listed even when absent, so the Builder cannot create one either
            if not any(policy.matches(c, g) for g in ctx.grant_control):
                rel_read.append(c.rstrip("/"))
        for t in ctx.test_paths() + ctx.ops_paths:
            t = t.strip().lstrip("./").rstrip("/")
            if t and not any(ch in t for ch in "*?[") and os.path.exists(os.path.join(ctx.worktree, t)):
                rel_read.append(t)
        for must in (".git", ".codex"):
            if must not in rel_read and os.path.exists(os.path.join(ctx.worktree, must)):
                rel_read.append(must)
    extends = ":workspace" if ctx.seat == "builder" and not ctx.read_only else ":read-only"
    lines = [f"# Devcraft pass layer for {ctx.source}. Written by seat.py codex-pass; rewrite it, never hand-edit.",
             f'default_permissions = "{name}"', "",
             f"[projects.{toml_str(ctx.worktree)}]", 'trust_level = "untrusted"', ""]
    lines += [f"[permissions.{name}]", f'extends = "{extends}"', f"[permissions.{name}.filesystem]"]
    lines += [f'{toml_str(p)} = "deny"' for p in sorted(set(deny))]
    lines += [f'{toml_str(ctx.engagement)} = "read"']  # the coordinator's; -o files the final message
    if rel_read:
        lines += [f'[permissions.{name}.filesystem.":workspace_roots"]']
        lines += [f'{toml_str(p)} = "read"' for p in sorted(set(rel_read))]
    lines += [f"[permissions.{name}.network]", "enabled = false", ""]
    return lines


def cmd_codex_pass(a) -> None:
    ctx = load(a.context)
    if ctx.seat not in policy.CODEX_SEATS:
        die(f"{ctx.seat} is not a Codex seat")
    home = Path(os.path.expanduser(a.home))
    eng_id = os.path.basename(ctx.engagement)
    pass_id = Path(a.context).name.split(".")[0]
    profile = f"{eng_id}-{pass_id}"
    text = "\n".join(codex_layer(ctx)) + "\n"
    (home / f"{profile}.config.toml").write_text(text)
    Path(a.context).with_name(f"{pass_id}.codex-layer.toml").write_text(text)  # the record's copy
    print(profile)


# --- git hooks per build worktree ---------------------------------------------------

def cmd_worktree(a) -> None:
    wt = policy.real(a.worktree)
    if worktree_git_dir(wt) == common_git_dir(wt):
        die(f"{wt} is a main checkout; Devcraft's git hooks go on a build worktree only")
    run = lambda *x: subprocess.run(["git", "-C", wt, *x], check=True)  # noqa: E731
    run("config", "extensions.worktreeConfig", "true")
    run("config", "--worktree", "core.hooksPath", str(HOOKS / "git"))
    run("config", "--worktree", "devcraft.engagement", policy.real(a.engagement))
    print(f"{wt}: core.hooksPath → {HOOKS / 'git'} (this worktree only)")


# --- launch -----------------------------------------------------------------------

def launch_argv(ctx: policy.Context, prompt: str, budget: str, home: Path, profile: str = "") -> List[str]:
    if ctx.seat in policy.CLAUDE_SEATS:
        settings = ctx.source.replace(".context.json", ".settings.json")
        plugin = str(STUDIOS / "devcraft" / "bench" / "plugins" / ctx.seat)
        argv = ["claude", "-p", "--output-format", "json", "--model", "claude-opus-5-5",
                "--permission-mode", "acceptEdits", "--setting-sources", "", "--settings", settings,
                "--strict-mcp-config", "--tools", "Read,Write,Edit,Bash,Glob,Grep,Skill"]
        if os.path.isdir(plugin):
            argv += ["--plugin-dir", plugin]
        agents = os.path.join(ctx.worktree, "AGENTS.md")
        if os.path.exists(agents):
            argv += ["--append-system-prompt-file", agents]
        for d in (ctx.worktree, ctx.engagement, str(STUDIOS / "devcraft" / "lanes"), str(STUDIOS / "devcraft" / "corpus")):
            argv += ["--add-dir", d]
        argv += ["--max-budget-usd", budget, prompt]
        return argv
    # #99: the Builder pin changes independently of the shared gate default.
    model = "gpt-6.1-sol" if ctx.seat == "builder" else "gpt-5.6-sol"
    effort = "high"
    pass_id = Path(ctx.source).name.split(".")[0]
    return ["codex", "exec", "--json", "--model", model, "-c", f'model_reasoning_effort="{effort}"',
            "-p", profile, "--strict-config", "-c", 'web_search="disabled"', "-C", ctx.worktree,
            "-o", os.path.join(ctx.engagement, "trace", "logs", f"{pass_id}.last.md"), prompt]


def scrubbed_env(ctx: policy.Context, home: Path) -> Dict[str, str]:
    env = {k: os.environ[k] for k in KEEP_ENV if k in os.environ}
    env["DEVCRAFT_CONTEXT"] = ctx.source
    env["DEVCRAFT_SEAT"] = ctx.seat
    if ctx.seat in policy.CODEX_SEATS:
        env["CODEX_HOME"] = str(home)
    return env


def cmd_launch(a) -> None:
    ctx = load(a.context)
    home = Path(os.path.expanduser(a.home))
    prompt = Path(a.prompt_file).read_text()
    profile = ""
    if ctx.seat in policy.CODEX_SEATS:
        profile = f"{os.path.basename(ctx.engagement)}-{Path(a.context).name.split('.')[0]}"
        if not (home / f"{profile}.config.toml").exists():
            die(f"no Codex layer {profile}; run seat.py codex-pass first")
    elif not Path(ctx.source.replace(".context.json", ".settings.json")).exists():
        die("no seat settings; run seat.py claude-settings first")
    argv = launch_argv(ctx, prompt, a.budget, home, profile)
    env = scrubbed_env(ctx, home)
    print(json.dumps({"argv": argv[:-1] + ["<prompt>"], "env": sorted(env)}, indent=1), file=sys.stderr)
    if a.run:
        os.chdir(ctx.worktree)
        os.execvpe(argv[0], argv, env)


# --- preflight ----------------------------------------------------------------------

def cmd_check(a) -> None:
    gaps = []
    for label, fn in (("employer-path list", policy.employer_paths), ("name list", policy.names)):
        try:
            fn()
        except policy.ContextError as e:
            gaps.append(str(e))
    for tool in ("/opt/homebrew/bin/gitleaks", "/opt/homebrew/bin/osv-scanner", PYTHON):
        if not os.access(tool, os.X_OK):
            gaps.append(f"missing {tool}")
    if not os.access(GUARD, os.R_OK):
        gaps.append(f"the guard is not at {GUARD}")
    home = Path(os.path.expanduser(a.home))
    if not (home / "auth.json").exists():
        gaps.append(f"the Codex seat home has no sign-in (CODEX_HOME={home} codex login)")
    hj = home / "hooks.json"
    if hj.exists():
        data = json.loads(hj.read_text())
        cfg = (home / "config.toml").read_text() if (home / "config.toml").exists() else ""
        for event, groups in data["hooks"].items():
            for gi, g in enumerate(groups):
                for hi, h in enumerate(g["hooks"]):
                    if hook_hash(event, g, h) not in cfg:
                        gaps.append(f"Codex hook {event}:{gi}:{hi} is not trusted at its current hash (it would be skipped silently)")
                    if h["command"] != GUARD_COMMAND:
                        gaps.append(f"Codex hook {event}:{gi}:{hi} does not run the guard")
    else:
        gaps.append(f"no Codex seat home at {home} (seat.py codex-home)")
    for g in gaps:
        print(f"GAP: {g}")
    print("preflight: " + ("clean" if not gaps else f"{len(gaps)} gap(s)"))
    sys.exit(1 if gaps else 0)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("context")
    c.add_argument("--seat", required=True)
    c.add_argument("--worktree", required=True)
    c.add_argument("--engagement", required=True)
    c.add_argument("--pass", dest="pass_id", required=True)
    c.add_argument("--branch", default="")
    for f in ("test-path", "ops-path", "grant-read", "grant-control", "host"):
        c.add_argument(f"--{f}", action="append", default=[])
    c.add_argument("--read-only", action="store_true")
    c.set_defaults(fn=cmd_context)
    s = sub.add_parser("claude-settings")
    s.add_argument("context")
    s.set_defaults(fn=cmd_claude_settings)
    h = sub.add_parser("codex-home")
    h.add_argument("--home", default=str(DEFAULT_HOME))
    h.set_defaults(fn=cmd_codex_home)
    p = sub.add_parser("codex-pass")
    p.add_argument("context")
    p.add_argument("--home", default=str(DEFAULT_HOME))
    p.set_defaults(fn=cmd_codex_pass)
    w = sub.add_parser("worktree")
    w.add_argument("worktree")
    w.add_argument("--engagement", required=True)
    w.set_defaults(fn=cmd_worktree)
    l = sub.add_parser("launch")  # noqa: E741
    l.add_argument("context")
    l.add_argument("--prompt-file", required=True)
    l.add_argument("--budget", default="5")
    l.add_argument("--home", default=str(DEFAULT_HOME))
    l.add_argument("--run", action="store_true")
    l.set_defaults(fn=cmd_launch)
    k = sub.add_parser("check")
    k.add_argument("--home", default=str(DEFAULT_HOME))
    k.set_defaults(fn=cmd_check)
    a = ap.parse_args()
    try:
        a.fn(a)
    except policy.ContextError as e:
        die(str(e))


if __name__ == "__main__":
    main()
