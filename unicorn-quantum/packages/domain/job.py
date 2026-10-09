"""Job model + JobStatus enum."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class JobStatus(str, Enum):
    DRAFT = "DRAFT"
    VALIDATING = "VALIDATING"
    VALIDATED = "VALIDATED"
    COMPILING = "COMPILING"
    COMPILED = "COMPILED"
    QUEUED = "QUEUED"
    SUBMITTED = "SUBMITTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    RETRYING = "RETRYING"

class JobModel(BaseModel):
    job_id: str
    circuit_id: str
    backend: str
    shots: int = Field(ge=1, le=1_000_000, default=1024)
    status: JobStatus = JobStatus.DRAFT
    idempotency_key: Optional[str] = None
    result_uri: Optional[str] = None
    error_message: Optional[str] = None
    created_at: float = 0.0
    updated_at: float = 0.0
