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

from typing import Optional, List
import pytest

import alphaclops
from alphaclops.transformers.transformer_primitives import MAPPED_CIRCUIT_OP_TAG


def test_map_operations_can_write_new_gates_inline():
    x = alphaclops.NamedQubit('x')
    y = alphaclops.NamedQubit('y')
    z = alphaclops.NamedQubit('z')
    c = alphaclops.Circuit(
        alphaclops.CZ(x, y),
        alphaclops.Y(x),
        alphaclops.Z(x),
        alphaclops.X(y),
        alphaclops.CNOT(y, z),
        alphaclops.Z(y),
        alphaclops.Z(x),
        alphaclops.CNOT(y, z),
        alphaclops.CNOT(z, y),
    )
    alphaclops.testing.assert_has_diagram(
        c,
        '''
x: ───@───Y───Z───Z───────────
      │
y: ───@───X───@───Z───@───X───
              │       │   │
z: ───────────X───────X───@───
''',
    )
    expected_diagram = '''
x: ───X───X───X───X───────────

y: ───X───X───X───X───X───X───

z: ───────────X───────X───X───
'''
    alphaclops.testing.assert_has_diagram(
        alphaclops.map_operations(c, lambda op, _: alphaclops.X.on_each(*op.qubits)), expected_diagram
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.map_operations_and_unroll(c, lambda op, _: alphaclops.X.on_each(*op.qubits)),
        expected_diagram,
    )


def test_map_operations_does_not_insert_too_many_moments():
    q = alphaclops.LineQubit.range(5)
    c_orig = alphaclops.Circuit(alphaclops.CX(q[0], q[1]), alphaclops.CX(q[3], q[2]), alphaclops.CX(q[3], q[4]))

    def map_func(op: alphaclops.Operation, _: int) -> alphaclops.OP_TREE:
        yield alphaclops.Z.on_each(*op.qubits)
        yield alphaclops.CX(*op.qubits)
        yield alphaclops.Z.on_each(*op.qubits)

    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───@───────
      │
1: ───X───────

2: ───X───────
      │
3: ───@───@───
          │
4: ───────X───
''',
    )

    c_mapped = alphaclops.map_operations(c_orig, map_func)
    circuit_op = alphaclops.CircuitOperation(
        alphaclops.FrozenCircuit(
            alphaclops.Z.on_each(q[0], q[1]), alphaclops.CNOT(q[0], q[1]), alphaclops.Z.on_each(q[0], q[1])
        )
    )
    c_expected = alphaclops.Circuit(
        circuit_op.with_qubits(q[0], q[1]).mapped_op().with_tags('<mapped_circuit_op>'),
        circuit_op.with_qubits(q[3], q[2]).mapped_op().with_tags('<mapped_circuit_op>'),
        circuit_op.with_qubits(q[3], q[4]).mapped_op().with_tags('<mapped_circuit_op>'),
    )
    alphaclops.testing.assert_same_circuits(c_mapped, c_expected)

    alphaclops.testing.assert_has_diagram(
        alphaclops.map_operations_and_unroll(c_orig, map_func),
        '''
0: ───Z───@───Z───────────────
          │
1: ───Z───X───Z───────────────

2: ───Z───X───Z───────────────
          │
3: ───Z───@───Z───Z───@───Z───
                      │
