# Justin Mayer's "Homebrew Python Is Not For You" (2021)

## What it is

A short blog post that explains, in plain terms, the exact failure behind Devcraft's first job. Homebrew, the main Mac installer, ships its own Python. Many people build their projects on it. But Homebrew keeps that Python mainly so its other packages can run, and it upgrades and removes it on its own schedule. When it does, every project box built on the old copy (a "virtual environment", or venv: a private set of Python add-ons for one project) breaks.

Written by Justin Mayer and published February 3, 2021. He's a long-time maintainer of Pelican, a popular Python tool for building websites, with about 1,200 changes to its code, the most of anyone.

Read it: https://justinmayer.com/posts/homebrew-python-is-not-for-you/

**Best part to look at: the "What's the Problem?" section.** In a few paragraphs it lays out the chain: you upgrade an unrelated package, that quietly upgrades Python, Homebrew's cleanup deletes the old Python, and your project box fails with a cryptic "library not loaded" error.

## How it turned out

- **Hacker News:** 82 points and 107 comments, posted under the title "Changes to Homebrew adversely affect Python development". A modest score, but a long argument. More comments than points usually means the topic hit a nerve.
- **Homebrew now says much the same thing in its own guide.** Its page on language runtimes says to use a separate Python version manager when a project needs a Python that lives independently of Homebrew's upgrades.
- **The mechanism still holds in late 2026.** Homebrew's current manual says that after an upgrade it runs a cleanup on what it upgraded, unless you turn that off.
- **Thin spot:** this is one person's blog post with a mid-sized audience, not a famous piece. It's on the shelf because it explains the problem clearly and its claims check out against Homebrew's own documents, not because of reach.

## What makes it good, measured

I read the post and checked its claims against Homebrew's current manual and package list.

- **Length:** about 770 words. Four sections: the problem, the core claim, the recommended alternative, and a short epilogue. One small code example.
- **It names the error you'd actually see,** so a reader with a broken setup can match it.
- **It names the moving parts:** automatic upgrades pulled in by other packages, and automatic cleanup that deletes old versions. It gives a check (a command that lists which installed packages depend on Python) so you can see your own exposure.
- **It weighs the obvious workaround and explains why it's fragile.** Homebrew has a setting that turns cleanup off. Mayer points out that it only works if it's set in every place Homebrew ever runs; miss one and the problem is back.
- **It's bigger now than when he wrote it.** He counted nearly 400 Homebrew packages depending on Python in 2021. I counted 774 in Homebrew's package list today, 733 of them on the newest Python. Every one of those can pull a Python upgrade when it updates.
- **Its fix is dated.** He recommends asdf, a general version manager. Since then uv (also on this shelf) has made the same idea much simpler for Python alone.

### Why it's here

It's the clearest plain-English statement of the problem Devcraft has to solve, with the cause, the symptom and the fragile workaround all named. A good fix note for the first job should explain the problem this clearly, and say why the easy workaround isn't enough.

## What Sean said about it

On the shelf Sean saw on November 10, 2026. He didn't single this one out; his pick was uv's design.

## More details

- The post (February 3, 2021): https://justinmayer.com/posts/homebrew-python-is-not-for-you/
- Hacker News thread: https://news.ycombinator.com/item?id=26017852 (read November 10, 2026)
- Homebrew's guide to language runtimes and packages: https://docs.brew.sh/Language-Runtimes-and-Packages
- Homebrew's manual, `man brew`, under `upgrade`: cleanup runs on upgraded packages unless `HOMEBREW_NO_INSTALL_CLEANUP` is set, and on everything every 30 days.
- The error he quotes is a `dyld: Library not loaded` message; the check he gives is `brew uses python --installed`; the workaround is `HOMEBREW_NO_INSTALL_CLEANUP`.
- Pelican contributor count from GitHub's API: https://github.com/getpelican/pelican
- My count: Homebrew's public package list (https://formulae.brew.sh/api/formula.json), 8,723 packages, counting those that list any `python@` version as a direct dependency. Packages that depend on Python only indirectly aren't included, so the true number is higher.
