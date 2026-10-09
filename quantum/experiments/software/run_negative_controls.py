"""Negative control suite — must NOT violate CHSH."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from bell.negative_controls import run_classical_control, run_separable_state_control, assert_no_violation

def main():
    results = {}
    classical = run_classical_control(shots=1024)
    separable = run_separable_state_control(shots=1024)
    results["classical_lhv"] = {"s": round(classical.s_value, 4), "pass": assert_no_violation(classical)}
    results["separable_state"] = {"s": round(separable.s_value, 4), "pass": assert_no_violation(separable)}
    all_pass = all(r["pass"] for r in results.values())
    results["all_controls_pass"] = all_pass
    print(json.dumps(results, indent=2))
    assert all_pass, "Negative control FAILED — violation detected where none should exist"

if __name__ == "__main__":
    main()
