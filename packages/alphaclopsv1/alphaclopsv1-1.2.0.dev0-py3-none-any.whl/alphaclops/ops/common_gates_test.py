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

import numpy as np
import pytest
import sympy

import alphaclops
from alphaclops.protocols.act_on_protocol_test import DummySimulationState

H = np.array([[1, 1], [1, -1]]) * np.sqrt(0.5)
HH = alphaclops.kron(H, H)
QFT2 = np.array([[1, 1, 1, 1], [1, 1j, -1, -1j], [1, -1, 1, -1], [1, -1j, -1, 1j]]) * 0.5


@pytest.mark.parametrize(
    'eigen_gate_type', [alphaclops.CZPowGate, alphaclops.XPowGate, alphaclops.YPowGate, alphaclops.ZPowGate]
)
def test_phase_insensitive_eigen_gates_consistent_protocols(eigen_gate_type):
    alphaclops.testing.assert_eigengate_implements_consistent_protocols(eigen_gate_type)


@pytest.mark.parametrize('eigen_gate_type', [alphaclops.CNotPowGate, alphaclops.HPowGate])
def test_phase_sensitive_eigen_gates_consistent_protocols(eigen_gate_type):
    alphaclops.testing.assert_eigengate_implements_consistent_protocols(eigen_gate_type)


def test_cz_init():
    assert alphaclops.CZPowGate(exponent=0.5).exponent == 0.5
    assert alphaclops.CZPowGate(exponent=5).exponent == 5
    assert (alphaclops.CZ ** 0.5).exponent == 0.5


@pytest.mark.parametrize('theta,pi', [(0.4, np.pi), (sympy.Symbol("theta"), sympy.pi)])
def test_transformations(theta, pi):
    initialRx = alphaclops.rx(theta)
    expectedPowx = alphaclops.X ** (theta / pi)
    receivedPowx = initialRx.with_canonical_global_phase()
    backToRx = receivedPowx.in_su2()
    assert receivedPowx == expectedPowx
    assert backToRx == initialRx
    initialRy = alphaclops.ry(theta)
    expectedPowy = alphaclops.Y ** (theta / pi)
    receivedPowy = initialRy.with_canonical_global_phase()
    backToRy = receivedPowy.in_su2()
    assert receivedPowy == expectedPowy
    assert backToRy == initialRy
    initialRz = alphaclops.rz(theta)
    expectedPowz = alphaclops.Z ** (theta / pi)
    receivedPowz = initialRz.with_canonical_global_phase()
    backToRz = receivedPowz.in_su2()
    assert receivedPowz == expectedPowz
    assert backToRz == initialRz


def test_cz_str():
    assert str(alphaclops.CZ) == 'CZ'
    assert str(alphaclops.CZ ** 0.5) == 'CZ**0.5'
    assert str(alphaclops.CZ ** -0.25) == 'CZ**-0.25'


def test_cz_repr():
    assert repr(alphaclops.CZ) == 'alphaclops.CZ'
    assert repr(alphaclops.CZ ** 0.5) == '(alphaclops.CZ**0.5)'
    assert repr(alphaclops.CZ ** -0.25) == '(alphaclops.CZ**-0.25)'


def test_cz_unitary():
    assert np.allclose(
        alphaclops.unitary(alphaclops.CZ), np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])
    )

    assert np.allclose(
        alphaclops.unitary(alphaclops.CZ ** 0.5),
        np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1j]]),
    )

    assert np.allclose(
        alphaclops.unitary(alphaclops.CZ ** 0),
        np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
    )

    assert np.allclose(
        alphaclops.unitary(alphaclops.CZ ** -0.5),
        np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1j]]),
    )


def test_z_init():
    z = alphaclops.ZPowGate(exponent=5)
    assert z.exponent == 5

    # Canonicalizes exponent for equality, but keeps the inner details.
    assert alphaclops.Z ** 0.5 != alphaclops.Z ** -0.5
    assert (alphaclops.Z ** -1) ** 0.5 == alphaclops.Z ** -0.5
    assert alphaclops.Z ** -1 == alphaclops.Z


@pytest.mark.parametrize(
    'input_gate, specialized_output',
    [
        (alphaclops.Z, alphaclops.CZ),
        (alphaclops.CZ, alphaclops.CCZ),
        (alphaclops.X, alphaclops.CX),
        (alphaclops.CX, alphaclops.CCX),
        (alphaclops.ZPowGate(exponent=0.5), alphaclops.CZPowGate(exponent=0.5)),
        (alphaclops.CZPowGate(exponent=0.5), alphaclops.CCZPowGate(exponent=0.5)),
        (alphaclops.XPowGate(exponent=0.5), alphaclops.CXPowGate(exponent=0.5)),
        (alphaclops.CXPowGate(exponent=0.5), alphaclops.CCXPowGate(exponent=0.5)),
    ],
)
def test_specialized_control(input_gate, specialized_output):
    # Single qubit control on the input gate gives the specialized output
    assert input_gate.controlled() == specialized_output
    assert input_gate.controlled(num_controls=1) == specialized_output
    assert input_gate.controlled(control_values=((1,),)) == specialized_output
    assert input_gate.controlled(control_values=alphaclops.SumOfProducts([[1]])) == specialized_output
    assert input_gate.controlled(control_qid_shape=(2,)) == specialized_output
    assert np.allclose(
        alphaclops.unitary(specialized_output),
        alphaclops.unitary(alphaclops.ControlledGate(input_gate, num_controls=1)),
    )

    # For multi-qudit controls, if the last control is a qubit with control
    # value 1, construct the specialized output leaving the rest of the
    # controls as they are.
    assert input_gate.controlled().controlled() == specialized_output.controlled(num_controls=1)
    assert input_gate.controlled(num_controls=2) == specialized_output.controlled(num_controls=1)
    assert input_gate.controlled(
        control_values=((0,), (0,), (1,))
    ) == specialized_output.controlled(num_controls=2, control_values=((0,), (0,)))
    assert input_gate.controlled(control_qid_shape=(3, 3, 2)) == specialized_output.controlled(
        num_controls=2, control_qid_shape=(3, 3)
    )
    assert input_gate.controlled(control_qid_shape=(2,)).controlled(
        control_qid_shape=(3,)
    ).controlled(control_qid_shape=(4,)) != specialized_output.controlled(
        num_controls=2, control_qid_shape=(3, 4)
    )

    # When a control_value 1 qubit is not acting first, results in a regular
    # ControlledGate on the input gate instance.
    assert input_gate.controlled(num_controls=1, control_qid_shape=(3,)) == alphaclops.ControlledGate(
        input_gate, num_controls=1, control_qid_shape=(3,)
    )
    assert input_gate.controlled(control_values=((0,), (1,), (0,))) == alphaclops.ControlledGate(
        input_gate, num_controls=3, control_values=((0,), (1,), (0,))
    )
    assert input_gate.controlled(control_qid_shape=(3, 2, 3)) == alphaclops.ControlledGate(
        input_gate, num_controls=3, control_qid_shape=(3, 2, 3)
    )
    assert input_gate.controlled(control_qid_shape=(3,)).controlled(
        control_qid_shape=(2,)
    ).controlled(control_qid_shape=(4,)) != alphaclops.ControlledGate(
        input_gate, num_controls=3, control_qid_shape=(3, 2, 4)
    )


