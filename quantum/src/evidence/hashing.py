"""SHA-256 chain-of-custody hashing."""
from __future__ import annotations
import hashlib, json
from typing import Any

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def sha256_obj(obj: Any) -> str:
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(canonical)

class HashChain:
    """Merkle-linked experiment ledger — each entry links to previous hash."""
    def __init__(self):
        self._entries: list[dict] = []
        self._last_hash: str | None = None

    def append(self, payload: Any) -> dict:
        entry = {
            "seq": len(self._entries),
            "payload_hash": sha256_obj(payload),
            "prev_hash": self._last_hash,
        }
        entry["entry_hash"] = sha256_obj(entry)
        self._last_hash = entry["entry_hash"]
        self._entries.append(entry)
        return entry

    @property
    def root_hash(self) -> str | None:
        return self._last_hash
