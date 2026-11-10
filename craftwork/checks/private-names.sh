#!/bin/sh
# Stops a commit that would put a private name in this public repo: Sean's
# employer, its products, anything on his private list. The list lives
# outside the repo, because a list in here would itself leak the names.
# It never prints a name it finds, only where it is.
#
#   private-names.sh staged          check what is staged: file paths and contents
#   private-names.sh message FILE    check a commit message
#
# The list: one name per line, lines starting with # ignored. Default
# ~/.config/devcraft/names; set STUDIOS_PRIVATE_NAMES to use another file.
# Matching ignores case; a name counts when it stands apart from letters and digits.
# Exit 0: nothing found. Exit 1: a name found, or the check couldn't run.
set -eu

list="${STUDIOS_PRIVATE_NAMES:-$HOME/.config/devcraft/names}"

if [ ! -r "$list" ]; then
  echo "The private-names check couldn't run: no list at $list." >&2
  echo "Ask Sean for it, or set STUDIOS_PRIVATE_NAMES to where it is." >&2
  exit 1
fi

patterns="$(mktemp)"
trap 'rm -f "$patterns"' EXIT
chmod 600 "$patterns"
# Each name becomes a pattern that needs the edge of the line, or a character
# that isn't a letter or digit, on each side. So "name_notes" and "name-api"
# are caught but a longer word that only contains the name isn't. A space in a
# name also matches "_" or "-", so "two words" catches "two_words". Not
# nothing at all: run together, a two-word name can match an ordinary word.
grep -v '^[[:space:]]*#' "$list" | grep -v '^[[:space:]]*$' |
  sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' \
      -e 's/[][\.*^$+?(){}|/]/\\&/g' \
      -e 's/[[:space:]]\{1,\}/[^[:alnum:]]/g' \
      -e 's/^/(^|[^[:alnum:]])/' -e 's/$/($|[^[:alnum:]])/' > "$patterns" || true
if [ ! -s "$patterns" ]; then
  echo "The private-names check couldn't run: the list at $list has no names." >&2
  exit 1
fi

found=0

case "${1:-}" in
  staged)
    files="$(git diff --cached --name-only --diff-filter=ACMR)"
    [ -n "$files" ] || exit 0

    # A path that holds a name can't be printed, so only count them.
    bad_paths="$(printf '%s\n' "$files" | grep -c -i -E -f "$patterns" || true)"
    if [ "$bad_paths" -gt 0 ]; then
      echo "A private name is in the path of $bad_paths staged file(s)." >&2
      echo "See them with: git diff --cached --name-only" >&2
      exit 1
    fi

    # Where in the staged contents: path and line number, never the text.
    # Paths go through xargs one per line, so spaces survive, and are read
    # literally, so a name like ":(exclude)x" can't dodge the scan.
    hits="$(printf '%s\n' "$files" | tr '\n' '\0' |
      xargs -0 git --literal-pathspecs grep --cached -n -I -i -E -f "$patterns" -- 2>/dev/null |
      cut -d: -f1,2 || true)"
    if [ -n "$hits" ]; then
      echo "A private name is in staged text at:" >&2
      printf '%s\n' "$hits" | sed 's/^/  /' >&2
      found=1
    fi
    ;;
  message)
    msg="${2:-}"
    if [ ! -r "$msg" ]; then
      echo "The private-names check couldn't run: no commit message file given." >&2
      exit 1
    fi
    # Check # lines too: git keeps them when the message comes from -m or -F.
    # Only the diff below the scissors line of "git commit -v" is skipped.
    lines="$(sed '/^# -* >8 -*$/,$d' "$msg" | grep -n -i -E -f "$patterns" |
      cut -d: -f1 | tr '\n' ' ' || true)"
    if [ -n "$lines" ]; then
      echo "A private name is in the commit message, line(s): $lines" >&2
      found=1
    fi
    ;;
  *)
    echo "usage: private-names.sh staged | private-names.sh message FILE" >&2
    exit 2
    ;;
esac

if [ "$found" -ne 0 ]; then
  echo "Take it out, or put a general word in its place, then commit again." >&2
  exit 1
fi
