# Source and version contract — every shot reproducible and revisable

How every version Motioncraft makes is named, kept, described, frozen, backed up and proved revisable, and what the finished film is delivered as. It answers SWCB #165 (*what source and delivery contract makes every shot reproducible and revisable?*), sized to a fifteen-second film. Written on the Motioncraft build map's **Source and version contract** ticket (2026-10-18). The folder and version naming come from the layout ruling (SWCB #186, sections 2–6), copied here so a seat reads one file. The delivery targets and the TC5 rule are Sean's rulings of 2026-10-18. The font shelf (§ 10) and the Fonts table are Sean's type ruling (SWCB #244, 2026-10-21), written in on SWCB #254.

Every seat that saves a version follows sections 1–6. Finishing, the accountable integrator, reads every manifest at TC5 and TC6 and fails the film on any gap. Nothing here approves artistry: a version passing every rule below is reproducible, not good.

## 1. Folders and version ids

The studio's media folder is named `media` on every machine (the trace kit's per-machine named folders); records write `media:<path inside it>`, never an absolute path.

```
media:<film>/<project>-<YYYY-MM-DD>/        # the project folder: named for the project and the date it was created
├── inputs/       # copied forward from earlier folders, original checksums kept
├── story/        # animatic-v01-<date>/ …
├── appearance/   # appearance-v01-<date>/ …
├── motion/       # motion-v01-<date>/ (its evidence pack inside)
├── finish/       # finish-v01-<date>/ …
└── approved/     # locked copies, named for the version approved
```

- mc-eng-001's project is **idea-seed**: `media:Question-Becomes-a-World/idea-seed-2026-10-17/`, and the ledger folder `engagements/idea-seed-2026-10-17/`. The film's older `Planning/` and `Tests/` folders are never edited.
- **The version id is the version folder's name**, `<artifact>-vNN-<YYYY-MM-DD>`, the date it was created. Never renamed, never reused. Every record cites that exact name with its `media:` path and sha256.
- **Every change is a new version folder.** A seat copies the prior version forward and changes the copy; nothing in a saved version is overwritten (rule 5 of [`motioncraft/CLAUDE.md`](../CLAUDE.md)).
- **Inside a version folder every path is relative.** Native projects point at their assets inside the same folder, so the folder can move, be restored or be copied forward without relinking.

## 2. What every version folder holds

| File | Written | What it is |
|---|---|---|
| `pointer.txt` | at creation, never edited | one line: the engagement id and its ledger folder, e.g. `mc-eng-001 · ledger: engagements/idea-seed-2026-10-17/` |
| `manifest.md` | by the seat that made the version, before freezing | the version's parts list, section 3 |
| `sources/` | | the native authoring files: Blender `.blend`, the Resolve project export `.drp`, Krita `.kra`, painted layers, composition HTML and scripts |
| `assets/` | | everything a source depends on: painted layers, textures, audio stems, and the font files the version sets, copied from the shelf with their licence text (§ 10) |
| `renders/` | | what the sources render: frame sequences, clips, stills |
| `evidence/` | | the evidence pack (adjacent frames, full-speed playback, burned-in frame numbers) and command output |
| `checksums.sha256` | last, when the version is finished | `shasum -a 256` of every other file in the folder, in the form `shasum -a 256 -c` reads |

A version with a render and no native source for it is incomplete, with one exception: **a generated image is its own master.** An image from the Codex imagegen path cannot be made again identically, so the downloaded file is the source, its generation record (prompt, input images by sha256, the model as the run reported it, date) sits beside it, and it is never deleted (never-do 13).

