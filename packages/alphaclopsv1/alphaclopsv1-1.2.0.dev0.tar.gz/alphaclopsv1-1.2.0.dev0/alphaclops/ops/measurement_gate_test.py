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

from typing import cast
import numpy as np
import pytest

import alphaclops


@pytest.mark.parametrize(
    'key',
    ['q0_1_0', alphaclops.MeasurementKey(name='q0_1_0'), alphaclops.MeasurementKey(path=('a', 'b'), name='c')],
)
def test_eval_repr(key):
    # Basic safeguard against repr-inequality.
    op = alphaclops.GateOperation(gate=alphaclops.MeasurementGate(1, key), qubits=[alphaclops.TensorCircuit(0, 1)])
    alphaclops.testing.assert_equivalent_repr(op)


@pytest.mark.parametrize('num_qubits', [1, 2, 4])
def test_measure_init(num_qubits):
    assert alphaclops.MeasurementGate(num_qubits, 'a').num_qubits() == num_qubits
    assert alphaclops.MeasurementGate(num_qubits, key='a').key == 'a'
    assert alphaclops.MeasurementGate(num_qubits, key='a').mkey == alphaclops.MeasurementKey('a')
    assert alphaclops.MeasurementGate(num_qubits, key=alphaclops.MeasurementKey('a')).key == 'a'
    assert alphaclops.MeasurementGate(num_qubits, key=alphaclops.MeasurementKey('a')) == alphaclops.MeasurementGate(
        num_qubits, key='a'
    )
    assert alphaclops.MeasurementGate(num_qubits, 'a', invert_mask=(True,)).invert_mask == (True,)
    assert alphaclops.qid_shape(alphaclops.MeasurementGate(num_qubits, 'a')) == (2,) * num_qubits
    cmap = {(0,): np.array([[0, 1], [1, 0]])}
    assert alphaclops.MeasurementGate(num_qubits, 'a', confusion_map=cmap).confusion_map == cmap


def test_measure_init_num_qubit_agnostic():
    assert alphaclops.qid_shape(alphaclops.MeasurementGate(3, 'a', qid_shape=(1, 2, 3))) == (1, 2, 3)
    assert alphaclops.qid_shape(alphaclops.MeasurementGate(key='a', qid_shape=(1, 2, 3))) == (1, 2, 3)
    with pytest.raises(ValueError, match='len.* >'):
        alphaclops.MeasurementGate(5, 'a', invert_mask=(True,) * 6)
    with pytest.raises(ValueError, match='len.* !='):
        alphaclops.MeasurementGate(5, 'a', qid_shape=(1, 2))
    with pytest.raises(ValueError, match='valid string'):
        alphaclops.MeasurementGate(2, qid_shape=(1, 2), key=None)
    with pytest.raises(ValueError, match='Confusion matrices have index out of bounds'):
        alphaclops.MeasurementGate(1, 'a', confusion_map={(1,): np.array([[0, 1], [1, 0]])})
    with pytest.raises(ValueError, match='Specify either'):
        alphaclops.MeasurementGate()


def test_measurement_has_unitary_returns_false():
    gate = alphaclops.MeasurementGate(1, 'a')
    assert not alphaclops.has_unitary(gate)


@pytest.mark.parametrize('num_qubits', [1, 2, 4])
def test_has_stabilizer_effect(num_qubits):
    assert alphaclops.has_stabilizer_effect(alphaclops.MeasurementGate(num_qubits, 'a'))


def test_measurement_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.make_equality_group(
        lambda: alphaclops.MeasurementGate(1, 'a'),
        lambda: alphaclops.MeasurementGate(1, 'a', invert_mask=()),
        lambda: alphaclops.MeasurementGate(1, 'a', qid_shape=(2,)),
        lambda: alphaclops.MeasurementGate(1, 'a', confusion_map={}),
    )
    eq.add_equality_group(alphaclops.MeasurementGate(1, 'a', invert_mask=(True,)))
    eq.add_equality_group(alphaclops.MeasurementGate(1, 'a', invert_mask=(False,)))
    eq.add_equality_group(
        alphaclops.MeasurementGate(1, 'a', confusion_map={(0,): np.array([[0, 1], [1, 0]])})
    )
    eq.add_equality_group(alphaclops.MeasurementGate(1, 'b'))
    eq.add_equality_group(alphaclops.MeasurementGate(2, 'a'))
    eq.add_equality_group(
        alphaclops.MeasurementGate(3, 'a'), alphaclops.MeasurementGate(3, 'a', qid_shape=(2, 2, 2))
    )
    eq.add_equality_group(alphaclops.MeasurementGate(3, 'a', qid_shape=(1, 2, 3)))


