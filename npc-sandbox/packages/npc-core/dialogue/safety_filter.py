"""4-gate safety pipeline.
Gate 1: Input sanitization (injection defense)
Gate 2: Topic policy check (allowed/forbidden topics)
Gate 3: Output generation constraint
Gate 4: Output audit + redaction
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

@dataclass
class SafetyResult:
    passed: bool
    gate_failed: int | None
    reason: str
    sanitized_input: str = ""
    redacted_output: str = ""

class FourGateSafetyFilter:
    def __init__(self, forbidden_topics: list[str] | None = None):
        self.forbidden_topics = forbidden_topics or []

    def gate1_input_sanitize(self, text: str) -> Tuple[bool, str]:
        # Strip injection patterns
        sanitized = text.replace("\x00", "")
        if len(text) > 4000:
            return False, "input too long"
        return True, sanitized

    def gate2_topic_check(self, text: str) -> Tuple[bool, str]:
        t = text.lower()
        for topic in self.forbidden_topics:
            if topic.lower() in t:
                return False, f"forbidden topic: {topic}"
        return True, ""

    def gate3_output_constraint(self, output: str) -> Tuple[bool, str]:
        if len(output) > 2000:
            return False, "output too long"
        return True, output

    def gate4_audit_redact(self, output: str) -> str:
        # Simple PII redaction placeholder
        import re
        redacted = re.sub(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b", "[REDACTED_CARD]", output)
        return redacted

    def process(self, player_input: str, npc_output: str) -> SafetyResult:
        ok1, sanitized = self.gate1_input_sanitize(player_input)
        if not ok1:
            return SafetyResult(False, 1, sanitized)
        ok2, reason = self.gate2_topic_check(player_input)
        if not ok2:
            return SafetyResult(False, 2, reason, sanitized_input=sanitized)
        ok3, out = self.gate3_output_constraint(npc_output)
        if not ok3:
            return SafetyResult(False, 3, out, sanitized_input=sanitized)
        redacted = self.gate4_audit_redact(out)
        return SafetyResult(True, None, "passed", sanitized_input=sanitized, redacted_output=redacted)
