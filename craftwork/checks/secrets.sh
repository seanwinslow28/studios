#!/bin/sh
# Stops a commit that would add a password, key or token.
# Scans only what is staged, with Betterleaks, or Gitleaks when Betterleaks
# isn't installed. Findings are redacted: the output says where, never what.
# Exit 0: nothing found. Exit 1: something found, or no scanner could run.
set -eu

if command -v betterleaks >/dev/null 2>&1; then
  scanner=betterleaks
elif command -v gitleaks >/dev/null 2>&1; then
  scanner=gitleaks
else
  echo "The secrets check couldn't run: neither Betterleaks nor Gitleaks is installed." >&2
  echo "Install one with: brew install betterleaks" >&2
  exit 1
fi

# Report only file, line and rule. --verbose would also print the rest of the
# line around the secret, which could hold a private name. Never pass
# --validation: it would send what it found to outside services.
template="$(mktemp)"
trap 'rm -f "$template"' EXIT
printf '%s\n' '{{if .}}A password, key or token is staged at:{{"\n"}}{{end}}{{range .}}  {{.File}}:{{.StartLine}} ({{.RuleID}}){{"\n"}}{{end}}' > "$template"
"$scanner" git --pre-commit --staged --redact --no-banner --no-color --exit-code 1 \
  --report-format template --report-template "$template" --report-path - .
