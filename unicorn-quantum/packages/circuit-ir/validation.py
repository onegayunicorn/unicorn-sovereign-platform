"""Validation pipeline for IR."""
from __future__ import annotations
from .models import UnicornCircuitIR
from typing import List

class ValidationError(Exception):
    pass

def validate_ir(ir: UnicornCircuitIR) -> List[str]:
    errors = []
    for i, op in enumerate(ir.operations):
        for q in op.qubits:
            if q < 0 or q >= ir.num_qubits:
                errors.append(f"op {i}: qubit {q} out of range (0..{ir.num_qubits-1})")
        if op.op == "measure" and op.params:
            c = int(op.params[0])
            if c < 0 or c >= ir.num_clbits:
                errors.append(f"op {i}: clbit {c} out of range")
    return errors

def assert_valid(ir: UnicornCircuitIR) -> None:
    errs = validate_ir(ir)
    if errs:
        raise ValidationError("; ".join(errs))