4: ───────────────Z───X───Z───
''',
    )


# pylint: disable=line-too-long
def test_map_operations_deep_subcircuits():
    q = alphaclops.LineQubit.range(5)
    c_orig = alphaclops.Circuit(alphaclops.CX(q[0], q[1]), alphaclops.CX(q[3], q[2]), alphaclops.CX(q[3], q[4]))
    c_orig_with_circuit_ops = alphaclops.Circuit(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                [
                    alphaclops.CircuitOperation(alphaclops.FrozenCircuit(op)).repeat(2).with_tags("internal")
                    for op in c_orig.all_operations()
                ]
            )
        )
        .repeat(6)
        .with_tags("external")
    )

    def map_func(op: alphaclops.Operation, _: int) -> alphaclops.OP_TREE:
        yield [
            alphaclops.Z.on_each(*op.qubits),
            alphaclops.CX(*op.qubits),
            alphaclops.Z.on_each(*op.qubits),
        ] if op.gate == alphaclops.CX else op

    alphaclops.testing.assert_has_diagram(
        c_orig_with_circuit_ops,
        '''
      [       [ 0: ───@─── ]                                                               ]
      [ 0: ───[       │    ]────────────────────────────────────────────────────────────── ]
      [       [ 1: ───X─── ](loops=2)['internal']                                          ]
      [       │                                                                            ]
      [ 1: ───#2────────────────────────────────────────────────────────────────────────── ]
      [                                                                                    ]
      [       [ 2: ───X─── ]                                                               ]
0: ───[ 2: ───[       │    ]────────────────────────────────────────────────────────────── ]────────────────────────
      [       [ 3: ───@─── ](loops=2)['internal']                                          ]
      [       │                                                                            ]
      [       │                                     [ 3: ───@─── ]                         ]
      [ 3: ───#2────────────────────────────────────[       │    ]──────────────────────── ]
      [                                             [ 4: ───X─── ](loops=2)['internal']    ]
      [                                             │                                      ]
      [ 4: ─────────────────────────────────────────#2──────────────────────────────────── ](loops=6)['external']
      │
1: ───#2────────────────────────────────────────────────────────────────────────────────────────────────────────────
      │
2: ───#3────────────────────────────────────────────────────────────────────────────────────────────────────────────
      │
3: ───#4────────────────────────────────────────────────────────────────────────────────────────────────────────────
      │
4: ───#5────────────────────────────────────────────────────────────────────────────────────────────────────────────
''',
    )

    c_mapped = alphaclops.map_operations(c_orig_with_circuit_ops, map_func, deep=True)
    for unroller in [
        alphaclops.unroll_circuit_op,
        alphaclops.unroll_circuit_op_greedy_earliest,
        alphaclops.unroll_circuit_op_greedy_frontier,
    ]:
        alphaclops.testing.assert_has_diagram(
            unroller(c_mapped, deep=True),
            '''
      [       [ 0: ───Z───@───Z─── ]                                                                       ]
      [ 0: ───[           │        ]────────────────────────────────────────────────────────────────────── ]
      [       [ 1: ───Z───X───Z─── ](loops=2)['internal']                                                  ]
      [       │                                                                                            ]
      [ 1: ───#2────────────────────────────────────────────────────────────────────────────────────────── ]
      [                                                                                                    ]
      [       [ 2: ───Z───X───Z─── ]                                                                       ]
0: ───[ 2: ───[           │        ]────────────────────────────────────────────────────────────────────── ]────────────────────────
      [       [ 3: ───Z───@───Z─── ](loops=2)['internal']                                                  ]
      [       │                                                                                            ]
      [       │                                             [ 3: ───Z───@───Z─── ]                         ]
      [ 3: ───#2────────────────────────────────────────────[           │        ]──────────────────────── ]
      [                                                     [ 4: ───Z───X───Z─── ](loops=2)['internal']    ]
      [                                                     │                                              ]
      [ 4: ─────────────────────────────────────────────────#2──────────────────────────────────────────── ](loops=6)['external']
      │
1: ───#2────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
      │
2: ───#3────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
      │
3: ───#4────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
      │
4: ───#5────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
''',
        )


# pylint: enable=line-too-long


def test_map_operations_deep_respects_tags_to_ignore():
    q = alphaclops.LineQubit.range(2)
    c_nested = alphaclops.FrozenCircuit(alphaclops.CX(*q), alphaclops.CX(*q).with_tags("ignore"), alphaclops.CX(*q))
    c_nested_mapped = alphaclops.FrozenCircuit(alphaclops.CZ(*q), alphaclops.CX(*q).with_tags("ignore"), alphaclops.CZ(*q))
    c_orig = alphaclops.Circuit(
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested,
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                alphaclops.CircuitOperation(c_nested).repeat(5).with_tags("preserve_tag"),
                alphaclops.CircuitOperation(c_nested).repeat(6).with_tags("ignore"),
                alphaclops.CircuitOperation(c_nested).repeat(7),
            )
        ),
        c_nested,
    )
    c_expected = alphaclops.Circuit(
        c_nested_mapped,
        alphaclops.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested_mapped,
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                alphaclops.CircuitOperation(c_nested_mapped).repeat(5).with_tags("preserve_tag"),
                alphaclops.CircuitOperation(c_nested).repeat(6).with_tags("ignore"),
                alphaclops.CircuitOperation(c_nested_mapped).repeat(7),
            )
        ),
        c_nested_mapped,
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.map_operations(
            c_orig,
            lambda op, _: alphaclops.CZ(*op.qubits) if op.gate == alphaclops.CX else op,
            tags_to_ignore=["ignore"],
            deep=True,
        ),
        c_expected,
    )


def test_map_operations_respects_tags_to_ignore():
    q = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.CNOT(*q), alphaclops.CNOT(*q).with_tags("ignore"), alphaclops.CNOT(*q))
    alphaclops.testing.assert_same_circuits(
        alphaclops.Circuit(alphaclops.Z.on_each(*q), alphaclops.CNOT(*q).with_tags("ignore"), alphaclops.Z.on_each(*q)),
        alphaclops.map_operations(c, lambda op, i: alphaclops.Z.on_each(*op.qubits), tags_to_ignore=["ignore"]),
    )


def test_apply_tag_to_inverted_op_set():
    q = alphaclops.LineQubit.range(2)
    op = alphaclops.CNOT(*q)
    tag = "tag_to_flip"
    c_orig = alphaclops.Circuit(op, op.with_tags(tag), alphaclops.CircuitOperation(alphaclops.FrozenCircuit(op)))
    # Toggle with deep = True.
    c_toggled = alphaclops.Circuit(
        op.with_tags(tag), op, alphaclops.CircuitOperation(alphaclops.FrozenCircuit(op.with_tags(tag)))
    )
    alphaclops.testing.assert_same_circuits(alphaclops.toggle_tags(c_orig, [tag], deep=True), c_toggled)
    alphaclops.testing.assert_same_circuits(alphaclops.toggle_tags(c_toggled, [tag], deep=True), c_orig)

    # Toggle with deep = False
    c_toggled = alphaclops.Circuit(
        op.with_tags(tag), op, alphaclops.CircuitOperation(alphaclops.FrozenCircuit(op)).with_tags(tag)
    )
    alphaclops.testing.assert_same_circuits(alphaclops.toggle_tags(c_orig, [tag], deep=False), c_toggled)
    alphaclops.testing.assert_same_circuits(alphaclops.toggle_tags(c_toggled, [tag], deep=False), c_orig)


def test_unroll_circuit_op_and_variants():
    q = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.X(q[0]), alphaclops.CNOT(q[0], q[1]), alphaclops.X(q[0]))
    alphaclops.testing.assert_has_diagram(
        c,
        '''
0: ───X───@───X───
          │
1: ───────X───────
''',
    )
    mapped_circuit = alphaclops.map_operations(
        c, lambda op, i: [alphaclops.Z(q[1])] * 2 if op.gate == alphaclops.CNOT else op
    )
    mapped_circuit_deep = alphaclops.Circuit(
        [alphaclops.Moment(alphaclops.CircuitOperation(alphaclops.FrozenCircuit(m))) for m in mapped_circuit[:-1]],
        mapped_circuit[-1],
    )
    alphaclops.testing.assert_has_diagram(
        mapped_circuit_deep,
        '''
0: ───[ 0: ───X─── ]────────────────────────────────────────────────────────────X───

1: ────────────────────[ 1: ───[ 1: ───Z───Z─── ]['<mapped_circuit_op>']─── ]───────
''',
    )
    for unroller in [
        alphaclops.unroll_circuit_op_greedy_earliest,
        alphaclops.unroll_circuit_op_greedy_frontier,
        alphaclops.unroll_circuit_op,
    ]:
        alphaclops.testing.assert_same_circuits(
            unroller(mapped_circuit), unroller(mapped_circuit_deep, deep=True, tags_to_check=None)
        )
        alphaclops.testing.assert_has_diagram(
            unroller(mapped_circuit_deep, deep=True),
            '''
0: ───[ 0: ───X─── ]────────────────────────X───

1: ────────────────────[ 1: ───Z───Z─── ]───────
            ''',
        )

    alphaclops.testing.assert_has_diagram(
        alphaclops.unroll_circuit_op(mapped_circuit),
        '''
0: ───X───────────X───

1: ───────Z───Z───────
''',
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.unroll_circuit_op_greedy_earliest(mapped_circuit),
        '''
0: ───X───────X───

1: ───Z───Z───────
''',
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.unroll_circuit_op_greedy_frontier(mapped_circuit),
        '''
0: ───X───────X───

1: ───────Z───Z───
''',
    )


def test_unroll_circuit_op_greedy_frontier_doesnt_touch_same_op_twice():
    q = alphaclops.NamedQubit("q")
    nested_ops = [alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.X(q)))] * 5
    nested_circuit_op = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(nested_ops))
    c = alphaclops.Circuit(nested_circuit_op, nested_circuit_op, nested_circuit_op)
    c_expected = alphaclops.Circuit(nested_ops, nested_ops, nested_ops)
    c_unrolled = alphaclops.unroll_circuit_op_greedy_frontier(c, tags_to_check=None)
    alphaclops.testing.assert_same_circuits(c_unrolled, c_expected)


def test_unroll_circuit_op_deep():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    c = alphaclops.Circuit(
        alphaclops.X(q0),
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.X(q1), alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.X(q2))))
        ),
    )
    expected = alphaclops.Circuit(alphaclops.X.on_each(q0, q1, q2))
    alphaclops.testing.assert_same_circuits(
        alphaclops.unroll_circuit_op(c, tags_to_check=None, deep=True), expected
    )
    expected = alphaclops.Circuit(
        alphaclops.X.on_each(q0, q1), alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.X(q2)))
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.unroll_circuit_op(c, tags_to_check=None, deep=False), expected
    )


def test_unroll_circuit_op_no_tags():
    q = alphaclops.LineQubit.range(2)
    op_list = [alphaclops.X(q[0]), alphaclops.Y(q[1])]
    op1 = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(op_list))
    op2 = op1.with_tags("custom tag")
    op3 = op1.with_tags(MAPPED_CIRCUIT_OP_TAG)
    c = alphaclops.Circuit(op1, op2, op3)
    for unroller in [
        alphaclops.unroll_circuit_op,
        alphaclops.unroll_circuit_op_greedy_earliest,
        alphaclops.unroll_circuit_op_greedy_frontier,
    ]:
        alphaclops.testing.assert_same_circuits(
            unroller(c, tags_to_check=None), alphaclops.Circuit([op_list] * 3)
        )
        alphaclops.testing.assert_same_circuits(unroller(c), alphaclops.Circuit([op1, op2, op_list]))
        alphaclops.testing.assert_same_circuits(
            unroller(c, tags_to_check=("custom tag",)), alphaclops.Circuit([op1, op_list, op3])
        )
        alphaclops.testing.assert_same_circuits(
            unroller(c, tags_to_check=("custom tag", MAPPED_CIRCUIT_OP_TAG)),
            alphaclops.Circuit([op1, op_list, op_list]),
        )


def test_map_operations_raises_qubits_not_subset():
    q = alphaclops.LineQubit.range(3)
    with pytest.raises(ValueError, match='should act on a subset'):
        _ = alphaclops.map_operations(
            alphaclops.Circuit(alphaclops.CNOT(q[0], q[1])), lambda op, i: alphaclops.CNOT(q[1], q[2])
        )


def test_map_operations_can_add_qubits_if_flag_false():
    q = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.H(q[0]))
    c_mapped = alphaclops.map_operations(c, lambda *_: alphaclops.CNOT(q[0], q[1]), raise_if_add_qubits=False)
    alphaclops.testing.assert_same_circuits(c_mapped, alphaclops.Circuit(alphaclops.CNOT(q[0], q[1])))


def test_map_operations_maps_different_ops_from_same_moment_to_shared_qubits():
    q = alphaclops.LineQubit.range(3)
    c = alphaclops.Circuit(alphaclops.H.on_each(q[:2]))
    c_mapped = alphaclops.map_operations(
        c, lambda op, _: op.controlled_by(q[2]), raise_if_add_qubits=False
    )
    alphaclops.testing.assert_same_circuits(
        c_mapped, alphaclops.Circuit(alphaclops.H(q[0]).controlled_by(q[2]), alphaclops.H(q[1]).controlled_by(q[2]))
    )


def test_map_operations_can_drop_operations():
    q = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.X(q[0]), alphaclops.Y(q[1]), alphaclops.X(q[1]), alphaclops.Y(q[0]))
    c_mapped = alphaclops.map_operations(c, lambda op, _: op if op.gate == alphaclops.X else [])
    c_expected = alphaclops.Circuit(alphaclops.Moment(alphaclops.X(q[0])), alphaclops.Moment(alphaclops.X(q[1])))
    alphaclops.testing.assert_same_circuits(c_mapped, c_expected)


def test_map_moments_drop_empty_moments():
    op = alphaclops.X(alphaclops.NamedQubit("x"))
    c = alphaclops.Circuit(alphaclops.Moment(op), alphaclops.Moment(), alphaclops.Moment(op))
    c_mapped = alphaclops.map_moments(c, lambda m, i: [] if len(m) == 0 else [m])
    alphaclops.testing.assert_same_circuits(c_mapped, alphaclops.Circuit(c[0], c[0]))


def test_map_moments_drop_empty_moments_deep():
    op = alphaclops.X(alphaclops.NamedQubit("q"))
    c_nested = alphaclops.FrozenCircuit(alphaclops.Moment(op), alphaclops.Moment(), alphaclops.Moment(op))
    circuit_op = alphaclops.CircuitOperation(c_nested).repeat(2)
    circuit_op_dropped = alphaclops.CircuitOperation(alphaclops.FrozenCircuit([op, op])).repeat(2)
    c_orig = alphaclops.Circuit(
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(6).with_tags("ignore"),
        c_nested,
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(circuit_op, circuit_op.with_tags("ignore"), circuit_op)
        )
        .repeat(5)
        .with_tags("preserve_tag"),
    )
    c_expected = alphaclops.Circuit(
        [op, op],
        alphaclops.CircuitOperation(c_nested).repeat(6).with_tags("ignore"),
        [op, op],
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                circuit_op_dropped, circuit_op.with_tags("ignore"), circuit_op_dropped
            )
        )
        .repeat(5)
        .with_tags("preserve_tag"),
    )
    c_mapped = alphaclops.map_moments(
        c_orig, lambda m, i: [] if len(m) == 0 else [m], deep=True, tags_to_ignore=("ignore",)
    )
    alphaclops.testing.assert_same_circuits(c_mapped, c_expected)


def _merge_z_moments_func(m1: alphaclops.Moment, m2: alphaclops.Moment) -> Optional[alphaclops.Moment]:
    if any(op.gate != alphaclops.Z for m in [m1, m2] for op in m):
        return None
    return alphaclops.Moment(
        alphaclops.Z(q) for q in (m1.qubits | m2.qubits) if m1.operates_on([q]) ^ m2.operates_on([q])
    )


def test_merge_moments():
    q = alphaclops.LineQubit.range(3)
    c_orig = alphaclops.Circuit(
        alphaclops.Z.on_each(q[0], q[1]),
        alphaclops.Z.on_each(q[1], q[2]),
        alphaclops.Z.on_each(q[1], q[0]),
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    c_orig = alphaclops.Circuit(c_orig, alphaclops.CCX(*q), c_orig)
    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───Z───────Z───@───Z───────Z───
                  │
1: ───Z───Z───Z───@───Z───Z───Z───
                  │
2: ───────Z───────X───────Z───────
''',
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.merge_moments(c_orig, _merge_z_moments_func),
        '''
0: ───────@───────
          │
1: ───Z───@───Z───
          │
2: ───Z───X───Z───
''',
    )


def test_merge_moments_deep():
    q = alphaclops.LineQubit.range(3)
    c_z_moments = alphaclops.Circuit(
        [alphaclops.Z.on_each(q[0], q[1]), alphaclops.Z.on_each(q[1], q[2]), alphaclops.Z.on_each(q[1], q[0])],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    merged_z_moment = alphaclops.Moment(alphaclops.Z.on_each(*q[1:]))
    c_nested_circuit = alphaclops.FrozenCircuit(c_z_moments, alphaclops.CCX(*q), c_z_moments)
    c_merged_circuit = alphaclops.FrozenCircuit(merged_z_moment, alphaclops.CCX(*q), merged_z_moment)
    c_orig = alphaclops.Circuit(
        alphaclops.CircuitOperation(c_nested_circuit).repeat(5).with_tags("ignore"),
        c_nested_circuit,
        alphaclops.CircuitOperation(c_nested_circuit).repeat(6).with_tags("preserve_tag"),
        c_nested_circuit,
        alphaclops.CircuitOperation(c_nested_circuit).repeat(7),
    )
    c_expected = alphaclops.Circuit(
        alphaclops.CircuitOperation(c_nested_circuit).repeat(5).with_tags("ignore"),
        c_merged_circuit,
        alphaclops.CircuitOperation(c_merged_circuit).repeat(6).with_tags("preserve_tag"),
        c_merged_circuit,
        alphaclops.CircuitOperation(c_merged_circuit).repeat(7),
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.merge_moments(c_orig, _merge_z_moments_func, tags_to_ignore=("ignore",), deep=True),
        c_expected,
    )


def test_merge_moments_empty_moment_as_intermediate_step():
    q = alphaclops.NamedQubit("q")
    c_orig = alphaclops.Circuit([alphaclops.X(q), alphaclops.Y(q), alphaclops.Z(q)] * 2, alphaclops.X(q) ** 0.5)

    def merge_func(m1: alphaclops.Moment, m2: alphaclops.Moment):
        gate = alphaclops.single_qubit_matrix_to_phxz(alphaclops.unitary(alphaclops.Circuit(m1, m2)), atol=1e-8)
        return alphaclops.Moment(gate.on(q) if gate else [])

    c_new = alphaclops.merge_moments(c_orig, merge_func)
    assert len(c_new) == 1
    assert isinstance(c_new[0][q].gate, alphaclops.PhasedXZGate)
    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_orig, c_new, atol=1e-8)


def test_merge_moments_empty_circuit():
    def fail_if_called_func(*_):
        assert False

    c = alphaclops.Circuit()
    assert alphaclops.merge_moments(c, fail_if_called_func) is c


def test_merge_operations_raises():
    q = alphaclops.LineQubit.range(3)
    c = alphaclops.Circuit(alphaclops.CZ(*q[:2]), alphaclops.X(q[0]))
    with pytest.raises(ValueError, match='must act on a subset of qubits'):
        alphaclops.merge_operations(c, lambda *_: alphaclops.X(q[2]))


def test_merge_operations_nothing_to_merge():
    def fail_if_called_func(*_):
        assert False

    # Empty Circuit.
    c = alphaclops.Circuit()
    assert alphaclops.merge_operations(c, fail_if_called_func) == c
    # Single moment
    q = alphaclops.LineQubit.range(3)
    c += alphaclops.Moment(alphaclops.CZ(*q[:2]))
    assert alphaclops.merge_operations(c, fail_if_called_func) == c
    # Multi moment with disjoint operations + global phase operation.
    c += alphaclops.Moment(alphaclops.X(q[2]), alphaclops.global_phase_operation(1j))
    assert alphaclops.merge_operations(c, fail_if_called_func) == c
    # Tagged operations to be ignored.
    c += alphaclops.Moment(alphaclops.CNOT(*q[:2]).with_tags("ignore"))
    assert alphaclops.merge_operations(c, fail_if_called_func, tags_to_ignore=["ignore"]) == c


def _create_circuit_to_merge():
    q = alphaclops.LineQubit.range(3)
    return alphaclops.Circuit(
        alphaclops.Moment(alphaclops.H.on_each(*q)),
        alphaclops.CNOT(q[0], q[2]),
        alphaclops.CNOT(*q[0:2]),
        alphaclops.H(q[0]),
        alphaclops.CZ(*q[:2]),
        alphaclops.X(q[0]),
        alphaclops.Y(q[1]),
        alphaclops.CNOT(*q[0:2]),
        alphaclops.CNOT(*q[1:3]),
        alphaclops.X(q[0]),
        alphaclops.Moment(alphaclops.X(q[0]).with_tags("ignore"), alphaclops.Y(q[1])),
        alphaclops.CNOT(*q[:2]),
        strategy=alphaclops.InsertStrategy.NEW,
    )


def test_merge_operations_merges_connected_component():
    c_orig = _create_circuit_to_merge()
    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───H───@───@───H───@───X───────@───────X───X['ignore']───@───
          │   │       │           │                         │
1: ───H───┼───X───────@───────Y───X───@───────Y─────────────X───
          │                           │
2: ───H───X───────────────────────────X─────────────────────────
''',
    )

    def merge_func(op1, op2):
        """Artificial example where a CZ will absorb any merge-able operation."""
        for op in [op1, op2]:
            if op.gate == alphaclops.CZ:
                return op
        return None

    c_new = alphaclops.merge_operations(c_orig, merge_func)
    alphaclops.testing.assert_has_diagram(
        c_new,
        '''
0: ───H───@───────────@───────────────────────────@───
          │           │                           │
1: ───────┼───────────@───────────────@───────Y───X───
          │                           │
2: ───H───X───────────────────────────X───────────────''',
    )


def test_merge_operations_deep():
    q = alphaclops.LineQubit.range(2)
    h_cz_y = [alphaclops.H(q[0]), alphaclops.CZ(*q), alphaclops.Y(q[1])]
    m_cz_m = [alphaclops.Moment(), alphaclops.Moment(alphaclops.CZ(*q)), alphaclops.Moment()]
    c_orig = alphaclops.Circuit(
        h_cz_y,
        alphaclops.Moment(alphaclops.X(q[0]).with_tags("ignore"), alphaclops.Y(q[1])),
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(h_cz_y)).repeat(6).with_tags("ignore"),
        [alphaclops.CNOT(*q), alphaclops.CNOT(*q)],
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(h_cz_y)).repeat(4),
        [alphaclops.CNOT(*q), alphaclops.CZ(*q), alphaclops.CNOT(*q)],
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(h_cz_y)).repeat(5).with_tags("preserve_tag"),
    )
    c_expected = alphaclops.Circuit(
        m_cz_m,
        alphaclops.Moment(alphaclops.X(q[0]).with_tags("ignore")),
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(h_cz_y)).repeat(6).with_tags("ignore"),
        [alphaclops.CNOT(*q), alphaclops.CNOT(*q)],
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(m_cz_m)).repeat(4),
        [alphaclops.CZ(*q), alphaclops.Moment(), alphaclops.Moment()],
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(m_cz_m)).repeat(5).with_tags("preserve_tag"),
        strategy=alphaclops.InsertStrategy.NEW,
    )

    def merge_func(op1, op2):
        """Artificial example where a CZ will absorb any merge-able operation."""
        for op in [op1, op2]:
            if op.gate == alphaclops.CZ:
                return op
        return None

    alphaclops.testing.assert_same_circuits(
        alphaclops.merge_operations(c_orig, merge_func, tags_to_ignore=["ignore"], deep=True), c_expected
    )


# pylint: disable=line-too-long


def test_merge_operations_to_circuit_op_merges_connected_component():
    c_orig = _create_circuit_to_merge()
    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───H───@───@───H───@───X───────@───────X───X['ignore']───@───
          │   │       │           │                         │
1: ───H───┼───X───────@───────Y───X───@───────Y─────────────X───
          │                           │
2: ───H───X───────────────────────────X─────────────────────────
''',
    )

    def can_merge(ops1: List['alphaclops.Operation'], ops2: List['alphaclops.Operation']) -> bool:
        """Artificial example where a CZ will absorb any merge-able operation."""
        return any(o.gate == alphaclops.CZ for op_list in [ops1, ops2] for o in op_list)

    c_new = alphaclops.merge_operations_to_circuit_op(
        c_orig, can_merge, merged_circuit_op_tag="merged", tags_to_ignore=["ignore"]
    )
    alphaclops.testing.assert_has_diagram(
        c_new,
        '''
                      [ 0: ───────@───H───@───X───@───X─── ]
0: ───H───@───────────[           │       │       │        ]─────────────────────────────────X['ignore']───@───
          │           [ 1: ───H───X───────@───Y───X─────── ]['merged']                                     │
          │           │                                                                                    │
1: ───────┼───────────#2─────────────────────────────────────────────────────────────@───────Y─────────────X───
          │                                                                          │
2: ───H───X──────────────────────────────────────────────────────────────────────────X─────────────────────────
''',
    )


def test_merge_2q_unitaries_to_circuit_op():
    c_orig = _create_circuit_to_merge()
    c_orig[-1] = c_orig[-1].with_operations(alphaclops.measure(alphaclops.LineQubit(2)))
    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───H───@───@───H───@───X───────@───────X───X['ignore']───@───
          │   │       │           │                         │
1: ───H───┼───X───────@───────Y───X───@───────Y─────────────X───
          │                           │
2: ───H───X───────────────────────────X─────────────────────M───
''',
    )

    c_new = alphaclops.merge_k_qubit_unitaries_to_circuit_op(
        c_orig, k=2, merged_circuit_op_tag="merged", tags_to_ignore=["ignore"]
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.drop_empty_moments(c_new),
        '''
      [ 0: ───H───@─── ]             [ 0: ───────@───H───@───X───@───X─── ]
0: ───[           │    ]─────────────[           │       │       │        ]────────────────────────────────────────────X['ignore']───@───
      [ 2: ───H───X─── ]['merged']   [ 1: ───H───X───────@───Y───X─────── ]['merged']                                                │
      │                              │                                                                                               │
      │                              │                                                  [ 1: ───@───Y─── ]                           │
1: ───┼──────────────────────────────#2─────────────────────────────────────────────────[       │        ]───────────────────────────X───
      │                                                                                 [ 2: ───X─────── ]['merged']
      │                                                                                 │
2: ───#2────────────────────────────────────────────────────────────────────────────────#2───────────────────────────────────────────M───''',
    )


# pylint: enable=line-too-long


def test_merge_operations_respects_tags_to_ignore():
    q = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(
        alphaclops.CZ(*q),
        alphaclops.Moment(alphaclops.X(q[0]), alphaclops.Y(q[1]).with_tags("ignore")),
        alphaclops.Moment(alphaclops.X(q[0]).with_tags("ignore"), alphaclops.Y(q[1])),
        alphaclops.CZ(*q),
        [alphaclops.CNOT(*q), alphaclops.CNOT(*q).with_tags("ignore"), alphaclops.CNOT(*q)],
        alphaclops.CZ(*q),
    )
    c_merged = alphaclops.Circuit(
        alphaclops.Moment(alphaclops.CZ(*q)),
        alphaclops.Moment(alphaclops.Y(q[1]).with_tags("ignore")),
        alphaclops.Moment(alphaclops.X(q[0]).with_tags("ignore")),
        alphaclops.Moment(alphaclops.CZ(*q)),
        alphaclops.Moment(),
        alphaclops.Moment(alphaclops.CNOT(*q).with_tags("ignore")),
        alphaclops.Moment(alphaclops.CZ(*q)),
        alphaclops.Moment(),
    )

    def merge_func(op1, op2):
        """Artificial example where a CZ will absorb any merge-able operation."""
        return op1 if op1.gate == alphaclops.CZ else (op2 if op2.gate == alphaclops.CZ else None)

    alphaclops.testing.assert_same_circuits(
        alphaclops.merge_operations(c, merge_func, tags_to_ignore=["ignore"]), c_merged
    )


@pytest.mark.parametrize('qubit_order', ([0, 1], [1, 0]))
def test_merge_operations_deterministic_order(qubit_order):
    q = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(alphaclops.identity_each(*q), alphaclops.H.on_each(q[i] for i in qubit_order))
    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───I───H───
      │
1: ───I───H───''',
    )
    c_new = alphaclops.merge_operations(
        c_orig, lambda op1, op2: op2 if isinstance(op1.gate, alphaclops.IdentityGate) else None
    )
    alphaclops.testing.assert_has_diagram(
        c_new,
        '''
0: ───H───────

1: ───────H───''',
    )


@pytest.mark.parametrize("op_density", [0.1, 0.5, 0.9])
def test_merge_operations_complexity(op_density):
    prng = alphaclops.value.parse_random_state(11011)
    circuit = alphaclops.testing.random_circuit(20, 500, op_density, random_state=prng)
    for merge_func in [
        lambda _, __: None,
        lambda op1, _: op1,
        lambda _, op2: op2,
        lambda op1, op2: (op1, op2, None)[prng.choice(3)],
    ]:

        def wrapped_merge_func(op1, op2):
            wrapped_merge_func.num_function_calls += 1
            return merge_func(op1, op2)

        wrapped_merge_func.num_function_calls = 0
        _ = alphaclops.merge_operations(circuit, wrapped_merge_func)
        total_operations = len([*circuit.all_operations()])
        assert wrapped_merge_func.num_function_calls <= 2 * total_operations


def test_merge_operations_does_not_merge_ccos_behind_measurements():
    q = alphaclops.LineQubit.range(2)
    cco_op = alphaclops.X(q[1]).with_classical_controls("a")

    def merge_func(op1, op2):
        return alphaclops.I(*op1.qubits) if op1 == cco_op and op2 == cco_op else None

    circuit = alphaclops.Circuit([alphaclops.H(q[0]), alphaclops.measure(q[0], key="a"), cco_op] * 2)
    alphaclops.testing.assert_same_circuits(alphaclops.merge_operations(circuit, merge_func), circuit)

    circuit = alphaclops.Circuit([alphaclops.H(q[0]), alphaclops.measure(q[0], key="a"), cco_op, cco_op] * 2)
    expected_circuit = alphaclops.Circuit([alphaclops.H(q[0]), alphaclops.measure(q[0], key="a"), alphaclops.I(q[1])] * 2)
    alphaclops.testing.assert_same_circuits(
        alphaclops.align_left(alphaclops.merge_operations(circuit, merge_func)), expected_circuit
    )


def test_merge_operations_does_not_merge_measurements_behind_ccos():
    q = alphaclops.LineQubit.range(2)
    measure_op = alphaclops.measure(q[0], key="a")
    cco_op = alphaclops.X(q[1]).with_classical_controls("a")

    def merge_func(op1, op2):
        return alphaclops.I(*op1.qubits) if op1 == measure_op and op2 == measure_op else None

    circuit = alphaclops.Circuit([alphaclops.H(q[0]), measure_op, cco_op] * 2)
    alphaclops.testing.assert_same_circuits(alphaclops.merge_operations(circuit, merge_func), circuit)

    circuit = alphaclops.Circuit([alphaclops.H(q[0]), measure_op, cco_op, measure_op, measure_op] * 2)
    expected_circuit = alphaclops.Circuit([alphaclops.H(q[0]), measure_op, cco_op, alphaclops.I(q[0])] * 2)
    alphaclops.testing.assert_same_circuits(
        alphaclops.align_left(alphaclops.merge_operations(circuit, merge_func)), expected_circuit
    )
