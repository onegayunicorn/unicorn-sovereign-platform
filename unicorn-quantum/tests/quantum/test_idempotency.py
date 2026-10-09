"""Idempotency: same key → one provider job only."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages"))
from execution.idempotency import IdempotencyStore

def test_idempotency_dedup():
    store = IdempotencyStore()
    assert store.register("key-1", "job-1") is True
    assert store.register("key-1", "job-2") is False  # duplicate
    assert store.check("key-1") == "job-1"
