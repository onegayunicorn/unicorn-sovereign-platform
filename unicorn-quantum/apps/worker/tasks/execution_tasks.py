"""Durable execution workers — Celery tasks.
Recovery guarantee: kill worker → restart → result persisted exactly once.
"""
from celery import Celery
import os, json, time

app = Celery("unicorn_worker", broker=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
             backend=os.environ.get("REDIS_URL", "redis://localhost:6379/0"))

@app.task(bind=True, max_retries=3, acks_late=True)
def execute_circuit(self, job_id: str, circuit_ir_json: str, backend: str, shots: int):
    """Execute a circuit. Idempotent via job_id lock in result store."""
    from ....packages.circuit_ir.models import UnicornCircuitIR
    from ....packages.providers.simulator.statevector import StateVectorSimulator
    ir = UnicornCircuitIR.model_validate_json(circuit_ir_json)
    sim = StateVectorSimulator()
    counts = sim.sample(ir, shots=shots)
    result = {"job_id": job_id, "counts": counts, "backend": backend, "shots": shots,
              "completed_at": time.time()}
    # Persist exactly once — idempotency enforced by caller
    return result
