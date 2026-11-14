# screenplain.

screenplain is a small command-line tool that turns a Fountain file into a screenplay PDF, a web page (HTML) or a Final Draft file (FDX). Fountain is the plain-text way of writing a screenplay: an ordinary text file that an app formats into proper pages. In Scriptcraft it's the agent's quick PDF, made with one command through uv (a tool that fetches and runs Python programs) so a draft can be looked at as pages without opening an app. Anything Sean reads or sends goes through Beat's own export instead. Facts below were checked against screenplain's GitHub repo, its PyPI page, its source code and test runs on this Mac on November 14, 2026.

## What it's best at.

- **A fast, honest look at a draft as pages.** One command, under a second once the tool is cached, and the PDF is on US Letter in Courier Prime, a screenplay typeface bundled with it.
- **Most of Fountain, done right.** Title page, scene headings with scene numbers, action, characters, parentheticals, dialogue, side-by-side dual dialogue, transitions, centered lines, page breaks, and italic, bold and underline. Notes and cut material stay out of the PDF.
- **Unattended use.** No app, no window, no account. An agent can make a PDF and read it back as text in the same breath.

Where Beat beats it: anything that leaves the Mac, anything where the page count or page breaks matter, A4 paper, revision marks, lyrics, and a Final Draft file with a title page. Beat from the App Store has no command-line tool, so an agent can't make a Beat PDF: ask Sean for a Beat export. When in doubt, ask.

## Setup.

- **Install:** nothing. uv is at `~/.local/bin/uv`, and its one-off runner `uvx` fetches screenplain when asked. Free, MIT licence.
- **Version:** 0.12.0 (April 28, 2026), the newest release. The one before it came out in 2023.
- **No extras needed.** Some instructions say `screenplain[PDF]`, but 0.12.0 lists no extras: the PDF library, ReportLab, is a normal requirement, so plain `screenplain` makes PDFs.
- **First run downloads.** `uvx` pulls screenplain and its helpers (ReportLab, Pillow, charset-normalizer) from PyPI, the Python package index, about 7 MB, into uv's cache. Later runs reuse the cache.
- **Reading PDFs back:** `pdfinfo`, `pdftotext` and `pdftoppm` come from poppler, installed through Homebrew on this MacBook Pro (26.06.0). The Mac Mini may not have it; check with `which pdfinfo` before relying on it there.
- **The command that proves it works,** runnable from an empty folder:

```bash
printf 'INT. KITCHEN - DAY\n\nThe toaster pops.\n' > sample.fountain && ~/.local/bin/uvx screenplain==0.12.0 sample.fountain sample.pdf && pdfinfo sample.pdf | grep Pages
```

It prints `Pages: 1`. screenplain itself says nothing on success. On a fresh machine the first run also prints `Downloading reportlab (1.9MiB)`, `Downloading pillow (4.6MiB)` and `Installed 4 packages in 5ms`.

## Getting the best out of it.

- **Pin the version.** screenplain has no `--version` flag, so the pin in the command (`screenplain==0.12.0`) is the only record of what made the PDF. Without it, `uvx` takes whatever is newest.
- **Name the format by the file ending.** `.pdf`, `.html` or `.fdx` picks the format. To read from standard input or write to standard output, use `-` and `--format pdf`. Any other ending, `.docx` say, stops with an error.
- **Read the PDF back before anyone sees it.** `pdftotext -layout sample.pdf -` shows the page as spaced text, so you can see a character name sitting in the middle and dialogue indented under it. `pdftoppm -png` makes page pictures for a visual check.
- **Force what the rules can't guess.** A line becomes a scene heading only if it starts with INT, EXT, EST, INT./EXT., INT/EXT or I/E; start it with a full stop (`.OPENING MONTAGE`) to force one. A character name must be all capitals, so `McAVOY` prints as action unless written `@McAVOY`. Only lines ending in `TO:` are transitions, so `FADE OUT.` sits at the left margin as action until written `> FADE OUT.`, which moves it to the right.
- **Number scenes yourself.** `INT. KITCHEN - DAY #1#` prints 1 in both margins. screenplain never numbers scenes on its own; Beat does.
- **Keep dual dialogue short.** A caret after the second name (`TOASTER (V.O.) ^`) sets the two speeches side by side, but each column is only about 18 characters wide. "Since when do you talk?" already wraps onto two lines.
- **Use HTML to review an outline.** Fountain sections (`# Act One`) and synopses (`= the toaster refuses`) don't print in the PDF, but the HTML shows them as headings with their summaries. `--bare` gives just the script, without a full web page around it.
- **Keep fonts embedded.** The default embeds Courier Prime in the PDF, so it looks the same everywhere. `--standard-font` switches to plain Courier, which isn't embedded and depends on the reader's machine. `--strong` makes scene headings bold and underlined.
- **A blank line inside a note needs two spaces.** That's Fountain's own rule: a note (`[[...]]`) broken by a truly empty line prints in full, brackets and all. A line of two spaces keeps it hidden.
- **Beat files work, mostly.** In a file saved by Beat, its colors and markers are notes and stay hidden, and so do the alternative takes and the settings line at the end of the file. Two things leak: a shot line (`!!CLOSE ON the toaster.`) prints as `!CLOSE ON the toaster.`, and a macro (`{{serial}}`) prints as raw text, braces included.
- **Don't count pages from it.** screenplain's page count runs long whenever speeches are long (see below). For a page count, ask Sean for Beat's PDF; for timing, use the words-a-minute rule from the tool list and the table read.

