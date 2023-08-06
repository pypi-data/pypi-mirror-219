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
import re

import numpy as np
import pytest
import sympy

import alphaclops

H = np.array([[1, 1], [1, -1]]) * np.sqrt(0.5)
HH = alphaclops.kron(H, H)
QFT2 = np.array([[1, 1, 1, 1], [1, 1j, -1, -1j], [1, -1, 1, -1], [1, -1j, -1, 1j]]) * 0.5
PLUS_ONE = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])


def test_single_qubit_init():
    m = np.array([[1, 1j], [1j, 1]]) * np.sqrt(0.5)
    x2 = alphaclops.MatrixGate(m)
    assert alphaclops.has_unitary(x2)
    assert np.all(alphaclops.unitary(x2) == m)
    assert alphaclops.qid_shape(x2) == (2,)

    x2 = alphaclops.MatrixGate(PLUS_ONE, qid_shape=(3,))
    assert alphaclops.has_unitary(x2)
    assert np.all(alphaclops.unitary(x2) == PLUS_ONE)
    assert alphaclops.qid_shape(x2) == (3,)

    with pytest.raises(ValueError, match='Not a .*unitary matrix'):
        alphaclops.MatrixGate(np.zeros((2, 2)))
    with pytest.raises(ValueError, match='must be a square 2d numpy array'):
        alphaclops.MatrixGate(alphaclops.eye_tensor((2, 2), dtype=float))
    with pytest.raises(ValueError, match='must be a square 2d numpy array'):
        alphaclops.MatrixGate(np.ones((3, 4)))
    with pytest.raises(ValueError, match='must be a square 2d numpy array'):
        alphaclops.MatrixGate(np.ones((2, 2, 2)))


def test_single_qubit_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.make_equality_group(lambda: alphaclops.MatrixGate(np.eye(2)))
    eq.make_equality_group(lambda: alphaclops.MatrixGate(np.array([[0, 1], [1, 0]])))
    x2 = np.array([[1, 1j], [1j, 1]]) * np.sqrt(0.5)
    eq.make_equality_group(lambda: alphaclops.MatrixGate(x2))
    eq.add_equality_group(alphaclops.MatrixGate(PLUS_ONE, qid_shape=(3,)))


def test_single_qubit_trace_distance_bound():
    x = alphaclops.MatrixGate(np.array([[0, 1], [1, 0]]))
    x2 = alphaclops.MatrixGate(np.array([[1, 1j], [1j, 1]]) * np.sqrt(0.5))
    assert alphaclops.trace_distance_bound(x) >= 1
    assert alphaclops.trace_distance_bound(x2) >= 0.5


def test_single_qubit_approx_eq():
    x = alphaclops.MatrixGate(np.array([[0, 1], [1, 0]]))
    i = alphaclops.MatrixGate(np.array([[1, 0], [0, 1]]))
    i_ish = alphaclops.MatrixGate(np.array([[1, 0.000000000000001], [0, 1]]))
    assert alphaclops.approx_eq(i, i_ish, atol=1e-9)
    assert alphaclops.approx_eq(i, i, atol=1e-9)
    assert not alphaclops.approx_eq(i, x, atol=1e-9)
    assert not alphaclops.approx_eq(i, '', atol=1e-9)


def test_single_qubit_extrapolate():
    i = alphaclops.MatrixGate(np.eye(2))
    x = alphaclops.MatrixGate(np.array([[0, 1], [1, 0]]))
    x2 = alphaclops.MatrixGate(np.array([[1, 1j], [1j, 1]]) * (1 - 1j) / 2)
    assert alphaclops.has_unitary(x2)
    x2i = alphaclops.MatrixGate(np.conj(alphaclops.unitary(x2).T))

    assert alphaclops.approx_eq(x ** 0, i, atol=1e-9)
    assert alphaclops.approx_eq(x2 ** 0, i, atol=1e-9)
    assert alphaclops.approx_eq(x2 ** 2, x, atol=1e-9)
    assert alphaclops.approx_eq(x2 ** -1, x2i, atol=1e-9)
    assert alphaclops.approx_eq(x2 ** 3, x2i, atol=1e-9)
    assert alphaclops.approx_eq(x ** -1, x, atol=1e-9)

    z2 = alphaclops.MatrixGate(np.array([[1, 0], [0, 1j]]))
    z4 = alphaclops.MatrixGate(np.array([[1, 0], [0, (1 + 1j) * np.sqrt(0.5)]]))
    assert alphaclops.approx_eq(z2 ** 0.5, z4, atol=1e-9)
    with pytest.raises(TypeError):
        _ = x ** sympy.Symbol('a')


