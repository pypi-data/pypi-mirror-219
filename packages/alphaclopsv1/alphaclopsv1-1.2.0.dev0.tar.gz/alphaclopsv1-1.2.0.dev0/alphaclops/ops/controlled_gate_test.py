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

from typing import Union, Tuple, cast

import numpy as np
import pytest
import sympy

import alphaclops
from alphaclops.type_workarounds import NotImplementedType


class GateUsingWorkspaceForApplyUnitary(alphaclops.testing.SingleQubitGate):
    def _apply_unitary_(self, args: alphaclops.ApplyUnitaryArgs) -> Union[np.ndarray, NotImplementedType]:
        args.available_buffer[...] = args.target_tensor
        args.target_tensor[...] = 0
        return args.available_buffer

    def _unitary_(self):
        return np.eye(2)

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __repr__(self):
        return 'alphaclops.ops.controlled_gate_test.GateUsingWorkspaceForApplyUnitary()'


class GateAllocatingNewSpaceForResult(alphaclops.testing.SingleQubitGate):
    def __init__(self):
        self._matrix = alphaclops.testing.random_unitary(2, random_state=4321)

    def _apply_unitary_(self, args: alphaclops.ApplyUnitaryArgs) -> Union[np.ndarray, NotImplementedType]:
        assert len(args.axes) == 1
        a = args.axes[0]
        seed = cast(Tuple[Union[int, slice, 'ellipsis'], ...], (slice(None),))
        zero = seed * a + (0, Ellipsis)
        one = seed * a + (1, Ellipsis)
        result = np.zeros(args.target_tensor.shape, args.target_tensor.dtype)
        result[zero] = (
            args.target_tensor[zero] * self._matrix[0][0]
            + args.target_tensor[one] * self._matrix[0][1]
        )
        result[one] = (
            args.target_tensor[zero] * self._matrix[1][0]
            + args.target_tensor[one] * self._matrix[1][1]
        )
        return result

    def _unitary_(self):
        return self._matrix

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __repr__(self):
        return 'alphaclops.ops.controlled_gate_test.GateAllocatingNewSpaceForResult()'


class RestrictedGate(alphaclops.testing.SingleQubitGate):
    def _unitary_(self):
        return True

    def __str__(self):
        return 'Restricted'


q = alphaclops.NamedQubit('q')
p = alphaclops.NamedQubit('p')
q3 = q.with_dimension(3)
p3 = p.with_dimension(3)

CY = alphaclops.ControlledGate(alphaclops.Y)
CCH = alphaclops.ControlledGate(alphaclops.ControlledGate(alphaclops.H))
CRestricted = alphaclops.ControlledGate(RestrictedGate())

C0Y = alphaclops.ControlledGate(alphaclops.Y, control_values=[0])
C0C1H = alphaclops.ControlledGate(alphaclops.ControlledGate(alphaclops.H, control_values=[1]), control_values=[0])

nand_control_values = alphaclops.SumOfProducts([(0, 1), (1, 0), (1, 1)])
xor_control_values = alphaclops.SumOfProducts([[0, 1], [1, 0]], name="xor")
C_01_10_11H = alphaclops.ControlledGate(alphaclops.H, control_values=nand_control_values)
C_xorH = alphaclops.ControlledGate(alphaclops.H, control_values=xor_control_values)
C0C_xorH = alphaclops.ControlledGate(C_xorH, control_values=[0])

C0Restricted = alphaclops.ControlledGate(RestrictedGate(), control_values=[0])
C_xorRestricted = alphaclops.ControlledGate(RestrictedGate(), control_values=xor_control_values)

