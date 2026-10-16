"""Corpus reads recovered from a pass's own transcript, never typed (SWCB #169).

On dc-eng-002 the coordinator typed `## Corpus read: none` on six Builder passes
whose transcripts show the reads, and rung-0 line 5, which trusts the record,
turned that into an accusation against the seat. `reads.py` recovers the list
from the log instead. Every transcript here is invented; the corpus is a temp
folder of made-up files.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tracekit.reads import corpus_path, format_section, read_log, read_logs, shell_reads

TRACE = Path(__file__).resolve().parents[1]


@pytest.fixture
def repo(tmp_path) -> Path:
    """A studios-shaped tree: one team's corpus with three files, and a work folder outside it."""
    canon = tmp_path / "studios" / "devcraft" / "corpus" / "canon"
    canon.mkdir(parents=True)
    for name in ("alpha.md", "beta.md", "gamma.md"):
        (canon / name).write_text(f"# {name}\n\n## A heading\n", encoding="utf-8")
    (tmp_path / "work").mkdir()
    (tmp_path / "work" / "notes.md").write_text("notes\n", encoding="utf-8")
    return tmp_path


def canon(repo: Path) -> Path:
    return repo / "studios" / "devcraft" / "corpus" / "canon"


ALPHA, BETA, GAMMA = ("devcraft/corpus/canon/alpha.md", "devcraft/corpus/canon/beta.md",
                      "devcraft/corpus/canon/gamma.md")


# --------------------------------------------------------------------------- #
# paths
# --------------------------------------------------------------------------- #


def test_corpus_paths_come_back_studio_prefixed(repo):
    assert corpus_path(str(canon(repo) / "alpha.md")) == ALPHA
    assert corpus_path("canon/alpha.md", str(repo / "studios" / "devcraft" / "corpus")) == ALPHA
    assert corpus_path("../devcraft/corpus/canon/alpha.md", str(repo / "studios" / "systemcraft")) == ALPHA
    assert corpus_path(f"file://{canon(repo)}/beta.md") == BETA
    assert corpus_path("corpus/canon/alpha.md") == "corpus/canon/alpha.md"   # line 5 matches either form


def test_paths_outside_a_corpus_are_not_corpus_paths(repo):
    assert corpus_path(str(repo / "work" / "notes.md")) is None
    assert corpus_path(str(repo / "studios" / "devcraft" / "corpus")) is None   # the folder itself
    assert corpus_path("") is None


# --------------------------------------------------------------------------- #
# shell commands
# --------------------------------------------------------------------------- #


def reads(script, cwd=None, output="text", ok=True):
    return shell_reads(script, cwd, output, ok)


def test_readers_read_every_corpus_operand(repo):
    c = canon(repo)
    assert reads(f"cat {c}/alpha.md {repo}/work/notes.md").paths == {ALPHA}
    assert reads(f"head -n 40 {c}/alpha.md; tail -5 {c}/beta.md").paths == {ALPHA, BETA}
    assert reads(f"nl -ba {c}/gamma.md | sed -n 1,20p").paths == {GAMMA}


def test_sed_and_awk_scripts_are_never_taken_for_files(repo):
    c = canon(repo)
    assert reads(f"sed -n '28,57p' {c}/alpha.md").paths == {ALPHA}
    assert reads(f"sed -e 's|corpus/canon|x|' {c}/beta.md").paths == {BETA}
    assert reads(f"awk 'NR<20' {c}/gamma.md").paths == {GAMMA}


def test_an_in_place_edit_is_not_a_read_and_is_named(repo):
    r = reads(f"sed -i '' 's/a/b/' {canon(repo)}/alpha.md")
    assert r.paths == set()
    assert r.unjudged and r.unjudged[0].startswith("edits in place")


def test_variables_and_cd_are_followed(repo):
    c = canon(repo)
    assert reads(f"C={c}; sed -n 1,40p $C/alpha.md; grep -n '^#' ${{C}}/beta.md").paths == {ALPHA, BETA}
    assert reads(f"cd {c} && cat gamma.md").paths == {GAMMA}
    assert reads("cat canon/alpha.md", cwd=str(repo / "studios" / "devcraft" / "corpus")).paths == {ALPHA}


def test_a_shell_wrapper_is_unwrapped(repo):
    assert reads(f"/bin/zsh -lc \"cat {canon(repo)}/alpha.md\"").paths == {ALPHA}


def test_listings_read_nothing(repo):
    c = canon(repo)
    for cmd in (f"ls -la {c}", f"rg --files {c}", f"grep -l heading {c}/alpha.md", f"wc -c {c}/alpha.md",
                f"shasum -a 256 {c}/beta.md", f"find {c} -name '*.md'", f"rg -c heading {c}"):
        r = reads(cmd, output=f"{c}/alpha.md:1\n")
        assert r.paths == set() and r.unjudged == [], cmd


