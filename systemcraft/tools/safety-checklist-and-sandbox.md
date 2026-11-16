# Safety checklist and sandbox

Systemcraft checks a design for safety in two steps. First come five plain questions that fit on one page and take a few minutes. Then the claims that matter are tested on something running, inside the sandbox built into Claude Code: a wall, kept by the Mac itself, around the commands a run starts. Read this before telling Sean a design is safe. Everything here was checked on November 16, 2026.

Two terms. An agent is a model that decides its own next step in a loop. Prompt injection is text inside a web page, email or file that gives the model orders, which it may follow as if they came from its owner.

## What it's best at

- **The checklist finds the dangerous combination before anything is built.** It asks what each part is able to do, not how well it will behave.
- **The sandbox turns a sentence into something shown.** "This step can't reach the network" becomes a command that was tried and refused.

Where something else beats it: the sandbox covers shell commands only. A wall around a whole run takes a container or a separate machine, as Stripe uses (`research/stripe-minions.md`).

## The checklist

**1. The three-part rule.** Does any one part of the design hold private information, read text written by outsiders, and have a way to send things out, all at once? This is Simon Willison's "lethal trifecta" (`research/lethal-trifecta-and-camel.md`).

- Pass: the design says which of the three each part lacks, and what takes it away (no tool, no key, no network).
- Fail: one agent that reads email, holds private files and can send messages. Or: "its instructions tell it not to."

**2. The "at most two" version.** Meta's "Agents Rule of Two" names three properties: the agent can process untrustworthy inputs, can reach sensitive systems or private data, and can change state or communicate externally. Within one session, no more than two. It differs from the three-part rule in three ways:

- **The third property is wider.** It covers any change, such as a delete or a purchase, not only sending data out. The nine-second deletion (`research/nine-second-database-deletion.md`) leaked nothing, so only this version catches it.
- **It counts per session.** A fresh session starts the count again. A session may also switch one way: browse the web first, then lose its way out before touching private systems.
- **It says what to do when all three are needed.** The agent may not run alone: a person approves, or another reliable check does.

Meta says passing isn't enough alone: it doesn't cover plain mistakes or too many powers.

- Pass: every session is marked with its two properties, and any that needs three names its supervising step.
- Fail: all three, with trust that the model will be careful.

**3. What is outside the agent.** Five brakes, and none may depend on the model behaving: narrow keys (test systems only, short-lived), an undo for anything that deletes, a person for anything that destroys, a cap on spending, and walls around where it runs.

- Pass: each brake names what enforces it: the host, the key, the Mac.
- Fail: a brake that lives in the instructions. In the deletion case the instructions said no, and the key worked on everything.

**4. The two OWASP lists, as a last sweep.** OWASP is a security non-profit that keeps lists of the ten most common risks. Read down both and ask of each line, "where could this happen here?" Write a fix, or "not here, because". The lists are not the method: they name what goes wrong, not what to build.

Top 10 for LLM Applications, 2025 edition (published November 17, 2024):

1. Prompt injection: planted text takes over the model.
2. Sensitive information disclosure: it gives out private or secret material.
3. Supply chain: a model, data set or add-on from someone else is bad.
4. Data and model poisoning: bad material is planted in what the model learns from.
5. Improper output handling: its output is passed to other software unchecked.
6. Excessive agency: more tools, powers or freedom than the job needs.
7. System prompt leakage: its instructions get out, with any secrets kept in them.
8. Vector and embedding weaknesses: the store it looks things up in is poisoned or leaks.
9. Misinformation: confident wrong answers that people rely on.
10. Unbounded consumption: no cap on use, so cost or load runs away.

Top 10 for Agentic Applications, 2026 edition (published December 9, 2025):

1. Agent goal hijack: planted text changes what the agent is trying to do.
2. Tool misuse: a proper tool is bent to a harmful use.
3. Identity and privilege abuse: keys or borrowed rights let it act beyond its job.
4. Agentic supply chain: a tool or add-on it loads while running is poisoned.
5. Unexpected code execution: text it reads ends up run as code.
6. Memory and context poisoning: something planted in its memory steers later runs.
7. Insecure inter-agent communication: forged messages between agents.
8. Cascading failures: one bad result spreads through the automated steps.
9. Human-agent trust exploitation: a polished explanation gets a person to approve harm.
10. Rogue agents: an agent drifts from its job, hides it, or acts for itself.

**5. Approval prompts are not a safety design.** People learn to click through them. The authors of CaMeL, the design on the shelf, say so, and Meta lists a blindly confirmed warning as a way its own rule fails. Take the ability away instead, and ask a person only for the rare, costly thing that can't be undone.

- Pass: the design counts how often a person is asked on a normal day, and the number is small.
- Fail: "the user approves each action."

## Proving it with the sandbox