def test_two_qubit_init():
    x2 = alphaclops.MatrixGate(QFT2)
    assert alphaclops.has_unitary(x2)
    assert np.all(alphaclops.unitary(x2) == QFT2)


def test_two_qubit_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.make_equality_group(lambda: alphaclops.MatrixGate(np.eye(4)))
    eq.make_equality_group(lambda: alphaclops.MatrixGate(QFT2))
    eq.make_equality_group(lambda: alphaclops.MatrixGate(HH))


def test_two_qubit_approx_eq():
    f = alphaclops.MatrixGate(QFT2)
    perturb = np.zeros(shape=QFT2.shape, dtype=np.float64)
    perturb[1, 2] = 1e-8

    assert alphaclops.approx_eq(f, alphaclops.MatrixGate(QFT2), atol=1e-9)

    assert not alphaclops.approx_eq(f, alphaclops.MatrixGate(QFT2 + perturb), atol=1e-9)
    assert alphaclops.approx_eq(f, alphaclops.MatrixGate(QFT2 + perturb), atol=1e-7)

    assert not alphaclops.approx_eq(f, alphaclops.MatrixGate(HH), atol=1e-9)


def test_two_qubit_extrapolate():
    cz2 = alphaclops.MatrixGate(np.diag([1, 1, 1, 1j]))
    cz4 = alphaclops.MatrixGate(np.diag([1, 1, 1, (1 + 1j) * np.sqrt(0.5)]))
    i = alphaclops.MatrixGate(np.eye(4))

    assert alphaclops.approx_eq(cz2 ** 0, i, atol=1e-9)
    assert alphaclops.approx_eq(cz4 ** 0, i, atol=1e-9)
    assert alphaclops.approx_eq(cz2 ** 0.5, cz4, atol=1e-9)
    with pytest.raises(TypeError):
        _ = cz2 ** sympy.Symbol('a')


def test_single_qubit_diagram():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    m = np.array([[1, 1j], [1j, 1]]) * np.sqrt(0.5)
    c = alphaclops.Circuit(alphaclops.MatrixGate(m).on(a), alphaclops.CZ(a, b))

    assert re.match(
        r"""
      ┌[          ]+┐
a: ───│[0-9\.+\-j ]+│───@───
      │[0-9\.+\-j ]+│   │
      └[          ]+┘   │
       [          ]+    │
b: ────[──────────]+────@───
    """.strip(),
        c.to_text_diagram().strip(),
    )

    assert re.match(
        r"""
a[          ]+  b
│[          ]+  │
┌[          ]+┐ │
│[0-9\.+\-j ]+│ │
│[0-9\.+\-j ]+│ │
└[          ]+┘ │
│[          ]+  │
@[──────────]+──@
│[          ]+  │
    """.strip(),
        c.to_text_diagram(transpose=True).strip(),
    )


def test_two_qubit_diagram():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')
    c = alphaclops.Circuit(
        alphaclops.MatrixGate(alphaclops.unitary(alphaclops.CZ)).on(a, b),
        alphaclops.MatrixGate(alphaclops.unitary(alphaclops.CZ)).on(c, a),
    )
    assert re.match(
        r"""
      ┌[          ]+┐
      │[0-9\.+\-j ]+│
a: ───│[0-9\.+\-j ]+│───#2─+
      │[0-9\.+\-j ]+│   │
      │[0-9\.+\-j ]+│   │
      └[          ]+┘   │
      │[          ]+    │
b: ───#2[─────────]+────┼──+
       [          ]+    │
       [          ]+    ┌[          ]+┐
       [          ]+    │[0-9\.+\-j ]+│
c: ────[──────────]+────│[0-9\.+\-j ]+│──+
       [          ]+    │[0-9\.+\-j ]+│
       [          ]+    │[0-9\.+\-j ]+│
       [          ]+    └[          ]+┘
    """.strip(),
        c.to_text_diagram().strip(),
    )

    assert re.match(
        r"""
a[          ]+  b  c
│[          ]+  │  │
┌[          ]+┐ │  │
│[0-9\.+\-j ]+│ │  │
│[0-9\.+\-j ]+│─#2 │
│[0-9\.+\-j ]+│ │  │
│[0-9\.+\-j ]+│ │  │
└[          ]+┘ │  │
│[          ]+  │  │
│[          ]+  │  ┌[          ]+┐
│[          ]+  │  │[0-9\.+\-j ]+│
#2[─────────]+──┼──│[0-9\.+\-j ]+│
│[          ]+  │  │[0-9\.+\-j ]+│
│[          ]+  │  │[0-9\.+\-j ]+│
│[          ]+  │  └[          ]+┘
│[          ]+  │  │
    """.strip(),
        c.to_text_diagram(transpose=True).strip(),
    )


