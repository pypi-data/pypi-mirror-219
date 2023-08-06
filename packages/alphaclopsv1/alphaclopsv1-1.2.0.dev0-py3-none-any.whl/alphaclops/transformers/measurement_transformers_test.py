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

import numpy as np
import pytest
import sympy
from sympy.parsing import sympy_parser

import alphaclops
from alphaclops.transformers.measurement_transformers import _ConfusionChannel, _MeasurementQid, _mod_add


def assert_equivalent_to_deferred(circuit: alphaclops.Circuit):
    qubits = list(circuit.all_qubits())
    sim = alphaclops.Simulator()
    num_qubits = len(qubits)
    dimensions = [q.dimension for q in qubits]
    for i in range(np.prod(dimensions)):
        bits = alphaclops.big_endian_int_to_digits(i, base=dimensions)
        modified = alphaclops.Circuit()
        for j in range(num_qubits):
            modified.append(alphaclops.XPowGate(dimension=qubits[j].dimension)(qubits[j]) ** bits[j])
        modified.append(circuit)
        deferred = alphaclops.defer_measurements(modified)
        result = sim.simulate(modified)
        result1 = sim.simulate(deferred)
        np.testing.assert_equal(result.measurements, result1.measurements)


def test_basic():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.X(q1).with_classical_controls('a'),
        alphaclops.measure(q1, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_ma),
            alphaclops.CX(q_ma, q1),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q1, key='b'),
        ),
    )


def test_qudits():
    q0, q1 = alphaclops.LineQid.range(2, dimension=3)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.XPowGate(dimension=3).on(q1).with_classical_controls('a'),
        alphaclops.measure(q1, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            _mod_add(q0, q_ma),
            alphaclops.XPowGate(dimension=3).on(q1).controlled_by(q_ma, control_values=[[1, 2]]),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q1, key='b'),
        ),
    )


def test_sympy_control():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.X(q1).with_classical_controls(sympy.Symbol('a')),
        alphaclops.measure(q1, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_ma),
            alphaclops.CX(q_ma, q1),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q1, key='b'),
        ),
    )


def test_sympy_qudits():
    q0, q1 = alphaclops.LineQid.range(2, dimension=3)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.XPowGate(dimension=3).on(q1).with_classical_controls(sympy.Symbol('a')),
        alphaclops.measure(q1, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            _mod_add(q0, q_ma),
            alphaclops.XPowGate(dimension=3).on(q1).controlled_by(q_ma, control_values=[[1, 2]]),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q1, key='b'),
        ),
    )


def test_sympy_control_complex():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.measure(q1, key='b'),
        alphaclops.X(q2).with_classical_controls(sympy_parser.parse_expr('a >= b')),
        alphaclops.measure(q2, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    q_mb = _MeasurementQid('b', q1)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_ma),
            alphaclops.CX(q1, q_mb),
            alphaclops.ControlledOperation(
                [q_ma, q_mb], alphaclops.X(q2), alphaclops.SumOfProducts([[0, 0], [1, 0], [1, 1]])
            ),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q_mb, key='b'),
            alphaclops.measure(q2, key='c'),
        ),
    )


def test_sympy_control_complex_qudit():
    q0, q1, q2 = alphaclops.LineQid.for_qid_shape((4, 2, 2))
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.measure(q1, key='b'),
        alphaclops.X(q2).with_classical_controls(sympy_parser.parse_expr('a > b')),
        alphaclops.measure(q2, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    q_mb = _MeasurementQid('b', q1)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            _mod_add(q0, q_ma),
            alphaclops.CX(q1, q_mb),
            alphaclops.ControlledOperation(
                [q_ma, q_mb],
                alphaclops.X(q2),
                alphaclops.SumOfProducts([[1, 0], [2, 0], [3, 0], [2, 1], [3, 1]]),
            ),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q_mb, key='b'),
            alphaclops.measure(q2, key='c'),
        ),
    )


