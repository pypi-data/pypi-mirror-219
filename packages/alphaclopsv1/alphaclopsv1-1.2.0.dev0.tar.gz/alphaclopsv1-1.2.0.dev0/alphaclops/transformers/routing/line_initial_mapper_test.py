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

import networkx as nx
import pytest

import alphaclops


def construct_small_circuit():
    return alphaclops.Circuit(
        [
            alphaclops.Moment(alphaclops.CNOT(alphaclops.NamedQubit('1'), alphaclops.NamedQubit('3'))),
            alphaclops.Moment(alphaclops.CNOT(alphaclops.NamedQubit('2'), alphaclops.NamedQubit('3'))),
            alphaclops.Moment(
                alphaclops.CNOT(alphaclops.NamedQubit('4'), alphaclops.NamedQubit('3')), alphaclops.X(alphaclops.NamedQubit('5'))
            ),
        ]
    )


def construct_step_circuit(k: int):
    q = alphaclops.LineQubit.range(k)
    return alphaclops.Circuit([alphaclops.CNOT(q[i], q[i + 1]) for i in range(k - 1)])


def construct_valid_circuit():
    return alphaclops.Circuit(
        [
            alphaclops.Moment(
                alphaclops.CNOT(alphaclops.NamedQubit('3'), alphaclops.NamedQubit('9')),
                alphaclops.CNOT(alphaclops.NamedQubit('8'), alphaclops.NamedQubit('12')),
            ),
            alphaclops.Moment(
                alphaclops.CNOT(alphaclops.NamedQubit('10'), alphaclops.NamedQubit('11')),
                alphaclops.CNOT(alphaclops.NamedQubit('8'), alphaclops.NamedQubit('12')),
                alphaclops.CNOT(alphaclops.NamedQubit('14'), alphaclops.NamedQubit('6')),
                alphaclops.CNOT(alphaclops.NamedQubit('5'), alphaclops.NamedQubit('4')),
            ),
            alphaclops.Moment(
                alphaclops.CNOT(alphaclops.NamedQubit('8'), alphaclops.NamedQubit('2')),
                alphaclops.CNOT(alphaclops.NamedQubit('3'), alphaclops.NamedQubit('9')),
                alphaclops.CNOT(alphaclops.NamedQubit('6'), alphaclops.NamedQubit('0')),
                alphaclops.CNOT(alphaclops.NamedQubit('14'), alphaclops.NamedQubit('10')),
            ),
            alphaclops.Moment(
                alphaclops.CNOT(alphaclops.NamedQubit('14'), alphaclops.NamedQubit('6')),
                alphaclops.CNOT(alphaclops.NamedQubit('1'), alphaclops.NamedQubit('4')),
            ),
            alphaclops.Moment(
                alphaclops.CNOT(alphaclops.NamedQubit('8'), alphaclops.NamedQubit('12')),
                alphaclops.CNOT(alphaclops.NamedQubit('14'), alphaclops.NamedQubit('10')),
            ),
        ]
    )


def test_valid_circuit():
    # Any circuit with a (full connectivity) graph of disjoint lines should be directly
    # executable after mapping a a supporting device topology without the need for inserting
    # any swaps.
    circuit = construct_valid_circuit()
    device = alphaclops.testing.construct_grid_device(7, 7)
    device_graph = device.metadata.nx_graph
    mapper = alphaclops.LineInitialMapper(device_graph)
    mapping = mapper.initial_mapping(circuit)
    mapped_circuit = circuit.transform_qubits(mapping)
    device.validate_circuit(mapped_circuit)


def test_long_line_on_grid_device():
    # tests
    #   -if strategy is able to map a single long line onto the device whenever the device topology
    #   supports it (i.e. is Hamiltonian)
    #   -if # of physical qubits <= # of logical qubits then strategy should succeed

    step_circuit = construct_step_circuit(49)
    device = alphaclops.testing.construct_grid_device(7, 7)
    device_graph = device.metadata.nx_graph
    mapper = alphaclops.LineInitialMapper(device_graph)
    mapping = mapper.initial_mapping(step_circuit)

    # all qubits in the input circuit are placed on the device
    assert set(mapping.keys()) == set(step_circuit.all_qubits())

    # the induced graph of the device on the physical qubits in the map is connected
    assert nx.is_connected(nx.induced_subgraph(device_graph, mapping.values()))

    # step_circuit s an example of a valid circuit (should not require any swaps after initial
    # mapping)
    device.validate_circuit(step_circuit.transform_qubits(mapping))

    step_circuit = construct_step_circuit(50)
    with pytest.raises(ValueError, match="No available physical qubits left on the device"):
        mapper.initial_mapping(step_circuit)


