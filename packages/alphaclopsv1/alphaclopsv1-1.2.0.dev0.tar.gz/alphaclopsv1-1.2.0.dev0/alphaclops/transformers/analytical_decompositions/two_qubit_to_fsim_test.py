# Copyright 2022 The alphaclops Developers
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
import random
from typing import Any

import numpy as np
import pytest
import sympy

import alphaclops
from alphaclops.transformers.analytical_decompositions.two_qubit_to_fsim import (
    _decompose_two_qubit_interaction_into_two_b_gates,
    _decompose_xx_yy_into_two_fsims_ignoring_single_qubit_ops,
    _sticky_0_to_1,
    _B,
)


UNITARY_OBJS = [
    alphaclops.IdentityGate(2),
                   alphaclops.XX ** 0.25,
    alphaclops.CNOT,
    alphaclops.CNOT(*alphaclops.LineQubit.range(2)),
    alphaclops.CNOT(*alphaclops.LineQubit.range(2)[::-1]),
    alphaclops.ISWAP,
    alphaclops.SWAP,
    alphaclops.FSimGate(theta=np.pi / 6, phi=np.pi / 6),
] + [alphaclops.testing.random_unitary(4) for _ in range(5)]

FEASIBLE_FSIM_GATES = [
    alphaclops.ISWAP,
    alphaclops.FSimGate(np.pi / 2, 0),
    alphaclops.FSimGate(-np.pi / 2, 0),
    alphaclops.FSimGate(np.pi / 2, np.pi / 6),
    alphaclops.FSimGate(np.pi / 2, -np.pi / 6),
    alphaclops.FSimGate(5 * np.pi / 9, -np.pi / 6),
    alphaclops.FSimGate(5 * np.pi / 9, 0),
    alphaclops.FSimGate(4 * np.pi / 9, -np.pi / 6),
    alphaclops.FSimGate(4 * np.pi / 9, 0),
    alphaclops.FSimGate(-4 * np.pi / 9, 0),
    # Extreme points.
    alphaclops.FSimGate(np.pi * 3 / 8, -np.pi / 4),
    alphaclops.FSimGate(np.pi * 5 / 8, -np.pi / 4),
    alphaclops.FSimGate(np.pi * 3 / 8, +np.pi / 4),
    alphaclops.FSimGate(np.pi * 5 / 8, +np.pi / 4),
] + [
    alphaclops.FSimGate(
        theta=random.uniform(np.pi * 3 / 8, np.pi * 5 / 8),
        phi=random.uniform(-np.pi / 4, np.pi / 4),
    )
    for _ in range(5)
]


@pytest.mark.parametrize('obj', UNITARY_OBJS)
def test_decompose_two_qubit_interaction_into_two_b_gates(obj: Any):
    circuit = alphaclops.Circuit(
        _decompose_two_qubit_interaction_into_two_b_gates(obj, qubits=alphaclops.LineQubit.range(2))
    )
    desired_unitary = obj if isinstance(obj, np.ndarray) else alphaclops.unitary(obj)
    for operation in circuit.all_operations():
        assert len(operation.qubits) < 2 or operation.gate == _B
    np.testing.assert_allclose(alphaclops.unitary(circuit), desired_unitary, atol=1e-6)


def test_decompose_xx_yy_into_two_fsims_ignoring_single_qubit_ops_fail():
    c = _decompose_xx_yy_into_two_fsims_ignoring_single_qubit_ops(
        qubits=alphaclops.LineQubit.range(2),
        fsim_gate=alphaclops.FSimGate(theta=np.pi / 2, phi=0),
        canonical_x_kak_coefficient=np.pi / 4,
        canonical_y_kak_coefficient=np.pi / 8,
    )
    np.testing.assert_allclose(
        alphaclops.kak_decomposition(alphaclops.Circuit(c)).interaction_coefficients, [np.pi / 4, np.pi / 8, 0]
    )

    with pytest.raises(ValueError, match='Failed to synthesize'):
        _ = _decompose_xx_yy_into_two_fsims_ignoring_single_qubit_ops(
            qubits=alphaclops.LineQubit.range(2),
            fsim_gate=alphaclops.FSimGate(theta=np.pi / 5, phi=0),
            canonical_x_kak_coefficient=np.pi / 4,
            canonical_y_kak_coefficient=np.pi / 8,
        )


