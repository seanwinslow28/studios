# Systemcraft's tool list

The tools Systemcraft uses, one pick per kind of work, with Sean's yes or no. Scouted on November 15, 2026 for today's best, not for what the last setup used. Each tool gets a mastery guide in this folder before the lead uses it on a job.

Sean said yes to the whole list on November 16, 2026, with the two free installs. Both are installed and tested. The pay-per-use account with Anthropic waits until a job needs it.

The short version: nothing needs buying. Systemcraft makes designs and cheap proofs that a design works, and almost everything that needs is already on the Mac. Two free tools are worth adding: one for drawing bigger systems, and one for small checks worth repeating.

## Words used here

- An **agent** is a model that decides its own next step in a loop.
- A **harness** is everything wrapped around the model: its instructions, tools, memory, checks, and where a person steps in.
- A **token** is a piece of a word. Models are billed by the token.
- A **sketch** is a cheap working version of a design, built to prove it before another studio builds it properly.

## The list

| Kind of work | The pick | Cost | Have it? | Sean's answer |
|---|---|---|---|---|
| Showing Sean a design | A house review page with simple drawn pictures: one design per picture, the weaker version underneath. The shelf page was made this way. | Free | Yes | Yes |
| Drawing a bigger system | D2, a free tool that turns a short text file into a diagram. Good at boxes inside boxes (an agent, its tools, its folders) and at step-by-step boards. | Free | Yes: installed November 16, 2026 | Yes |
| A cheap working sketch | Claude Code's own parts: a skill, helpers and hooks, run without anyone at the keyboard. A run can report what it cost and be given a spending cap. | On the Claude plan | Yes | Yes |
| Seeing what a run did | Claude Code's own saved transcripts, read whole. When there are too many runs to read one by one, Arize Phoenix, a free viewer that runs on the Mac and keeps every recorded run there. | Free | Transcripts yes; Phoenix is one command, when first needed | Yes |
| Deciding how a design is judged | Read the first cases by hand in a sheet and write down what good means. Then promptfoo for checks worth repeating: cases in a short text file, results side by side in a report file. | Free tool; each check is a model call | Yes: promptfoo installed November 16, 2026 | Yes |
| What a design costs to run | The model makers' own price pages, read fresh for each job, plus ccusage, which adds up what past runs on this Mac used. | Free | Yes; ccusage runs with no install | Yes |
| Checking a design for safety | A one-page checklist: the three-part rule on the shelf (private data, outside text, a way to send things out: never all three), the "at most two" version of it, and the OWASP lists. Proved with Claude Code's sandbox, which blocks a run from reaching the network. | Free | Yes | Yes |
| Keeping up with models and tools | The makers' changelogs, plus Context7 for pulling a tool's current documents into a session. | Free up to 1,000 look-ups a month | Yes | Yes |
| What a design can count on overnight | launchd, the Mac's own scheduler, starting a Claude Code run. Borrowed from Devcraft, which has the guide. | Free | Yes | Yes |
| Research that changes a call | Two researchers on the same question: the lead in the session, and Codex as a second opinion. Borrowed from Productcraft, which tested it blind. | On the Claude and ChatGPT plans | Yes | Yes |

## Sean's two decisions

Asked on November 16, 2026, Sean answered: "Yes to the list, with the two free installs."

1. **Two free installs: D2 and promptfoo. Yes.** Both were installed and tested that day. Each promptfoo check is a model call.
2. **A pay-per-use account with Anthropic. Not now.** The Claude plan covers Claude Code, including runs with nobody at the keyboard. A few things want a separate key that is billed by the token: the Claude Agent SDK (the same engine as a standalone program), the free token counter, and promptfoo's default link to Claude. Ask again the first time a job's sketch has to be a standalone program.

## Runners-up and not now

- **Drawing:** Mermaid, which Productcraft uses and which shows up inside GitHub and Obsidian without a tool; its layouts get messy on bigger diagrams. Excalidraw for a hand-drawn look Sean can drag around; it isn't text, so an agent can't easily redraw it. That D2 lays out big systems better than Mermaid is the scout's reading, not a test; the D2 guide starts with the same system drawn in both.
- **Sketches:** the Claude Agent SDK, when a sketch must be real code (needs the pay-per-use key). Codex, to prove a design also works on OpenAI's models. LangGraph and n8n are heavier than a sketch needs. OpenAI's Agents SDK uploads every step to OpenAI unless switched off.
- **Seeing a run:** the hosted recorders (Arize AX, Langfuse, LangSmith, Braintrust) all upload every recorded step, prompts included. The 14 Arize skills already on the Mac are written for hosted Arize AX, which needs an account; local Phoenix doesn't.
- **Checks:** Inspect AI, free, from the UK's AI Security Institute, for checking a whole agent inside a sealed box; more to learn. Claude Code's own skill tester, new in September 2026, for testing one packaged skill.
- **Safety:** promptfoo's attack-testing mode, which fires real takeover attempts at a sketch. Snyk's scanner for installed skills needs an account and sends skill text to Snyk; not by default.
- **Overnight:** Claude's own scheduled tasks need no setup, but the desktop kind only fires while the app is open, and the cloud kind can't see local files. Engines that let a job pick up exactly where it stopped after a crash (Temporal, Inngest) are for the building studio; a design only needs to know they exist.

## Things to know

