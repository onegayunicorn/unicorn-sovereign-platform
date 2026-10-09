"""Circuit CRUD endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Dict
from ....packages.domain.circuit import CircuitModel

router = APIRouter()
_store: Dict[str, CircuitModel] = {}

@router.post("/")
def create_circuit(circuit: CircuitModel):
    _store[circuit.circuit_id] = circuit
    return {"circuit_id": circuit.circuit_id, "checksum": circuit.checksum()}

@router.get("/{circuit_id}")
def get_circuit(circuit_id: str):
    if circuit_id not in _store:
        raise HTTPException(404, "Circuit not found")
    return _store[circuit_id]

@router.get("/")
def list_circuits():
    return list(_store.keys())