@pytest.mark.parametrize('obj,fsim_gate', itertools.product(UNITARY_OBJS, FEASIBLE_FSIM_GATES))
def test_decompose_two_qubit_interaction_into_four_fsim_gates_equivalence(
    obj: Any, fsim_gate: alphaclops.FSimGate
):
    qubits = obj.qubits if isinstance(obj, alphaclops.Operation) else alphaclops.LineQubit.range(2)
    circuit = alphaclops.decompose_two_qubit_interaction_into_four_fsim_gates(obj, fsim_gate=fsim_gate)
    desired_unitary = obj if isinstance(obj, np.ndarray) else alphaclops.unitary(obj)
    for operation in circuit.all_operations():
        assert len(operation.qubits) < 2 or operation.gate == fsim_gate
    assert len(circuit) <= 4 * 3 + 5
    assert alphaclops.approx_eq(circuit.unitary(qubit_order=qubits), desired_unitary, atol=1e-4)


def test_decompose_two_qubit_interaction_into_four_fsim_gates_validate():
    iswap = alphaclops.FSimGate(theta=np.pi / 2, phi=0)
    with pytest.raises(ValueError, match='fsim_gate.theta'):
        alphaclops.decompose_two_qubit_interaction_into_four_fsim_gates(
            np.eye(4), fsim_gate=alphaclops.FSimGate(theta=np.pi / 10, phi=0)
        )
    with pytest.raises(ValueError, match='fsim_gate.phi'):
        alphaclops.decompose_two_qubit_interaction_into_four_fsim_gates(
            np.eye(4), fsim_gate=alphaclops.FSimGate(theta=np.pi / 2, phi=np.pi / 3)
        )
    with pytest.raises(ValueError, match='pair of qubits'):
        alphaclops.decompose_two_qubit_interaction_into_four_fsim_gates(
            np.eye(4), fsim_gate=iswap, qubits=alphaclops.LineQubit.range(3)
        )
    with pytest.raises(ValueError, match='parameterized'):
        fsim = alphaclops.FSimGate(theta=np.pi / 2, phi=sympy.Symbol("x"))
        alphaclops.decompose_two_qubit_interaction_into_four_fsim_gates(np.eye(4), fsim_gate=fsim)


def test_decompose_two_qubit_interaction_into_four_fsim_gates():
    iswap = alphaclops.FSimGate(theta=np.pi / 2, phi=0)

    # Defaults to line qubits.
    c = alphaclops.decompose_two_qubit_interaction_into_four_fsim_gates(np.eye(4), fsim_gate=iswap)
    assert set(c.all_qubits()) == set(alphaclops.LineQubit.range(2))

    # Infers from operation but not gate.
    c = alphaclops.decompose_two_qubit_interaction_into_four_fsim_gates(alphaclops.CZ, fsim_gate=iswap)
    assert set(c.all_qubits()) == set(alphaclops.LineQubit.range(2))
    c = alphaclops.decompose_two_qubit_interaction_into_four_fsim_gates(
        alphaclops.CZ(*alphaclops.LineQubit.range(20, 22)), fsim_gate=iswap
    )
    assert set(c.all_qubits()) == set(alphaclops.LineQubit.range(20, 22))

    # Can override.
    c = alphaclops.decompose_two_qubit_interaction_into_four_fsim_gates(
        np.eye(4), fsim_gate=iswap, qubits=alphaclops.LineQubit.range(10, 12)
    )
    assert set(c.all_qubits()) == set(alphaclops.LineQubit.range(10, 12))
    c = alphaclops.decompose_two_qubit_interaction_into_four_fsim_gates(
        alphaclops.CZ(*alphaclops.LineQubit.range(20, 22)), fsim_gate=iswap, qubits=alphaclops.LineQubit.range(10, 12)
    )
    assert set(c.all_qubits()) == set(alphaclops.LineQubit.range(10, 12))


def test_sticky_0_to_1():
    assert _sticky_0_to_1(-1, atol=1e-8) is None

    assert _sticky_0_to_1(-1e-6, atol=1e-8) is None
    assert _sticky_0_to_1(-1e-10, atol=1e-8) == 0
    assert _sticky_0_to_1(0, atol=1e-8) == 0
    assert _sticky_0_to_1(1e-10, atol=1e-8) == 1e-10
    assert _sticky_0_to_1(1e-6, atol=1e-8) == 1e-6

    assert _sticky_0_to_1(0.5, atol=1e-8) == 0.5

    assert _sticky_0_to_1(1 - 1e-6, atol=1e-8) == 1 - 1e-6
    assert _sticky_0_to_1(1 - 1e-10, atol=1e-8) == 1 - 1e-10
    assert _sticky_0_to_1(1, atol=1e-8) == 1
    assert _sticky_0_to_1(1 + 1e-10, atol=1e-8) == 1
    assert _sticky_0_to_1(1 + 1e-6, atol=1e-8) is None

    assert _sticky_0_to_1(2, atol=1e-8) is None

    assert _sticky_0_to_1(-0.1, atol=0.5) == 0