@pytest.mark.parametrize(
    'input_gate, specialized_output',
    [
        (alphaclops.Z, alphaclops.CCZ),
        (alphaclops.X, alphaclops.CCX),
        (alphaclops.ZPowGate(exponent=0.5), alphaclops.CCZPowGate(exponent=0.5)),
        (alphaclops.XPowGate(exponent=0.5), alphaclops.CCXPowGate(exponent=0.5)),
    ],
)
def test_specialized_control_two_step(input_gate, specialized_output):
    # Two-qubit control on the input gate gives the specialized output
    assert input_gate.controlled().controlled() == specialized_output
    assert input_gate.controlled(num_controls=2) == specialized_output
    assert input_gate.controlled(control_values=[1, 1]) == specialized_output
    assert input_gate.controlled(control_values=alphaclops.SumOfProducts([[1, 1]])) == specialized_output
    assert input_gate.controlled(control_qid_shape=(2, 2)) == specialized_output
    assert np.allclose(
        alphaclops.unitary(specialized_output),
        alphaclops.unitary(alphaclops.ControlledGate(input_gate, num_controls=2)),
    )


@pytest.mark.parametrize(
    'gate, specialized_type',
    [
        (alphaclops.ZPowGate(global_shift=-0.5, exponent=0.5), alphaclops.CZPowGate),
        (alphaclops.CZPowGate(global_shift=-0.5, exponent=0.5), alphaclops.CCZPowGate),
        (alphaclops.XPowGate(global_shift=-0.5, exponent=0.5), alphaclops.CXPowGate),
        (alphaclops.CXPowGate(global_shift=-0.5, exponent=0.5), alphaclops.CCXPowGate),
    ],
)
def test_no_specialized_control_for_global_shift_non_zero(gate, specialized_type):
    assert not isinstance(gate.controlled(), specialized_type)


@pytest.mark.parametrize(
    'gate, matrix',
    [
        (alphaclops.ZPowGate(global_shift=-0.5, exponent=1), np.diag([1, 1, -1j, 1j])),
        (alphaclops.CZPowGate(global_shift=-0.5, exponent=1), np.diag([1, 1, 1, 1, -1j, -1j, -1j, 1j])),
        (
                alphaclops.XPowGate(global_shift=-0.5, exponent=1),
                np.block(
                [[np.eye(2), np.zeros((2, 2))], [np.zeros((2, 2)), np.array([[0, -1j], [-1j, 0]])]]
            ),
        ),
        (
                alphaclops.CXPowGate(global_shift=-0.5, exponent=1),
                np.block(
                [
                    [np.diag([1, 1, 1, 1, -1j, -1j]), np.zeros((6, 2))],
                    [np.zeros((2, 6)), np.array([[0, -1j], [-1j, 0]])],
                ]
            ),
        ),
    ],
)
def test_global_phase_controlled_gate(gate, matrix):
    np.testing.assert_equal(alphaclops.unitary(gate.controlled()), matrix)


def test_rot_gates_eq():
    eq = alphaclops.testing.EqualsTester()
    gates = [
        lambda p: alphaclops.CZ ** p,
        lambda p: alphaclops.X ** p,
        lambda p: alphaclops.Y ** p,
        lambda p: alphaclops.Z ** p,
        lambda p: alphaclops.CNOT ** p,
    ]
    for gate in gates:
        eq.add_equality_group(gate(3.5), gate(-0.5))
        eq.make_equality_group(lambda: gate(0))
        eq.make_equality_group(lambda: gate(0.5))

    eq.add_equality_group(alphaclops.XPowGate(), alphaclops.XPowGate(exponent=1), alphaclops.X)
    eq.add_equality_group(alphaclops.YPowGate(), alphaclops.YPowGate(exponent=1), alphaclops.Y)
    eq.add_equality_group(alphaclops.ZPowGate(), alphaclops.ZPowGate(exponent=1), alphaclops.Z)
    eq.add_equality_group(
        alphaclops.ZPowGate(exponent=1, global_shift=-0.5), alphaclops.ZPowGate(exponent=5, global_shift=-0.5)
    )
    eq.add_equality_group(alphaclops.ZPowGate(exponent=3, global_shift=-0.5))
    eq.add_equality_group(alphaclops.ZPowGate(exponent=1, global_shift=-0.1))
    eq.add_equality_group(alphaclops.ZPowGate(exponent=5, global_shift=-0.1))
    eq.add_equality_group(
        alphaclops.CNotPowGate(), alphaclops.CXPowGate(), alphaclops.CNotPowGate(exponent=1), alphaclops.CNOT
    )
    eq.add_equality_group(alphaclops.CZPowGate(), alphaclops.CZPowGate(exponent=1), alphaclops.CZ)


def test_z_unitary():
    assert np.allclose(alphaclops.unitary(alphaclops.Z), np.array([[1, 0], [0, -1]]))
    assert np.allclose(alphaclops.unitary(alphaclops.Z ** 0.5), np.array([[1, 0], [0, 1j]]))
    assert np.allclose(alphaclops.unitary(alphaclops.Z ** 0), np.array([[1, 0], [0, 1]]))
    assert np.allclose(alphaclops.unitary(alphaclops.Z ** -0.5), np.array([[1, 0], [0, -1j]]))


def test_y_unitary():
    assert np.allclose(alphaclops.unitary(alphaclops.Y), np.array([[0, -1j], [1j, 0]]))

    assert np.allclose(
        alphaclops.unitary(alphaclops.Y ** 0.5), np.array([[1 + 1j, -1 - 1j], [1 + 1j, 1 + 1j]]) / 2
    )

    assert np.allclose(alphaclops.unitary(alphaclops.Y ** 0), np.array([[1, 0], [0, 1]]))

    assert np.allclose(
        alphaclops.unitary(alphaclops.Y ** -0.5), np.array([[1 - 1j, 1 - 1j], [-1 + 1j, 1 - 1j]]) / 2
    )


def test_x_unitary():
    assert np.allclose(alphaclops.unitary(alphaclops.X), np.array([[0, 1], [1, 0]]))

    assert np.allclose(
        alphaclops.unitary(alphaclops.X ** 0.5), np.array([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]]) / 2
    )

    assert np.allclose(alphaclops.unitary(alphaclops.X ** 0), np.array([[1, 0], [0, 1]]))

    assert np.allclose(
        alphaclops.unitary(alphaclops.X ** -0.5), np.array([[1 - 1j, 1 + 1j], [1 + 1j, 1 - 1j]]) / 2
    )


