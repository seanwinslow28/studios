# Table reads with Kokoro.

A table read is hearing a script read aloud, one voice per character. Scriptcraft does it with Kokoro, a small, free text-to-speech model that runs on the Mac with no account. The same audio is the timing check. Facts were checked against Kokoro's model card and code, and by rendering a made-up scene on Sean's MacBook Pro, on November 14, 2026.

## What it's best at.

- **Hearing the script, free and private.** Nothing leaves the Mac, so a draft can be read as often as it changes.
- **Telling characters apart.** 54 voices in eight languages (English has both American and British voices), so each character gets their own sound.
- **Timing.** Every line is its own audio file with a measurable length. The same line, voice and speed always gives the same audio (tested), so a change in length is a change in the script.

Where another tool beats it: Kokoro can't act. With no emotion setting, it shows rhythm and length, not performance. ElevenLabs reads with feeling but costs credits and uploads the script; choices.md keeps it as a question for Sean. Sean reading a line himself is still the best test of a joke.

## Setup.

- **What's on the Mac already.** HyperFrames, a video tool whose `tts` command wraps Kokoro, keeps the model files in `~/.cache/hyperframes/tts/`: `models/kokoro-v1.0.onnx` and `voices/voices-v1.0.bin`. A Python environment with `kokoro-onnx` 0.5.0 (a lighter repackaging of Kokoro) is needed to run them; on Sean's Macs that's the narrator agent's environment. Set `KOKORO_PYTHON` to that environment's `python` once, in the shell profile. ffmpeg and ffprobe come from Homebrew; macOS's own `afplay` plays the result.
- **What it costs.** Nothing. The model is Apache 2.0 and kokoro-onnx is MIT.
- **The catch.** `hyperframes tts` fails on its own with "The kokoro-onnx package is not installed"; point `HYPERFRAMES_PYTHON` at `KOKORO_PYTHON`. HyperFrames isn't installed globally, so npx runs it from npm's cache. Pin the version: plain `npx hyperframes` fetches the newest from the internet.
- **The command that proves it works,** which makes one line and prints its length:

```bash
HYPERFRAMES_PYTHON="$KOKORO_PYTHON" \
  npx hyperframes@0.9.43 tts "It's a toaster, Gran." -v am_puck -o line.wav
```

It printed `Generated 1.3s of speech`. For any file, `ffprobe -v error -show_entries format=duration -of csv=p=0 line.wav` prints the length in seconds.

## Getting the best out of it.

**The method.** The per-character script gets written on the first real job; this method was tested on a made-up two-character scene.

1. **Pull the lines from the Fountain file.** Fountain is the plain-text screenplay format: a character's name in capitals on its own line with their dialogue underneath, a parenthetical such as `(not looking up)` in round brackets under the name, and action lines as plain paragraphs. Keep each line with its speaker. Before a line is spoken, strip: parentheticals; extensions on the name such as `(V.O.)` and `(CONT'D)`; the `^` and `@` marks; notes in `[[…]]`; cut material in `/* … */`, which includes Beat's alternatives tail `/** ALTERNATIVES: … */` and its settings line; emphasis marks `*` and `_`, and lyric tildes `~`; and sections (`#`) and synopses (`=`).
2. **Render each line to its own numbered file.** Run Python with `KOKORO_PYTHON`, load the model once from the two files above (`model` and `voices` are their full paths), then render line by line:

```python
from kokoro_onnx import Kokoro; import soundfile as sf
k = Kokoro(model, voices)
a, sr = k.create(text, voice="bf_emma", speed=1.0, lang="en-gb")
sf.write("001_mavis.wav", a, sr)
```

   Use `lang="en-gb"` for `b` voices and `"en-us"` for `a` voices. Seven lines took under 4 seconds. `hyperframes tts` also works, one command a line, at about 2 seconds a line.
3. **Make silence to put between lines,** at Kokoro's own format (24,000 samples a second, mono):

```bash
ffmpeg -v error -y -f lavfi -i anullsrc=r=24000:cl=mono -t 0.4 -c:a pcm_s16le gap.wav
ffmpeg -v error -y -f lavfi -i anullsrc=r=24000:cl=mono -t 1.2 -c:a pcm_s16le hold.wav
```

4. **List the pieces in order** in `concat.txt`, one `file '001_mavis.wav'` line each, with `gap.wav` or `hold.wav` between, then join them and measure:

```bash
ffmpeg -v error -y -f concat -safe 0 -i concat.txt -c:a pcm_s16le table-read.wav
ffprobe -v error -show_entries format=duration -of csv=p=0 table-read.wav
afplay table-read.wav
```

The test scene came to `22.138667` seconds: 18.5 seconds of speech, 0.4-second gaps and one 1.2-second hold.

**Cast for contrast, then quality.** Kokoro's voice list grades each voice. The best are female American: `af_heart` (A) and `af_bella` (A-). The best British is `bf_emma` (B-). Male voices top out at C+ (`am_michael`, `am_fenrir`, `am_puck`), with `bm_george` and `bm_fable` at C. Skip the D and F voices; `am_adam` grades F+. Set characters apart by accent and by sex where you can: in the test, Mavis was `bf_emma` and Dev `am_puck`. Two men? Split them by accent, `am_puck` against `bm_george`. kokoro-onnx can also blend two voices into a new one (untested here).

**Give the narrator its own voice.** Action lines, if read at all, go to a voice no character uses; `am_michael` and `bm_george` read slowest of those measured, which suits description. A launch-film voiceover has one voice; pick from the A and B grades.

