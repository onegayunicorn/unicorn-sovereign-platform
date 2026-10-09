"""Job submission + status endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
from ....packages.domain.job import JobModel, JobStatus
from ....packages.execution.idempotency import IdempotencyStore
import time, uuid

router = APIRouter()
_jobs: Dict[str, JobModel] = {}
_idem = IdempotencyStore()

@router.post("/")
def submit_job(circuit_id: str, backend: str = "simulator", shots: int = 1024,
               idempotency_key: Optional[str] = None):
    if idempotency_key:
        existing = _idem.check(idempotency_key)
        if existing:
            return {"job_id": existing, "status": "duplicate_suppressed"}
    job_id = str(uuid.uuid4())
    job = JobModel(job_id=job_id, circuit_id=circuit_id, backend=backend, shots=shots,
                   status=JobStatus.DRAFT, idempotency_key=idempotency_key,
                   created_at=time.time(), updated_at=time.time())
    _jobs[job_id] = job
    if idempotency_key:
        _idem.register(idempotency_key, job_id)
    return {"job_id": job_id, "status": job.status.value}

@router.get("/{job_id}")
def get_job(job_id: str):
    if job_id not in _jobs:
        raise HTTPException(404, "Job not found")
    return _jobs[job_id]
