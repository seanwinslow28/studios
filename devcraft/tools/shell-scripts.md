# ShellCheck, shfmt and Bats.

Three free tools for shell scripts. ShellCheck reads a script and points out bugs before it runs. shfmt tidies the layout so every script looks the same. Bats runs tests against a script, the way pytest does for Python. Read this before writing or changing any shell script, including the small ones that launchd (macOS's scheduler) runs overnight.

## What each is best at.

- **ShellCheck: the bugs shell hides.** Unquoted variables that split on spaces, a `cd` that fails and leaves the script deleting files in the wrong folder, a failed command whose error is thrown away. Each warning has a code like `SC2086` and a wiki page explaining it.
- **shfmt: one layout, no arguments.** It also checks that the script parses at all.
- **Bats: proof the script does what it says.** Each test runs the script and checks its exit code (the number a program hands back when it finishes: 0 for success) and its output.

Where something else beats them: once a script grows logic, Python with pytest is easier to get right. See the last section but one.

## Setup.

- **ShellCheck 0.11.0** is installed (Homebrew, the latest release).
- **shfmt 3.14.1 and Bats 1.14.0** are not yet installed: `brew install shfmt bats-core`.
- **Proof they work:** `shellcheck --version; shfmt --version; bats --version`.

All three run locally and need nothing else.

## A script header that holds up.

```bash
#!/usr/bin/env bash
set -euo pipefail
```

- **`-e`** stops the script when a command fails.
- **`-u`** stops it when it uses a variable that was never set, which catches typos.
- **`-o pipefail`** makes a pipeline fail if any part fails, not just the last.

Each has traps:

- **`-e` is switched off in places.** Inside an `if` test, on the left of `&&` or `||`, and in any function called from those spots, failures don't stop anything. `local out=$(cmd)` also hides `cmd`'s failure, because the exit code is `local`'s. Declare first, assign on the next line (ShellCheck's `SC2155`).
- **`-e` stops on things that aren't errors.** `grep` finding nothing returns 1. `((count++))` returns 1 when `count` was 0. Write `grep ... || true` where no match is fine, and `count=$((count + 1))`.
- **`pipefail` and early readers.** `some_cmd | head -1` can fail when `head` stops reading and `some_cmd` is cut off mid-write.
- **`-u` and arguments.** `$1` with no arguments stops the script; use `${1:-}` and then check it.
- **The Mac's own bash is 3.2, from 2007.** `#!/usr/bin/env bash` picks the first `bash` on the path. launchd starts jobs with a short path (`/usr/bin:/bin:/usr/sbin:/sbin`), so an overnight job gets 3.2 even if Homebrew's bash 5 is what you tested with. Under 3.2 with `-u`, expanding an empty array stops the script, and newer features such as `mapfile` don't exist. Test with `/bin/bash`, or name the bash you mean in the shebang line.

Clean up with a trap, so temporary files go even when the script fails:

```bash
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
```

## Quoting.

Quote every expansion: `"$var"`, `"$(cmd)"`, `"$@"`. Unquoted, the shell splits the value on spaces and expands `*` into file names. A path like `~/Library/Application Support` becomes two arguments, and `rm -rf $dir/` with an empty `$dir` becomes `rm -rf /`. Pass a list of options as an array, `opts=(--quiet --force)` then `cmd "${opts[@]}"`, never as a space-separated string. Prefer `[[ ... ]]` to `[ ... ]` in bash; it doesn't split words.

## ShellCheck's most important warnings.

- **`SC2086`, unquoted variable.** `cp $src $dest` breaks on spaces. Write `cp "$src" "$dest"`.
- **`SC2046`, unquoted command output.** `rm $(find . -name '*.tmp')` splits names. Use `find ... -delete` or a `while read` loop.
- **`SC2068`, unquoted `$@`.** Arguments with spaces get split. Write `"$@"`.
- **`SC2164`, `cd` without a fallback.** `cd "$dir"; rm -rf build` deletes in the wrong place if `cd` fails. Write `cd "$dir" || exit 1`.
- **`SC2155`, declare and assign together.** Hides the command's failure (above).
- **`SC2181`, checking `$?` afterwards.** `cmd; if [ $? -ne 0 ]` is fragile; write `if ! cmd; then`.
- **`SC2034`, variable never used.** Often a typo in the name where it's used.
- **`SC1091`, sourced file not followed.** Tell ShellCheck where it is with `# shellcheck source=lib/common.sh`.

Release 0.11.0 turned off the "useless use of cat" warning (`SC2002`) by default and added `SC2329` for functions that are never called. Optional checks, off by default, are listed by `shellcheck --list-optional`; `require-variable-braces` and `check-unassigned-uppercase` are worth trying. Put choices for a whole project in a `.shellcheckrc` file, such as `enable=check-unassigned-uppercase`, so every run agrees.

