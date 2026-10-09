"""unicorn CLI (Typer-based)."""
import typer, json
from typing import Optional

app = typer.Typer(name="unicorn", help="Unicorn Quantum Platform CLI")

@app.command()
def submit(circuit: str, backend: str = "simulator", shots: int = 1024,
           idempotency_key: Optional[str] = None):
    """Submit a circuit file for execution."""
    typer.echo(json.dumps({"circuit": circuit, "backend": backend, "shots": shots,
                           "idempotency_key": idempotency_key, "status": "submitted"}))

@app.command()
def status(job_id: str):
    """Check job status."""
    typer.echo(json.dumps({"job_id": job_id, "status": "UNKNOWN"}))

@app.command()
def backends():
    """List available backends."""
    typer.echo(json.dumps(["simulator_statevector", "ibm_kyiv"]))

if __name__ == "__main__":
    app()