def test_named_single_qubit_diagram():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    m = np.array([[1, 1j], [1j, 1]]) * np.sqrt(0.5)
    c = alphaclops.Circuit(alphaclops.MatrixGate(m, name='Foo').on(a), alphaclops.CZ(a, b))

    expected_horizontal = """
a: ───Foo───@───
            │
b: ─────────@───
    """.strip()
    assert expected_horizontal == c.to_text_diagram().strip()

    expected_vertical = """
a   b
│   │
Foo │
│   │
@───@
│   │
    """.strip()
    assert expected_vertical == c.to_text_diagram(transpose=True).strip()


def test_named_two_qubit_diagram():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')
    c = alphaclops.Circuit(
        alphaclops.MatrixGate(alphaclops.unitary(alphaclops.CZ), name='Foo').on(a, b),
        alphaclops.MatrixGate(alphaclops.unitary(alphaclops.CZ), name='Bar').on(c, a),
    )

    expected_horizontal = """
a: ───Foo[1]───Bar[2]───
      │        │
b: ───Foo[2]───┼────────
               │
c: ────────────Bar[1]───
    """.strip()
    assert expected_horizontal == c.to_text_diagram().strip()

    expected_vertical = """
a      b      c
│      │      │
Foo[1]─Foo[2] │
│      │      │
Bar[2]─┼──────Bar[1]
│      │      │
    """.strip()
    assert expected_vertical == c.to_text_diagram(transpose=True).strip()


def test_with_name():
    gate = alphaclops.MatrixGate(alphaclops.unitary(alphaclops.Z ** 0.25))
    T = gate.with_name('T')
    S = (T**2).with_name('S')
    assert T._name == 'T'
    np.testing.assert_allclose(alphaclops.unitary(T), alphaclops.unitary(gate))
    assert S._name == 'S'
    np.testing.assert_allclose(alphaclops.unitary(S), alphaclops.unitary(T ** 2))


def test_str_executes():
    assert '1' in str(alphaclops.MatrixGate(np.eye(2)))
    assert '0' in str(alphaclops.MatrixGate(np.eye(4)))


@pytest.mark.parametrize('n', [1, 2, 3, 4, 5])
def test_implements_consistent_protocols(n):
    u = alphaclops.testing.random_unitary(2 ** n)
    g1 = alphaclops.MatrixGate(u)
    alphaclops.testing.assert_implements_consistent_protocols(g1, ignoring_global_phase=True)
    alphaclops.testing.assert_decompose_ends_at_default_gateset(g1)

    if n == 1:
        return

    g2 = alphaclops.MatrixGate(u, qid_shape=(4,) + (2,) * (n - 2))
    alphaclops.testing.assert_implements_consistent_protocols(g2, ignoring_global_phase=True)
    alphaclops.testing.assert_decompose_ends_at_default_gateset(g2)


def test_repr():
    alphaclops.testing.assert_equivalent_repr(alphaclops.MatrixGate(alphaclops.testing.random_unitary(2)))
    alphaclops.testing.assert_equivalent_repr(alphaclops.MatrixGate(alphaclops.testing.random_unitary(4)))


def test_matrix_gate_init_validation():
    with pytest.raises(ValueError, match='square 2d numpy array'):
        _ = alphaclops.MatrixGate(np.ones(shape=(1, 1, 1)))
    with pytest.raises(ValueError, match='square 2d numpy array'):
        _ = alphaclops.MatrixGate(np.ones(shape=(2, 1)))
    with pytest.raises(ValueError, match='not a power of 2'):
        _ = alphaclops.MatrixGate(np.ones(shape=(0, 0)))
    with pytest.raises(ValueError, match='not a power of 2'):
        _ = alphaclops.MatrixGate(np.eye(3))
    with pytest.raises(ValueError, match='matrix shape for qid_shape'):
        _ = alphaclops.MatrixGate(np.eye(3), qid_shape=(4,))


