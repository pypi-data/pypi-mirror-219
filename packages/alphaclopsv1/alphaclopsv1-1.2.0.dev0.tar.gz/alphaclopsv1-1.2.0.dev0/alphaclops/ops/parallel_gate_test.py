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
import numpy as np
import sympy
import alphaclops


@pytest.mark.parametrize(
    'gate, num_copies, qubits',
    [
        (alphaclops.testing.SingleQubitGate(), 2, alphaclops.LineQubit.range(2)),
        (alphaclops.X ** 0.5, 4, alphaclops.LineQubit.range(4)),
    ],
)
def test_parallel_gate_operation_init(gate, num_copies, qubits):
    v = alphaclops.ParallelGate(gate, num_copies)
    assert v.sub_gate == gate
    assert v.num_copies == num_copies
    assert v.on(*qubits).qubits == tuple(qubits)


@pytest.mark.parametrize(
    'gate, num_copies, qubits, error_msg',
    [
        (alphaclops.testing.SingleQubitGate(), 3, alphaclops.LineQubit.range(2), "Wrong number of qubits"),
        (
                alphaclops.testing.SingleQubitGate(),
                0,
                alphaclops.LineQubit.range(4),
            "gate must be applied at least once",
        ),
        (
                alphaclops.testing.SingleQubitGate(),
                2,
                [alphaclops.NamedQubit("a"), alphaclops.NamedQubit("a")],
            "Duplicate",
        ),
        (alphaclops.testing.TwoQubitGate(), 2, alphaclops.LineQubit.range(4), "must be a single qubit gate"),
    ],
)
def test_invalid_parallel_gate_operation(gate, num_copies, qubits, error_msg):
    with pytest.raises(ValueError, match=error_msg):
        alphaclops.ParallelGate(gate, num_copies)(*qubits)


@pytest.mark.parametrize(
    'gate, num_copies, qubits',
    [(alphaclops.X, 2, alphaclops.LineQubit.range(2)), (alphaclops.H ** 0.5, 4, alphaclops.LineQubit.range(4))],
)
def test_decompose(gate, num_copies, qubits):
    g = alphaclops.ParallelGate(gate, num_copies)
    step = gate.num_qubits()
    qubit_lists = [qubits[i * step : (i + 1) * step] for i in range(num_copies)]
    assert set(alphaclops.decompose_once(g(*qubits))) == set(gate.on_each(qubit_lists))


def test_decompose_raises():
    g = alphaclops.ParallelGate(alphaclops.X, 2)
    qubits = alphaclops.LineQubit.range(4)
    with pytest.raises(ValueError, match=r'len\(qubits\)=4 should be 2'):
        alphaclops.decompose_once_with_qubits(g, qubits)


def test_with_num_copies():
    g = alphaclops.testing.SingleQubitGate()
    pg = alphaclops.ParallelGate(g, 3)
    assert pg.with_num_copies(5) == alphaclops.ParallelGate(g, 5)


def test_extrapolate():
    # If the gate isn't extrapolatable, you get a type error.
    g = alphaclops.ParallelGate(alphaclops.testing.SingleQubitGate(), 2)
    with pytest.raises(TypeError):
        _ = g**0.5
    # If the gate is extrapolatable, the effect is applied on the underlying gate.
    g = alphaclops.ParallelGate(alphaclops.Y, 2)
    assert g ** 0.5 == alphaclops.ParallelGate(alphaclops.Y ** 0.5, 2)
    assert alphaclops.inverse(g) == g ** -1 == alphaclops.ParallelGate(alphaclops.Y ** -1, 2)


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_parameterizable_gates(resolve_fn):
    r = alphaclops.ParamResolver({'a': 0.5})
    g1 = alphaclops.ParallelGate(alphaclops.Z ** sympy.Symbol('a'), 2)
    assert alphaclops.is_parameterized(g1)
    g2 = resolve_fn(g1, r)
    assert not alphaclops.is_parameterized(g2)


@pytest.mark.parametrize('gate', [alphaclops.X ** sympy.Symbol("a"), alphaclops.testing.SingleQubitGate()])
def test_no_unitary(gate):
    g = alphaclops.ParallelGate(gate, 2)
    assert not alphaclops.has_unitary(g)
    assert alphaclops.unitary(g, None) is None


@pytest.mark.parametrize(
    'gate, num_copies, qubits',
    [
        (alphaclops.X ** 0.5, 2, alphaclops.LineQubit.range(2)),
        (alphaclops.MatrixGate(alphaclops.unitary(alphaclops.H ** 0.25)), 6, alphaclops.LineQubit.range(6)),
    ],
)
def test_unitary(gate, num_copies, qubits):
    g = alphaclops.ParallelGate(gate, num_copies)
    step = gate.num_qubits()
    qubit_lists = [qubits[i * step : (i + 1) * step] for i in range(num_copies)]
    np.testing.assert_allclose(
        alphaclops.unitary(g), alphaclops.unitary(alphaclops.Circuit(gate.on_each(qubit_lists))), atol=1e-8
    )


def test_not_implemented_diagram():
    q = alphaclops.LineQubit.range(2)
    g = alphaclops.testing.SingleQubitGate()
    c = alphaclops.Circuit()
    c.append(alphaclops.ParallelGate(g, 2)(*q))
    assert 'alphaclops.testing.gate_features.SingleQubitGate ' in str(c)


def test_repr():
    assert repr(alphaclops.ParallelGate(alphaclops.X, 2)) == 'alphaclops.ParallelGate(sub_gate=alphaclops.X, num_copies=2)'


def test_str():
    assert str(alphaclops.ParallelGate(alphaclops.X ** 0.5, 10)) == 'X**0.5 x 10'


def test_equivalent_circuit():
    qreg = alphaclops.LineQubit.range(4)
    oldc = alphaclops.Circuit()
    newc = alphaclops.Circuit()
    single_qubit_gates = [alphaclops.X ** (1 / 2), alphaclops.Y ** (1 / 3), alphaclops.Z ** -1]
    for gate in single_qubit_gates:
        for qubit in qreg:
            oldc.append(gate.on(qubit))
        newc.append(alphaclops.ParallelGate(gate, 4)(*qreg))
    alphaclops.testing.assert_has_diagram(newc, oldc.to_text_diagram())
    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(oldc, newc, atol=1e-6)


@pytest.mark.parametrize('gate, num_copies', [(alphaclops.X, 1), (alphaclops.Y, 2), (alphaclops.Z, 3), (alphaclops.H, 4)])
def test_parallel_gate_operation_is_consistent(gate, num_copies):
    alphaclops.testing.assert_implements_consistent_protocols(alphaclops.ParallelGate(gate, num_copies))


def test_trace_distance():
    s = alphaclops.X ** 0.25
    two_g = alphaclops.ParallelGate(s, 2)
    three_g = alphaclops.ParallelGate(s, 3)
    four_g = alphaclops.ParallelGate(s, 4)
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(two_g), np.sin(np.pi / 4))
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(three_g), np.sin(3 * np.pi / 8))
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(four_g), 1.0)
    spg = alphaclops.ParallelGate(alphaclops.X ** sympy.Symbol('a'), 4)
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(spg), 1.0)


@pytest.mark.parametrize('gate, num_copies', [(alphaclops.X, 1), (alphaclops.Y, 2), (alphaclops.Z, 3), (alphaclops.H, 4)])
def test_parallel_gate_op(gate, num_copies):
    qubits = alphaclops.LineQubit.range(num_copies * gate.num_qubits())
    assert alphaclops.parallel_gate_op(gate, *qubits) == alphaclops.ParallelGate(gate, num_copies).on(*qubits)
