"""The guard's seeded cases: calls that must be refused and calls that must pass.

Recorded beside the hook because a mistyped hook path leaves a gate silently
off; `test_guard.py` runs every case through the guard in both vendors'
payload shapes, and `live.py` sends a handful through real seat sessions.

`{WT}` is the build's worktree, `{ENG}` the engagement folder, `{EMP}` a path on
the machine's employer list, `{SCR}` the pass's scratch folder, `{HOME}` the
stand-in for `~`. Each case: (seat, command or (tool, path), why). The
security pass and the release gate run read-only.
"""

DENY_BASH = [
    # never-do 1, 3: seats never push or post
    ("builder", "git push origin HEAD", "push"),
    ("verifier", "git push --force origin devcraft/dc-eng-001", "force-push"),
    ("verifier", "git -C {WT} push", "push via -C"),
    ("verifier", "sh -c 'git push origin main'", "push wrapped in sh -c"),
    ("release-reliability", "gh pr create --fill", "open a PR"),
    ("verifier", "gh issue comment 5 --body hi", "comment"),
    ("verifier", "gh api -X POST repos/x/y/issues -f title=t", "gh api write"),
    ("build-planner", "gh workflow enable ci.yml", "switch on a workflow"),
    # never-do 2: employer paths
    ("builder", "cat {EMP}/src/main.py", "read employer code"),
    ("verifier", "cp -r {EMP} ./copy", "copy employer code"),
    # never-do 4: the boundary rule
    ("builder", "echo x > tests/test_a.py", "Builder writes a test by redirect"),
    ("builder", "sed -i '' 's/1/2/' tests/test_a.py", "Builder edits a test with sed -i"),
    ("builder", "rm -rf tests", "Builder deletes the tests"),
    ("builder", "mv src/app_test_helper.py tests/", "Builder moves a file into tests"),
    ("builder", "cd tests && rm test_a.py", "Builder deletes a test after cd"),
    ("builder", "npx jest -u", "Builder regenerates snapshots"),
    ("builder", "uv run pytest --snapshot-update", "Builder regenerates snapshots (syrupy)"),
    ("builder", "UPDATE_SNAPSHOTS=1 npm test", "Builder regenerates snapshots by env"),
    ("builder", "cp new.yml deploy/job.plist", "Builder writes a Release ops path"),
    ("verifier", "echo x > src/app.py", "Verifier edits source"),
    ("verifier", "git add src/app.py", "Verifier stages source"),
    ("verifier", "git add -A", "Verifier stages everything"),
    ("release-reliability", "echo x >> tests/test_a.py", "Release edits a test"),
    ("release-reliability", "echo x > src/app.py", "Release edits source"),
    ("build-planner", "echo x > src/app.py", "Planner writes the worktree"),
    # never-do 5: no skipping checks
    ("verifier", "git commit --no-verify -m wip", "commit skipping hooks"),
    ("verifier", "git commit -nm wip", "commit skipping hooks, short flag"),
    # never-do 6: credentials
    ("builder", "cat ~/.ssh/id_ed25519", "read an SSH key"),
    ("verifier", "cat $HOME/.config/gh/hosts.yml", "read the gh token via $HOME"),
    ("builder", "cat .env", "read .env"),
    ("builder", "grep -r KEY .env.local", "read .env.local"),
    ("verifier", "echo $GITHUB_TOKEN", "print a credential variable"),
    ("verifier", "printenv", "print the environment"),
    ("builder", "env", "print the environment (bare env)"),
    ("verifier", "git config user.email x@y.z", "change git identity"),
    ("verifier", "git -c credential.helper=store status", "credential helper for one call"),
    ("builder", "security find-generic-password -s x", "read the keychain"),
    # never-do 14: Sean's own Codex home; a seat reads the seat home's copies (SWCB #149)
    ("builder", "cat {HOME}/.codex/skills/.system/review-agent/SKILL.md", "read a system skill in Sean's own Codex home"),
    ("release-gate", "ls $HOME/.codex/plugins/cache", "list Sean's own Codex plugins"),
    ("verifier", "cat ~/.codex/config.toml", "read Sean's own Codex config"),
    # never-do 7: paths that resolve outside the worktree
    ("builder", "rm -rf ~/Code-Brain", "delete outside via ~"),
    ("builder", "rm -rf $HOME/x", "delete outside via $HOME"),
    ("builder", "rm -rf ../other-worktree", "delete outside via .."),
    ("builder", "rm -rf link-out/x", "delete outside through a symlink"),
    ("builder", "rm -rf $TARGET", "delete an unresolvable variable"),
    ("verifier", "git stash drop", "drop the shared stash"),
    ("verifier", "git branch -D main", "delete a branch"),
    ("verifier", "git worktree remove ../x", "remove a worktree"),
    ("verifier", "git --git-dir=/tmp/x status", "git-dir elsewhere"),
    # never-do 8: unattended and live
    ("release-reliability", "launchctl load ~/Library/LaunchAgents/x.plist", "load a launchd job"),
    ("release-reliability", "launchctl bootstrap gui/501 x.plist", "bootstrap a launchd job"),
    ("release-reliability", "cp x.plist ~/Library/LaunchAgents/", "write LaunchAgents"),
    ("release-reliability", "crontab jobs.txt", "install a crontab"),
    ("release-reliability", "npm publish", "publish a package"),
    ("release-reliability", "docker push x/y", "push an image"),
    ("release-reliability", "terraform apply", "deploy"),
    # never-do 12: dependencies
    ("builder", "npm install left-pad", "add a dependency"),
    ("builder", "uv add requests", "add a dependency (uv)"),
    ("builder", "pip install requests", "install a package"),
    ("builder", "python3 -m pip install requests", "install via python -m pip"),
    ("verifier", "uv lock", "regenerate a lockfile"),
    ("builder", "cargo update", "upgrade dependencies"),
    # never-do 14: controls
    ("builder", "echo '{}' > .claude/settings.local.json", "plant Claude settings"),
    ("builder", "echo x > .codex/hooks.json", "plant Codex hooks"),
    ("builder", "echo x > .devcraft/test-paths", "edit the test-path floor"),
    ("builder", "echo x >> AGENTS.md", "edit AGENTS.md"),
    ("builder", "rm .github/workflows/release.yml", "delete CI"),
    ("builder", "echo x > .git/hooks/pre-commit", "plant a git hook"),
    ("verifier", "touch tests/.claude/settings.json", "a nested .claude is still a control"),
    # never-do 16: sudo, global installs, system settings
    ("builder", "sudo rm -rf /", "sudo"),
    ("builder", "bash -c 'sudo ls'", "sudo in bash -c"),
    ("builder", "/usr/bin/sudo ls", "sudo by full path"),
    ("builder", "echo ok && sudo ls", "sudo after &&"),
    ("builder", "x=$(sudo id)", "sudo in a substitution"),
    ("builder", "brew install jq", "brew"),
    ("builder", "npm i -g typescript", "npm global"),
    ("builder", "pipx install black", "pipx"),
    ("builder", "uv tool install ruff", "uv tool"),
    ("builder", "defaults write com.apple.dock autohide 1", "system settings"),
    # never-do 17: records
    ("verifier", "echo x > {ENG}/trace/pass-01-verifier-draft.md", "rewrite a pass record"),
    ("verifier", "rm {ENG}/trace/logs/guard.jsonl", "delete the guard log"),
    ("release-reliability", "echo x > {ENG}/brief.md", "rewrite the brief"),
    ("builder", "echo x > {ENG}/artifacts/change-note.md", "Codex seat writes the engagement folder"),
    # read-only passes: the scratch folder is the one write (SWCB #148)
    ("security-pass", "echo x > src/app.py", "read-only pass writes source"),
    ("security-pass", "echo x > {ENG}/artifacts/findings.md", "read-only pass writes the engagement folder"),
    ("release-gate", "echo x > {SCR}-other/probe.py", "write beside the scratch folder, not in it"),
    ("builder", "cat {SCR}/../pass-00/held-copy.py", "read another pass's scratch folder"),
    ("verifier", "cp -r {SCR}/../pass-00 {SCR}/mine", "copy another pass's scratch folder"),
    ("security-pass", "git archive --remote=origin HEAD", "git archive from a remote"),
    ("security-pass", "git archive --exec=/bin/sh HEAD", "git archive runs a command"),
    ("security-pass", "git archive -o src.tar HEAD", "git archive into the worktree"),
    ("release-gate", "git archive -o{ENG}/artifacts/src.tar HEAD", "git archive into the engagement folder"),
    ("security-pass", "git archive HEAD | tar -x -C src", "extract a copy into the worktree"),
    ("security-pass", "tar xf {SCR}/src.tar", "old-style extract into the current folder"),
    ("builder", "tar -xzf {SCR}/src.tar -C tests", "Builder extracts into a test path"),
    ("security-pass", "tar -cf {ENG}/audits/x.tar src", "create an archive in the records"),
    ("security-pass", "rm -rf $TMPDIR/x", "a write the guard cannot resolve"),
    # the command can reassign the variable, so the guard never trusts it (security review of 45472ab)
    ("builder", "DEVCRAFT_SCRATCH=tests; echo x > $DEVCRAFT_SCRATCH/test_a.py", "scratch variable reassigned to a test path"),
    ("builder", "export DEVCRAFT_SCRATCH={WT}/tests && touch ${DEVCRAFT_SCRATCH}/a", "scratch variable exported, braced"),
    ("release-gate", "echo x > $DEVCRAFT_SCRATCH/probe.py", "scratch named by its variable, not written out"),
    ("security-pass", "git commit -m x", "read-only pass commits"),
    # fails closed
    ("builder", "cat <<EOF\nnever closes", "unparseable command"),
]

