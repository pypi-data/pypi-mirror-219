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

import itertools
import re
from typing import cast, Tuple, Union

import numpy as np
import pytest
import sympy

import alphaclops
from alphaclops import protocols
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
        return 'alphaclops.ops.controlled_operation_test.GateUsingWorkspaceForApplyUnitary()'


class GateAllocatingNewSpaceForResult(alphaclops.testing.SingleQubitGate):
    def __init__(self):
        self._matrix = alphaclops.testing.random_unitary(2, random_state=1234)

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
        return 'alphaclops.ops.controlled_operation_test.GateAllocatingNewSpaceForResult()'


def test_controlled_operation_init():
    class G(alphaclops.testing.SingleQubitGate):
        def _has_mixture_(self):
            return True

    g = G()
    cb = alphaclops.NamedQubit('ctr')
    q = alphaclops.NamedQubit('q')
    v = alphaclops.GateOperation(g, (q,))
    c = alphaclops.ControlledOperation([cb], v)
    assert c.sub_operation == v
    assert c.controls == (cb,)
    assert c.qubits == (cb, q)
    assert c == c.with_qubits(cb, q)
    assert c.control_values == alphaclops.SumOfProducts(((1,),))
    assert alphaclops.qid_shape(c) == (2, 2)

    c = alphaclops.ControlledOperation([cb], v, control_values=[0])
    assert c.sub_operation == v
    assert c.controls == (cb,)
    assert c.qubits == (cb, q)
    assert c == c.with_qubits(cb, q)
    assert c.control_values == alphaclops.SumOfProducts(((0,),))
    assert alphaclops.qid_shape(c) == (2, 2)

    c = alphaclops.ControlledOperation([cb.with_dimension(3)], v)
    assert c.sub_operation == v
    assert c.controls == (cb.with_dimension(3),)
    assert c.qubits == (cb.with_dimension(3), q)
    assert c == c.with_qubits(cb.with_dimension(3), q)
    assert c.control_values == alphaclops.SumOfProducts(((1,),))
    assert alphaclops.qid_shape(c) == (3, 2)

    with pytest.raises(ValueError, match=r'alphaclops\.num_qubits\(control_values\) != len\(controls\)'):
        _ = alphaclops.ControlledOperation([cb], v, control_values=[1, 1])
    with pytest.raises(ValueError, match='Control values .*outside of range'):
        _ = alphaclops.ControlledOperation([cb], v, control_values=[2])
    with pytest.raises(ValueError, match='Control values .*outside of range'):
        _ = alphaclops.ControlledOperation([cb], v, control_values=[(1, -1)])
    with pytest.raises(ValueError, match=re.escape("Duplicate control qubits ['ctr'].")):
        _ = alphaclops.ControlledOperation([cb, alphaclops.LineQubit(0), cb], alphaclops.X(q))
    with pytest.raises(ValueError, match=re.escape("Sub-op and controls share qubits ['ctr']")):
        _ = alphaclops.ControlledOperation([cb, alphaclops.LineQubit(0)], alphaclops.CX(cb, q))
    with pytest.raises(ValueError, match='Cannot control measurement'):
        _ = alphaclops.ControlledOperation([cb], alphaclops.measure(q))
    with pytest.raises(ValueError, match='Cannot control channel'):
        _ = alphaclops.ControlledOperation([cb], alphaclops.PhaseDampingChannel(1)(q))


def test_controlled_operation_eq():
    c1 = alphaclops.NamedQubit('c1')
    q1 = alphaclops.NamedQubit('q1')
    c2 = alphaclops.NamedQubit('c2')

    eq = alphaclops.testing.EqualsTester()

    eq.make_equality_group(lambda: alphaclops.ControlledOperation([c1], alphaclops.X(q1)))
    eq.make_equality_group(lambda: alphaclops.ControlledOperation([c2], alphaclops.X(q1)))
    eq.make_equality_group(lambda: alphaclops.ControlledOperation([c1], alphaclops.Z(q1)))
    eq.add_equality_group(alphaclops.ControlledOperation([c2], alphaclops.Z(q1)))
    eq.add_equality_group(
        alphaclops.ControlledOperation([c1, c2], alphaclops.Z(q1)),
        alphaclops.ControlledOperation([c2, c1], alphaclops.Z(q1)),
    )
    eq.add_equality_group(
        alphaclops.ControlledOperation(
            [c1, c2.with_dimension(3)], alphaclops.Z(q1), control_values=[1, (0, 2)]
        ),
        alphaclops.ControlledOperation(
            [c2.with_dimension(3), c1], alphaclops.Z(q1), control_values=[(2, 0), 1]
        ),
    )


