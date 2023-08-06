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
import pytest
import numpy as np
import sympy

import alphaclops

dps_empty = alphaclops.DensePauliString('')
dps_x = alphaclops.DensePauliString('X')
dps_y = alphaclops.DensePauliString('Y')
dps_xy = alphaclops.DensePauliString('XY')
dps_yx = alphaclops.DensePauliString('YX')
dps_xyz = alphaclops.DensePauliString('XYZ')
dps_zyx = alphaclops.DensePauliString('ZYX')


def _make_qubits(n):
    return [alphaclops.NamedQubit(f'q{i}') for i in range(n)]


def test_init():
    a = alphaclops.LineQubit(0)
    with pytest.raises(ValueError, match='eigenvalues'):
        _ = alphaclops.PauliStringPhasor(1j * alphaclops.X(a))
    v1 = alphaclops.PauliStringPhasor(-alphaclops.X(a), exponent_neg=0.25, exponent_pos=-0.5)
    assert v1.pauli_string == alphaclops.X(a)
    assert v1.exponent_neg == -0.5
    assert v1.exponent_pos == 0.25

    v2 = alphaclops.PauliStringPhasor(alphaclops.X(a), exponent_neg=0.75, exponent_pos=-0.125)
    assert v2.pauli_string == alphaclops.X(a)
    assert v2.exponent_neg == 0.75
    assert v2.exponent_pos == -0.125


def test_qubit_order_mismatch():
    q0, q1 = alphaclops.LineQubit.range(2)
    with pytest.raises(ValueError, match='are not an ordered subset'):
        _ = alphaclops.PauliStringPhasor(1j * alphaclops.X(q0), qubits=[q1])
    with pytest.raises(ValueError, match='are not an ordered subset'):
        _ = alphaclops.PauliStringPhasor(1j * alphaclops.X(q0) * alphaclops.X(q1), qubits=[q1])
    with pytest.raises(ValueError, match='are not an ordered subset'):
        _ = alphaclops.PauliStringPhasor(1j * alphaclops.X(q0), qubits=[])
    with pytest.raises(ValueError, match='are not an ordered subset'):
        _ = alphaclops.PauliStringPhasor(1j * alphaclops.X(q0) * alphaclops.X(q1), qubits=[q1, q0])


def test_eq_ne_hash():
    q0, q1, q2, q3 = _make_qubits(4)
    eq = alphaclops.testing.EqualsTester()
    ps1 = alphaclops.X(q0) * alphaclops.Y(q1) * alphaclops.Z(q2)
    ps2 = alphaclops.X(q0) * alphaclops.Y(q1) * alphaclops.X(q2)
    eq.make_equality_group(
        lambda: alphaclops.PauliStringPhasor(alphaclops.PauliString(), exponent_neg=0.5),
        lambda: alphaclops.PauliStringPhasor(alphaclops.PauliString(), exponent_neg=-1.5),
        lambda: alphaclops.PauliStringPhasor(alphaclops.PauliString(), exponent_neg=2.5),
    )
    eq.make_equality_group(lambda: alphaclops.PauliStringPhasor(-alphaclops.PauliString(), exponent_neg=-0.5))
    eq.add_equality_group(alphaclops.PauliStringPhasor(ps1), alphaclops.PauliStringPhasor(ps1, exponent_neg=1))
    eq.add_equality_group(alphaclops.PauliStringPhasor(-ps1, exponent_neg=1))
    eq.add_equality_group(alphaclops.PauliStringPhasor(ps2), alphaclops.PauliStringPhasor(ps2, exponent_neg=1))
    eq.add_equality_group(alphaclops.PauliStringPhasor(-ps2, exponent_neg=1))
    eq.add_equality_group(alphaclops.PauliStringPhasor(ps2, exponent_neg=0.5))
    eq.add_equality_group(alphaclops.PauliStringPhasor(-ps2, exponent_neg=-0.5))
    eq.add_equality_group(alphaclops.PauliStringPhasor(ps1, exponent_neg=sympy.Symbol('a')))
    eq.add_equality_group(alphaclops.PauliStringPhasor(ps1, qubits=[q0, q1, q2, q3]))


