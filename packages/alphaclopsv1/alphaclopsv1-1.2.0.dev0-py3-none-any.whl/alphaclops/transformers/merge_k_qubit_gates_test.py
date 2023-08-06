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

# pylint: skip-file

from typing import List

import numpy as np
import pytest

import alphaclops


def assert_optimizes(optimized: alphaclops.RandomGrid, expected: alphaclops.RandomGrid):
    # Ignore differences that would be caught by follow-up optimizations.
    followup_transformers: List[alphaclops.TRANSFORMER] = [
        alphaclops.drop_negligible_operations,
        alphaclops.drop_empty_moments,
    ]
    for transform in followup_transformers:
        optimized = transform(optimized)
        expected = transform(expected)

    alphaclops.testing.assert_same_circuits(optimized, expected)


def test_merge_1q_unitaries():
    q, q2 = alphaclops.LineQubit.range(2)
    # 1. Combines trivial 1q sequence.
    c = alphaclops.Circuit(alphaclops.X(q) ** 0.5, alphaclops.Z(q) ** 0.5, alphaclops.X(q) ** -0.5)
    c = alphaclops.merge_k_qubit_unitaries(c, k=1)
    op_list = [*c.all_operations()]
    assert len(op_list) == 1
    assert isinstance(op_list[0].gate, alphaclops.MatrixGate)
    alphaclops.testing.assert_allclose_up_to_global_phase(
        alphaclops.unitary(c), alphaclops.unitary(alphaclops.Y ** 0.5), atol=1e-7
    )

    # 2. Gets blocked at a 2q operation.
    c = alphaclops.Circuit([alphaclops.Z(q), alphaclops.H(q), alphaclops.X(q), alphaclops.H(q), alphaclops.CZ(q, q2), alphaclops.H(q)])
    c = alphaclops.drop_empty_moments(alphaclops.merge_k_qubit_unitaries(c, k=1))
    assert len(c) == 3
    alphaclops.testing.assert_allclose_up_to_global_phase(alphaclops.unitary(c[0]), np.eye(2), atol=1e-7)
    assert isinstance(c[-1][q].gate, alphaclops.MatrixGate)


def test_respects_nocompile_tags():
    q = alphaclops.NamedQubit("q")
    c = alphaclops.Circuit(
        [alphaclops.Z(q), alphaclops.H(q), alphaclops.X(q), alphaclops.H(q), alphaclops.X(q).with_tags("nocompile"), alphaclops.H(q)]
    )
    context = alphaclops.TransformerContext(tags_to_ignore=("nocompile",))
    c = alphaclops.drop_empty_moments(alphaclops.merge_k_qubit_unitaries(c, k=1, context=context))
    assert len(c) == 3
    alphaclops.testing.assert_allclose_up_to_global_phase(alphaclops.unitary(c[0]), np.eye(2), atol=1e-7)
    assert c[1][q] == alphaclops.X(q).with_tags("nocompile")
    assert isinstance(c[-1][q].gate, alphaclops.MatrixGate)


def test_ignores_2qubit_target():
    c = alphaclops.Circuit(alphaclops.CZ(*alphaclops.LineQubit.range(2)))
    assert_optimizes(optimized=alphaclops.merge_k_qubit_unitaries(c, k=1), expected=c)


def test_ignore_unsupported_gate():
    class UnsupportedDummy(alphaclops.testing.SingleQubitGate):
        pass

    c = alphaclops.Circuit(UnsupportedDummy()(alphaclops.LineQubit(0)))
    assert_optimizes(optimized=alphaclops.merge_k_qubit_unitaries(c, k=1), expected=c)


def test_1q_rewrite():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.X(q0), alphaclops.Y(q0), alphaclops.X(q1), alphaclops.CZ(q0, q1), alphaclops.Y(q1), alphaclops.measure(q0, q1)
    )
    assert_optimizes(
        optimized=alphaclops.merge_k_qubit_unitaries(
            circuit, k=1, rewriter=lambda ops: alphaclops.H(ops.qubits[0])
        ),
        expected=alphaclops.Circuit(
            alphaclops.H(q0), alphaclops.H(q1), alphaclops.CZ(q0, q1), alphaclops.H(q1), alphaclops.measure(q0, q1)
        ),
    )


def test_merge_k_qubit_unitaries_raises():
    with pytest.raises(ValueError, match="k should be greater than or equal to 1"):
        _ = alphaclops.merge_k_qubit_unitaries(alphaclops.Circuit())


