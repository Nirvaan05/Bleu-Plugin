#!/usr/bin/env bash
# Bleu Hook Adapter: git auto-commit
# Registered on both Stop and SubagentStop (with async: true). Stages only
# blueprint/ and commits asynchronously so the user never loses a phase.
# See plugins/bleu/skills/bleu/references/claude-code-integration.md section 4.
set -euo pipefail

cd "${CLAUDE_PROJECT_DIR:-.}"

# Loop protection: stop_hook_active is set when this hook itself triggered a continuation.
INPUT=$(cat 2>/dev/null || echo '{}')
STOP_ACTIVE=$(printf '%s' "$INPUT" | jq -r '.stop_hook_active // false')
if [ "$STOP_ACTIVE" = "true" ]; then
  exit 0
fi

# Only commit if blueprint/ has changes.
if git diff --quiet --exit-code -- blueprint/ && \
   git diff --cached --quiet --exit-code -- blueprint/; then
  exit 0
fi

git add blueprint/

CHANGED=$(git diff --cached --name-only -- blueprint/ | head -10 | sed 's/^/  - /')
COUNT=$(git diff --cached --name-only -- blueprint/ | wc -l | tr -d ' ')

git -c user.email="claude-code@local" -c user.name="Claude Code (blueprint)" \
    commit -m "blueprint: auto-commit ($COUNT files)

$CHANGED" >/dev/null

echo "blueprint: committed $COUNT file(s)"
