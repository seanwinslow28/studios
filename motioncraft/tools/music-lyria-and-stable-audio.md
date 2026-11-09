# Music with Lyria, and Stable Audio 3 as an offline backup.

Lyria, Google's music model, is Motioncraft's pick for music. Stable Audio 3's free version, which runs on the Mac, is an optional offline backup for sound effects. Facts below were checked against Google's and Stability AI's own pages on November 8, 2026. Where a fact could not be confirmed, this guide says so.

## Lyria.

### What it's best at.

- **Score that follows a film's shape.** Lyria takes a written brief with instruments, tempo, key, mood and structure, and can be told when sections and instruments come in by timestamp. That suits a film whose music must turn where the picture turns.
- **Two models.** `lyria-3-clip-preview` makes a 30-second clip, good for loops, stings and trying ideas. `lyria-3.5` makes a full piece of about two minutes, its length steerable through the prompt. Both give 44.1 kHz stereo; MP3 by default, and Lyria 3.5 can also return WAV.
- **Images as inspiration.** A request can include up to ten images. Feeding it the film's own style frames is a quick way to get a first direction that feels of a piece with the picture.

Where another tool wins: Lyria makes a whole piece in one go and cannot edit a clip it made, so exact hit points (a beat landing on a single frame) are finished in Resolve by cutting and arranging takes. For a film with no voice, like The Line's Freeview Play film, the music carries the emotion, so the time goes into choosing and cutting the score, not into one perfect generation. ElevenLabs Music, which sets section lengths by plan, is a fallback if Lyria cannot hold a structure.

### Setup.

- **The account.** Lyria runs on the Gemini API's paid tier, billed per piece. There is no free tier for the Lyria models. As of the date above: `lyria-3-clip-preview` costs $0.04 a clip and `lyria-3.5` $0.08 a song.
- **The key.** The Gemini API key lives in the machine's audio keys file, `~/.config/audio-keys/keys.env` (check the variable's name there). Source it into the one command that needs it, send it in the `x-goog-api-key` header, and never print it or put it in a web address.
- **The call.** `POST https://generativelanguage.googleapis.com/v1beta/interactions` with the header `Api-Revision: 2026-05-20`, a body naming the model and the prompt, and the audio read from the answer's steps. The answer can carry text beside the audio, such as lyrics or a section map.
- **The proof it works.** A clip with a one-line instrumental prompt, at $0.04, that comes back as playable audio. Ask Sean before even this first paid call on a new job.

### Getting the best out of it.

- **Draft with Clip, finish with 3.5.** Find the instrumentation and mood in 30-second clips; make the full piece once a direction is chosen.
- **Write the brief like a composer's note.** Instruments, tempo in beats a minute, key, mood and structure: "solo felt piano and soft strings, 72 bpm, D major, hesitant then hopeful; near silence at 0:57; full warm entrance at 1:30; gentle ending by 1:58."
- **Time it to the cut.** Use timestamps from the locked edit or the animatic so sections change where scenes do. Section tags such as [Intro] and [Bridge] help it hold a structure.
- **Ask for an instrumental, then check.** Lyria 3.5 can sing. Say "instrumental, no vocals" in the prompt, then listen, or run speech-to-text over it, for any sung words before a take goes in the cut.
- **Lock the style prompt.** Once Sean picks a direction, reuse that prompt word for word for every later take, changing only timings.
- **Make several and choose.** Results differ between identical calls, so three takes of a direction cost pennies and give real choice.
- **Shape it in the mix.** A half-second of silence before a big entrance can be made in the edit. Under a voice, duck the music gently, about 10 to 14 dB. Set loudness to the sound brief's target with a two-pass measurement or fixed gain, never a one-pass normaliser, which pumps.

### Where it goes wrong.

- **Vocals sneak in** even when not asked for. Always check.
- **Sections land near the cut, not on it.** Timestamps guide, they don't guarantee. Trim and arrange in the edit.
- **The stock-music sound.** A prompt of mood words gives generic library music. Name instruments, tempo, key and the moments that must change.
- **Blocked prompts.** Every prompt passes safety filters; one that names a real artist's voice or asks for copyrighted lyrics is refused. Describe the qualities of a sound instead.

