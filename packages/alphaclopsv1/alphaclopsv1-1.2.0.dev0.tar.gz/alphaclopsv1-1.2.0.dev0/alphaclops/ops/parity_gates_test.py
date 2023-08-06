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

"""Tests for `parity_gates.py`."""

import numpy as np
import pytest
import sympy

import alphaclops


@pytest.mark.parametrize('eigen_gate_type', [alphaclops.XXPowGate, alphaclops.YYPowGate, alphaclops.ZZPowGate])
def test_eigen_gates_consistent_protocols(eigen_gate_type):
    alphaclops.testing.assert_eigengate_implements_consistent_protocols(eigen_gate_type)


def test_xx_init():
    assert alphaclops.XXPowGate(exponent=1).exponent == 1
    v = alphaclops.XXPowGate(exponent=0.5)
    assert v.exponent == 0.5


def test_xx_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(
        alphaclops.XX,
        alphaclops.XXPowGate(),
        alphaclops.XXPowGate(exponent=1, global_shift=0),
        alphaclops.XXPowGate(exponent=3, global_shift=0),
    )
    eq.add_equality_group(alphaclops.XX ** 0.5, alphaclops.XX ** 2.5, alphaclops.XX ** 4.5)
    eq.add_equality_group(alphaclops.XX ** 0.25, alphaclops.XX ** 2.25, alphaclops.XX ** -1.75)

    iXX = alphaclops.XXPowGate(global_shift=0.5)
    eq.add_equality_group(iXX**0.5, iXX**4.5)
    eq.add_equality_group(iXX**2.5, iXX**6.5)


def test_xx_pow():
    assert alphaclops.XX ** 0.5 != alphaclops.XX ** -0.5
    assert alphaclops.XX ** -1 == alphaclops.XX
    assert (alphaclops.XX ** -1) ** 0.5 == alphaclops.XX ** -0.5


def test_xx_str():
    assert str(alphaclops.XX) == 'XX'
    assert str(alphaclops.XX ** 0.5) == 'XX**0.5'
    assert str(alphaclops.XXPowGate(global_shift=0.1)) == 'XX'


def test_xx_repr():
    assert repr(alphaclops.XXPowGate()) == 'alphaclops.XX'
    assert repr(alphaclops.XXPowGate(exponent=0.5)) == '(alphaclops.XX**0.5)'


def test_xx_matrix():
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.XX),
        np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]),
        atol=1e-8,
    )
    np.testing.assert_allclose(alphaclops.unitary(alphaclops.XX ** 2), np.eye(4), atol=1e-8)
    c = np.cos(np.pi / 6)
    s = -1j * np.sin(np.pi / 6)
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.XXPowGate(exponent=1 / 3, global_shift=-0.5)),
        np.array([[c, 0, 0, s], [0, c, s, 0], [0, s, c, 0], [s, 0, 0, c]]),
        atol=1e-8,
    )


def test_xx_diagrams():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    circuit = alphaclops.Circuit(alphaclops.XX(a, b), alphaclops.XX(a, b) ** 3, alphaclops.XX(a, b) ** 0.5)
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a: ───XX───XX───XX───────
      │    │    │
