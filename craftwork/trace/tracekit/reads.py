"""Recover a pass's corpus reads from its own transcript, so nobody types the list (SWCB #169).

Ruled on SWCB #169 (2026-10-16), piece 1 of the coordinator's record contract.
Rung-0 line 5 trusts a record's `## Corpus read`, and on dc-eng-002 the
coordinator typed `none` on six Builder passes whose transcripts show the reads;
the checker then turned a record error into an accusation against the seat. So
the list is recovered by this script and pasted, never written by hand.

What counts as a read is what put a corpus file's text in front of the seat:

- **Claude** (`claude -p` stream-json, an Agent-tool subagent JSONL, a Claude Code
  session file): a successful `Read`; a `Grep` in `content` mode, for each file
  its output quotes; a successful `Bash` command, judged as below.
- **Codex** (`codex exec --json`, plus the session files saved in
  `pass-NN.rollouts/`): every completed `command_execution`, judged as below.
- **A shell command** reads the corpus files it hands to a reader (`cat`, `head`,
  `sed -n`, `awk`, `nl` …), and a search (`grep`, `rg` …) reads the files its
  output quotes, or the one file it was given. A listing (`ls`, `find`,
  `rg --files`, `grep -l`, `wc`, `shasum` …) reads nothing. Simple variables
  (`C=…/corpus/canon; cat $C/x.md`) and `cd` are followed.

A call that names a corpus path the script cannot judge (a Python heredoc, an
unknown program, a failed command) is never guessed into the list: it is
returned in `unjudged`, for the coordinator to check against the transcript and
say so in `## Notes`. Paths come back studio-prefixed (`devcraft/corpus/…`), the
form rung-0 line 5 matches citations against.
"""
from __future__ import annotations

import json
import os
import re
import shlex
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Optional

__all__ = ["Reads", "corpus_path", "shell_reads", "read_log", "read_logs", "format_section"]

# programs whose every operand is a file they print
READERS = {"cat", "head", "tail", "nl", "less", "more", "bat", "tac", "strings", "fold", "fmt", "cut", "sort",
           "uniq", "column", "od", "xxd", "hexdump"}
# programs whose first operand is a script, unless -e / -f gave it
SCRIPTED = {"sed", "gsed", "awk", "gawk", "nawk", "mawk"}
SEARCHES = {"grep", "egrep", "fgrep", "rg", "ag", "ack"}
# programs that name files without putting their text in front of the seat
LISTINGS = {"ls", "find", "fd", "stat", "file", "du", "wc", "shasum", "sha256sum", "sha1sum", "md5", "md5sum",
            "cksum", "test", "[", "realpath", "readlink", "basename", "dirname", "tree", "git", "cd", "pwd",
            "echo", "printf", "true", "false", "mkdir", "touch", "exit"}
# wrappers to look through to the real program
WRAPPERS = {"env", "command", "nice", "nohup", "time", "timeout", "builtin", "exec"}
SHELLS = {"sh", "bash", "zsh", "dash", "ksh"}
# Claude tools that name a corpus path without reading it
_CLAUDE_NON_READS = {"Glob", "LS", "Write", "Edit", "MultiEdit"}

# a search that only lists file names or counts, never their text
_LIST_FLAGS_LONG = {"--files", "--files-with-matches", "--files-without-match", "--count", "--count-matches",
                    "--quiet", "--type-list"}
_LIST_FLAGS_SHORT = set("lLcq")
# options that take a value, so the value is not a pattern or a path; grep's -E is a flag, rg's takes a value
_SEARCH_VALUE_SHORT = {"grep": set("efmABCdD"), "rg": set("efgtTmABCjMrE"), "ag": set("efGgmABC"),
                       "ack": set("fmABCg")}
_SEARCH_VALUE_LONG = {"--regexp", "--file", "--glob", "--iglob", "--type", "--type-not", "--max-count",
                      "--after-context", "--before-context", "--context", "--threads", "--replace",
                      "--max-columns", "--encoding", "--sort", "--sortr", "--max-depth", "--type-add",
                      "--pre", "--pre-glob", "--path-separator", "--include", "--exclude", "--exclude-dir",
                      "--label", "--devices", "--directories", "--binary-files", "--max-filesize",
                      "--ignore-file"}
_RG_VALUE_LONG = _SEARCH_VALUE_LONG | {"--color", "--colors"}   # grep's --color takes its value only after =
_SCRIPT_GIVEN_SHORT = set("ef")
_SCRIPT_GIVEN_LONG = ("--expression", "--file")

