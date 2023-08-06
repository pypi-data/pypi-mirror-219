# Copyright 2020 The alphaclops Developers
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
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple, cast

import networkx as nx
import numpy as np
import pytest

import alphaclops
from alphaclops.experiments import (
    GridInteractionLayer,
    random_rotations_between_grid_interaction_layers_circuit,
)
from alphaclops.experiments.random_quantum_circuit_generation import (
    random_rotations_between_two_qubit_circuit,
    generate_library_of_2q_circuits,
    get_random_combinations_for_device,
    get_random_combinations_for_pairs,
    get_random_combinations_for_layer_circuit,
    get_grid_interaction_layer_circuit,
)

SINGLE_QUBIT_LAYER = Dict[alphaclops.TensorCircuit, Optional[alphaclops.Gate]]


def test_random_rotation_between_two_qubit_circuit():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = random_rotations_between_two_qubit_circuit(q0, q1, 4, seed=52)
    assert len(circuit) == 4 * 2 + 1
    assert circuit.all_qubits() == {q0, q1}

    circuit = random_rotations_between_two_qubit_circuit(
        q0, q1, 4, seed=52, add_final_single_qubit_layer=False
    )
    assert len(circuit) == 4 * 2
    assert circuit.all_qubits() == {q0, q1}

    alphaclops.testing.assert_has_diagram(
        circuit,
        """\
0             1
│             │
Y^0.5         X^0.5
│             │
@─────────────@
│             │
PhX(0.25)^0.5 Y^0.5
│             │
@─────────────@
│             │
Y^0.5         X^0.5
│             │
@─────────────@
│             │
X^0.5         PhX(0.25)^0.5
│             │
@─────────────@
│             │""",
        transpose=True,
    )


def test_generate_library_of_2q_circuits():
    circuits = generate_library_of_2q_circuits(
        n_library_circuits=5, two_qubit_gate=alphaclops.CNOT, max_cycle_depth=13, random_state=9
    )
    assert len(circuits) == 5
    for circuit in circuits:
        assert len(circuit.all_qubits()) == 2
        assert sorted(circuit.all_qubits()) == alphaclops.LineQubit.range(2)
        for m1, m2 in zip(circuit.moments[::2], circuit.moments[1::2]):
            assert len(m1.operations) == 2  # single qubit layer
            assert len(m2.operations) == 1
            assert m2.operations[0].gate == alphaclops.CNOT


def test_generate_library_of_2q_circuits_custom_qubits():
    circuits = generate_library_of_2q_circuits(
        n_library_circuits=5,
        two_qubit_gate=alphaclops.ISWAP ** 0.5,
        max_cycle_depth=13,
        q0=alphaclops.TensorCircuit(9, 9),
        q1=alphaclops.NamedQubit('hi mom'),
        random_state=9,
    )
    assert len(circuits) == 5
    for circuit in circuits:
        assert sorted(circuit.all_qubits()) == [alphaclops.TensorCircuit(9, 9), alphaclops.NamedQubit('hi mom')]
        for m1, m2 in zip(circuit.moments[::2], circuit.moments[1::2]):
            assert len(m1.operations) == 2  # single qubit layer
            assert len(m2.operations) == 1
            assert m2.operations[0].gate == alphaclops.ISWAP ** 0.5


def _gridqubits_to_graph_device(qubits: Iterable[alphaclops.TensorCircuit]):
    # alphaclops contrib: routing.gridqubits_to_graph_device
    def _manhattan_distance(qubit1: alphaclops.TensorCircuit, qubit2: alphaclops.TensorCircuit) -> int:
        return abs(qubit1.row - qubit2.row) + abs(qubit1.col - qubit2.col)

    return nx.Graph(
        pair for pair in itertools.combinations(qubits, 2) if _manhattan_distance(*pair) == 1
    )


def test_get_random_combinations_for_device():
    graph = _gridqubits_to_graph_device(alphaclops.TensorCircuit.rect(3, 3))
    n_combinations = 4
    combinations = get_random_combinations_for_device(
        n_library_circuits=3, n_combinations=n_combinations, device_graph=graph, random_state=99
    )
    assert len(combinations) == 4  # degree-four graph
    for i, comb in enumerate(combinations):
        assert comb.combinations.shape[0] == n_combinations
        assert comb.combinations.shape[1] == len(comb.pairs)
        assert np.all(comb.combinations >= 0)
        assert np.all(comb.combinations < 3)  # number of library circuits
        for q0, q1 in comb.pairs:
            assert q0 in alphaclops.TensorCircuit.rect(3, 3)
            assert q1 in alphaclops.TensorCircuit.rect(3, 3)

        assert alphaclops.experiments.HALF_GRID_STAGGERED_PATTERN[i] == comb.layer