def test_multiple_sympy_control_complex():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.measure(q1, key='b'),
        alphaclops.X(q2)
        .with_classical_controls(sympy_parser.parse_expr('a >= b'))
        .with_classical_controls(sympy_parser.parse_expr('a <= b')),
        alphaclops.measure(q2, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    q_mb = _MeasurementQid('b', q1)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_ma),
            alphaclops.CX(q1, q_mb),
            alphaclops.ControlledOperation(
                [q_ma, q_mb], alphaclops.X(q2), alphaclops.SumOfProducts([[0, 0], [1, 1]])
            ),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q_mb, key='b'),
            alphaclops.measure(q2, key='c'),
        ),
    )


def test_sympy_and_key_control():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.X(q1).with_classical_controls(sympy.Symbol('a')).with_classical_controls('a'),
        alphaclops.measure(q1, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_ma),
            alphaclops.CX(q_ma, q1),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q1, key='b'),
        ),
    )


def test_sympy_control_multiqubit():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, q1, key='a'),
        alphaclops.X(q2).with_classical_controls(sympy_parser.parse_expr('a >= 2')),
        alphaclops.measure(q2, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma0 = _MeasurementQid('a', q0)
    q_ma1 = _MeasurementQid('a', q1)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_ma0),
            alphaclops.CX(q1, q_ma1),
            alphaclops.ControlledOperation(
                [q_ma0, q_ma1], alphaclops.X(q2), alphaclops.SumOfProducts([[1, 0], [1, 1]])
            ),
            alphaclops.measure(q_ma0, q_ma1, key='a'),
            alphaclops.measure(q2, key='c'),
        ),
    )


def test_nocompile_context():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a').with_tags('nocompile'),
        alphaclops.X(q1).with_classical_controls('a').with_tags('nocompile'),
        alphaclops.measure(q1, key='b'),
    )
    deferred = alphaclops.defer_measurements(
        circuit, context=alphaclops.TransformerContext(tags_to_ignore=('nocompile',))
    )
    alphaclops.testing.assert_same_circuits(deferred, circuit)


def test_nocompile_context_leaves_invalid_circuit():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a').with_tags('nocompile'),
        alphaclops.X(q1).with_classical_controls('a'),
        alphaclops.measure(q1, key='b'),
    )
    with pytest.raises(ValueError, match='Deferred measurement for key=a not found'):
        _ = alphaclops.defer_measurements(
            circuit, context=alphaclops.TransformerContext(tags_to_ignore=('nocompile',))
        )


def test_pauli():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.PauliMeasurementGate(alphaclops.DensePauliString('Y'), key='a').on(q0),
        alphaclops.X(q1).with_classical_controls('a'),
        alphaclops.measure(q1, key='b'),
    )
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    alphaclops.testing.assert_same_circuits(
        alphaclops.unroll_circuit_op(deferred),
        alphaclops.Circuit(
            alphaclops.SingleQubitCliffordGate.X_sqrt(q0),
            alphaclops.CX(q0, q_ma),
            (alphaclops.SingleQubitCliffordGate.X_sqrt(q0) ** -1),
            alphaclops.Moment(alphaclops.CX(q_ma, q1)),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q1, key='b'),
        ),
    )


def test_extra_measurements():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.measure(q0, key='b'),
        alphaclops.X(q1).with_classical_controls('a'),
        alphaclops.measure(q1, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_ma),
            alphaclops.CX(q_ma, q1),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q0, key='b'),
            alphaclops.measure(q1, key='c'),
        ),
    )


def test_extra_controlled_bits():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.CX(q0, q1).with_classical_controls('a'),
        alphaclops.measure(q1, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_ma),
            alphaclops.CCX(q_ma, q0, q1),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q1, key='b'),
        ),
    )