def test_small_circuit_on_grid_device():
    circuit = construct_small_circuit()
    device_graph = alphaclops.testing.construct_grid_device(7, 7).metadata.nx_graph
    mapper = alphaclops.LineInitialMapper(device_graph)
    mapping = mapper.initial_mapping(circuit)

    assert mapper.center == alphaclops.TensorCircuit(3, 3)

    expected_circuit = alphaclops.Circuit(
        [
            alphaclops.Moment(alphaclops.CNOT(alphaclops.TensorCircuit(1, 3), alphaclops.TensorCircuit(2, 3))),
            alphaclops.Moment(alphaclops.CNOT(alphaclops.TensorCircuit(3, 3), alphaclops.TensorCircuit(2, 3))),
            alphaclops.Moment(
                alphaclops.CNOT(alphaclops.TensorCircuit(2, 2), alphaclops.TensorCircuit(2, 3)), alphaclops.X(alphaclops.TensorCircuit(3, 2))
            ),
        ]
    )
    alphaclops.testing.assert_same_circuits(circuit.transform_qubits(mapping), expected_circuit)


def test_small_circuit_on_ring_device():
    circuit = construct_small_circuit()
    device_graph = alphaclops.testing.construct_ring_device(10, directed=True).metadata.nx_graph

    mapper = alphaclops.LineInitialMapper(device_graph)
    mapping = mapper.initial_mapping(circuit)
    assert mapper.center == alphaclops.LineQubit(0)

    expected_circuit = alphaclops.Circuit(
        [
            alphaclops.Moment(alphaclops.CNOT(alphaclops.LineQubit(2), alphaclops.LineQubit(1))),
            alphaclops.Moment(alphaclops.CNOT(alphaclops.LineQubit(0), alphaclops.LineQubit(1))),
            alphaclops.Moment(alphaclops.CNOT(alphaclops.LineQubit(3), alphaclops.LineQubit(1)), alphaclops.X(alphaclops.LineQubit(4))),
        ]
    )
    alphaclops.testing.assert_same_circuits(circuit.transform_qubits(mapping), expected_circuit)


glob_device_graph = alphaclops.testing.construct_grid_device(7, 7).metadata.nx_graph
glob_mapper = alphaclops.LineInitialMapper(glob_device_graph)


@pytest.mark.parametrize(
    "qubits, n_moments, op_density, random_state",
    [
        (5 * size, 20 * size, density, seed)
        for size in range(1, 3)
        for seed in range(3)
        for density in [0.4, 0.5, 0.6]
    ],
)
def test_random_circuits_grid_device(
    qubits: int, n_moments: int, op_density: float, random_state: int
):
    c_orig = alphaclops.testing.random_circuit(
        qubits=qubits, n_moments=n_moments, op_density=op_density, random_state=random_state
    )
    mapping = glob_mapper.initial_mapping(c_orig)

    assert len(set(mapping.values())) == len(mapping.values())
    assert set(mapping.keys()) == set(c_orig.all_qubits())
    assert nx.is_connected(nx.induced_subgraph(glob_device_graph, mapping.values()))


@pytest.mark.parametrize(
    "qubits, n_moments, op_density, random_state",
    [(30, size, 0.5, seed) for size in [50, 100] for seed in range(2)],
)
def test_large_random_circuits_grid_device(
    qubits: int, n_moments: int, op_density: float, random_state: int
):
    c_orig = alphaclops.testing.random_circuit(
        qubits=qubits, n_moments=n_moments, op_density=op_density, random_state=random_state
    )
    mapping = glob_mapper.initial_mapping(c_orig)

    assert len(set(mapping.values())) == len(mapping.values())
    assert set(mapping.keys()) == set(c_orig.all_qubits())
    assert nx.is_connected(nx.induced_subgraph(glob_device_graph, mapping.values()))


def test_repr():
    device_graph = alphaclops.testing.construct_grid_device(7, 7).metadata.nx_graph
    mapper = alphaclops.LineInitialMapper(device_graph)
    alphaclops.testing.assert_equivalent_repr(mapper, setup_code='import alphaclops\nimport networkx as nx')