_VAR = re.compile(r"\$\{(\w+)\}|\$(\w+)")
_ASSIGN = re.compile(r"^([A-Za-z_]\w*)=(.*)$", re.S)
_HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1")
_OUTPUT_PREFIX = re.compile(r"^([\w./~+@-]+):")   # a search's `path:` prefix; prose lines never match
_DURATION = re.compile(r"^\d+(\.\d+)?[smhd]?$")


@dataclass
class Reads:
    """What one pass's transcript shows it read from the corpus."""
    paths: set[str] = field(default_factory=set)        # studio-prefixed corpus paths
    unjudged: list[str] = field(default_factory=list)   # "<why>: <call>", calls naming a corpus path not judged
    error: str = ""
    cwd: Optional[str] = None                           # a shell's working directory once the command ran

    def note(self, why: str, call: str) -> None:
        line = f"{why}: {' '.join(call.split())[:300]}"
        if line not in self.unjudged:
            self.unjudged.append(line)

    def merge(self, other: "Reads") -> None:
        self.paths |= other.paths
        for u in other.unjudged:
            if u not in self.unjudged:
                self.unjudged.append(u)


def corpus_path(raw: str, cwd: Optional[str] = None) -> Optional[str]:
    """`/…/studios/devcraft/corpus/canon/x.md` → `devcraft/corpus/canon/x.md`; None when not under a corpus."""
    p = raw.strip().strip("'\"")
    if not p or "\n" in p:
        return None
    if p.startswith("file://"):
        p = p[len("file://"):]
    p = os.path.expanduser(p)
    if cwd and not p.startswith("/"):
        p = os.path.join(cwd, p)
    if "corpus" not in p:
        return None
    parts = PurePosixPath(os.path.normpath(p)).parts
    idx = [i for i, part in enumerate(parts) if part == "corpus" and i < len(parts) - 1]
    if not idx:
        return None
    i = idx[-1]
    head = [parts[i - 1]] if i > 0 and parts[i - 1] not in ("/", "..", ".") else []
    return "/".join(head + list(parts[i:]))


def _absolute(raw: str, cwd: Optional[str]) -> str:
    p = os.path.expanduser(raw.strip())
    return os.path.normpath(os.path.join(cwd, p) if cwd and not p.startswith("/") else p)


def _is_dir(raw: str, cwd: Optional[str]) -> bool:
    """A directory on disk, or a path with no file suffix that is not a file on disk."""
    p = Path(_absolute(raw, cwd))
    if p.is_dir():
        return True
    if p.is_file():
        return False
    return raw.rstrip().endswith("/") or not PurePosixPath(raw).suffix


def _expand_globs(word: str, cwd: Optional[str]) -> list[str]:
    if not any(ch in word for ch in "*?["):
        return [word]
    import glob
    hits = sorted(glob.glob(_absolute(word, cwd)))
    return hits or [word]


def _quoted_paths(output: str, cwd: Optional[str]) -> set[str]:
    """Corpus files a search's output quotes, from its `path:` line prefixes."""
    found = set()
    for line in output.splitlines():
        m = _OUTPUT_PREFIX.match(line)
        if not m:
            continue
        cand = m.group(1)
        cp = corpus_path(cand, cwd)
        if cp and not _is_dir(cand, cwd):
            found.add(cp)
    return found


# --------------------------------------------------------------------------- #
# shell
# --------------------------------------------------------------------------- #


def _strip_heredocs(script: str) -> tuple[str, list[str]]:
    """Remove heredoc bodies (they are another program's input, never shell); return them apart."""
    lines = script.split("\n")
    out, bodies = [], []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        m = _HEREDOC.search(line)
        i += 1
        if m:
            end, body = m.group(2), []
            while i < len(lines) and lines[i].strip() != end:
                body.append(lines[i])
                i += 1
            i += 1
            bodies.append("\n".join(body))
    return "\n".join(out), bodies


def _tokens(script: str) -> list[str]:
    lex = shlex.shlex(script, posix=True, punctuation_chars="();<>|&\n")
    lex.whitespace = " \t\r"
    lex.whitespace_split = True
    lex.commenters = ""
    try:
        return list(lex)
    except ValueError:            # an unbalanced quote: fall back to plain words
        return script.replace("\n", " ; ").split()