def test_merge_complex_circuit_preserving_moment_structure():
    q = alphaclops.LineQubit.range(3)
    c_orig = alphaclops.Circuit(
        alphaclops.Moment(alphaclops.H.on_each(*q)),
        alphaclops.CNOT(q[0], q[2]),
        alphaclops.CNOT(*q[0:2]),
        alphaclops.H(q[0]),
        alphaclops.CZ(*q[:2]),
        alphaclops.X(q[0]),
        alphaclops.Y(q[1]),
        alphaclops.CNOT(*q[0:2]),
        alphaclops.CNOT(*q[1:3]).with_tags("ignore"),
        alphaclops.X(q[0]),
        alphaclops.Moment(alphaclops.X(q[0]).with_tags("ignore"), alphaclops.Y(q[1]), alphaclops.Z(q[2])),
        alphaclops.Moment(alphaclops.CNOT(*q[:2]), alphaclops.measure(q[2], key="a")),
        alphaclops.X(q[0]).with_classical_controls("a"),
        strategy=alphaclops.InsertStrategy.NEW,
    )
    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───H───@───@───H───@───X───────@─────────────────X───X['ignore']───@───X───
          │   │       │           │                                   │   ║
1: ───H───┼───X───────@───────Y───X───@['ignore']───────Y─────────────X───╫───
          │                           │                                   ║
2: ───H───X───────────────────────────X─────────────────Z─────────────M───╫───
                                                                      ║   ║
a: ═══════════════════════════════════════════════════════════════════@═══^═══
''',
    )
    component_id = 0

    def rewriter_merge_to_circuit_op(op: 'alphaclops.CircuitOperation') -> 'alphaclops.OP_TREE':
        nonlocal component_id
        component_id = component_id + 1
        return op.with_tags(f'{component_id}')

    c_new = alphaclops.merge_k_qubit_unitaries(
        c_orig,
        k=2,
        context=alphaclops.TransformerContext(tags_to_ignore=("ignore",)),
        rewriter=rewriter_merge_to_circuit_op,
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.drop_empty_moments(c_new),
        '''
      [ 0: ───H───@─── ]        [ 0: ───────@───H───@───X───@───X─── ]                                            [ 0: ───────@─── ]
0: ───[           │    ]────────[           │       │       │        ]──────────────────────X['ignore']───────────[           │    ]────────X───
      [ 2: ───H───X─── ]['1']   [ 1: ───H───X───────@───Y───X─────── ]['2']                                       [ 1: ───Y───X─── ]['4']   ║
      │                         │                                                                                 │                         ║
1: ───┼─────────────────────────#2────────────────────────────────────────────@['ignore']─────────────────────────#2────────────────────────╫───
      │                                                                       │                                                             ║
2: ───#2──────────────────────────────────────────────────────────────────────X─────────────[ 2: ───Z─── ]['3']───M─────────────────────────╫───
                                                                                                                  ║                         ║
a: ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════@═════════════════════════^═══''',
    )

    component_id = 0

    def rewriter_replace_with_decomp(op: 'alphaclops.CircuitOperation') -> 'alphaclops.OP_TREE':
        nonlocal component_id
        component_id = component_id + 1
        tag = f'{component_id}'
        if len(op.qubits) == 1:
            return [alphaclops.T(op.qubits[0]).with_tags(tag)]
        one_layer = [op.with_tags(tag) for op in alphaclops.T.on_each(*op.qubits)]
        two_layer = [alphaclops.SQRT_ISWAP(*op.qubits).with_tags(tag)]
        return [one_layer, two_layer, one_layer]

    c_new = alphaclops.merge_k_qubit_unitaries(
        c_orig,
        k=2,
        context=alphaclops.TransformerContext(tags_to_ignore=("ignore",)),
        rewriter=rewriter_replace_with_decomp,
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.drop_empty_moments(c_new),
        '''
0: ───T['1']───iSwap['1']───T['1']───T['2']───iSwap['2']───T['2']─────────────────X['ignore']───T['4']───iSwap['4']───T['4']───X───
               │                              │                                                          │                     ║
1: ────────────┼─────────────────────T['2']───iSwap^0.5────T['2']───@['ignore']─────────────────T['4']───iSwap^0.5────T['4']───╫───
               │                                                    │                                                          ║
2: ───T['1']───iSwap^0.5────T['1']──────────────────────────────────X─────────────T['3']────────M──────────────────────────────╫───
                                                                                                ║                              ║