def test_measurement_full_invert_mask():
    assert alphaclops.MeasurementGate(1, 'a').full_invert_mask() == (False,)
    assert alphaclops.MeasurementGate(2, 'a', invert_mask=(False, True)).full_invert_mask() == (
        False,
        True,
    )
    assert alphaclops.MeasurementGate(2, 'a', invert_mask=(True,)).full_invert_mask() == (True, False)


@pytest.mark.parametrize('use_protocol', [False, True])
@pytest.mark.parametrize(
    'gate',
    [
        alphaclops.MeasurementGate(1, 'a'),
        alphaclops.MeasurementGate(1, 'a', invert_mask=(True,)),
        alphaclops.MeasurementGate(1, 'a', qid_shape=(3,)),
        alphaclops.MeasurementGate(2, 'a', invert_mask=(True, False), qid_shape=(2, 3)),
    ],
)
def test_measurement_with_key(use_protocol, gate):
    if use_protocol:
        gate1 = alphaclops.with_measurement_key_mapping(gate, {'a': 'b'})
    else:
        gate1 = gate.with_key('b')
    assert gate1.key == 'b'
    assert gate1.num_qubits() == gate.num_qubits()
    assert gate1.invert_mask == gate.invert_mask
    assert alphaclops.qid_shape(gate1) == alphaclops.qid_shape(gate)
    if use_protocol:
        gate2 = alphaclops.with_measurement_key_mapping(gate, {'a': 'a'})
    else:
        gate2 = gate.with_key('a')
    assert gate2 == gate


@pytest.mark.parametrize(
    'num_qubits, mask, bits, flipped',
    [
        (1, (), [0], (True,)),
        (3, (False,), [1], (False, True)),
        (3, (False, False), [0, 2], (True, False, True)),
    ],
)
def test_measurement_with_bits_flipped(num_qubits, mask, bits, flipped):
    gate = alphaclops.MeasurementGate(num_qubits, key='a', invert_mask=mask, qid_shape=(3,) * num_qubits)

    gate1 = gate.with_bits_flipped(*bits)
    assert gate1.key == gate.key
    assert gate1.num_qubits() == gate.num_qubits()
    assert gate1.invert_mask == flipped
    assert alphaclops.qid_shape(gate1) == alphaclops.qid_shape(gate)

    # Flipping bits again restores the mask (but may have extended it).
    gate2 = gate1.with_bits_flipped(*bits)
    assert gate2.full_invert_mask() == gate.full_invert_mask()


def test_qudit_measure_qasm():
    assert (
            alphaclops.qasm(
            alphaclops.measure(alphaclops.LineQid(0, 3), key='a'),
            args=alphaclops.QasmArgs(),
            default='not implemented',
        )
            == 'not implemented'
    )


def test_confused_measure_qasm():
    q0 = alphaclops.LineQubit(0)
    assert (
            alphaclops.qasm(
            alphaclops.measure(q0, key='a', confusion_map={(0,): np.array([[0, 1], [1, 0]])}),
            args=alphaclops.QasmArgs(),
            default='not implemented',
        )
            == 'not implemented'
    )


