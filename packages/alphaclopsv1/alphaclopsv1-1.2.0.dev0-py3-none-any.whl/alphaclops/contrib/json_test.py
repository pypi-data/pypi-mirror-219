# pylint: disable=wrong-or-nonexistent-copyright-notice
import alphaclops
from alphaclops.testing import assert_json_roundtrip_works
from alphaclops.contrib.json import DEFAULT_CONTRIB_RESOLVERS
from alphaclops.contrib.acquaintance import SwapPermutationGate
from alphaclops.contrib.bayesian_network import BayesianNetworkGate
from alphaclops.contrib.quantum_volume import QuantumVolumeResult


def test_bayesian_network_gate():
    gate = BayesianNetworkGate(
        init_probs=[('q0', 0.125), ('q1', None)], arc_probs=[('q1', ('q0',), [0.25, 0.5])]
    )
    assert_json_roundtrip_works(gate, resolvers=DEFAULT_CONTRIB_RESOLVERS)


def test_quantum_volume():
    qubits = alphaclops.LineQubit.range(5)
    qvr = QuantumVolumeResult(
        model_circuit=alphaclops.Circuit(alphaclops.H.on_each(qubits)),
        heavy_set=[1, 2, 3],
        compiled_circuit=alphaclops.Circuit(alphaclops.H.on_each(qubits)),
        sampler_result=0.1,
    )
    assert_json_roundtrip_works(qvr, resolvers=DEFAULT_CONTRIB_RESOLVERS)


def test_swap_permutation_gate():
    gate = SwapPermutationGate(swap_gate=alphaclops.SWAP)
    assert_json_roundtrip_works(gate, resolvers=DEFAULT_CONTRIB_RESOLVERS)