def test_get_random_combinations_for_small_device():
    graph = _gridqubits_to_graph_device(alphaclops.TensorCircuit.rect(3, 1))
    n_combinations = 4
    combinations = get_random_combinations_for_device(
        n_library_circuits=3, n_combinations=n_combinations, device_graph=graph, random_state=99
    )
    assert len(combinations) == 2  # 3x1 device only fits two layers


def test_get_random_combinations_for_pairs():
    all_pairs = [
        [(alphaclops.LineQubit(0), alphaclops.LineQubit(1)), (alphaclops.LineQubit(2), alphaclops.LineQubit(3))],
        [(alphaclops.LineQubit(1), alphaclops.LineQubit(2))],
    ]
    combinations = get_random_combinations_for_pairs(
        n_library_circuits=3, n_combinations=4, all_pairs=all_pairs, random_state=99
    )
    assert len(combinations) == len(all_pairs)
    for i, comb in enumerate(combinations):
        assert comb.combinations.shape[0] == 4  # n_combinations
        assert comb.combinations.shape[1] == len(comb.pairs)
        assert np.all(comb.combinations >= 0)
        assert np.all(comb.combinations < 3)  # number of library circuits
        for q0, q1 in comb.pairs:
            assert q0 in alphaclops.LineQubit.range(4)
            assert q1 in alphaclops.LineQubit.range(4)

        assert comb.layer is None
        assert comb.pairs == all_pairs[i]


def test_get_random_combinations_for_layer_circuit():
    q0, q1, q2, q3 = alphaclops.LineQubit.range(4)
    circuit = alphaclops.Circuit(alphaclops.CNOT(q0, q1), alphaclops.CNOT(q2, q3), alphaclops.CNOT(q1, q2))
    combinations = get_random_combinations_for_layer_circuit(
        n_library_circuits=3, n_combinations=4, layer_circuit=circuit, random_state=99
    )
    assert len(combinations) == 2  # operations pack into two layers
    for i, comb in enumerate(combinations):
        assert comb.combinations.shape[0] == 4  # n_combinations
        assert comb.combinations.shape[1] == len(comb.pairs)
        assert np.all(comb.combinations >= 0)
        assert np.all(comb.combinations < 3)  # number of library circuits
        for q0, q1 in comb.pairs:
            assert q0 in alphaclops.LineQubit.range(4)
            assert q1 in alphaclops.LineQubit.range(4)

        assert comb.layer == circuit.moments[i]


def test_get_random_combinations_for_bad_layer_circuit():
    q0, q1, q2, q3 = alphaclops.LineQubit.range(4)
    circuit = alphaclops.Circuit(
        alphaclops.H.on_each(q0, q1, q2, q3), alphaclops.CNOT(q0, q1), alphaclops.CNOT(q2, q3), alphaclops.CNOT(q1, q2)
    )

    with pytest.raises(ValueError, match=r'non-2-qubit operation'):
        _ = get_random_combinations_for_layer_circuit(
            n_library_circuits=3, n_combinations=4, layer_circuit=circuit, random_state=99
        )


def test_get_grid_interaction_layer_circuit():
    graph = _gridqubits_to_graph_device(alphaclops.TensorCircuit.rect(3, 3))
    layer_circuit = get_grid_interaction_layer_circuit(graph)

    sqrtisw = alphaclops.ISWAP ** 0.5
    gq = alphaclops.TensorCircuit
    should_be = alphaclops.Circuit(
        # Vertical
        sqrtisw(gq(0, 0), gq(1, 0)),
        sqrtisw(gq(1, 1), gq(2, 1)),
        sqrtisw(gq(0, 2), gq(1, 2)),
        # Vertical, offset
        sqrtisw(gq(0, 1), gq(1, 1)),
        sqrtisw(gq(1, 2), gq(2, 2)),
        sqrtisw(gq(1, 0), gq(2, 0)),
        # Horizontal, offset
        sqrtisw(gq(0, 1), gq(0, 2)),
        sqrtisw(gq(1, 0), gq(1, 1)),
        sqrtisw(gq(2, 1), gq(2, 2)),
        # Horizontal
        sqrtisw(gq(0, 0), gq(0, 1)),
        sqrtisw(gq(1, 1), gq(1, 2)),
        sqrtisw(gq(2, 0), gq(2, 1)),
    )
    assert layer_circuit == should_be