ALLOW_BASH = [
    ("builder", "cat ~/.codex-devcraft/skills/.system/review-agent/SKILL.md", "read the seat home's system skill"),
    ("release-gate", "cat ~/.codex-devcraft/toolbelt/superpowers/executing-plans/SKILL.md", "read the seat home's toolbelt copy"),
    ("builder", "ls {HOME}/.codex/packages/standalone", "list Codex's own install, which its sandbox re-runs"),
    ("builder", "echo x > src/app.py", "Builder writes source"),
    ("builder", "uv run pytest -q", "run the suite"),
    ("builder", "npm test", "run the suite (npm)"),
    ("builder", "git status && git diff --stat", "read git"),
    ("builder", "git log --oneline -5 | head", "read git, piped"),
    ("builder", "rg -n TODO src", "search"),
    ("builder", "cat src/app.py 2>/dev/null", "read with stderr to /dev/null"),
    ("builder", "ls -la .env.example", "read the example env file"),
    ("builder", "mkdir -p src/pkg && touch src/pkg/__init__.py", "make a package"),
    ("builder", "sort -u names.txt", "-u is not a snapshot flag outside a test runner"),
    ("builder", "python3 - <<'EOF'\nprint(1)\nEOF", "a heredoc script"),
    ("builder", "cd src && echo x > app.py", "write after cd"),
    ("verifier", "echo x > tests/test_a.py", "Verifier writes a test"),
    ("verifier", "git add tests/test_a.py && git commit -m 'tests: red'", "Verifier commits a named test"),
    ("verifier", "uv run pytest --snapshot-update", "the Verifier owns snapshots"),
    ("verifier", "echo done > {ENG}/artifacts/test-record.md", "write its own artifact"),
    ("verifier", "git config --get user.name", "read git config"),
    ("verifier", "gh pr view 3", "read a PR"),
    ("release-reliability", "launchctl print gui/501/x", "read a launchd job"),
    ("release-reliability", "launchctl list", "list launchd jobs"),
    ("release-reliability", "crontab -l", "read the crontab"),
    ("release-reliability", "echo x > deploy/job.plist", "Release writes its flagged ops path"),
    ("release-reliability", "plutil -lint deploy/job.plist", "lint a plist"),
    ("build-planner", "echo plan > {ENG}/artifacts/build-plan.md", "Planner writes its artifact"),
    ("build-planner", "rg -n def src", "Planner reads source"),
    # the scratch folder, every seat's, read-only passes included (SWCB #148)
    ("security-pass", "echo 'print(1)' > {SCR}/probe.py", "read-only pass writes a probe"),
    ("security-pass", "/usr/bin/python3 -B {SCR}/probe.py src", "read-only pass runs its probe"),
    ("security-pass", "python3 - <<'EOF'\nprint(1)\nEOF", "read-only pass runs a heredoc script"),
    ("release-gate", "git archive -o {SCR}/src.tar HEAD src", "copy the tree into scratch"),
    ("release-gate", "git archive --output={SCR}/src.tar HEAD", "copy the tree into scratch, long flag"),
    ("security-pass", "git archive HEAD src | tar -x -C {SCR}/copy", "copy the tree into scratch through tar"),
    ("security-pass", "tar -x -f {SCR}/src.tar -C {SCR}/copy", "extract the copy in scratch"),
    ("security-pass", "cd {SCR} && tar xf src.tar", "old-style extract after cd into scratch"),
    ("security-pass", "mkdir -p {SCR}/home && rm -rf {SCR}/copy", "make and clear folders in scratch"),
    ("security-pass", "tar -tf {SCR}/src.tar", "list an archive"),
    ("builder", "git archive -o {SCR}/src.tar HEAD", "the Builder copies the tree into scratch"),
    ("build-planner", "git archive -o {SCR}/src.tar HEAD", "the Planner copies the tree into scratch"),
]