def test_measurement_gate_diagram():
    # Shows key.
    assert alphaclops.circuit_diagram_info(
        alphaclops.MeasurementGate(1, key='test')
    ) == alphaclops.CircuitDiagramInfo(("M('test')",))

    # Uses known qubit count.
    assert alphaclops.circuit_diagram_info(
        alphaclops.MeasurementGate(3, 'a'),
        alphaclops.CircuitDiagramInfoArgs(
            known_qubits=None,
            known_qubit_count=3,
            use_unicode_characters=True,
            precision=None,
            label_map=None,
        ),
    ) == alphaclops.CircuitDiagramInfo(("M('a')", 'M', 'M'))

    # Shows invert mask.
    assert alphaclops.circuit_diagram_info(
        alphaclops.MeasurementGate(2, 'a', invert_mask=(False, True))
    ) == alphaclops.CircuitDiagramInfo(("M('a')", "!M"))

    # Omits key when it is the default.
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(alphaclops.measure(a, b)),
        """
a: ───M───
      │
b: ───M───
""",
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(alphaclops.measure(a, b, invert_mask=(True,))),
        """
a: ───!M───
      │
b: ───M────
""",
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(alphaclops.measure(a, b, confusion_map={(1,): np.array([[0, 1], [1, 0]])})),
        """
a: ───M────
      │
b: ───?M───
""",
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            alphaclops.measure(
                a, b, invert_mask=(False, True), confusion_map={(1,): np.array([[0, 1], [1, 0]])}
            )
        ),
        """
a: ───M─────
      │
b: ───!?M───
""",
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(alphaclops.measure(a, b, key='test')),
        """
a: ───M('test')───
      │
b: ───M───────────
""",
    )


