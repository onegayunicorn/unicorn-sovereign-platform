#!/usr/bin/env python3
"""Build the Tranche #2 drop-in ZIP and SHA-256 sidecar from repository files."""
from __future__ import annotations

import hashlib
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "unicorn-platform-tranche-2-capabilities-v1.0"
DIST = ROOT / "dist"
SOURCE_PATHS = (
    "unicorn-quantum",
    "quantum/tests/test_capability_endpoint.py",
    "schemas/sovereign-event-v1.schema.json",
)

README = """# Unicorn Platform Tranche #2 — Capability Reporting

Maturity: PROTOTYPE. This is a drop-in package for the read-only FastAPI capability endpoint.

## Install / apply
Copy the contents under files/ into the target repository, preserving paths. Review the diff before committing. Do not copy this package onto main directly.

## Verify
Run ./verify.sh from the extracted package root. It installs only the test dependencies needed for this tranche and runs the endpoint contract tests.

## Runtime configuration
Set SOVEREIGN_SOURCE_REVISION to the exact deployed Git commit SHA. Configure SOVEREIGN_CAPABILITY_EVIDENCE_FILE only when a reviewed evidence producer exists. Without a source revision, the endpoint returns UNKNOWN and omits individual capability claims.

## Safety
GET only. No shell execution, deployment, Git writes, hardware activation, or remote mutation. The local evidence file is not a signed attestation. SIMULATED remains SIMULATED.

## Rollback
Use a visible git revert on the development branch. Never force-push or overwrite main.
"""

CODE_NOTES = """# CODE_NOTES — Tranche #2

- Adds the read-only GET /api/v1/capabilities/ route to the existing FastAPI app.
- Reports only the explicit capability registry.
- Requires fresh, revision-matched evidence before emitting per-capability event envelopes.
- Missing revision means UNKNOWN summary and zero per-capability claims.
- Stale, malformed, duplicate, mismatched, and unavailable evidence fails closed.
- Preserves SIMULATED and records PROTOTYPE as maturity metadata, not as a v1 classification.
- The configured local evidence file is not cryptographically authenticated.
- CI must pass before the PR is marked ready; merge remains an explicit human gate.
"""

VERIFY = """#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/files"
python -m pip install 'fastapi>=0.115,<1' 'httpx>=0.27,<1' 'pytest>=8.3,<9' 'jsonschema[format]>=4.23,<5'
python -m pytest quantum/tests/test_capability_endpoint.py -v
"""

CI = """name: Tranche 2 Capability Validation
on:
  pull_request:
  push:
jobs:
  capability-contract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e '.[dev]'
      - run: python -m pytest quantum/tests/test_capability_endpoint.py -v
      - run: node scripts/validate-all.mjs
"""


def main() -> None:
    DIST.mkdir(exist_ok=True)
    archive = DIST / f"{NAME}.zip"
    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp) / NAME
        (stage / "files").mkdir(parents=True)
        (stage / "ci").mkdir()
        (stage / "README.md").write_text(README, encoding="utf-8")
        (stage / "CODE_NOTES.md").write_text(CODE_NOTES, encoding="utf-8")
        (stage / "verify.sh").write_text(VERIFY, encoding="utf-8")
        (stage / "ci" / "validate.yml").write_text(CI, encoding="utf-8")
        for item in SOURCE_PATHS:
            src = ROOT / item
            dst = stage / "files" / item
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
            elif src.is_file():
                shutil.copy2(src, dst)
            else:
                raise FileNotFoundError(f"Required package source missing: {item}")
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for file in sorted(stage.rglob("*")):
                if file.is_file():
                    zf.write(file, file.relative_to(stage.parent))
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    sidecar = archive.with_suffix(archive.suffix + ".sha256")
    sidecar.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    print(f"Created {archive}")
    print(f"SHA256 {digest}")
    print(f"Sidecar {sidecar}")


if __name__ == "__main__":
    main()
