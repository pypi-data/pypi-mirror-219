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
import pytest
import sympy

import alphaclops


def test_init():
    op = alphaclops.global_phase_operation(1j)
    assert op.gate.coefficient == 1j
    assert op.qubits == ()
    assert op.with_qubits() == op
    assert alphaclops.has_stabilizer_effect(op)

    with pytest.raises(ValueError, match='not unitary'):
        _ = alphaclops.global_phase_operation(2)
    with pytest.raises(ValueError, match='0 qubits'):
        _ = alphaclops.global_phase_operation(1j).with_qubits(alphaclops.LineQubit(0))


def test_protocols():
    for p in [1, 1j, -1]:
        alphaclops.testing.assert_implements_consistent_protocols(alphaclops.global_phase_operation(p))

    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.global_phase_operation(1j)), np.array([[1j]]), atol=1e-8
    )


@pytest.mark.parametrize('phase', [1, 1j, -1])
def test_act_on_tableau(phase):
    original_tableau = alphaclops.CliffordTableau(0)
    args = alphaclops.CliffordTableauSimulationState(original_tableau.copy(), np.random.RandomState())
    alphaclops.act_on(alphaclops.global_phase_operation(phase), args, allow_decompose=False)
    assert args.tableau == original_tableau


@pytest.mark.parametrize('phase', [1, 1j, -1])
def test_act_on_ch_form(phase):
    state = alphaclops.StabilizerStateChForm(0)
    args = alphaclops.StabilizerChFormSimulationState(
        qubits=[], prng=np.random.RandomState(), initial_state=state
    )
    alphaclops.act_on(alphaclops.global_phase_operation(phase), args, allow_decompose=False)
    assert state.state_vector() == [[phase]]


def test_str():
    assert str(alphaclops.global_phase_operation(1j)) == '1j'


def test_repr():
    op = alphaclops.global_phase_operation(1j)
    alphaclops.testing.assert_equivalent_repr(op)


def test_diagram():
    a, b = alphaclops.LineQubit.range(2)
    x, y = alphaclops.LineQubit.range(10, 12)

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            [alphaclops.Moment([alphaclops.CNOT(a, x), alphaclops.CNOT(b, y), alphaclops.global_phase_operation(-1)])]
        ),
        """
                ┌──┐
0: ──────────────@─────
                 │
1: ──────────────┼@────
                 ││
10: ─────────────X┼────
                  │
11: ──────────────X────

global phase:    π
                └──┘
        """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            [
                alphaclops.Moment(
                    [
                        alphaclops.CNOT(a, x),
                        alphaclops.CNOT(b, y),
                        alphaclops.global_phase_operation(-1),
                        alphaclops.global_phase_operation(-1),
                    ]
                )
            ]
        ),
        """
                ┌──┐
0: ──────────────@─────
                 │
1: ──────────────┼@────
                 ││
10: ─────────────X┼────
                  │
11: ──────────────X────

global phase:
                └──┘
        """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            [
                alphaclops.Moment(
                    [
                        alphaclops.CNOT(a, x),
                        alphaclops.CNOT(b, y),
                        alphaclops.global_phase_operation(-1),
                        alphaclops.global_phase_operation(-1),
                    ]
                ),
                alphaclops.Moment([alphaclops.global_phase_operation(1j)]),
                alphaclops.Moment([alphaclops.X(a)]),
            ]
        ),
        """
                ┌──┐
0: ──────────────@────────────X───
                 │
1: ──────────────┼@───────────────
                 ││
10: ─────────────X┼───────────────
                  │
11: ──────────────X───────────────

global phase:          0.5π
                └──┘
        """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.global_phase_operation(-1j)])]),
        """
0: ─────────────X───────────

global phase:       -0.5π
        """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a), alphaclops.global_phase_operation(np.exp(1j))])]),
        """
0: ─────────────X────────

global phase:   0.318π
        """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a), alphaclops.global_phase_operation(np.exp(1j))])]),
        """
0: ─────────────X──────────

global phase:   0.31831π
        """,
        precision=5,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            [
                alphaclops.Moment([alphaclops.X(a), alphaclops.global_phase_operation(1j)]),
                alphaclops.Moment([alphaclops.global_phase_operation(-1j)]),
            ]
        ),
        """
0: -------------X----------------

global phase:   0.5pi   -0.5pi
        """,
        use_unicode_characters=False,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit([alphaclops.Moment([alphaclops.global_phase_operation(-1j)])]),
        """
global phase:   -0.5π
        """,
    )


