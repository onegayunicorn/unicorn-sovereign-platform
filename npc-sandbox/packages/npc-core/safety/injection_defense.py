"""Prompt injection defense for NPC dialogue."""
from __future__ import annotations
import re

INJECTION_PATTERNS = [
    r"ignore (all |previous )?instructions",
    r"you are now",
    r"system prompt",
    r"\[system\]",
    r"override (your |the )?(safety|policy|rules)",
    r"jailbreak",
    r"developer mode",
]

def detect_injection(text: str) -> tuple[bool, list[str]]:
    found = []
    lower = text.lower()
    for pat in INJECTION_PATTERNS:
        if re.search(pat, lower):
            found.append(pat)
    return len(found) > 0, found

def sanitize_input(text: str) -> str:
    # Strip control characters and normalize
    return re.sub(r"[\x00-\x1f\x7f]", "", text)[:4000]
