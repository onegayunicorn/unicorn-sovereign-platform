from quantum.src.bell.simulation import run_chsh
def test_chsh_simulation_is_reproducible():
    assert run_chsh(shots=500, seed=42) == run_chsh(shots=500, seed=42)
def test_visibility_validation():
    import pytest
    with pytest.raises(ValueError): run_chsh(visibility=2)