def test_equal_up_to_global_phase():
    a, b, c = alphaclops.LineQubit.range(3)
    groups = [
        [
            alphaclops.PauliStringPhasor(alphaclops.PauliString({a: alphaclops.X}), exponent_neg=0.25),
            alphaclops.PauliStringPhasor(
                alphaclops.PauliString({a: alphaclops.X}), exponent_neg=0, exponent_pos=-0.25
            ),
            alphaclops.PauliStringPhasor(
                alphaclops.PauliString({a: alphaclops.X}), exponent_pos=-0.125, exponent_neg=0.125
            ),
        ],
        [alphaclops.PauliStringPhasor(alphaclops.PauliString({a: alphaclops.X}))],
        [alphaclops.PauliStringPhasor(alphaclops.PauliString({a: alphaclops.Y}), exponent_neg=0.25)],
        [alphaclops.PauliStringPhasor(alphaclops.PauliString({a: alphaclops.X, b: alphaclops.Y}), exponent_neg=0.25)],
        [
            alphaclops.PauliStringPhasor(
                alphaclops.PauliString({a: alphaclops.X, b: alphaclops.Y}), qubits=[a, b, c], exponent_neg=0.25
            )
        ],
    ]
    for g1 in groups:
        for e1 in g1:
            assert not e1.equal_up_to_global_phase("not even close")
            for g2 in groups:
                for e2 in g2:
                    assert e1.equal_up_to_global_phase(e2) == (g1 is g2)


def test_map_qubits():
    q0, q1, q2, q3, q4, q5 = _make_qubits(6)
    qubit_map = {q1: q2, q0: q3}
    before = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z, q1: alphaclops.Y}), exponent_neg=0.1)
    after = alphaclops.PauliStringPhasor(alphaclops.PauliString({q3: alphaclops.Z, q2: alphaclops.Y}), exponent_neg=0.1)
    assert before.map_qubits(qubit_map) == after

    qubit_map = {q1: q3, q0: q4, q2: q5}
    before = alphaclops.PauliStringPhasor(
        alphaclops.PauliString({q0: alphaclops.Z, q1: alphaclops.Y}), qubits=[q0, q1, q2], exponent_neg=0.1
    )
    after = alphaclops.PauliStringPhasor(
        alphaclops.PauliString({q4: alphaclops.Z, q3: alphaclops.Y}), qubits=[q4, q3, q5], exponent_neg=0.1
    )
    assert before.map_qubits(qubit_map) == after


def test_map_qubits_missing_qubits():
    q0, q1, q2 = _make_qubits(3)
    qubit_map = {q1: q2}
    before = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z, q1: alphaclops.Y}), exponent_neg=0.1)
    with pytest.raises(ValueError, match="have a key"):
        _ = before.map_qubits(qubit_map)


def test_pow():
    a = alphaclops.LineQubit(0)
    s = alphaclops.PauliString({a: alphaclops.X})
    p = alphaclops.PauliStringPhasor(s, exponent_neg=0.25, exponent_pos=0.5)
    assert p ** 0.5 == alphaclops.PauliStringPhasor(s, exponent_neg=0.125, exponent_pos=0.25)
    with pytest.raises(TypeError, match='unsupported operand'):
        _ = p ** object()
    assert p**1 == p
    p = alphaclops.PauliStringPhasor(s, qubits=[a], exponent_neg=0.25, exponent_pos=0.5)
    assert p ** 0.5 == alphaclops.PauliStringPhasor(s, exponent_neg=0.125, exponent_pos=0.25)


def test_consistent():
    a, b = alphaclops.LineQubit.range(2)
    op = np.exp(1j * np.pi / 2 * alphaclops.X(a) * alphaclops.X(b))
    alphaclops.testing.assert_implements_consistent_protocols(op)
    p = alphaclops.PauliStringPhasor(alphaclops.X(a), qubits=[a], exponent_neg=0.25, exponent_pos=0.5)
    alphaclops.testing.assert_implements_consistent_protocols(p)


