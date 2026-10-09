"""Stage 0 CHSH experiment — no hardware required.
Acceptance: S ~ 2.828 (quantum) with 1024 shots; CI lower bound > 2.
"""
import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from bell.simulation import run_chsh, bell_state_counts
from bell.analysis import chsh_confidence_interval, violates_classical_bound

def main():
    shots = 1024
    counts = bell_state_counts(shots=shots, noise=0.0)
    result = run_chsh(shots=shots, noise=0.0)
    ci = chsh_confidence_interval(result.s_value, shots)
    report = {
        "experiment_id": "chsh-stage0-001",
        "classification": "Simulated",
        "shots": shots,
        "bell_counts": counts,
        "chsh_s_value": round(result.s_value, 4),
        "correlation_terms": [round(t, 4) for t in result.correlation_terms],
        "confidence_interval_95": [round(ci.lower, 4), round(ci.upper, 4)],
        "classical_bound_violated": violates_classical_bound(ci),
        "classical_bound": 2.0,
        "quantum_max": 2.8284,
    }
    print(json.dumps(report, indent=2))
    out = os.path.join(os.path.dirname(__file__), "chsh_result.json")
    with open(out, "w") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    main()
