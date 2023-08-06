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
from typing import Sequence

import numpy as np
import pytest

import alphaclops

Q0, Q1, Q2, Q3 = alphaclops.LineQubit.range(4)


def test_state_tomography_diagonal():
    n = 2
    qubits = alphaclops.LineQubit.range(n)
    for state in range(2**n):
        circuit = alphaclops.Circuit()
        for i, q in enumerate(qubits):
            bit = state & (1 << (n - i - 1))
            if bit:
                circuit.append(alphaclops.X(q))
        res = alphaclops.experiments.state_tomography(
            alphaclops.Simulator(seed=87539319),
            qubits,
            circuit,
            repetitions=1000,
            prerotations=[(0, 0), (0, 0.5), (0.5, 0.5)],
        )
        should_be = np.zeros((2**n, 2**n))
        should_be[state, state] = 1
        assert np.allclose(res.data, should_be, atol=0.05)


def test_state_tomography_ghz_state():
    circuit = alphaclops.Circuit()
    circuit.append(alphaclops.H(alphaclops.LineQubit(0)))
    circuit.append(alphaclops.CNOT(alphaclops.LineQubit(0), alphaclops.LineQubit(1)))
    circuit.append(alphaclops.CNOT(alphaclops.LineQubit(0), alphaclops.LineQubit(2)))
    res = alphaclops.experiments.state_tomography(
        alphaclops.Simulator(seed=87539319),
        [alphaclops.LineQubit(0), alphaclops.LineQubit(1), alphaclops.LineQubit(2)],
        circuit,
        repetitions=1000,
    )
    should_be = np.zeros((8, 8))
    should_be[0, 0] = 0.5
    should_be[7, 7] = 0.5
    should_be[0, 7] = 0.5
    should_be[7, 0] = 0.5
    assert np.allclose(res.data, should_be, atol=0.05)


def test_make_experiment_no_rots():
    exp = alphaclops.experiments.StateTomographyExperiment(
        [alphaclops.LineQubit(0), alphaclops.LineQubit(1), alphaclops.LineQubit(2)]
    )
    assert len(exp.rot_sweep) > 0


def compute_density_matrix(circuit: alphaclops.Circuit, qubits: Sequence[alphaclops.Qid]) -> np.ndarray:
    """Computes density matrix prepared by circuit based on its unitary."""
    u = circuit.unitary(qubit_order=qubits)
    phi = u[:, 0]
    rho = np.outer(phi, np.conjugate(phi))
    return rho


@pytest.mark.parametrize(
    'circuit, qubits',
    (
        (alphaclops.Circuit(alphaclops.X(Q0) ** 0.25), (Q0,)),
        (alphaclops.Circuit(alphaclops.CNOT(Q0, Q1) ** 0.25), (Q0, Q1)),
        (alphaclops.Circuit(alphaclops.CNOT(Q0, Q1) ** 0.25), (Q1, Q0)),
        (alphaclops.Circuit(alphaclops.TOFFOLI(Q0, Q1, Q2)), (Q1, Q0, Q2)),
        (
                alphaclops.Circuit(
                alphaclops.H(Q0),
                alphaclops.H(Q1),
                alphaclops.CNOT(Q0, Q2),
                alphaclops.CNOT(Q1, Q3),
                alphaclops.X(Q0),
                alphaclops.X(Q1),
                alphaclops.CNOT(Q1, Q0),
            ),
                (Q1, Q0, Q2, Q3),
        ),
    ),
)
def test_density_matrix_from_state_tomography_is_correct(circuit, qubits):
    sim = alphaclops.Simulator(seed=87539319)
    tomography_result = alphaclops.experiments.state_tomography(sim, qubits, circuit, repetitions=5000)
    actual_rho = tomography_result.data
    expected_rho = compute_density_matrix(circuit, qubits)
    error_rho = actual_rho - expected_rho
    assert np.linalg.norm(error_rho) < 0.05
    assert np.max(np.abs(error_rho)) < 0.05


@pytest.mark.parametrize(
    'circuit',
    (
            alphaclops.Circuit(alphaclops.CNOT(Q0, Q1) ** 0.3),
            alphaclops.Circuit(alphaclops.H(Q0), alphaclops.CNOT(Q0, Q1)),
            alphaclops.Circuit(alphaclops.X(Q0) ** 0.25, alphaclops.ISWAP(Q0, Q1)),
    ),
)
def test_agrees_with_two_qubit_state_tomography(circuit):
    qubits = (Q0, Q1)
    sim = alphaclops.Simulator(seed=87539319)
    tomography_result = alphaclops.experiments.state_tomography(sim, qubits, circuit, repetitions=5000)
    actual_rho = tomography_result.data

    two_qubit_tomography_result = alphaclops.experiments.two_qubit_state_tomography(
        sim, qubits[0], qubits[1], circuit, repetitions=5000
    )
    expected_rho = two_qubit_tomography_result.data

    error_rho = actual_rho - expected_rho

    assert np.linalg.norm(error_rho) < 0.06
    assert np.max(np.abs(error_rho)) < 0.05