def test_random_combinations_layer_circuit_vs_device():
    # Random combinations from layer circuit is the same as getting it directly from graph
    graph = _gridqubits_to_graph_device(alphaclops.TensorCircuit.rect(3, 3))
    layer_circuit = get_grid_interaction_layer_circuit(graph)
    combs1 = get_random_combinations_for_layer_circuit(
        n_library_circuits=10, n_combinations=10, layer_circuit=layer_circuit, random_state=1
    )
    combs2 = get_random_combinations_for_device(
        n_library_circuits=10, n_combinations=10, device_graph=graph, random_state=1
    )
    for comb1, comb2 in zip(combs1, combs2):
        assert comb1.pairs == comb2.pairs
        assert np.all(comb1.combinations == comb2.combinations)


def _cz_with_adjacent_z_rotations(
    a: alphaclops.TensorCircuit, b: alphaclops.TensorCircuit, prng: np.random.RandomState
):
    z_exponents = [prng.uniform(0, 1) for _ in range(4)]
    yield alphaclops.Z(a) ** z_exponents[0]
    yield alphaclops.Z(b) ** z_exponents[1]
    yield alphaclops.CZ(a, b)
    yield alphaclops.Z(a) ** z_exponents[2]
    yield alphaclops.Z(b) ** z_exponents[3]


class FakeSycamoreGate(alphaclops.FSimGate):
    def __init__(self):
        super().__init__(theta=np.pi / 2, phi=np.pi / 6)


@pytest.mark.parametrize(
    'qubits, depth, two_qubit_op_factory, pattern, '
    'single_qubit_gates, add_final_single_qubit_layer, '
    'seed, expected_circuit_length, single_qubit_layers_slice, '
    'two_qubit_layers_slice',
    (
        (
                alphaclops.TensorCircuit.rect(4, 3),
                20,
                lambda a, b, _: alphaclops.CZ(a, b),
                alphaclops.experiments.GRID_STAGGERED_PATTERN,
                (alphaclops.X ** 0.5, alphaclops.Y ** 0.5, alphaclops.Z ** 0.5),
                True,
                1234,
                41,
                slice(None, None, 2),
                slice(1, None, 2),
        ),
        (
                alphaclops.TensorCircuit.rect(4, 3),
                20,
                lambda a, b, _: FakeSycamoreGate()(a, b),
                alphaclops.experiments.HALF_GRID_STAGGERED_PATTERN,
                (alphaclops.X ** 0.5, alphaclops.Y ** 0.5, alphaclops.Z ** 0.5),
                True,
                1234,
                41,
                slice(None, None, 2),
                slice(1, None, 2),
        ),
        (
                alphaclops.TensorCircuit.rect(4, 5),
                21,
                lambda a, b, _: alphaclops.CZ(a, b),
                alphaclops.experiments.GRID_ALIGNED_PATTERN,
                (alphaclops.X ** 0.5, alphaclops.Y ** 0.5, alphaclops.Z ** 0.5),
                True,
                1234,
                43,
                slice(None, None, 2),
                slice(1, None, 2),
        ),
        (
                alphaclops.TensorCircuit.rect(5, 4),
                22,
                _cz_with_adjacent_z_rotations,
                alphaclops.experiments.GRID_STAGGERED_PATTERN,
                (alphaclops.X ** 0.5, alphaclops.Y ** 0.5, alphaclops.Z ** 0.5),
                True,
                1234,
                89,
                slice(None, None, 4),
                slice(2, None, 4),
        ),
        (
                alphaclops.TensorCircuit.rect(5, 5),
                23,
                lambda a, b, _: alphaclops.CZ(a, b),
                alphaclops.experiments.GRID_ALIGNED_PATTERN,
                (alphaclops.X ** 0.5, alphaclops.Y ** 0.5, alphaclops.Z ** 0.5),
                False,
                1234,
                46,
                slice(None, None, 2),
                slice(1, None, 2),
        ),
        (
                alphaclops.TensorCircuit.rect(5, 5),
                24,
                lambda a, b, _: alphaclops.CZ(a, b),
                alphaclops.experiments.GRID_ALIGNED_PATTERN,
                (alphaclops.X ** 0.5, alphaclops.X ** 0.5),
                True,
                1234,
                49,
                slice(None, None, 2),
                slice(1, None, 2),
        ),
    ),
)
def test_random_rotations_between_grid_interaction_layers(
    qubits: Iterable[alphaclops.TensorCircuit],
    depth: int,
    two_qubit_op_factory: Callable[
        [alphaclops.TensorCircuit, alphaclops.TensorCircuit, np.random.RandomState], alphaclops.OP_TREE
    ],
    pattern: Sequence[GridInteractionLayer],
    single_qubit_gates: Sequence[alphaclops.Gate],
    add_final_single_qubit_layer: bool,
    seed: 'alphaclops.RANDOM_STATE_OR_SEED_LIKE',
    expected_circuit_length: int,
    single_qubit_layers_slice: slice,
    two_qubit_layers_slice: slice,
):
    qubits = set(qubits)
    circuit = random_rotations_between_grid_interaction_layers_circuit(
        qubits,
        depth,
        two_qubit_op_factory=two_qubit_op_factory,
        pattern=pattern,
        single_qubit_gates=single_qubit_gates,
        add_final_single_qubit_layer=add_final_single_qubit_layer,
        seed=seed,
    )

    assert len(circuit) == expected_circuit_length
    _validate_single_qubit_layers(
        qubits,
        cast(Sequence[alphaclops.Moment], circuit[single_qubit_layers_slice]),
        non_repeating_layers=len(set(single_qubit_gates)) > 1,
    )
    _validate_two_qubit_layers(
        qubits, cast(Sequence[alphaclops.Moment], circuit[two_qubit_layers_slice]), pattern
    )