C2Y = alphaclops.ControlledGate(alphaclops.Y, control_values=[2], control_qid_shape=(3,))
C2C2H = alphaclops.ControlledGate(
    alphaclops.ControlledGate(alphaclops.H, control_values=[2], control_qid_shape=(3,)),
    control_values=[2],
    control_qid_shape=(3,),
)
C_02_20H = alphaclops.ControlledGate(
    alphaclops.H, control_values=alphaclops.SumOfProducts([[0, 2], [1, 0]]), control_qid_shape=(2, 3)
)
C2Restricted = alphaclops.ControlledGate(RestrictedGate(), control_values=[2], control_qid_shape=(3,))


def test_init():
    gate = alphaclops.ControlledGate(alphaclops.Z)
    assert gate.sub_gate is alphaclops.Z
    assert gate.num_qubits() == 2


def test_init2():
    with pytest.raises(ValueError, match=r'alphaclops\.num_qubits\(control_values\) != num_controls'):
        alphaclops.ControlledGate(alphaclops.Z, num_controls=1, control_values=(1, 0))
    with pytest.raises(ValueError, match=r'len\(control_qid_shape\) != num_controls'):
        alphaclops.ControlledGate(alphaclops.Z, num_controls=1, control_qid_shape=(2, 2))
    with pytest.raises(ValueError, match='Control values .*outside of range'):
        alphaclops.ControlledGate(alphaclops.Z, control_values=[2])
    with pytest.raises(ValueError, match='Control values .*outside of range'):
        alphaclops.ControlledGate(alphaclops.Z, control_values=[(1, -1)])
    with pytest.raises(ValueError, match='Control values .*outside of range'):
        alphaclops.ControlledGate(alphaclops.Z, control_values=[3], control_qid_shape=[3])
    with pytest.raises(ValueError, match='Cannot control measurement'):
        alphaclops.ControlledGate(alphaclops.MeasurementGate(1))
    with pytest.raises(ValueError, match='Cannot control channel'):
        alphaclops.ControlledGate(alphaclops.PhaseDampingChannel(1))

    gate = alphaclops.ControlledGate(alphaclops.Z, 1)
    assert gate.sub_gate is alphaclops.Z
    assert gate.num_controls() == 1
    assert gate.control_values == alphaclops.ProductOfSums(((1,),))
    assert gate.control_qid_shape == (2,)
    assert gate.num_qubits() == 2
    assert alphaclops.qid_shape(gate) == (2, 2)

    gate = alphaclops.ControlledGate(alphaclops.Z, 2)
    assert gate.sub_gate is alphaclops.Z
    assert gate.num_controls() == 2
    assert gate.control_values == alphaclops.ProductOfSums(((1,), (1,)))
    assert gate.control_qid_shape == (2, 2)
    assert gate.num_qubits() == 3
    assert alphaclops.qid_shape(gate) == (2, 2, 2)

    gate = alphaclops.ControlledGate(
        alphaclops.ControlledGate(alphaclops.ControlledGate(alphaclops.Z, 3), num_controls=2), 2
    )
    assert gate.sub_gate is alphaclops.Z
    assert gate.num_controls() == 7
    assert gate.control_values == alphaclops.ProductOfSums(((1,),) * 7)
    assert gate.control_qid_shape == (2,) * 7
    assert gate.num_qubits() == 8
    assert alphaclops.qid_shape(gate) == (2,) * 8
    op = gate(*alphaclops.LineQubit.range(8))
    assert op.qubits == (
        alphaclops.LineQubit(0),
        alphaclops.LineQubit(1),
        alphaclops.LineQubit(2),
        alphaclops.LineQubit(3),
        alphaclops.LineQubit(4),
        alphaclops.LineQubit(5),
        alphaclops.LineQubit(6),
        alphaclops.LineQubit(7),
    )

    gate = alphaclops.ControlledGate(alphaclops.Z, control_values=(0, (0, 1)))
    assert gate.sub_gate is alphaclops.Z
    assert gate.num_controls() == 2
    assert gate.control_values == alphaclops.ProductOfSums(((0,), (0, 1)))
    assert gate.control_qid_shape == (2, 2)
    assert gate.num_qubits() == 3
    assert alphaclops.qid_shape(gate) == (2, 2, 2)

    gate = alphaclops.ControlledGate(alphaclops.Z, control_qid_shape=(3, 3))
    assert gate.sub_gate is alphaclops.Z
    assert gate.num_controls() == 2
    assert gate.control_values == alphaclops.ProductOfSums(((1,), (1,)))
    assert gate.control_qid_shape == (3, 3)
    assert gate.num_qubits() == 3
    assert alphaclops.qid_shape(gate) == (3, 3, 2)


