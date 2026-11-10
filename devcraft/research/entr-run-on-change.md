# entr, the "run this again when a file changes" tool (2012 to now)

## What it is

A small command-line tool that watches a list of files and reruns a command whenever one of them changes. You hand it the file names, then the command to run. Developers use it to rerun tests or rebuild a page every time they save. Its name stands for "event notify test runner".

Made by Eric Radman, one developer, who has kept it going since the first release on April 12, 2012. The latest release is 5.9, October 1, 2026. It works on Mac, Linux and the BSD family of systems, and asks the operating system to tell it about changes instead of checking files over and over (that repeated checking is called polling, and it wastes battery and time).

Code and instructions: https://github.com/eradman/entr. Project page: https://eradman.com/entrproject/

**Best part to look at: the top of `system_test.sh`** (the test file), from line 64 on. Each test opens with a plain-English name, like "no arguments" or "empty input". You can read the list of names as a list of promises the tool keeps, without reading any code.

## How it turned out

- **Fourteen years, one maintainer, 50 releases.** The release history file lists every version back to 1.0. Steady, small releases over that long a span is strong evidence the design held up.
- **About 5,700 stars on GitHub** (a star is a public bookmark; read November 10, 2026). Packaged by Homebrew, the main Mac installer, with about 9,300 installs in the last year.
- **Julia Evans, a widely read programming writer, gave it a whole post in June 2020.** She said it gives her "a magical build experience where I get instant feedback".
- **What I couldn't find:** no big launch moment or long Hacker News thread. Its fame is quiet and word-of-mouth. The install count is modest next to bigger tools, so its standing rests on longevity and the praise of people who use it daily.

## What makes it good, measured

I counted these from a fresh copy of the code. I didn't run it.

- **Small enough to read in an afternoon:** 849 lines in the main file, plus 117 lines in one helper. That's the whole tool.
- **More test than tool, nearly:** the test script is 626 lines and holds 54 named test cases. The instructions tell you to run the tests as part of installing (the second of three install steps), so a broken build shows up before it's on your machine.
- **A README you finish in a minute:** 58 lines, five short sections. What it is (two sentences), how to install, two known quirks with their workarounds, five real examples, and where to find release news. No badges or marketing.
- **Nine options, not ninety.** The manual lists nine single-letter switches (clear the screen first, restart a server instead of rerunning, stop after one run, and so on). Each gets a short paragraph.
- **It says what happens when things go wrong.** The manual has an "exit status" section that names each result code: 0 for a normal stop, 1 for an error or no files, 2 when files were added or removed. A result code is the number a program hands back when it finishes. A script or scheduled job reads it to decide what to do next.
- **Honest about its limits.** The README names two places it can misbehave (Docker on Mac and Windows' Linux layer) and the setting that fixes each.

### Why it's here

It's the model for "does one thing superbly": a tool small enough to read, a test list that doubles as a promise list, and a manual that tells a calling script exactly what each outcome means. That last part matters for Devcraft's scheduled-job work, where nothing is watching and the exit code is the only signal.

## What Sean said about it

On the shelf Sean saw on November 10, 2026. He didn't single this one out; his pick was uv's design.

## More details

- Repository: https://github.com/eradman/entr (code, README, `NEWS` release history, `entr.1` manual, `system_test.sh`)
- Project page with examples: https://eradman.com/entrproject/
- Julia Evans, "entr: rerun your build when files change" (June 28, 2020): https://jvns.ca/blog/2020/06/28/entr/
- Homebrew install counts: https://formulae.brew.sh/formula/entr (365-day figure read from Homebrew's public analytics on November 10, 2026)
- Star count read from GitHub's API on November 10, 2026. The GitHub repository dates from 2018; earlier releases lived on Bitbucket, per the release history.
- My measurements: line counts with `wc -l`; test cases counted as lines starting with `try "` in the test script; options counted from the manual's option list.
