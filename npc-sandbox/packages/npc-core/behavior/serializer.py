"""Save/load serialization for NPC behavior state."""
from __future__ import annotations
import json
from dataclasses import asdict, is_dataclass
from typing import Any

def serialize_state(state: Any) -> str:
    if is_dataclass(state):
        return json.dumps(asdict(state), indent=2, default=str)
    return json.dumps(state, indent=2, default=str)

def deserialize_state(data: str, cls: type) -> Any:
    obj = json.loads(data)
    return cls(**obj)
