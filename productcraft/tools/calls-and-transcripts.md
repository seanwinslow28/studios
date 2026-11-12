# Calls and transcripts.

Two ways to turn a conversation into text, and one way to make sense of it. Granola takes calls Sean may record; parakeet-mlx transcribes anything sensitive on the Mac itself; the interview-summary skill plus Claude turns a transcript into findings. Read this before recording a call, transcribing audio or summarizing an interview.

## What each is best at.

- **Granola, for calls Sean is allowed to record.** It runs on the Mac, listens to the microphone and the computer's sound, and no bot joins the call. It writes notes around whatever Sean jots down during the call, and it keeps no audio once the transcript is done. Best for discovery calls with people outside the day job who've agreed to AI notes.
- **parakeet-mlx, for anything sensitive.** It turns an audio file into text using the Mac's own chip. The audio never leaves the machine. It gives a plain transcript and nothing more: no summary, no speaker names. It's the choice for day-job material that mustn't reach an outside service.
- **The summarize-interview skill plus Claude, for making sense of it.** The skill gives a fixed shape for one interview; Claude fills it from the transcript; every quote gets checked against the transcript word for word.

Where something else wins: MacWhisper Pro (about $69 once) labels who is speaking, worth asking Sean about if parakeet's unlabelled transcripts keep causing mix-ups.
## Setup.

**Granola** is installed. The free plan, called Basic, costs nothing and includes AI notes and chat, but keeps only **30 days of meeting history**. The Business plan, $14 a month, adds unlimited history, more integrations and programming access. On the free plan, Granola's connector to Claude reaches only the last 30 days of Sean's own notes, and it's waiting for Sean to sign in.

The training switch matters. Granola trains on anonymised data by default. The switch is labelled "Use my data to improve models for everyone", and lives in the desktop app under the workspace name (bottom left), then Settings, then Preferences. It covers the whole account, so turning it off once is enough. Confirm it's off before the first real call. Granola's page doesn't say whether data from before the change is removed.

**parakeet-mlx** is fetched and run through uv. Sean said yes to adding it. The command that proves it works, and fetches only the program:

```bash
uvx --from parakeet-mlx parakeet-mlx --help
```

On November 12, 2026 this fetched version 0.7.0 and printed its help cleanly. To keep it installed rather than fetched each time, the project's own instruction is `uv tool install parakeet-mlx -U`. It needs ffmpeg, which is on the Mac.

The first real transcription downloads the speech model once from Hugging Face: `parakeet-tdt-0.6b-v3`, about 2.5 GB, which handles 25 languages. Tell Sean before that download. After it, transcription runs offline.

A typical run:

```bash
parakeet-mlx interview.m4a --output-format all --output-dir <job folder>
```

The default output is a subtitle file (`.srt`), which carries timestamps. `all` also writes plain text and JSON. Keep the timestamped version: it's how a quote gets found again in the audio.

## Getting the best out of it.

**Recording.**

- **Consent comes first, every time.** Granola's own guidance puts consent on the person recording and suggests saying at the start that you're taking AI notes. For parakeet there has to be a recording, which means asking to record.
- **Jot a few words during a Granola call.** Its notes grow from what Sean types, so three rough lines ("pays for two tools", "hates Friday reconciling") steer the summary toward what he noticed. With nothing typed, the notes are generic.
- **Treat Granola's polished notes as a draft.** They're an AI's reading and can blend Sean's jottings with what was said. The transcript is the record: summarize from it, and save it to the job folder the same day, before the 30-day window closes.
- **parakeet works on files only.** For an in-person talk, the Mac's own recorder is enough. For a video call, use the call app's local recording and check where it saves: one that uploads to the cloud defeats the point of a local transcriber.
- **Good audio beats any setting:** a headset and a quiet room. For very long audio, `--local-attention` uses less memory.
- **Expect names and jargon to come out wrong.** Product names, people's names and acronyms are the usual errors. Fix them in one find-and-replace pass and note the fix before summarizing.

**Making sense of an interview.**

