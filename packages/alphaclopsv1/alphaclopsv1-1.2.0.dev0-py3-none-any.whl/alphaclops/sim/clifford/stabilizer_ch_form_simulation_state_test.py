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


def test_init_state():
    args = alphaclops.StabilizerChFormSimulationState(qubits=alphaclops.LineQubit.range(1), initial_state=1)
    np.testing.assert_allclose(args.state.state_vector(), [0, 1])
    with pytest.raises(ValueError, match='Must specify qubits'):
        _ = alphaclops.StabilizerChFormSimulationState(initial_state=1)


def test_cannot_act():
    class NoDetails(alphaclops.testing.SingleQubitGate):
        pass

    args = alphaclops.StabilizerChFormSimulationState(qubits=[], prng=np.random.RandomState())

    with pytest.raises(TypeError, match="Failed to act"):
        alphaclops.act_on(NoDetails(), args, qubits=())


def test_gate_with_act_on():
    class CustomGate(alphaclops.testing.SingleQubitGate):
        def _act_on_(self, sim_state, qubits):
            if isinstance(sim_state, alphaclops.StabilizerChFormSimulationState):
                qubit = sim_state.qubit_map[qubits[0]]
                sim_state.state.gamma[qubit] += 1
                return True

    state = alphaclops.StabilizerStateChForm(num_qubits=3)
    args = alphaclops.StabilizerChFormSimulationState(
        qubits=alphaclops.LineQubit.range(3), prng=np.random.RandomState(), initial_state=state
    )

    alphaclops.act_on(CustomGate(), args, [alphaclops.LineQubit(1)])

    np.testing.assert_allclose(state.gamma, [0, 1, 0])


def test_unitary_fallback_y():
    class UnitaryYGate(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 1

        def _unitary_(self):
            return np.array([[0, -1j], [1j, 0]])

    args = alphaclops.StabilizerChFormSimulationState(
        qubits=alphaclops.LineQubit.range(3), prng=np.random.RandomState()
    )
    alphaclops.act_on(UnitaryYGate(), args, [alphaclops.LineQubit(1)])
    expected_args = alphaclops.StabilizerChFormSimulationState(
        qubits=alphaclops.LineQubit.range(3), prng=np.random.RandomState()
    )
    alphaclops.act_on(alphaclops.Y, expected_args, [alphaclops.LineQubit(1)])
    np.testing.assert_allclose(args.state.state_vector(), expected_args.state.state_vector())


def test_unitary_fallback_h():
    class UnitaryHGate(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 1

        def _unitary_(self):
            return np.array([[1, 1], [1, -1]]) / (2**0.5)

    args = alphaclops.StabilizerChFormSimulationState(
        qubits=alphaclops.LineQubit.range(3), prng=np.random.RandomState()
    )
    alphaclops.act_on(UnitaryHGate(), args, [alphaclops.LineQubit(1)])
    expected_args = alphaclops.StabilizerChFormSimulationState(
        qubits=alphaclops.LineQubit.range(3), prng=np.random.RandomState()
    )
    alphaclops.act_on(alphaclops.H, expected_args, [alphaclops.LineQubit(1)])
    np.testing.assert_allclose(args.state.state_vector(), expected_args.state.state_vector())


def test_copy():
    args = alphaclops.StabilizerChFormSimulationState(
        qubits=alphaclops.LineQubit.range(3), prng=np.random.RandomState()
    )
    args1 = args.copy()
    assert isinstance(args1, alphaclops.StabilizerChFormSimulationState)
    assert args is not args1
    assert args.state is not args1.state
    np.testing.assert_equal(args.state.state_vector(), args1.state.state_vector())
    assert args.qubits == args1.qubits
    assert args.prng is args1.prng
    assert args.log_of_measurement_results is not args1.log_of_measurement_results
    assert args.log_of_measurement_results == args1.log_of_measurement_results
