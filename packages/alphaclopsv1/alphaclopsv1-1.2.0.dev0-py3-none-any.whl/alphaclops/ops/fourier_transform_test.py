# Copyright 2019 The alphaclops Developers
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
import pytest, sympy

import alphaclops


def test_phase_gradient():
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.PhaseGradientGate(num_qubits=2, exponent=1)), np.diag([1, 1j, -1, -1j])
    )

    for k in range(4):
        alphaclops.testing.assert_implements_consistent_protocols(
            alphaclops.PhaseGradientGate(num_qubits=k, exponent=1)
        )


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_phase_gradient_symbolic(resolve_fn):
    a = alphaclops.PhaseGradientGate(num_qubits=2, exponent=0.5)
    b = alphaclops.PhaseGradientGate(num_qubits=2, exponent=sympy.Symbol('t'))
    assert not alphaclops.is_parameterized(a)
    assert alphaclops.is_parameterized(b)
    assert alphaclops.has_unitary(a)
    assert not alphaclops.has_unitary(b)
    assert resolve_fn(a, {'t': 0.25}) is a
    assert resolve_fn(b, {'t': 0.5}) == a
    assert resolve_fn(b, {'t': 0.25}) == alphaclops.PhaseGradientGate(num_qubits=2, exponent=0.25)


def test_str():
    assert str(alphaclops.PhaseGradientGate(num_qubits=2, exponent=0.5)) == 'Grad[2]^0.5'
    assert str(alphaclops.PhaseGradientGate(num_qubits=2, exponent=1)) == 'Grad[2]'


def test_phase_gradient_gate_repr():
    a = alphaclops.PhaseGradientGate(num_qubits=2, exponent=0.5)
    alphaclops.testing.assert_equivalent_repr(a)


def test_quantum_fourier_transform_gate_repr():
    b = alphaclops.QuantumFourierTransformGate(num_qubits=2, without_reverse=False)
    alphaclops.testing.assert_equivalent_repr(b)


def test_pow():
    a = alphaclops.PhaseGradientGate(num_qubits=2, exponent=0.5)
    assert a ** 0.5 == alphaclops.PhaseGradientGate(num_qubits=2, exponent=0.25)
    assert a ** sympy.Symbol('t') == alphaclops.PhaseGradientGate(
        num_qubits=2, exponent=0.5 * sympy.Symbol('t')
    )


def test_qft():
    # fmt: off
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.qft(*alphaclops.LineQubit.range(2))),
        np.array(
            [
                [1, 1, 1, 1],
                [1, 1j, -1, -1j],
                [1, -1, 1, -1],
                [1, -1j, -1, 1j],
            ]
        )
        / 2,
        atol=1e-8,
    )

    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.qft(*alphaclops.LineQubit.range(2), without_reverse=True)),
        np.array(
            [
                [1, 1, 1, 1],
                [1, -1, 1, -1],
                [1, 1j, -1, -1j],
                [1, -1j, -1, 1j],
            ]
        )
        / 2,
        atol=1e-8,
    )
    # fmt: on

    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.qft(*alphaclops.LineQubit.range(4))),
        np.array([[np.exp(2j * np.pi * i * j / 16) for i in range(16)] for j in range(16)]) / 4,
        atol=1e-8,
    )

    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.qft(*alphaclops.LineQubit.range(2)) ** -1),
        np.array([[1, 1, 1, 1], [1, -1j, -1, 1j], [1, -1, 1, -1], [1, 1j, -1, -1j]]) / 2,
        atol=1e-8,
    )

    for k in range(4):
        for b in [False, True]:
            alphaclops.testing.assert_implements_consistent_protocols(
                alphaclops.QuantumFourierTransformGate(num_qubits=k, without_reverse=b)
            )


def test_inverse():
    a, b, c = alphaclops.LineQubit.range(3)
    assert alphaclops.qft(a, b, c, inverse=True) == alphaclops.qft(a, b, c) ** -1
    assert alphaclops.qft(a, b, c, inverse=True, without_reverse=True) == alphaclops.inverse(
        alphaclops.qft(a, b, c, without_reverse=True)
    )


def test_circuit_diagram():
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(alphaclops.decompose_once(alphaclops.qft(*alphaclops.LineQubit.range(4)))),
        """
0: ───H───Grad^0.5───────#2─────────────#3─────────────×───
          │              │              │              │
1: ───────@──────────H───Grad^0.5───────#2─────────×───┼───
                         │              │          │   │
2: ──────────────────────@──────────H───Grad^0.5───×───┼───
                                        │              │
3: ─────────────────────────────────────@──────────H───×───
        """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(alphaclops.decompose_once(alphaclops.qft(*alphaclops.LineQubit.range(4), without_reverse=True))),
        """
0: ───H───Grad^0.5───────#2─────────────#3─────────────
          │              │              │
1: ───────@──────────H───Grad^0.5───────#2─────────────
                         │              │
2: ──────────────────────@──────────H───Grad^0.5───────
                                        │
3: ─────────────────────────────────────@──────────H───
        """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            alphaclops.qft(*alphaclops.LineQubit.range(4)), alphaclops.inverse(alphaclops.qft(*alphaclops.LineQubit.range(4)))
        ),
        """
0: ───qft───qft^-1───
      │     │
1: ───#2────#2───────
      │     │
2: ───#3────#3───────
      │     │
3: ───#4────#4───────
        """,
    )