def test_gate_init():
    gate = alphaclops.GlobalPhaseGate(1j)
    assert gate.coefficient == 1j
    assert isinstance(gate.on(), alphaclops.GateOperation)
    assert gate.on().gate == gate
    assert alphaclops.has_stabilizer_effect(gate)

    with pytest.raises(ValueError, match='Coefficient is not unitary'):
        _ = alphaclops.GlobalPhaseGate(2)
    with pytest.raises(ValueError, match='Wrong number of qubits'):
        _ = gate.on(alphaclops.LineQubit(0))


def test_gate_protocols():
    for p in [1, 1j, -1]:
        alphaclops.testing.assert_implements_consistent_protocols(alphaclops.GlobalPhaseGate(p))

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.GlobalPhaseGate(1j)), np.array([[1j]]), atol=1e-8)


@pytest.mark.parametrize('phase', [1, 1j, -1])
def test_gate_act_on_tableau(phase):
    original_tableau = alphaclops.CliffordTableau(0)
    args = alphaclops.CliffordTableauSimulationState(original_tableau.copy(), np.random.RandomState())
    alphaclops.act_on(alphaclops.GlobalPhaseGate(phase), args, qubits=(), allow_decompose=False)
    assert args.tableau == original_tableau


@pytest.mark.parametrize('phase', [1, 1j, -1])
def test_gate_act_on_ch_form(phase):
    state = alphaclops.StabilizerStateChForm(0)
    args = alphaclops.StabilizerChFormSimulationState(
        qubits=[], prng=np.random.RandomState(), initial_state=state
    )
    alphaclops.act_on(alphaclops.GlobalPhaseGate(phase), args, qubits=(), allow_decompose=False)
    assert state.state_vector() == [[phase]]


def test_gate_str():
    assert str(alphaclops.GlobalPhaseGate(1j)) == '1j'


def test_gate_repr():
    gate = alphaclops.GlobalPhaseGate(1j)
    alphaclops.testing.assert_equivalent_repr(gate)


def test_gate_op_repr():
    gate = alphaclops.GlobalPhaseGate(1j)
    alphaclops.testing.assert_equivalent_repr(gate.on())


def test_gate_global_phase_op_json_dict():
    assert alphaclops.GlobalPhaseGate(-1j)._json_dict_() == {'coefficient': -1j}


def test_parameterization():
    t = sympy.Symbol('t')
    gpt = alphaclops.GlobalPhaseGate(coefficient=t)
    assert alphaclops.is_parameterized(gpt)
    assert alphaclops.parameter_names(gpt) == {'t'}
    assert not alphaclops.has_unitary(gpt)
    assert gpt.coefficient == t
    assert (gpt**2).coefficient == t**2


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_resolve(resolve_fn):
    t = sympy.Symbol('t')
    gpt = alphaclops.GlobalPhaseGate(coefficient=t)
    assert resolve_fn(gpt, {'t': -1}) == alphaclops.GlobalPhaseGate(coefficient=-1)


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_resolve_error(resolve_fn):
    t = sympy.Symbol('t')
    gpt = alphaclops.GlobalPhaseGate(coefficient=t)
    with pytest.raises(ValueError, match='Coefficient is not unitary'):
        resolve_fn(gpt, {'t': -2})


@pytest.mark.parametrize(
    'coeff, exp', [(-1, 1), (1j, 0.5), (-1j, -0.5), (1 / np.sqrt(2) * (1 + 1j), 0.25)]
)
def test_global_phase_gate_controlled(coeff, exp):
    g = alphaclops.GlobalPhaseGate(coeff)
    op = alphaclops.global_phase_operation(coeff)
    q = alphaclops.LineQubit.range(3)
    for num_controls, target_gate in zip(range(1, 4), [alphaclops.Z, alphaclops.CZ, alphaclops.CCZ]):
        assert g.controlled(num_controls) == target_gate**exp
        np.testing.assert_allclose(
            alphaclops.unitary(alphaclops.ControlledGate(g, num_controls)),
            alphaclops.unitary(g.controlled(num_controls)),
        )
        assert op.controlled_by(*q[:num_controls]) == target_gate(*q[:num_controls]) ** exp
    assert g.controlled(control_values=[0]) == alphaclops.ControlledGate(g, control_values=[0])
    xor_control_values = alphaclops.SumOfProducts(((0, 0), (1, 1)))
    assert g.controlled(control_values=xor_control_values) == alphaclops.ControlledGate(
        g, control_values=xor_control_values
    )