def test_a_search_reads_the_files_its_output_quotes(repo):
    c = canon(repo)
    out = f"{c}/alpha.md:3:## A heading\n{c}/gamma.md:3:## A heading\n"
    assert reads(f"rg -n 'A heading' {c}", output=out).paths == {ALPHA, GAMMA}
    assert reads(f"rg -n -g '!beta.md' heading {c}", output=out).paths == {ALPHA, GAMMA}


def test_a_search_of_one_file_reads_it_only_when_it_matched(repo):
    c = canon(repo)
    assert reads(f"grep -n -E 'A|B' {c}/alpha.md", output="3:## A heading\n").paths == {ALPHA}
    assert reads(f"grep -n zzz {c}/alpha.md", output="", ok=False).paths == set()


def test_search_prose_output_is_not_taken_for_paths(repo):
    out = "- **A note** - [`alpha.md`](../corpus/canon/alpha.md) - see: below\n"
    assert reads(f"rg -n note {canon(repo)}", output=out).paths == set()


def test_what_the_script_cannot_judge_is_named_never_guessed(repo):
    c = canon(repo)
    heredoc = f"python3 - <<'PY'\nprint(open('{c}/alpha.md').read())\nPY"
    for cmd, why in ((heredoc, "a heredoc"), (f"python3 tool.py {c}/alpha.md", "`python3`"),
                     (f"cat {c}/alpha.md {c}/missing.md", "the command failed")):
        r = reads(cmd, ok=not why.startswith("the command"))
        assert r.paths == set(), cmd
        assert len(r.unjudged) == 1 and r.unjudged[0].startswith(why), r.unjudged


def test_input_redirection_is_a_read(repo):
    assert reads(f"cat < {canon(repo)}/beta.md > /tmp/out.txt").paths == {BETA}


# --------------------------------------------------------------------------- #
# transcripts
# --------------------------------------------------------------------------- #


def claude_log(*calls, cwd=None) -> str:
    """Claude stream-json: an init line, then one assistant tool_use and one user tool_result per call."""
    lines = [{"type": "system", "subtype": "init", "cwd": cwd or "/nowhere", "model": "claude-opus-5-5"}]
    for i, (name, inp, result, is_error) in enumerate(calls):
        uid = f"toolu_{i}"
        lines.append({"type": "assistant", "message": {"model": "claude-opus-5-5", "role": "assistant", "content": [
            {"type": "tool_use", "id": uid, "name": name, "input": inp}]}})
        lines.append({"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": uid, "content": result, "is_error": is_error}]}})
    return "\n".join(json.dumps(x) for x in lines) + "\n"


def test_claude_read_and_failed_read(repo):
    c = canon(repo)
    r = read_log(claude_log(("Read", {"file_path": f"{c}/alpha.md"}, "1\t# alpha", False),
                            ("Read", {"file_path": f"{c}/beta.md"}, "File does not exist.", True)))
    assert r.paths == {ALPHA}
    assert r.unjudged == [f"the Read failed: Read {c}/beta.md"]


def test_claude_grep_reads_only_in_content_mode(repo):
    c = canon(repo)
    quoted = f"{c}/beta.md:3:## A heading"
    r = read_log(claude_log(("Grep", {"pattern": "A", "path": str(c), "output_mode": "content"}, quoted, False),
                            ("Grep", {"pattern": "A", "path": str(c)}, f"{c}/gamma.md", False),
                            ("Glob", {"pattern": "*.md", "path": str(c)}, f"{c}/alpha.md", False)))
    assert r.paths == {BETA}
    assert r.unjudged == []


def test_claude_bash_cd_carries_into_the_next_call_when_its_paths_exist_there(repo):
    corpus = repo / "studios" / "devcraft" / "corpus"
    r = read_log(claude_log(("Bash", {"command": f"cd {corpus}"}, "", False),
                            ("Bash", {"command": "sed -n 1,9p canon/alpha.md"}, "# alpha", False),
                            cwd=str(repo / "work")))
    assert r.paths == {ALPHA}


def test_claude_bash_cd_does_not_carry_into_a_fresh_shell(repo):
    # an Agent-tool subagent's shell starts in the project each call: `notes.md` exists there, not in the corpus
    r = read_log(claude_log(("Bash", {"command": f"cd {canon(repo)} && ls"}, "alpha.md", False),
                            ("Bash", {"command": "cat notes.md"}, "notes", False),
                            cwd=str(repo / "work")))
    assert r.paths == set()


def test_claude_bash_shell_reset_is_honoured(repo):
    r = read_log(claude_log(("Bash", {"command": f"cd {canon(repo)}"}, f"Shell cwd was reset to {repo}/work", False),
                            ("Bash", {"command": "cat alpha.md"}, "# alpha", False),
                            cwd=str(repo / "work")))
    assert r.paths == set()


