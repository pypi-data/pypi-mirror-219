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

import alphaclops
from alphaclops.testing import assert_allclose_up_to_global_phase


def test_misaligned_qubits():
    qubits = alphaclops.LineQubit.range(1)
    tableau = alphaclops.CliffordTableau(num_qubits=2)
    with pytest.raises(ValueError):
        alphaclops.decompose_clifford_tableau_to_operations(qubits, tableau)


def test_clifford_decompose_one_qubit():
    """Two random instance for one qubit decomposition."""
    qubits = alphaclops.LineQubit.range(1)
    args = alphaclops.CliffordTableauSimulationState(
        tableau=alphaclops.CliffordTableau(num_qubits=1), qubits=qubits, prng=np.random.RandomState()
    )
    alphaclops.act_on(alphaclops.X, args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.H, args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.S, args, qubits=[qubits[0]], allow_decompose=False)
    expect_circ = alphaclops.Circuit(alphaclops.X(qubits[0]), alphaclops.H(qubits[0]), alphaclops.S(qubits[0]))
    ops = alphaclops.decompose_clifford_tableau_to_operations(qubits, args.tableau)
    circ = alphaclops.Circuit(ops)
    assert_allclose_up_to_global_phase(alphaclops.unitary(expect_circ), alphaclops.unitary(circ), atol=1e-7)

    qubits = alphaclops.LineQubit.range(1)
    args = alphaclops.CliffordTableauSimulationState(
        tableau=alphaclops.CliffordTableau(num_qubits=1), qubits=qubits, prng=np.random.RandomState()
    )
    alphaclops.act_on(alphaclops.Z, args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.H, args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.S, args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.H, args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.X, args, qubits=[qubits[0]], allow_decompose=False)
    expect_circ = alphaclops.Circuit(
        alphaclops.Z(qubits[0]),
        alphaclops.H(qubits[0]),
        alphaclops.S(qubits[0]),
        alphaclops.H(qubits[0]),
        alphaclops.X(qubits[0]),
    )
    ops = alphaclops.decompose_clifford_tableau_to_operations(qubits, args.tableau)
    circ = alphaclops.Circuit(ops)
    assert_allclose_up_to_global_phase(alphaclops.unitary(expect_circ), alphaclops.unitary(circ), atol=1e-7)


def test_clifford_decompose_two_qubits():
    """Two random instance for two qubits decomposition."""
    qubits = alphaclops.LineQubit.range(2)
    args = alphaclops.CliffordTableauSimulationState(
        tableau=alphaclops.CliffordTableau(num_qubits=2), qubits=qubits, prng=np.random.RandomState()
    )
    alphaclops.act_on(alphaclops.H, args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.CNOT, args, qubits=[qubits[0], qubits[1]], allow_decompose=False)
    expect_circ = alphaclops.Circuit(alphaclops.H(qubits[0]), alphaclops.CNOT(qubits[0], qubits[1]))
    ops = alphaclops.decompose_clifford_tableau_to_operations(qubits, args.tableau)
    circ = alphaclops.Circuit(ops)
    assert_allclose_up_to_global_phase(alphaclops.unitary(expect_circ), alphaclops.unitary(circ), atol=1e-7)

    qubits = alphaclops.LineQubit.range(2)
    args = alphaclops.CliffordTableauSimulationState(
        tableau=alphaclops.CliffordTableau(num_qubits=2), qubits=qubits, prng=np.random.RandomState()
    )
    alphaclops.act_on(alphaclops.H, args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.CNOT, args, qubits=[qubits[0], qubits[1]], allow_decompose=False)
    alphaclops.act_on(alphaclops.H, args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.S, args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.X, args, qubits=[qubits[1]], allow_decompose=False)
    expect_circ = alphaclops.Circuit(
        alphaclops.H(qubits[0]),
        alphaclops.CNOT(qubits[0], qubits[1]),
        alphaclops.H(qubits[0]),
        alphaclops.S(qubits[0]),
        alphaclops.X(qubits[1]),
    )

    ops = alphaclops.decompose_clifford_tableau_to_operations(qubits, args.tableau)
    circ = alphaclops.Circuit(ops)
    assert_allclose_up_to_global_phase(alphaclops.unitary(expect_circ), alphaclops.unitary(circ), atol=1e-7)


def test_clifford_decompose_by_unitary():
    """Validate the decomposition of random Clifford Tableau by unitary matrix.

    Due to the exponential growth in dimension, it cannot validate very large number of qubits.
    """
    n, num_ops = 5, 20
    gate_candidate = [alphaclops.X, alphaclops.Y, alphaclops.Z, alphaclops.H, alphaclops.S, alphaclops.CNOT, alphaclops.CZ]
    for seed in range(100):
        prng = np.random.RandomState(seed)
        t = alphaclops.CliffordTableau(num_qubits=n)
        qubits = alphaclops.LineQubit.range(n)
        expect_circ = alphaclops.Circuit()
        args = alphaclops.CliffordTableauSimulationState(tableau=t, qubits=qubits, prng=prng)
        for _ in range(num_ops):
            g = prng.randint(len(gate_candidate))
            indices = (prng.randint(n),) if g < 5 else prng.choice(n, 2, replace=False)
            alphaclops.act_on(
                gate_candidate[g], args, qubits=[qubits[i] for i in indices], allow_decompose=False
            )
            expect_circ.append(gate_candidate[g].on(*[qubits[i] for i in indices]))
        ops = alphaclops.decompose_clifford_tableau_to_operations(qubits, args.tableau)
        circ = alphaclops.Circuit(ops)
        circ.append(alphaclops.I.on_each(qubits))
        expect_circ.append(alphaclops.I.on_each(qubits))
        assert_allclose_up_to_global_phase(alphaclops.unitary(expect_circ), alphaclops.unitary(circ), atol=1e-7)


def test_clifford_decompose_by_reconstruction():
    """Validate the decomposition of random Clifford Tableau by reconstruction.

    This approach can validate large number of qubits compared with the unitary one.
    """
    n, num_ops = 100, 500
    gate_candidate = [alphaclops.X, alphaclops.Y, alphaclops.Z, alphaclops.H, alphaclops.S, alphaclops.CNOT, alphaclops.CZ]
    for seed in range(10):
        prng = np.random.RandomState(seed)
        t = alphaclops.CliffordTableau(num_qubits=n)
        qubits = alphaclops.LineQubit.range(n)
        expect_circ = alphaclops.Circuit()
        args = alphaclops.CliffordTableauSimulationState(tableau=t, qubits=qubits, prng=prng)
        for _ in range(num_ops):
            g = prng.randint(len(gate_candidate))
            indices = (prng.randint(n),) if g < 5 else prng.choice(n, 2, replace=False)
            alphaclops.act_on(
                gate_candidate[g], args, qubits=[qubits[i] for i in indices], allow_decompose=False
            )
            expect_circ.append(gate_candidate[g].on(*[qubits[i] for i in indices]))
        ops = alphaclops.decompose_clifford_tableau_to_operations(qubits, args.tableau)

        reconstruct_t = alphaclops.CliffordTableau(num_qubits=n)
        reconstruct_args = alphaclops.CliffordTableauSimulationState(
            tableau=reconstruct_t, qubits=qubits, prng=prng
        )
        for op in ops:
            alphaclops.act_on(op.gate, reconstruct_args, qubits=op.qubits, allow_decompose=False)

        assert t == reconstruct_t
