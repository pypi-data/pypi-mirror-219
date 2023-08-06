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
import numpy as np
import pytest
import sympy

import alphaclops


@pytest.mark.parametrize('eigen_gate_type', [alphaclops.CCXPowGate, alphaclops.CCZPowGate])
def test_eigen_gates_consistent_protocols(eigen_gate_type):
    alphaclops.testing.assert_eigengate_implements_consistent_protocols(eigen_gate_type)


@pytest.mark.parametrize(
    'gate',
    (
        (alphaclops.CSWAP),
        (alphaclops.ThreeQubitDiagonalGate([2, 3, 5, 7, 11, 13, 17, 19])),
        (alphaclops.ThreeQubitDiagonalGate([0, 0, 0, 0, 0, 0, 0, 0])),
        (alphaclops.CCX),
        (alphaclops.CCZ),
    ),
)
def test_consistent_protocols(gate):
    alphaclops.testing.assert_implements_consistent_protocols(gate)


def test_init():
    assert (alphaclops.CCZ ** 0.5).exponent == 0.5
    assert (alphaclops.CCZ ** 0.25).exponent == 0.25
    assert (alphaclops.CCX ** 0.5).exponent == 0.5
    assert (alphaclops.CCX ** 0.25).exponent == 0.25


def test_unitary():
    assert alphaclops.has_unitary(alphaclops.CCX)
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.CCX),
        np.array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 1, 0],
            ]
        ),
        atol=1e-8,
    )

    assert alphaclops.has_unitary(alphaclops.CCX ** 0.5)
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.CCX ** 0.5),
        np.array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0.5 + 0.5j, 0.5 - 0.5j],
                [0, 0, 0, 0, 0, 0, 0.5 - 0.5j, 0.5 + 0.5j],
            ]
        ),
        atol=1e-8,
    )

    assert alphaclops.has_unitary(alphaclops.CCZ)
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.CCZ), np.diag([1, 1, 1, 1, 1, 1, 1, -1]), atol=1e-8
    )

    assert alphaclops.has_unitary(alphaclops.CCZ ** 0.5)
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.CCZ ** 0.5), np.diag([1, 1, 1, 1, 1, 1, 1, 1j]), atol=1e-8
    )

    assert alphaclops.has_unitary(alphaclops.CSWAP)
    u = alphaclops.unitary(alphaclops.CSWAP)
    np.testing.assert_allclose(
        u,
        np.array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(u @ u, np.eye(8))

    diagonal_angles = [2, 3, 5, 7, 11, 13, 17, 19]
    assert alphaclops.has_unitary(alphaclops.ThreeQubitDiagonalGate(diagonal_angles))
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.ThreeQubitDiagonalGate(diagonal_angles)),
        np.diag([np.exp(1j * angle) for angle in diagonal_angles]),
        atol=1e-8,
    )


def test_str():
    assert str(alphaclops.CCX) == 'TOFFOLI'
    assert str(alphaclops.TOFFOLI) == 'TOFFOLI'
    assert str(alphaclops.CSWAP) == 'FREDKIN'
    assert str(alphaclops.FREDKIN) == 'FREDKIN'
    assert str(alphaclops.CCZ) == 'CCZ'

    assert str(alphaclops.CCX ** 0.5) == 'TOFFOLI**0.5'
    assert str(alphaclops.CCZ ** 0.5) == 'CCZ**0.5'


def test_repr():
    assert repr(alphaclops.CCX) == 'alphaclops.TOFFOLI'
    assert repr(alphaclops.TOFFOLI) == 'alphaclops.TOFFOLI'
    assert repr(alphaclops.CSWAP) == 'alphaclops.FREDKIN'
    assert repr(alphaclops.FREDKIN) == 'alphaclops.FREDKIN'
    assert repr(alphaclops.CCZ) == 'alphaclops.CCZ'

    assert repr(alphaclops.CCX ** 0.5) == '(alphaclops.TOFFOLI**0.5)'
    assert repr(alphaclops.CCZ ** 0.5) == '(alphaclops.CCZ**0.5)'


