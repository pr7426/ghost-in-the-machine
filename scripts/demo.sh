#!/usr/bin/env bash
# Scripted Phantom Shell demo (mock mode — works without Ollama).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
export PHANTOM_MOCK=1
exec python3 -m phantom_shell demo --color always