The skill's shape for one interview: date, who took part, their background, what they use today, what they like about it, what's wrong with it (each as a job they're trying to get done, the outcome they want, how much it matters and how satisfied they are), key insights and action items. It says to put a dash where the transcript has nothing. That's its best habit: a blank beats a guess.

What a master adds:

- **One interview at a time, soon after the call,** before reading the others. Summaries written in a batch blur people together.
- **Split what people did from what they say they'd do.** A story about last Tuesday is evidence. "I'd definitely use that" is an opinion about the future, and Rob Fitzpatrick's point in *The Mom Test* is that those are nearly worthless. Jason Cohen's bar on the shelf is the sharp version: compliments don't count, only people who say they'll pay, with a real number.
- **Every quote checked word for word.** Search the transcript for the exact words. If they aren't there, it isn't a quote: mark it as a paraphrase or cut it. Note the timestamp beside each quote. Claude tends to tidy speech, join two sentences, or produce a crisper line than anyone said; the check catches all three.
- **Counts, not adjectives.** "Three of seven described paying for a workaround" beats "users are frustrated".
- **Keep the raw transcript beside the summary,** so anyone can check it.

The difference, in a made-up example:

- **Weak:** "She said it's a great idea and she'd buy it."
- **Strong:** "Freelance bookkeeper. Spends about two hours each Friday copying receipts into a sheet [12:40]. Pays $15 a month for an app she half uses. Asked about price, she named $10, then said she'd have to think about it [31:05]. Counts as interest, not as someone who'll pay."

## Where it goes wrong.

- **The training switch left on.** It's on by default. Check it before the first call.
- **Transcripts lost to the 30-day window.** Spot it early: every past call should have a saved transcript in its job folder.
- **A day-job call recorded in Granola without checking.** Whether his employer allows Granola on work calls is Sean's to check. Until he has, day-job audio goes to parakeet.
- **Invented or tidied quotes.** The commonest failure, and the most damaging, because a crisp fake quote is exactly what gets repeated on a review page. Run the word-for-word search on every quote.
- **The wrong speaker.** parakeet doesn't label who's talking, so a line can be Sean's own question read back as the customer's answer. When a quote carries weight, listen to that moment.
- **A polite yes counted as demand.** "Sounds great" from a friendly stranger is not a sign of anything. Check the summary for future-tense promises standing in for past behaviour.

## Safety.

- **Granola uploads.** Audio goes out for transcription and is deleted afterwards; notes are stored on servers in the US. Notes are private by default, with sharing options for the company or anyone with the link. Never set a note to anyone-with-the-link without Sean's yes.
- **parakeet uploads nothing.** Its only network use is fetching the program and the one-time model download.
- **A transcript sent to Claude leaves the Mac.** parakeet keeps the audio local, but summarizing the transcript with Claude sends its text to Anthropic. For day-job material that mustn't leave, ask Sean first, or summarize with a local Ollama model instead.
- **Transcripts hold other people's words and details.** They stay in the job's folder, never in this public repo. Day-job transcripts live in Sean's private work repo.
- **Ask Sean before** recording anyone, before the first 2.5 GB model download, and before buying MacWhisper or moving to Granola's paid plan.

## More details

- Granola plans and limits (Basic $0 with 30 days of history; Business $14; training opt-out per user): https://www.granola.ai/pricing, read November 12, 2026.
- Granola training switch, its label and location: https://docs.granola.ai/help-center/consent-security-privacy/model-training
- Granola audio, storage, sharing levels, no bot, consent: https://docs.granola.ai/help-center/consent-security-privacy/security-privacy-data-faqs
- parakeet-mlx: https://github.com/senstella/parakeet-mlx. Version, flags, default model and output formats were checked against `parakeet-mlx --help` and `--version` (0.7.0) on this Mac, November 12, 2026. No transcription was run.
- Model size, languages and licence: https://huggingface.co/mlx-community/parakeet-tdt-0.6b-v3
- The skill: `~/.claude/plugins/synced/<id>/pm-product-discovery/skills/summarize-interview/SKILL.md`; the `/interview` command in the same plugin uses it for its summarize mode.
- Cohen's bar: `productcraft/research/cohen-ten-who-will-pay.md`. For how to run the conversation itself: `productcraft/expertise/talking-to-customers.md`.
- The privacy split between local and outside tools: `productcraft/tools/choices.md`.