def codex_stream(*commands) -> str:
    lines = [{"type": "thread.started", "thread_id": "t-1"}, {"type": "turn.started"}]
    for i, (cmd, code, out) in enumerate(commands):
        item = {"id": f"item_{i}", "type": "command_execution", "command": cmd, "aggregated_output": out,
                "exit_code": code, "status": "completed" if code == 0 else "failed"}
        lines.append({"type": "item.started", "item": {**item, "exit_code": None, "status": "in_progress"}})
        lines.append({"type": "item.completed", "item": item})
    lines.append({"type": "item.completed", "item": {"id": "f", "type": "file_change",
                                                     "changes": [{"path": str(canon(Path("/x")) / "z.md")}]}})
    lines.append({"type": "turn.completed", "usage": {"input_tokens": 1, "output_tokens": 1}})
    return "\n".join(json.dumps(x) for x in lines) + "\n"


def test_codex_stream_completed_commands_are_judged(repo):
    c = canon(repo)
    r = read_log(codex_stream((f"/bin/zsh -lc 'cat {c}/alpha.md'", 0, "# alpha"),
                              (f"/bin/zsh -lc \"rg -n heading {c}\"", 0, f"{c}/gamma.md:3:## A heading"),
                              (f"/bin/zsh -lc 'cat {c}/beta.md; false'", 1, "# beta")))
    assert r.paths == {ALPHA, GAMMA}
    assert len(r.unjudged) == 1 and r.unjudged[0].startswith("the command failed")


def test_codex_session_files_are_read_beside_the_stream_and_merged(repo, tmp_path):
    c = canon(repo)
    logs = tmp_path / "logs"
    (logs / "pass-07.rollouts").mkdir(parents=True)
    log = logs / "pass-07.jsonl"
    log.write_text(codex_stream((f"/bin/zsh -lc 'cat {c}/alpha.md; false'", 1, "# alpha")), encoding="utf-8")
    session = [{"type": "session_meta", "payload": {"id": "t-1", "cwd": str(c)}},
               {"type": "event_msg", "payload": {"type": "item_completed", "item": {
                   "type": "CommandExecution", "command": ["/bin/zsh", "-lc", "sed -n 1,5p beta.md"],
                   "cwd": f"file://{c}", "aggregated_output": "# beta", "exit_code": 0, "status": "completed"}}},
               {"type": "event_msg", "payload": {"type": "item_completed", "item": {
                   "type": "CommandExecution", "command": ["/bin/zsh", "-lc", f"cat {c}/alpha.md; false"],
                   "cwd": f"file://{c}", "aggregated_output": "# alpha", "exit_code": 1, "status": "failed"}}}]
    (logs / "pass-07.rollouts" / "rollout-1.jsonl").write_text("\n".join(json.dumps(x) for x in session) + "\n",
                                                               encoding="utf-8")
    r = read_logs(log)
    assert r.paths == {BETA}
    assert len(r.unjudged) == 1   # the same failed command, from the stream and the session file, named once


def codex_text(workdir, *commands) -> str:
    """`codex exec` stdout without --json: a header, then `exec` / command / status / output blocks."""
    out = ["Reading additional input from stdin...", "OpenAI Codex v0.146.0", "--------", f"workdir: {workdir}",
           "model: gpt-5.6-sol", "--------", "user", "# Pass-07 brief", "", "codex", "I'll read the corpus first."]
    for cmd, status, text in commands:
        out += ["exec", f"{cmd} in {workdir}", f" {status} in 0ms:", *text.split("\n")]
    out += ["codex", "Done.", "tokens used", "12,345"]
    return "\n".join(out) + "\n"


def test_codex_text_commands_are_judged_like_the_json_stream(repo):
    c = str(canon(repo))
    text = codex_text(c, ("/bin/zsh -lc 'cat alpha.md'", "succeeded", "# alpha\n\n## A heading"),
                      ("/bin/zsh -lc 'rg --files .'", "succeeded", "alpha.md\nbeta.md\ngamma.md"),
                      ("/bin/zsh -lc \"rg -n heading .\"", "succeeded", "./gamma.md:3:## A heading\nexec"),
                      ("/bin/zsh -lc 'cat beta.md; false'", "exited 1", "# beta"),
                      (f"/bin/zsh -lc \"python3 - <<'PY'\nopen('{c}/beta.md')\nPY\"", "succeeded", ""))
    r = read_logs_text(text)
    assert r.error == ""
    assert r.paths == {ALPHA, GAMMA}
    assert [u.split(":")[0] for u in r.unjudged] == ["the command failed", "a heredoc script may read the corpus"]


def read_logs_text(text):
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        log = Path(d) / "pass-07.log"
        log.write_text(text, encoding="utf-8")
        return read_logs(log)