def test_extra_control_bits():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.measure(q0, key='b'),
        alphaclops.X(q1).with_classical_controls('a', 'b'),
        alphaclops.measure(q1, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)
    q_mb = _MeasurementQid('b', q0)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_ma),
            alphaclops.CX(q0, q_mb),
            alphaclops.CCX(q_ma, q_mb, q1),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q_mb, key='b'),
            alphaclops.measure(q1, key='c'),
        ),
    )


def test_subcircuit():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                alphaclops.measure(q0, key='a'),
                alphaclops.X(q1).with_classical_controls('a'),
                alphaclops.measure(q1, key='b'),
            )
        )
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_m = _MeasurementQid('a', q0)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_m),
            alphaclops.CX(q_m, q1),
            alphaclops.measure(q_m, key='a'),
            alphaclops.measure(q1, key='b'),
        ),
    )


def test_multi_qubit_measurements():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, q1, key='a'),
        alphaclops.X(q0),
        alphaclops.measure(q0, key='b'),
        alphaclops.measure(q1, key='c'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma0 = _MeasurementQid('a', q0)
    q_ma1 = _MeasurementQid('a', q1)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_ma0),
            alphaclops.CX(q1, q_ma1),
            alphaclops.X(q0),
            alphaclops.measure(q_ma0, q_ma1, key='a'),
            alphaclops.measure(q0, key='b'),
            alphaclops.measure(q1, key='c'),
        ),
    )


def test_multi_qubit_control():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, q1, key='a'),
        alphaclops.X(q2).with_classical_controls('a'),
        alphaclops.measure(q2, key='b'),
    )
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma0 = _MeasurementQid('a', q0)
    q_ma1 = _MeasurementQid('a', q1)
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_ma0),
            alphaclops.CX(q1, q_ma1),
            alphaclops.X(q2).controlled_by(
                q_ma0, q_ma1, control_values=alphaclops.SumOfProducts(((0, 1), (1, 0), (1, 1)))
            ),
            alphaclops.measure(q_ma0, q_ma1, key='a'),
            alphaclops.measure(q2, key='b'),
        ),
    )


@pytest.mark.parametrize('index', [-3, -2, -1, 0, 1, 2])
def test_repeated(index: int):
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),  # The control measurement when `index` is 0 or -2
        alphaclops.X(q0),
        alphaclops.measure(q0, key='a'),  # The control measurement when `index` is 1 or -1
        alphaclops.X(q1).with_classical_controls(alphaclops.KeyCondition(alphaclops.MeasurementKey('a'), index)),
        alphaclops.measure(q1, key='b'),
    )
    if index in [-3, 2]:
        with pytest.raises(ValueError, match='Invalid index'):
            _ = alphaclops.defer_measurements(circuit)
        return
    assert_equivalent_to_deferred(circuit)
    deferred = alphaclops.defer_measurements(circuit)
    q_ma = _MeasurementQid('a', q0)  # The ancilla qubit created for the first `a` measurement
    q_ma1 = _MeasurementQid('a', q0, 1)  # The ancilla qubit created for the second `a` measurement
    # The ancilla used for control should match the measurement used for control above.
    q_expected_control = q_ma if index in [0, -2] else q_ma1
    alphaclops.testing.assert_same_circuits(
        deferred,
        alphaclops.Circuit(
            alphaclops.CX(q0, q_ma),
            alphaclops.X(q0),
            alphaclops.CX(q0, q_ma1),
            alphaclops.Moment(alphaclops.CX(q_expected_control, q1)),
            alphaclops.measure(q_ma, key='a'),
            alphaclops.measure(q_ma1, key='a'),
            alphaclops.measure(q1, key='b'),
        ),
    )