## Where it goes wrong.

- **No (MORE) or (CONT'D) on a split speech.** Proper format breaks a long speech at the page bottom with (MORE), then repeats the name with (CONT'D). screenplain moves a speech that would fit on one page to the next page whole, leaving a gap. In a test with an 18-line speech in every scene, pages ran about two-thirds full: 12 pages where tight packing needs about 8. A speech longer than a page jumps to a fresh page, then splits mid-sentence with no marker.
- **Lyrics print with the tilde.** `~Happy birthday~` comes out as action, tildes included.
- **Some titles push the title page onto two pages.** A 30-character title sent the draft date and contact onto a page of their own (4 pages instead of 3); a 35-character title was fine. The project's issue list says 28 to 30 characters. Check that page 2 is the script.
- **A synopsis needs a heading above it.** `= orphan synopsis` placed after action, with no scene heading or section right above it, printed as action, equals sign and all.
- **US Letter only.** No A4 option. No revision marks, watermark or page header.
- **The FDX is thin.** It has no title page and no scene numbers, and it drops page breaks. Fine for opening in Final Draft, not for handing to anyone who uses Final Draft.
- **The HTML is plainer than the PDF.** No title page, no page numbers, and the browser tab just says "Screenplay".
- **Other alphabets.** The issue list says Chinese, Japanese and Korean aren't handled properly (not tested). Curly quotes, dashes and accents worked.

When any of these matter, ask Sean for a Beat export. Beat's source shows a paper-size choice of A4 or Letter and a (MORE) line for split dialogue, plus an automatic (CONT'D) setting, and its site says revisions are highlighted in exported PDFs.

## Safety.

- **What goes up:** nothing. screenplain runs on the Mac. The only network use is `uvx` downloading packages from PyPI on first run. Don't use the online version on screenplain.com, which would mean uploading a script.
- **What it spends:** nothing. Free, and the cache is a few megabytes in your home folder.
- **What the PDF carries:** the title page's Title and Author go into the PDF's file details too, and the Contact line prints on the page. Check both before a file goes anywhere.
- **Ask Sean first** before sending a screenplain PDF to anyone. For anything that goes out, Beat's export is the pick.

## More details.

- Sources checked November 14, 2026: the GitHub repo and README (https://github.com/vilcans/screenplain), its open issues (https://github.com/vilcans/screenplain/issues), the PyPI page (https://pypi.org/project/screenplain/), and the 0.12.0 source in uv's cache (`parsers/fountain.py`, `export/pdf.py`, `export/html.py`, `export/fdx.py`).
- Tested on this Mac with uv 0.10.2 and screenplain 0.12.0 (ReportLab 5.1.0, Pillow 13.0.0): the proof command, a made-up sample using every element listed above (3 pages), long speeches, edge cases, two title lengths, HTML, FDX, every flag, and Beat markup (marker and color notes, a settings comment, an alternatives block, a shot line, a macro).
- Page layout, measured from the PDF: US Letter, 55 lines a page, 12-point type, a 1.5-inch left margin and a 1-inch top. From the left edge, character names start at 3.4 inches, dialogue at 2.4 inches (running to 6 inches) and parentheticals at 2.8 inches. Page numbers sit top right from page 2, and the title page has none.
- Beat facts were read in Beat's GitHub source (https://github.com/lmparppei/Beat) and site (https://www.beat-app.fi/), not tested. Beat 2.2.12 is installed; its source has a command-line tool with a paper-size option, but none was found inside the installed app.
- Not verified: whether screenplain's page breaks match Beat's or Final Draft's on a real script, and the industry figures for where character names, dialogue and parentheticals should sit.