def _simple_commands(tokens: list[str]) -> list[list[str]]:
    """Split on ; && || | & ( ) and newlines; drop redirection targets but keep `< file` as an operand."""
    cmds, cur = [], []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t and all(ch in ";&|()\n" for ch in t):
            if cur:
                cmds.append(cur)
            cur = []
        elif t and all(ch in "<>&" for ch in t):
            if t == "<" and i + 1 < len(tokens):
                cur.append(tokens[i + 1])
            i += 1                    # the redirection's target
        else:
            cur.append(t)
        i += 1
    if cur:
        cmds.append(cur)
    return cmds


def _expand(word: str, env: dict[str, str]) -> str:
    return _VAR.sub(lambda m: env.get(m.group(1) or m.group(2), m.group(0)), word)


def _operands(words: list[str], value_short: set[str] = frozenset(), value_long: set[str] = frozenset()):
    """Yield (kind, text) for each word: ('opt', flag) or ('arg', operand); option values are skipped."""
    i, done = 0, False
    while i < len(words):
        w = words[i]
        if done or w == "-" or not w.startswith("-"):
            yield "arg", w
        elif w == "--":
            done = True
        elif w.startswith("--"):
            yield "opt", w
            if "=" not in w and w in value_long:
                i += 1
        else:
            yield "opt", w
            for j, ch in enumerate(w[1:], 1):
                if ch in value_short:
                    if j == len(w) - 1:
                        i += 1        # value is the next word
                    break             # else the rest of the bundle is the value
        i += 1


def _bundle_has(opt: str, chars: set[str], value_short: set[str]) -> bool:
    """Whether a short-option bundle (`-rn`, `-m1l`) sets one of these flags before any value starts."""
    for ch in opt[1:]:
        if ch in chars:
            return True
        if ch in value_short:
            return False
    return False


def _search(prog: str, args: list[str], cwd: Optional[str], output: str, ok: bool, call: str, r: Reads) -> None:
    vshort = _SEARCH_VALUE_SHORT.get("grep" if prog in ("egrep", "fgrep") else prog, _SEARCH_VALUE_SHORT["grep"])
    vlong = _RG_VALUE_LONG if prog == "rg" else _SEARCH_VALUE_LONG
    parsed = list(_operands(args, vshort, vlong))
    opts = [t for k, t in parsed if k == "opt"]
    for o in opts:
        if o.split("=", 1)[0] in _LIST_FLAGS_LONG if o.startswith("--") else _bundle_has(o, _LIST_FLAGS_SHORT, vshort):
            return                    # names files or counts matches, never quotes their text
    pattern_given = any(o.split("=", 1)[0] in ("--regexp", "--file") if o.startswith("--")
                        else next((ch for ch in o[1:] if ch in vshort), "") in ("e", "f") for o in opts)
    operands = [t for k, t in parsed if k == "arg"]
    if not pattern_given and operands:
        operands = operands[1:]
    quoted = _quoted_paths(output, cwd)
    r.paths |= quoted
    files = []
    for word in operands:
        for path in _expand_globs(word, cwd):
            if corpus_path(path, cwd) and not _is_dir(path, cwd):
                files.append(path)
    if len(files) == 1 and not quoted and ok and output.strip():
        r.paths.add(corpus_path(files[0], cwd))   # one file searched: its output carries no path prefix
    elif files and not ok and not quoted and output.strip():
        r.note("search exited non-zero", call)


