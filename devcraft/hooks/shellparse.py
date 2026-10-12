"""Split a shell command line into the simple commands the guard judges.

Best effort, and it knows it: a hook sees command text, never what a script
does once it runs, so the sandbox stays the wall and this only adds sight
(a resolved path, a wrapped `sh -c`, a `cd` earlier in the chain). Anything it
cannot parse is reported as unparseable, and the guard refuses it.
"""
from __future__ import annotations

import re
import shlex
from typing import List, Optional, Tuple

SEPARATORS = {";", "&&", "||", "|", "&", "|&", "(", ")", "\n", ";;", "{", "}"}
REDIRECTS = {">", ">>", ">|", "&>", "&>>", "<", "<<", "<<<", "<>", ">&", "<&"}
WRAPPERS = {"nohup", "time", "command", "exec", "builtin", "caffeinate", "noglob", "then", "do", "else", "if", "while", "until", "!"}
SHELLS = {"sh", "bash", "zsh", "dash", "ksh", "fish"}

_HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
_SUBST = re.compile(r"\$\(([^()]*(?:\([^()]*\)[^()]*)*)\)|`([^`]*)`")


class Simple:
    """One simple command: its words, its assignments and its redirect targets."""

    def __init__(self, argv: List[str], env: List[str], writes: List[str], reads: List[str], cwd: Optional[str]):
        self.argv = argv
        self.env = env
        self.writes = writes  # redirect targets that write (>, >>, &>)
        self.reads = reads  # redirect sources (<)
        self.cwd = cwd  # None once a `cd` the parser could not follow has run

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Simple({self.argv!r}, env={self.env!r}, writes={self.writes!r}, cwd={self.cwd!r})"


class Unparseable(Exception):
    pass


def strip_heredocs(text: str) -> Tuple[str, List[str]]:
    """Remove heredoc bodies (they are data, not commands); return them apart."""
    lines = text.split("\n")
    out, bodies = [], []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        delims = [m.group(2) for m in _HEREDOC.finditer(line)]
        i += 1
        for d in delims:
            body = []
            while i < len(lines) and lines[i].strip() != d:
                body.append(lines[i])
                i += 1
            if i >= len(lines):
                raise Unparseable(f"heredoc {d} never closes")
            bodies.append("\n".join(body))
            i += 1
    return "\n".join(out), bodies


def substitutions(text: str) -> List[str]:
    """The inner text of every $( ... ) and `...`, outermost first."""
    found = []
    for m in _SUBST.finditer(text):
        inner = m.group(1) if m.group(1) is not None else m.group(2)
        found.append(inner)
        found.extend(substitutions(inner))
    return found


def _tokens(text: str) -> List[str]:
    lex = shlex.shlex(text, posix=True, punctuation_chars=";&|()<>")
    lex.whitespace = " \t\r"
    lex.whitespace_split = True
    lex.commenters = "#"
    try:
        toks = list(lex)
    except ValueError as e:
        raise Unparseable(str(e))
    # shlex drops newlines into whitespace unless told; keep them as separators.
    return toks


def _split_newlines(text: str) -> str:
    return text.replace("\n", " ; ")


def parse(text: str, cwd: Optional[str], depth: int = 0) -> List[Simple]:
    """Every simple command in `text`, wrappers unwrapped, `sh -c` recursed."""
    if depth > 4:
        raise Unparseable("nested too deep")
    body, _ = strip_heredocs(text)
    out: List[Simple] = []
    for inner in substitutions(body):
        out.extend(parse(inner, cwd, depth + 1))
    toks = _tokens(_split_newlines(body))
    current: List[str] = []
    groups: List[List[str]] = []
    for t in toks:
        if t in SEPARATORS or (set(t) <= set(";&|()") and t):
            if current:
                groups.append(current)
            current = []
        else:
            current.append(t)
    if current:
        groups.append(current)

    for g in groups:
        simple = _simple(g, cwd)
        if simple is None:
            continue
        argv = simple.argv
        # `cd` changes where later relative paths land.
        if argv and argv[0] in ("cd", "pushd"):
            target = argv[1] if len(argv) > 1 else "~"
            if target == "-" or "$" in target.replace("$HOME", "") or cwd is None:
                cwd = None
            else:
                import os
                cwd = os.path.normpath(os.path.join(cwd, os.path.expanduser(target.replace("$HOME", "~"))))
            out.append(simple)
            continue
        if argv and argv[0] in SHELLS:
            script = _dash_c(argv)
            if script is not None:
                out.append(simple)
                out.extend(parse(script, cwd, depth + 1))
                continue
        if argv and argv[0] == "eval":
            out.append(simple)
            out.extend(parse(" ".join(argv[1:]), cwd, depth + 1))
            continue
        out.append(simple)
    return out


def _dash_c(argv: List[str]) -> Optional[str]:
    for i, a in enumerate(argv[1:], 1):
        if a == "-c" or (a.startswith("-") and not a.startswith("--") and "c" in a[1:]):
            return argv[i + 1] if i + 1 < len(argv) else ""
    return None


def _simple(words: List[str], cwd: Optional[str]) -> Optional[Simple]:
    env: List[str] = []
    argv: List[str] = []
    writes: List[str] = []
    reads: List[str] = []
    i = 0
    while i < len(words):
        w = words[i]
        nxt = words[i + 1] if i + 1 < len(words) else ""
        if w.isdigit() and (nxt in REDIRECTS or nxt.startswith((">", "<", "&>"))):
            i += 1  # the fd number of `2>file`, split off by the lexer
            continue
        if w in REDIRECTS or re.fullmatch(r"\d*(>>?|>\||<|&>>?|>&|<&)", w):
            op = w.lstrip("0123456789")
            target = words[i + 1] if i + 1 < len(words) else ""
            # `>` followed by `&` then a digit is fd duplication (2>&1).
            if target in ("&",) or re.fullmatch(r"&?-?\d*-?", target or "x"):
                i += 2
                continue
            if op.startswith("<"):
                if op not in ("<<", "<<<"):
                    reads.append(target)
            else:
                writes.append(target)
            i += 2
            continue
        if not argv and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", w):
            env.append(w)
            i += 1
            continue
        argv.append(w)
        i += 1
    # unwrap prefixes: env, sudo-likes are judged by the guard, so only
    # transparent wrappers go here.
    while argv:
        head = argv[0]
        if head in WRAPPERS:
            argv = argv[1:]
            continue
        if head == "env":
            rest = argv[1:]
            if not rest:
                break  # bare `env` prints the environment; the guard judges it
            j = 0
            while j < len(rest) and (rest[j].startswith("-") or "=" in rest[j]):
                if "=" in rest[j] and not rest[j].startswith("-"):
                    env.append(rest[j])
                if rest[j] in ("-u", "-C", "-S", "-P"):
                    j += 1
                j += 1
            if j >= len(rest):
                break
            argv = rest[j:]
            continue
        if head in ("nice", "timeout", "gtimeout", "xargs", "stdbuf"):
            rest = argv[1:]
            j = 0
            while j < len(rest) and rest[j].startswith("-"):
                if rest[j] in ("-n", "-I", "-P", "-L", "-s", "-d", "-k", "-s", "-E", "-i", "-o", "-e"):
                    j += 1
                j += 1
            if head in ("timeout", "gtimeout") and j < len(rest):
                j += 1  # the duration
            if j >= len(rest):
                break
            argv = rest[j:]
            continue
        break
    if not argv and not writes and not env:
        return None
    return Simple(argv, env, writes, reads, cwd)
