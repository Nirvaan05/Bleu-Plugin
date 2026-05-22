#!/usr/bin/env bash
# Bleu Hook Adapter: SessionStart
# Triggers recovery and graph refresh via the deterministic harness.
#
# SessionStart delivers a JSON payload on STDIN; this adapter takes no fields
# from it but still drains stdin so the pipe does not block.
set -euo pipefail

cat >/dev/null 2>&1 || true

# Portable interpreter: python3 on most Unix, python on Windows / many distros.
PY="${PYTHON:-$(command -v python3 || command -v python)}"

cd "${CLAUDE_PROJECT_DIR:-.}"
"$PY" scripts/bleu/harness.py --hook session_start