def test_h_unitary():
    sqrt = alphaclops.unitary(alphaclops.H ** 0.5)
    m = np.dot(sqrt, sqrt)
    assert np.allclose(m, alphaclops.unitary(alphaclops.H), atol=1e-8)


def test_h_init():
    h = alphaclops.HPowGate(exponent=0.5)
    assert h.exponent == 0.5


def test_h_str():
    assert str(alphaclops.H) == 'H'
    assert str(alphaclops.H ** 0.5) == 'H**0.5'


def test_x_act_on_tableau():
    with pytest.raises(TypeError, match="Failed to act"):
        alphaclops.act_on(alphaclops.X, DummySimulationState(), qubits=())
    original_tableau = alphaclops.CliffordTableau(num_qubits=5, initial_state=31)
    flipped_tableau = alphaclops.CliffordTableau(num_qubits=5, initial_state=23)

    state = alphaclops.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=alphaclops.LineQubit.range(5),
        prng=np.random.RandomState(),
    )

    alphaclops.act_on(alphaclops.X ** 0.5, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.X ** 0.5, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    alphaclops.act_on(alphaclops.X, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    alphaclops.act_on(alphaclops.X ** 3.5, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.X ** 3.5, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    alphaclops.act_on(alphaclops.X ** 2, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    foo = sympy.Symbol('foo')
    with pytest.raises(TypeError, match="Failed to act action on state"):
        alphaclops.act_on(alphaclops.X ** foo, state, [alphaclops.LineQubit(1)])


class iZGate(alphaclops.testing.SingleQubitGate):
    """Equivalent to an iZ gate without _act_on_ defined on it."""

    def _unitary_(self):
        return np.array([[1j, 0], [0, -1j]])


class MinusOnePhaseGate(alphaclops.testing.SingleQubitGate):
    """Equivalent to a -1 global phase without _act_on_ defined on it."""

    def _unitary_(self):
        return np.array([[-1, 0], [0, -1]])


def test_y_act_on_tableau():
    with pytest.raises(TypeError, match="Failed to act"):
        alphaclops.act_on(alphaclops.Y, DummySimulationState(), qubits=())
    original_tableau = alphaclops.CliffordTableau(num_qubits=5, initial_state=31)
    flipped_tableau = alphaclops.CliffordTableau(num_qubits=5, initial_state=23)

    state = alphaclops.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=alphaclops.LineQubit.range(5),
        prng=np.random.RandomState(),
    )

    alphaclops.act_on(alphaclops.Y ** 0.5, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.Y ** 0.5, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(iZGate(), state, [alphaclops.LineQubit(1)])
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    alphaclops.act_on(alphaclops.Y, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(iZGate(), state, [alphaclops.LineQubit(1)], allow_decompose=True)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    alphaclops.act_on(alphaclops.Y ** 3.5, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.Y ** 3.5, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(iZGate(), state, [alphaclops.LineQubit(1)])
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    alphaclops.act_on(alphaclops.Y ** 2, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    foo = sympy.Symbol('foo')
    with pytest.raises(TypeError, match="Failed to act action on state"):
        alphaclops.act_on(alphaclops.Y ** foo, state, [alphaclops.LineQubit(1)])


def test_z_h_act_on_tableau():
    with pytest.raises(TypeError, match="Failed to act"):
        alphaclops.act_on(alphaclops.Z, DummySimulationState(), qubits=())
    with pytest.raises(TypeError, match="Failed to act"):
        alphaclops.act_on(alphaclops.H, DummySimulationState(), qubits=())
    original_tableau = alphaclops.CliffordTableau(num_qubits=5, initial_state=31)
    flipped_tableau = alphaclops.CliffordTableau(num_qubits=5, initial_state=23)

    state = alphaclops.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=alphaclops.LineQubit.range(5),
        prng=np.random.RandomState(),
    )

    alphaclops.act_on(alphaclops.H, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.Z ** 0.5, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.Z ** 0.5, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.H, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    alphaclops.act_on(alphaclops.H, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.Z, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.H, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    alphaclops.act_on(alphaclops.H, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.Z ** 3.5, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.Z ** 3.5, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.H, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    alphaclops.act_on(alphaclops.Z ** 2, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    alphaclops.act_on(alphaclops.H ** 2, state, [alphaclops.LineQubit(1)], allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == flipped_tableau

    foo = sympy.Symbol('foo')
    with pytest.raises(TypeError, match="Failed to act action on state"):
        alphaclops.act_on(alphaclops.Z ** foo, state, [alphaclops.LineQubit(1)])

    with pytest.raises(TypeError, match="Failed to act action on state"):
        alphaclops.act_on(alphaclops.H ** foo, state, [alphaclops.LineQubit(1)])

    with pytest.raises(TypeError, match="Failed to act action on state"):
        alphaclops.act_on(alphaclops.H ** 1.5, state, [alphaclops.LineQubit(1)])


def test_cx_act_on_tableau():
    with pytest.raises(TypeError, match="Failed to act"):
        alphaclops.act_on(alphaclops.CX, DummySimulationState(), qubits=())
    original_tableau = alphaclops.CliffordTableau(num_qubits=5, initial_state=31)

    state = alphaclops.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=alphaclops.LineQubit.range(5),
        prng=np.random.RandomState(),
    )

    alphaclops.act_on(alphaclops.CX, state, alphaclops.LineQubit.range(2), allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau.stabilizers() == [
        alphaclops.DensePauliString('ZIIII', coefficient=-1),
        alphaclops.DensePauliString('ZZIII', coefficient=-1),
        alphaclops.DensePauliString('IIZII', coefficient=-1),
        alphaclops.DensePauliString('IIIZI', coefficient=-1),
        alphaclops.DensePauliString('IIIIZ', coefficient=-1),
    ]
    assert state.tableau.destabilizers() == [
        alphaclops.DensePauliString('XXIII', coefficient=1),
        alphaclops.DensePauliString('IXIII', coefficient=1),
        alphaclops.DensePauliString('IIXII', coefficient=1),
        alphaclops.DensePauliString('IIIXI', coefficient=1),
        alphaclops.DensePauliString('IIIIX', coefficient=1),
    ]

    alphaclops.act_on(alphaclops.CX, state, alphaclops.LineQubit.range(2), allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    alphaclops.act_on(alphaclops.CX ** 4, state, alphaclops.LineQubit.range(2), allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    foo = sympy.Symbol('foo')
    with pytest.raises(TypeError, match="Failed to act action on state"):
        alphaclops.act_on(alphaclops.CX ** foo, state, alphaclops.LineQubit.range(2))

    with pytest.raises(TypeError, match="Failed to act action on state"):
        alphaclops.act_on(alphaclops.CX ** 1.5, state, alphaclops.LineQubit.range(2))


def test_cz_act_on_tableau():
    with pytest.raises(TypeError, match="Failed to act"):
        alphaclops.act_on(alphaclops.CZ, DummySimulationState(), qubits=())
    original_tableau = alphaclops.CliffordTableau(num_qubits=5, initial_state=31)

    state = alphaclops.CliffordTableauSimulationState(
        tableau=original_tableau.copy(),
        qubits=alphaclops.LineQubit.range(5),
        prng=np.random.RandomState(),
    )

    alphaclops.act_on(alphaclops.CZ, state, alphaclops.LineQubit.range(2), allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau.stabilizers() == [
        alphaclops.DensePauliString('ZIIII', coefficient=-1),
        alphaclops.DensePauliString('IZIII', coefficient=-1),
        alphaclops.DensePauliString('IIZII', coefficient=-1),
        alphaclops.DensePauliString('IIIZI', coefficient=-1),
        alphaclops.DensePauliString('IIIIZ', coefficient=-1),
    ]
    assert state.tableau.destabilizers() == [
        alphaclops.DensePauliString('XZIII', coefficient=1),
        alphaclops.DensePauliString('ZXIII', coefficient=1),
        alphaclops.DensePauliString('IIXII', coefficient=1),
        alphaclops.DensePauliString('IIIXI', coefficient=1),
        alphaclops.DensePauliString('IIIIX', coefficient=1),
    ]

    alphaclops.act_on(alphaclops.CZ, state, alphaclops.LineQubit.range(2), allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    alphaclops.act_on(alphaclops.CZ ** 4, state, alphaclops.LineQubit.range(2), allow_decompose=False)
    assert state.log_of_measurement_results == {}
    assert state.tableau == original_tableau

    foo = sympy.Symbol('foo')
    with pytest.raises(TypeError, match="Failed to act action on state"):
        alphaclops.act_on(alphaclops.CZ ** foo, state, alphaclops.LineQubit.range(2))

    with pytest.raises(TypeError, match="Failed to act action on state"):
        alphaclops.act_on(alphaclops.CZ ** 1.5, state, alphaclops.LineQubit.range(2))


def test_cz_act_on_equivalent_to_h_cx_h_tableau():
    state1 = alphaclops.CliffordTableauSimulationState(
        tableau=alphaclops.CliffordTableau(num_qubits=2),
        qubits=alphaclops.LineQubit.range(2),
        prng=np.random.RandomState(),
    )
    state2 = alphaclops.CliffordTableauSimulationState(
        tableau=alphaclops.CliffordTableau(num_qubits=2),
        qubits=alphaclops.LineQubit.range(2),
        prng=np.random.RandomState(),
    )
    alphaclops.act_on(alphaclops.S, sim_state=state1, qubits=[alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.S, sim_state=state2, qubits=[alphaclops.LineQubit(1)], allow_decompose=False)

    # state1 uses H*CNOT*H
    alphaclops.act_on(alphaclops.H, sim_state=state1, qubits=[alphaclops.LineQubit(1)], allow_decompose=False)
    alphaclops.act_on(alphaclops.CNOT, sim_state=state1, qubits=alphaclops.LineQubit.range(2), allow_decompose=False)
    alphaclops.act_on(alphaclops.H, sim_state=state1, qubits=[alphaclops.LineQubit(1)], allow_decompose=False)
    # state2 uses CZ
    alphaclops.act_on(alphaclops.CZ, sim_state=state2, qubits=alphaclops.LineQubit.range(2), allow_decompose=False)

    assert state1.tableau == state2.tableau


foo = sympy.Symbol('foo')


@pytest.mark.parametrize(
    'input_gate_sequence, outcome',
    [
        ([alphaclops.X ** foo], 'Error'),
        ([alphaclops.X ** 0.25], 'Error'),
        ([alphaclops.X ** 4], 'Original'),
        ([alphaclops.X ** 0.5, alphaclops.X ** 0.5], 'Flipped'),
        ([alphaclops.X], 'Flipped'),
        ([alphaclops.X ** 3.5, alphaclops.X ** 3.5], 'Flipped'),
        ([alphaclops.Y ** foo], 'Error'),
        ([alphaclops.Y ** 0.25], 'Error'),
        ([alphaclops.Y ** 4], 'Original'),
        ([alphaclops.Y ** 0.5, alphaclops.Y ** 0.5, iZGate()], 'Flipped'),
        ([alphaclops.Y, iZGate()], 'Flipped'),
        ([alphaclops.Y ** 3.5, alphaclops.Y ** 3.5, iZGate()], 'Flipped'),
        ([alphaclops.Z ** foo], 'Error'),
        ([alphaclops.H ** foo], 'Error'),
        ([alphaclops.H ** 1.5], 'Error'),
        ([alphaclops.Z ** 4], 'Original'),
        ([alphaclops.H ** 4], 'Original'),
        ([alphaclops.H, alphaclops.S, alphaclops.S, alphaclops.H], 'Flipped'),
        ([alphaclops.H, alphaclops.Z, alphaclops.H], 'Flipped'),
        ([alphaclops.H, alphaclops.Z ** 3.5, alphaclops.Z ** 3.5, alphaclops.H], 'Flipped'),
        ([alphaclops.CX ** foo], 'Error'),
        ([alphaclops.CX ** 1.5], 'Error'),
        ([alphaclops.CX ** 4], 'Original'),
        ([alphaclops.CX], 'Flipped'),
        ([alphaclops.CZ ** foo], 'Error'),
        ([alphaclops.CZ ** 1.5], 'Error'),
        ([alphaclops.CZ ** 4], 'Original'),
        ([alphaclops.CZ, MinusOnePhaseGate()], 'Original'),
    ],
)
def test_act_on_ch_form(input_gate_sequence, outcome):
    original_state = alphaclops.StabilizerStateChForm(num_qubits=5, initial_state=31)
    num_qubits = alphaclops.num_qubits(input_gate_sequence[0])
    if num_qubits == 1:
        qubits = [alphaclops.LineQubit(1)]
    else:
        assert num_qubits == 2
        qubits = alphaclops.LineQubit.range(2)
    state = alphaclops.StabilizerChFormSimulationState(
        qubits=alphaclops.LineQubit.range(2),
        prng=np.random.RandomState(),
        initial_state=original_state.copy(),
    )

    flipped_state = alphaclops.StabilizerStateChForm(num_qubits=5, initial_state=23)

    if outcome == 'Error':
        with pytest.raises(TypeError, match="Failed to act action on state"):
            for input_gate in input_gate_sequence:
                alphaclops.act_on(input_gate, state, qubits)
        return

    for input_gate in input_gate_sequence:
        alphaclops.act_on(input_gate, state, qubits)

    if outcome == 'Original':
        np.testing.assert_allclose(state.state.state_vector(), original_state.state_vector())

    if outcome == 'Flipped':
        np.testing.assert_allclose(state.state.state_vector(), flipped_state.state_vector())


@pytest.mark.parametrize(
    'input_gate, assert_implemented',
    [
        (alphaclops.X, True),
        (alphaclops.Y, True),
        (alphaclops.Z, True),
        (alphaclops.X ** 0.5, True),
        (alphaclops.Y ** 0.5, True),
        (alphaclops.Z ** 0.5, True),
        (alphaclops.X ** 3.5, True),
        (alphaclops.Y ** 3.5, True),
        (alphaclops.Z ** 3.5, True),
        (alphaclops.X ** 4, True),
        (alphaclops.Y ** 4, True),
        (alphaclops.Z ** 4, True),
        (alphaclops.H, True),
        (alphaclops.CX, True),
        (alphaclops.CZ, True),
        (alphaclops.H ** 4, True),
        (alphaclops.CX ** 4, True),
        (alphaclops.CZ ** 4, True),
        # Unsupported gates should not fail too.
        (alphaclops.X ** 0.25, False),
        (alphaclops.Y ** 0.25, False),
        (alphaclops.Z ** 0.25, False),
        (alphaclops.H ** 0.5, False),
        (alphaclops.CX ** 0.5, False),
        (alphaclops.CZ ** 0.5, False),
    ],
)
def test_act_on_consistency(input_gate, assert_implemented):
    alphaclops.testing.assert_all_implemented_act_on_effects_match_unitary(
        input_gate, assert_implemented, assert_implemented
    )


def test_runtime_types_of_rot_gates():
    for gate_type in [
        lambda p: alphaclops.CZPowGate(exponent=p),
        lambda p: alphaclops.XPowGate(exponent=p),
        lambda p: alphaclops.YPowGate(exponent=p),
        lambda p: alphaclops.ZPowGate(exponent=p),
    ]:
        p = gate_type(sympy.Symbol('a'))
        assert alphaclops.unitary(p, None) is None
        assert alphaclops.pow(p, 2, None) == gate_type(2 * sympy.Symbol('a'))
        assert alphaclops.inverse(p, None) == gate_type(-sympy.Symbol('a'))

        c = gate_type(0.5)
        assert alphaclops.unitary(c, None) is not None
        assert alphaclops.pow(c, 2) == gate_type(1)
        assert alphaclops.inverse(c) == gate_type(-0.5)


def test_interchangeable_qubit_eq():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')
    eq = alphaclops.testing.EqualsTester()

    eq.add_equality_group(alphaclops.CZ(a, b), alphaclops.CZ(b, a))
    eq.add_equality_group(alphaclops.CZ(a, c))

    eq.add_equality_group(alphaclops.CNOT(a, b))
    eq.add_equality_group(alphaclops.CNOT(b, a))
    eq.add_equality_group(alphaclops.CNOT(a, c))


def test_identity_multiplication():
    a, b, c = alphaclops.LineQubit.range(3)
    assert alphaclops.I(a) * alphaclops.CX(a, b) == alphaclops.CX(a, b)
    assert alphaclops.CX(a, b) * alphaclops.I(a) == alphaclops.CX(a, b)
    assert alphaclops.CZ(a, b) * alphaclops.I(c) == alphaclops.CZ(a, b)
    assert alphaclops.CX(a, b) ** 0.5 * alphaclops.I(c) == alphaclops.CX(a, b) ** 0.5
    assert alphaclops.I(c) * alphaclops.CZ(b, c) ** 0.5 == alphaclops.CZ(b, c) ** 0.5
    assert alphaclops.T(a) * alphaclops.I(a) == alphaclops.T(a)
    assert alphaclops.T(b) * alphaclops.I(c) == alphaclops.T(b)
    assert alphaclops.T(a) ** 0.25 * alphaclops.I(c) == alphaclops.T(a) ** 0.25
    assert alphaclops.I(c) * alphaclops.T(b) ** 0.25 == alphaclops.T(b) ** 0.25


def test_text_diagrams():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    circuit = alphaclops.Circuit(
        alphaclops.X(a),
        alphaclops.Y(a),
        alphaclops.Z(a),
        alphaclops.Z(a) ** sympy.Symbol('x'),
        alphaclops.rx(sympy.Symbol('x')).on(a),
        alphaclops.CZ(a, b),
        alphaclops.CNOT(a, b),
        alphaclops.CNOT(b, a),
        alphaclops.CNOT(a, b) ** 0.5,
        alphaclops.CNOT(b, a) ** 0.5,
        alphaclops.H(a) ** 0.5,
        alphaclops.I(a),
        alphaclops.IdentityGate(2)(a, b),
        alphaclops.cphase(sympy.pi * sympy.Symbol('t')).on(a, b),
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a: ───X───Y───Z───Z^x───Rx(x)───@───@───X───@───────X^0.5───H^0.5───I───I───@─────
                                │   │   │   │       │                   │   │
b: ─────────────────────────────@───X───@───X^0.5───@───────────────────I───@^t───
""",
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a: ---X---Y---Z---Z^x---Rx(x)---@---@---X---@-------X^0.5---H^0.5---I---I---@-----
                                |   |   |   |       |                   |   |
b: -----------------------------@---X---@---X^0.5---@-------------------I---@^t---
""",
        use_unicode_characters=False,
    )


def test_cnot_unitary():
    np.testing.assert_almost_equal(
        alphaclops.unitary(alphaclops.CNOT ** 0.5),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0.5 + 0.5j, 0.5 - 0.5j],
                [0, 0, 0.5 - 0.5j, 0.5 + 0.5j],
            ]
        ),
    )


def test_cnot_decompose():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    assert alphaclops.decompose_once(alphaclops.CNOT(a, b) ** sympy.Symbol('x')) is not None


def test_repr():
    assert repr(alphaclops.X) == 'alphaclops.X'
    assert repr(alphaclops.X ** 0.5) == '(alphaclops.X**0.5)'

    assert repr(alphaclops.Z) == 'alphaclops.Z'
    assert repr(alphaclops.Z ** 0.5) == 'alphaclops.S'
    assert repr(alphaclops.Z ** 0.25) == 'alphaclops.T'
    assert repr(alphaclops.Z ** 0.125) == '(alphaclops.Z**0.125)'

    assert repr(alphaclops.S) == 'alphaclops.S'
    assert repr(alphaclops.S ** -1) == '(alphaclops.S**-1)'
    assert repr(alphaclops.T) == 'alphaclops.T'
    assert repr(alphaclops.T ** -1) == '(alphaclops.T**-1)'

    assert repr(alphaclops.Y) == 'alphaclops.Y'
    assert repr(alphaclops.Y ** 0.5) == '(alphaclops.Y**0.5)'

    assert repr(alphaclops.CNOT) == 'alphaclops.CNOT'
    assert repr(alphaclops.CNOT ** 0.5) == '(alphaclops.CNOT**0.5)'

    alphaclops.testing.assert_equivalent_repr(
        alphaclops.X ** (sympy.Symbol('a') / 2 - sympy.Symbol('c') * 3 + 5)
    )
    alphaclops.testing.assert_equivalent_repr(alphaclops.Rx(rads=sympy.Symbol('theta')))
    alphaclops.testing.assert_equivalent_repr(alphaclops.Ry(rads=sympy.Symbol('theta')))
    alphaclops.testing.assert_equivalent_repr(alphaclops.Rz(rads=sympy.Symbol('theta')))

    # There should be no floating point error during initialization, and repr
    # should be using the "shortest decimal value closer to X than any other
    # floating point value" strategy, as opposed to the "exactly value in
    # decimal" strategy.
    assert repr(alphaclops.CZ ** 0.2) == '(alphaclops.CZ**0.2)'


def test_str():
    assert str(alphaclops.X) == 'X'
    assert str(alphaclops.X ** 0.5) == 'X**0.5'
    assert str(alphaclops.rx(np.pi)) == 'Rx(π)'
    assert str(alphaclops.rx(0.5 * np.pi)) == 'Rx(0.5π)'
    assert str(alphaclops.XPowGate(global_shift=-0.25)) == 'XPowGate(exponent=1.0, global_shift=-0.25)'

    assert str(alphaclops.Z) == 'Z'
    assert str(alphaclops.Z ** 0.5) == 'S'
    assert str(alphaclops.Z ** 0.125) == 'Z**0.125'
    assert str(alphaclops.rz(np.pi)) == 'Rz(π)'
    assert str(alphaclops.rz(1.4 * np.pi)) == 'Rz(1.4π)'
    assert str(alphaclops.ZPowGate(global_shift=0.25)) == 'ZPowGate(exponent=1.0, global_shift=0.25)'

    assert str(alphaclops.S) == 'S'
    assert str(alphaclops.S ** -1) == 'S**-1'
    assert str(alphaclops.T) == 'T'
    assert str(alphaclops.T ** -1) == 'T**-1'

    assert str(alphaclops.Y) == 'Y'
    assert str(alphaclops.Y ** 0.5) == 'Y**0.5'
    assert str(alphaclops.ry(np.pi)) == 'Ry(π)'
    assert str(alphaclops.ry(3.14 * np.pi)) == 'Ry(3.14π)'
    assert (
        str(alphaclops.YPowGate(exponent=2, global_shift=-0.25))
        == 'YPowGate(exponent=2, global_shift=-0.25)'
    )

    assert str(alphaclops.CX) == 'CNOT'
    assert str(alphaclops.CNOT ** 0.5) == 'CNOT**0.5'
    assert str(alphaclops.CZ) == 'CZ'
    assert str(alphaclops.CZ ** 0.5) == 'CZ**0.5'
    assert str(alphaclops.cphase(np.pi)) == 'CZ'
    assert str(alphaclops.cphase(np.pi / 2)) == 'CZ**0.5'


def test_rx_unitary():
    s = np.sqrt(0.5)
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.rx(np.pi / 2)), np.array([[s, -s * 1j], [-s * 1j, s]])
    )

    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.rx(-np.pi / 2)), np.array([[s, s * 1j], [s * 1j, s]])
    )

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.rx(0)), np.array([[1, 0], [0, 1]]))

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.rx(2 * np.pi)), np.array([[-1, 0], [0, -1]]))

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.rx(np.pi)), np.array([[0, -1j], [-1j, 0]]))

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.rx(-np.pi)), np.array([[0, 1j], [1j, 0]]))


def test_ry_unitary():
    s = np.sqrt(0.5)
    np.testing.assert_allclose(alphaclops.unitary(alphaclops.ry(np.pi / 2)), np.array([[s, -s], [s, s]]))

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.ry(-np.pi / 2)), np.array([[s, s], [-s, s]]))

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.ry(0)), np.array([[1, 0], [0, 1]]))

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.ry(2 * np.pi)), np.array([[-1, 0], [0, -1]]))

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.ry(np.pi)), np.array([[0, -1], [1, 0]]))

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.ry(-np.pi)), np.array([[0, 1], [-1, 0]]))