a: ═════════════════════════════════════════════════════════════════════════════════════════════@══════════════════════════════^═══''',
    )


def test_merge_k_qubit_unitaries_deep():
    q = alphaclops.LineQubit.range(2)
    h_cz_y = [alphaclops.H(q[0]), alphaclops.CZ(*q), alphaclops.Y(q[1])]
    c_orig = alphaclops.Circuit(
        h_cz_y,
        alphaclops.Moment(alphaclops.X(q[0]).with_tags("ignore"), alphaclops.Y(q[1])),
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(h_cz_y)).repeat(6).with_tags("ignore"),
        [alphaclops.CNOT(*q), alphaclops.CNOT(*q)],
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(h_cz_y)).repeat(4),
        [alphaclops.CNOT(*q), alphaclops.CZ(*q), alphaclops.CNOT(*q)],
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(h_cz_y)).repeat(5).with_tags("preserve_tag"),
    )

    def _wrap_in_cop(ops: alphaclops.OP_TREE, tag: str):
        return alphaclops.CircuitOperation(alphaclops.FrozenCircuit(ops)).with_tags(tag)

    c_expected = alphaclops.Circuit(
        _wrap_in_cop([h_cz_y, alphaclops.Y(q[1])], '1'),
        alphaclops.Moment(alphaclops.X(q[0]).with_tags("ignore")),
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(h_cz_y)).repeat(6).with_tags("ignore"),
        _wrap_in_cop([alphaclops.CNOT(*q), alphaclops.CNOT(*q)], '2'),
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(_wrap_in_cop(h_cz_y, '3'))).repeat(4),
        _wrap_in_cop([alphaclops.CNOT(*q), alphaclops.CZ(*q), alphaclops.CNOT(*q)], '4'),
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(_wrap_in_cop(h_cz_y, '5')))
        .repeat(5)
        .with_tags("preserve_tag"),
        strategy=alphaclops.InsertStrategy.NEW,
    )

    component_id = 0

    def rewriter_merge_to_circuit_op(op: 'alphaclops.CircuitOperation') -> 'alphaclops.OP_TREE':
        nonlocal component_id
        component_id = component_id + 1
        return op.with_tags(f'{component_id}')

    context = alphaclops.TransformerContext(tags_to_ignore=("ignore",), deep=True)
    c_new = alphaclops.merge_k_qubit_unitaries(
        c_orig, k=2, context=context, rewriter=rewriter_merge_to_circuit_op
    )
    alphaclops.testing.assert_same_circuits(c_new, c_expected)

    def _wrap_in_matrix_gate(ops: alphaclops.OP_TREE):
        op = _wrap_in_cop(ops, 'temp')
        return alphaclops.MatrixGate(alphaclops.unitary(op)).on(*op.qubits)

    c_expected_matrix = alphaclops.Circuit(
        _wrap_in_matrix_gate([h_cz_y, alphaclops.Y(q[1])]),
        alphaclops.Moment(alphaclops.X(q[0]).with_tags("ignore")),
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(h_cz_y)).repeat(6).with_tags("ignore"),
        _wrap_in_matrix_gate([alphaclops.CNOT(*q), alphaclops.CNOT(*q)]),
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(_wrap_in_matrix_gate(h_cz_y))).repeat(4),
        _wrap_in_matrix_gate([alphaclops.CNOT(*q), alphaclops.CZ(*q), alphaclops.CNOT(*q)]),
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(_wrap_in_matrix_gate(h_cz_y)))
        .repeat(5)
        .with_tags("preserve_tag"),
        strategy=alphaclops.InsertStrategy.NEW,
    )
    c_new_matrix = alphaclops.merge_k_qubit_unitaries(c_orig, k=2, context=context)
    alphaclops.testing.assert_same_circuits(c_new_matrix, c_expected_matrix)


def test_merge_k_qubit_unitaries_deep_recurses_on_large_circuit_op():
    q = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.X(q[0]), alphaclops.H(q[0]), alphaclops.CNOT(*q)))
    )
    c_expected = alphaclops.Circuit(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.X(q[0]), alphaclops.H(q[0]))).with_tags(
                    "merged"
                ),
                alphaclops.CNOT(*q),
            )
        )
    )
    c_new = alphaclops.merge_k_qubit_unitaries(
        c_orig,
        context=alphaclops.TransformerContext(deep=True),
        k=1,
        rewriter=lambda op: op.with_tags("merged"),
    )
    alphaclops.testing.assert_same_circuits(c_new, c_expected)