def test_pass_operations_over():
    q0, q1 = _make_qubits(2)
    op = alphaclops.SingleQubitCliffordGate.from_double_map(
        {alphaclops.Z: (alphaclops.X, False), alphaclops.X: (alphaclops.Z, False)}
    )(q0)
    ps_before = alphaclops.PauliString({q0: alphaclops.X, q1: alphaclops.Y}, -1)
    ps_after = alphaclops.PauliString({q0: alphaclops.Z, q1: alphaclops.Y}, -1)
    before = alphaclops.PauliStringPhasor(ps_before, exponent_neg=0.1)
    after = alphaclops.PauliStringPhasor(ps_after, exponent_neg=0.1)
    assert before.pass_operations_over([op]) == after
    assert after.pass_operations_over([op], after_to_before=True) == before


def test_extrapolate_effect():
    op1 = alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=0.5)
    op2 = alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=1.5)
    op3 = alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=0.125)
    assert op1**3 == op2
    assert op1**0.25 == op3


def test_extrapolate_effect_with_symbol():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(
        alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=sympy.Symbol('a')),
        alphaclops.PauliStringPhasor(alphaclops.PauliString({})) ** sympy.Symbol('a'),
    )
    eq.add_equality_group(alphaclops.PauliStringPhasor(alphaclops.PauliString({})) ** sympy.Symbol('b'))
    eq.add_equality_group(
        alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=0.5) ** sympy.Symbol('b')
    )
    eq.add_equality_group(
        alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=sympy.Symbol('a')) ** 0.5
    )
    eq.add_equality_group(
        alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=sympy.Symbol('a'))
        ** sympy.Symbol('b')
    )


def test_inverse():
    i = alphaclops.PauliString({})
    op1 = alphaclops.PauliStringPhasor(i, exponent_neg=0.25)
    op2 = alphaclops.PauliStringPhasor(i, exponent_neg=-0.25)
    op3 = alphaclops.PauliStringPhasor(i, exponent_neg=sympy.Symbol('s'))
    op4 = alphaclops.PauliStringPhasor(i, exponent_neg=-sympy.Symbol('s'))
    assert alphaclops.inverse(op1) == op2
    assert alphaclops.inverse(op3, None) == op4


def test_can_merge_with():
    q0, q1 = _make_qubits(2)

    op1 = alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=0.25)
    op2 = alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=0.75)
    assert op1.can_merge_with(op2)

    op1 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, +1), exponent_neg=0.25)
    op2 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, -1), exponent_neg=0.75)
    assert op1.can_merge_with(op2)

    op1 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, +1), exponent_neg=0.25)
    op2 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Y}, -1), exponent_neg=0.75)
    assert not op1.can_merge_with(op2)

    op1 = alphaclops.PauliStringPhasor(
        alphaclops.PauliString({q0: alphaclops.X}, +1), qubits=[q0, q1], exponent_neg=0.25
    )
    op2 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, -1), exponent_neg=0.75)
    assert not op1.can_merge_with(op2)


def test_merge_with():
    (q0,) = _make_qubits(1)

    op1 = alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=0.25)
    op2 = alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=0.75)
    op12 = alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=1.0)
    assert op1.merged_with(op2).equal_up_to_global_phase(op12)

    op1 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, +1), exponent_neg=0.25)
    op2 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, +1), exponent_neg=0.75)
    op12 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, +1), exponent_neg=1.0)
    assert op1.merged_with(op2).equal_up_to_global_phase(op12)

    op1 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, +1), exponent_neg=0.25)
    op2 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, -1), exponent_neg=0.75)
    op12 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, +1), exponent_neg=-0.5)
    assert op1.merged_with(op2).equal_up_to_global_phase(op12)

    op1 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, -1), exponent_neg=0.25)
    op2 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, +1), exponent_neg=0.75)
    op12 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, -1), exponent_neg=-0.5)
    assert op1.merged_with(op2).equal_up_to_global_phase(op12)

    op1 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, -1), exponent_neg=0.25)
    op2 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, -1), exponent_neg=0.75)
    op12 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, -1), exponent_neg=1.0)
    assert op1.merged_with(op2).equal_up_to_global_phase(op12)

    op1 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, +1), exponent_neg=0.25)
    op2 = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Y}, -1), exponent_neg=0.75)
    with pytest.raises(ValueError):
        op1.merged_with(op2)