def test_validate_args():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')

    # Need a control qubit.
    with pytest.raises(ValueError):
        CRestricted.validate_args([])
    with pytest.raises(ValueError):
        CRestricted.validate_args([a])
    CRestricted.validate_args([a, b])

    # CY is a two-qubit operation (control + single-qubit sub gate).
    with pytest.raises(ValueError):
        CY.validate_args([a])
    with pytest.raises(ValueError):
        CY.validate_args([a, b, c])
    CY.validate_args([a, b])

    # Applies when creating operations.
    with pytest.raises(ValueError):
        _ = CY.on()
    with pytest.raises(ValueError):
        _ = CY.on(a)
    with pytest.raises(ValueError):
        _ = CY.on(a, b, c)
    _ = CY.on(a, b)

    # Applies when creating operations.
    with pytest.raises(ValueError):
        _ = CCH.on()
    with pytest.raises(ValueError):
        _ = CCH.on(a)
    with pytest.raises(ValueError):
        _ = CCH.on(a, b)

    # Applies when creating operations. Control qids have different dimensions.
    with pytest.raises(ValueError, match="Wrong shape of qids"):
        _ = CY.on(q3, b)
    with pytest.raises(ValueError, match="Wrong shape of qids"):
        _ = C2Y.on(a, b)
    with pytest.raises(ValueError, match="Wrong shape of qids"):
        _ = C2C2H.on(a, b, c)
    _ = C2C2H.on(q3, p3, a)


def test_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(CY, alphaclops.ControlledGate(alphaclops.Y))
    eq.add_equality_group(CCH)
    eq.add_equality_group(alphaclops.ControlledGate(alphaclops.H))
    eq.add_equality_group(alphaclops.ControlledGate(alphaclops.X))
    eq.add_equality_group(alphaclops.X)
    eq.add_equality_group(
        alphaclops.ControlledGate(alphaclops.H, control_values=[1, (0, 2)], control_qid_shape=[2, 3]),
        alphaclops.ControlledGate(alphaclops.H, control_values=(1, [0, 2]), control_qid_shape=(2, 3)),
        alphaclops.ControlledGate(
            alphaclops.H, control_values=alphaclops.SumOfProducts([[1, 0], [1, 2]]), control_qid_shape=(2, 3)
        ),
    )
    eq.add_equality_group(
        alphaclops.ControlledGate(alphaclops.H, control_values=[(2, 0), 1], control_qid_shape=[3, 2]),
        alphaclops.ControlledGate(
            alphaclops.H, control_values=alphaclops.SumOfProducts([[2, 1], [0, 1]]), control_qid_shape=(3, 2)
        ),
    )
    eq.add_equality_group(
        alphaclops.ControlledGate(alphaclops.H, control_values=[1, 0], control_qid_shape=[2, 3]),
        alphaclops.ControlledGate(alphaclops.H, control_values=(1, 0), control_qid_shape=(2, 3)),
    )
    eq.add_equality_group(
        alphaclops.ControlledGate(alphaclops.H, control_values=[0, 1], control_qid_shape=[3, 2])
    )
    eq.add_equality_group(
        alphaclops.ControlledGate(alphaclops.H, control_values=[1, 0]),
        alphaclops.ControlledGate(alphaclops.H, control_values=(1, 0)),
    )
    eq.add_equality_group(alphaclops.ControlledGate(alphaclops.H, control_values=[0, 1]))
    for group in eq._groups:
        if isinstance(group[0], alphaclops.Gate):
            for item in group:
                np.testing.assert_allclose(alphaclops.unitary(item), alphaclops.unitary(group[0]))


