"""Node enrollment + health checks. A node cannot join the network until it passes all launch gates."""
from __future__ import annotations
from .model import NodeRecord, NodeStatus
from dataclasses import dataclass
from typing import List

LAUNCH_GATES = [
    "hardware_inspection",
    "electrical_optical_safety_review",
    "firmware_signature_verification",
    "calibration_check",
    "detector_characterization",
    "clock_timestamp_validation",
    "classical_channel_authentication",
    "negative_control_experiment",
    "operator_training",
    "incident_response_test",
    "evidence_package_review",
]

@dataclass
class EnrollmentResult:
    node_id: str
    passed_gates: List[str]
    failed_gates: List[str]
    enrolled: bool

class NodeEnroller:
    def __init__(self):
        self._nodes: dict[str, NodeRecord] = {}

    def register(self, node: NodeRecord) -> None:
        self._nodes[node.node_id] = node

    def pass_gate(self, node_id: str, gate: str) -> None:
        if node_id in self._nodes:
            # In a real system this persists to DB; here we track via status
            self._nodes[node_id].status = NodeStatus.ENROLLED

    def enroll(self, node_id: str, passed_gates: List[str]) -> EnrollmentResult:
        failed = [g for g in LAUNCH_GATES if g not in passed_gates]
        enrolled = len(failed) == 0
        if enrolled and node_id in self._nodes:
            self._nodes[node_id].status = NodeStatus.ONLINE
        return EnrollmentResult(node_id, passed_gates, failed, enrolled)

    def get(self, node_id: str) -> NodeRecord | None:
        return self._nodes.get(node_id)