def test_str():
    c1 = alphaclops.NamedQubit('c1')
    c2 = alphaclops.NamedQubit('c2')
    q2 = alphaclops.NamedQubit('q2')

    assert str(alphaclops.ControlledOperation([c1], alphaclops.CZ(c2, q2))) == "CCZ(c1, c2, q2)"

    class SingleQubitOp(alphaclops.Operation):
        @property
        def qubits(self) -> Tuple[alphaclops.Qid, ...]:
            return ()

        def with_qubits(self, *new_qubits: alphaclops.Qid):
            pass

        def __str__(self):
            return "Op(q2)"

        def _has_mixture_(self):
            return True

    assert str(alphaclops.ControlledOperation([c1, c2], SingleQubitOp())) == "CC(c1, c2, Op(q2))"

    assert (
        str(alphaclops.ControlledOperation([c1, c2.with_dimension(3)], SingleQubitOp()))
        == "CC(c1, c2 (d=3), Op(q2))"
    )

    assert (
        str(
            alphaclops.ControlledOperation(
                [c1, c2.with_dimension(3)], SingleQubitOp(), control_values=[1, (2, 0)]
            )
        )
        == "C1C02(c1, c2 (d=3), Op(q2))"
    )


def test_repr():
    a, b, c, d = alphaclops.LineQubit.range(4)

    ch = alphaclops.H(a).controlled_by(b)
    cch = alphaclops.H(a).controlled_by(b, c)
    ccz = alphaclops.ControlledOperation([a], alphaclops.CZ(b, c))
    c1c02z = alphaclops.ControlledOperation(
        [a, b.with_dimension(3)], alphaclops.CZ(d, c), control_values=[1, (2, 0)]
    )

    assert repr(ch) == ('alphaclops.H(alphaclops.LineQubit(0)).controlled_by(alphaclops.LineQubit(1))')
    alphaclops.testing.assert_equivalent_repr(ch)
    alphaclops.testing.assert_equivalent_repr(cch)
    alphaclops.testing.assert_equivalent_repr(ccz)
    alphaclops.testing.assert_equivalent_repr(c1c02z)


# A contrived multiqubit Hadamard gate that asserts the consistency of
# the passed in Args and puts an H on all qubits
# displays them as 'H(qubit)' on the wire
class MultiH(alphaclops.Gate):
    def __init__(self, num_qubits):
        self._num_qubits = num_qubits

    def num_qubits(self) -> int:
        return self._num_qubits

    def _circuit_diagram_info_(
        self, args: protocols.CircuitDiagramInfoArgs
    ) -> protocols.CircuitDiagramInfo:
        assert args.known_qubit_count is not None
        assert args.known_qubits is not None

        return protocols.CircuitDiagramInfo(
            wire_symbols=tuple(f'H({q})' for q in args.known_qubits), connected=True
        )

    def _has_mixture_(self):
        return True