def test_grid_interaction_layer_repr():
    layer = GridInteractionLayer(col_offset=0, vertical=True, stagger=False)
    assert repr(layer) == (
        'alphaclops.experiments.GridInteractionLayer(col_offset=0, vertical=True, stagger=False)'
    )


def _validate_single_qubit_layers(
    qubits: Set[alphaclops.TensorCircuit], moments: Sequence[alphaclops.Moment], non_repeating_layers: bool = True
) -> None:
    previous_single_qubit_gates: SINGLE_QUBIT_LAYER = {q: None for q in qubits}

    for moment in moments:
        # All qubits are acted upon
        assert moment.qubits == qubits
        for op in moment:
            # Operation is single-qubit
            assert alphaclops.num_qubits(op) == 1
            if non_repeating_layers:
                # Gate differs from previous single-qubit gate on this qubit
                q = cast(alphaclops.TensorCircuit, op.qubits[0])
                assert op.gate != previous_single_qubit_gates[q]
                previous_single_qubit_gates[q] = op.gate


def _validate_two_qubit_layers(
    qubits: Set[alphaclops.TensorCircuit],
    moments: Sequence[alphaclops.Moment],
    pattern: Sequence[alphaclops.experiments.GridInteractionLayer],
) -> None:
    coupled_qubit_pairs = _coupled_qubit_pairs(qubits)
    for i, moment in enumerate(moments):
        active_pairs = set()
        for op in moment:
            # Operation is two-qubit
            assert alphaclops.num_qubits(op) == 2
            # Operation fits pattern
            assert op.qubits in pattern[i % len(pattern)]
            active_pairs.add(op.qubits)
        # All interactions that should be in this layer are present
        assert all(
            pair in active_pairs
            for pair in coupled_qubit_pairs
            if pair in pattern[i % len(pattern)]
        )


def _coupled_qubit_pairs(
    qubits: Set['alphaclops.TensorCircuit'],
) -> List[Tuple['alphaclops.TensorCircuit', 'alphaclops.TensorCircuit']]:
    pairs = []
    for qubit in qubits:

        def add_pair(neighbor: 'alphaclops.TensorCircuit'):
            if neighbor in qubits:
                pairs.append((qubit, neighbor))

        add_pair(alphaclops.TensorCircuit(qubit.row, qubit.col + 1))
        add_pair(alphaclops.TensorCircuit(qubit.row + 1, qubit.col))

    return pairs