def test_rz_unitary():
    s = np.sqrt(0.5)
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.rz(np.pi / 2)), np.array([[s - s * 1j, 0], [0, s + s * 1j]])
    )

    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.rz(-np.pi / 2)), np.array([[s + s * 1j, 0], [0, s - s * 1j]])
    )

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.rz(0)), np.array([[1, 0], [0, 1]]))

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.rz(2 * np.pi)), np.array([[-1, 0], [0, -1]]))

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.rz(np.pi)), np.array([[-1j, 0], [0, 1j]]))

    np.testing.assert_allclose(alphaclops.unitary(alphaclops.rz(-np.pi)), np.array([[1j, 0], [0, -1j]]))


@pytest.mark.parametrize(
    'angle_rads, expected_unitary',
    [(0, np.eye(4)), (1, np.diag([1, 1, 1, np.exp(1j)])), (np.pi / 2, np.diag([1, 1, 1, 1j]))],
)
def test_cphase_unitary(angle_rads, expected_unitary):
    np.testing.assert_allclose(alphaclops.unitary(alphaclops.cphase(angle_rads)), expected_unitary)


def test_parameterized_cphase():
    assert alphaclops.cphase(sympy.pi) == alphaclops.CZ
    assert alphaclops.cphase(sympy.pi / 2) == alphaclops.CZ ** 0.5


