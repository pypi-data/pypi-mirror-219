# Copyright 2022 The alphaclops Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import alphaclops
import pytest


def test_directed_device():
    device = alphaclops.testing.construct_ring_device(10, directed=True)
    device_graph = device.metadata.nx_graph
    with pytest.raises(ValueError, match="Device graph must be undirected."):
        alphaclops.RouteCQC(device_graph)


@pytest.mark.parametrize(
    "n_qubits, n_moments, op_density, seed",
    [
        (8, size, op_density, seed)
        for size in [50, 100]
        for seed in range(3)
        for op_density in [0.3, 0.5, 0.7]
    ],
)
def test_route_small_circuit_random(n_qubits, n_moments, op_density, seed):
    c_orig = alphaclops.testing.random_circuit(
        qubits=n_qubits, n_moments=n_moments, op_density=op_density, random_state=seed
    )
    device = alphaclops.testing.construct_grid_device(4, 4)
    device_graph = device.metadata.nx_graph
    router = alphaclops.RouteCQC(device_graph)
    c_routed, imap, swap_map = router.route_circuit(c_orig, tag_inserted_swaps=True)
    device.validate_circuit(c_routed)
    alphaclops.testing.assert_circuits_have_same_unitary_given_final_permutation(
        c_routed, c_orig.transform_qubits(imap), swap_map
    )


def test_high_qubit_count():
    c_orig = alphaclops.testing.random_circuit(qubits=40, n_moments=350, op_density=0.4, random_state=0)
    device = alphaclops.testing.construct_grid_device(7, 7)
    device_graph = device.metadata.nx_graph
    router = alphaclops.RouteCQC(device_graph)
    c_routed = router(c_orig)
    device.validate_circuit(c_routed)


def test_multi_qubit_gate_inputs():
    device = alphaclops.testing.construct_grid_device(4, 4)
    device_graph = device.metadata.nx_graph
    router = alphaclops.RouteCQC(device_graph)
    q = alphaclops.LineQubit.range(5)

    invalid_subcircuit_op = alphaclops.CircuitOperation(
        alphaclops.Circuit(alphaclops.X(q[1]), alphaclops.CCZ(q[0], q[1], q[2]), alphaclops.Y(q[1])).freeze()
    ).with_tags('<mapped_circuit_op>')
    invalid_circuit = alphaclops.Circuit(alphaclops.H(q[0]), alphaclops.H(q[2]), invalid_subcircuit_op)
    with pytest.raises(
        ValueError, match="Input circuit must only have ops that act on 1 or 2 qubits."
    ):
        router(invalid_circuit, context=alphaclops.TransformerContext(deep=True))
    with pytest.raises(
        ValueError, match="Input circuit must only have ops that act on 1 or 2 qubits."
    ):
        router(invalid_circuit, context=alphaclops.TransformerContext(deep=False))

    invalid_circuit = alphaclops.Circuit(alphaclops.CCX(q[0], q[1], q[2]))
    with pytest.raises(
        ValueError, match="Input circuit must only have ops that act on 1 or 2 qubits."
    ):
        router(invalid_circuit, context=alphaclops.TransformerContext(deep=True))
    with pytest.raises(
        ValueError, match="Input circuit must only have ops that act on 1 or 2 qubits."
    ):
        router(invalid_circuit, context=alphaclops.TransformerContext(deep=False))

    valid_subcircuit_op = alphaclops.CircuitOperation(
        alphaclops.Circuit(alphaclops.X(q[1]), alphaclops.CZ(q[0], q[1]), alphaclops.CZ(q[1], q[2]), alphaclops.Y(q[1])).freeze()
    ).with_tags('<mapped_circuit_op>')
    valid_circuit = alphaclops.Circuit(alphaclops.H(q[0]), alphaclops.H(q[2]), valid_subcircuit_op)
    with pytest.raises(
        ValueError, match="Input circuit must only have ops that act on 1 or 2 qubits."
    ):
        router(invalid_circuit, context=alphaclops.TransformerContext(deep=False))
    c_routed = router(valid_circuit, context=alphaclops.TransformerContext(deep=True))
    device.validate_circuit(c_routed)


def test_circuit_with_measurement_gates():
    device = alphaclops.testing.construct_ring_device(3)
    device_graph = device.metadata.nx_graph
    q = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(alphaclops.MeasurementGate(2).on(q[0], q[2]), alphaclops.MeasurementGate(3).on(*q))
    hard_coded_mapper = alphaclops.HardCodedInitialMapper({q[i]: q[i] for i in range(3)})
    router = alphaclops.RouteCQC(device_graph)
    routed_circuit = router(circuit, initial_mapper=hard_coded_mapper)
    alphaclops.testing.assert_same_circuits(routed_circuit, circuit)