# --------------------------------------------------------------------------- #
# zsh stops a command line at an unquoted `=word` it cannot look up
# --------------------------------------------------------------------------- #


def test_the_commands_before_a_zsh_equals_failure_are_judged(repo):
    # zsh reads `=====` as a lookup of a command called `====`, prints `==== not found`
    # and abandons the rest of the line: what came before ran, what came after never did
    c = canon(repo)
    cmd = f"cd {c}; sed -n 1,9p alpha.md; echo =====; cat beta.md"
    r = read_log(claude_log(("Bash", {"command": cmd}, "Exit code 1\n# alpha\n## A heading\n(eval):1: ==== not found",
                             True)))
    assert r.paths == {ALPHA} and r.unjudged == []
    r = read_log(codex_stream((f"/bin/zsh -lc 'cat {c}/alpha.md {c}/gamma.md && echo ===== && cat {c}/beta.md'", 1,
                               "# alpha\n# gamma\nzsh:1: ==== not found\n")))
    assert r.paths == {ALPHA, GAMMA} and r.unjudged == []


def test_a_zsh_equals_failure_first_on_the_line_reads_nothing(repo):
    r = reads(f"echo =====; cat {canon(repo)}/alpha.md", output="(eval):1: ==== not found", ok=False)
    assert r.paths == set() and r.unjudged == []


def test_a_zsh_equals_failure_after_another_error_is_named_not_judged(repo):
    c = canon(repo)
    r = reads(f"cat {c}/missing.md; echo =====; cat {c}/beta.md", ok=False,
              output=f"cat: {c}/missing.md: No such file or directory\n(eval):1: ==== not found")
    assert r.paths == set()
    assert len(r.unjudged) == 1
    assert r.unjudged[0].startswith("the command failed at `=====`, which zsh reads as a command lookup"), r.unjudged


def test_a_quoted_separator_is_not_a_zsh_equals_failure(repo):
    c = canon(repo)
    r = reads(f"cat {c}/alpha.md; echo '====='; cat {c}/missing.md", ok=False,
              output=f"# alpha\n=====\ncat: {c}/missing.md: No such file or directory")
    assert r.paths == set()
    assert len(r.unjudged) == 1 and r.unjudged[0].startswith("the command failed: "), r.unjudged


def test_the_section_is_one_path_per_line_or_none(repo):
    r = read_log(claude_log(("Read", {"file_path": f"{canon(repo)}/beta.md"}, "x", False),
                            ("Read", {"file_path": f"{canon(repo)}/alpha.md"}, "x", False)))
    assert format_section(r) == f"- {ALPHA}\n- {BETA}"
    assert format_section(read_log(claude_log())) == "none"


# --------------------------------------------------------------------------- #
# the command
# --------------------------------------------------------------------------- #


def run(*args):
    return subprocess.run([sys.executable, "reads.py", *args], capture_output=True, text=True, cwd=TRACE)


def test_the_command_prints_the_section_and_names_the_unjudged_on_stderr(repo, tmp_path):
    c = canon(repo)
    log = tmp_path / "pass-03.jsonl"
    log.write_text(claude_log(("Read", {"file_path": f"{c}/gamma.md"}, "x", False),
                              ("Bash", {"command": f"python3 x.py {c}/alpha.md"}, "", False)), encoding="utf-8")
    r = run(str(log))
    assert r.returncode == 0
    assert r.stdout == f"- {GAMMA}\n"
    assert "1 call(s) name a corpus path the script did not judge" in r.stderr
    assert "`python3` is not a program the script judges" in r.stderr


def test_the_command_exits_two_on_a_missing_log(tmp_path):
    r = run(str(tmp_path / "pass-99.jsonl"))
    assert r.returncode == 2 and "pass-99.jsonl" in r.stderr and r.stdout == ""


def test_the_command_exits_two_on_a_log_it_cannot_read_never_none(tmp_path):
    # `none` from a log the script could not parse would be the typed-`none` error again (SWCB #169)
    for name, text in (("pass-01.jsonl", ""), ("pass-02.md", "# Coordinator notes\n\nRead the brief.\n"),
                       ("pass-03.log", "Reading additional input from stdin...\nsome tool's plain output\n")):
        log = tmp_path / name
        log.write_text(text, encoding="utf-8")
        r = run(str(log))
        assert r.returncode == 2 and r.stdout == "", name
        assert name in r.stderr and "no JSON lines" in r.stderr, r.stderr


def test_the_command_reads_a_codex_text_log(repo, tmp_path):
    log = tmp_path / "pass-07.log"
    log.write_text(codex_text(str(canon(repo)), (f"/bin/zsh -lc 'cat alpha.md'", "succeeded", "# alpha")),
                   encoding="utf-8")
    r = run(str(log))
    assert r.returncode == 0 and r.stdout == f"- {ALPHA}\n" and r.stderr == ""