@pytest.mark.parametrize('gate', [alphaclops.X, alphaclops.Y, alphaclops.Z])
def test_x_y_z_stabilizer(gate):
    assert alphaclops.has_stabilizer_effect(gate)
    assert alphaclops.has_stabilizer_effect(gate ** 0.5)
    assert alphaclops.has_stabilizer_effect(gate ** 0)
    assert alphaclops.has_stabilizer_effect(gate ** -0.5)
    assert alphaclops.has_stabilizer_effect(gate ** 4)
    assert not alphaclops.has_stabilizer_effect(gate ** 1.2)
    foo = sympy.Symbol('foo')
    assert not alphaclops.has_stabilizer_effect(gate ** foo)


def test_h_stabilizer():
    gate = alphaclops.H
    assert alphaclops.has_stabilizer_effect(gate)
    assert not alphaclops.has_stabilizer_effect(gate ** 0.5)
    assert alphaclops.has_stabilizer_effect(gate ** 0)
    assert not alphaclops.has_stabilizer_effect(gate ** -0.5)
    assert alphaclops.has_stabilizer_effect(gate ** 4)
    assert not alphaclops.has_stabilizer_effect(gate ** 1.2)
    foo = sympy.Symbol('foo')
    assert not alphaclops.has_stabilizer_effect(gate ** foo)


