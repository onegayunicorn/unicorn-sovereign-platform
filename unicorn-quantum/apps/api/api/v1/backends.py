"""Backend registry endpoints."""
from fastapi import APIRouter

router = APIRouter()

BACKENDS = {
    "simulator_statevector": {"type": "simulator", "max_qubits": 32, "available": True},
    "ibm_kyiv": {"type": "hardware", "max_qubits": 127, "available": "conditional"},
}

@router.get("/")
def list_backends():
    return BACKENDS

@router.get("/{backend_name}")
def get_backend(backend_name: str):
    if backend_name not in BACKENDS:
        return {"error": "unknown backend", "available_backends": list(BACKENDS.keys())}
    return BACKENDS[backend_name]
