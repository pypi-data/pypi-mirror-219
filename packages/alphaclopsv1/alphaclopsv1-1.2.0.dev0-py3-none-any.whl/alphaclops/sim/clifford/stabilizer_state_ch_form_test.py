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

import alphaclops
import alphaclops.testing

# TODO: This and clifford tableau need tests.
# Github issue: https://github.com/quantumlib/alphaclops/issues/3021


def test_initial_state():
    with pytest.raises(ValueError, match='Out of range'):
        _ = alphaclops.StabilizerStateChForm(initial_state=-31, num_qubits=5)
    with pytest.raises(ValueError, match='Out of range'):
        _ = alphaclops.StabilizerStateChForm(initial_state=32, num_qubits=5)
    state = alphaclops.StabilizerStateChForm(initial_state=23, num_qubits=5)
    expected_state_vector = np.zeros(32)
    expected_state_vector[23] = 1
    np.testing.assert_allclose(state.state_vector(), expected_state_vector)


def test_run():
    (q0, q1, q2) = (alphaclops.LineQubit(0), alphaclops.LineQubit(1), alphaclops.LineQubit(2))

    """
    0: ───H───@───────────────X───M───────────
              │
    1: ───────X───@───────X───────────X───M───
                  │                   │
    2: ───────────X───M───────────────@───────

    After the third moment, before the measurement, the state is |000> + |111>.
    After measurement of q2, q0 and q1 both get a bit flip, so the q0
    measurement always yields opposite of the q2 measurement. q1 has an
    additional controlled not from q2, making it yield 1 always when measured.
    If there were no measurements in the circuit, the final state would be
    |110> + |011>.
    """
    circuit = alphaclops.Circuit(
        alphaclops.H(q0),
        alphaclops.CNOT(q0, q1),
        alphaclops.CNOT(q1, q2),
        alphaclops.measure(q2),
        alphaclops.X(q1),
        alphaclops.X(q0),
        alphaclops.measure(q0),
        alphaclops.CNOT(q2, q1),
        alphaclops.measure(q1),
        strategy=alphaclops.InsertStrategy.NEW,
    )
    for _ in range(10):
        state = alphaclops.StabilizerStateChForm(num_qubits=3)
        classical_data = alphaclops.ClassicalDataDictionaryStore()
        for op in circuit.all_operations():
            args = alphaclops.StabilizerChFormSimulationState(
                qubits=list(circuit.all_qubits()),
                prng=np.random.RandomState(),
                classical_data=classical_data,
                initial_state=state,
            )
            alphaclops.act_on(op, args)
        measurements = {str(k): list(v[-1]) for k, v in classical_data.records.items()}
        assert measurements['q(1)'] == [1]
        assert measurements['q(0)'] != measurements['q(2)']
