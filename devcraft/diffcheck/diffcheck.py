#!/usr/bin/env python3
"""Devcraft's diff check: the after-check layer of the never-do list.

    diffcheck.py --worktree W --engagement E [--base C] [--candidate C] [--branch B]
                 [--test-path P]... [--ops-path P]... [--out FILE] [--offline]

A model-free comparison of a build branch with its base, run by the coordinator
(never a seat) before every push and once more to build the release gate's
packet. It reads the wall's rules from `devcraft/hooks/policy.py`, the frozen
exceptions from the plan gate's findings, and writes one report into the
engagement's `evidence/`, which rung 0 hashes without reading code.

What it scans for, from the never-do ticket's diff-check column:

- each seat's commits inside its paths: the Verifier in the test paths (the
  repo's `.devcraft/test-paths` floor at the base commit, plus the plan's
  additions), the Builder outside them and outside Release's flagged ops
  paths, Release inside its ops paths only (never-do 4);
- skip and xfail markers, deleted tests, lowered thresholds, lint and type
  suppressions, changed timeouts, CI and check-config edits (never-do 5);
- credential files and credential values, the latter through gitleaks by full
  path (never-do 6);
- new launchd, cron, timer and scheduled-workflow files (never-do 8);
- manifest and lockfile changes, with a registry lookup for every new package
  recording that it exists, its age and its maintainers (never-do 12);
- control-file edits (never-do 14);
- a listed name in anything the range adds (never-do 11).

The matching rule: a hit must match a row of the plan gate's frozen
"Exceptions on the record" table (by kind and by what the row names), or a
ledger entry of this engagement that Sean ratified (`ratified: <date>`) and that
names the hit. An unmatched hit is a release-gate finding. A push to a default
branch, or a control edit no exception names, fails outright.

Exit 0: clean. Exit 1: findings, recorded for the release gate (a push may
proceed). Exit 2: refused (the push fails). The report is written in every case
it can be.

Stdlib only, Python 3.9 or later. Written on the Devcraft build map's "Build the
diff check" ticket (2026-10-12).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "hooks"))
import policy  # noqa: E402

GITLEAKS = [os.environ.get("DEVCRAFT_GITLEAKS", ""), "/opt/homebrew/bin/gitleaks", "/usr/local/bin/gitleaks"]
DEFAULT_BRANCHES = ("main", "master")

# --- what the scan looks for ---------------------------------------------------

SNAPSHOT_PATHS = ("__snapshots__/", "__image_snapshots__/", "snapshots/", "*.snap", "*.golden")
CI_PATHS = (".github/workflows/", ".gitlab-ci.yml", ".circleci/", "Jenkinsfile", ".travis.yml",
            "azure-pipelines.yml", "bitbucket-pipelines.yml", ".buildkite/", ".drone.yml")
CHECK_CONFIG = ("pytest.ini", "tox.ini", "setup.cfg", ".coveragerc", "conftest.py", "jest.config.*",
                "vitest.config.*", ".eslintrc*", "eslint.config.*", "ruff.toml", ".ruff.toml", "mypy.ini",
                "pyrightconfig.json", "codecov.yml", ".codecov.yml", "sonar-project.properties",
                ".pylintrc", "pylintrc", ".flake8", "Makefile", "noxfile.py", "biome.json", ".mocharc*")
PYPROJECT_CHECK_LINE = re.compile(r"(addopts|--ignore|--deselect|fail_under|fail-under|exclude|omit|skip|xfail_strict|"
                                  r"markers|filterwarnings|timeout|\[tool\.(pytest|coverage|ruff|mypy|pyright))", re.I)
SKIP_MARK = re.compile(
    r"(@pytest\.mark\.(skip|skipif|xfail)|pytest\.(skip|xfail|importorskip)\(|@unittest\.(skip|skipIf|skipUnless|expectedFailure)|"
    r"unittest\.SkipTest|\b(it|test|describe|context|suite)\.(skip|only|todo|fixme)\s*\(|\bx(it|test|describe)\s*\(|"
    r"\bf(it|describe)\s*\(|#\[ignore\b|\bt\.(Skip|SkipNow|Skipf)\(|@Disabled\b|@Ignore\b|\.skip\s*=\s*true|"
    r"\bpending\s*\(|\bskip:\s*true)")
SUPPRESS_MARK = re.compile(
    r"(#\s*noqa|#\s*type:\s*ignore|#\s*ruff:\s*noqa|#\s*flake8:\s*noqa|#\s*pylint:\s*disable|#\s*pyright:\s*ignore|"
    r"#\s*mypy:\s*(ignore|disable)|#\s*nosec|#\s*pragma:\s*no\s*cover|#\s*shellcheck\s+disable|"
    r"eslint-disable|@ts-ignore|@ts-expect-error|@ts-nocheck|/\*\s*istanbul\s+ignore|//\s*nolint|//\s*NOSONAR|"
    r"#\[allow\(|@SuppressWarnings|#\s*noinspection|rubocop:disable|prettier-ignore)", re.I)
THRESHOLD_MARK = re.compile(r"(fail[_-]?under|coverageThreshold|min(imum)?[_-]?coverage|coverage[_-]?threshold|"
                            r"\bthreshold\b|\bbranches\s*[:=]\s*\d|\blines\s*[:=]\s*\d|\bstatements\s*[:=]\s*\d|"
                            r"\bfunctions\s*[:=]\s*\d)", re.I)
TIMEOUT_MARK = re.compile(r"\btimeout", re.I)
TEST_NAME = [
    re.compile(r"^\s*(?:async\s+)?def\s+(test_\w+)", re.M),
    re.compile(r"\b(?:it|test)\s*\(\s*['\"`]([^'\"`\n]+)", re.M),
    re.compile(r"#\[(?:tokio::)?test[^\]]*\]\s*(?:async\s+)?fn\s+(\w+)", re.M),
    re.compile(r"^\s*func\s+(Test\w+)\s*\(", re.M),
    re.compile(r"^\s*@Test\b[^\n]*\n\s*(?:public\s+)?(?:void\s+)?(\w+)\s*\(", re.M),
]
UNATTENDED_PATHS = ("LaunchAgents/", "LaunchDaemons/", "crontab", "crontab.*", "*.cron", "cron.d/", "*.timer",
                    "*.service", "cron/", "routines/")
PLIST_JOB = re.compile(r"<key>(StartCalendarInterval|StartInterval|RunAtLoad|KeepAlive|WatchPaths)</key>")
SCHEDULE_LINE = re.compile(r"^\s*(schedule:|-?\s*cron:|StartCalendarInterval|StartInterval|OnCalendar=)", re.M)
ENV_PATHS = (".env", ".env.*")

MANIFESTS = {
    "package.json": "npm", "pyproject.toml": "pypi", "requirements.txt": "pypi", "requirements-*.txt": "pypi",
    "requirements/*.txt": "pypi", "Pipfile": "pypi", "setup.py": "pypi", "setup.cfg": "pypi", "Cargo.toml": "crates",
    "go.mod": "go", "Gemfile": "rubygems", "*.gemspec": "rubygems",
}
LOCKFILES = ("package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "bun.lock",
             "uv.lock", "poetry.lock", "Pipfile.lock", "pdm.lock", "Cargo.lock", "go.sum", "Gemfile.lock",
             "composer.lock", "flake.lock")
LOCK_ECOSYSTEM = {"package-lock.json": "npm", "npm-shrinkwrap.json": "npm", "yarn.lock": "npm", "pnpm-lock.yaml": "npm",
                  "bun.lockb": "npm", "bun.lock": "npm", "uv.lock": "pypi", "poetry.lock": "pypi", "Pipfile.lock": "pypi",
                  "pdm.lock": "pypi", "Cargo.lock": "crates", "go.sum": "go", "Gemfile.lock": "rubygems"}
REQ_NAME = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")
EX_KIND = {"skip": "skip", "credential": "credential", "credential file": "credential", "dependency": "dependency",
           "control": "control", "control file": "control", "host": "host"}
TRAILER = re.compile(r"^Devcraft-Seat:\s*(\S+)\s*$", re.M)


class Refuse(Exception):
    pass


# --- git ---------------------------------------------------------------------------

class Git:
    def __init__(self, worktree: str):
        self.wt = worktree

    def run(self, *args: str, check: bool = True) -> str:
        r = subprocess.run(["git", "-C", self.wt, *args], capture_output=True, text=True)
        if check and r.returncode != 0:
            raise Refuse(f"git {' '.join(args[:2])} failed: {r.stderr.strip()[:200]}")
        return r.stdout

    def rev(self, ref: str) -> str:
        return self.run("rev-parse", "--verify", f"{ref}^{{commit}}").strip()

    def show(self, commit: str, path: str) -> Optional[str]:
        r = subprocess.run(["git", "-C", self.wt, "show", f"{commit}:{path}"], capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None

    def exists(self, commit: str, path: str) -> bool:
        return subprocess.run(["git", "-C", self.wt, "cat-file", "-e", f"{commit}:{path}"], capture_output=True).returncode == 0

    def commits(self, base: str, cand: str) -> List[Dict]:
        out = []
        raw = self.run("log", "--reverse", "--format=%H%x00%B%x01", f"{base}..{cand}")
        for chunk in raw.split("\x01"):
            if not chunk.strip():
                continue
            sha, _, body = chunk.lstrip("\n").partition("\x00")
            files = self.run("diff-tree", "--no-commit-id", "-r", "--name-status", "-M", "--root", sha)
            paths = []
            for line in files.splitlines():
                parts = line.split("\t")
                if len(parts) >= 2:
                    status = parts[0][0]
                    paths.append((status, parts[-1]))  # a rename's new name
            out.append({"sha": sha, "message": body.strip(), "paths": paths})
        return out

    def changed(self, base: str, cand: str) -> List[Tuple[str, str]]:
        out = []
        for line in self.run("diff", "--name-status", "-M", f"{base}..{cand}").splitlines():
            parts = line.split("\t")
            if len(parts) >= 2:
                out.append((parts[0][0], parts[-1]))
        return out

    def added_lines(self, base: str, cand: str, path: str) -> List[Tuple[int, str]]:
        """(line number in the candidate, text) for every added line of one file."""
        diff = self.run("diff", "--no-color", "-U0", "--no-ext-diff", f"{base}..{cand}", "--", path)
        out, n = [], 0
        for line in diff.splitlines():
            m = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)", line)
            if m:
                n = int(m.group(1))
                continue
            if line.startswith("+") and not line.startswith("+++"):
                out.append((n, line[1:]))
                n += 1
            elif line.startswith("-") and not line.startswith("---"):
                pass
            elif not line.startswith("\\"):
                n += 1
        return out

    def branch(self) -> str:
        return self.run("symbolic-ref", "-q", "--short", "HEAD", check=False).strip()


# --- the engagement's record --------------------------------------------------------

def frontmatter(text: str) -> Dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    out = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*(#.*)?$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def section(text: str, heading: str) -> str:
    """The body under the first `## <heading>…` line, up to the next `## `."""
    m = re.search(r"^## " + re.escape(heading) + r".*?$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def table_rows(text: str) -> List[List[str]]:
    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c) or not any(cells):
            continue
        rows.append(cells)
    return rows[1:] if rows else []  # drop the header


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def backticked(text: str) -> List[str]:
    return [t.strip() for t in re.findall(r"`([^`]+)`", text)]


def mentions(text: str, subject: str) -> bool:
    """Does an exception row or a ledger entry name `subject` (a path, a package, a test name)?"""
    if not subject:
        return False
    s = subject.strip().strip("/")
    for span in backticked(text):
        span_s = span.strip().strip("/")
        if span_s == s or span_s.split("==")[0].split("@")[0].strip() == s:
            return True
        if any(c in span_s for c in "*?[") and policy.matches(s, span_s):
            return True
        if "/" in span_s and s.startswith(span_s + "/"):
            return True
    return re.search(r"(?<![\w./-])" + re.escape(s) + r"(?![\w.-])", text) is not None


class Record:
    """What the engagement folder says: the frozen exceptions, the plan's path lists, Sean's yeses."""

    def __init__(self, engagement: str):
        self.eng = Path(engagement)
        self.notes: List[str] = []
        self.brief = frontmatter((self.eng / "brief.md").read_text(encoding="utf-8")) if (self.eng / "brief.md").is_file() else {}
        m = re.match(r"^([a-z]{2}-eng-\d+)", self.brief.get("id", "")) or re.match(r"^([a-z]{2}-eng-\d+)", self.eng.name)
        self.eng_id = m.group(1) if m else self.eng.name
        self.gate_file: Optional[Path] = None
        self.anchor_sha = ""
        self.plan_file: Optional[Path] = None
        self.plan_source = ""
        self.exceptions: List[Dict[str, str]] = []
        self.plan_frozen = False
        self.test_paths_add: List[str] = []
        self.ops_paths: List[str] = []
        self.yeses: List[Dict[str, str]] = []
        self._read_gate()
        self._read_plan()
        self._read_yeses()

    def _read_gate(self) -> None:
        gates = sorted((self.eng / "audits").glob("plan-gate*.md")) if (self.eng / "audits").is_dir() else []

        def rank(p: Path) -> int:
            m = re.search(r"-r(\d+)\.md$", p.name)
            return int(m.group(1)) if m else 1

        if not gates:
            self.notes.append("no plan gate on record: no exception is honored")
            return
        self.gate_file = max(gates, key=rank)
        text = self.gate_file.read_text(encoding="utf-8")
        fm = frontmatter(text)
        self.anchor_sha = fm.get("anchor_sha256", "")
        for row in table_rows(section(text, "Exceptions on the record")):
            if len(row) < 3 or not re.fullmatch(r"EX\d+", row[0]):
                continue
            kind = EX_KIND.get(row[1].lower().strip(), "")
            if not kind:
                self.notes.append(f"{row[0]} has an unknown kind {row[1]!r} and is not honored")
                continue
            self.exceptions.append({"id": row[0], "kind": kind, "what": row[2], "seat": row[3] if len(row) > 3 else ""})

    def _gate_anchor(self) -> Optional[Tuple[str, str]]:
        """The anchor the plan gate's pass named, from the launch record that filed the gate file.

        `seat.py launch` records the anchor a gate was given (`vendor_basis`) beside
        the file it filed (`outputs`), so a redraft filed under a new name by `-o`
        is found where the gate read it (SWCB #145). None when no launch record
        filed this gate file: a gate filed by hand reads `artifacts/build-plan.md`.
        """
        logs = self.eng / "trace" / "logs"
        if not self.gate_file or not logs.is_dir():
            return None
        gate = str(self.gate_file.relative_to(self.eng))
        for rec in sorted(logs.glob("pass-*.launch.json")):
            try:
                data = json.loads(rec.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            basis = data.get("vendor_basis") or {}
            if data.get("seat") != "plan-gate" or basis.get("by") != "anchor" or not basis.get("path"):
                continue
            if any(o.get("path") == gate for o in data.get("outputs") or []):
                return basis["path"], data.get("pass") or rec.name.split(".")[0]
        return None

    def _read_plan(self) -> None:
        named = self._gate_anchor()
        rel = named[0] if named else "artifacts/build-plan.md"
        self.plan_source = f"the anchor {named[1]} named" if named else "by name"
        plan = (self.eng / rel).resolve()
        inside = os.path.relpath(plan, self.eng.resolve())
        if inside.startswith("..") or inside.split(os.sep)[0] not in ("artifacts", "inherited") or inside.count(os.sep) < 1:
            self.notes.append(f"the plan gate's anchor {rel} is not in artifacts/ or inherited/: its path additions are not honored")
            return
        if not plan.is_file():
            if named:
                self.notes.append(f"the plan gate's anchor {rel} is missing: its path additions are not honored")
            return
        self.plan_file = plan
        if not self.gate_file:
            self.notes.append("a build plan with no plan gate on record: its additions are not honored")
            return
        actual = sha256(plan)
        if actual != self.anchor_sha:
            self.notes.append(f"the build plan was edited after the plan gate read it (anchor {self.anchor_sha[:12]}, "
                              f"on disk {actual[:12]}): its path additions are void until the plan gate re-runs")
            return
        self.plan_frozen = True
        text = plan.read_text(encoding="utf-8")
        m = re.search(r"\*\*Test paths added:\*\*(.*)$", text, re.M)
        if m:
            self.test_paths_add = [p for p in backticked(m.group(1)) if p.lower() != "none"]
        for row in table_rows(section(text, "Interfaces and data changes")):
            if row and re.fullmatch(r"OP\d+", row[0]) and len(row) > 1:
                paths = backticked(row[1]) or [row[1]]
                self.ops_paths += [p for p in paths if p]

    def _read_yeses(self) -> None:
        for entry in sorted(self.eng.glob("d[0-9]*.md")):
            text = entry.read_text(encoding="utf-8")
            fm = frontmatter(text)
            when = fm.get("ratified", "")
            if when and when.lower() not in ("null", "none", "~", ""):
                self.yeses.append({"id": fm.get("id", entry.name), "date": when, "text": text, "file": entry.name})

    def match(self, kind: Optional[str], subjects: Iterable[str]) -> Optional[str]:
        """The exception id or ratified ledger entry that covers a hit, or None.

        `kind` None means no exception kind exists for the hit (an unattended
        file), so only a ratified entry can cover it.
        """
        subjects = [s for s in subjects if s]
        for ex in self.exceptions:
            if kind and ex["kind"] == kind and any(mentions(ex["what"], s) for s in subjects):
                return ex["id"]
        for y in self.yeses:
            if any(mentions(y["text"], s) for s in subjects):
                return f"{y['id']} (ratified {y['date']})"
        return None


# --- seat attribution -------------------------------------------------------------------

def seat_of(commit: Dict, eng_id: str) -> str:
    m = TRAILER.search(commit["message"])
    if m:
        return m.group(1)
    if re.match(r"^" + re.escape(eng_id) + r"\s+S\d+\b", commit["message"]):
        return "builder"  # the coordinator's commit of a Builder slice, named paths only
    return ""


# --- dependencies ---------------------------------------------------------------------

def ecosystem(path: str) -> str:
    name = os.path.basename(path)
    for pat, eco in MANIFESTS.items():
        if policy.matches(path, pat) or policy.matches(name, pat):
            return eco
    return ""


def package_names(path: str, text: str) -> List[str]:
    eco = ecosystem(path)
    base = os.path.basename(path)
    names: List[str] = []
    if base == "package.json":
        try:
            data = json.loads(text)
        except ValueError:
            return []
        for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
            names += list((data.get(key) or {}).keys())
    elif base == "pyproject.toml":
        sect, in_array = "", False
        for line in text.splitlines():
            m = re.match(r"^\s*\[([^\]]+)\]", line)
            if m and not in_array:
                sect = m.group(1).strip()
                continue
            dep_sect = re.search(r"(^|\.)(dependencies|dev-dependencies|optional-dependencies|dependency-groups)(\.|$)", sect)
            if dep_sect and not in_array:
                k = re.match(r"^\s*\"?([A-Za-z0-9][A-Za-z0-9._-]*)\"?\s*=\s*(?!\[)", line)
                if k and k.group(1) not in ("python",):
                    names.append(k.group(1))
            opens = re.match(r"^\s*\"?([A-Za-z0-9][A-Za-z0-9._-]*)\"?\s*=\s*\[", line)
            if opens and (opens.group(1) in ("dependencies", "dev-dependencies") or dep_sect):
                in_array = True
            if in_array:
                for s_ in re.findall(r"[\"']([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?\s*(?:[<>=!~;@ ][^\"']*)?[\"']", line):
                    names.append(s_)
                if "]" in line.split("#")[0]:
                    in_array = False
    elif base in ("Pipfile",):
        sect = ""
        for line in text.splitlines():
            m = re.match(r"^\s*\[([^\]]+)\]", line)
            if m:
                sect = m.group(1)
                continue
            if "packages" in sect:
                k = re.match(r"^\s*\"?([A-Za-z0-9][A-Za-z0-9._-]*)\"?\s*=", line)
                if k:
                    names.append(k.group(1))
    elif eco == "pypi":  # requirements*.txt, setup.py, setup.cfg: every requirement-looking line or string
        for line in text.splitlines():
            line = line.split("#")[0].strip()
            if not line or line.startswith(("-", ".", "/")):
                continue
            m = REQ_NAME.match(line)
            if m and base.startswith("requirements"):
                names.append(m.group(1))
        if not base.startswith("requirements"):
            names += re.findall(r"[\"']([A-Za-z0-9][A-Za-z0-9._-]*)\s*(?:\[[^\]]*\])?\s*(?:[<>=!~;][^\"']*)?[\"']", text)
    elif base == "Cargo.toml":
        sect = ""
        for line in text.splitlines():
            m = re.match(r"^\s*\[([^\]]+)\]", line)
            if m:
                sect = m.group(1).strip()
                continue
            if re.search(r"(^|\.)(dependencies|dev-dependencies|build-dependencies)$", sect):
                k = re.match(r"^\s*([A-Za-z0-9][A-Za-z0-9_-]*)\s*=", line)
                if k:
                    names.append(k.group(1))
            m2 = re.match(r"^\s*\[(?:.*\.)?dependencies\.([A-Za-z0-9_-]+)\]", "[" + sect + "]")
            if m2:
                names.append(m2.group(1))
    elif base == "go.mod":
        block = False
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("require ("):
                block = True
                continue
            if block and s == ")":
                block = False
                continue
            m = re.match(r"^(?:require\s+)?([A-Za-z0-9][\w./-]*)\s+v\S+", s) if (block or s.startswith("require ")) else None
            if m and "// indirect" not in s:
                names.append(m.group(1))
    elif eco == "rubygems":
        names += re.findall(r"^\s*(?:gem|spec\.add_(?:runtime_|development_)?dependency)\s*\(?\s*[\"']([^\"']+)[\"']", text, re.M)
    seen, out = set(), []
    for n in names:
        key = n.lower()
        if key not in seen:
            seen.add(key)
            out.append(n)
    return out


def fetch_json(url: str) -> Optional[Dict]:
    req = urllib.request.Request(url, headers={"User-Agent": "devcraft-diffcheck/1 (+https://github.com/seanwinslow28)",
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def registry_lookup(eco: str, name: str, offline: bool) -> Dict[str, str]:
    """{exists, first_release, age_days, maintainers, note}. Never raises."""
    fixture = os.environ.get("DIFFCHECK_REGISTRY_FIXTURE")
    if fixture:
        data = json.loads(Path(fixture).read_text(encoding="utf-8"))
        hit = data.get(f"{eco}:{name}")
        return hit if hit else {"exists": "no", "note": "not on the registry (fixture)"}
    if offline:
        return {"exists": "?", "note": "not looked up (--offline)"}
    try:
        today = dt.datetime.now(dt.timezone.utc)
        if eco == "npm":
            d = fetch_json(f"https://registry.npmjs.org/{name}")
            created = (d.get("time") or {}).get("created", "")
            maint = ", ".join(m.get("name", "") for m in d.get("maintainers", []))[:200]
        elif eco == "pypi":
            d = fetch_json(f"https://pypi.org/pypi/{name}/json")
            dates = [f.get("upload_time_iso_8601", "") for files in (d.get("releases") or {}).values() for f in files]
            created = min(x for x in dates if x) if any(dates) else ""
            info = d.get("info") or {}
            maint = ", ".join(x for x in (info.get("maintainer") or "", info.get("author") or "") if x)[:200]
        elif eco == "crates":
            d = fetch_json(f"https://crates.io/api/v1/crates/{name}")
            created = (d.get("crate") or {}).get("created_at", "")
            owners = fetch_json(f"https://crates.io/api/v1/crates/{name}/owners") or {}
            maint = ", ".join(u.get("login", "") for u in owners.get("users", []))[:200]
        elif eco == "go":
            d = fetch_json(f"https://proxy.golang.org/{name.lower()}/@latest")
            created = d.get("Time", "")
            maint = "module host: " + name.split("/")[0]
        elif eco == "rubygems":
            d = fetch_json(f"https://rubygems.org/api/v1/gems/{name}.json")
            versions = fetch_json(f"https://rubygems.org/api/v1/versions/{name}.json") or []
            created = min((v.get("created_at", "") for v in versions if v.get("created_at")), default="")
            maint = (d.get("authors") or "")[:200]
        else:
            return {"exists": "?", "note": f"no registry known for {eco}"}
        age = ""
        if created:
            try:
                first = dt.datetime.fromisoformat(created.replace("Z", "+00:00"))
                age = str((today - first).days)
            except ValueError:
                age = "?"
        return {"exists": "yes", "first_release": created[:10], "age_days": age, "maintainers": maint or "?"}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"exists": "no", "note": "not on the registry (404)"}
        return {"exists": "?", "note": f"lookup failed: HTTP {e.code}"}
    except Exception as e:  # network down, bad JSON: the gate sees it either way
        return {"exists": "?", "note": f"lookup failed: {type(e).__name__}"}


# --- the check ----------------------------------------------------------------------

class Hit:
    def __init__(self, kind: str, where: str, what: str, subjects: List[str], refuse: bool = False):
        self.kind, self.where, self.what, self.subjects, self.refuse = kind, where, what, subjects, refuse
        self.matched: Optional[str] = None


class DiffCheck:
    def __init__(self, a) -> None:
        self.wt = policy.real(a.worktree)
        self.git = Git(self.wt)
        self.rec = Record(policy.real(a.engagement))
        self.base = self.git.rev(a.base or self.rec.brief.get("base", "") or "")
        self.cand = self.git.rev(a.candidate or "HEAD")
        self.branch = a.branch or self.git.branch() or self.rec.brief.get("branch", "")
        self.offline = a.offline
        self.flag_tests = list(a.test_path)
        self.flag_ops = list(a.ops_path)
        self.hits: List[Hit] = []
        self.checks: List[str] = []  # checks that could not run
        self.commits: List[Dict] = []
        self.floor: List[str] = []
        self.controls = list(policy.CONTROLS)
        if self.git.exists(self.base, "devcraft/CLAUDE.md"):
            self.controls += list(policy.STUDIOS_CONTROLS)
        self.names_hits = 0

    # -- rules the sets of paths --------------------------------------------------------
    def test_paths(self) -> List[str]:
        return self.floor + self.rec.test_paths_add + self.flag_tests

    def ops_paths(self) -> List[str]:
        return self.rec.ops_paths + self.flag_ops

    def is_test(self, rel: str) -> bool:
        return policy.any_match(rel, self.test_paths()) is not None

    def is_ops(self, rel: str) -> bool:
        return policy.any_match(rel, self.ops_paths()) is not None

    # -- run --------------------------------------------------------------------------
    def run(self) -> None:
        if self.branch in DEFAULT_BRANCHES:
            self.hits.append(Hit("branch", self.branch, "the candidate is a default branch; nothing reaches one from a "
                                 "build worktree (never-do 3)", [], refuse=True))
        floor = self.git.show(self.base, ".devcraft/test-paths")
        if floor is None:
            raise Refuse("the repo has no .devcraft/test-paths at the base commit; the boundary rule cannot be checked "
                         "(the engagement should have stopped at Open)")
        self.floor = [l.strip() for l in floor.splitlines() if l.strip() and not l.startswith("#")]
        self.commits = self.git.commits(self.base, self.cand)
        for c in self.commits:
            c["seat"] = seat_of(c, self.rec.eng_id)
            self.check_commit(c)
        self.check_range()

    def check_commit(self, c: Dict) -> None:
        seat, sha = c["seat"], c["sha"][:7]
        if not seat:
            self.hits.append(Hit("commit", sha, "no seat on the commit: no Devcraft-Seat trailer and not a "
                                 f"`{self.rec.eng_id} S<n>` slice commit", []))
        for status, rel in c["paths"]:
            ctl = policy.any_match(rel, self.controls)
            if ctl:
                h = Hit("control", f"{sha} {rel}", f"a control ({ctl}) edited (never-do 14)", [rel])
                if policy.any_match(rel, policy.NO_EXCEPTION):
                    h.what += "; no exception exists for this file"
                    h.refuse = True
                else:
                    h.matched = self.rec.match("control", [rel])
                    h.refuse = h.matched is None
                self.hits.append(h)
            is_test, is_ops = self.is_test(rel), self.is_ops(rel)
            is_snap = policy.any_match(rel, SNAPSHOT_PATHS) is not None
            if is_test and status == "D":
                self.add("weaken", f"{sha} {rel}", "a test file deleted", [rel], "skip")
            elif is_test and status in ("M", "R"):
                before, after = self.git.show(c["sha"] + "^", rel), self.git.show(c["sha"], rel)
                for name in sorted(test_names(before or "") - test_names(after or ""))[:50]:
                    self.add("weaken", f"{sha} {rel}", f"test removed: {name}", [rel, name], "skip")
            if seat == "builder":
                if is_test:
                    self.hits.append(Hit("boundary", f"{sha} {rel}", "the Builder's commit touches a test path (never-do 4)", []))
                elif is_snap:
                    self.hits.append(Hit("boundary", f"{sha} {rel}", "the Builder's commit touches a snapshot or golden file (never-do 4)", []))
                if is_ops:
                    self.hits.append(Hit("boundary", f"{sha} {rel}", "the Builder's commit touches a path flagged for Release (never-do 4)", []))
            elif seat == "verifier":
                if not is_test:
                    self.hits.append(Hit("boundary", f"{sha} {rel}", "the Verifier's commit touches a path outside the test paths (never-do 4)", []))
            elif seat == "release-reliability":
                if is_test:
                    self.hits.append(Hit("boundary", f"{sha} {rel}", "Release's commit touches a test path (never-do 4)", []))
                elif not is_ops:
                    self.hits.append(Hit("boundary", f"{sha} {rel}", "Release's commit touches a path outside its flagged ops paths (never-do 4)", []))
            elif seat:
                self.hits.append(Hit("boundary", f"{sha} {rel}", f"a commit by the {seat}, which never writes the worktree (never-do 4)", []))

    def check_range(self) -> None:
        changed = self.git.changed(self.base, self.cand)
        test_paths = self.test_paths()
        lockfiles: List[Tuple[str, Hit]] = []
        covered_ecosystems: set = set()  # a named, verified package regenerates its own lockfile
        for status, rel in changed:
            base_name = os.path.basename(rel)
            text = self.git.show(self.cand, rel) if status != "D" else None
            before = self.git.show(self.base, rel) if status != "A" else None
            added = self.git.added_lines(self.base, self.cand, rel) if status != "D" else []
            in_tests = policy.any_match(rel, test_paths) is not None
            # never-do 5: markers, suppressions, thresholds, timeouts, CI and check config
            # (deleted tests and removed test functions are judged per commit, in check_commit)
            for n, line in added:
                if SKIP_MARK.search(line):
                    self.add("weaken", f"{rel}:{n}", "a skip, xfail, only or ignore marker added", [rel] + names_in(line), "skip")
                if SUPPRESS_MARK.search(line):
                    self.add("weaken", f"{rel}:{n}", "a lint, type or coverage suppression added", [rel], "skip")
                if THRESHOLD_MARK.search(line) and (in_tests or is_check_config(rel) or base_name in ("package.json", "pyproject.toml")):
                    self.add("weaken", f"{rel}:{n}", "a threshold line changed", [rel], "skip")
                if TIMEOUT_MARK.search(line) and (in_tests or is_check_config(rel) or policy.any_match(rel, CI_PATHS)):
                    self.add("weaken", f"{rel}:{n}", "a timeout changed", [rel], "skip")
            if policy.any_match(rel, CI_PATHS):
                self.add("weaken", rel, "a CI file edited", [rel], "skip", "control")  # a named control covers its CI edit
            elif is_check_config(rel):
                if base_name == "pyproject.toml":
                    if any(PYPROJECT_CHECK_LINE.search(line) for _, line in added):
                        self.add("weaken", rel, "check configuration in pyproject.toml edited", [rel], "skip")
                else:
                    self.add("weaken", rel, "a check configuration file edited", [rel], "skip")
            # never-do 6: credential files
            if policy.ENV_FILE.search(rel) and not policy.ENV_OK.search(rel):
                self.add("credential", rel, "a credential file in the change", [rel], "credential")
            # never-do 8: unattended
            if status != "D" and text is not None:
                if policy.any_match(rel, UNATTENDED_PATHS) or (rel.endswith(".plist") and PLIST_JOB.search(text)):
                    h = Hit("unattended", rel, "a job, schedule or timer file in the change; it switches on only after the "
                            "release gate and Sean's dated yes (never-do 8)", [rel])
                    h.matched = self.rec.match(None, [rel])  # only a ratified entry can match
                    self.hits.append(h)
                elif policy.any_match(rel, CI_PATHS) and any(SCHEDULE_LINE.search(line) for _, line in added):
                    h = Hit("unattended", rel, "a schedule added to a workflow (never-do 8)", [rel])
                    h.matched = self.rec.match(None, [rel])
                    self.hits.append(h)
            # never-do 12: manifests and lockfiles
            if policy.any_match(rel, LOCKFILES):
                h = Hit("dependency", rel, "a lockfile changed", [rel])
                h.matched = self.rec.match("dependency", [rel])
                lockfiles.append((LOCK_ECOSYSTEM.get(base_name, ""), h))
                self.hits.append(h)
            eco = ecosystem(rel)
            if eco and status != "D":
                after_names = package_names(rel, text or "")
                before_names = {m.lower() for m in package_names(rel, before or "")}
                new = [n for n in after_names if n.lower() not in before_names]
                removed = sorted(before_names - {n.lower() for n in after_names})
                bumped = sorted({n for n in after_names if n.lower() in before_names
                                 for _, line in added if re.search(r"(?<![\w.-])" + re.escape(n) + r"(?![\w-])", line, re.I)})
                if removed or bumped:
                    what = "a manifest edited: " + ", ".join(
                        ([f"removed {', '.join(removed)}"] if removed else []) + ([f"changed {', '.join(bumped)}"] if bumped else []))
                    self.add("dependency", rel, what, [rel] + removed + bumped, "dependency")
                for name in new:
                    info = registry_lookup(eco, name, self.offline)
                    desc = f"new package {name} ({eco}): "
                    if info.get("exists") == "yes":
                        desc += f"on the registry since {info.get('first_release') or '?'} ({info.get('age_days') or '?'} days); maintainers: {info.get('maintainers') or '?'}"
                    else:
                        desc += info.get("note", "unknown")
                    h = Hit("dependency", rel, desc, [name, rel])
                    h.matched = self.rec.match("dependency", [name])
                    if info.get("exists") != "yes":
                        h.matched = None  # an unverified package is never covered
                        self.checks.append(f"registry lookup for {name}: {info.get('note', 'failed')}")
                    elif h.matched:
                        covered_ecosystems.add(eco)
                    self.hits.append(h)
            # never-do 11: a listed name in what the range adds
            for n, line in added:
                if name_in(line):
                    self.hits.append(Hit("leak", f"{rel}:{n}", "a name from the machine's list in an added line (never-do 11)", []))
        for eco, h in lockfiles:
            if not h.matched and eco and eco in covered_ecosystems:
                h.matched = f"a named {eco} package in this range"
        for c in self.commits:
            if name_in(c["message"]):
                self.hits.append(Hit("leak", c["sha"][:7], "a name from the machine's list in a commit message (never-do 11)", []))
        if name_in(self.branch):
            self.hits.append(Hit("leak", "branch name", "a name from the machine's list in the branch name (never-do 11)", []))
        self.secret_scan()

    def add(self, kind: str, where: str, what: str, subjects: List[str], *ex_kinds: str) -> None:
        h = Hit(kind, where, what, subjects)
        for ex_kind in ex_kinds:
            h.matched = h.matched or self.rec.match(ex_kind, subjects)
        self.hits.append(h)

    def secret_scan(self) -> None:
        tool = next((g for g in GITLEAKS if g and os.access(g, os.X_OK)), "")
        if not tool:
            self.checks.append("secret scan: gitleaks is not installed at a known full path")
            return
        with tempfile.TemporaryDirectory() as tmp:
            report = os.path.join(tmp, "gitleaks.json")
            r = subprocess.run([tool, "git", f"--log-opts={self.base}..{self.cand}", "--redact", "--no-banner",
                                "--exit-code", "1", "--report-format", "json", "--report-path", report, self.wt],
                               capture_output=True, text=True)
            if r.returncode not in (0, 1):
                self.checks.append(f"secret scan: gitleaks exited {r.returncode}: {r.stderr.strip()[-300:]}")
                return
            try:
                found = json.loads(Path(report).read_text(encoding="utf-8") or "[]")
            except (OSError, ValueError):
                found = []
                if r.returncode == 1:
                    self.checks.append("secret scan: gitleaks found secrets but its report could not be read")
        for f in found:
            where = f"{f.get('File', '?')}:{f.get('StartLine', '?')} ({str(f.get('Commit', ''))[:7]})"
            self.hits.append(Hit("credential", where, f"a credential value in the change, rule {f.get('RuleID', '?')} "
                                 "(never-do 6); a value is never covered by an exception", []))

    # -- verdict and report -------------------------------------------------------------
    def verdict(self) -> Tuple[int, str]:
        refused = [h for h in self.hits if h.refuse]
        if refused:
            return 2, f"DIFF CHECK REFUSED — {len(refused)} outright: " + "; ".join(h.what.split(" (")[0] for h in refused[:3])
        unmatched = [h for h in self.hits if not h.matched]
        if unmatched or self.checks:
            return 1, f"DIFF CHECK FINDINGS — {len(unmatched)} unmatched hit(s), {len(self.checks)} check(s) that could not run"
        return 0, f"DIFF CHECK CLEAN — {len(self.hits)} hit(s), every one on the record"

    def report(self, code: int, line: str) -> str:
        now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        out = [f"# Diff check — {self.rec.eng.name}", "",
               f"run: {now}", f"worktree: {self.wt}", f"branch: {self.branch or '?'}", f"base: {self.base}",
               f"candidate: {self.cand}", f"commits: {len(self.commits)}",
               f"test-paths floor (at base): {', '.join(self.floor) or 'none'}",
               f"test paths added: {', '.join(self.rec.test_paths_add + self.flag_tests) or 'none'}"
               + (" (from flags: " + ", ".join(self.flag_tests) + ")" if self.flag_tests else ""),
               f"ops paths flagged for Release: {', '.join(self.ops_paths()) or 'none'}"
               + (" (from flags: " + ", ".join(self.flag_ops) + ")" if self.flag_ops else ""),
               f"plan gate: {self.rec.gate_file.relative_to(self.rec.eng) if self.rec.gate_file else 'none'}"
               + (f" (anchor {self.rec.anchor_sha[:12]})" if self.rec.anchor_sha else ""),
               f"build plan: {self.rec.plan_file.relative_to(self.rec.eng.resolve()) if self.rec.plan_file else 'none'}"
               + (f" ({self.rec.plan_source})" if self.rec.plan_file else ""),
               f"build plan frozen at that anchor: {'yes' if self.rec.plan_frozen else 'no'}",
               f"exceptions honored: {', '.join(e['id'] + ' ' + e['kind'] for e in self.rec.exceptions) or 'none'}",
               f"ratified ledger entries seen: {', '.join(y['id'] + ' (' + y['date'] + ')' for y in self.rec.yeses) or 'none'}",
               f"controls list: {'studios' if len(self.controls) > len(policy.CONTROLS) else 'standard'}", ""]
        for n in self.rec.notes:
            out.append(f"note: {n}")
        if self.rec.notes:
            out.append("")
        out += ["## Commits", ""]
        for c in self.commits:
            first = c["message"].splitlines()[0] if c["message"] else ""
            out.append(f"- {c['sha'][:7]} · {c['seat'] or 'UNATTRIBUTED'} · {len(c['paths'])} path(s) · {first[:100]}")
        out += ["", "## Hits", ""]
        if not self.hits:
            out.append("none")
        for i, h in enumerate(self.hits, 1):
            state = "REFUSED" if h.refuse else (f"matched {h.matched}" if h.matched else "UNMATCHED")
            out.append(f"- H{i} · {h.kind} · {h.where} · {h.what} · {state}")
        out += ["", "## Checks that could not run", ""]
        out += [f"- {c}" for c in self.checks] or ["none"]
        out += ["", "## Verdict", "", line, "",
                "Exit 0 clean, 1 findings for the release gate, 2 refused (the push fails). "
                "A hit matches a plan-gate exception by kind and name, or a ratified ledger entry that names it.",
                f"exit: {code}", ""]
        return redact("\n".join(out))


def is_check_config(rel: str) -> bool:
    return policy.any_match(rel, CHECK_CONFIG) is not None or os.path.basename(rel) == "pyproject.toml"


def test_names(text: str) -> set:
    out = set()
    for rx in TEST_NAME:
        out.update(rx.findall(text))
    return out


def names_in(line: str) -> List[str]:
    """Test names on a marker line, so an exception naming the test matches."""
    out: List[str] = []
    for rx in TEST_NAME:
        out += rx.findall(line)
    return out


_NAME_PATS: Optional[List[re.Pattern]] = None


def redact(text: str) -> str:
    """A listed name never reaches the report (never-do 11): it is replaced, never printed."""
    name_in("")  # loads the patterns
    for p in _NAME_PATS or []:
        text = p.sub("[a listed name]", text)
    return text


def name_in(text: str) -> bool:
    global _NAME_PATS
    if _NAME_PATS is None:
        _NAME_PATS = [re.compile(r"(?<![A-Za-z0-9])" + re.escape(n) + r"(?![A-Za-z0-9])", re.I) for n in policy.names()]
    return any(p.search(text) for p in _NAME_PATS)


def output_path(a, dc: DiffCheck) -> Path:
    if a.out:
        return Path(a.out)
    folder = dc.rec.eng / "evidence"
    folder.mkdir(parents=True, exist_ok=True)
    stem = f"diff-check-{dc.cand[:7]}"
    p = folder / f"{stem}.txt"
    n = 2
    while p.exists():  # evidence is append-only: a re-run is a new file
        p = folder / f"{stem}-{n}.txt"
        n += 1
    return p


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--worktree", required=True)
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--base", default="", help="default: the brief's base:")
    ap.add_argument("--candidate", default="HEAD")
    ap.add_argument("--branch", default="", help="default: the worktree's branch")
    ap.add_argument("--test-path", action="append", default=[], help="a test path the record cannot supply (recorded as from flags)")
    ap.add_argument("--ops-path", action="append", default=[], help="an ops path the record cannot supply (ops-only asks)")
    ap.add_argument("--out", default="", help="default: <engagement>/evidence/diff-check-<candidate>.txt, never overwritten")
    ap.add_argument("--offline", action="store_true", help="skip registry lookups; each is then a check that could not run")
    a = ap.parse_args(argv)
    try:
        dc = DiffCheck(a)
        dc.run()
    except (Refuse, policy.ContextError) as e:
        sys.stderr.write(f"diffcheck: refused. {e}\n")
        return 2
    code, line = dc.verdict()
    text = dc.report(code, line)
    out = output_path(a, dc)
    out.write_text(text, encoding="utf-8")
    print(line)
    print(f"report: {out} (sha256 {hashlib.sha256(text.encode('utf-8')).hexdigest()})")
    return code


if __name__ == "__main__":
    sys.exit(main())
