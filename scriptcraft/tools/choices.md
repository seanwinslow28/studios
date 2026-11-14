# Scriptcraft's tool list

The tools Scriptcraft uses, one pick per kind of work, with Sean's yes or no. Scouted on November 13, 2026 for today's best. Each tool has a mastery guide in this folder: Beat, screenplain, and table reads with Kokoro.

Sean said yes to the whole free list on November 13, 2026, and installed Beat on his MacBook Pro the same day; the Mac Mini gets it next.

The short version: write every script as a plain Fountain file, open it in Beat, and keep everything else free and on the Mac. Nothing needs buying.

A few words used below: **Fountain** is the plain-text way of writing a screenplay, so a script is an ordinary text file that both Sean and an agent can edit, and an app formats it into proper screenplay pages. A **table read** is hearing the script read aloud, one voice per character.

## The list

| Kind of work | The pick | Cost | Have it? | Sean's answer |
|---|---|---|---|---|
| Writing and formatting | Beat, a free, open-source Mac app that saves plain Fountain files. Updated about monthly through October 2026. It has index cards, revision marks and alternate takes on a line. | Free | Yes on the MacBook Pro; the Mac Mini next | Yes. |
| Screenplay PDFs | Beat's own export for anything Sean reads or sends. For an agent making a quick PDF, screenplain, one command through uv. Beat's PDF needs Sean at the window: the App Store copy has no command-line tool. | Free | Yes: nothing to install, uv runs it (tested November 14, 2026) | Yes. |
| Table reads | Kokoro, the free voice already on the Mac: each line read in its own character's voice, then the lines joined with ffmpeg. The brain's narrator reads in one voice only, so the per-character read is new work. | Free, runs on the Mac | Yes, the narrator; the per-character script gets written on the first job | Yes. |
| Timing | About 150 words a minute for a voiceover (roughly 35 words for 15 seconds, 75 for 30). An animated page plays shorter than a live-action one, about 40 seconds. Checked against the table-read audio, remembering Kokoro reads faster than a person; count pages in Beat's PDF, not screenplain's, which runs long. | Free | Yes | Yes. |
| Outlining and punch-up | Plain text inside the script: Fountain sections and synopses show as cards in Beat; alternate jokes sit on the line in Beat or in Fountain notes. Drafts compared word by word with git. | Free | Yes | Yes. |

## Looked at and not picked

- **Highland Pro:** polished, from a working screenwriter's company, but $59.99 a year, and its own file format wraps the text in a zip.
- **Final Draft 13:** the industry standard, $199.99, but its files aren't plain text. Worth it only if a buyer insists on Final Draft files.
- **Fade In:** $79.95 once, with a built-in table read, but its own file format.
- **JumpCut:** a new command-line PDF maker that aims to match Final Draft's page breaks and can write Final Draft files. Free, but it needs the Rust toolchain installed, and almost nobody uses it yet. Worth a test only if Final Draft files are ever needed.
- **ElevenLabs and Table Read Studio** for table reads: better voices, but paid and the script is uploaded. Asked about only if Kokoro's voices fall short on a real job.
- **Slugline 2, WriterDuet, Arc Studio:** possibly dormant, or not plain text, or cloud-only.

## More details

- One catch with Beat: it keeps revision marks, tags and review notes in a hidden block on the file's last line, placed by character count, so an agent's edit above a mark moves the words but not the mark. Turning revision tracking off stops new marks but doesn't fix old ones. Before an agent edits, the script is closed in Beat and that block checked; if it holds marks, Sean clears or commits them first. Git keeps the history.
- Checked November 14, 2026: Beat's App Store copy has no command-line tool (its source builds one only for the direct download, untested). Not checked yet: whether JumpCut's page breaks really match Final Draft.
- Sources: Beat's site, GitHub and App Store page; screenplain and JumpCut on GitHub and PyPI; vendor pricing pages for Highland Pro, Final Draft, Fade In and Arc Studio; voiceover timing from Voice123 and Voice Bros; Kokoro's model card, voice list and the kokoro-onnx project; animation page timing from writers on John August's site (rough).

## Books

Sean said yes to the first five on November 13, 2026, then had them researched properly the same day, after the first list was found to be checked too lightly. He said yes to this final five, and buys them himself as ebooks into `~/Books/screencraft/`, outside every repo. The lead turns each into private notes in `scriptcraft/library/books/`. The research, with runners-up, store links and prices, is in `books-research.md` in this folder.

| Book | What it teaches Scriptcraft |
|---|---|
| The Upright Citizens Brigade Comedy Improvisation Manual (Besser, Roberts and Walsh, second edition, 2023) | "The game": find the first unusual thing, then heighten it. The basis of most modern sketch writing. Kindle only, as page pictures. |
| The Hidden Tools of Comedy (Steve Kaplan, 2013) | Why a comic scene works: characters who keep trying and keep losing. |
| Into the Woods (John Yorke, 2013) | Story structure at any length: one shape that repeats in every scene, so it holds for a two-minute short as well as a feature. |
| Joke Farming (Elliott Kalan, 2025) | A step-by-step way to build a joke and punch it up, from premise and structure to the final wording. |
| Hey Whipple, Squeeze This (Luke Sullivan, sixth edition, 2022) | Writing ads, for launch-film voiceovers: the idea, short copy and the video spot. |

Borrowed from Motioncraft: Liz Blazer's Animated Storytelling, for writing for animation.