b: ───XX───XX───XX^0.5───
""",
    )


def test_yy_init():
    assert alphaclops.YYPowGate(exponent=1).exponent == 1
    v = alphaclops.YYPowGate(exponent=0.5)
    assert v.exponent == 0.5


def test_yy_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(
        alphaclops.YY,
        alphaclops.YYPowGate(),
        alphaclops.YYPowGate(exponent=1, global_shift=0),
        alphaclops.YYPowGate(exponent=3, global_shift=0),
    )
    eq.add_equality_group(alphaclops.YY ** 0.5, alphaclops.YY ** 2.5, alphaclops.YY ** 4.5)
    eq.add_equality_group(alphaclops.YY ** 0.25, alphaclops.YY ** 2.25, alphaclops.YY ** -1.75)

    iYY = alphaclops.YYPowGate(global_shift=0.5)
    eq.add_equality_group(iYY**0.5, iYY**4.5)
    eq.add_equality_group(iYY**2.5, iYY**6.5)


def test_yy_pow():
    assert alphaclops.YY ** 0.5 != alphaclops.YY ** -0.5
    assert alphaclops.YY ** -1 == alphaclops.YY
    assert (alphaclops.YY ** -1) ** 0.5 == alphaclops.YY ** -0.5


def test_yy_str():
    assert str(alphaclops.YY) == 'YY'
    assert str(alphaclops.YY ** 0.5) == 'YY**0.5'
    assert str(alphaclops.YYPowGate(global_shift=0.1)) == 'YY'

    iYY = alphaclops.YYPowGate(global_shift=0.5)
    assert str(iYY) == 'YY'


def test_yy_repr():
    assert repr(alphaclops.YYPowGate()) == 'alphaclops.YY'
    assert repr(alphaclops.YYPowGate(exponent=0.5)) == '(alphaclops.YY**0.5)'


def test_yy_matrix():
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.YY),
        np.array([[0, 0, 0, -1], [0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0]]),
        atol=1e-8,
    )
    np.testing.assert_allclose(alphaclops.unitary(alphaclops.YY ** 2), np.eye(4), atol=1e-8)
    c = np.cos(np.pi / 6)
    s = 1j * np.sin(np.pi / 6)
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.YYPowGate(exponent=1 / 3, global_shift=-0.5)),
        np.array([[c, 0, 0, s], [0, c, -s, 0], [0, -s, c, 0], [s, 0, 0, c]]),
        atol=1e-8,
    )


def test_yy_diagrams():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    circuit = alphaclops.Circuit(alphaclops.YY(a, b), alphaclops.YY(a, b) ** 3, alphaclops.YY(a, b) ** 0.5)
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a: ───YY───YY───YY───────
      │    │    │
b: ───YY───YY───YY^0.5───
""",
    )


def test_zz_init():
    assert alphaclops.ZZPowGate(exponent=1).exponent == 1
    v = alphaclops.ZZPowGate(exponent=0.5)
    assert v.exponent == 0.5


def test_zz_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(
        alphaclops.ZZ,
        alphaclops.ZZPowGate(),
        alphaclops.ZZPowGate(exponent=1, global_shift=0),
        alphaclops.ZZPowGate(exponent=3, global_shift=0),
    )
    eq.add_equality_group(alphaclops.ZZ ** 0.5, alphaclops.ZZ ** 2.5, alphaclops.ZZ ** 4.5)
    eq.add_equality_group(alphaclops.ZZ ** 0.25, alphaclops.ZZ ** 2.25, alphaclops.ZZ ** -1.75)

    iZZ = alphaclops.ZZPowGate(global_shift=0.5)
    eq.add_equality_group(iZZ**0.5, iZZ**4.5)
    eq.add_equality_group(iZZ**2.5, iZZ**6.5)


def test_zz_pow():
    assert alphaclops.ZZ ** 0.5 != alphaclops.ZZ ** -0.5
    assert alphaclops.ZZ ** -1 == alphaclops.ZZ
    assert (alphaclops.ZZ ** -1) ** 0.5 == alphaclops.ZZ ** -0.5


def test_zz_phase_by():
    assert alphaclops.phase_by(alphaclops.ZZ, 0.25, 0) == alphaclops.phase_by(alphaclops.ZZ, 0.25, 1) == alphaclops.ZZ
    assert alphaclops.phase_by(alphaclops.ZZ ** 0.5, 0.25, 0) == alphaclops.ZZ ** 0.5
    assert alphaclops.phase_by(alphaclops.ZZ ** -0.5, 0.25, 1) == alphaclops.ZZ ** -0.5


def test_zz_str():
    assert str(alphaclops.ZZ) == 'ZZ'
    assert str(alphaclops.ZZ ** 0.5) == 'ZZ**0.5'
    assert str(alphaclops.ZZPowGate(global_shift=0.1)) == 'ZZ'

    iZZ = alphaclops.ZZPowGate(global_shift=0.5)
    assert str(iZZ) == 'ZZ'


def test_zz_repr():
    assert repr(alphaclops.ZZPowGate()) == 'alphaclops.ZZ'
    assert repr(alphaclops.ZZPowGate(exponent=0.5)) == '(alphaclops.ZZ**0.5)'


