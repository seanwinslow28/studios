# launchd.

launchd is the scheduler built into macOS. It starts every background job on the Mac, including Sean's overnight ones. Two built-in tools drive it: launchctl loads, runs and inspects jobs, and plutil checks the job files. Read this before writing, changing or diagnosing a scheduled job.

## What it's best at.

- **Jobs that catch up after sleep.** A job set for a time of day runs when the Mac next wakes if it slept through that time. cron, the older Unix scheduler, simply skips it.
- **Telling you what happened.** `launchctl print` shows how many times a job ran, its last exit code, the exact program and the environment it got.
- **Running without anyone logged in,** for jobs that need it (daemons, below).

Where another tool beats it: LaunchControl, a paid app (about $33), shows every job and why it failed, with fixes. Sean said no to it; agents can read the same facts from `launchctl print`.

## Setup.

Built in, free, nothing to install. The man pages are the reference: `man launchctl` and `man launchd.plist`. Apple's older guide, "Creating Launch Daemons and Agents", last updated in 2016, still explains the basics.

**The command that proves it works,** read-only, listing your jobs and their last exit codes:

```bash
launchctl print gui/$(id -u) | head -40
```

## Agents and daemons.

- **A user agent** runs as you, only while you're logged in. Its file lives in `~/Library/LaunchAgents`. Devcraft's jobs are agents, so the Mac Mini has to stay logged in for them to run.
- **A daemon** runs at boot, with or without anyone logged in. Its file lives in `/Library/LaunchDaemons`, owned by root. It needs admin rights to install, so it's a bigger step and Sean's call.

Job files must not be writable by anyone but their owner. launchd refuses them otherwise, since whoever can edit the file chooses what runs.

## The keys that matter.