@pytest.mark.parametrize('gate', [alphaclops.CX, alphaclops.CZ])
def test_cx_cz_stabilizer(gate):
    assert alphaclops.has_stabilizer_effect(gate)
    assert not alphaclops.has_stabilizer_effect(gate ** 0.5)
    assert alphaclops.has_stabilizer_effect(gate ** 0)
    assert not alphaclops.has_stabilizer_effect(gate ** -0.5)
    assert alphaclops.has_stabilizer_effect(gate ** 4)
    assert not alphaclops.has_stabilizer_effect(gate ** 1.2)
    foo = sympy.Symbol('foo')
    assert not alphaclops.has_stabilizer_effect(gate ** foo)


def test_phase_by_xy():
    assert alphaclops.phase_by(alphaclops.X, 0.25, 0) == alphaclops.Y
    assert alphaclops.phase_by(alphaclops.X ** 0.5, 0.25, 0) == alphaclops.Y ** 0.5
    assert alphaclops.phase_by(alphaclops.X ** -0.5, 0.25, 0) == alphaclops.Y ** -0.5


def test_ixyz_circuit_diagram():
    q = alphaclops.NamedQubit('q')
    ix = alphaclops.XPowGate(exponent=1, global_shift=0.5)
    iy = alphaclops.YPowGate(exponent=1, global_shift=0.5)
    iz = alphaclops.ZPowGate(exponent=1, global_shift=0.5)

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            ix(q),
            ix(q) ** -1,
            ix(q) ** -0.99999,
            ix(q) ** -1.00001,
            ix(q) ** 3,
            ix(q) ** 4.5,
            ix(q) ** 4.500001,
        ),
        """
q: ───X───X───X───X───X───X^0.5───X^0.5───
        """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(iy(q), iy(q) ** -1, iy(q) ** 3, iy(q) ** 4.5, iy(q) ** 4.500001),
        """
q: ───Y───Y───Y───Y^0.5───Y^0.5───
    """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(iz(q), iz(q) ** -1, iz(q) ** 3, iz(q) ** 4.5, iz(q) ** 4.500001),
        """
q: ───Z───Z───Z───S───S───
    """,
    )