**Disable a warning narrowly, with a reason.** A directive above a command covers only that command; one right after the shebang line covers the whole file, so avoid that. Write why at the end:

```bash
# shellcheck disable=SC2029 # $remote_dir is meant to expand here, before sending
ssh "$host" "ls $remote_dir"
```

If you can't write a reason, fix the warning instead.

## shfmt.

```bash
shfmt -i 2 -ci -bn -s -w scripts/   # format in place
shfmt -d scripts/                    # show a diff; exit 1 if anything would change
```

`-i 2` indents two spaces (the default is tabs), `-ci` indents `case` branches, `-bn` lets a line start with `&&` or `|`, `-s` simplifies code where the meaning is unchanged, `-w` writes the files. `-l` lists files that would change and, since 3.13, exits with an error when it lists any. Better than flags: put the settings in `.editorconfig`, which editors also read:

```ini
[*.{sh,bash,bats}]
indent_style = space
indent_size = 2
case_indent = true
binary_next_line = true
```

Beware: any formatting flag on the command line makes shfmt ignore `.editorconfig` entirely. Use flags or the file, not both.

## Bats.

```bash
#!/usr/bin/env bats
bats_require_minimum_version 1.14.0

setup() {
  fakebin="$BATS_TEST_TMPDIR/bin"
  mkdir -p "$fakebin"
  log="$BATS_TEST_TMPDIR/brew.log"
  cat >"$fakebin/brew" <<EOF
#!/bin/bash
echo "brew \$*" >>"$log"
EOF
  chmod +x "$fakebin/brew"
  PATH="$fakebin:$PATH"
}

@test "skips Homebrew's Python when upgrading" {
  run -0 "$BATS_TEST_DIRNAME/../upgrade.sh"
  [[ "$output" == *"skipping python@3.14"* ]]
  run ! grep -q "python@3.14" "$log"
}
```

- **`run`** captures the exit code in `$status`, the output in `$output` and `${lines[@]}`, and never fails by itself. `run -0` (or `-1`, `-2`...) also checks the exit code; `run !` expects any failure, which is how to check that something did not happen. `run --separate-stderr` puts error output in `$stderr`.
- **`setup` and `teardown`** run around every test; `setup_file` and `teardown_file` once per file. `$BATS_TEST_TMPDIR` is a fresh folder for each test, so nothing needs cleaning by hand.
- **Fakes first on the path.** The test above puts a fake `brew` ahead of the real one. It records how it was called and touches nothing. The script must call `brew` by name for this to work, not `/opt/homebrew/bin/brew`. When a script needs a full path, let a variable choose it, `BREW="${BREW:-/opt/homebrew/bin/brew}"`, and the test sets `BREW`.
- **Pipes.** `run cmd | grep x` pipes `run`'s own output, not the command's. Use `run bats_pipe cmd \| grep x`.
- **Bats 1.14 changes:** `run` now honours `set -e` inside your functions, so a failing middle line stops the function as it would in real use; and a run that finds no tests is now an error.

## When a script should become Python.

Shell is the right tool for gluing a few commands together. Move to Python when:

- **It holds data:** lists of records, JSON beyond a single `jq` line, dates and times, sums with decimals.
- **It needs to recover from errors,** not just stop.
- **Its logic deserves unit tests,** not only end-to-end ones.
- **You're fighting quoting** or reaching for arrays of arrays.

The catch on these Macs: a Python script run by launchd must use Python that uv installed and pinned, never Homebrew's. That's the point of Devcraft's first job.

## Where it goes wrong.

- **Tested in one shell, run in another.** Homebrew's bash in the terminal, `/bin/bash` 3.2 under launchd. Run the tests with the bash the job will use.
- **Tested with your full environment.** launchd gives a short path and few variables. A script that finds `brew` in your terminal may not find it at night.
- **Blanket disables.** `disable=SC2086` at the top of a file hides every future quoting bug. Disable per line, with a reason.
- **Formatter flags in one place, `.editorconfig` in another,** and two people's tools rewriting each other's work.
- **Tests that run the real tool.** A Bats test that calls the real `brew upgrade` changes the machine. Fake it on the path, or test in a throwaway Mac (see the Tart guide).

## Safety.

All three run locally and upload nothing. ShellCheck and Bats change no files; `shfmt -w` rewrites them, so start from a clean git state. Bats runs the script for real: anything it calls that isn't faked really happens.

## More details

- ShellCheck wiki (each warning, directives, optional checks): https://github.com/koalaman/shellcheck/wiki. Releases: https://github.com/koalaman/shellcheck/releases
- shfmt manual: https://github.com/mvdan/sh/blob/master/cmd/shfmt/shfmt.1.scd. Releases: https://github.com/mvdan/sh/releases
- Bats docs: https://bats-core.readthedocs.io/en/stable/writing-tests.html. 1.14.0 notes: https://github.com/bats-core/bats-core/releases/tag/v1.14.0