def shell_reads(script: str, cwd: Optional[str] = None, output: str = "", ok: bool = True,
                call: str = "") -> Reads:
    """The corpus files one shell command line reads. `ok` is whether it succeeded; `output` is what it printed."""
    r = Reads()
    call = call or script
    body, heredocs = _strip_heredocs(script)
    env: dict[str, str] = {"HOME": os.path.expanduser("~")}
    here = cwd
    for words in _simple_commands(_tokens(body)):
        words = [_expand(w, env) for w in words]
        while words and _ASSIGN.match(words[0]):
            name, value = _ASSIGN.match(words[0]).groups()
            env[name] = value
            words = words[1:]
        if words and words[0] == "export":
            for w in words[1:]:
                m = _ASSIGN.match(w)
                if m:
                    env[m.group(1)] = m.group(2)
            continue
        while words and (os.path.basename(words[0]) in WRAPPERS or _ASSIGN.match(words[0])):
            words = words[1:]
            while words and (words[0].startswith("-") or _ASSIGN.match(words[0]) or _DURATION.match(words[0])):
                words = words[1:]
        if not words:
            continue
        prog, args = os.path.basename(words[0]), words[1:]
        if prog == "cd":
            target = args[0] if args else "~"
            here = _absolute(target, here)
            continue
        if prog in SHELLS:
            ops = list(_operands(args))
            if any(k == "opt" and "c" in t.lstrip("-") for k, t in ops):
                inner = next((t for k, t in ops if k == "arg"), "")
                r.merge(shell_reads(inner, here, output, ok, call))
                continue
        names_corpus = any(corpus_path(a, here) for a in args if not a.startswith("-"))
        if prog in SEARCHES:
            _search(prog, args, here, output, ok, call, r)
        elif prog in READERS or prog in SCRIPTED:
            if prog in SCRIPTED and any(k == "opt" and (t.startswith("-i") or t.startswith("--in-place"))
                                        for k, t in _operands(args)):
                if names_corpus:
                    r.note("edits in place, not a read", call)
                continue
            ops = list(_operands(args, _SCRIPT_GIVEN_SHORT if prog in SCRIPTED else set(),
                                 set(_SCRIPT_GIVEN_LONG) if prog in SCRIPTED else set()))
            operands = [t for k, t in ops if k == "arg"]
            script_given = any(k == "opt" and (t[1:2] in _SCRIPT_GIVEN_SHORT or t.startswith(_SCRIPT_GIVEN_LONG))
                               for k, t in ops)
            if prog in SCRIPTED and not script_given and operands:
                operands = operands[1:]
            hits = [corpus_path(p, here) for w in operands for p in _expand_globs(w, here)
                    if corpus_path(p, here) and not _is_dir(p, here)]
            if hits and ok:
                r.paths |= set(hits)
            elif hits:
                r.note("the command failed", call)
        elif prog in LISTINGS:
            continue
        elif names_corpus:
            r.note(f"`{prog}` is not a program the script judges", call)
    r.cwd = here
    in_corpus = bool(here) and corpus_path(os.path.join(here, "x")) is not None
    for body_text in heredocs:
        if in_corpus or any(corpus_path(w) for w in re.split(r"[\s'\"(),]+", body_text)):
            r.note("a heredoc script may read the corpus", call)
    return r


# --------------------------------------------------------------------------- #
# transcripts
# --------------------------------------------------------------------------- #


def _text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(_text(c.get("text", c.get("content", ""))) if isinstance(c, dict) else str(c)
                         for c in content)
    return ""


_CWD_RESET = re.compile(r"Shell cwd was reset to (\S+)")


def _claude_call(name: str, inp: dict, result: str, is_error: bool, cwd: Optional[str], r: Reads) -> Optional[str]:
    """Judge one Claude tool call; return the Bash shell's working directory after it, when it is a Bash call."""
    if name == "Read":
        path = str(inp.get("file_path") or "")
        cp = corpus_path(path, cwd)
        if cp and not is_error:
            r.paths.add(cp)
        elif cp:
            r.note("the Read failed", f"Read {path}")
    elif name == "Grep":
        if (inp.get("output_mode") or "files_with_matches") != "content" or is_error:
            return
        quoted = _quoted_paths(result, cwd)
        r.paths |= quoted
        target = str(inp.get("path") or "")
        cp = corpus_path(target, cwd)
        if cp and not quoted and result.strip() and not _is_dir(target, cwd):
            r.paths.add(cp)
    elif name == "Bash":
        cmd = str(inp.get("command") or "")
        sub = shell_reads(cmd, cwd, result, not is_error)
        r.merge(sub)
        reset = _CWD_RESET.search(result)
        return reset.group(1) if reset else sub.cwd
    elif name not in _CLAUDE_NON_READS and _names_corpus(inp):
        r.note(f"the {name} tool is not one the script judges", json.dumps(inp))
    return None


def _pick_cwd(script: str, carried: str, base: Optional[str]) -> str:
    """Where a Bash call's relative paths resolve: the directory an earlier `cd` left, or the session's own.

    Claude Code's Bash tool keeps one shell in some setups (a `cd` carries into
    the next call) and resets it to the project in others (an Agent-tool
    subagent, or a `cd` out of bounds), and the log does not always say which.
    So the carried directory is kept only when it is where this command's own
    relative paths exist on disk; otherwise the session's directory is used."""
    if base is None:
        return carried
    words = [w for w in _tokens(_strip_heredocs(script)[0])
             if w and not w.startswith(("-", "/", "~", "$")) and ("/" in w or "." in w)]
    if any(os.path.exists(os.path.join(carried, w)) and not os.path.exists(os.path.join(base, w)) for w in words):
        return carried
    return base