@pytest.mark.parametrize(
    'theta,exp',
    [
        (sympy.Symbol("theta"), 1 / 2),
        (np.pi / 2, 1 / 2),
        (np.pi / 2, sympy.Symbol("exp")),
        (sympy.Symbol("theta"), sympy.Symbol("exp")),
    ],
)
def test_rxyz_exponent(theta, exp):
    def resolve(gate):
        return alphaclops.resolve_parameters(gate, {'theta': np.pi / 4}, {'exp': 1 / 4})

    assert resolve(alphaclops.Rx(rads=theta) ** exp) == resolve(alphaclops.Rx(rads=theta * exp))
    assert resolve(alphaclops.Ry(rads=theta) ** exp) == resolve(alphaclops.Ry(rads=theta * exp))
    assert resolve(alphaclops.Rz(rads=theta) ** exp) == resolve(alphaclops.Rz(rads=theta * exp))


def test_rxyz_circuit_diagram():
    q = alphaclops.NamedQubit('q')

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            alphaclops.rx(np.pi).on(q),
            alphaclops.rx(-np.pi).on(q),
            alphaclops.rx(-np.pi + 0.00001).on(q),
            alphaclops.rx(-np.pi - 0.00001).on(q),
            alphaclops.rx(3 * np.pi).on(q),
            alphaclops.rx(7 * np.pi / 2).on(q),
            alphaclops.rx(9 * np.pi / 2 + 0.00001).on(q),
        ),
        """
q: ───Rx(π)───Rx(-π)───Rx(-π)───Rx(-π)───Rx(-π)───Rx(-0.5π)───Rx(0.5π)───
    """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            alphaclops.rx(np.pi).on(q),
            alphaclops.rx(np.pi / 2).on(q),
            alphaclops.rx(-np.pi + 0.00001).on(q),
            alphaclops.rx(-np.pi - 0.00001).on(q),
        ),
        """
q: ---Rx(pi)---Rx(0.5pi)---Rx(-pi)---Rx(-pi)---
        """,
        use_unicode_characters=False,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            alphaclops.ry(np.pi).on(q),
            alphaclops.ry(-np.pi).on(q),
            alphaclops.ry(3 * np.pi).on(q),
            alphaclops.ry(9 * np.pi / 2).on(q),
        ),
        """
q: ───Ry(π)───Ry(-π)───Ry(-π)───Ry(0.5π)───
    """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            alphaclops.rz(np.pi).on(q),
            alphaclops.rz(-np.pi).on(q),
            alphaclops.rz(3 * np.pi).on(q),
            alphaclops.rz(9 * np.pi / 2).on(q),
            alphaclops.rz(9 * np.pi / 2 + 0.00001).on(q),
        ),
        """
q: ───Rz(π)───Rz(-π)───Rz(-π)───Rz(0.5π)───Rz(0.5π)───
    """,
    )


def test_trace_distance():
    foo = sympy.Symbol('foo')
    sx = alphaclops.X ** foo
    sy = alphaclops.Y ** foo
    sz = alphaclops.Z ** foo
    sh = alphaclops.H ** foo
    scx = alphaclops.CX ** foo
    scz = alphaclops.CZ ** foo
    # These values should have 1.0 or 0.0 directly returned
    assert alphaclops.trace_distance_bound(sx) == 1.0
    assert alphaclops.trace_distance_bound(sy) == 1.0
    assert alphaclops.trace_distance_bound(sz) == 1.0
    assert alphaclops.trace_distance_bound(scx) == 1.0
    assert alphaclops.trace_distance_bound(scz) == 1.0
    assert alphaclops.trace_distance_bound(sh) == 1.0
    assert alphaclops.trace_distance_bound(alphaclops.I) == 0.0
    # These values are calculated, so we use approx_eq
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(alphaclops.X), 1.0)
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(alphaclops.Y ** -1), 1.0)
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(alphaclops.Z ** 0.5), np.sin(np.pi / 4))
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(alphaclops.H ** 0.25), np.sin(np.pi / 8))
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(alphaclops.CX ** 2), 0.0)
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(alphaclops.CZ ** (1 / 9)), np.sin(np.pi / 18))


def test_commutes():
    assert alphaclops.commutes(alphaclops.ZPowGate(exponent=sympy.Symbol('t')), alphaclops.Z)
    assert alphaclops.commutes(alphaclops.Z, alphaclops.Z(alphaclops.LineQubit(0)), default=None) is None
    assert alphaclops.commutes(alphaclops.Z ** 0.1, alphaclops.XPowGate(exponent=0))


