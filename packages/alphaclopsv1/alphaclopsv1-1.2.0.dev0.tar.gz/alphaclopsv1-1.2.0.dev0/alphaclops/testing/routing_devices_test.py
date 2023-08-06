# Copyright 2021 The alphaclops Developers
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
import pytest
import networkx as nx
import alphaclops


def test_grid_device():
    rect_device = alphaclops.testing.construct_grid_device(5, 7)
    rect_device_graph = rect_device.metadata.nx_graph
    isomorphism_class = nx.Graph()
    row_edges = [
        (alphaclops.TensorCircuit(i, j), alphaclops.TensorCircuit(i, j + 1)) for i in range(5) for j in range(6)
    ]
    col_edges = [
        (alphaclops.TensorCircuit(i, j), alphaclops.TensorCircuit(i + 1, j)) for j in range(7) for i in range(4)
    ]
    isomorphism_class.add_edges_from(row_edges)
    isomorphism_class.add_edges_from(col_edges)
    assert all(q in rect_device_graph.nodes for q in alphaclops.TensorCircuit.rect(5, 7))
    assert nx.is_isomorphic(isomorphism_class, rect_device_graph)


def test_grid_op_validation():
    device = alphaclops.testing.construct_grid_device(5, 7)

    with pytest.raises(ValueError, match="Qubits not on device"):
        device.validate_operation(alphaclops.X(alphaclops.NamedQubit("a")))
    with pytest.raises(ValueError, match="Qubits not on device"):
        device.validate_operation(alphaclops.CNOT(alphaclops.NamedQubit("a"), alphaclops.TensorCircuit(0, 0)))
    with pytest.raises(ValueError, match="Qubits not on device"):
        device.validate_operation(alphaclops.CNOT(alphaclops.TensorCircuit(5, 4), alphaclops.TensorCircuit(4, 4)))
    with pytest.raises(ValueError, match="Qubits not on device"):
        device.validate_operation(alphaclops.CNOT(alphaclops.TensorCircuit(4, 7), alphaclops.TensorCircuit(4, 6)))

    with pytest.raises(ValueError, match="Qubit pair is not a valid edge on device"):
        device.validate_operation(alphaclops.CNOT(alphaclops.TensorCircuit(0, 0), alphaclops.TensorCircuit(0, 2)))
    with pytest.raises(ValueError, match="Qubit pair is not a valid edge on device"):
        device.validate_operation(alphaclops.CNOT(alphaclops.TensorCircuit(2, 0), alphaclops.TensorCircuit(0, 0)))

    device.validate_operation(alphaclops.CNOT(alphaclops.TensorCircuit(0, 0), alphaclops.TensorCircuit(0, 1)))
    device.validate_operation(alphaclops.CNOT(alphaclops.TensorCircuit(0, 1), alphaclops.TensorCircuit(0, 0)))
    device.validate_operation(alphaclops.CNOT(alphaclops.TensorCircuit(1, 0), alphaclops.TensorCircuit(0, 0)))
    device.validate_operation(alphaclops.CNOT(alphaclops.TensorCircuit(0, 0), alphaclops.TensorCircuit(1, 0)))


def test_ring_device():
    undirected_device = alphaclops.testing.construct_ring_device(5)
    undirected_device_graph = undirected_device.metadata.nx_graph
    assert all(q in undirected_device_graph.nodes for q in alphaclops.LineQubit.range(5))
    isomorphism_class = nx.Graph()
    edges = [(alphaclops.LineQubit(i % 5), alphaclops.LineQubit((i + 1) % 5)) for i in range(5)]
    isomorphism_class.add_edges_from(edges)
    assert nx.is_isomorphic(isomorphism_class, undirected_device_graph)

    directed_device = alphaclops.testing.construct_ring_device(5, directed=True)
    directed_device_graph = directed_device.metadata.nx_graph
    assert all(q in directed_device_graph.nodes for q in alphaclops.LineQubit.range(5))
    isomorphism_class = nx.DiGraph()
    edges = [(alphaclops.LineQubit(i % 5), alphaclops.LineQubit((i + 1) % 5)) for i in range(5)]
    isomorphism_class.add_edges_from(edges)
    assert nx.is_isomorphic(isomorphism_class, directed_device_graph)


def test_ring_op_validation():
    directed_device = alphaclops.testing.construct_ring_device(5, directed=True)
    undirected_device = alphaclops.testing.construct_ring_device(5, directed=False)

    with pytest.raises(ValueError, match="Qubits not on device"):
        directed_device.validate_operation(alphaclops.X(alphaclops.LineQubit(5)))
    with pytest.raises(ValueError, match="Qubits not on device"):
        undirected_device.validate_operation(alphaclops.X(alphaclops.LineQubit(5)))

    with pytest.raises(ValueError, match="Qubit pair is not a valid edge on device"):
        undirected_device.validate_operation(alphaclops.CNOT(alphaclops.LineQubit(0), alphaclops.LineQubit(2)))
    with pytest.raises(ValueError, match="Qubit pair is not a valid edge on device"):
        directed_device.validate_operation(alphaclops.CNOT(alphaclops.LineQubit(1), alphaclops.LineQubit(0)))

    undirected_device.validate_operation(alphaclops.CNOT(alphaclops.LineQubit(0), alphaclops.LineQubit(1)))
    undirected_device.validate_operation(alphaclops.CNOT(alphaclops.LineQubit(1), alphaclops.LineQubit(0)))
    directed_device.validate_operation(alphaclops.CNOT(alphaclops.LineQubit(0), alphaclops.LineQubit(1)))


def test_allowed_multi_qubit_gates():
    device = alphaclops.testing.construct_ring_device(5)

    device.validate_operation(alphaclops.MeasurementGate(1).on(alphaclops.LineQubit(0)))
    device.validate_operation(alphaclops.MeasurementGate(2).on(*alphaclops.LineQubit.range(2)))
    device.validate_operation(alphaclops.MeasurementGate(3).on(*alphaclops.LineQubit.range(3)))

    with pytest.raises(ValueError, match="Unsupported operation"):
        device.validate_operation(alphaclops.CCNOT(*alphaclops.LineQubit.range(3)))

    device.validate_operation(alphaclops.CNOT(*alphaclops.LineQubit.range(2)))


def test_namedqubit_device():
    # 4-star graph
    nx_graph = nx.Graph([("a", "b"), ("a", "c"), ("a", "d")])

    device = alphaclops.testing.RoutingTestingDevice(nx_graph)
    relabeled_graph = device.metadata.nx_graph
    qubit_set = {alphaclops.NamedQubit(n) for n in "abcd"}
    assert set(relabeled_graph.nodes) == qubit_set
    assert nx.is_isomorphic(nx_graph, relabeled_graph)
