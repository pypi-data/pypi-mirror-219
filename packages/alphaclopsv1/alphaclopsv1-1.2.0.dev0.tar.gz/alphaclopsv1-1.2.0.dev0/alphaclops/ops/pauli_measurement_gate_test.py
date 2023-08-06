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

import alphaclops


@pytest.mark.parametrize(
    'key',
    ['q0_1_0', alphaclops.MeasurementKey(name='q0_1_0'), alphaclops.MeasurementKey(path=('a', 'b'), name='c')],
)
def test_eval_repr(key):
    # Basic safeguard against repr-inequality.
    op = alphaclops.GateOperation(
        gate=alphaclops.PauliMeasurementGate([alphaclops.X, alphaclops.Y], key),
        qubits=[alphaclops.TensorCircuit(0, 1), alphaclops.TensorCircuit(1, 1)],
    )
    alphaclops.testing.assert_equivalent_repr(op)
    assert alphaclops.is_measurement(op)
    assert alphaclops.measurement_key_name(op) == str(key)


@pytest.mark.parametrize('observable', [[alphaclops.X], [alphaclops.Y, alphaclops.Z], alphaclops.DensePauliString('XYZ')])
@pytest.mark.parametrize('key', ['a', alphaclops.MeasurementKey('a')])
def test_init(observable, key):
    g = alphaclops.PauliMeasurementGate(observable, key)
    assert g.num_qubits() == len(observable)
    assert g.key == 'a'
    assert g.mkey == alphaclops.MeasurementKey('a')
    assert g._observable == alphaclops.DensePauliString(observable)
    assert alphaclops.qid_shape(g) == (2,) * len(observable)


def test_measurement_has_unitary_returns_false():
    gate = alphaclops.PauliMeasurementGate([alphaclops.X], 'a')
    assert not alphaclops.has_unitary(gate)


def test_measurement_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.make_equality_group(
        lambda: alphaclops.PauliMeasurementGate([alphaclops.X, alphaclops.Y], 'a'),
        lambda: alphaclops.PauliMeasurementGate([alphaclops.X, alphaclops.Y], alphaclops.MeasurementKey('a')),
    )
    eq.add_equality_group(alphaclops.PauliMeasurementGate([alphaclops.X, alphaclops.Y], 'b'))
    eq.add_equality_group(alphaclops.PauliMeasurementGate([alphaclops.Y, alphaclops.X], 'a'))


@pytest.mark.parametrize(
    'protocol,args,key',
    [
        (None, None, 'b'),
        (alphaclops.with_key_path, ('p', 'q'), 'p:q:a'),
        (alphaclops.with_measurement_key_mapping, {'a': 'b'}, 'b'),
    ],
)
@pytest.mark.parametrize(
    'gate',
    [
        alphaclops.PauliMeasurementGate([alphaclops.X], 'a'),
        alphaclops.PauliMeasurementGate([alphaclops.X, alphaclops.Y, alphaclops.Z], 'a'),
    ],
)
def test_measurement_with_key(protocol, args, key, gate):
    if protocol:
        gate_with_key = protocol(gate, args)
    else:
        gate_with_key = gate.with_key('b')
    assert gate_with_key.key == key
    assert gate_with_key.num_qubits() == gate.num_qubits()
    assert gate_with_key.observable() == gate.observable()
    assert alphaclops.qid_shape(gate_with_key) == alphaclops.qid_shape(gate)
    if protocol:
        same_gate = alphaclops.with_measurement_key_mapping(gate, {'a': 'a'})
    else:
        same_gate = gate.with_key('a')
    assert same_gate == gate


def test_measurement_gate_diagram():
    # Shows observable & key.
    assert alphaclops.circuit_diagram_info(
        alphaclops.PauliMeasurementGate([alphaclops.X], key='test')
    ) == alphaclops.CircuitDiagramInfo(("M(X)('test')",))

    # Shows multiple observables.
    assert alphaclops.circuit_diagram_info(
        alphaclops.PauliMeasurementGate([alphaclops.X, alphaclops.Y, alphaclops.Z], 'a')
    ) == alphaclops.CircuitDiagramInfo(("M(X)('a')", 'M(Y)', 'M(Z)'))

    # Omits key when it is the default.
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(alphaclops.measure_single_paulistring(alphaclops.X(a) * alphaclops.Y(b))),
        """
a: ───M(X)───
      │
b: ───M(Y)───
""",
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(alphaclops.measure_single_paulistring(alphaclops.X(a) * alphaclops.Y(b), key='test')),
        """
a: ───M(X)('test')───
      │
b: ───M(Y)───────────
""",
    )