def test_zz_matrix():
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.ZZ),
        np.array([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]),
        atol=1e-8,
    )
    np.testing.assert_allclose(alphaclops.unitary(alphaclops.ZZ ** 2), np.eye(4), atol=1e-8)
    b = 1j**0.25
    a = np.conj(b)
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.ZZPowGate(exponent=0.25, global_shift=-0.5)),
        np.array([[a, 0, 0, 0], [0, b, 0, 0], [0, 0, b, 0], [0, 0, 0, a]]),
        atol=1e-8,
    )


def test_zz_diagrams():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    circuit = alphaclops.Circuit(alphaclops.ZZ(a, b), alphaclops.ZZ(a, b) ** 3, alphaclops.ZZ(a, b) ** 0.5)
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a: ───ZZ───ZZ───ZZ───────
      │    │    │
b: ───ZZ───ZZ───ZZ^0.5───
""",
    )


def test_trace_distance():
    foo = sympy.Symbol('foo')
    assert alphaclops.trace_distance_bound(alphaclops.XX ** foo) == 1.0
    assert alphaclops.trace_distance_bound(alphaclops.YY ** foo) == 1.0
    assert alphaclops.trace_distance_bound(alphaclops.ZZ ** foo) == 1.0
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(alphaclops.XX), 1.0)
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(alphaclops.YY ** 0), 0)
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(alphaclops.ZZ ** (1 / 3)), np.sin(np.pi / 6))


def test_ms_arguments():
    eq_tester = alphaclops.testing.EqualsTester()
    eq_tester.add_equality_group(alphaclops.ms(np.pi / 2), alphaclops.ops.MSGate(rads=np.pi / 2))
    eq_tester.add_equality_group(alphaclops.XXPowGate(global_shift=-0.5))


def test_ms_str():
    ms = alphaclops.ms(np.pi / 2)
    assert str(ms) == 'MS(π/2)'
    assert str(alphaclops.ms(np.pi)) == 'MS(2.0π/2)'
    assert str(ms**0.5) == 'MS(0.5π/2)'
    assert str(ms**2) == 'MS(2.0π/2)'
    assert str(ms**-1) == 'MS(-1.0π/2)'


def test_ms_matrix():
    s = np.sqrt(0.5)
    # yapf: disable
    np.testing.assert_allclose(alphaclops.unitary(alphaclops.ms(np.pi / 4)),
                               np.array([[s, 0, 0, -1j*s],
                                 [0, s, -1j*s, 0],
                                 [0, -1j*s, s, 0],
                                 [-1j*s, 0, 0, s]]),
                               atol=1e-8)
    # yapf: enable
    np.testing.assert_allclose(alphaclops.unitary(alphaclops.ms(np.pi)), np.diag([-1, -1, -1, -1]), atol=1e-8)


def test_ms_repr():
    assert repr(alphaclops.ms(np.pi / 2)) == 'alphaclops.ms(np.pi/2)'
    assert repr(alphaclops.ms(np.pi / 4)) == 'alphaclops.ms(0.5*np.pi/2)'
    alphaclops.testing.assert_equivalent_repr(alphaclops.ms(np.pi / 4))
    ms = alphaclops.ms(np.pi / 2)
    assert repr(ms**2) == 'alphaclops.ms(2.0*np.pi/2)'
    assert repr(ms**-0.5) == 'alphaclops.ms(-0.5*np.pi/2)'


def test_ms_diagrams():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    circuit = alphaclops.Circuit(alphaclops.SWAP(a, b), alphaclops.X(a), alphaclops.Y(a), alphaclops.ms(np.pi).on(a, b))
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a: ───×───X───Y───MS(π)───
      │           │
b: ───×───────────MS(π)───
""",
    )


def test_json_serialization():
    def custom_resolver(alphaclops_type: str):
        if alphaclops_type == "MSGate":
            return alphaclops.ops.MSGate
        return None

    assert alphaclops.read_json(
        json_text=alphaclops.to_json(alphaclops.ms(np.pi / 2)), resolvers=[custom_resolver]
    ) == alphaclops.ms(np.pi / 2)
    assert custom_resolver('X') is None