def test_diagram():
    q0, q1, q2, q3 = alphaclops.LineQubit.range(4)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, q2, key='a'),
        alphaclops.measure(q1, q3, key='b'),
        alphaclops.X(q0),
        alphaclops.measure(q0, q1, q2, q3, key='c'),
    )
    deferred = alphaclops.defer_measurements(circuit)
    alphaclops.testing.assert_has_diagram(
        deferred,
        """
                      ┌────┐
0: ────────────────────@───────X────────M('c')───
                       │                │
1: ────────────────────┼─@──────────────M────────
                       │ │              │
2: ────────────────────┼@┼──────────────M────────
                       │││              │
3: ────────────────────┼┼┼@─────────────M────────
                       ││││
M('a[0]', q=q(0)): ────X┼┼┼────M('a')────────────
                        │││    │
M('a[0]', q=q(2)): ─────X┼┼────M─────────────────
                         ││
M('b[0]', q=q(1)): ──────X┼────M('b')────────────
                          │    │
M('b[0]', q=q(3)): ───────X────M─────────────────
                      └────┘
""",
        use_unicode_characters=True,
    )


def test_repr():
    def test_repr(qid: _MeasurementQid):
        alphaclops.testing.assert_equivalent_repr(qid, global_vals={'_MeasurementQid': _MeasurementQid})

    test_repr(_MeasurementQid('a', alphaclops.LineQubit(0)))
    test_repr(_MeasurementQid('a', alphaclops.NamedQubit('x')))
    test_repr(_MeasurementQid('a', alphaclops.NamedQid('x', 4)))
    test_repr(_MeasurementQid('a', alphaclops.TensorCircuit(2, 3)))
    test_repr(_MeasurementQid('0:1:a', alphaclops.LineQid(9, 4)))


def test_confusion_map():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.H(q0),
        alphaclops.measure(q0, key='a', confusion_map={(0,): np.array([[0.8, 0.2], [0.1, 0.9]])}),
        alphaclops.X(q1).with_classical_controls('a'),
        alphaclops.measure(q1, key='b'),
    )
    deferred = alphaclops.defer_measurements(circuit)

    # We use DM simulator because the deferred circuit has channels
    sim = alphaclops.DensityMatrixSimulator()

    # 10K samples would take a long time if we had not deferred the measurements, as we'd have to
    # run 10K simulations. Here with DM simulator it's 100ms.
    result = sim.sample(deferred, repetitions=10_000)

    # This should be 5_000 due to the H, then 1_000 more due to 0's flipping to 1's with p=0.2, and
    # then 500 less due to 1's flipping to 0's with p=0.1, so 5_500.
    assert 5_100 <= np.sum(result['a']) <= 5_900
    assert np.all(result['a'] == result['b'])


def test_confusion_map_density_matrix():
    q0, q1 = alphaclops.LineQubit.range(2)
    p_q0 = 0.3  # probability to measure 1 for q0
    confusion = np.array([[0.8, 0.2], [0.1, 0.9]])
    circuit = alphaclops.Circuit(
        # Rotate q0 such that the probability to measure 1 is p_q0
        alphaclops.X(q0) ** (np.arcsin(np.sqrt(p_q0)) * 2 / np.pi),
        alphaclops.measure(q0, key='a', confusion_map={(0,): confusion}),
        alphaclops.X(q1).with_classical_controls('a'),
    )
    deferred = alphaclops.defer_measurements(circuit)
    q_order = (q0, q1, _MeasurementQid('a', q0))
    rho = alphaclops.final_density_matrix(deferred, qubit_order=q_order).reshape((2,) * 6)

    # q0 density matrix should be a diagonal with the probabilities [1-p, p].
    q0_probs = [1 - p_q0, p_q0]
    assert np.allclose(alphaclops.partial_trace(rho, [0]), np.diag(q0_probs))

    # q1 and the ancilla should both be the q1 probs matmul the confusion matrix.
    expected = np.diag(q0_probs @ confusion)
    assert np.allclose(alphaclops.partial_trace(rho, [1]), expected)
    assert np.allclose(alphaclops.partial_trace(rho, [2]), expected)


