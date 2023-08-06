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

import unittest.mock as mock

import numpy as np
import sympy

import alphaclops


def test_apply_gate():
    q0, q1 = alphaclops.LineQubit.range(2)
    state = mock.Mock()
    args = alphaclops.StabilizerSimulationState(state=state, qubits=[q0, q1])

    assert args._strat_apply_gate(alphaclops.X, [q0]) is True
    state.apply_x.assert_called_with(0, 1.0, 0.0)

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.X ** 2, [q0]) is True
    state.apply_x.assert_called_with(0, 2.0, 0.0)

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.X ** sympy.Symbol('t'), [q0]) is NotImplemented
    state.apply_x.assert_not_called()

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.XPowGate(exponent=2, global_shift=1.3), [q1]) is True
    state.apply_x.assert_called_with(1, 2.0, 1.3)

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.X ** 1.4, [q0]) == NotImplemented
    state.apply_x.assert_not_called()

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.Y, [q0]) is True
    state.apply_y.assert_called_with(0, 1.0, 0.0)

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.Z, [q0]) is True
    state.apply_z.assert_called_with(0, 1.0, 0.0)

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.H, [q0]) is True
    state.apply_h.assert_called_with(0, 1.0, 0.0)

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.CX, [q0, q1]) is True
    state.apply_cx.assert_called_with(0, 1, 1.0, 0.0)

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.CX, [q1, q0]) is True
    state.apply_cx.assert_called_with(1, 0, 1.0, 0.0)

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.CZ, [q0, q1]) is True
    state.apply_cz.assert_called_with(0, 1, 1.0, 0.0)

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.GlobalPhaseGate(1j), []) is True
    state.apply_global_phase.assert_called_with(1j)

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.GlobalPhaseGate(sympy.Symbol('t')), []) is NotImplemented
    state.apply_global_phase.assert_not_called()

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.SWAP, [q0, q1]) is True
    state.apply_cx.assert_has_calls([mock.call(0, 1), mock.call(1, 0, 1.0, 0.0), mock.call(0, 1)])

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.SwapPowGate(exponent=2, global_shift=1.3), [q0, q1]) is True
    state.apply_cx.assert_has_calls([mock.call(0, 1), mock.call(1, 0, 2.0, 1.3), mock.call(0, 1)])

    state.reset_mock()
    assert args._strat_apply_gate(alphaclops.BitFlipChannel(0.5), [q0]) == NotImplemented
    state.apply_x.assert_not_called()


def test_apply_mixture():
    q0 = alphaclops.LineQubit(0)
    state = mock.Mock()
    args = alphaclops.StabilizerSimulationState(state=state, qubits=[q0])

    for _ in range(100):
        assert args._strat_apply_mixture(alphaclops.BitFlipChannel(0.5), [q0]) is True
    state.apply_x.assert_called_with(0, 1.0, 0.0)
    assert 10 < state.apply_x.call_count < 90


def test_act_from_single_qubit_decompose():
    q0 = alphaclops.LineQubit(0)
    state = mock.Mock()
    args = alphaclops.StabilizerSimulationState(state=state, qubits=[q0])
    assert (
        args._strat_act_from_single_qubit_decompose(
            alphaclops.MatrixGate(np.array([[0, 1], [1, 0]])), [q0]
        )
        is True
    )
    state.apply_x.assert_called_with(0, 1.0, 0.0)


def test_decompose():
    class XContainer(alphaclops.Gate):
        def _decompose_(self, qs):
            return [alphaclops.X(*qs)]

        def _qid_shape_(self):
            pass

    q0 = alphaclops.LineQubit(0)
    state = mock.Mock()
    args = alphaclops.StabilizerSimulationState(state=state, qubits=[q0])
    assert args._strat_decompose(XContainer(), [q0]) is True
    state.apply_x.assert_called_with(0, 1.0, 0.0)