@pytest.mark.parametrize('observable', [[alphaclops.X], [alphaclops.X, alphaclops.Y, alphaclops.Z]])
@pytest.mark.parametrize(
    'key',
    ['q0_1_0', alphaclops.MeasurementKey(name='q0_1_0'), alphaclops.MeasurementKey(path=('a', 'b'), name='c')],
)
def test_consistent_protocols(observable, key):
    gate = alphaclops.PauliMeasurementGate(observable, key=key)
    alphaclops.testing.assert_implements_consistent_protocols(gate)
    assert alphaclops.is_measurement(gate)
    assert alphaclops.measurement_key_name(gate) == str(key)


def test_op_repr():
    a, b, c = alphaclops.LineQubit.range(3)
    ps = alphaclops.X(a) * alphaclops.Y(b) * alphaclops.Z(c)
    assert (
        repr(alphaclops.measure_single_paulistring(ps))
        == 'alphaclops.measure_single_paulistring(((1+0j)*alphaclops.X(alphaclops.LineQubit(0))'
        '*alphaclops.Y(alphaclops.LineQubit(1))*alphaclops.Z(alphaclops.LineQubit(2))))'
    )
    assert (
        repr(alphaclops.measure_single_paulistring(ps, key='out'))
        == "alphaclops.measure_single_paulistring(((1+0j)*alphaclops.X(alphaclops.LineQubit(0))"
        "*alphaclops.Y(alphaclops.LineQubit(1))*alphaclops.Z(alphaclops.LineQubit(2))), "
        "key=alphaclops.MeasurementKey(name='out'))"
    )


def test_bad_observable_raises():
    with pytest.raises(ValueError, match='Pauli observable .* is empty'):
        _ = alphaclops.PauliMeasurementGate([])

    with pytest.raises(ValueError, match=r'Pauli observable .* must be Iterable\[`alphaclops.Pauli`\]'):
        _ = alphaclops.PauliMeasurementGate([alphaclops.I, alphaclops.X, alphaclops.Y])

    with pytest.raises(ValueError, match=r'Pauli observable .* must be Iterable\[`alphaclops.Pauli`\]'):
        _ = alphaclops.PauliMeasurementGate(alphaclops.DensePauliString('XYZI'))

    with pytest.raises(ValueError, match=r'must have coefficient \+1/-1.'):
        _ = alphaclops.PauliMeasurementGate(alphaclops.DensePauliString('XYZ', coefficient=1j))


def test_with_observable():
    o1 = [alphaclops.Z, alphaclops.Y, alphaclops.X]
    o2 = [alphaclops.X, alphaclops.Y, alphaclops.Z]
    g1 = alphaclops.PauliMeasurementGate(o1, key='a')
    g2 = alphaclops.PauliMeasurementGate(o2, key='a')
    assert g1.with_observable(o2) == g2
    assert g1.with_observable(o1) is g1


@pytest.mark.parametrize(
    'rot, obs, out',
    [
        (alphaclops.I, alphaclops.DensePauliString("Z", coefficient=+1), 0),
        (alphaclops.I, alphaclops.DensePauliString("Z", coefficient=-1), 1),
        (alphaclops.Y ** 0.5, alphaclops.DensePauliString("X", coefficient=+1), 0),
        (alphaclops.Y ** 0.5, alphaclops.DensePauliString("X", coefficient=-1), 1),
        (alphaclops.X ** -0.5, alphaclops.DensePauliString("Y", coefficient=+1), 0),
        (alphaclops.X ** -0.5, alphaclops.DensePauliString("Y", coefficient=-1), 1),
    ],
)
def test_pauli_measurement_gate_samples(rot, obs, out):
    q = alphaclops.NamedQubit("q")
    c = alphaclops.Circuit(rot(q), alphaclops.PauliMeasurementGate(obs, key='out').on(q))
    assert alphaclops.Simulator().sample(c)['out'][0] == out
