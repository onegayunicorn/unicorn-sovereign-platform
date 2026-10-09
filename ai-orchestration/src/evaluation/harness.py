"""Evaluation harness + golden test sets."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, List, Dict

@dataclass
class GoldenTest:
    test_id: str
    input: str
    expected_output: str
    matcher: Callable[[str, str], bool] = lambda a, b: a.strip() == b.strip()
    category: str = "general"

class EvaluationHarness:
    def __init__(self):
        self._tests: List[GoldenTest] = []

    def add_test(self, test: GoldenTest) -> None:
        self._tests.append(test)

    def run(self, agent_fn: Callable[[str], str]) -> Dict[str, float]:
        passed = 0
        results = {}
        for t in self._tests:
            output = agent_fn(t.input)
            ok = t.matcher(output, t.expected_output)
            results[t.test_id] = "pass" if ok else "fail"
            if ok:
                passed += 1
        results["pass_rate"] = passed / len(self._tests) if self._tests else 0.0
        return results