**Render line by line, never the whole script at once.** Kokoro's notes say voices may rush on long passages. A 75-word voiceover read in one go ran faster than sentence by sentence: a little in one test (214 against 198 words a minute), a lot in another (264 against 200).

**Speed.** 0.5 to 2.0, and not proportional: on one line, 0.9 added 6% and 0.8 added 25%. Use 0.9 for an unhurried narrator or voiceover; leave characters at 1.0 and get pace from the gaps.

**Pauses and holds belong in the gaps.** Punctuation barely moves the length: an ellipsis added about 0.13 seconds, and a dash can even shorten a line. Kokoro trims the silence from the start of a line, but 0.1 to 0.17 seconds stays at the end, so a real gap runs slightly longer than its gap file. The test used 0.4 seconds between lines and a 1.2-second hold before the punchline. Try a joke with and without its hold.

**Names and numbers.** Check the phonemes (Kokoro's sound spelling) first: `from kokoro_onnx.tokenizer import Tokenizer; Tokenizer().phonemize("Niamh.", "en-us")`. Niamh came out "NYE-um" and Joaquin "JOE-kwin"; respelling in the spoken text, not the script, fixes them ("Neeve", "Wahkeen"). For exact control, swap in the right sounds and pass `is_phonemes=True`. Write numbers as said: "$4.99" came out as "dollar four", a stop, "ninety nine".

**What a table read reveals.**

- **Lines that trip.** A line that sounds tangled even in a flat machine read will be harder for an actor. Look again at any line over about 20 words.
- **Jokes that need a beat.** If the laugh line lands on top of the setup, add a hold. If the hold makes it worse, the joke may be in the wrong place.
- **Characters who sound alike,** and **a script that runs long** (timing, next).

## Timing against the clock.

The rules of thumb in choices.md: about 150 words a minute for a voiceover (roughly 35 words for 15 seconds, 75 for 30), and about 40 seconds an animated page.

**Kokoro reads faster than a person.** On a 75-word voiceover at speed 1.0, read sentence by sentence, the voices spoke at 171 to 205 words a minute; with a 0.35-second pause between sentences, 153 to 179, so a 30-second script came in at 25 to 29 seconds. So:

- **Count first.** Words divided by 150 is the target length.
- **Then read, with pauses between sentences.** If that read is already at or over the slot, the script is long; a person will be slower still. If it's 10 to 15% under, it's about right. A read without pauses comes in 12 to 27% under, so don't judge by that one.
- **For a closer match,** read at 0.9 with a pause between sentences: `am_michael` came out at 147 words a minute and `bm_george` at 142.

**For an animated short,** the dialogue time is solid, but action read aloud isn't screen time: "The toaster pops. Two slices, perfectly golden." took 3.5 seconds to read and could be a one-second gag or a four-second hold. Time the dialogue-only read, add a guess for each action beat, and check the total against the page count times 40 seconds. Count pages from Beat's PDF, not screenplain's: a check on November 14 found screenplain's count running about 50% long.

## Where it goes wrong.

- **Names in capitals get spelled out.** Screenwriters capitalise a character's name the first time they appear (a habit, not a Fountain rule); Kokoro turned "DEV" into the letters "D-E-V". Put names into normal case before speaking action lines.
- **The pronunciation trick from Kokoro's main project doesn't work here.** Its `[word](/sounds/)` spelling belongs to the official Python package; kokoro-onnx, which HyperFrames and the narrator use, reads the slashes aloud. Respell or use phonemes instead.
- **Abbreviations add a stop.** "Dr. Pell" phonemized as "Doctor. Pell", with a full stop in the middle. Write "Doctor Pell".
- **Short lines are weaker,** Kokoro's notes say. Listen to every "No." and "What?".
- **The same take every time.** A bad read won't fix itself on a second render. Change the wording, the speed or the voice.

## Safety.

Kokoro runs entirely on the Mac, uploads nothing and spends nothing. Nothing downloads once npm's cache holds hyperframes 0.9.43 and the model files are in place; otherwise the first run fetches them (a fresh Mac Mini will). Table-read audio contains the script, so keep it in a scratch folder or Sean's private files, never in this public repo. The voices are synthetic; never try to imitate a real person's voice. Ask Sean before installing anything new, including a fresh kokoro-onnx, or before changing the narrator's environment, which other jobs rely on.

## More details.

- Tested November 14, 2026: the proof command, the method on a made-up scene (kokoro-onnx 0.5.0, model v1.0), speed, punctuation, pace, repeatability and phonemes. Nothing was listened to: voice quality comes from the official grades, pronunciation from phonemes and length.
- Kokoro model card (82 million parameters, Apache 2.0, v1.0 of January 27, 2025, 8 languages and 54 voices): https://huggingface.co/hexgrad/Kokoro-82M
- Voice list and grades, and the note on short and long passages: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
- The official Python package (`kokoro` 0.9.4, with the `[word](/sounds/)` syntax): https://github.com/hexgrad/kokoro and https://pypi.org/project/kokoro/
- kokoro-onnx (MIT; its podcast, blending and phoneme examples): https://github.com/thewh1teagle/kokoro-onnx. The newest is 0.6.1 (August 19, 2026); the narrator's environment pins below 0.6. What changed in 0.6 wasn't checked.
- `hyperframes tts --help` on 0.9.43; 0.9.45 is the newest on npm. Not tested: voice blending, overlapping lines.