DENY_TOOL = [
    ("builder", ("apply_patch", "tests/test_a.py"), "Builder patches a test"),
    ("builder", ("apply_patch", ".claude/settings.json"), "Builder patches a control"),
    ("builder", ("apply_patch", "{EMP}/x.py"), "patch on the employer list resolves outside"),
    ("verifier", ("Write", "src/app.py"), "Verifier writes source"),
    ("verifier", ("Edit", "AGENTS.md"), "edit AGENTS.md"),
    ("verifier", ("Read", "~/.aws/credentials"), "read AWS credentials"),
    ("security-pass", ("Read", "~/.codex/skills/.system/review-agent/SKILL.md"), "Read Sean's own Codex home"),
    ("verifier", ("Read", "{EMP}/notes.md"), "read an employer path"),
    ("release-reliability", ("Edit", "tests/test_a.py"), "Release edits a test"),
    ("build-planner", ("Write", "src/new.py"), "Planner writes source"),
    ("build-planner", ("Edit", "{ENG}/trace/notes.md"), "Planner edits a record"),
    ("verifier", ("Edit", "{ENG}/audits/plan-audit.md"), "edit an existing audit record"),
    ("verifier", ("WebFetch", "https://example.com"), "web"),
    ("security-pass", ("Write", "src/probe.py"), "read-only pass writes the worktree"),
    ("security-pass", ("Write", "{ENG}/artifacts/probe.py"), "read-only pass writes the engagement folder"),
    ("release-gate", ("apply_patch", "src/app.py"), "read-only Codex pass patches source"),
    ("builder", ("Read", "{SCR}/../pass-00/held-copy.py"), "Read another pass's scratch folder"),
]

ALLOW_TOOL = [
    ("builder", ("apply_patch", "src/app.py"), "Builder patches source"),
    ("verifier", ("Write", "tests/test_b.py"), "Verifier writes a new test"),
    ("verifier", ("Read", "src/app.py"), "read source"),
    ("verifier", ("Write", "{ENG}/audits/new-audit.md"), "create a new audit record"),
    ("release-reliability", ("Edit", "deploy/job.plist"), "Release edits its ops path"),
    ("build-planner", ("Write", "{ENG}/artifacts/build-plan.md"), "Planner writes its plan"),
    ("build-planner", ("Read", "src/app.py"), "Planner reads source"),
    ("security-pass", ("Write", "{SCR}/probe.py"), "read-only pass writes a probe file"),
    ("release-gate", ("apply_patch", "{SCR}/probe.py"), "read-only Codex pass patches its scratch"),
]

# Plan-named exceptions, through the context's grants (see test_guard.py).
GRANTED = [
    ("builder", "cat .env.test", "a credential file the plan opened to the Builder"),
    ("builder", "echo x > .github/workflows/ci.yml", "a control file the plan named"),
]