def test_confusion_map_invert_mask_ordering():
    q0 = alphaclops.LineQubit(0)
    # Confusion map sets the measurement to zero, and the invert mask changes it to one.
    # If these are run out of order then the result would be zero.
    circuit = alphaclops.Circuit(
        alphaclops.measure(
            q0, key='a', confusion_map={(0,): np.array([[1, 0], [1, 0]])}, invert_mask=(1,)
        ),
        alphaclops.I(q0),
    )
    assert_equivalent_to_deferred(circuit)


def test_confusion_map_qudits():
    q0 = alphaclops.LineQid(0, dimension=3)
    # First op takes q0 to superposed state, then confusion map measures 2 regardless.
    circuit = alphaclops.Circuit(
        alphaclops.XPowGate(dimension=3).on(q0) ** 1.3,
        alphaclops.measure(
            q0, key='a', confusion_map={(0,): np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]])}
        ),
        alphaclops.IdentityGate(qid_shape=(3,)).on(q0),
    )
    assert_equivalent_to_deferred(circuit)


def test_multi_qubit_confusion_map():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(
        alphaclops.measure(
            q0,
            q1,
            key='a',
            confusion_map={
                (0, 1): np.array(
                    [
                        [0.7, 0.1, 0.1, 0.1],
                        [0.1, 0.6, 0.1, 0.2],
                        [0.2, 0.2, 0.5, 0.1],
                        [0.0, 0.0, 1.0, 0.0],
                    ]
                )
            },
        ),
        alphaclops.X(q2).with_classical_controls('a'),
        alphaclops.measure(q2, key='b'),
    )
    deferred = alphaclops.defer_measurements(circuit)
    sim = alphaclops.DensityMatrixSimulator()
    result = sim.sample(deferred, repetitions=10_000)

    # The initial state is zero, so the first measurement will confuse by the first line in the
    # map, giving 7000 0's, 1000 1's, 1000 2's, and 1000 3's, for a sum of 6000 on average.
    assert 5_600 <= np.sum(result['a']) <= 6_400

    # The measurement will be non-zero 3000 times on average.
    assert 2_600 <= np.sum(result['b']) <= 3_400

    # Try a deterministic one: initial state is 3, which the confusion map sends to 2 with p=1.
    deferred.insert(0, alphaclops.X.on_each(q0, q1))
    result = sim.sample(deferred, repetitions=100)
    assert np.sum(result['a']) == 200
    assert np.sum(result['b']) == 100


def test_confusion_map_errors():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a', confusion_map={(0,): np.array([1])}),
        alphaclops.X(q1).with_classical_controls('a'),
    )
    with pytest.raises(ValueError, match='map must be 2D'):
        _ = alphaclops.defer_measurements(circuit)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a', confusion_map={(0,): np.array([[0.7, 0.3]])}),
        alphaclops.X(q1).with_classical_controls('a'),
    )
    with pytest.raises(ValueError, match='map must be square'):
        _ = alphaclops.defer_measurements(circuit)
    circuit = alphaclops.Circuit(
        alphaclops.measure(
            q0,
            key='a',
            confusion_map={(0,): np.array([[0.7, 0.1, 0.2], [0.1, 0.6, 0.3], [0.2, 0.2, 0.6]])},
        ),
        alphaclops.X(q1).with_classical_controls('a'),
    )
    with pytest.raises(ValueError, match='size does not match'):
        _ = alphaclops.defer_measurements(circuit)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a', confusion_map={(0,): np.array([[-1, 2], [0, 1]])}),
        alphaclops.X(q1).with_classical_controls('a'),
    )
    with pytest.raises(ValueError, match='negative probabilities'):
        _ = alphaclops.defer_measurements(circuit)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a', confusion_map={(0,): np.array([[0.3, 0.3], [0.3, 0.3]])}),
        alphaclops.X(q1).with_classical_controls('a'),
    )
    with pytest.raises(ValueError, match='invalid probabilities'):
        _ = alphaclops.defer_measurements(circuit)


