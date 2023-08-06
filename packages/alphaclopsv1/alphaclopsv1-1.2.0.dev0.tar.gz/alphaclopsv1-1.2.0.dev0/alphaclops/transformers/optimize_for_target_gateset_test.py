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

import alphaclops
from alphaclops.protocols.decompose_protocol import DecomposeResult
from alphaclops.transformers.optimize_for_target_gateset import _decompose_operations_to_target_gateset
import pytest


def test_decompose_operations_raises_on_stuck():
    c_orig = alphaclops.Circuit(alphaclops.X(alphaclops.NamedQubit("q")).with_tags("ignore"))
    gateset = alphaclops.Gateset(alphaclops.Y)
    with pytest.raises(ValueError, match="Unable to convert"):
        _ = _decompose_operations_to_target_gateset(c_orig, gateset=gateset, ignore_failures=False)

    # Gates marked with a no-compile tag are completely ignored.
    c_new = _decompose_operations_to_target_gateset(
        c_orig,
        context=alphaclops.TransformerContext(tags_to_ignore=("ignore",)),
        gateset=gateset,
        ignore_failures=False,
    )
    alphaclops.testing.assert_same_circuits(c_orig, c_new)


# pylint: disable=line-too-long
def test_decompose_operations_to_target_gateset_default():
    q = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(
        alphaclops.T(q[0]),
        alphaclops.SWAP(*q),
        alphaclops.T(q[0]),
        alphaclops.SWAP(*q).with_tags("ignore"),
        alphaclops.measure(q[0], key="m"),
        alphaclops.X(q[1]).with_classical_controls("m"),
        alphaclops.Moment(alphaclops.T.on_each(*q)),
        alphaclops.SWAP(*q),
        alphaclops.T.on_each(*q),
    )
    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───T───×───T───×['ignore']───M───────T───×───T───
          │       │             ║           │
1: ───────×───────×─────────────╫───X───T───×───T───
                                ║   ║
m: ═════════════════════════════@═══^═══════════════''',
    )
    context = alphaclops.TransformerContext(tags_to_ignore=("ignore",))
    c_new = _decompose_operations_to_target_gateset(c_orig, context=context)
    alphaclops.testing.assert_has_diagram(
        c_new,
        '''
0: ───T────────────@───Y^-0.5───@───Y^0.5────@───────────T───×['ignore']───M───────T────────────@───Y^-0.5───@───Y^0.5────@───────────T───
                   │            │            │               │             ║                    │            │            │
1: ───────Y^-0.5───@───Y^0.5────@───Y^-0.5───@───Y^0.5───────×─────────────╫───X───T───Y^-0.5───@───Y^0.5────@───Y^-0.5───@───Y^0.5───T───
                                                                           ║   ║
m: ════════════════════════════════════════════════════════════════════════@═══^══════════════════════════════════════════════════════════
''',
    )


def test_decompose_operations_to_target_gateset():
    q = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(
        alphaclops.T(q[0]),
        alphaclops.SWAP(*q),
        alphaclops.T(q[0]),
        alphaclops.SWAP(*q).with_tags("ignore"),
        alphaclops.measure(q[0], key="m"),
        alphaclops.X(q[1]).with_classical_controls("m"),
        alphaclops.Moment(alphaclops.T.on_each(*q)),
        alphaclops.SWAP(*q),
        alphaclops.T.on_each(*q),
    )
    gateset = alphaclops.Gateset(alphaclops.H, alphaclops.CNOT)
    decomposer = (
        lambda op, _: alphaclops.H(op.qubits[0])
        if alphaclops.has_unitary(op) and alphaclops.num_qubits(op) == 1
        else NotImplemented
    )
    context = alphaclops.TransformerContext(tags_to_ignore=("ignore",))
    c_new = _decompose_operations_to_target_gateset(
        c_orig, gateset=gateset, decomposer=decomposer, context=context
    )
    alphaclops.testing.assert_has_diagram(
        c_new,
        '''
0: ───H───@───X───@───H───×['ignore']───M───────H───@───X───@───H───
          │   │   │       │             ║           │   │   │
1: ───────X───@───X───────×─────────────╫───X───H───X───@───X───H───
                                        ║   ║
m: ═════════════════════════════════════@═══^═══════════════════════''',
    )

    with pytest.raises(ValueError, match="Unable to convert"):
        _ = _decompose_operations_to_target_gateset(
            c_orig, gateset=gateset, decomposer=decomposer, context=context, ignore_failures=False
        )


class MatrixGateTargetGateset(alphaclops.CompilationTargetGateset):
    def __init__(self):
        super().__init__(alphaclops.MatrixGate)

    @property
    def num_qubits(self) -> int:
        return 2

    def decompose_to_target_gateset(self, op: 'alphaclops.Operation', _) -> DecomposeResult:
        if alphaclops.num_qubits(op) != 2 or not alphaclops.has_unitary(op):
            return NotImplemented
        return alphaclops.MatrixGate(alphaclops.unitary(op), name="M").on(*op.qubits)


def test_optimize_for_target_gateset_default():
    q = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(
        alphaclops.T(q[0]), alphaclops.SWAP(*q), alphaclops.T(q[0]), alphaclops.SWAP(*q).with_tags("ignore")
    )
    context = alphaclops.TransformerContext(tags_to_ignore=("ignore",))
    c_new = alphaclops.optimize_for_target_gateset(c_orig, context=context)
    alphaclops.testing.assert_has_diagram(
        c_new,
        '''