- **OpenAI agreed to buy promptfoo's maker in March 2026.** Whether the sale has closed could not be confirmed on November 16, 2026. It stays free and open source. Worth watching that it keeps treating other makers' models fairly.
- **promptfoo reports how it is used back to its maker unless told not to.** Found in the installed copy on November 16, 2026. Systemcraft always runs it with that reporting switched off; the switch is in "More details", and the tool's guide says so.
- **The switch does not make promptfoo fully silent.** Tested on November 16, 2026: with reporting off, each run still sends its maker one small notice saying so. The notice carries a random number for this install, the version and the kind of Mac, and no prompts, cases or answers. No switch stops it. Its results page in the browser also reports to its maker's analytics, so Systemcraft reads results from a report file, which calls nothing.
- **Phoenix keeps the runs on the Mac, but by default it is not silent.** Found in its documents on November 16, 2026: its viewer counts page views and fetches fonts and a price list from the internet unless two switches are set. No run data leaves either way. The switches are in the tool's guide.
- **Phoenix can't open a run that is already saved.** It shows only runs recorded into it while it is running, so it has to be started before the run. For a run already made, the saved transcript is read directly.
- **Switching on Claude Code's sandbox no longer lets sandboxed commands run unasked.** The default changed in a recent version, found by test on November 16, 2026. A sketch that relies on the sandbox has to say so in its settings, or the run is refused before the wall is ever tested. The safety guide has the settings.
- **A run with nobody at the keyboard can't answer questions.** A design has to say what happens at each step that would normally ask permission. Tested on November 16, 2026: such a step is refused quietly, and the run still ends reporting success. So a sketch has to check for refusals itself.
- **A run with nobody at the keyboard also runs the folder's own hooks without asking whether the folder is trusted.** Pointing one at a folder someone else wrote is the risk.
- **Everything a Claude or Codex session reads goes to that company.** Only D2, ccusage, local Phoenix, the sandbox and launchd keep text on the Mac; promptfoo keeps prompts and answers on the Mac too, once its reporting is off, apart from the model calls its checks make and the small notice described above. Day-job material stays out of Systemcraft's public pages and in Sean's private work repo.
- **Prices move monthly.** The lead reads the price page at the start of a job and never works from memory.
- **Two things Productcraft's list says are on the Mac were not found on this MacBook on November 15, 2026:** Mermaid's drawing tool and any local Ollama model. They may be on the Mac Mini.

## Books

Sean bought two of the three on November 16, 2026. The third, Thinking in Systems, is not bought: he asked whether Meadows's free essay would do instead, the lead said yes, and he agreed the same day. The research, with runners-up, shops and prices, is in `books-research.md` in this folder. His books are in `~/Books/systemcraft/`, outside every repo, and the lead turns each into private notes in `systemcraft/library/books/`.

| Book | What it teaches Systemcraft | Where it stands |
|---|---|---|
| AI Engineering (Chip Huyen, 2024) | The whole craft: when to use a model at all, judging its output, what it sees, agents, cost and speed. | Already owned |
| Prompt Engineering for LLMs (Berryman and Ziegler, 2024) | What goes in front of the model, in what order, and why. | Already owned |
| Evals for AI Engineers (Shankar and Husain, 2026) | The full method for telling whether an AI system works. | Bought November 16, 2026; no copy lock |
| Designing Agentive Technology (Christopher Noessel, 2017) | Designing something that acts for a person: where they step in, and how work is handed back. | Bought November 16, 2026; no copy lock |
| Release It!, second edition (Michael Nygard, 2018) | How running systems fail, and how to contain the damage. | Borrowed from Devcraft |
| "Leverage Points: Places to Intervene in a System" (Donella Meadows, 1999 essay) | How any system behaves over time, and where a small change does the most. | Free to read on the publisher's site; all rights reserved, so only notes in the lead's own words are kept |
| Thinking in Systems (Donella Meadows, 2008) | The same ideas at book length, plus a chapter on the common ways systems go wrong. | Not bought: Sean chose the essay instead, November 16, 2026. Look again if a real job shows the essay isn't enough |

The other three books Sean owns stay as background reading.

## More details

**Checked on this MacBook, November 15, 2026, read-only.** Installed: Claude Code, the Codex and Gemini command-line tools, Ollama (no models), uv, node, gh, jq, sqlite3, Docker, Betterleaks, prek, pip-audit. Not installed that day: D2 and promptfoo (both since installed), Mermaid's command-line tool, Graphviz, Phoenix, Inspect, just, ccusage (runs through `npx`).

**Installed November 16, 2026, with Homebrew, after Sean's yes:** D2 0.9.0 and promptfoo 0.125.1. D2 drew a test diagram; promptfoo reported its version.

- promptfoo brought its own copy of Node, which stepped in front of the Mac's usual one. It was unlinked straight away (`brew unlink node`), so the usual Node 22 is the default again and promptfoo still runs on its own copy.
- Run promptfoo with `PROMPTFOO_DISABLE_TELEMETRY=1` set, so it sends no usage reports to its maker. The guide lists three more switches to set beside it.

**No install needed:** `npx ccusage@latest` and `uvx arize-phoenix serve`.

**Could not be confirmed on November 15, 2026:** whether the API credits that come with the larger Claude plans cover the Agent SDK.

**Sources:** each tool's own site, documents and pricing page, read November 15, 2026: D2, Mermaid, Excalidraw, Claude Code's documents (running without a person, sessions, sandbox, scheduled tasks, costs), the Claude plans page, promptfoo, Inspect, Arize Phoenix and AX, Langfuse, LangSmith, Braintrust, ccusage, Context7, OWASP's two top-ten lists, Meta's "Rule of Two" post, Temporal and Inngest.
