# What the model sees and remembers

Read this when a design says what a model step is given to work from, or when a running system does something foolish and the question is what it was looking at. A model knows two things: what it learned in training, which is general and out of date, and what is put in front of it on this call. It remembers nothing between calls unless the system gives it a memory. So what the model sees is a thing that gets designed, like a page. Sean put the condition in his own words when he picked the long-job harness: it works as long as the agents are given the right tools and the right knowledge.

## What is in front of the model

On every call the model is shown one long piece of text, and nothing else. It is usually made of:

- **Standing instructions:** who it is, what the job is, what good looks like.
- **Tool descriptions:** every tool it may call, each with its name and how to use it.
- **Reference material** fetched for this request: a file, search results, a customer's record.
- **The work so far:** the conversation, the tool calls, what came back.
- **The request itself.**

All of it competes for the same room and the same attention. People call the room the context window. It has a hard limit, and long before the limit the model's grip on any one part gets looser.

## Show it less

The model treats everything it is shown as something that matters. Put in a fact that doesn't bear on the job and it will try to use it. So the first skill is leaving things out.

- Honeycomb's customers can have over 5,000 data fields. The assistant is shown only the fields that received data in the past seven days.
- Wrong or beside-the-point reference material misleads. The model tends to use what it is given.
- Tools count too. Every tool's description is read on every turn.

The test for each piece: would a capable person, new to this, need it to do this step? If not, it comes out.

## Order and layout

The model reads top to bottom, once. That makes order matter in ways it doesn't for a person who can look back.

- **Instructions come before the material they govern.** A marking guide goes ahead of the work to be marked.
- **The start and the end get the most attention.** The middle of a long prompt usually gets the least, though models differ. The most important instruction goes first and is often worth repeating last, next to the request.
- **Label the parts.** Clear headings or tags, so the model can tell instructions from material, and material from the request.
- **What never changes goes first.** Standing instructions and reference text at the front, the part that varies at the end. Makers charge less for a front part they have seen before, and a stable front is also easier to test.
- **Shape the request like the answer you want.** A model continues the kind of document it thinks it is in. A prompt laid out like a careful report gets a careful report back.

## Where the knowledge comes from

A design should say, for each thing the model has to know, which of these supplies it:

- **Written into the instructions.** For what is always true and always needed. Keep it short; this is read on every call.
- **Put in whole.** When the reference material is small, handing over all of it is often simpler than building a search step, and there is no search to get wrong.
- **Looked up at the time.** A search step finds the few pieces that bear on this request. Start with plain keyword search: it is easy to see why it found what it found. Reach for search by meaning when the user's words and the material's words don't match.
- **Loaded when a step needs it.** A page of guidance that is read only when the work reaches that point. The studio itself works this way: the lead reads two pages at the start, and everything else loads when a step asks.
- **Fetched because it must be.** A look-up the design requires before a decision. The shop on the shelf did better in a second phase that told the agent to check the real cost before quoting.

What the model learned in training is the one source not to rely on for anything that changes: prices, versions, what a tool can do today. Those get looked up.

**Examples in the prompt** are a strong lever. When what's wanted is hard to describe, a few worked examples do more than a paragraph of rules. They also pull hard: the model copies their length, tone and quirks. So they should be varied, and include a hard case.

## Three kinds of memory

**Within one run.** The conversation so far is the memory. It grows with every turn, costs more with every turn, and eventually fills. Systems cope by trimming or summarising the older part, and every summary loses something. The post-mortem on the shelf has the failure: a step meant to clear old reasoning once began clearing it on every turn, and the agent turned forgetful and repeated itself.

**Between runs.** The model starts each new session knowing nothing. The long-job harness on the shelf solves this with plain files: a list of features that all start as "failing", a progress log, and the saved work. Every session begins the same way: read the notes, start the thing, run one basic test, then pick one unfinished item. Plain files have a second virtue. A person can open them and see exactly what the system believes.

**About a person or a business, over months.** Customer records, past decisions, preferences. The shop on the shelf did better in its second phase, which gave it customer records and what each item cost, along with a newer model.

