"""Source characterization routines: pump power, temperature, isolation, polarization, coincidence window, source-rate logging, dark-count, spectral filtering, visibility."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .interface import PhotonicSource, SourceMetrics

@dataclass
class CharacterizationReport:
    source_id: str
    timestamp: float
    metrics_series: List[SourceMetrics]
    stability_score: float
    classification: str = "Prototype"

def characterize_source(source: PhotonicSource, samples: int = 10) -> CharacterizationReport:
    series = [source.get_metrics() for _ in range(samples)]
    visibilities = [m.visibility for m in series]
    avg_vis = sum(visibilities) / len(visibilities)
    return CharacterizationReport(
        source_id="mock-source-001",
        timestamp=__import__("time").time(),
        metrics_series=series,
        stability_score=avg_vis,
    )