def test_measurement_channel():
    np.testing.assert_allclose(
        alphaclops.kraus(alphaclops.MeasurementGate(1, 'a')),
        (np.array([[1, 0], [0, 0]]), np.array([[0, 0], [0, 1]])),
    )
    alphaclops.testing.assert_consistent_channel(alphaclops.MeasurementGate(1, 'a'))
    assert not alphaclops.has_mixture(alphaclops.MeasurementGate(1, 'a'))
    # yapf: disable
    np.testing.assert_allclose(
            alphaclops.kraus(alphaclops.MeasurementGate(2, 'a')),
            (np.array([[1, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]),
             np.array([[0, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]),
             np.array([[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 0]]),
             np.array([[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 1]])))
    np.testing.assert_allclose(
            alphaclops.kraus(alphaclops.MeasurementGate(2, 'a', qid_shape=(2, 3))),
            (np.diag([1, 0, 0, 0, 0, 0]),
             np.diag([0, 1, 0, 0, 0, 0]),
             np.diag([0, 0, 1, 0, 0, 0]),
             np.diag([0, 0, 0, 1, 0, 0]),
             np.diag([0, 0, 0, 0, 1, 0]),
             np.diag([0, 0, 0, 0, 0, 1])))
    # yapf: enable


def test_measurement_qubit_count_vs_mask_length():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')

    _ = alphaclops.MeasurementGate(num_qubits=1, key='a', invert_mask=(True,)).on(a)
    _ = alphaclops.MeasurementGate(num_qubits=2, key='a', invert_mask=(True, False)).on(a, b)
    _ = alphaclops.MeasurementGate(num_qubits=3, key='a', invert_mask=(True, False, True)).on(a, b, c)
    with pytest.raises(ValueError):
        _ = alphaclops.MeasurementGate(num_qubits=1, key='a', invert_mask=(True, False)).on(a)
    with pytest.raises(ValueError):
        _ = alphaclops.MeasurementGate(num_qubits=3, key='a', invert_mask=(True, False, True)).on(a, b)


def test_consistent_protocols():
    for n in range(1, 5):
        gate = alphaclops.MeasurementGate(num_qubits=n, key='a')
        alphaclops.testing.assert_implements_consistent_protocols(gate)

        gate = alphaclops.MeasurementGate(num_qubits=n, key='a', qid_shape=(3,) * n)
        alphaclops.testing.assert_implements_consistent_protocols(gate)


def test_op_repr():
    a, b = alphaclops.LineQubit.range(2)
    assert repr(alphaclops.measure(a)) == 'alphaclops.measure(alphaclops.LineQubit(0))'
    assert repr(alphaclops.measure(a, b)) == ('alphaclops.measure(alphaclops.LineQubit(0), alphaclops.LineQubit(1))')
    assert repr(alphaclops.measure(a, b, key='out', invert_mask=(False, True))) == (
        "alphaclops.measure(alphaclops.LineQubit(0), alphaclops.LineQubit(1), "
        "key=alphaclops.MeasurementKey(name='out'), "
        "invert_mask=(False, True))"
    )
    assert repr(
        alphaclops.measure(
            a,
            b,
            key='out',
            invert_mask=(False, True),
            confusion_map={(0,): np.array([[0, 1], [1, 0]], dtype=np.dtype('int64'))},
        )
    ) == (
        "alphaclops.measure(alphaclops.LineQubit(0), alphaclops.LineQubit(1), "
        "key=alphaclops.MeasurementKey(name='out'), "
        "invert_mask=(False, True), "
        "confusion_map={(0,): np.array([[0, 1], [1, 0]], dtype=np.dtype('int64'))})"
    )


def test_repr():
    gate = alphaclops.MeasurementGate(
        3,
        'a',
        (True, False),
        (1, 2, 3),
        {(2,): np.array([[0, 1], [1, 0]], dtype=np.dtype('int64'))},
    )
    assert repr(gate) == (
        "alphaclops.MeasurementGate(3, alphaclops.MeasurementKey(name='a'), (True, False), "
        "qid_shape=(1, 2, 3), "
        "confusion_map={(2,): np.array([[0, 1], [1, 0]], dtype=np.dtype('int64'))})"
    )


def test_act_on_state_vector():
    a, b = [alphaclops.LineQubit(3), alphaclops.LineQubit(1)]
    m = alphaclops.measure(
        a, b, key='out', invert_mask=(True,), confusion_map={(1,): np.array([[0, 1], [1, 0]])}
    )

    args = alphaclops.StateVectorSimulationState(
        available_buffer=np.empty(shape=(2, 2, 2, 2, 2)),
        qubits=alphaclops.LineQubit.range(5),
        prng=np.random.RandomState(),
        initial_state=alphaclops.one_hot(shape=(2, 2, 2, 2, 2), dtype=np.complex64),
        dtype=np.complex64,
    )
    alphaclops.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [1, 1]}

    args = alphaclops.StateVectorSimulationState(
        available_buffer=np.empty(shape=(2, 2, 2, 2, 2)),
        qubits=alphaclops.LineQubit.range(5),
        prng=np.random.RandomState(),
        initial_state=alphaclops.one_hot(
            index=(0, 1, 0, 0, 0), shape=(2, 2, 2, 2, 2), dtype=np.complex64
        ),
        dtype=np.complex64,
    )
    alphaclops.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [1, 0]}

    args = alphaclops.StateVectorSimulationState(
        available_buffer=np.empty(shape=(2, 2, 2, 2, 2)),
        qubits=alphaclops.LineQubit.range(5),
        prng=np.random.RandomState(),
        initial_state=alphaclops.one_hot(
            index=(0, 1, 0, 1, 0), shape=(2, 2, 2, 2, 2), dtype=np.complex64
        ),
        dtype=np.complex64,
    )
    alphaclops.act_on(m, args)
    datastore = cast(alphaclops.ClassicalDataDictionaryStore, args.classical_data)
    out = alphaclops.MeasurementKey('out')
    assert args.log_of_measurement_results == {'out': [0, 0]}
    assert datastore.records[out] == [(0, 0)]
    alphaclops.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [0, 0]}
    assert datastore.records[out] == [(0, 0), (0, 0)]