def test_is_parameterized():
    op = alphaclops.PauliStringPhasor(alphaclops.PauliString({}))
    assert not alphaclops.is_parameterized(op)
    assert not alphaclops.is_parameterized(op ** 0.1)
    assert alphaclops.is_parameterized(op ** sympy.Symbol('a'))


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_with_parameters_resolved_by(resolve_fn):
    op = alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=sympy.Symbol('a'))
    resolver = alphaclops.ParamResolver({'a': 0.1})
    actual = resolve_fn(op, resolver)
    expected = alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_neg=0.1)
    assert actual == expected

    with pytest.raises(ValueError, match='complex'):
        resolve_fn(op, alphaclops.ParamResolver({'a': 0.1j}))
    op = alphaclops.PauliStringPhasor(alphaclops.PauliString({}), exponent_pos=sympy.Symbol('a'))
    with pytest.raises(ValueError, match='complex'):
        resolve_fn(op, alphaclops.ParamResolver({'a': 0.1j}))


def test_drop_negligible():
    (q0,) = _make_qubits(1)
    sym = sympy.Symbol('a')
    circuit = alphaclops.Circuit(
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z})) ** 0.25,
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z})) ** 1e-10,
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z})) ** sym,
    )
    expected = alphaclops.Circuit(
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z})) ** 0.25,
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z})) ** sym,
    )
    circuit = alphaclops.drop_negligible_operations(circuit)
    circuit = alphaclops.drop_empty_moments(circuit)
    assert circuit == expected


def test_manual_default_decompose():
    q0, q1, q2 = _make_qubits(3)

    mat = alphaclops.Circuit(
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z})) ** 0.25, alphaclops.Z(q0) ** -0.25
    ).unitary()
    alphaclops.testing.assert_allclose_up_to_global_phase(mat, np.eye(2), rtol=1e-7, atol=1e-7)

    mat = alphaclops.Circuit(
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Y})) ** 0.25, alphaclops.Y(q0) ** -0.25
    ).unitary()
    alphaclops.testing.assert_allclose_up_to_global_phase(mat, np.eye(2), rtol=1e-7, atol=1e-7)

    mat = alphaclops.Circuit(
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z, q1: alphaclops.Z, q2: alphaclops.Z}))
    ).unitary()
    alphaclops.testing.assert_allclose_up_to_global_phase(
        mat, np.diag([1, -1, -1, 1, -1, 1, 1, -1]), rtol=1e-7, atol=1e-7
    )

    mat = alphaclops.Circuit(
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z, q1: alphaclops.Y, q2: alphaclops.X})) ** 0.5
    ).unitary()
    alphaclops.testing.assert_allclose_up_to_global_phase(
        mat,
        np.array(
            [
                [1, 0, 0, -1, 0, 0, 0, 0],
                [0, 1, -1, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0, 0],
                [1, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 1],
                [0, 0, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, -1, 1, 0],
                [0, 0, 0, 0, -1, 0, 0, 1],
            ]
        )
        / np.sqrt(2),
        rtol=1e-7,
        atol=1e-7,
    )


