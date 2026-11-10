# Betterleaks and prek.

The pair that checks every commit in the studios repo before it exists. Betterleaks looks for passwords, keys and tokens. prek is the hook manager: it decides which checks run at which moment and runs them fast. A **hook** is a script git runs on its own at a set moment, here just before a commit is made and just after its message is written.

## What they're best at.

**Betterleaks** reads text and spots secrets by their shape: a GitHub token's prefix and length, a cloud key's pattern, a private key's header, plus a measure of how random a string looks (its "entropy"). It was written by the original author of Gitleaks and keeps Gitleaks's commands and config format, so Gitleaks works as a stand-in with no changes. It is at its best on the staged change, the few lines about to be committed, where it runs in well under a second. It can also sweep a whole history, a folder, or anything piped to it.

It is not a name finder. It knows what secrets look like, not what Sean considers private. Names on his private list are caught by the studios repo's own small script, `craftwork/checks/private-names.sh`, which prek runs beside it.

**prek** reads the same `.pre-commit-config.yaml` the older pre-commit tool uses, but it is one small program with no Python inside. That matters here: Devcraft's first job is about Python breaking under upgrades, and a commit check that breaks with it would fail exactly when it's needed. prek runs local scripts, shared hooks from other repos, and its own built-in ones.

Where another tool wins: a hosted scanner on GitHub catches what slips past a laptop, such as a commit made with the hook switched off. For checks that must run on every machine with nothing installed, plain git hooks still work; they're just harder to share and keep in step.

## Setup.

Both are free and installed with Homebrew:

```
brew install betterleaks prek
betterleaks version && prek --version
```

The studios repo keeps prek's two small launcher scripts in `.githooks/`, tracked like any other file. Each clone points git at them once:

```
git config core.hooksPath .githooks
```

`core.hooksPath` is git's setting for where its hooks live. Setting it, rather than copying files into the hidden `.git/hooks` folder, means every worktree of the clone, every agent and every commit Sean makes by hand gets the same checks. The launchers call prek by its full Homebrew path and fall back to whatever `prek` is on the PATH. To rebuild them after a prek upgrade, run `prek install -t pre-commit -t commit-msg` from the top of the repo: prek writes into whatever folder `core.hooksPath` names.

The one command that proves it all works:

```
uvx --from pytest pytest craftwork/checks/test_commit_checks.py
```

It builds throwaway repos, plants a made-up name and a made-up token, and checks that each is stopped, that neither is ever printed, and that a missing list or scanner stops the commit instead of waving it through.

## Getting the best out of them.

- **Scan the staged change, not the files.** `betterleaks git --pre-commit --staged` reads only what this commit adds. A whole-folder scan in a hook is slow and flags things committed long ago that this commit can't fix.
- **Always redact, and say only where.** `--redact` hides the secret itself, but `--verbose` still prints the rest of its line, which can hold a private name. The studios check prints just file, line and rule through a report template (`--report-format template --report-template <file> --report-path -`), which is safe to paste into a chat or a log. With neither, Betterleaks only says how many it found.
- **Never switch on validation in a hook.** Betterleaks can check whether a key is live by trying it against the provider's servers (`--validation`). That sends the secret off the machine. It is off unless asked for; leave it off.
- **Mark a real false alarm in place, once.** A line that looks like a secret but isn't, such as an example key in a test, gets a `betterleaks:allow` comment at its end. For a finding that can't carry a comment, add its fingerprint to a `.betterleaksignore` file. The fingerprint reads `path:rule:line`, such as `config.py:github-pat:12`; the JSON report (`--report-format json --report-path -`) prints it. Either way, the reason goes in the commit message. Never widen the rules to quiet one finding.
- **Build test secrets at run time.** A test that needs a token-shaped string should assemble it while running, so the test file itself never looks like a leak. The studios repo's tests do this.
- **Sweep history when it matters.** Before a private repo goes public, or after a scare, scan everything: `betterleaks git --redact --verbose .`, read in a private terminal, since `--verbose` prints each finding's line. A key found in history is already exposed; the fix is to revoke it at the provider, not only to delete the line.
- **One hook, one job, plain names.** In prek's config each hook's `name` is what prints when it fails, so write it as the thing it protects: "no passwords, keys or tokens". `prek list` shows every hook; `prek run --all-files` runs them across the repo, useful after changing a check.
- **Stages keep checks where they belong.** A hook tagged `stages: [commit-msg]` gets the message file, which is the only way to check message text. The name check runs at both moments, because a commit message is as public as the code.

## Where it goes wrong.

- **A check that couldn't run looks like a pass.** If the scanner isn't installed, or the name list is missing on a new machine, a careless script exits cleanly and every commit sails through. The studios repo's scripts stop the commit and say what's missing. Keep it that way.
- **The private list leaks itself.** A rule file naming what to hide, committed to a public repo, publishes the very names it protects. The list stays in Sean's home folder; only the path to it is in the repo.
- **Printing what was found.** A message like "found ACME in line 3" leaks the name into the terminal, an agent's log, or a chat transcript. Say where, never what.
- **Skipping the hook becomes a habit.** `git commit --no-verify` jumps every check. It is there for emergencies. An agent should never use it; if a check is wrong, fix the check.
- **False alarms breed blanket ignores.** Each ignore should be one line, one finding, one reason. A config that turns off a whole rule because of one noisy file stops catching that kind of secret everywhere.
- **The hook folder moves.** If someone runs `prek install` with `core.hooksPath` unset, prek writes into `.git/hooks` instead, and the tracked launchers drift from what actually runs. Check with `git config --get core.hooksPath`.
- **Gitleaks as a long-term home.** Gitleaks still works and uses the same rules, but its last release was in March 2026. Use it only as the stand-in.

## Safety.

Neither tool uploads anything in the way the studios repo uses them: both read files on the Mac and print to the terminal. Betterleaks talks to the internet only when validation is switched on, which it never is here. prek downloads code only for hooks pulled from another repo (`repo:` set to a URL); the studios repo's hooks are all local scripts. Adding a hook from someone else's repo means running their code on every commit, so ask Sean first.

A finding is a near miss, not an incident: nothing was committed. If a real key was ever committed, even briefly, tell Sean, and revoke and replace the key before anything else.

## Sources.

- Betterleaks 1.10.0, November 4, 2026, MIT: [releases](https://github.com/betterleaks/betterleaks/releases). Flags confirmed against `betterleaks git --help` on this Mac.
- prek 0.5.10, November 4, 2026: [releases](https://github.com/j178/prek/releases). Hook placement under `core.hooksPath` confirmed by installing into a test repo.
- Gitleaks 8.30.1, the stand-in: [releases](https://github.com/gitleaks/gitleaks/releases).