def test_control():
    class G(alphaclops.testing.SingleQubitGate):
        def _has_mixture_(self):
            return True

    g = G()

    # Ignores empty.
    assert g.controlled() == alphaclops.ControlledGate(g)

    # Combined.
    cg = g.controlled()
    assert isinstance(cg, alphaclops.ControlledGate)
    assert cg.sub_gate == g
    assert cg.num_controls() == 1

    # Equality ignores ordering but cares about set and quantity.
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(g)
    eq.add_equality_group(
        g.controlled(),
        g.controlled(control_values=[1]),
        g.controlled(control_qid_shape=(2,)),
        alphaclops.ControlledGate(g, num_controls=1),
        g.controlled(control_values=alphaclops.SumOfProducts([[1]])),
    )
    eq.add_equality_group(
        alphaclops.ControlledGate(g, num_controls=2),
        g.controlled(control_values=[1, 1]),
        g.controlled(control_qid_shape=[2, 2]),
        g.controlled(num_controls=2),
        g.controlled().controlled(),
        g.controlled(control_values=alphaclops.SumOfProducts([[1, 1]])),
    )
    eq.add_equality_group(
        alphaclops.ControlledGate(g, control_values=[0, 1]),
        g.controlled(control_values=[0, 1]),
        g.controlled(control_values=[1]).controlled(control_values=[0]),
        g.controlled(control_values=alphaclops.SumOfProducts([[1]])).controlled(control_values=[0]),
    )
    eq.add_equality_group(g.controlled(control_values=[0]).controlled(control_values=[1]))
    eq.add_equality_group(
        alphaclops.ControlledGate(g, control_qid_shape=[4, 3]),
        g.controlled(control_qid_shape=[4, 3]),
        g.controlled(control_qid_shape=[3]).controlled(control_qid_shape=[4]),
    )
    eq.add_equality_group(g.controlled(control_qid_shape=[4]).controlled(control_qid_shape=[3]))


def test_unitary():
    cxa = alphaclops.ControlledGate(alphaclops.X ** sympy.Symbol('a'))
    assert not alphaclops.has_unitary(cxa)
    assert alphaclops.unitary(cxa, None) is None

    assert alphaclops.has_unitary(CY)
    assert alphaclops.has_unitary(CCH)
    # fmt: off
    np.testing.assert_allclose(
        alphaclops.unitary(CY),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, -1j],
                [0, 0, 1j, 0],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        alphaclops.unitary(C0Y),
        np.array(
            [
                [0, -1j, 0, 0],
                [1j, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )
    # fmt: on
    np.testing.assert_allclose(
        alphaclops.unitary(CCH),
        np.array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, np.sqrt(0.5), np.sqrt(0.5)],
                [0, 0, 0, 0, 0, 0, np.sqrt(0.5), -np.sqrt(0.5)],
            ]
        ),
        atol=1e-8,
    )

    C_xorX = alphaclops.ControlledGate(alphaclops.X, control_values=xor_control_values)
    # fmt: off
    np.testing.assert_allclose(alphaclops.unitary(C_xorX), np.array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1]]
    ))
    # fmt: on


