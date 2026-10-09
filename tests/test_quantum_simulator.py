import numpy as np
from unicorn_quantum.packages.provider.simulator.state_vector import simulate, sample_counts
def test_hadamard_probabilities():
    state = simulate({"num_qubits":1,"gates":[{"name":"H","qubits":[0]}]})
    assert np.allclose(np.abs(state)**2, [0.5,0.5])
def test_counts_sum_to_shots():
    state = simulate({"num_qubits":1,"gates":[{"name":"H","qubits":[0]}]})
    assert sum(sample_counts(state, 100, seed=1).values()) == 100