0: ───T────────────@───Y^-0.5───@───Y^0.5────@───────────T───×['ignore']───
                   │            │            │               │
1: ───────Y^-0.5───@───Y^0.5────@───Y^-0.5───@───Y^0.5───────×─────────────
''',
    )
    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_orig, c_new, atol=1e-6)


def test_optimize_for_target_gateset():
    q = alphaclops.LineQubit.range(4)
    c_orig = alphaclops.Circuit(
        alphaclops.QuantumFourierTransformGate(4).on(*q),
        alphaclops.Y(q[0]).with_tags("ignore"),
        alphaclops.Y(q[1]).with_tags("ignore"),
        alphaclops.CNOT(*q[2:]).with_tags("ignore"),
        alphaclops.measure(*q[:2], key="m"),
        alphaclops.CZ(*q[2:]).with_classical_controls("m"),
        alphaclops.inverse(alphaclops.QuantumFourierTransformGate(4).on(*q)),
    )

    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───qft───Y['ignore']───M───────qft^-1───
      │                   ║       │
1: ───#2────Y['ignore']───M───────#2───────
      │                   ║       │
2: ───#3────@['ignore']───╫───@───#3───────
      │     │             ║   ║   │
3: ───#4────X─────────────╫───@───#4───────
                          ║   ║
m: ═══════════════════════@═══^════════════
''',
    )
    gateset = MatrixGateTargetGateset()
    context = alphaclops.TransformerContext(tags_to_ignore=("ignore",))
    c_new = alphaclops.optimize_for_target_gateset(c_orig, gateset=gateset, context=context)
    alphaclops.testing.assert_has_diagram(
        c_new,
        '''
                                         ┌────────┐                         ┌────────┐                 ┌────────┐
0: ───M[1]──────────M[1]──────────────────────M[1]────Y['ignore']───M────────────M[1]───────────────────M[1]────────M[1]───M[1]───
      │             │                         │                     ║            │                      │           │      │
1: ───M[2]───M[1]───┼─────────────M[1]────M[1]┼───────Y['ignore']───M────────M[1]┼──────────────M[1]────┼───M[1]────┼──────M[2]───
             │      │             │       │   │                     ║        │   │              │       │   │       │
2: ──────────M[2]───M[2]───M[1]───┼───────M[2]┼───────@['ignore']───╫───@────M[2]┼───────M[1]───┼───────┼───M[2]────M[2]──────────
                           │      │           │       │             ║   ║        │       │      │       │
3: ────────────────────────M[2]───M[2]────────M[2]────X─────────────╫───@────────M[2]────M[2]───M[2]────M[2]──────────────────────
                                                                    ║   ║
m: ═════════════════════════════════════════════════════════════════@═══^═════════════════════════════════════════════════════════
                                         └────────┘                         └────────┘                 └────────┘
       ''',
    )

    with pytest.raises(ValueError, match="Unable to convert"):
        # Raises an error due to CCO and Measurement gate, which are not part of the gateset.
        _ = alphaclops.optimize_for_target_gateset(
            c_orig, gateset=gateset, context=context, ignore_failures=False
        )


def test_optimize_for_target_gateset_deep():
    q0, q1 = alphaclops.LineQubit.range(2)
    c_nested = alphaclops.FrozenCircuit(alphaclops.CX(q0, q1))
    c_orig = alphaclops.Circuit(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.H(q0), alphaclops.CircuitOperation(c_nested).repeat(3))
        ).repeat(5)
    )
    c_expected = alphaclops.Circuit(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                alphaclops.single_qubit_matrix_to_phxz(alphaclops.unitary(alphaclops.H(q0))).on(q0),
                alphaclops.CircuitOperation(
                    alphaclops.FrozenCircuit(
                        alphaclops.MatrixGate(c_nested.unitary(qubit_order=[q0, q1]), name="M").on(q0, q1)
                    )
                ).repeat(3),
            )
        ).repeat(5)
    )
    gateset = MatrixGateTargetGateset()
    context = alphaclops.TransformerContext(deep=True)
    c_new = alphaclops.optimize_for_target_gateset(c_orig, gateset=gateset, context=context)
    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_new, c_expected)
    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
      [           [ 0: ───@─── ]             ]
      [ 0: ───H───[       │    ]──────────── ]
0: ───[           [ 1: ───X─── ](loops=3)    ]────────────
      [           │                          ]
      [ 1: ───────#2──────────────────────── ](loops=5)
      │
1: ───#2──────────────────────────────────────────────────
''',
    )
    alphaclops.testing.assert_has_diagram(
        c_new,
        '''
      [                                 [ 0: ───M[1]─── ]             ]
      [ 0: ───PhXZ(a=-0.5,x=0.5,z=-1)───[       │       ]──────────── ]
0: ───[                                 [ 1: ───M[2]─── ](loops=3)    ]────────────
      [                                 │                             ]
      [ 1: ─────────────────────────────#2─────────────────────────── ](loops=5)
      │
1: ───#2───────────────────────────────────────────────────────────────────────────
''',
    )