def test_act_on_clifford_tableau():
    a, b = [alphaclops.LineQubit(3), alphaclops.LineQubit(1)]
    m = alphaclops.measure(
        a, b, key='out', invert_mask=(True,), confusion_map={(1,): np.array([[0, 1], [1, 0]])}
    )
    # The below assertion does not fail since it ignores non-unitary operations
    alphaclops.testing.assert_all_implemented_act_on_effects_match_unitary(m)

    args = alphaclops.CliffordTableauSimulationState(
        tableau=alphaclops.CliffordTableau(num_qubits=5, initial_state=0),
        qubits=alphaclops.LineQubit.range(5),
        prng=np.random.RandomState(),
    )
    alphaclops.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [1, 1]}

    args = alphaclops.CliffordTableauSimulationState(
        tableau=alphaclops.CliffordTableau(num_qubits=5, initial_state=8),
        qubits=alphaclops.LineQubit.range(5),
        prng=np.random.RandomState(),
    )

    alphaclops.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [1, 0]}

    args = alphaclops.CliffordTableauSimulationState(
        tableau=alphaclops.CliffordTableau(num_qubits=5, initial_state=10),
        qubits=alphaclops.LineQubit.range(5),
        prng=np.random.RandomState(),
    )
    alphaclops.act_on(m, args)
    datastore = cast(alphaclops.ClassicalDataDictionaryStore, args.classical_data)
    out = alphaclops.MeasurementKey('out')
    assert args.log_of_measurement_results == {'out': [0, 0]}
    assert datastore.records[out] == [(0, 0)]
    alphaclops.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [0, 0]}
    assert datastore.records[out] == [(0, 0), (0, 0)]


def test_act_on_stabilizer_ch_form():
    a, b = [alphaclops.LineQubit(3), alphaclops.LineQubit(1)]
    m = alphaclops.measure(
        a, b, key='out', invert_mask=(True,), confusion_map={(1,): np.array([[0, 1], [1, 0]])}
    )
    # The below assertion does not fail since it ignores non-unitary operations
    alphaclops.testing.assert_all_implemented_act_on_effects_match_unitary(m)

    args = alphaclops.StabilizerChFormSimulationState(
        qubits=alphaclops.LineQubit.range(5), prng=np.random.RandomState(), initial_state=0
    )
    alphaclops.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [1, 1]}

    args = alphaclops.StabilizerChFormSimulationState(
        qubits=alphaclops.LineQubit.range(5), prng=np.random.RandomState(), initial_state=8
    )

    alphaclops.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [1, 0]}

    args = alphaclops.StabilizerChFormSimulationState(
        qubits=alphaclops.LineQubit.range(5), prng=np.random.RandomState(), initial_state=10
    )
    alphaclops.act_on(m, args)
    datastore = cast(alphaclops.ClassicalDataDictionaryStore, args.classical_data)
    out = alphaclops.MeasurementKey('out')
    assert args.log_of_measurement_results == {'out': [0, 0]}
    assert datastore.records[out] == [(0, 0)]
    alphaclops.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [0, 0]}
    assert datastore.records[out] == [(0, 0), (0, 0)]


def test_act_on_qutrit():
    a, b = [alphaclops.LineQid(3, dimension=3), alphaclops.LineQid(1, dimension=3)]
    m = alphaclops.measure(
        a,
        b,
        key='out',
        invert_mask=(True,),
        confusion_map={(1,): np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])},
    )

    args = alphaclops.StateVectorSimulationState(
        available_buffer=np.empty(shape=(3, 3, 3, 3, 3)),
        qubits=alphaclops.LineQid.range(5, dimension=3),
        prng=np.random.RandomState(),
        initial_state=alphaclops.one_hot(
            index=(0, 2, 0, 2, 0), shape=(3, 3, 3, 3, 3), dtype=np.complex64
        ),
        dtype=np.complex64,
    )
    alphaclops.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [2, 0]}

    args = alphaclops.StateVectorSimulationState(
        available_buffer=np.empty(shape=(3, 3, 3, 3, 3)),
        qubits=alphaclops.LineQid.range(5, dimension=3),
        prng=np.random.RandomState(),
        initial_state=alphaclops.one_hot(
            index=(0, 1, 0, 2, 0), shape=(3, 3, 3, 3, 3), dtype=np.complex64
        ),
        dtype=np.complex64,
    )
    alphaclops.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [2, 2]}

    args = alphaclops.StateVectorSimulationState(
        available_buffer=np.empty(shape=(3, 3, 3, 3, 3)),
        qubits=alphaclops.LineQid.range(5, dimension=3),
        prng=np.random.RandomState(),
        initial_state=alphaclops.one_hot(
            index=(0, 2, 0, 1, 0), shape=(3, 3, 3, 3, 3), dtype=np.complex64
        ),
        dtype=np.complex64,
    )
    alphaclops.act_on(m, args)
    assert args.log_of_measurement_results == {'out': [0, 0]}
