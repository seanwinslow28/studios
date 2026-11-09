"""Builds a review page (REVIEW-<n>.html) in the job folder from a content.json.

Run from the job folder: python3 build_review.py <content.json> [<n>]
(<n> defaults to the number ending the content file's folder name, as in edits/review-7/, else 1.)
The page opens with one plain sentence and one decision, then the film, then sections, then everything else folded under "More details".
The builder refuses any heading, paragraph, list item, caption or table cell that doesn't end with punctuation (Sean listens to pages
read aloud), and any image or video that doesn't exist. Paths in content.json are relative to the job folder.

content.json:
{
  "tag": "Review 7 · film v02 · November 5, 2026.", "h1": "...", "lead": "One plain sentence: what happened and what I need from you.",
  "ask": "Lock the picture, or send notes?", "rec": "locking it.", "rec_why": "...", "alt_cost": "...",
  "video": "motion-experiments/film-v02/renders/film-v02.mp4", "video_note": "...",
  "sections": [ {"title": "...", "paragraphs": ["..."], "bullets": ["..."], "table": {"head": ["..."], "rows": [["..."]]},
                 "images": [["path.jpg", "Caption."]], "videos": [["path.mp4", "Caption."]], "pairs": [["before.jpg", "Caption.", "after.jpg", "Caption."]]} ],
  "more": [ same shape as sections ]
}
"""
import html
import json
import sys
from pathlib import Path

if sys.argv[1:2] in (["-h"], ["--help"]) or len(sys.argv) < 2:
    sys.exit(print(__doc__) or 0)
CONTENT = Path(sys.argv[1])
ROOT = Path.cwd()  # the job folder
D = json.loads(CONTENT.read_text())
TAIL = CONTENT.resolve().parent.name.split("-")[-1]
N = sys.argv[2] if len(sys.argv) > 2 else (TAIL if TAIL.isdigit() else "1")
e = html.escape
ENDS = (".", "?", "!", ":", ".)", ".”", "?”", ")")
STRINGS = []
CSS = """:root{--ink:#1F2A37;--muted:#5B6472;--line:#E5E7EB;--blue:#1A73E8;--bg:#FAFAF8;--card:#FFFFFF}
@media(prefers-color-scheme:dark){:root{--ink:#E8EAED;--muted:#A0A7B4;--line:#2E3440;--blue:#7AB0FF;--bg:#15181D;--card:#1D2127}}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{max-width:980px;margin:0 auto;padding:28px 16px 80px}h1{font-size:30px;line-height:1.2;margin:6px 0 10px}h2{margin-top:40px}
.tag{color:var(--muted);font-size:14px}.lead{font-size:18px}.ask{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px}
.muted{color:var(--muted)}video{width:100%;border-radius:10px;background:#000;margin:8px 0}figure{margin:12px 0}img{width:100%;display:block;border-radius:8px}
figcaption{margin-top:6px;font-size:13.5px;color:var(--muted)}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}
table{width:100%;border-collapse:collapse;font-size:14.5px}th,td{text-align:left;vertical-align:top;padding:8px 10px;border-top:1px solid var(--line)}.tw{overflow-x:auto}
details{margin-top:32px}summary{cursor:pointer;font-weight:600;font-size:18px}a{color:var(--blue)}
@media(max-width:640px){.pair{grid-template-columns:1fr}.tw table,.tw tbody,.tw tr,.tw td{display:block;width:100%}.tw tr:first-child{display:none}
.tw tr{padding:10px 0;border-top:1px solid var(--line)}.tw td{border:0;padding:3px 0}.tw td::before{content:attr(data-h);display:block;font-size:12px;font-weight:600;color:var(--muted)}}"""


def P(s):
    STRINGS.append(s)
    return e(s)


def need(p):
    if not (ROOT / p).exists():
        raise SystemExit("missing file: " + p)
    return p


def section(s, level="h2"):
    out = [f"<{level}>{P(s['title'])}</{level}>"]
    out += [f"<p>{P(x)}</p>" for x in s.get("paragraphs", [])]
    if s.get("bullets"):
        out.append("<ul>" + "".join(f"<li>{P(x)}</li>" for x in s["bullets"]) + "</ul>")
    if s.get("table"):
        h = s["table"]["head"]
        out.append('<div class="tw"><table><tr>' + "".join(f"<th>{P(x)}</th>" for x in h) + "</tr>" + "".join(
            "<tr>" + "".join(f'<td data-h="{e(h[i])}">{P(c)}</td>' for i, c in enumerate(r)) + "</tr>" for r in s["table"]["rows"]) + "</table></div>")
    for p, c in s.get("videos", []):
        out.append(f'<figure><video controls preload="metadata" src="{need(p)}"></video><figcaption>{P(c)}</figcaption></figure>')
    for a, ca, b, cb in s.get("pairs", []):
        out.append(f'<div class="pair"><figure><img src="{need(a)}" alt="" loading="lazy"><figcaption>{P(ca)}</figcaption></figure>'
                   f'<figure><img src="{need(b)}" alt="" loading="lazy"><figcaption>{P(cb)}</figcaption></figure></div>')
    for p, c in s.get("images", []):
        out.append(f'<figure><img src="{need(p)}" alt="" loading="lazy"><figcaption>{P(c)}</figcaption></figure>')
    return "\n".join(out)


def main():
    body = [f'<p class="tag">{P(D["tag"])}</p>', f"<h1>{P(D['h1'])}</h1>", f'<p class="lead">{P(D["lead"])}</p>',
            f'<div class="ask"><p><b>Your decision. {P(D["ask"])}</b> I recommend {P(D["rec"])} {P(D["rec_why"])}</p><p class="muted">{P(D["alt_cost"])}</p></div>']
    if D.get("video"):
        body.append(f'<video controls preload="metadata" src="{need(D["video"])}"></video><p class="muted">{P(D["video_note"])}</p>')
    body += [section(s) for s in D.get("sections", [])]
    if D.get("more"):
        body.append(f'<details><summary>{P("More details.")}</summary>' + "".join(section(s, "h3") for s in D["more"]) + "</details>")
    bad = [s[-60:] for s in STRINGS if s and not s.rstrip().endswith(ENDS)]
    if bad:
        raise SystemExit("missing end punctuation: " + repr(bad))
    out = ROOT / f"REVIEW-{N}.html"
    out.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                   f'<title>Review {N}</title><style>{CSS}</style></head><body><main>' + "\n".join(body) + "</main></body></html>")
    print("wrote", out, len(STRINGS), "strings checked")


if __name__ == "__main__":
    main()
