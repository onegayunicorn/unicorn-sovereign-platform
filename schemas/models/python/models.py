from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal

# ------------------------------
# Quantum Job
# ------------------------------
class BackendInfo(BaseModel):
    provider: str
    target: str
    region: Optional[str] = None

class Policy(BaseModel):
    jurisdiction: str
    dataClassification: Literal["public", "internal", "confidential", "regulated"]
    approved: bool
    decisionReason: Optional[str] = None

class ExecutionOptions(BaseModel):
    shots: int = Field(gt=0)
    priority: Optional[int] = Field(None, ge=1, le=10)

class QuantumJob(BaseModel):
    jobId: str
    correlationId: str
    tenantId: str
    workspaceId: Optional[str] = None
    circuitId: str
    status: Literal[
        "submitted", "validated", "approved", "queued",
        "executing", "completed", "failed", "cancelled", "rejected"
    ]
    backend: BackendInfo
    policy: Policy
    execution: Optional[ExecutionOptions] = None
    submittedAt: str  # ISO-8601
    startedAt: Optional[str] = None
    completedAt: Optional[str] = None
    createdBy: Optional[str] = None

# ------------------------------
# Quantum Circuit
# ------------------------------
class QuantumCircuit(BaseModel):
    circuitId: str
    name: str
    version: Optional[str] = None
    format: Literal["openqasm2", "openqasm3", "qir", "quil", "cirq-json"]
    qubitCount: Optional[int] = None
    depth: Optional[int] = None
    content: str
    hash: str
    signature: Optional[str] = None
    createdBy: Optional[str] = None
    createdAt: str

# ------------------------------
# Artifact
# ------------------------------
class Artifact(BaseModel):
    artifactId: str
    jobId: str
    artifactType: Literal[
        "circuit", "compiled-circuit", "result", "histogram",
        "simulation-output", "attestation", "audit-export",
        "sbom", "evidence-package"
    ]
    storageUri: str
    contentType: Optional[str] = None
    sizeBytes: Optional[int] = None
    hash: str
    encrypted: Optional[bool] = None
    kmsKeyId: Optional[str] = None
    retentionDays: Optional[int] = None
    createdAt: str

# ------------------------------
# Audit Event
# ------------------------------
class AuditEvent(BaseModel):
    eventId: str
    correlationId: str
    jobId: str
    tenantId: Optional[str] = None
    timestamp: str
    eventType: Literal[
        "job-submitted", "policy-evaluated", "job-approved", "job-rejected",
        "job-queued", "execution-started", "execution-completed",
        "execution-failed", "artifact-created", "attestation-verified",
        "result-delivered"
    ]
    source: Literal["unicorndrop", "qps", "scheduler", "gateway", "kms", "operator"]
    severity: Literal["info", "warning", "error", "critical"]
    details: Optional[Dict[str, Any]] = None
    signature: Optional[str] = None