def test_eq():
    a, b, c, d = alphaclops.LineQubit.range(4)
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(alphaclops.CCZ(a, b, c), alphaclops.CCZ(a, c, b), alphaclops.CCZ(b, c, a))
    eq.add_equality_group(
        alphaclops.CCZ(a, b, c) ** 0.5, alphaclops.CCZ(a, c, b) ** 2.5, alphaclops.CCZ(b, c, a) ** -1.5
    )
    eq.add_equality_group(
        alphaclops.TOFFOLI(a, b, c) ** 0.5, alphaclops.TOFFOLI(b, a, c) ** 2.5, alphaclops.TOFFOLI(a, b, c) ** -1.5
    )
    eq.add_equality_group(alphaclops.CCZ(a, b, d))
    eq.add_equality_group(alphaclops.TOFFOLI(a, b, c), alphaclops.CCX(a, b, c))
    eq.add_equality_group(alphaclops.TOFFOLI(a, c, b), alphaclops.TOFFOLI(c, a, b))
    eq.add_equality_group(alphaclops.TOFFOLI(a, b, d))
    eq.add_equality_group(alphaclops.CSWAP(a, b, c), alphaclops.FREDKIN(a, b, c), alphaclops.FREDKIN(a, b, c) ** -1)
    eq.add_equality_group(alphaclops.CSWAP(b, a, c), alphaclops.CSWAP(b, c, a))


def test_gate_equality():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(alphaclops.CSwapGate(), alphaclops.CSwapGate())
    eq.add_equality_group(alphaclops.CZPowGate(), alphaclops.CZPowGate())
    eq.add_equality_group(alphaclops.CCXPowGate(), alphaclops.CCXPowGate(), alphaclops.CCNotPowGate())
    eq.add_equality_group(alphaclops.CCZPowGate(), alphaclops.CCZPowGate())


def test_identity_multiplication():
    a, b, c = alphaclops.LineQubit.range(3)
    assert alphaclops.CCX(a, b, c) * alphaclops.I(a) == alphaclops.CCX(a, b, c)
    assert alphaclops.CCX(a, b, c) * alphaclops.I(b) == alphaclops.CCX(a, b, c)
    assert alphaclops.CCX(a, b, c) ** 0.5 * alphaclops.I(c) == alphaclops.CCX(a, b, c) ** 0.5
    assert alphaclops.I(c) * alphaclops.CCZ(a, b, c) ** 0.5 == alphaclops.CCZ(a, b, c) ** 0.5


@pytest.mark.parametrize(
    'op,max_two_cost',
    [
        (alphaclops.CCZ(*alphaclops.LineQubit.range(3)), 8),
        (alphaclops.CCX(*alphaclops.LineQubit.range(3)), 8),
        (alphaclops.CCZ(alphaclops.LineQubit(0), alphaclops.LineQubit(2), alphaclops.LineQubit(1)), 8),
        (alphaclops.CCZ(alphaclops.LineQubit(0), alphaclops.LineQubit(2), alphaclops.LineQubit(1)) ** sympy.Symbol("s"), 8),
        (alphaclops.CSWAP(*alphaclops.LineQubit.range(3)), 9),
        (alphaclops.CSWAP(*reversed(alphaclops.LineQubit.range(3))), 9),
        (alphaclops.CSWAP(alphaclops.LineQubit(1), alphaclops.LineQubit(0), alphaclops.LineQubit(2)), 12),
        (
                alphaclops.ThreeQubitDiagonalGate([2, 3, 5, 7, 11, 13, 17, 19])(
                alphaclops.LineQubit(1), alphaclops.LineQubit(2), alphaclops.LineQubit(3)
            ),
                8,
        ),
    ],
)
def test_decomposition_cost(op: alphaclops.Operation, max_two_cost: int):
    ops = tuple(alphaclops.flatten_op_tree(alphaclops.decompose(op)))
    two_cost = len([e for e in ops if len(e.qubits) == 2])
    over_cost = len([e for e in ops if len(e.qubits) > 2])
    assert over_cost == 0
    assert two_cost == max_two_cost


def test_parameterized_ccz_decompose_no_global_phase():
    decomposed_ops = alphaclops.decompose(alphaclops.CCZ(*alphaclops.LineQubit.range(3)) ** sympy.Symbol("theta"))
    assert not any(isinstance(op.gate, alphaclops.GlobalPhaseGate) for op in decomposed_ops)


def test_diagonal_gate_property():
    assert alphaclops.ThreeQubitDiagonalGate([2, 3, 5, 7, 0, 0, 0, 1]).diag_angles_radians == (
        (2, 3, 5, 7, 0, 0, 0, 1)
    )


