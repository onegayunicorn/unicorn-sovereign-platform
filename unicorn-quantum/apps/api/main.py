"""FastAPI entry point."""
from fastapi import FastAPI
from .api.v1 import circuits, jobs, backends
from .websockets import job_events

app = FastAPI(title="Unicorn Quantum Platform API", version="1.0.0")
app.include_router(circuits.router, prefix="/api/v1/circuits", tags=["circuits"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["jobs"])
app.include_router(backends.router, prefix="/api/v1/backends", tags=["backends"])
app.include_router(job_events.router, prefix="/ws", tags=["websockets"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "unicorn-quantum-api"}