@pytest.mark.parametrize(
    'gate, should_decompose_to_target',
    [
        (alphaclops.X, True),
        (alphaclops.X ** 0.5, True),
        (alphaclops.rx(np.pi), True),
        (alphaclops.rx(np.pi / 2), True),
        (alphaclops.Z, True),
        (alphaclops.H, True),
        (alphaclops.CNOT, True),
        (alphaclops.SWAP, True),
        (alphaclops.CCZ, True),
        (alphaclops.ControlledGate(alphaclops.ControlledGate(alphaclops.CCZ)), True),
        (GateUsingWorkspaceForApplyUnitary(), True),
        (GateAllocatingNewSpaceForResult(), True),
        (alphaclops.IdentityGate(qid_shape=(3, 4)), True),
        (
                alphaclops.ControlledGate(
                alphaclops.XXPowGate(exponent=0.25, global_shift=-0.5),
                num_controls=2,
                control_values=(1, (1, 0)),
            ),
                True,
        ),
        # Single qudit gate with dimension 4.
        (alphaclops.MatrixGate(np.kron(*(alphaclops.unitary(alphaclops.H),) * 2), qid_shape=(4,)), False),
        (alphaclops.MatrixGate(alphaclops.testing.random_unitary(4, random_state=1234)), False),
        (alphaclops.XX ** sympy.Symbol("s"), True),
        (alphaclops.CZ ** sympy.Symbol("s"), True),
        # Non-trivial `alphaclops.ProductOfSum` controls.
        (C_01_10_11H, False),
        (C_xorH, False),
        (C0C_xorH, False),
    ],
)
def test_controlled_gate_is_consistent(gate: alphaclops.Gate, should_decompose_to_target):
    cgate = alphaclops.ControlledGate(gate)
    alphaclops.testing.assert_implements_consistent_protocols(cgate)
    alphaclops.testing.assert_decompose_ends_at_default_gateset(
        cgate, ignore_known_gates=not should_decompose_to_target
    )


def test_pow_inverse():
    assert alphaclops.inverse(CRestricted, None) is None
    assert alphaclops.pow(CRestricted, 1.5, None) is None
    assert alphaclops.pow(CY, 1.5) == alphaclops.ControlledGate(alphaclops.Y ** 1.5)
    assert alphaclops.inverse(CY) == CY ** -1 == CY

    assert alphaclops.inverse(C0Restricted, None) is None
    assert alphaclops.pow(C0Restricted, 1.5, None) is None
    assert alphaclops.pow(C0Y, 1.5) == alphaclops.ControlledGate(alphaclops.Y ** 1.5, control_values=[0])
    assert alphaclops.inverse(C0Y) == C0Y ** -1 == C0Y

    assert alphaclops.inverse(C2Restricted, None) is None
    assert alphaclops.pow(C2Restricted, 1.5, None) is None
    assert alphaclops.pow(C2Y, 1.5) == alphaclops.ControlledGate(
        alphaclops.Y ** 1.5, control_values=[2], control_qid_shape=(3,)
    )
    assert alphaclops.inverse(C2Y) == C2Y ** -1 == C2Y


def test_extrapolatable_effect():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    assert alphaclops.ControlledGate(alphaclops.Z) ** 0.5 == alphaclops.ControlledGate(alphaclops.Z ** 0.5)

    assert alphaclops.ControlledGate(alphaclops.Z).on(a, b) ** 0.5 == alphaclops.ControlledGate(alphaclops.Z ** 0.5).on(
        a, b
    )

    assert alphaclops.ControlledGate(alphaclops.Z) ** 0.5 == alphaclops.ControlledGate(alphaclops.Z ** 0.5)


def test_reversible():
    assert alphaclops.inverse(alphaclops.ControlledGate(alphaclops.S)) == alphaclops.ControlledGate(alphaclops.S ** -1)
    assert alphaclops.inverse(alphaclops.ControlledGate(alphaclops.S, num_controls=4)) == alphaclops.ControlledGate(
        alphaclops.S ** -1, num_controls=4
    )
    assert alphaclops.inverse(alphaclops.ControlledGate(alphaclops.S, control_values=[1])) == alphaclops.ControlledGate(
        alphaclops.S ** -1, control_values=[1]
    )
    assert alphaclops.inverse(alphaclops.ControlledGate(alphaclops.S, control_qid_shape=(3,))) == alphaclops.ControlledGate(
        alphaclops.S ** -1, control_qid_shape=(3,)
    )


