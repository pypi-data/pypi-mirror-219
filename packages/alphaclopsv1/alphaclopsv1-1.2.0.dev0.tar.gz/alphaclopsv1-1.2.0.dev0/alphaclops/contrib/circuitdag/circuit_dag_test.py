# Copyright 2018 The alphaclops Developers
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

import itertools
import random

import pytest
import networkx

import alphaclops


class FakeDevice(alphaclops.Device):
    pass


def test_wrapper_eq():
    q0, q1 = alphaclops.LineQubit.range(2)
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(alphaclops.contrib.CircuitDag.make_node(alphaclops.X(q0)))
    eq.add_equality_group(alphaclops.contrib.CircuitDag.make_node(alphaclops.X(q0)))
    eq.add_equality_group(alphaclops.contrib.CircuitDag.make_node(alphaclops.Y(q0)))
    eq.add_equality_group(alphaclops.contrib.CircuitDag.make_node(alphaclops.X(q1)))


def test_wrapper_cmp():
    u0 = alphaclops.contrib.Unique(0)
    u1 = alphaclops.contrib.Unique(1)
    # The ordering of Unique instances is unpredictable
    u0, u1 = (u1, u0) if u1 < u0 else (u0, u1)
    assert u0 == u0
    assert u0 != u1
    assert u0 < u1
    assert u1 > u0
    assert u0 <= u0
    assert u0 <= u1
    assert u0 >= u0
    assert u1 >= u0


def test_wrapper_cmp_failure():
    with pytest.raises(TypeError):
        _ = object() < alphaclops.contrib.Unique(1)
    with pytest.raises(TypeError):
        _ = alphaclops.contrib.Unique(1) < object()


def test_wrapper_repr():
    q0 = alphaclops.LineQubit(0)

    node = alphaclops.contrib.CircuitDag.make_node(alphaclops.X(q0))
    expected = f'alphaclops.contrib.Unique({id(node)}, alphaclops.X(alphaclops.LineQubit(0)))'
    assert repr(node) == expected


def test_init():
    dag = alphaclops.contrib.CircuitDag()
    assert networkx.dag.is_directed_acyclic_graph(dag)
    assert list(dag.nodes()) == []
    assert list(dag.edges()) == []


def test_append():
    q0 = alphaclops.LineQubit(0)
    dag = alphaclops.contrib.CircuitDag()
    dag.append(alphaclops.X(q0))
    dag.append(alphaclops.Y(q0))
    assert networkx.dag.is_directed_acyclic_graph(dag)
    assert len(dag.nodes()) == 2
    assert [(n1.val, n2.val) for n1, n2 in dag.edges()] == [(alphaclops.X(q0), alphaclops.Y(q0))]


def test_two_identical_ops():
    q0 = alphaclops.LineQubit(0)
    dag = alphaclops.contrib.CircuitDag()
    dag.append(alphaclops.X(q0))
    dag.append(alphaclops.Y(q0))
    dag.append(alphaclops.X(q0))
    assert networkx.dag.is_directed_acyclic_graph(dag)
    assert len(dag.nodes()) == 3
    assert set((n1.val, n2.val) for n1, n2 in dag.edges()) == {
        (alphaclops.X(q0), alphaclops.Y(q0)),
        (alphaclops.X(q0), alphaclops.X(q0)),
        (alphaclops.Y(q0), alphaclops.X(q0)),
    }


def test_from_ops():
    q0 = alphaclops.LineQubit(0)
    dag = alphaclops.contrib.CircuitDag.from_ops(alphaclops.X(q0), alphaclops.Y(q0))
    assert networkx.dag.is_directed_acyclic_graph(dag)
    assert len(dag.nodes()) == 2
    assert [(n1.val, n2.val) for n1, n2 in dag.edges()] == [(alphaclops.X(q0), alphaclops.Y(q0))]


def test_from_circuit():
    q0 = alphaclops.LineQubit(0)
    circuit = alphaclops.Circuit(alphaclops.X(q0), alphaclops.Y(q0))
    dag = alphaclops.contrib.CircuitDag.from_circuit(circuit)
    assert networkx.dag.is_directed_acyclic_graph(dag)
    assert len(dag.nodes()) == 2
    assert [(n1.val, n2.val) for n1, n2 in dag.edges()] == [(alphaclops.X(q0), alphaclops.Y(q0))]
    assert sorted(circuit.all_qubits()) == sorted(dag.all_qubits())


def test_to_empty_circuit():
    circuit = alphaclops.Circuit()
    dag = alphaclops.contrib.CircuitDag.from_circuit(circuit)
    assert networkx.dag.is_directed_acyclic_graph(dag)
    assert circuit == dag.to_circuit()


def test_to_circuit():
    q0 = alphaclops.LineQubit(0)
    circuit = alphaclops.Circuit(alphaclops.X(q0), alphaclops.Y(q0))
    dag = alphaclops.contrib.CircuitDag.from_circuit(circuit)

    assert networkx.dag.is_directed_acyclic_graph(dag)
    # Only one possible output circuit for this simple case
    assert circuit == dag.to_circuit()

    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit.unitary(), dag.to_circuit().unitary(), atol=1e-7
    )