@pytest.mark.parametrize(
    'paulis,phase_exponent_negative,sign',
    itertools.product(
        itertools.product((alphaclops.X, alphaclops.Y, alphaclops.Z, None), repeat=3),
        (0, 0.1, 0.5, 1, -0.25),
        (+1, -1),
    ),
)
def test_default_decompose(paulis, phase_exponent_negative: float, sign: int):
    paulis = [pauli for pauli in paulis if pauli is not None]
    qubits = _make_qubits(len(paulis))

    # Get matrix from decomposition
    pauli_string = alphaclops.PauliString(
        qubit_pauli_map={q: p for q, p in zip(qubits, paulis)}, coefficient=sign
    )
    actual = alphaclops.Circuit(
        alphaclops.PauliStringPhasor(pauli_string, exponent_neg=phase_exponent_negative)
    ).unitary()

    # Calculate expected matrix
    to_z_mats = {
        alphaclops.X: alphaclops.unitary(alphaclops.Y ** -0.5),
        alphaclops.Y: alphaclops.unitary(alphaclops.X ** 0.5),
        alphaclops.Z: np.eye(2),
    }
    expected_convert = np.eye(1)
    for pauli in paulis:
        expected_convert = np.kron(expected_convert, to_z_mats[pauli])
    t = 1j ** (phase_exponent_negative * 2 * sign)
    expected_z = np.diag([1, t, t, 1, t, 1, 1, t][: 2 ** len(paulis)])
    expected = expected_convert.T.conj().dot(expected_z).dot(expected_convert)

    alphaclops.testing.assert_allclose_up_to_global_phase(actual, expected, rtol=1e-7, atol=1e-7)


def test_decompose_with_symbol():
    (q0,) = _make_qubits(1)
    ps = alphaclops.PauliString({q0: alphaclops.Y})
    op = alphaclops.PauliStringPhasor(ps, exponent_neg=sympy.Symbol('a'))
    circuit = alphaclops.Circuit(op)
    circuit = alphaclops.expand_composite(circuit)
    alphaclops.testing.assert_has_diagram(circuit, "q0: ───X^0.5───Z^a───X^-0.5───")

    ps = alphaclops.PauliString({q0: alphaclops.Y}, -1)
    op = alphaclops.PauliStringPhasor(ps, exponent_neg=sympy.Symbol('a'))
    circuit = alphaclops.Circuit(op)
    circuit = alphaclops.expand_composite(circuit)
    alphaclops.testing.assert_has_diagram(circuit, "q0: ───X^0.5───X───Z^a───X───X^-0.5───")


def test_text_diagram():
    q0, q1, q2 = _make_qubits(3)
    circuit = alphaclops.Circuit(
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z})),
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Y})) ** 0.25,
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z, q1: alphaclops.Z, q2: alphaclops.Z})),
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z, q1: alphaclops.Y, q2: alphaclops.X}, -1)) ** 0.5,
        alphaclops.PauliStringPhasor(
            alphaclops.PauliString({q0: alphaclops.Z, q1: alphaclops.Y, q2: alphaclops.X}), exponent_neg=sympy.Symbol('a')
        ),
        alphaclops.PauliStringPhasor(
            alphaclops.PauliString({q0: alphaclops.Z, q1: alphaclops.Y, q2: alphaclops.X}, -1),
            exponent_neg=sympy.Symbol('b'),
        ),
        alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.Z}), qubits=[q0, q1], exponent_neg=0.5),
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
q0: ───[Z]───[Y]^0.25───[Z]───[Z]────────[Z]─────[Z]────────[Z]───────
                        │     │          │       │          │
q1: ────────────────────[Z]───[Y]────────[Y]─────[Y]────────[I]^0.5───
                        │     │          │       │
