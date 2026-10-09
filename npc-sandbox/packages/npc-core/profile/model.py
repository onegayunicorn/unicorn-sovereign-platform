"""Character profile model — original fictional game asset."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Dict

class CharacterProfile(BaseModel):
    character_id: str
    name: str
    archetype: str
    backstory: str
    traits: List[str] = Field(default_factory=list)
    dialogue_style: str
    fictional_disclaimer: str = "Fictional game asset — 100% original content, no copyrighted IP."
    allowed_topics: List[str] = Field(default_factory=list)
    forbidden_topics: List[str] = Field(default_factory=list)
