#!/usr/bin/env bash
set -euo pipefail
find . -name '__pycache__' -type d -prune -exec rm -rf {} +
find . -name '*.pyc' -type f -delete
python -m pytest quantum/tests/ ai-orchestration/tests/ -v
node scripts/validate-all.mjs
