"""Makes a lean job folder for a film: the media folders, a .gitignore that keeps media out of git, and the venv requirements.

Creates references/, assets/, motion-experiments/, edits/ and sound/, writes .gitignore, and copies requirements-venv.txt
from beside this script. Refuses to write into a folder that already has files.
Usage: python3 new_production.py <dest folder>
"""
import argparse
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDERS = ("references", "assets", "motion-experiments", "edits", "sound")
# Autosaving repos push untracked files, so these patterns are in place before any media lands.
GITIGNORE = """\
# Media stays local: reference films are third-party (analysis only), and renders are large.
*.mp4
*.mov
*.m4v
*.webm
*.mkv
*.wav
*.mp3
*.m4a
*.aac
*.flac
*.psd
*.kra
*.drp
*.blend
*.blend1
exports/
references/**/source/
references/**/frames/
references/**/*.jpg
references/**/*.png
references/**/*.webp
references/**/*.jpeg
references/**/*.gif
references/**/watch-run/
motion-experiments/**/*.png
motion-experiments/**/*.jpg
motion-experiments/**/renders/
motion-experiments/**/media/
edits/**/boards/
assets/**/img/
assets/**/generated/
assets/**/higgsfield/
assets/**/build/
assets/**/*.png
assets/**/*.jpg
assets/**/*.jpeg
assets/**/*.webp
# Product source must never be copied into the repo; if an export ever lands here by mistake, it stays out of git.
assets/source-export-*/
assets/*-source-*/
node_modules/
.venv/
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description="Make a lean job folder: media folders, a .gitignore and the venv requirements.")
    ap.add_argument("dest", help="a new or empty folder")
    a = ap.parse_args(argv)
    dest = Path(a.dest).expanduser().resolve()
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"{dest} already has files; choose an empty or new folder")
    for d in FOLDERS:
        (dest / d).mkdir(parents=True, exist_ok=True)
    (dest / ".gitignore").write_text(GITIGNORE)
    shutil.copy(HERE / "requirements-venv.txt", dest / "requirements-venv.txt")
    print("made", dest)
    print("next: python3 -m venv", dest / ".venv", "&&", dest / ".venv/bin/pip", "install -r", dest / "requirements-venv.txt")


if __name__ == "__main__":
    main()