q2: ────────────────────[Z]───[X]^-0.5───[X]^a───[X]^(-b)─────────────
""",
    )


def test_repr():
    q0, q1, q2 = _make_qubits(3)
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.PauliStringPhasor(
            alphaclops.PauliString({q2: alphaclops.Z, q1: alphaclops.Y, q0: alphaclops.X}),
            exponent_neg=0.5,
            exponent_pos=0.25,
        )
    )
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.PauliStringPhasor(
            -alphaclops.PauliString({q1: alphaclops.Y, q0: alphaclops.X}), exponent_neg=-0.5, exponent_pos=0.25
        )
    )


def test_str():
    q0, q1, q2 = _make_qubits(3)
    ps = alphaclops.PauliStringPhasor(alphaclops.PauliString({q2: alphaclops.Z, q1: alphaclops.Y, q0: alphaclops.X}, +1)) ** 0.5
    assert str(ps) == '(X(q0)*Y(q1)*Z(q2))**0.5'

    ps = alphaclops.PauliStringPhasor(alphaclops.PauliString({q2: alphaclops.Z, q1: alphaclops.Y, q0: alphaclops.X}, +1)) ** -0.5
    assert str(ps) == '(X(q0)*Y(q1)*Z(q2))**-0.5'

    ps = alphaclops.PauliStringPhasor(alphaclops.PauliString({q2: alphaclops.Z, q1: alphaclops.Y, q0: alphaclops.X}, -1)) ** -0.5
    assert str(ps) == '(X(q0)*Y(q1)*Z(q2))**0.5'

    assert str(np.exp(0.5j * np.pi * alphaclops.X(q0) * alphaclops.Y(q1))) == 'exp(iπ0.5*X(q0)*Y(q1))'
    assert str(np.exp(-0.25j * np.pi * alphaclops.X(q0) * alphaclops.Y(q1))) == 'exp(-iπ0.25*X(q0)*Y(q1))'
    assert str(np.exp(0.5j * np.pi * alphaclops.PauliString())) == 'exp(iπ0.5*I)'

    ps = alphaclops.PauliStringPhasor(alphaclops.PauliString({q0: alphaclops.X}, +1), qubits=[q0, q1]) ** 0.5
    assert str(ps) == '(X(q0))**0.5'


def test_old_json():
    """Older versions of PauliStringPhasor did not have a qubit field."""
    old_json = """
    {
      "alphaclops_type": "PauliStringPhasor",
      "pauli_string": {
        "alphaclops_type": "PauliString",
        "qubit_pauli_map": [
          [
            {
              "alphaclops_type": "LineQubit",
              "x": 0
            },
            {
              "alphaclops_type": "_PauliX",
              "exponent": 1.0,
              "global_shift": 0.0
            }
          ],
          [
            {
              "alphaclops_type": "LineQubit",
              "x": 1
            },
            {
              "alphaclops_type": "_PauliY",
              "exponent": 1.0,
              "global_shift": 0.0
            }
          ],
          [
            {
              "alphaclops_type": "LineQubit",
              "x": 2
            },
            {
              "alphaclops_type": "_PauliZ",
              "exponent": 1.0,
              "global_shift": 0.0
            }
          ]
        ],
        "coefficient": {
          "alphaclops_type": "complex",
          "real": 1.0,
          "imag": 0.0
        }
      },
      "exponent_neg": 0.2,
      "exponent_pos": 0.1
    }
    """
    phasor = alphaclops.read_json(json_text=old_json)
    assert phasor == alphaclops.PauliStringPhasor(
        (
                (1 + 0j)
                * alphaclops.X(alphaclops.LineQubit(0))
                * alphaclops.Y(alphaclops.LineQubit(1))
                * alphaclops.Z(alphaclops.LineQubit(2))
        ),
        qubits=(alphaclops.LineQubit(0), alphaclops.LineQubit(1), alphaclops.LineQubit(2)),
        exponent_neg=0.2,
        exponent_pos=0.1,
    )


def test_gate_init():
    a = alphaclops.LineQubit(0)
    with pytest.raises(ValueError, match='eigenvalues'):
        _ = alphaclops.PauliStringPhasorGate(1j * alphaclops.X(a))

    v1 = alphaclops.PauliStringPhasorGate(
        alphaclops.DensePauliString('X', coefficient=-1), exponent_neg=0.25, exponent_pos=-0.5
    )
    assert v1.dense_pauli_string == dps_x
    assert v1.exponent_neg == -0.5
    assert v1.exponent_pos == 0.25

    v2 = alphaclops.PauliStringPhasorGate(dps_x, exponent_neg=0.75, exponent_pos=-0.125)
    assert v2.dense_pauli_string == dps_x
    assert v2.exponent_neg == 0.75
    assert v2.exponent_pos == -0.125


def test_gate_on():
    q = alphaclops.LineQubit(0)
    g1 = alphaclops.PauliStringPhasorGate(
        alphaclops.DensePauliString('X', coefficient=-1), exponent_neg=0.25, exponent_pos=-0.5
    )

    op1 = g1.on(q)
    assert isinstance(op1, alphaclops.PauliStringPhasor)
    assert op1.qubits == (q,)
    assert op1.gate == g1
    assert op1.pauli_string == dps_x.on(q)
    assert op1.exponent_neg == -0.5
    assert op1.exponent_pos == 0.25

    g2 = alphaclops.PauliStringPhasorGate(dps_x, exponent_neg=0.75, exponent_pos=-0.125)
    op2 = g2.on(q)
    assert isinstance(op2, alphaclops.PauliStringPhasor)
    assert op2.qubits == (q,)
    assert op2.gate == g2
    assert op2.pauli_string == dps_x.on(q)
    assert op2.exponent_neg == 0.75
    assert op2.exponent_pos == -0.125


def test_gate_eq_ne_hash():
    eq = alphaclops.testing.EqualsTester()
    dps_xyx = alphaclops.DensePauliString('XYX')
    eq.make_equality_group(
        lambda: alphaclops.PauliStringPhasorGate(dps_empty, exponent_neg=0.5),
        lambda: alphaclops.PauliStringPhasorGate(dps_empty, exponent_neg=-1.5),
        lambda: alphaclops.PauliStringPhasorGate(dps_empty, exponent_neg=2.5),
    )
    eq.make_equality_group(lambda: alphaclops.PauliStringPhasorGate(-dps_empty, exponent_neg=-0.5))
    eq.add_equality_group(
        alphaclops.PauliStringPhasorGate(dps_xyz), alphaclops.PauliStringPhasorGate(dps_xyz, exponent_neg=1)
    )
    eq.add_equality_group(alphaclops.PauliStringPhasorGate(-dps_xyz, exponent_neg=1))
    eq.add_equality_group(
        alphaclops.PauliStringPhasorGate(dps_xyx), alphaclops.PauliStringPhasorGate(dps_xyx, exponent_neg=1)
    )
    eq.add_equality_group(
        alphaclops.PauliStringPhasorGate(dps_xy), alphaclops.PauliStringPhasorGate(dps_xy, exponent_neg=1)
    )
    eq.add_equality_group(
        alphaclops.PauliStringPhasorGate(dps_yx), alphaclops.PauliStringPhasorGate(dps_yx, exponent_neg=1)
    )
    eq.add_equality_group(alphaclops.PauliStringPhasorGate(-dps_xyx, exponent_neg=1))
    eq.add_equality_group(alphaclops.PauliStringPhasorGate(dps_xyx, exponent_neg=0.5))
    eq.add_equality_group(alphaclops.PauliStringPhasorGate(-dps_xyx, exponent_neg=-0.5))
    eq.add_equality_group(alphaclops.PauliStringPhasorGate(dps_xyz, exponent_neg=sympy.Symbol('a')))


def test_gate_equal_up_to_global_phase():
    groups = [
        [
            alphaclops.PauliStringPhasorGate(dps_x, exponent_neg=0.25),
            alphaclops.PauliStringPhasorGate(dps_x, exponent_neg=0, exponent_pos=-0.25),
            alphaclops.PauliStringPhasorGate(dps_x, exponent_pos=-0.125, exponent_neg=0.125),
        ],
        [alphaclops.PauliStringPhasorGate(dps_x)],
        [alphaclops.PauliStringPhasorGate(dps_y, exponent_neg=0.25)],
        [alphaclops.PauliStringPhasorGate(dps_xy, exponent_neg=0.25)],
    ]
    for g1 in groups:
        for e1 in g1:
            assert not e1.equal_up_to_global_phase("not even close")
            for g2 in groups:
                for e2 in g2:
                    assert e1.equal_up_to_global_phase(e2) == (g1 is g2)


def test_gate_pow():
    s = dps_x
    p = alphaclops.PauliStringPhasorGate(s, exponent_neg=0.25, exponent_pos=0.5)
    assert p ** 0.5 == alphaclops.PauliStringPhasorGate(s, exponent_neg=0.125, exponent_pos=0.25)
    with pytest.raises(TypeError, match='unsupported operand'):
        _ = p ** object()
    assert p**1 == p


def test_gate_extrapolate_effect():
    gate1 = alphaclops.PauliStringPhasorGate(dps_empty, exponent_neg=0.5)
    gate2 = alphaclops.PauliStringPhasorGate(dps_empty, exponent_neg=1.5)
    gate3 = alphaclops.PauliStringPhasorGate(dps_empty, exponent_neg=0.125)
    assert gate1**3 == gate2
    assert gate1**0.25 == gate3


def test_gate_extrapolate_effect_with_symbol():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(
        alphaclops.PauliStringPhasorGate(dps_empty, exponent_neg=sympy.Symbol('a')),
        alphaclops.PauliStringPhasorGate(dps_empty) ** sympy.Symbol('a'),
    )
    eq.add_equality_group(alphaclops.PauliStringPhasorGate(dps_empty) ** sympy.Symbol('b'))
    eq.add_equality_group(
        alphaclops.PauliStringPhasorGate(dps_empty, exponent_neg=0.5) ** sympy.Symbol('b')
    )
    eq.add_equality_group(
        alphaclops.PauliStringPhasorGate(dps_empty, exponent_neg=sympy.Symbol('a')) ** 0.5
    )
    eq.add_equality_group(
        alphaclops.PauliStringPhasorGate(dps_empty, exponent_neg=sympy.Symbol('a')) ** sympy.Symbol('b')
    )


def test_gate_inverse():
    i = dps_empty
    gate1 = alphaclops.PauliStringPhasorGate(i, exponent_neg=0.25)
    gate2 = alphaclops.PauliStringPhasorGate(i, exponent_neg=-0.25)
    gate3 = alphaclops.PauliStringPhasorGate(i, exponent_neg=sympy.Symbol('s'))
    gate4 = alphaclops.PauliStringPhasorGate(i, exponent_neg=-sympy.Symbol('s'))
    assert alphaclops.inverse(gate1) == gate2
    assert alphaclops.inverse(gate3, None) == gate4


def test_gate_is_parameterized():
    gate = alphaclops.PauliStringPhasorGate(dps_empty)
    assert not alphaclops.is_parameterized(gate)
    assert not alphaclops.is_parameterized(gate ** 0.1)
    assert alphaclops.is_parameterized(gate ** sympy.Symbol('a'))


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_gate_with_parameters_resolved_by(resolve_fn):
    gate = alphaclops.PauliStringPhasorGate(dps_empty, exponent_neg=sympy.Symbol('a'))
    resolver = alphaclops.ParamResolver({'a': 0.1})
    actual = resolve_fn(gate, resolver)
    expected = alphaclops.PauliStringPhasorGate(dps_empty, exponent_neg=0.1)
    assert actual == expected


def test_gate_repr():
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.PauliStringPhasorGate(dps_zyx, exponent_neg=0.5, exponent_pos=0.25)
    )
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.PauliStringPhasorGate(-dps_yx, exponent_neg=-0.5, exponent_pos=0.25)
    )


def test_gate_str():
    gate = alphaclops.PauliStringPhasorGate(alphaclops.DensePauliString('ZYX', coefficient=+1)) ** 0.5
    assert str(gate) == '(+ZYX)**0.5'

    gate = alphaclops.PauliStringPhasorGate(alphaclops.DensePauliString('ZYX', coefficient=+1)) ** -0.5
    assert str(gate) == '(+ZYX)**-0.5'

    gate = alphaclops.PauliStringPhasorGate(alphaclops.DensePauliString('ZYX', coefficient=-1)) ** -0.5
    assert str(gate) == '(+ZYX)**0.5'

    gate = alphaclops.PauliStringPhasorGate(
        alphaclops.DensePauliString('ZYX'), exponent_pos=0.5, exponent_neg=-0.5
    )
    assert str(gate) == 'exp(iπ0.5*+ZYX)'

    gate = (
            alphaclops.PauliStringPhasorGate(
            alphaclops.DensePauliString('ZYX'), exponent_pos=0.5, exponent_neg=-0.5
        )
            ** -0.5
    )
    assert str(gate) == 'exp(-iπ0.25*+ZYX)'
