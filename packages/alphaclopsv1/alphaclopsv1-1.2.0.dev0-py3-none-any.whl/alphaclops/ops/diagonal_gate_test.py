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

from typing import List
import numpy as np
import pytest
import sympy

import alphaclops

_candidate_angles: List[float] = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]


@pytest.mark.parametrize(
    'gate',
    (
        (
                alphaclops.DiagonalGate([2, 3, 5, 7]),
                alphaclops.DiagonalGate([0, 0, 0, 0]),
                alphaclops.DiagonalGate([2, 3, 5, sympy.Symbol('a')]),
                alphaclops.DiagonalGate([0.34, 0.12, 0, 0.96]),
                alphaclops.DiagonalGate(_candidate_angles[:8]),
                alphaclops.DiagonalGate(_candidate_angles[:16]),
        )
    ),
)
def test_consistent_protocols(gate):
    alphaclops.testing.assert_implements_consistent_protocols(gate)


def test_property():
    assert alphaclops.DiagonalGate([2, 3, 5, 7]).diag_angles_radians == (2, 3, 5, 7)


@pytest.mark.parametrize('n', [1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_decomposition_unitary(n):
    diagonal_angles = np.random.randn(2**n)
    diagonal_gate = alphaclops.DiagonalGate(diagonal_angles)
    decomposed_circ = alphaclops.Circuit(alphaclops.decompose(diagonal_gate(*alphaclops.LineQubit.range(n))))

    expected_f = [np.exp(1j * angle) for angle in diagonal_angles]
    decomposed_f = alphaclops.unitary(decomposed_circ).diagonal()

    # For large qubit counts, the decomposed circuit is rather large, so we lose a lot of
    # precision.
    np.testing.assert_allclose(decomposed_f, expected_f)


@pytest.mark.parametrize('n', [1, 2, 3, 4])
def test_diagonal_exponent(n):
    diagonal_angles = _candidate_angles[: 2**n]
    diagonal_gate = alphaclops.DiagonalGate(diagonal_angles)

    sqrt_diagonal_gate = diagonal_gate**0.5

    expected_angles = [prime / 2 for prime in diagonal_angles]
    np.testing.assert_allclose(expected_angles, sqrt_diagonal_gate._diag_angles_radians, atol=1e-8)

    assert alphaclops.pow(alphaclops.DiagonalGate(diagonal_angles), "test", None) is None


@pytest.mark.parametrize('n', [1, 2, 3, 4])
def test_decomposition_diagonal_exponent(n):
    diagonal_angles = np.random.randn(2**n)
    diagonal_gate = alphaclops.DiagonalGate(diagonal_angles)
    sqrt_diagonal_gate = diagonal_gate**0.5
    decomposed_circ = alphaclops.Circuit(alphaclops.decompose(sqrt_diagonal_gate(*alphaclops.LineQubit.range(n))))

    expected_f = [np.exp(1j * angle / 2) for angle in diagonal_angles]
    decomposed_f = alphaclops.unitary(decomposed_circ).diagonal()

    np.testing.assert_allclose(decomposed_f, expected_f)


@pytest.mark.parametrize('n', [1, 2, 3, 4])
def test_decomposition_with_parameterization(n):
    angles = sympy.symbols([f'x_{i}' for i in range(2**n)])
    exponent = sympy.Symbol('e')
    diagonal_gate = alphaclops.DiagonalGate(angles) ** exponent
    parameterized_op = diagonal_gate(*alphaclops.LineQubit.range(n))
    decomposed_circuit = alphaclops.Circuit(alphaclops.decompose(parameterized_op))
    for exponent_value in [-0.5, 0.5, 1]:
        for i in range(len(_candidate_angles) - 2**n + 1):
            resolver = {exponent: exponent_value}
            resolver.update(
                {angles[j]: x_j for j, x_j in enumerate(_candidate_angles[i : i + 2**n])}
            )
            resolved_op = alphaclops.resolve_parameters(parameterized_op, resolver)
            resolved_circuit = alphaclops.resolve_parameters(decomposed_circuit, resolver)
            np.testing.assert_allclose(
                alphaclops.unitary(resolved_op), alphaclops.unitary(resolved_circuit), atol=1e-8
            )


def test_diagram():
    a, b, c, d = alphaclops.LineQubit.range(4)

    diagonal_circuit = alphaclops.Circuit(alphaclops.DiagonalGate(_candidate_angles[:16])(a, b, c, d))
    alphaclops.testing.assert_has_diagram(
        diagonal_circuit,
        """
0: ───diag(2, 3, ..., 47, 53)───
      │
1: ───#2────────────────────────
      │
2: ───#3────────────────────────
      │
3: ───#4────────────────────────
""",
    )

    diagonal_circuit = alphaclops.Circuit(alphaclops.DiagonalGate(_candidate_angles[:8])(a, b, c))
    alphaclops.testing.assert_has_diagram(
        diagonal_circuit,
        """
0: ───diag(2, 3, ..., 17, 19)───
      │
1: ───#2────────────────────────
      │
2: ───#3────────────────────────
""",
    )

    diagonal_circuit = alphaclops.Circuit(alphaclops.DiagonalGate(_candidate_angles[:4])(a, b))
    alphaclops.testing.assert_has_diagram(
        diagonal_circuit,
        """
0: ───diag(2, 3, 5, 7)───
      │
1: ───#2─────────────────
""",
    )


@pytest.mark.parametrize('n', [1, 2, 3, 4])
def test_unitary(n):
    diagonal_angles = _candidate_angles[: 2**n]
    assert alphaclops.has_unitary(alphaclops.DiagonalGate(diagonal_angles))
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.DiagonalGate(diagonal_angles)).diagonal(),
        [np.exp(1j * angle) for angle in diagonal_angles],
        atol=1e-8,
    )


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_resolve(resolve_fn):
    diagonal_angles = [2, 3, 5, 7, 11, 13, 17, 19]
    diagonal_gate = alphaclops.DiagonalGate(diagonal_angles[:6] + [sympy.Symbol('a'), sympy.Symbol('b')])
    assert alphaclops.is_parameterized(diagonal_gate)

    diagonal_gate = resolve_fn(diagonal_gate, {'a': 17})
    assert diagonal_gate == alphaclops.DiagonalGate(diagonal_angles[:7] + [sympy.Symbol('b')])
    assert alphaclops.is_parameterized(diagonal_gate)

    diagonal_gate = resolve_fn(diagonal_gate, {'b': 19})
    assert diagonal_gate == alphaclops.DiagonalGate(diagonal_angles)
    assert not alphaclops.is_parameterized(diagonal_gate)