def test_dephase():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                alphaclops.CX(q1, q0),
                alphaclops.measure(q0, key='a'),
                alphaclops.CX(q0, q1),
                alphaclops.measure(q1, key='b'),
            )
        )
    )
    dephased = alphaclops.dephase_measurements(circuit)
    alphaclops.testing.assert_same_circuits(
        dephased,
        alphaclops.Circuit(
            alphaclops.CircuitOperation(
                alphaclops.FrozenCircuit(
                    alphaclops.CX(q1, q0),
                    alphaclops.KrausChannel.from_channel(alphaclops.phase_damp(1), key='a')(q0),
                    alphaclops.CX(q0, q1),
                    alphaclops.KrausChannel.from_channel(alphaclops.phase_damp(1), key='b')(q1),
                )
            )
        ),
    )


def test_dephase_classical_conditions():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.X(q1).with_classical_controls('a'),
        alphaclops.measure(q1, key='b'),
    )
    with pytest.raises(ValueError, match='defer_measurements first to remove classical controls'):
        _ = alphaclops.dephase_measurements(circuit)


def test_dephase_nocompile_context():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                alphaclops.CX(q1, q0),
                alphaclops.measure(q0, key='a').with_tags('nocompile'),
                alphaclops.CX(q0, q1),
                alphaclops.measure(q1, key='b'),
            )
        )
    )
    dephased = alphaclops.dephase_measurements(
        circuit, context=alphaclops.TransformerContext(deep=True, tags_to_ignore=('nocompile',))
    )
    alphaclops.testing.assert_same_circuits(
        dephased,
        alphaclops.Circuit(
            alphaclops.CircuitOperation(
                alphaclops.FrozenCircuit(
                    alphaclops.CX(q1, q0),
                    alphaclops.measure(q0, key='a').with_tags('nocompile'),
                    alphaclops.CX(q0, q1),
                    alphaclops.KrausChannel.from_channel(alphaclops.phase_damp(1), key='b')(q1),
                )
            )
        ),
    )


def test_drop_terminal():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.CX(q0, q1), alphaclops.measure(q0, q1, key='a~b', invert_mask=[0, 1]))
        )
    )
    dropped = alphaclops.drop_terminal_measurements(circuit)
    alphaclops.testing.assert_same_circuits(
        dropped,
        alphaclops.Circuit(
            alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.CX(q0, q1), alphaclops.I(q0), alphaclops.X(q1)))
        ),
    )


def test_drop_terminal_nonterminal_error():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.measure(q0, q1, key='a~b', invert_mask=[0, 1]), alphaclops.CX(q0, q1))
        )
    )
    with pytest.raises(ValueError, match='Circuit contains a non-terminal measurement'):
        _ = alphaclops.drop_terminal_measurements(circuit)

    with pytest.raises(ValueError, match='Context has `deep=False`'):
        _ = alphaclops.drop_terminal_measurements(circuit, context=alphaclops.TransformerContext(deep=False))

    with pytest.raises(ValueError, match='Context has `deep=False`'):
        _ = alphaclops.drop_terminal_measurements(circuit, context=None)


def test_confusion_channel_consistency():
    two_d_chan = _ConfusionChannel(np.array([[0.5, 0.5], [0.4, 0.6]]), shape=(2,))
    alphaclops.testing.assert_has_consistent_apply_channel(two_d_chan)
    three_d_chan = _ConfusionChannel(
        np.array([[0.5, 0.3, 0.2], [0.4, 0.5, 0.1], [0, 0, 1]]), shape=(3,)
    )
    alphaclops.testing.assert_has_consistent_apply_channel(three_d_chan)
    two_q_chan = _ConfusionChannel(
        np.array([[0.5, 0.3, 0.1, 0.1], [0.4, 0.5, 0.1, 0], [0, 0, 1, 0], [0, 0, 0.5, 0.5]]),
        shape=(2, 2),
    )
    alphaclops.testing.assert_has_consistent_apply_channel(two_q_chan)
