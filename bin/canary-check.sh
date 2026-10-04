#!/usr/bin/env bash
# Proves the private layer stays private. Drops a canary file into every
# team's corpus/, ledger/ and books/ (and into a made-up future team), then
# fails if git would stage any of them or already tracks anything there.
# Run before every push. Exit 0 means pass.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

stamp="CANARY-$$-$RANDOM"
fail=0
made=()
dirs=()

cleanup() {
  for f in "${made[@]:-}"; do [ -n "$f" ] && rm -f "$f"; done
  # Remove only the folders this run created, deepest first.
  for (( i=${#dirs[@]}-1; i>=0; i-- )); do rmdir "${dirs[$i]}" 2>/dev/null || true; done
}
trap cleanup EXIT

mkd() {  # mkdir -p that remembers each folder it had to create
  local path="" part
  IFS=/ read -ra parts <<< "$1"
  for part in "${parts[@]}"; do
    path="${path:+$path/}$part"
    if [ ! -d "$path" ]; then mkdir "$path"; dirs+=("$path"); fi
  done
}

teams=(canaryteam)
for team in */; do
  team="${team%/}"
  [ -f "$team/CLAUDE.md" ] || [ -d "$team/corpus" ] || [ -d "$team/ledger" ] || continue
  teams+=("$team")
done

for team in "${teams[@]}"; do
  for d in corpus ledger books; do
    mkd "$team/$d/nested"
    for f in "$team/$d/$stamp.md" "$team/$d/nested/.$stamp" "$team/$d/nested/$stamp.epub"; do
      if [ ! -e "$f" ]; then echo canary > "$f"; made+=("$f"); fi
    done
  done
done
echo canary > "$stamp.epub"; made+=("$stamp.epub")

# 1. Every canary is ignored.
for f in "${made[@]}"; do
  if ! git check-ignore -q --no-index "$f"; then
    echo "FAIL: not ignored: $f"; fail=1
  fi
done

# 2. Staging everything would stage no canary and nothing private.
staged="$(git add --dry-run --all . 2>/dev/null || true)"
if printf '%s\n' "$staged" | grep -E "$stamp|^add '[^/]+/(corpus|ledger|books)/|\.epub'" >/dev/null; then
  echo "FAIL: git add would stage private files:"
  printf '%s\n' "$staged" | grep -E "$stamp|^add '[^/]+/(corpus|ledger|books)/|\.epub'"
  fail=1
fi

# 3. Nothing private is already tracked or in the index.
tracked="$(git ls-files --cached | grep -E '^[^/]+/(corpus|ledger|books)/|\.epub$' || true)"
if [ -n "$tracked" ]; then
  echo "FAIL: private files are tracked:"; printf '%s\n' "$tracked"; fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "PASS: ${#made[@]} canaries across ${#teams[@]} teams (${teams[*]}) all ignored; nothing private tracked."
fi
exit "$fail"