**An imported render never replaces its authoring source** (SWCB #159, check 5). When one application's render goes into another (a Blender render into Resolve, a painted layer into Blender), the receiving version lists it under dependencies with the id of the version that made it, and that version keeps its own native source. Revising the imported picture means revising its source in a new version of that source, never painting over the render.

## 3. The manifest

One per version folder, written by the seat that made it, in the same pass. Every drafting task names it as a required output, and the launcher refuses a pass that leaves a version without it, or without the pointer or the checksums ([the launcher README](../launcher/README.md#the-launch), SWCB #249). A seat on Codex writes it into its version folder like any other file; it never writes into the ledger. The ledger cites the version (path and folder sha256), which covers the manifest.

```markdown
---
version: motion-vNN-<YYYY-MM-DD>
version_path: "media:<film>/<project>-<YYYY-MM-DD>/motion/motion-vNN-<YYYY-MM-DD>"
engagement: mc-eng-001
artifact: mc-eng-001.motion
seat: animator                     # the one named operator of every application below
machine: <laptop | mini>
created: <YYYY-MM-DD>
prior_version: <version id> | none
---

## Shots

| Shot | Frames | Count | Rate | Native source | Renders to |
|---|---|---|---|---|---|
| SH<n> | <first>–<last> | <n> | 24 | `sources/<file>` | `renders/<file or sequence pattern>` |

## Files

| Path | Role | Made by (application and exact version, or model as reported) | From | sha256 |
|---|---|---|---|---|
| `sources/<file>` | native source | Blender 4.x.y | — | |
| `renders/<file>` | render | Blender 4.x.y | `sources/<file>` | |
| `assets/<file>` | dependency | <tool>, or generated | <version id it came from, or its generation record> | |

Roles: native source, dependency, render, generated master, generation record, evidence, record.

## Dependencies outside this folder

Plugins, add-ons, brushes, LUTs or anything else the source needs that is not in the folder, with name and exact version. `none` is the goal.

## Fonts

| Font | Version | File | sha256 | Licence | Licence text kept at | Licence sha256 | From the shelf |
|---|---|---|---|---|---|---|---|
| <family, size cut and style> | <version> | `assets/fonts/<file>` | | SIL OFL 1.1 | `assets/fonts/<family>-<version>-LICENSE.md` | | `media:fonts/<family>-<version>/<path to the file>` |

One row per font file the version sets. Both sha256 values must match the shelf family's `checksums.sha256`. `none` when no text is set. **A technical fail at TC5:** a font not on the shelf, a file or licence whose sha256 differs from the shelf's, a font missing from `assets/`, an Apple system font (SF Pro and New York above all), or an Adobe Fonts face.

## Settings

- Canvas: <width>×<height>, square pixels.
- Rate: 24 fps, or the source's rate on an exercise (§ 7).
- Colour: Rec.709, gamma 2.4 for video; sRGB for stills. A still with no embedded profile is read as sRGB, and the manifest says so.
- Audio: 48 kHz, 24-bit, stereo, or `no audio`.
- Render or export: codec, container, bit depth, alpha, and the exact command or render settings used.

## Reopen and render

Numbered steps a fresh session follows to open the native source and render it again, with the command it runs. Any step that needs the screen (a dialog, a UI save) is named here.

## Known failures

What went wrong while making this version and what recovered it, or `none`.
```

## 4. Saving, freezing and the approved copy

- **A save counts only when it is checked.** A scripted save is read by its return value; an application that reports none or false did not save. A UI save is checked by the project's edited state clearing. In October's Fusion tests, three scripted saves in a row returned nothing while a transient dialog was blocking the application; dismissing it made the same save succeed. So on a failed save: look at the screen, dismiss any blocking dialog, run the same save once more, and record it under Known failures. A third repeat of one failure is the #158 checkpoint: stop and go to Sean (`"Blocked: budget"`).
- **The save, reopen and render test runs on a clean project** holding only the shot, never the exploratory project it was developed in. October's exploratory project crashed on reopen while a clean project holding only the final sample passed twice.
- **Resolve keeps a portable copy.** Every Resolve version exports its project (`.drp`) into `sources/`, so the version does not depend on Resolve's own project database. Fusion is closed for every seat (2026-10-19), so no `.comp` is made; one would be saved beside the `.drp` only once a Fusion slice opens on its own ticket.
- **Freezing.** When a version is finished: write `checksums.sha256` last, then make the folder read-only (`chmod -R a-w <folder>`), then take its folder sha256 with the trace kit. Read-only also keeps the Finder from adding `.DS_Store`, which would change the folder's hash. A frozen version is never unfrozen; a change is a new version. **The launcher does this for every version a pass makes** (SWCB #258): when the pass ends, each whole version (the three files there, `checksums.sha256` verifying and covering every other file, no link inside) is made read-only, files and folders, and its record line in `pass-NN.launch.json` says `locked`; one that is not whole is refused (`version refused`, exit 5), left as it is and never locked, and goes back to its seat ([the launcher README](../launcher/README.md#freezing-versions)). A version made outside a pass, or left over from before the launcher locked, is locked by hand with `python3 motioncraft/launcher/freeze.py lock <media:project> --version <stage>/<version-id>`, which locks only a folder whose checksums verify.
- **The approved copy.** When Sean approves a version, the exact files he saw are copied to `approved/<version-id>/` and made read-only with `freeze.py lock`, never trusted from the copy: a copy made with `cp -R` keeps each file's read-only bits and gets fresh writable folders, which is how the first film's approved copies came to hold 49 writable folders between them (mc-eng-001 d17, mc-self-001 SC9). His approvals entry records that folder's path and sha256. At Close, `freeze.py sweep <media:project>` reads every version folder in the project by its mode bits, superseded versions and approved copies alike, and must exit 0. Approved copies count against the 10 GB limit. Versions approved before this contract (the October opening treatment and appearance frame) stay where they are, in place, never edited; their manifests sit in the ledger, under `references/`, because their folders cannot take a new file.

## 5. Backup, restore and relink

- **Backup:** Google Drive mirrors the studio folder `~/Movies/Animation-Studio/` (SWCB #186, sections 9–10). Drive keeps old versions only for a while, so the never-overwrite rule, not Drive's history, is what keeps every version.
- **Restoring a version:** copy the folder from Drive to a scratch location, run `shasum -a 256 -c checksums.sha256` inside it (every line `OK`), check its folder sha256 against the record that cites it, then follow the manifest's Reopen and render steps. The restore test before mc-eng-001 opens (Sean's task on the map) does this once for a whole folder.
- **Relinking after a move:** a moved studio folder changes one line in the machine's named-folder settings, and every `media:` path resolves again. Inside a version nothing needs relinking, because its paths are relative (§ 1). If an application still reports missing media, relink it to the same file inside the version folder (Blender: make paths relative, then report missing files; Resolve: relink the clip to the version folder), save it as a new version, and record the relink under Known failures. A relink never points at another version's files or at a render in place of a source.

## 6. What proves a shot can be revised without rebuilding

**The revision drill.** A fresh session, given only the version's manifest and one named change (a timing, a pose, a colour), with no chat history:

1. copies the version forward to a new version folder;
2. opens the native source by the manifest's Reopen and render steps, never a render;
3. makes the change, saves it (checked, § 4), and renders;
4. compares the new render with the prior one by the TC5 method below.

It passes when the change is in the native source, the frames the change should touch differ, and **every other frame matches exactly**. A revision that could only be made by painting over a render, or that changes frames outside its reach, fails. The motion gate's directed revision is this drill on the real film; E3's and E6's directed revisions are its first runs.

## 7. TC5: save, reopen and render again

The project is saved, closed, reopened in a fresh session and rendered again, and the two renders are compared frame by frame. **Any frame that differs is a technical fail until its cause is found, however small the difference** (Sean's ruling, 2026-10-18). The record gives the count of differing frames and the largest difference; Sean may set a tolerance later, and until he does there is none.

October's record is mixed, which is why the rule is strict: a clean one-sample project rendered identical pixels twice, but the two longer Fusion studies differed after reopening, with sampled average differences of up to about 2.1 levels out of 255, and a repeat render differed too. The cause was never found.

Count of differing frames, from decoded RGB (each render's per-frame checksums, compared):

~~~
ffmpeg -v error -i <render A> -pix_fmt rgb24 -f framemd5 a.md5
ffmpeg -v error -i <render B> -pix_fmt rgb24 -f framemd5 b.md5
paste -d' ' <(grep -v '^#' a.md5 | awk -F', *' '{print $2, $6}') <(grep -v '^#' b.md5 | awk -F', *' '{print $6}') \
  | awk '$2!=$3{n++; print "differs:", $1} END{print n+0, "frames differ"}'
~~~

Largest difference, in levels of 0–255 on any colour channel, per frame (the highest line is the record's figure):

~~~
ffmpeg -v error -i <render A> -i <render B> -filter_complex \
  "[0:v]format=gbrp[x];[1:v]format=gbrp[y];[x][y]blend=all_mode=difference,extractplanes=r+g+b[r][g][b];[r][g]blend=all_mode=lighten[rg];[rg][b]blend=all_mode=lighten,signalstats,metadata=print:key=lavfi.signalstats.YMAX:file=diff.txt" \
  -f null -
grep YMAX diff.txt | cut -d= -f2 | sort -n | tail -1
~~~

Both commands were checked on 2026-10-18 against a test clip with three frames changed by exactly 7 levels on one channel: they reported three frames and 7. Two renders with different frame counts are a fail before any comparison. The renders compared are the lossless renders or frame sequences from `renders/`, never the compressed web copy, whose encoder can differ from run to run.

## 8. Delivery targets

Sean's rulings of 2026-10-18. The film is delivered as two files from one finished timeline, and TC1–TC6 and the loudness record run on **each** file, because compression can change a file's peaks.

| | Master | Web copy |
|---|---|---|
| Use | the reference copy, kept; every later copy is made from it | for sharing and posting |
| Container and codec | QuickTime `.mov`, Apple ProRes 422 HQ, 10-bit 4:2:2 | MP4, H.264 High, 8-bit 4:2:0, `+faststart` |
| Picture | 1920×1080, square pixels, 24 fps constant, progressive | the same |
| Colour tags | Rec.709 primaries, transfer and matrix | the same |
| Audio | PCM, 48 kHz, 24-bit, stereo | AAC-LC, 48 kHz, stereo, 320 kb/s |
| Loudness | −23 LUFS integrated; short-term highest at most −18 LUFS; true peak at most −1 dBTP; set by hand, never `loudnorm`'s defaults; no loudness-range figure under a minute | the same, measured on the web copy itself |

Duration is the approved animatic's, to the frame: the frame count in `ffprobe` matches the scene record and the animatic, or TC6 fails. The delivery package's `delivery:` header line names both files in these terms.

**Exercises keep their source's settings.** E3 and E6 are tests of the train, not the film: they deliver at the rate, size and length of the source they were given (October's material is 30 fps at 1280×720), and their TC6 checks against that source. Only mc-eng-001 and later films deliver to the targets above.

## 9. The check record, from this contract

| Check | What this contract gives it |
|---|---|
| TC1, TC2 | the delivered files of § 8 |
| TC4 and the loudness record | the audio targets of § 8, measured on each file |
| TC5 | every manifest in the delivery's chain (§ 3) with nothing missing; the save, reopen and render comparison of § 7 on the finished timeline; every font in every Fonts table from the shelf, its file and licence matching the shelf's sha256 (§ 10) |
| TC6 | the targets of § 8, read from `ffprobe` on each file |

A manifest that is missing, or a file in a version that is not in its `checksums.sha256`, fails TC5.

**A card's edges** (alpha and halo, under TC2) are judged on a 4:4:4 comparison render (ProRes 4444) from the same timeline, labelled not a delivery, against an `ffmpeg` composite of the same card over the same plate, with tolerances written before measuring. The 4:2:2 master's result is recorded beside it as the format's, never hidden, since 4:2:2 shares colour between neighbouring pixels and fails any tight edge tolerance whatever the compositor does. Sean's ruling on E8 (SWCB #256, 2026-10-21, ledger mc-e8.d02).

**A card's fade** is in the card's own frames, never in the project. Resolve 21.1.1's fader (`SetFades`) is lost on save and reload, so a faded card failed TC5 on every fade frame (mc-e8.d01). Finishing bakes the fade with `ffmpeg` from a filter file saved in the version's `sources/` (SWCB #262). How its frames count is Sean's ruling (2026-10-22, SWCB #262): **a fade of N frames is N frames of partial card**, the fade-in's frame k (k = 1…N) at opacity k/(N+1) and the fade-out its mirror, so a card is fade-in, hold and fade-out frames long and the hold at full is exactly the animatic's. TC3 reads it in the master: the frames that differ from the picture under the card are exactly the card's frames, and the card's opacity, read at a point inside it as `(rendered − under) / (card − under)`, is k/(N+1) on the fade frames and 1 on the hold.

## 10. The font shelf

Every font a film sets comes from one shelf in the studio's media folder, so a version never depends on what is installed on a machine. Sean's type ruling (SWCB #244, 2026-10-21) is why: Apple's system fonts are licensed for display on the Mac and SF Pro and New York are barred from artwork; Adobe's terms forbid embedding the files and end use when the subscription lapses; only open-licence fonts allow the file to be copied into a project, packed into a `.blend` and moved between machines, with video and commercial use allowed.

```
media:fonts/
├── README.md                       # the shelf index: one line per family, its licence, when it was fetched, its ledger record
└── <family>-<version>/             # e.g. source-serif-4.005/
    ├── <the release's font files>  # unchanged, in the release's own folders
    ├── LICENSE.md                  # the licence text as released
    ├── SOURCE.md                   # source URL, release, the download's sha256, designer and foundry, Sean's yes
    └── checksums.sha256            # every other file, in the form shasum -a 256 -c reads
```

- **Open-licence only.** A family on the shelf is under the SIL Open Font License. A font under any other licence is a purchase: a separate yes from Sean, per font, and its licence must name video use and online distribution in writing before it is shelved.
- **Fetched in a live session.** Seats have no network, so a family is downloaded only in a live session Sean drives, each download with his yes, and recorded in the ledger's `setup/` with the download's sha256.
- **Read-only.** A family folder is frozen like a version (§ 4): `checksums.sha256` written last, then `chmod -R a-w`. A newer release is a new folder beside it, never a change to it.
- **Backed up with the studio folder.** The shelf sits inside `~/Movies/Animation-Studio/`, so Drive mirrors it (§ 5). Each machine keeps its own copy, matched file for file by `checksums.sha256`.
- **Copied into the version.** A version that sets text copies each font file it uses, and the family's `LICENSE.md`, from the shelf into its own `assets/fonts/`, and lists each in its manifest's Fonts table with both sha256 values and the shelf path it came from (§ 3). The version then stays self-contained: it opens and renders with no shelf and no installed font. The licence copy is named `<family>-<version>-LICENSE.md`, so two families' licences can sit side by side.

The shelf as it stands is listed in its own `README.md`; the first family, Source Serif 4, was fetched on 2026-10-21 (ledger mc-setup-017).