## Memory the system writes for itself

Notes a system writes and later reads back are powerful and need care.

- **It can write something wrong and later read it as fact.** Nothing in a note marks it as a guess.
- **Outside text saved into memory becomes a standing order.** An instruction hidden in a web page is a problem once. Saved into notes, it is a problem on every run.
- **It grows stale.** A note that was true in March is read in November with the same trust.

So a design says who may write to memory and what may be written, dates what is written, keeps memory where a person can read it, and never loads the system's own writing as rules. The first long-job harness tells its builder to change only the pass or fail mark on its list, never the list. A design can make that a wall instead of a request.

## Helpers see only their brief

A helper agent has its own separate memory. That is the point: it keeps the lead's memory clear, and lets several helpers work at once. It is also the risk. The helper knows only what its brief says.

- A good brief gives one bounded task, what is already known, how much effort to spend, and the form the answer should take. Anthropic found that vague one-line tasks made helpers repeat each other and miss parts of the question.
- What comes back is a short finding, not the helper's whole record.
- Two helpers can't see each other's choices. Cognition's example is two of them building halves of a game that don't match. That is why several may read and only one writes.

## A fresh start, or one long thread

A long conversation drifts, and re-reading it costs more each turn. Starting again with a short handover note fixes both, and loses whatever the note left out. Which is better is a bet that changes with the model. The first long-job harness forced fresh starts. Four months later, on a newer model, the second one took them out and ran one continuous session. Test it; don't assume.

## Look at what it actually saw

The surest check in this whole area: print the full text the model was sent, exactly as sent, and read it. Faults in how the prompt was put together show only there. A section is missing, a file came in empty, two instructions disagree, the important line sits in the middle of forty pages. None of that shows in the design. All of it shows on the page.

In an audit the same move finds causes. Go to the turn where it first went wrong and read what it had just been shown.

## Where it goes wrong

- **Everything put in, in case it helps.** Fix: the newcomer test, piece by piece.
- **The key instruction buried in the middle.** Fix: first, and again at the end.
- **Instructions and material run together.** Fix: label the parts.
- **Relying on what the model "knows"** for something that changes. Fix: look it up.
- **A summary that dropped the one thing that mattered.** Fix: say what a summary must keep.
- **Memory nobody can read.** Fix: plain files.
- **Notes the system wrote, loaded as rules.** Fix: its own writing is information only.
- **A one-line brief to a helper.** Fix: task, what is known, effort, form of the answer.
- **Nobody has read the assembled prompt.** Fix: print it and read it.

## Examples

All on the shelf. **Honeycomb's query assistant** shows a model only what it needs. **The long-job harness** keeps memory in plain files the next session reads first. **Anthropic's Research system** is helpers with separate memory and bounded briefs, and **Cognition's reply** is what happens when they can't see each other. **The Claude Code post-mortem** is memory cleared by mistake. **Project Vend** is records and a required look-up doing what recall couldn't.

## What a strong system designer would notice

- A prompt nobody has printed and read whole.
- Reference material included "for context" with no stated use.
- The one rule that matters, halfway down.
- A fact that changes monthly, left to the model's training.
- Memory kept somewhere a person can't open.
- No rule about what the system may write into its own notes.
- A helper sent off with one sentence.
- No answer to "what does it know at the start of a new session?"

## More details

- Figures and cases come from the shelf entries in `systemcraft/research/`, which list their sources: `honeycomb-query-assistant.md`, `anthropic-long-running-harness.md` (the files, the session start, fresh starts removed, Vercel's tools), `anthropic-research-and-cognition.md` (helpers' briefs, the mismatched halves), `claude-code-april-2026-post-mortem.md`, `project-vend.md`.
- Sean's words on the long-job harness are on its shelf entry, dated November 16, 2026.
- Fundamentals, in the studio's own words: Berryman and Ziegler's *Prompt Engineering for LLMs* (how a model reads a prompt, what to put in and in what order, and choosing reference material) and Chip Huyen's *AI Engineering* (the chapters on prompts and on retrieval, including printing the assembled prompt and starting with keyword search).