def test_approx_eq():
    assert alphaclops.approx_eq(alphaclops.Z ** 0.1, alphaclops.Z ** 0.2, atol=0.3)
    assert not alphaclops.approx_eq(alphaclops.Z ** 0.1, alphaclops.Z ** 0.2, atol=0.05)
    assert alphaclops.approx_eq(alphaclops.Y ** 0.1, alphaclops.Y ** 0.2, atol=0.3)
    assert not alphaclops.approx_eq(alphaclops.Y ** 0.1, alphaclops.Y ** 0.2, atol=0.05)
    assert alphaclops.approx_eq(alphaclops.X ** 0.1, alphaclops.X ** 0.2, atol=0.3)
    assert not alphaclops.approx_eq(alphaclops.X ** 0.1, alphaclops.X ** 0.2, atol=0.05)


def test_xpow_dim_3():
    x = alphaclops.XPowGate(dimension=3)
    assert alphaclops.X != x
    # fmt: off
    expected = [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ]
    # fmt: on
    assert np.allclose(alphaclops.unitary(x), expected)

    sim = alphaclops.Simulator()
    circuit = alphaclops.Circuit([x(alphaclops.LineQid(0, 3)) ** 0.5] * 6)
    svs = [step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit)]
    # fmt: off
    expected = [
        [0.67, 0.67, 0.33],
        [0.0, 1.0, 0.0],
        [0.33, 0.67, 0.67],
        [0.0, 0.0, 1.0],
        [0.67, 0.33, 0.67],
        [1.0, 0.0, 0.0],
    ]
    # fmt: on
    assert np.allclose(np.abs(svs), expected, atol=1e-2)


def test_xpow_dim_4():
    x = alphaclops.XPowGate(dimension=4)
    assert alphaclops.X != x
    # fmt: off
    expected = [
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
    ]
    # fmt: on
    assert np.allclose(alphaclops.unitary(x), expected)

    sim = alphaclops.Simulator()
    circuit = alphaclops.Circuit([x(alphaclops.LineQid(0, 4)) ** 0.5] * 8)
    svs = [step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit)]
    # fmt: off
    expected = [
        [0.65, 0.65, 0.27, 0.27],
        [0.0, 1.0, 0.0, 0.0],
        [0.27, 0.65, 0.65, 0.27],
        [0.0, 0.0, 1.0, 0.0],
        [0.27, 0.27, 0.65, 0.65],
        [0.0, 0.0, 0.0, 1.0],
        [0.65, 0.27, 0.27, 0.65],
        [1.0, 0.0, 0.0, 0.0],
    ]
    # fmt: on
    assert np.allclose(np.abs(svs), expected, atol=1e-2)


def test_zpow_dim_3():
    L = np.exp(2 * np.pi * 1j / 3)
    L2 = L**2
    z = alphaclops.ZPowGate(dimension=3)
    assert alphaclops.Z != z
    # fmt: off
    expected = [
        [1, 0, 0],
        [0, L, 0],
        [0, 0, L2],
    ]
    # fmt: on
    assert np.allclose(alphaclops.unitary(z), expected)

    sim = alphaclops.Simulator()
    circuit = alphaclops.Circuit([z(alphaclops.LineQid(0, 3)) ** 0.5] * 6)
    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=0)
    ]
    expected = [[1, 0, 0]] * 6
    assert np.allclose((svs), expected)

    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=1)
    ]
    # fmt: off
    expected = [
        [0, L**0.5, 0],
        [0, L**1.0, 0],
        [0, L**1.5, 0],
        [0, L**2.0, 0],
        [0, L**2.5, 0],
        [0, 1, 0],
    ]
    # fmt: on
    assert np.allclose((svs), expected)

    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=2)
    ]
    # fmt: off
    expected = [
        [0, 0, L],
        [0, 0, L2],
        [0, 0, 1],
        [0, 0, L],
        [0, 0, L2],
        [0, 0, 1],
    ]
    # fmt: on
    assert np.allclose((svs), expected)


def test_zpow_dim_4():
    z = alphaclops.ZPowGate(dimension=4)
    assert alphaclops.Z != z
    # fmt: off
    expected = [
        [1, 0, 0, 0],
        [0, 1j, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1j],
    ]
    # fmt: on
    assert np.allclose(alphaclops.unitary(z), expected)

    sim = alphaclops.Simulator()
    circuit = alphaclops.Circuit([z(alphaclops.LineQid(0, 4)) ** 0.5] * 8)
    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=0)
    ]
    expected = [[1, 0, 0, 0]] * 8
    assert np.allclose((svs), expected)

    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=1)
    ]
    # fmt: off
    expected = [
        [0, 1j**0.5, 0, 0],
        [0, 1j**1.0, 0, 0],
        [0, 1j**1.5, 0, 0],
        [0, 1j**2.0, 0, 0],
        [0, 1j**2.5, 0, 0],
        [0, 1j**3.0, 0, 0],
        [0, 1j**3.5, 0, 0],
        [0, 1, 0, 0],
    ]
    # fmt: on
    assert np.allclose(svs, expected)

    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=2)
    ]
    # fmt: off
    expected = [
        [0, 0, 1j, 0],
        [0, 0, -1, 0],
        [0, 0, -1j, 0],
        [0, 0, 1, 0],
        [0, 0, 1j, 0],
        [0, 0, -1, 0],
        [0, 0, -1j, 0],
        [0, 0, 1, 0],
    ]
    # fmt: on
    assert np.allclose(svs, expected)

    svs = [
        step.state_vector(copy=True) for step in sim.simulate_moment_steps(circuit, initial_state=3)
    ]
    # fmt: off
    expected = [
        [0, 0, 0, 1j**1.5],
        [0, 0, 0, 1j**3],
        [0, 0, 0, 1j**0.5],
        [0, 0, 0, 1j**2],
        [0, 0, 0, 1j**3.5],
        [0, 0, 0, 1j**1],
        [0, 0, 0, 1j**2.5],
        [0, 0, 0, 1],
    ]
    # fmt: on
    assert np.allclose(svs, expected)


def test_wrong_dims():
    x3 = alphaclops.XPowGate(dimension=3)
    with pytest.raises(ValueError, match='Wrong shape'):
        _ = x3.on(alphaclops.LineQubit(0))
    with pytest.raises(ValueError, match='Wrong shape'):
        _ = x3.on(alphaclops.LineQid(0, dimension=4))

    z3 = alphaclops.ZPowGate(dimension=3)
    with pytest.raises(ValueError, match='Wrong shape'):
        _ = z3.on(alphaclops.LineQubit(0))
    with pytest.raises(ValueError, match='Wrong shape'):
        _ = z3.on(alphaclops.LineQid(0, dimension=4))

    with pytest.raises(ValueError, match='Wrong shape'):
        _ = alphaclops.X.on(alphaclops.LineQid(0, dimension=3))

    with pytest.raises(ValueError, match='Wrong shape'):
        _ = alphaclops.Z.on(alphaclops.LineQid(0, dimension=3))