**What it is.** A boundary the operating system keeps around the shell commands a run starts, and whatever those start. It holds whatever the model chose to run. It is off by default, free, and already on the Mac.

**Switching it on.** Type `/sandbox` in a session, set `sandbox.enabled` in a settings file, or pass settings for one run. Systemcraft uses the one-run way, so Sean's settings files never change. The command that proves it works, from an empty folder:

```bash
claude -p "Run this shell command once and show its output word for word: touch ~/sandbox-probe" \
  --safe-mode --model haiku --max-budget-usd 0.50 --permission-mode dontAsk \
  --settings '{"sandbox":{"enabled":true,"autoAllowBashIfSandboxed":true,"allowUnsandboxedCommands":false,"failIfUnavailable":true}}'
```

It answers `Operation not permitted`, and no file appears. The four settings: on; commands inside the wall run without asking; no second try outside the wall; stop if the wall can't start.

**What it blocks and lets through, as seen here:**

| Tried inside the sandbox | What came back |
|---|---|
| Write a file in the folder | Worked |
| Write a file in the home folder | `Operation not permitted`; no file made |
| Fetch example.com | `CONNECT tunnel failed, response 403` and `deny network-outbound example.com:443` |
| Fetch it going round the checker | `Could not resolve host` |
| Fetch it once example.com was on the allowed list | 200; example.org still refused |
| Read a system file outside the folder | Worked |
| Write to another folder in Claude's temporary area | Worked |

Outside the sandbox, the same fetch returned 200.

**What it doesn't cover.** Claude's own file and web tools, hooks and connectors run outside it and follow the permission rules. Reading is open by default, key files included.

**From claim to proof.** Write the claim as one sentence. Find the command that would break it. Run it inside the sandbox with the design's own settings, and keep the refusal as evidence.

**The cheap one-person version.** From the shelf: a closed-off space, accounts that only touch test systems, and a small spending limit. Willison's example is an account capped at $5. It removes the ability instead of tracking the information, which one person can keep up.

## Where it goes wrong

- **A filter that catches most attacks.** One that stops 95% still fails: the attacker tries again.
- **A second agent as the guard.** In Project Vend (`research/project-vend.md`) the manager agent approved about eight times as often as it refused: the same model, with the same soft spots. A guard must differ in what it knows, what it's rewarded for, or by being a fixed rule.
- **A checklist ticked from the design document, never tested on the running thing.** Here, the first two runs proved nothing: the permission system refused the commands before the sandbox was reached. A "blocked" from the wrong layer looks the same in a summary.
- **Auto-allow is now off by default.** Without `autoAllowBashIfSandboxed`, a run with nobody at the keyboard has its writes refused, even inside the folder.
- **An allowed list that grows.** Claude Code's documents warn that a broad entry such as `github.com` is a way out. With open reading, that is private data plus an exit.

## Safety

- **What it uploads and spends:** the sandbox uploads nothing and costs nothing. Each test is a model call on the Claude plan; the five measured here reported about 2 cents in all.
- **Never use a flag that skips permission checks.**
- **Never test against anything live.** Use an empty folder, test accounts and example.com.
- **Attack testing waits for Sean.** Testing takeover attempts against a sketch is promptfoo's attack-testing mode, never used without asking him.

## More details

- **Versions:** Claude Code 2.1.325 on macOS 27.0.1, where the sandbox uses the Mac's own Seatbelt.
- **Runs:** six, each `claude -p` in an empty scratch folder with `--safe-mode`, `--permission-mode dontAsk`, the haiku model and a 50-cent cap, read from the raw tool output. Runs 1 and 2, without auto-allow: refused by the permission mode. Run 3: the three writes. Run 4, with `--allowedTools "Bash(curl *)"`: the network refusals, also tried with `nc` and Python. Run 5: example.com allowed. Run 6: the proof command, cost not recorded.
- **Read, not tested:** `/sandbox`; what runs outside the sandbox; that key files are readable; the allowed-list warning.
- **Sources, read November 16, 2026:**
  - Sandbox: https://code.claude.com/docs/en/sandboxing
  - Settings (`autoAllowBashIfSandboxed` default `false` since 2.1.324): https://code.claude.com/docs/en/settings-reference
  - Permission modes: https://code.claude.com/docs/en/permission-modes
  - `claude --help`
  - Meta, "Agents Rule of Two: A Practical Approach to AI Agent Security", October 31, 2025: https://ai.meta.com/blog/practical-ai-agent-security/
  - OWASP LLM list: https://genai.owasp.org/llm-top-10/ and its ten item pages
  - OWASP agentic list: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
  - OWASP's launch post, December 9, 2025: https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/
- **Not confirmed:** the agentic list's full document is a download and was not opened; its ten names come from OWASP's launch post. No newer edition of the LLM list was found on OWASP's site.