@pytest.mark.parametrize(
    'gate',
    [alphaclops.CCX, alphaclops.CSWAP, alphaclops.CCZ, alphaclops.ThreeQubitDiagonalGate([2, 3, 5, 7, 11, 13, 17, 19])],
)
def test_decomposition_respects_locality(gate):
    a = alphaclops.TensorCircuit(0, 0)
    b = alphaclops.TensorCircuit(1, 0)
    c = alphaclops.TensorCircuit(0, 1)
    dev = alphaclops.testing.ValidatingTestDevice(qubits={a, b, c}, validate_locality=True)
    for x, y, z in itertools.permutations([a, b, c]):
        circuit = alphaclops.Circuit(gate(x, y, z))
        circuit = alphaclops.Circuit(alphaclops.decompose(circuit))
        dev.validate_circuit(circuit)


def test_diagram():
    a, b, c, d = alphaclops.LineQubit.range(4)
    circuit = alphaclops.Circuit(
        alphaclops.TOFFOLI(a, b, c),
        alphaclops.TOFFOLI(a, b, c) ** 0.5,
        alphaclops.TOFFOLI(c, b, a) ** 0.5,
        alphaclops.CCX(a, c, b),
        alphaclops.CCZ(a, d, b),
        alphaclops.CCZ(a, d, b) ** 0.5,
        alphaclops.CSWAP(a, c, d),
        alphaclops.FREDKIN(a, b, c),
    )
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ───@───@───────X^0.5───@───@───@───────@───@───
      │   │       │       │   │   │       │   │
1: ───@───@───────@───────X───@───@───────┼───×───
      │   │       │       │   │   │       │   │
2: ───X───X^0.5───@───────@───┼───┼───────×───×───
                              │   │       │
3: ───────────────────────────@───@^0.5───×───────
""",
    )
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ---@---@-------X^0.5---@---@---@-------@------@------
      |   |       |       |   |   |       |      |
1: ---@---@-------@-------X---@---@-------|------swap---
      |   |       |       |   |   |       |      |
2: ---X---X^0.5---@-------@---|---|-------swap---swap---
                              |   |       |
3: ---------------------------@---@^0.5---swap----------
""",
        use_unicode_characters=False,
    )

    diagonal_circuit = alphaclops.Circuit(
        alphaclops.ThreeQubitDiagonalGate([2, 3, 5, 7, 11, 13, 17, 19])(a, b, c)
    )
    alphaclops.testing.assert_has_diagram(
        diagonal_circuit,
        """
0: ───diag(2, 3, 5, 7, 11, 13, 17, 19)───
      │
1: ───#2─────────────────────────────────
      │
2: ───#3─────────────────────────────────
""",
    )
    alphaclops.testing.assert_has_diagram(
        diagonal_circuit,
        """
0: ---diag(2, 3, 5, 7, 11, 13, 17, 19)---
      |
1: ---#2---------------------------------
      |
2: ---#3---------------------------------
""",
        use_unicode_characters=False,
    )


def test_diagonal_exponent():
    diagonal_angles = [2, 3, 5, 7, 11, 13, 17, 19]
    diagonal_gate = alphaclops.ThreeQubitDiagonalGate(diagonal_angles)

    sqrt_diagonal_gate = diagonal_gate**0.5

    expected_angles = [prime / 2 for prime in diagonal_angles]
    np.testing.assert_allclose(expected_angles, sqrt_diagonal_gate._diag_angles_radians, atol=1e-8)

    assert alphaclops.pow(alphaclops.ThreeQubitDiagonalGate(diagonal_angles), "test", None) is None


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_resolve(resolve_fn):
    diagonal_angles = [2, 3, 5, 7, 11, 13, 17, 19]
    diagonal_gate = alphaclops.ThreeQubitDiagonalGate(
        diagonal_angles[:6] + [sympy.Symbol('a'), sympy.Symbol('b')]
    )
    assert alphaclops.is_parameterized(diagonal_gate)

    diagonal_gate = resolve_fn(diagonal_gate, {'a': 17})
    assert diagonal_gate == alphaclops.ThreeQubitDiagonalGate(diagonal_angles[:7] + [sympy.Symbol('b')])
    assert alphaclops.is_parameterized(diagonal_gate)

    diagonal_gate = resolve_fn(diagonal_gate, {'b': 19})
    assert diagonal_gate == alphaclops.ThreeQubitDiagonalGate(diagonal_angles)
    assert not alphaclops.is_parameterized(diagonal_gate)


@pytest.mark.parametrize('gate', [alphaclops.CCX, alphaclops.CCZ, alphaclops.CSWAP])
def test_controlled_ops_consistency(gate):
    a, b, c, d = alphaclops.LineQubit.range(4)
    assert gate.controlled(0) is gate
    assert gate(a, b, c).controlled_by(d) == gate(d, b, c).controlled_by(a)