def test_circuit_with_non_unitary_and_global_phase():
    device = alphaclops.testing.construct_ring_device(4)
    device_graph = device.metadata.nx_graph
    q = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(
        [
            alphaclops.Moment(alphaclops.CNOT(q[0], q[1]), alphaclops.global_phase_operation(-1)),
            alphaclops.Moment(alphaclops.CNOT(q[1], q[2])),
            alphaclops.Moment(alphaclops.depolarize(0.1, 2).on(q[0], q[2]), alphaclops.depolarize(0.1).on(q[1])),
        ]
    )
    hard_coded_mapper = alphaclops.HardCodedInitialMapper({q[i]: q[i] for i in range(3)})
    router = alphaclops.RouteCQC(device_graph)
    routed_circuit = router(circuit, initial_mapper=hard_coded_mapper)
    expected = alphaclops.Circuit(
        [
            alphaclops.Moment(alphaclops.CNOT(q[0], q[1]), alphaclops.global_phase_operation(-1)),
            alphaclops.Moment(alphaclops.CNOT(q[1], q[2])),
            alphaclops.Moment(alphaclops.depolarize(0.1).on(q[1])),
            alphaclops.Moment(alphaclops.SWAP(q[0], q[1])),
            alphaclops.Moment(alphaclops.depolarize(0.1, 2).on(q[1], q[2])),
        ]
    )
    alphaclops.testing.assert_same_circuits(routed_circuit, expected)


def test_circuit_with_tagged_ops():
    device = alphaclops.testing.construct_ring_device(4)
    device_graph = device.metadata.nx_graph
    q = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(
        [
            alphaclops.Moment(alphaclops.CNOT(q[0], q[1]).with_tags("u")),
            alphaclops.Moment(alphaclops.CNOT(q[1], q[2])),
            alphaclops.Moment(alphaclops.CNOT(q[0], q[2]).with_tags("u")),
            alphaclops.Moment(alphaclops.X(q[0]).with_tags("u")),
            alphaclops.Moment(alphaclops.X(q[0]).with_tags("u")),
        ]
    )
    hard_coded_mapper = alphaclops.HardCodedInitialMapper({q[i]: q[i] for i in range(3)})
    router = alphaclops.RouteCQC(device_graph)
    routed_circuit = router(circuit, initial_mapper=hard_coded_mapper)
    expected = alphaclops.Circuit(
        [
            alphaclops.Moment(alphaclops.TaggedOperation(alphaclops.CNOT(q[0], q[1]), 'u')),
            alphaclops.Moment(alphaclops.CNOT(q[1], q[2])),
            alphaclops.Moment(alphaclops.SWAP(q[0], q[1])),
            alphaclops.Moment(alphaclops.TaggedOperation(alphaclops.CNOT(q[1], q[2]), 'u')),
            alphaclops.Moment(alphaclops.TaggedOperation(alphaclops.X(q[1]), 'u')),
            alphaclops.Moment(alphaclops.TaggedOperation(alphaclops.X(q[1]), 'u')),
        ]
    )
    alphaclops.testing.assert_same_circuits(routed_circuit, expected)


def test_already_valid_circuit():
    device = alphaclops.testing.construct_ring_device(10)
    device_graph = device.metadata.nx_graph
    circuit = alphaclops.Circuit(
        [alphaclops.Moment(alphaclops.CNOT(alphaclops.LineQubit(i), alphaclops.LineQubit(i + 1))) for i in range(9)],
        alphaclops.X(alphaclops.LineQubit(1)),
    )
    hard_coded_mapper = alphaclops.HardCodedInitialMapper(
        {alphaclops.LineQubit(i): alphaclops.LineQubit(i) for i in range(10)}
    )
    router = alphaclops.RouteCQC(device_graph)
    routed_circuit = router(circuit, initial_mapper=hard_coded_mapper)

    device.validate_circuit(routed_circuit)
    alphaclops.testing.assert_same_circuits(routed_circuit, circuit)


def test_empty_circuit():
    device = alphaclops.testing.construct_grid_device(5, 5)
    device_graph = device.metadata.nx_graph
    empty_circuit = alphaclops.Circuit()
    router = alphaclops.RouteCQC(device_graph)
    empty_circuit_routed = router(empty_circuit)

    device.validate_circuit(empty_circuit_routed)
    assert len(list(empty_circuit.all_operations())) == len(
        list(empty_circuit_routed.all_operations())
    )


def test_repr():
    device = alphaclops.testing.construct_ring_device(10)
    device_graph = device.metadata.nx_graph
    router = alphaclops.RouteCQC(device_graph)
    alphaclops.testing.assert_equivalent_repr(router, setup_code='import alphaclops\nimport networkx as nx')