class UnphaseableGate(alphaclops.Gate):
    pass


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_parameterizable(resolve_fn):
    a = sympy.Symbol('a')
    cy = alphaclops.ControlledGate(alphaclops.Y)
    cya = alphaclops.ControlledGate(alphaclops.YPowGate(exponent=a))
    assert alphaclops.is_parameterized(cya)
    assert not alphaclops.is_parameterized(cy)
    assert resolve_fn(cya, alphaclops.ParamResolver({'a': 1})) == cy

    cchan = alphaclops.ControlledGate(
        alphaclops.RandomGateChannel(sub_gate=alphaclops.PhaseDampingChannel(0.1), probability=a)
    )
    with pytest.raises(ValueError, match='Cannot control channel'):
        resolve_fn(cchan, alphaclops.ParamResolver({'a': 0.1}))


def test_circuit_diagram_info():
    assert alphaclops.circuit_diagram_info(CY) == alphaclops.CircuitDiagramInfo(
        wire_symbols=('@', 'Y'), exponent=1
    )

    assert alphaclops.circuit_diagram_info(C0Y) == alphaclops.CircuitDiagramInfo(
        wire_symbols=('(0)', 'Y'), exponent=1
    )

    assert alphaclops.circuit_diagram_info(C2Y) == alphaclops.CircuitDiagramInfo(
        wire_symbols=('(2)', 'Y'), exponent=1
    )

    assert alphaclops.circuit_diagram_info(alphaclops.ControlledGate(alphaclops.Y ** 0.5)) == alphaclops.CircuitDiagramInfo(
        wire_symbols=('@', 'Y'), exponent=0.5
    )

    assert alphaclops.circuit_diagram_info(alphaclops.ControlledGate(alphaclops.S)) == alphaclops.CircuitDiagramInfo(
        wire_symbols=('@', 'S'), exponent=1
    )

    class UndiagrammableGate(alphaclops.testing.SingleQubitGate):
        def _has_unitary_(self):
            return True

    assert (
            alphaclops.circuit_diagram_info(alphaclops.ControlledGate(UndiagrammableGate()), default=None) is None
    )


# A contrived multiqubit Hadamard gate that asserts the consistency of
# the passed in Args and puts an H on all qubits
# displays them as 'H(qubit)' on the wire
class MultiH(alphaclops.Gate):
    def num_qubits(self) -> int:
        return self._num_qubits

    def __init__(self, num_qubits):
        self._num_qubits = num_qubits

    def _circuit_diagram_info_(self, args: alphaclops.CircuitDiagramInfoArgs) -> alphaclops.CircuitDiagramInfo:
        assert args.known_qubit_count is not None
        assert args.known_qubits is not None

        return alphaclops.CircuitDiagramInfo(
            wire_symbols=tuple(f'H({q})' for q in args.known_qubits), connected=True
        )

    def _has_unitary_(self):
        return True


def test_circuit_diagram_product_of_sums():
    qubits = alphaclops.LineQubit.range(3)
    c = alphaclops.Circuit()
    c.append(alphaclops.ControlledGate(MultiH(2))(*qubits))

    alphaclops.testing.assert_has_diagram(
        c,
        """
0: ───@─────────
      │
1: ───H(q(1))───
      │
2: ───H(q(2))───
""",
    )

    qubits = alphaclops.LineQid.for_qid_shape((3, 3, 3, 2))
    c = alphaclops.Circuit(
        MultiH(1)(*qubits[3:]).controlled_by(*qubits[:3], control_values=[1, (0, 1), (2, 0)])
    )

    alphaclops.testing.assert_has_diagram(
        c,
        """
0 (d=3): ───@───────────────
            │
1 (d=3): ───(0,1)───────────
            │
2 (d=3): ───(0,2)───────────
            │
3 (d=2): ───H(q(3) (d=2))───
""",
    )


