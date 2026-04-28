#!/usr/bin/env bash
set -euo pipefail

# Validate staged files against Hermes multi-agent ownership rules.
# Usage: scripts/check-agent-ownership.sh [agent]
# If [agent] is omitted, it is inferred from the current branch prefix.

branch="$(git branch --show-current 2>/dev/null || true)"
agent="${1:-}"

if [[ -z "$agent" ]]; then
  case "$branch" in
    alpha/*) agent="alpha" ;;
    beta/*) agent="beta" ;;
    gamma/*) agent="gamma" ;;
    *)
      echo "No agent inferred from branch '$branch'; skipping ownership check."
      exit 0
      ;;
  esac
fi

case "$agent" in
  alpha|beta|gamma) ;;
  *) echo "Unknown agent '$agent'. Expected alpha, beta, or gamma." >&2; exit 2 ;;
esac

changed="$(git diff --cached --name-only)"
if [[ -z "$changed" ]]; then
  changed="$(git diff --name-only)"
fi

if [[ -z "$changed" ]]; then
  echo "No changed files to check."
  exit 0
fi

violations=0
warnings=0

is_allowed() {
  local file="$1"
  case "$agent" in
    alpha)
      [[ "$file" == "index.html" ]] && return 0
      [[ "$file" == public/* ]] && return 0
      ;;
    beta)
      [[ "$file" == "server.py" ]] && return 0
      [[ "$file" == "kwr_backend.py" ]] && return 0
      [[ "$file" == "backup.py" ]] && return 0
      [[ "$file" == "r5_features.py" ]] && return 0
      [[ "$file" == "r6_features.py" ]] && return 0
      [[ "$file" == n8n_*.py ]] && return 0
      [[ "$file" == "openapi.yaml" ]] && return 0
      ;;
    gamma)
      [[ "$file" == tests/* ]] && return 0
      [[ "$file" == scripts/* ]] && return 0
      [[ "$file" == .github/* ]] && return 0
      [[ "$file" == docs/* ]] && return 0
      ;;
  esac
  return 1
}

is_danger() {
  local file="$1"
  case "$file" in
    index.html|data.json|Dockerfile|AGENTS.md|.github/workflows/*) return 0 ;;
    *) return 1 ;;
  esac
}

echo "Agent: $agent"
echo "Branch: $branch"
echo "Changed files:"

while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  echo "  - $file"
  if is_danger "$file"; then
    echo "    ⚠️ danger/locked file: coordinate before merge"
    warnings=$((warnings + 1))
  fi
  if ! is_allowed "$file"; then
    # Allow docs/AGENTS updates on non-agent maintainer branches only. Agent branches must stay scoped.
    echo "    ❌ outside $agent ownership scope"
    violations=$((violations + 1))
  fi
done <<< "$changed"

if [[ "$violations" -gt 0 ]]; then
  echo "🚫 Ownership check failed: $violations violation(s)."
  exit 1
fi

if [[ "$warnings" -gt 0 ]]; then
  echo "⚠️ Ownership check passed with $warnings danger-file warning(s)."
else
  echo "✅ Ownership check passed."
fi
