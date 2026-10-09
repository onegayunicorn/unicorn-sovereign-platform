"""Photonic model tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from photonic.source.mock_driver import MockPhotonicSource
from photonic.source.interface import SourceConfig
from photonic.detector.mock_driver import MockDetector
from photonic.timing.correlation import correlate

def test_mock_source_lifecycle():
    src = MockPhotonicSource()
    src.initialize(SourceConfig(100, 25, "H", 2.0, 3.0))
    assert src.health_check()
    src.start()
    m = src.get_metrics()
    assert 0 < m.visibility <= 1.0
    src.stop()

def test_mock_detector():
    d = MockDetector(0)
    d.arm()
    ts = d.read_timestamps()
    assert isinstance(ts, list)
    d.disarm()

def test_correlation_empty():
    r = correlate([], [], window_ns=2.0)
    assert r.coincidences == 0