def test_circuit_diagram():
    qubits = alphaclops.LineQubit.range(3)
    c = alphaclops.Circuit()
    c.append(alphaclops.ControlledOperation(qubits[:1], MultiH(2)(*qubits[1:])))

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

    c = alphaclops.Circuit()
    c.append(alphaclops.ControlledOperation(qubits[:2], MultiH(1)(*qubits[2:])))

    alphaclops.testing.assert_has_diagram(
        c,
        """
0: ───@─────────
      │
1: ───@─────────
      │
2: ───H(q(2))───
""",
    )

    qubits = alphaclops.LineQid.for_qid_shape((3, 3, 3, 2))
    c = alphaclops.Circuit()
    c.append(
        alphaclops.ControlledOperation(
            qubits[:3], MultiH(1)(*qubits[3:]), control_values=[1, (0, 1), (2, 0)]
        )
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


class MockGate(alphaclops.testing.TwoQubitGate):
    def __init__(self, exponent_qubit_index=None):
        self._exponent_qubit_index = exponent_qubit_index

    def _circuit_diagram_info_(
        self, args: protocols.CircuitDiagramInfoArgs
    ) -> protocols.CircuitDiagramInfo:
        self.captured_diagram_args = args
        return alphaclops.CircuitDiagramInfo(
            wire_symbols=tuple(['M1', 'M2']),
            exponent=1,
            exponent_qubit_index=self._exponent_qubit_index,
            connected=True,
        )

    def _has_mixture_(self):
        return True


def test_controlled_diagram_exponent():
    for q in itertools.permutations(alphaclops.LineQubit.range(5)):
        for idx in [None, 0, 1]:
            op = MockGate(idx)(*q[:2]).controlled_by(*q[2:])
            add = 0 if idx is None else idx
            assert alphaclops.circuit_diagram_info(op).exponent_qubit_index == len(q[2:]) + add


def test_uninformed_circuit_diagram_info():
    qbits = alphaclops.LineQubit.range(3)
    mock_gate = MockGate()
    c_op = alphaclops.ControlledOperation(qbits[:1], mock_gate(*qbits[1:]))

    args = protocols.CircuitDiagramInfoArgs.UNINFORMED_DEFAULT

    assert alphaclops.circuit_diagram_info(c_op, args) == alphaclops.CircuitDiagramInfo(
        wire_symbols=('@', 'M1', 'M2'), exponent=1, connected=True, exponent_qubit_index=1
    )
    assert mock_gate.captured_diagram_args == args


def test_non_diagrammable_subop():
    qbits = alphaclops.LineQubit.range(2)

    class UndiagrammableGate(alphaclops.testing.SingleQubitGate):
        def _has_mixture_(self):
            return True

    undiagrammable_op = UndiagrammableGate()(qbits[1])

    c_op = alphaclops.ControlledOperation(qbits[:1], undiagrammable_op)
    assert alphaclops.circuit_diagram_info(c_op, default=None) is None


@pytest.mark.parametrize(
    'gate, should_decompose_to_target',
    [
        (alphaclops.X(alphaclops.NamedQubit('q1')), True),
        (alphaclops.X(alphaclops.NamedQubit('q1')) ** 0.5, True),
        (alphaclops.rx(np.pi)(alphaclops.NamedQubit('q1')), True),
        (alphaclops.rx(np.pi / 2)(alphaclops.NamedQubit('q1')), True),
        (alphaclops.Z(alphaclops.NamedQubit('q1')), True),
        (alphaclops.H(alphaclops.NamedQubit('q1')), True),
        (alphaclops.CNOT(alphaclops.NamedQubit('q1'), alphaclops.NamedQubit('q2')), True),
        (alphaclops.SWAP(alphaclops.NamedQubit('q1'), alphaclops.NamedQubit('q2')), True),
        (alphaclops.CCZ(alphaclops.NamedQubit('q1'), alphaclops.NamedQubit('q2'), alphaclops.NamedQubit('q3')), True),
        (alphaclops.ControlledGate(alphaclops.ControlledGate(alphaclops.CCZ))(*alphaclops.LineQubit.range(5)), True),
        (GateUsingWorkspaceForApplyUnitary()(alphaclops.NamedQubit('q1')), True),
        (GateAllocatingNewSpaceForResult()(alphaclops.NamedQubit('q1')), True),
        (
                alphaclops.MatrixGate(np.kron(*(alphaclops.unitary(alphaclops.H),) * 2), qid_shape=(4,)).on(
                alphaclops.NamedQid("q", 4)
            ),
                False,
        ),
        (
                alphaclops.MatrixGate(alphaclops.testing.random_unitary(4, random_state=1234)).on(
                alphaclops.NamedQubit('q1'), alphaclops.NamedQubit('q2')
            ),
                False,
        ),
        (alphaclops.XX(alphaclops.NamedQubit('q1'), alphaclops.NamedQubit('q2')) ** sympy.Symbol("s"), True),
        (alphaclops.DiagonalGate(sympy.symbols("s1, s2")).on(alphaclops.NamedQubit("q")), False),
    ],
)
def test_controlled_operation_is_consistent(
    gate: alphaclops.GateOperation, should_decompose_to_target: bool
):
    cb = alphaclops.NamedQubit('ctr')
    cgate = alphaclops.ControlledOperation([cb], gate)
    alphaclops.testing.assert_implements_consistent_protocols(cgate)
    alphaclops.testing.assert_decompose_ends_at_default_gateset(
        cgate, ignore_known_gates=not should_decompose_to_target
    )

    cgate = alphaclops.ControlledOperation([cb], gate, control_values=[0])
    alphaclops.testing.assert_implements_consistent_protocols(cgate)
    alphaclops.testing.assert_decompose_ends_at_default_gateset(
        cgate, ignore_known_gates=(not should_decompose_to_target or alphaclops.is_parameterized(gate))
    )

    cgate = alphaclops.ControlledOperation([cb], gate, control_values=[(0, 1)])
    alphaclops.testing.assert_implements_consistent_protocols(cgate)
    alphaclops.testing.assert_decompose_ends_at_default_gateset(
        cgate, ignore_known_gates=(not should_decompose_to_target or alphaclops.is_parameterized(gate))
    )

    cb3 = cb.with_dimension(3)
    cgate = alphaclops.ControlledOperation([cb3], gate, control_values=[(0, 2)])
    alphaclops.testing.assert_implements_consistent_protocols(cgate)
    alphaclops.testing.assert_decompose_ends_at_default_gateset(cgate)


def test_controlled_circuit_operation_is_consistent():
    op = alphaclops.CircuitOperation(
        alphaclops.FrozenCircuit(
            alphaclops.XXPowGate(exponent=0.25, global_shift=-0.5).on(*alphaclops.LineQubit.range(2))
        )
    )
    cb = alphaclops.NamedQubit('ctr')
    cop = alphaclops.ControlledOperation([cb], op)
    alphaclops.testing.assert_implements_consistent_protocols(cop, exponents=(-1, 1, 2))
    alphaclops.testing.assert_decompose_ends_at_default_gateset(cop)

    cop = alphaclops.ControlledOperation([cb], op, control_values=[0])
    alphaclops.testing.assert_implements_consistent_protocols(cop, exponents=(-1, 1, 2))
    alphaclops.testing.assert_decompose_ends_at_default_gateset(cop)

    cop = alphaclops.ControlledOperation([cb], op, control_values=[(0, 1)])
    alphaclops.testing.assert_implements_consistent_protocols(cop, exponents=(-1, 1, 2))
    alphaclops.testing.assert_decompose_ends_at_default_gateset(cop)


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_parameterizable(resolve_fn):
    a = sympy.Symbol('a')
    qubits = alphaclops.LineQubit.range(3)

    cz = alphaclops.ControlledOperation(qubits[:1], alphaclops.Z(qubits[1]))
    cza = alphaclops.ControlledOperation(qubits[:1], alphaclops.ZPowGate(exponent=a)(qubits[1]))
    assert alphaclops.is_parameterized(cza)
    assert not alphaclops.is_parameterized(cz)
    assert resolve_fn(cza, alphaclops.ParamResolver({'a': 1})) == cz

    cchan = alphaclops.ControlledOperation(
        [qubits[0]],
        alphaclops.RandomGateChannel(sub_gate=alphaclops.PhaseDampingChannel(0.1), probability=a)(qubits[1]),
    )
    with pytest.raises(ValueError, match='Cannot control channel'):
        resolve_fn(cchan, alphaclops.ParamResolver({'a': 0.1}))


def test_bounded_effect():
    qubits = alphaclops.LineQubit.range(3)
    cy = alphaclops.ControlledOperation(qubits[:1], alphaclops.Y(qubits[1]))
    assert alphaclops.trace_distance_bound(cy ** 0.001) < 0.01
    foo = sympy.Symbol('foo')
    scy = alphaclops.ControlledOperation(qubits[:1], alphaclops.Y(qubits[1]) ** foo)
    assert alphaclops.trace_distance_bound(scy) == 1.0
    assert alphaclops.approx_eq(alphaclops.trace_distance_bound(cy), 1.0)


def test_controlled_operation_gate():
    gate = alphaclops.X.controlled(control_values=[0, 1], control_qid_shape=[2, 3])
    op = gate.on(alphaclops.LineQubit(0), alphaclops.LineQid(1, 3), alphaclops.LineQubit(2))
    assert op.gate == gate

    class Gateless(alphaclops.Operation):
        @property
        def qubits(self):
            return ()  # coverage: ignore

        def with_qubits(self, *new_qubits):
            return self  # coverage: ignore

        def _has_mixture_(self):
            return True

    op = Gateless().controlled_by(alphaclops.LineQubit(0))
    assert op.gate is None


def test_controlled_mixture():
    a, b = alphaclops.LineQubit.range(2)
    c_yes = alphaclops.ControlledOperation(controls=[b], sub_operation=alphaclops.phase_flip(0.25).on(a))
    assert alphaclops.has_mixture(c_yes)
    assert alphaclops.approx_eq(alphaclops.mixture(c_yes), [(0.75, np.eye(4)), (0.25, alphaclops.unitary(alphaclops.CZ))])