### Google's terms: check before a paid job.

Sean asked for Google's terms to be checked before Lyria music goes into a paid job. What the Gemini API's additional terms said on the date above (effective March 23, 2026):

- Google claims no ownership of generated content, but may generate the same or similar content for others.
- You are responsible for how the content is used, including by anyone you share it with.
- Users must be 18 or over and follow Google's prohibited-use policy.
- On the paid tier, Google says it does not use prompts or results to improve its products; on unpaid services it does.

The terms say nothing specific about music, Lyria or commercial use of generated songs, and I found no Lyria-specific licence page. That gap is exactly why the check matters: before a paid job, read the live terms and Lyria's pages again and tell Sean what they say. Every Lyria output also carries SynthID, an inaudible watermark that marks it as AI-made.

## Stable Audio 3, free on the Mac.

### What it is, and its place.

Stable Audio 3 is Stability AI's audio model family, released May 20, 2026. Three versions have free, downloadable weights: Small SFX for sound effects, Small for music up to about two minutes, and Medium for music up to about six minutes. A Large version is sold only through Stability's paid service. Stability says the models were trained on licensed and Creative Commons audio.

Its place in Motioncraft is narrow: an optional backup for sound effects when ElevenLabs is down, the month's credits are gone, or a sound should never leave the Mac. ElevenLabs remains the first choice for effects. Never pay for Stable Audio, and never use the Large version.

### Setup.

- **No Stability account needed.** Sean made an online Stability account, but the free version doesn't use it.
- **A free Hugging Face login is needed.** The official weights (`stabilityai/stable-audio-3-small-sfx`) sit behind a gate on Hugging Face: you sign in and accept Stability's Community License, its privacy policy and Google's Gemma terms (its text encoder is built on Gemma). That is a one-time free step, separate from the Stability account.
- **The code.** Stability's repository, `github.com/Stability-AI/stable-audio-3`, installs with `uv sync`. Its default install pulls a PyTorch built for NVIDIA graphics cards, so on the Mac use the repository's Apple Silicon route under `optimized/mlx`, or the community conversion `mlx-community/stable-audio-3-small-sfx`. Medium needs Flash Attention, an NVIDIA-only part, so expect only the Small models to run here.
- **The proof it works.** The repository documents `stable-audio --model small-sfx -p "door slam with echo" --duration 3 -o test.wav`. Not yet run on Sean's Mac; whether that exact command works through the Apple Silicon route is unconfirmed.

### Getting the best out of it.

- **Concrete prompts with a set length.** Its own example pairs a plain physical description with a duration, such as a train arriving with its horn, seven seconds long. English only.
- **Make several and choose.** It is fast and free, so make five takes and pick by ear.
- **Treat it like any effect in the mix.** The same rules apply as for ElevenLabs effects: place to the frame, ride the level against the mix.
- **Editing is possible.** The family can fill in or extend part of an existing recording, useful for lengthening a short real sound.

### Where it goes wrong.

- **Setup friction.** The default install assumes an NVIDIA card. Use the Apple Silicon route from the start.
- **Unknown quality against ElevenLabs.** Untested here. Compare it on one real cue before trusting it for a job.
- **Unconfirmed limits.** The repository lists a maximum length for Small SFX of about two minutes; Stability's announcement doesn't state one. Effects are short anyway.

### Safety.

- **Never pay.** The free Small models only.
- **Download only from Stability's own repository and Hugging Face page,** or a named, well-known conversion, into its own folder.
- **The licence.** Under the Community License you own what you make. An organisation with over $1 million a year in revenue needs Stability's enterprise licence, so if a job is made for such a company, ask Sean first.
- **Nothing goes up.** After the download, it runs offline.

## More details.

- Sources checked November 8, 2026: Google's music generation guide (aistudio.google.com/docs/music-generation), the Gemini API pricing page (aistudio.google.com/docs/pricing) and additional terms (aistudio.google.com/docs/terms); Stability's research page (stability.ai/research/stable-audio-3) and announcement (stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models), the Small SFX model card on Hugging Face, and the GitHub repository.
- The exact setting for Lyria 3.5's WAV output was not shown on Google's page. Check it before the first job that needs WAV.
