"""Model registry with version pinning."""
from __future__ import annotations
from pydantic import BaseModel
from typing import Dict, Optional

class ModelSpec(BaseModel):
    model_id: str
    provider: str
    version: str
    pinned: bool = True
    context_window: int = 4096
    max_output_tokens: int = 1024

class ModelRegistry:
    def __init__(self):
        self._models: Dict[str, ModelSpec] = {}

    def register(self, spec: ModelSpec) -> None:
        self._models[spec.model_id] = spec

    def resolve(self, model_id: str) -> Optional[ModelSpec]:
        return self._models.get(model_id)
