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

import numpy as np
import pytest
import sympy

import alphaclops


@pytest.mark.parametrize(
    'gate',
    (
        (
                alphaclops.TwoQubitDiagonalGate([2, 3, 5, 7]),
                alphaclops.TwoQubitDiagonalGate([0, 0, 0, 0]),
                alphaclops.TwoQubitDiagonalGate([2, 3, 5, sympy.Symbol('a')]),
                alphaclops.TwoQubitDiagonalGate([0.34, 0.12, 0, 0.96]),
        )
    ),
)
def test_consistent_protocols(gate):
    alphaclops.testing.assert_implements_consistent_protocols(gate)


def test_property():
    assert alphaclops.TwoQubitDiagonalGate([2, 3, 5, 7]).diag_angles_radians == (2, 3, 5, 7)


def test_parameterized_decompose():
    angles = sympy.symbols('x0, x1, x2, x3')
    parameterized_op = alphaclops.TwoQubitDiagonalGate(angles).on(*alphaclops.LineQubit.range(2))
    decomposed_circuit = alphaclops.Circuit(alphaclops.decompose(parameterized_op))
    for resolver in (
            alphaclops.Linspace('x0', -2, 2, 3)
            * alphaclops.Linspace('x1', -2, 2, 3)
            * alphaclops.Linspace('x2', -2, 2, 3)
            * alphaclops.Linspace('x3', -2, 2, 3)
    ):
        np.testing.assert_allclose(
            alphaclops.unitary(alphaclops.resolve_parameters(parameterized_op, resolver)),
            alphaclops.unitary(alphaclops.resolve_parameters(decomposed_circuit, resolver)),
        )


def test_unitary():
    diagonal_angles = [2, 3, 5, 7]
    assert alphaclops.has_unitary(alphaclops.TwoQubitDiagonalGate(diagonal_angles))
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.TwoQubitDiagonalGate(diagonal_angles)),
        np.diag([np.exp(1j * angle) for angle in diagonal_angles]),
        atol=1e-8,
    )


def test_diagram():
    a, b = alphaclops.LineQubit.range(2)

    diagonal_circuit = alphaclops.Circuit(alphaclops.TwoQubitDiagonalGate([2, 3, 5, 7])(a, b))
    alphaclops.testing.assert_has_diagram(
        diagonal_circuit,
        """
0: ───diag(2, 3, 5, 7)───
      │
1: ───#2─────────────────
""",
    )
    alphaclops.testing.assert_has_diagram(
        diagonal_circuit,
        """
0: ---diag(2, 3, 5, 7)---
      |
1: ---#2-----------------
""",
        use_unicode_characters=False,
    )


def test_diagonal_exponent():
    diagonal_angles = [2, 3, 5, 7]
    diagonal_gate = alphaclops.TwoQubitDiagonalGate(diagonal_angles)

    sqrt_diagonal_gate = diagonal_gate**0.5

    expected_angles = [prime / 2 for prime in diagonal_angles]
    assert alphaclops.approx_eq(sqrt_diagonal_gate, alphaclops.TwoQubitDiagonalGate(expected_angles))

    assert alphaclops.pow(alphaclops.TwoQubitDiagonalGate(diagonal_angles), "test", None) is None


def test_protocols_mul_not_implemented():
    diagonal_angles = [2, 3, None, 7]
    diagonal_gate = alphaclops.TwoQubitDiagonalGate(diagonal_angles)
    with pytest.raises(TypeError):
        alphaclops.protocols.pow(diagonal_gate, 3)


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_resolve(resolve_fn):
    diagonal_angles = [2, 3, 5, 7]
    diagonal_gate = alphaclops.TwoQubitDiagonalGate(
        diagonal_angles[:2] + [sympy.Symbol('a'), sympy.Symbol('b')]
    )
    assert alphaclops.is_parameterized(diagonal_gate)

    diagonal_gate = resolve_fn(diagonal_gate, {'a': 5})
    assert diagonal_gate == alphaclops.TwoQubitDiagonalGate(diagonal_angles[:3] + [sympy.Symbol('b')])
    assert alphaclops.is_parameterized(diagonal_gate)

    diagonal_gate = resolve_fn(diagonal_gate, {'b': 7})
    assert diagonal_gate == alphaclops.TwoQubitDiagonalGate(diagonal_angles)
    assert not alphaclops.is_parameterized(diagonal_gate)