def test_matrix_gate_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(alphaclops.MatrixGate(np.eye(1)))
    eq.add_equality_group(alphaclops.MatrixGate(-np.eye(1)))
    eq.add_equality_group(alphaclops.MatrixGate(np.diag([1, 1, 1, 1, 1, -1]), qid_shape=(2, 3)))
    eq.add_equality_group(alphaclops.MatrixGate(np.diag([1, 1, 1, 1, 1, -1]), qid_shape=(3, 2)))


def test_matrix_gate_pow():
    t = sympy.Symbol('t')
    assert alphaclops.pow(alphaclops.MatrixGate(1j * np.eye(1)), t, default=None) is None
    assert alphaclops.pow(alphaclops.MatrixGate(1j * np.eye(1)), 2) == alphaclops.MatrixGate(-np.eye(1))

    m = alphaclops.MatrixGate(np.diag([1, 1j, -1]), qid_shape=(3,))
    assert m ** 3 == alphaclops.MatrixGate(np.diag([1, -1j, -1]), qid_shape=(3,))


def test_phase_by():
    # Single qubit case.
    x = alphaclops.MatrixGate(alphaclops.unitary(alphaclops.X))
    y = alphaclops.phase_by(x, 0.25, 0)
    alphaclops.testing.assert_allclose_up_to_global_phase(
        alphaclops.unitary(y), alphaclops.unitary(alphaclops.Y), atol=1e-8
    )

    # Two qubit case. Commutes with control.
    cx = alphaclops.MatrixGate(alphaclops.unitary(alphaclops.X.controlled(1)))
    cx2 = alphaclops.phase_by(cx, 0.25, 0)
    alphaclops.testing.assert_allclose_up_to_global_phase(alphaclops.unitary(cx2), alphaclops.unitary(cx), atol=1e-8)

    # Two qubit case. Doesn't commute with target.
    cy = alphaclops.phase_by(cx, 0.25, 1)
    alphaclops.testing.assert_allclose_up_to_global_phase(
        alphaclops.unitary(cy), alphaclops.unitary(alphaclops.Y.controlled(1)), atol=1e-8
    )

    m = alphaclops.MatrixGate(np.eye(3), qid_shape=[3])
    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = alphaclops.phase_by(m, 0.25, 0)


def test_protocols_and_repr():
    alphaclops.testing.assert_implements_consistent_protocols(alphaclops.MatrixGate(np.diag([1, 1j, 1, -1])))
    alphaclops.testing.assert_implements_consistent_protocols(
        alphaclops.MatrixGate(np.diag([1, 1j, -1]), qid_shape=(3,))
    )


def test_matrixgate_unitary_tolerance():
    ## non-unitary matrix
    with pytest.raises(ValueError):
        _ = alphaclops.MatrixGate(np.array([[1, 0], [0, -0.6]]), unitary_check_atol=0.5)

    # very high atol -> check converges quickly
    _ = alphaclops.MatrixGate(np.array([[1, 0], [0, 1]]), unitary_check_atol=1)

    # very high rtol -> check converges quickly
    _ = alphaclops.MatrixGate(np.array([[1, 0], [0, -0.6]]), unitary_check_rtol=1)

    ## unitary matrix
    _ = alphaclops.MatrixGate(np.array([[0.707, 0.707], [-0.707, 0.707]]), unitary_check_atol=0.5)

    # very low atol -> the check never converges
    with pytest.raises(ValueError):
        _ = alphaclops.MatrixGate(np.array([[0.707, 0.707], [-0.707, 0.707]]), unitary_check_atol=1e-10)

    # very low atol -> the check never converges
    with pytest.raises(ValueError):
        _ = alphaclops.MatrixGate(np.array([[0.707, 0.707], [-0.707, 0.707]]), unitary_check_rtol=1e-10)


def test_matrixgate_name_serialization():
    # https://github.com/quantumlib/alphaclops/issues/5999

    # Test name serialization
    gate1 = alphaclops.MatrixGate(np.eye(2), name='test_name')
    gate_after_serialization1 = alphaclops.read_json(json_text=alphaclops.to_json(gate1))
    assert gate1._name == 'test_name'
    assert gate_after_serialization1._name == 'test_name'

    # Test name backwards compatibility
    gate2 = alphaclops.MatrixGate(np.eye(2))
    gate_after_serialization2 = alphaclops.read_json(json_text=alphaclops.to_json(gate2))
    assert gate2._name is None
    assert gate_after_serialization2._name is None

    # Test empty name
    gate3 = alphaclops.MatrixGate(np.eye(2), name='')
    gate_after_serialization3 = alphaclops.read_json(json_text=alphaclops.to_json(gate3))
    assert gate3._name == ''
    assert gate_after_serialization3._name == ''