def test_equality():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit1 = alphaclops.Circuit(
        alphaclops.X(q0), alphaclops.Y(q0), alphaclops.Z(q1), alphaclops.CZ(q0, q1), alphaclops.X(q1), alphaclops.Y(q1), alphaclops.Z(q0)
    )
    circuit2 = alphaclops.Circuit(
        alphaclops.Z(q1), alphaclops.X(q0), alphaclops.Y(q0), alphaclops.CZ(q0, q1), alphaclops.Z(q0), alphaclops.X(q1), alphaclops.Y(q1)
    )
    circuit3 = alphaclops.Circuit(
        alphaclops.X(q0),
        alphaclops.Y(q0),
        alphaclops.Z(q1),
        alphaclops.CZ(q0, q1),
        alphaclops.X(q1),
        alphaclops.Y(q1),
        alphaclops.Z(q0) ** 0.5,
    )
    circuit4 = alphaclops.Circuit(
        alphaclops.X(q0), alphaclops.Y(q0), alphaclops.Z(q1), alphaclops.CZ(q0, q1), alphaclops.X(q1), alphaclops.Y(q1)
    )

    eq = alphaclops.testing.EqualsTester()
    eq.make_equality_group(
        lambda: alphaclops.contrib.CircuitDag.from_circuit(circuit1),
        lambda: alphaclops.contrib.CircuitDag.from_circuit(circuit2),
    )
    eq.add_equality_group(alphaclops.contrib.CircuitDag.from_circuit(circuit3))
    eq.add_equality_group(alphaclops.contrib.CircuitDag.from_circuit(circuit4))


def test_larger_circuit():
    q0, q1, q2, q3 = [
        alphaclops.TensorCircuit(0, 5),
        alphaclops.TensorCircuit(1, 5),
        alphaclops.TensorCircuit(2, 5),
        alphaclops.TensorCircuit(3, 5),
    ]
    # This circuit does not have CZ gates on adjacent qubits because the order
    # dag.to_circuit() would append them is non-deterministic.
    circuit = alphaclops.Circuit(
        alphaclops.X(q0),
        alphaclops.CZ(q1, q2),
        alphaclops.CZ(q0, q1),
        alphaclops.Y(q0),
        alphaclops.Z(q0),
        alphaclops.CZ(q1, q2),
        alphaclops.X(q0),
        alphaclops.Y(q0),
        alphaclops.CZ(q0, q1),
        alphaclops.T(q3),
        strategy=alphaclops.InsertStrategy.EARLIEST,
    )

    dag = alphaclops.contrib.CircuitDag.from_circuit(circuit)

    assert networkx.dag.is_directed_acyclic_graph(dag)
    # Operation order within a moment is non-deterministic
    # but text diagrams still look the same.
    desired = """
(0, 5): ───X───@───Y───Z───X───Y───@───
               │                   │
(1, 5): ───@───@───@───────────────@───
           │       │
(2, 5): ───@───────@───────────────────

(3, 5): ───T───────────────────────────
"""
    alphaclops.testing.assert_has_diagram(circuit, desired)
    alphaclops.testing.assert_has_diagram(dag.to_circuit(), desired)

    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit.unitary(), dag.to_circuit().unitary(), atol=1e-7
    )


@pytest.mark.parametrize('circuit', [alphaclops.testing.random_circuit(10, 10, 0.5) for _ in range(3)])
def test_is_maximalist(circuit):
    dag = alphaclops.contrib.CircuitDag.from_circuit(circuit)
    transitive_closure = networkx.dag.transitive_closure(dag)
    assert alphaclops.contrib.CircuitDag(incoming_graph_data=transitive_closure) == dag
    assert not any(dag.has_edge(b, a) for a, b in itertools.combinations(dag.ordered_nodes(), 2))


def _get_circuits_and_is_blockers():
    qubits = alphaclops.LineQubit.range(10)
    circuits = [alphaclops.testing.random_circuit(qubits, 10, 0.5) for _ in range(1)]
    edges = [
        set(qubit_pair) for qubit_pair in itertools.combinations(qubits, 2) if random.random() > 0.5
    ]
    not_on_edge = lambda op: len(op.qubits) > 1 and set(op.qubits) not in edges
    is_blockers = [lambda op: False, not_on_edge]
    return itertools.product(circuits, is_blockers)


@pytest.mark.parametrize('circuit, is_blocker', _get_circuits_and_is_blockers())
def test_findall_nodes_until_blocked(circuit, is_blocker):
    dag = alphaclops.contrib.CircuitDag.from_circuit(circuit)
    all_nodes = list(dag.ordered_nodes())
    found_nodes = list(dag.findall_nodes_until_blocked(is_blocker))
    assert not any(dag.has_edge(b, a) for a, b in itertools.combinations(found_nodes, 2))

    blocking_nodes = set(node for node in all_nodes if is_blocker(node.val))
    blocked_nodes = blocking_nodes.union(*(dag.succ[node] for node in blocking_nodes))
    expected_nodes = set(all_nodes) - blocked_nodes
    assert sorted(found_nodes) == sorted(expected_nodes)
