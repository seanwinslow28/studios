# The ChatGPT desktop opening prompt, and the capture-back

The stills walkthrough runs in ChatGPT desktop on the subscription (SWCB #267, locks 3 and 4). The room writes the opening prompt from this template, Sean pastes it, and the rounds run there; the sidecar, the meter and the brief stay in Claude's room. Before the first paste: "Improve the model for everyone" is off (mc-setup-001); the app has the project filesystem, so frames are saved by path, never attached back.

## The prompt

Fill every `<…>` from the sidecar's locks and the board; nothing in it is invented in the prompt. Keep it under a page.

```
You are running a look walkthrough for a short film, with its director (me) choosing. We are finding the DIRECTION of the look, not designing it: no style frame, no layers, no character sheet. Every round you show me three options side by side, I lean, you narrow.

THE PIECE, SO FAR
<the single objective, who feels it, where it lives, in three lines>
Subjects: <each with its design-bearing specific and what must stay recognisable>
The hero moment: <in words, from the lock; the composition we hold constant>
The signature move: <in words; its timing feel in my words>
Length / ratio: <numbers>

THE BOARD
<one line per binding row: "B1: <work> (<link>), borrowed: <what>; not borrowed: <what>">
<for rows that are my own work, the file path>
Negatives: <one line per N row: what, and what I named wrong>

WHAT THIS IS NOT
<the NOT lines>

ROUND RULES
1. One axis per round. The axes, in order, unless I change it: <medium, palette, line, shape language, staging of the hero moment>.
2. Three options per round, each a different answer on that axis and only that axis. Hold the hero moment's composition roughly constant across the three, so I compare the axis and not the framing.
3. With the three images, give me one recommendation and one question. No menus, no lists of adjectives.
4. Wait for my lean. On "narrow", render three finer options inside the lean. On "reach back to round N option X", mix that concept in. On "next axis", move on.
5. Name the style, do not describe it: one style token per prompt, drawn from the board's borrowed-whats; where a board row names a real work, look it up before drawing rather than narrating its look.
6. Save every image to "<media root>/<piece>/Planning/<slug>/look/" as round-NN-<axis>-<a|b|c>.png, and beside each a .txt holding the exact prompt that made it and the line "host: chatgpt-desktop; generated". Never overwrite a file.
7. No text, no watermark, no logo in any frame. No frame is final art.
8. Do not write the story, the beats, the boards or the timing. If a round needs a story decision, ask me the one question and stop.
```

## The capture-back ritual

Closes every round, and no new axis opens until it has:

1. **The frames are on disk** under `look/`, each with its `.txt` beside it, named as the rules say. The room lists them (`ls look/`) and reads the three `.txt` files; a missing prompt is fetched from Sean before anything else.
2. **Sean's words on the round** are pasted into Claude's room: which option, and why, in his words. The room appends the `### look:<axis> — round: n — host: chatgpt-desktop` block with the three option records (`file:`, `prompt:`), then locks `[Ln] look:<axis>: <option>, <file>` with his reason verbatim.
3. **The meter line** is unchanged (stills spend nothing) and said anyway, so the habit holds for the motion rounds.
4. **The next axis's prompt**, if the rules need a change (a reach-back, a new order), is one short paste the room writes; otherwise "next axis" suffices.

A round whose frames never reached `look/` is not a round: its lean is an open question until the files exist. Making the capture mechanical (Codex in the desktop app saving each round's images and Sean's lines by path) is an open item the first run tests; until then the ritual is by hand.