def test_circuit_diagram_sum_of_products():
    q = alphaclops.LineQubit.range(4)
    c = alphaclops.Circuit(C_xorH.on(*q[:3]), C_01_10_11H.on(*q[:3]), C0C_xorH.on(*q))
    alphaclops.testing.assert_has_diagram(
        c,
        """
0: ───@────────@(011)───@(00)───
      │        │        │
1: ───@(xor)───@(101)───@(01)───
      │        │        │
2: ───H────────H────────@(10)───
                        │
3: ─────────────────────H───────
""",
    )
    q = alphaclops.LineQid.for_qid_shape((2, 3, 2))
    c = alphaclops.Circuit(C_02_20H(*q))
    alphaclops.testing.assert_has_diagram(
        c,
        """
0 (d=2): ───@(01)───
            │
1 (d=3): ───@(20)───
            │
2 (d=2): ───H───────
""",
    )


class MockGate(alphaclops.testing.TwoQubitGate):
    def _circuit_diagram_info_(self, args: alphaclops.CircuitDiagramInfoArgs) -> alphaclops.CircuitDiagramInfo:
        self.captured_diagram_args = args
        return alphaclops.CircuitDiagramInfo(wire_symbols=tuple(['M1', 'M2']), exponent=1, connected=True)

    def _has_unitary_(self):
        return True


def test_uninformed_circuit_diagram_info():
    qbits = alphaclops.LineQubit.range(3)
    mock_gate = MockGate()
    cgate = alphaclops.ControlledGate(mock_gate)(*qbits)

    args = alphaclops.CircuitDiagramInfoArgs.UNINFORMED_DEFAULT

    assert alphaclops.circuit_diagram_info(cgate, args) == alphaclops.CircuitDiagramInfo(
        wire_symbols=('@', 'M1', 'M2'), exponent=1, connected=True, exponent_qubit_index=1
    )
    assert mock_gate.captured_diagram_args == args


def test_bounded_effect():
    assert alphaclops.trace_distance_bound(CY ** 0.001) < 0.01
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(CCH), 1.0)
    foo = sympy.Symbol('foo')
    assert alphaclops.trace_distance_bound(alphaclops.ControlledGate(alphaclops.X ** foo)) == 1


@pytest.mark.parametrize(
    'gate',
    [
        alphaclops.ControlledGate(alphaclops.Z),
        alphaclops.ControlledGate(alphaclops.Z, num_controls=1),
        alphaclops.ControlledGate(alphaclops.Z, num_controls=2),
        C0C1H,
        C2C2H,
        C_01_10_11H,
        C_xorH,
        C_02_20H,
    ],
)
def test_repr(gate):
    alphaclops.testing.assert_equivalent_repr(gate)


def test_str():
    assert str(alphaclops.ControlledGate(alphaclops.X)) == 'CX'
    assert str(alphaclops.ControlledGate(alphaclops.Z)) == 'CZ'
    assert str(alphaclops.ControlledGate(alphaclops.S)) == 'CS'
    assert str(alphaclops.ControlledGate(alphaclops.Z ** 0.125)) == 'CZ**0.125'
    assert str(alphaclops.ControlledGate(alphaclops.ControlledGate(alphaclops.S))) == 'CCS'
    assert str(C0Y) == 'C0Y'
    assert str(C0C1H) == 'C0C1H'
    assert str(C0Restricted) == 'C0Restricted'
    assert str(C2Y) == 'C2Y'
    assert str(C2C2H) == 'C2C2H'
    assert str(C2Restricted) == 'C2Restricted'


def test_controlled_mixture():
    c_yes = alphaclops.ControlledGate(sub_gate=alphaclops.phase_flip(0.25), num_controls=1)
    assert alphaclops.has_mixture(c_yes)
    assert alphaclops.approx_eq(alphaclops.mixture(c_yes), [(0.75, np.eye(4)), (0.25, alphaclops.unitary(alphaclops.CZ))])