def _names_corpus(inp: Any) -> bool:
    """A tool input that spells out a corpus path (not one that only resolves into it from the cwd)."""
    return isinstance(inp, dict) and any(isinstance(v, str) and corpus_path(v) for v in inp.values())


def _codex_command(cmd: Any, cwd: Optional[str], output: str, exit_code: Any, status: str, r: Reads) -> None:
    """One Codex command. The `--json` stream gives a string, the session file a list; both unwrap to the script."""
    if not isinstance(cmd, list):
        try:
            cmd = shlex.split(str(cmd))
        except ValueError:
            cmd = [str(cmd)]
    shell = len(cmd) == 3 and os.path.basename(cmd[0]) in SHELLS and cmd[1].startswith("-") and "c" in cmd[1]
    script = cmd[2] if shell else shlex.join(cmd)
    ok = exit_code == 0 and status in ("completed", "")
    r.merge(shell_reads(script, cwd, output or "", ok))


def read_log(text: str, cwd: Optional[str] = None) -> Reads:
    """Reads from one JSONL transcript, Claude or Codex, told apart line by line."""
    r = Reads()
    uses: dict[str, tuple[str, dict, Optional[str]]] = {}
    results: dict[str, tuple[str, bool]] = {}
    here = cwd
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(e, dict):
            continue
        t = e.get("type")
        if isinstance(e.get("cwd"), str) and not cwd:
            here = e["cwd"]
        # Codex `exec --json`
        if t == "item.completed" and isinstance(e.get("item"), dict) and e["item"].get("type") == "command_execution":
            it = e["item"]
            _codex_command(it.get("command"), here, it.get("aggregated_output") or "", it.get("exit_code"),
                           str(it.get("status") or ""), r)
            continue
        # Codex session file
        p = e.get("payload")
        if isinstance(p, dict):
            if t == "session_meta" and isinstance(p.get("cwd"), str) and not cwd:
                here = p["cwd"]
            it = p.get("item") if p.get("type") == "item_completed" else None
            if isinstance(it, dict) and it.get("type") == "CommandExecution":
                c = it.get("cwd")
                c = c[len("file://"):] if isinstance(c, str) and c.startswith("file://") else (c or here)
                _codex_command(it.get("command"), c, it.get("aggregated_output") or "", it.get("exit_code"),
                               str(it.get("status") or ""), r)
            continue
        # Claude: stream-json, an Agent-tool subagent JSONL, or a session file
        if t == "system" and e.get("subtype") == "init" and isinstance(e.get("cwd"), str) and not cwd:
            here = e["cwd"]
        msg = e.get("message")
        if not isinstance(msg, dict) or not isinstance(msg.get("content"), list):
            continue
        for block in msg["content"]:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use" and block.get("id"):
                uses[block["id"]] = (str(block.get("name") or ""), block.get("input") or {}, here)
            elif block.get("type") == "tool_result" and block.get("tool_use_id"):
                results[block["tool_use_id"]] = (_text(block.get("content")), bool(block.get("is_error")))
    shell_cwd: Optional[str] = None     # where the last `cd` left the Bash shell
    for uid, (name, inp, c) in uses.items():
        if uid not in results:
            if _names_corpus(inp):
                r.note("no result in the log", f"{name} {json.dumps(inp)}")
            continue
        out, err = results[uid]
        if name == "Bash" and shell_cwd and shell_cwd != c:
            c = _pick_cwd(str((inp or {}).get("command") or ""), shell_cwd, c)
        after = _claude_call(name, inp if isinstance(inp, dict) else {}, out, err, c, r)
        if name == "Bash" and after:
            shell_cwd = after
    return r


def read_logs(log: Path, cwd: Optional[str] = None) -> Reads:
    """A pass's raw log plus, for Codex, the session files saved beside it in `pass-NN.rollouts/`."""
    r = Reads()
    try:
        r.merge(read_log(log.read_text(encoding="utf-8"), cwd))
    except OSError as exc:
        r.error = f"{log}: {exc.strerror or exc}"
        return r
    rollouts = log.with_name(log.name[: -len(".jsonl")] + ".rollouts") if log.name.endswith(".jsonl") else None
    if rollouts is not None and rollouts.is_dir():
        for f in sorted(rollouts.glob("*.jsonl")):
            r.merge(read_log(f.read_text(encoding="utf-8"), cwd))
    return r


def format_section(r: Reads) -> str:
    """The body of a record's `## Corpus read`: one path per line, or `none`."""
    return "\n".join(f"- {p}" for p in sorted(r.paths)) if r.paths else "none"
