"""Node registry Pydantic model."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class NodeStatus(str, Enum):
    PROVISIONING = "provisioning"
    ENROLLED = "enrolled"
    ONLINE = "online"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
    DECOMMISSIONED = "decommissioned"

class NodeCapabilities(BaseModel):
    photonic_source: bool = False
    single_photon_detector: bool = False
    timing_hardware: bool = False
    fiber_link: bool = False
    free_space_link: bool = False

class NodeRecord(BaseModel):
    node_id: str
    region: str
    physical_location: str
    capabilities: NodeCapabilities
    firmware_version: str
    calibration_status: str = "uncalibrated"
    last_heartbeat: Optional[float] = None
    link_status: str = "unknown"
    maintenance_state: str = "none"
    evidence_status: str = "none"
    operator_identity: str
    status: NodeStatus = NodeStatus.PROVISIONING
    public_key: Optional[str] = None