A job file is a plist (Apple's settings format, XML here), named after its label:

```xml
<key>Label</key><string>com.example.nightly</string>
<key>ProgramArguments</key><array>
  <string>/Users/you/project/.venv/bin/python</string>
  <string>/Users/you/project/job.py</string>
</array>
<key>WorkingDirectory</key><string>/Users/you/project</string>
<key>StartCalendarInterval</key><dict>
  <key>Hour</key><integer>2</integer><key>Minute</key><integer>30</integer>
</dict>
<key>StandardOutPath</key><string>/Users/you/project/logs/nightly.log</string>
<key>StandardErrorPath</key><string>/Users/you/project/logs/nightly.err.log</string>
<key>EnvironmentVariables</key><dict>
  <key>PATH</key><string>/usr/bin:/bin</string>
</dict>
```

- **Label:** the job's unique name. Required.
- **ProgramArguments:** the program and its arguments, one string each. There's no shell, so `~`, `$HOME`, pipes and wildcards mean nothing. The first entry should be a full path.
- **StartCalendarInterval:** a time of day, cron-style; a missing field means "every". Several times go in an array.
- **StartInterval:** every so many seconds. A firing during sleep, or while the last run is still going, is simply missed.
- **RunAtLoad:** also run when the job is loaded. The man page advises against it, since it slows login.
- **StandardOutPath / StandardErrorPath:** where output goes. Without them, it's thrown away.
- **EnvironmentVariables:** extra variables. Values must be strings; anything else is ignored.
- **WorkingDirectory:** the folder the job starts in.

## Commands: the current set.

The domain for your agents is `gui/<your user id>`, and one job is `gui/<id>/<label>`:

```bash
plutil -lint ~/Library/LaunchAgents/com.example.nightly.plist     # syntax check
plutil -p ~/Library/LaunchAgents/com.example.nightly.plist        # readable dump
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.example.nightly.plist
launchctl bootout gui/$(id -u)/com.example.nightly
launchctl kickstart -p gui/$(id -u)/com.example.nightly             # run now
launchctl print gui/$(id -u)/com.example.nightly
```

`bootstrap` loads a job; `bootout` removes it; `enable` and `disable` decide whether it may load at all, and that state survives reboots. `kickstart` runs it now, whatever its schedule; `-k` kills a running copy first.

The old `load` and `unload` still work, but the man page lists the commands above in their place, and has a damning note: `load` and `unload` return success even when they fail, unless you mistyped the command. A script that checks their exit code learns nothing.

Editing a loaded job's file changes nothing until it is booted out and bootstrapped again. Bootstrapping a job that's already loaded fails with a vague error; boot it out first.

## Reading why a job failed.

`launchctl print gui/$(id -u)/<label>` shows, among much else:

- **`runs`** and **`last exit code`**. A job of Sean's checked today read `runs = 23`, `last exit code = 0`.
- **`program`** and **`arguments`**, exactly as launchd will run them.
- **`default environment`**, which on this Mac is `PATH => /usr/bin:/bin:/usr/sbin:/sbin`.

What the codes usually mean:

- **0:** the program ran and said it succeeded. It may still have done nothing; only the job's own log can say.
- **1 or another small number:** the program ran and failed. For Python, the traceback is in the error log.
- **78:** launchd couldn't start the program at all, for a reason in the job's setup, most often a missing program path, working folder or log folder. This is widely reported rather than documented. `launchctl error 78` misleadingly answers "Function not implemented"; ignore it.
- **A negative number** in `launchctl list`: the job was killed by that signal, so `-9` is a forced kill.

The man page says `print`'s layout isn't stable and shouldn't be parsed by programs. Read it by eye. For automated checks, have the job write its own log and timestamp.

## The world a job wakes up in.

A job doesn't get your Terminal's setup. No shell profile runs, so nothing from `.zshrc` applies. The PATH is the bare list above: no Homebrew, no `~/.local/bin`, so a bare `python3` finds Apple's old 3.9 and a bare `uv` isn't found. Write every path in full. Set any variable the job needs in `EnvironmentVariables`.

## Sleep, shutdown and missed runs.

The man page promises that a time-of-day job missed during sleep runs on wake, and that several missed times merge into one run. It promises nothing after a shutdown, so don't count on a catch-up then. `StartInterval` jobs just skip. A job meant to run nightly can therefore run at 7 a.m. after a sleepy night, or twice close together, so it must be safe to run twice. Waking the Mac on a schedule (`pmset`) is a system setting, and Sean's call.

## Privacy prompts.

macOS guards folders such as Documents, Desktop and Downloads, and Full Disk Access covers the rest. A script has no permission of its own; the grant goes to the program that runs it, here the Python interpreter. A job tested in Terminal borrows Terminal's grant, so it works by hand and fails at night with "Operation not permitted". Reports on Apple's developer forums say a grant is tied to the program's path, so a new interpreter path may need granting again. The man page warns that naming protected folders in a job file can stop it running.

## When the interpreter moves.

This is how the first job's problem plays out. A job file names an interpreter path, typically a venv's `bin/python`. That is a link to a real Python somewhere else. If that Python is upgraded away, the link points at nothing. launchd doesn't check ahead of time. At 2:30 a.m. it tries, can't start the program, records a non-zero exit code, and moves on. Python never ran, so the job's own log gets nothing, and an empty error log looks like a quiet night.

A nightly job on this Mac shows the exposure: its file names a venv's Python, and that venv links straight to one exact uv-installed release. Uninstall that release and the job stops, silently.

The defences:

- **Point at a path that survives upgrades.** The uv guide covers which.
- **Check the link before trusting it:** `ls -lL` on the program path fails if the link is broken.
- **Watch for silence.** Each good run writes a timestamp; a separate check complains when it's stale. Exit codes alone can't report a run that never started.
- **Read `last exit code` after any change** to Python, Homebrew or uv.

## Where it goes wrong.

- **A typo in the file.** `plutil -lint` catches syntax, not meaning, so check paths exist.
- **Works in Terminal, fails at night.** PATH, missing variables or privacy grants. Compare `launchctl print`'s environment with your shell's.
- **Edited but not reloaded.** Boot out, then bootstrap.
- **No log paths.** Output vanishes. Always set both.
- **Trusting `load`'s success.** Use `bootstrap`, then `print`.
- **Logged out.** Agents don't run. The Mini must stay logged in.

## Safety.

Reading is safe: `print`, `list`, `plutil -lint` and `plutil -p` change nothing. Everything else changes what runs on Sean's Mac: `bootstrap`, `bootout`, `enable`, `disable`, `kickstart`, and any edit to `~/Library/LaunchAgents`. Ask Sean first. Before changing a job, copy its file aside and try the way back once.

## More details

- `man launchctl` and `man launchd.plist` on macOS 27.0.1, read November 10, 2026. Missed-run behaviour is under `StartInterval` and `StartCalendarInterval`; the note on `load` and `unload` exit codes is in their entry.
- Apple, Creating Launch Daemons and Agents (2016): https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html
- Exit code 78 reports: https://hackernoon.com/debugging-macos-launchagent-failures-with-launchctl-and-exit-code-78
- Privacy grants and interpreters, Apple developer forums: https://developer.apple.com/forums/thread/756510
