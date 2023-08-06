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
import pytest

import alphaclops


def test_stratified_circuit_classifier_types():
    a, b, c, d = alphaclops.LineQubit.range(4)

    circuit = alphaclops.Circuit(alphaclops.Moment([alphaclops.X(a), alphaclops.Y(b), alphaclops.X(c) ** 0.5, alphaclops.X(d)]))

    gate_result = alphaclops.stratified_circuit(circuit, categories=[alphaclops.X])
    alphaclops.testing.assert_same_circuits(
        gate_result,
        alphaclops.Circuit(
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(d)]), alphaclops.Moment([alphaclops.Y(b), alphaclops.X(c) ** 0.5])
        ),
    )

    gate_type_result = alphaclops.stratified_circuit(circuit, categories=[alphaclops.XPowGate])
    alphaclops.testing.assert_same_circuits(
        gate_type_result,
        alphaclops.Circuit(
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(c) ** 0.5, alphaclops.X(d)]), alphaclops.Moment([alphaclops.Y(b)])
        ),
    )

    operation_result = alphaclops.stratified_circuit(circuit, categories=[alphaclops.X(a)])
    alphaclops.testing.assert_same_circuits(
        operation_result,
        alphaclops.Circuit(
            alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.Y(b), alphaclops.X(c) ** 0.5, alphaclops.X(d)])
        ),
    )

    operation_type_result = alphaclops.stratified_circuit(circuit, categories=[alphaclops.GateOperation])
    alphaclops.testing.assert_same_circuits(
        operation_type_result,
        alphaclops.Circuit(alphaclops.Moment([alphaclops.X(a), alphaclops.Y(b), alphaclops.X(c) ** 0.5, alphaclops.X(d)])),
    )

    predicate_result = alphaclops.stratified_circuit(circuit, categories=[lambda op: op.qubits == (b,)])
    alphaclops.testing.assert_same_circuits(
        predicate_result,
        alphaclops.Circuit(
            alphaclops.Moment([alphaclops.Y(b)]), alphaclops.Moment([alphaclops.X(a), alphaclops.X(d), alphaclops.X(c) ** 0.5])
        ),
    )

    with pytest.raises(TypeError, match='Unrecognized'):
        _ = alphaclops.stratified_circuit(circuit, categories=['unknown'])


def test_overlapping_categories():
    a, b, c, d = alphaclops.LineQubit.range(4)

    result = alphaclops.stratified_circuit(
        alphaclops.Circuit(
            alphaclops.Moment([alphaclops.X(a), alphaclops.Y(b), alphaclops.Z(c)]),
            alphaclops.Moment([alphaclops.CNOT(a, b)]),
            alphaclops.Moment([alphaclops.CNOT(c, d)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.Y(b), alphaclops.Z(c)]),
        ),
        categories=[
            lambda op: len(op.qubits) == 1 and not isinstance(op.gate, alphaclops.XPowGate),
            lambda op: len(op.qubits) == 1 and not isinstance(op.gate, alphaclops.ZPowGate),
        ],
    )

    alphaclops.testing.assert_same_circuits(
        result,
        alphaclops.Circuit(
            alphaclops.Moment([alphaclops.Y(b), alphaclops.Z(c)]),
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.CNOT(a, b), alphaclops.CNOT(c, d)]),
            alphaclops.Moment([alphaclops.Y(b), alphaclops.Z(c)]),
            alphaclops.Moment([alphaclops.X(a)]),
        ),
    )


def test_empty():
    a = alphaclops.LineQubit(0)
    assert alphaclops.stratified_circuit(alphaclops.Circuit(), categories=[]) == alphaclops.Circuit()
    assert alphaclops.stratified_circuit(alphaclops.Circuit(), categories=[alphaclops.X]) == alphaclops.Circuit()
    assert alphaclops.stratified_circuit(alphaclops.Circuit(alphaclops.X(a)), categories=[]) == alphaclops.Circuit(
        alphaclops.X(a)
    )


def test_greedy_merging():
    """Tests a tricky situation where the algorithm of "Merge single-qubit
    gates, greedily align single-qubit then 2-qubit operations" doesn't work.
    Our algorithm succeeds because we also run it in reverse order."""
    q1, q2, q3, q4 = alphaclops.LineQubit.range(4)
    input_circuit = alphaclops.Circuit(
        alphaclops.Moment([alphaclops.X(q1)]),
        alphaclops.Moment([alphaclops.SWAP(q1, q2), alphaclops.SWAP(q3, q4)]),
        alphaclops.Moment([alphaclops.X(q3)]),
        alphaclops.Moment([alphaclops.SWAP(q3, q4)]),
    )
    expected = alphaclops.Circuit(
        alphaclops.Moment([alphaclops.SWAP(q3, q4)]),
        alphaclops.Moment([alphaclops.X(q1), alphaclops.X(q3)]),
        alphaclops.Moment([alphaclops.SWAP(q1, q2), alphaclops.SWAP(q3, q4)]),
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.stratified_circuit(input_circuit, categories=[alphaclops.X]), expected
    )


def test_greedy_merging_reverse():
    """Same as the above test, except that the aligning is done in reverse."""
    q1, q2, q3, q4 = alphaclops.LineQubit.range(4)
    input_circuit = alphaclops.Circuit(
        alphaclops.Moment([alphaclops.SWAP(q1, q2), alphaclops.SWAP(q3, q4)]),
        alphaclops.Moment([alphaclops.X(q4)]),
        alphaclops.Moment([alphaclops.SWAP(q3, q4)]),
        alphaclops.Moment([alphaclops.X(q1)]),
    )
    expected = alphaclops.Circuit(
        alphaclops.Moment([alphaclops.SWAP(q1, q2), alphaclops.SWAP(q3, q4)]),
        alphaclops.Moment([alphaclops.X(q1), alphaclops.X(q4)]),
        alphaclops.Moment([alphaclops.SWAP(q3, q4)]),
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.stratified_circuit(input_circuit, categories=[alphaclops.X]), expected
    )


def test_complex_circuit():
    """Tests that a complex circuit is correctly optimized."""
    q1, q2, q3, q4, q5 = alphaclops.LineQubit.range(5)
    input_circuit = alphaclops.Circuit(
        alphaclops.Moment([alphaclops.X(q1), alphaclops.ISWAP(q2, q3), alphaclops.Z(q5)]),
        alphaclops.Moment([alphaclops.X(q1), alphaclops.ISWAP(q4, q5)]),
        alphaclops.Moment([alphaclops.ISWAP(q1, q2), alphaclops.X(q4)]),
    )
    expected = alphaclops.Circuit(
        alphaclops.Moment([alphaclops.X(q1)]),
        alphaclops.Moment([alphaclops.Z(q5)]),
        alphaclops.Moment([alphaclops.ISWAP(q2, q3), alphaclops.ISWAP(q4, q5)]),
        alphaclops.Moment([alphaclops.X(q1), alphaclops.X(q4)]),
        alphaclops.Moment([alphaclops.ISWAP(q1, q2)]),
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.stratified_circuit(input_circuit, categories=[alphaclops.X, alphaclops.Z]), expected
    )


def test_complex_circuit_deep():
    q = alphaclops.LineQubit.range(5)
    c_nested = alphaclops.FrozenCircuit(
        alphaclops.Moment(
            alphaclops.X(q[0]).with_tags("ignore"),
            alphaclops.ISWAP(q[1], q[2]).with_tags("ignore"),
            alphaclops.Z(q[4]),
        ),
        alphaclops.Moment(alphaclops.Z(q[1]), alphaclops.ISWAP(q[3], q[4])),
        alphaclops.Moment(alphaclops.ISWAP(q[0], q[1]), alphaclops.X(q[3])),
        alphaclops.Moment(alphaclops.X.on_each(q[0])),
    )
    c_nested_stratified = alphaclops.FrozenCircuit(
        alphaclops.Moment(alphaclops.X(q[0]).with_tags("ignore"), alphaclops.ISWAP(q[1], q[2]).with_tags("ignore")),
        alphaclops.Moment(alphaclops.Z.on_each(q[1], q[4])),
        alphaclops.Moment(alphaclops.ISWAP(*q[:2]), alphaclops.ISWAP(*q[3:])),
        alphaclops.Moment(alphaclops.X.on_each(q[0], q[3])),
    )
    c_orig = alphaclops.Circuit(
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(5).with_tags("ignore"),
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(6).with_tags("preserve_tag"),
        c_nested,
    )
    c_expected = alphaclops.Circuit(
        c_nested_stratified,
        alphaclops.CircuitOperation(c_nested).repeat(5).with_tags("ignore"),
        c_nested_stratified,
        alphaclops.CircuitOperation(c_nested_stratified).repeat(6).with_tags("preserve_tag"),
        c_nested_stratified,
    )
    context = alphaclops.TransformerContext(tags_to_ignore=["ignore"], deep=True)
    c_stratified = alphaclops.stratified_circuit(c_orig, context=context, categories=[alphaclops.X, alphaclops.Z])
    alphaclops.testing.assert_same_circuits(c_stratified, c_expected)


def test_no_categories_earliest_insert():
    q1, q2, q3, q4, q5 = alphaclops.LineQubit.range(5)
    input_circuit = alphaclops.Circuit(
        alphaclops.Moment([alphaclops.ISWAP(q2, q3)]),
        alphaclops.Moment([alphaclops.X(q1), alphaclops.ISWAP(q4, q5)]),
        alphaclops.Moment([alphaclops.ISWAP(q1, q2), alphaclops.X(q4)]),
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.Circuit(input_circuit.all_operations()), alphaclops.stratified_circuit(input_circuit)
    )


def test_stratify_respects_no_compile_operations():
    q1, q2, q3, q4, q5 = alphaclops.LineQubit.range(5)
    input_circuit = alphaclops.Circuit(
        alphaclops.Moment(
            [
                alphaclops.X(q1).with_tags("nocompile"),
                alphaclops.ISWAP(q2, q3).with_tags("nocompile"),
                alphaclops.Z(q5),
            ]
        ),
        alphaclops.Moment([alphaclops.X(q1), alphaclops.ISWAP(q4, q5)]),
        alphaclops.Moment([alphaclops.ISWAP(q1, q2), alphaclops.X(q4)]),
    )
    expected = alphaclops.Circuit(
        [
            alphaclops.Moment(alphaclops.Z(alphaclops.LineQubit(4))),
            alphaclops.Moment(alphaclops.ISWAP(alphaclops.LineQubit(3), alphaclops.LineQubit(4))),
            alphaclops.Moment(
                alphaclops.TaggedOperation(alphaclops.X(alphaclops.LineQubit(0)), 'nocompile'),
                alphaclops.TaggedOperation(alphaclops.ISWAP(alphaclops.LineQubit(1), alphaclops.LineQubit(2)), 'nocompile'),
            ),
            alphaclops.Moment(alphaclops.X(alphaclops.LineQubit(0)), alphaclops.X(alphaclops.LineQubit(3))),
            alphaclops.Moment(alphaclops.ISWAP(alphaclops.LineQubit(0), alphaclops.LineQubit(1))),
        ]
    )
    alphaclops.testing.assert_has_diagram(
        input_circuit,
        '''
0: ───X['nocompile']───────X───────iSwap───
                                   │
1: ───iSwap['nocompile']───────────iSwap───
      │
2: ───iSwap────────────────────────────────

3: ────────────────────────iSwap───X───────
                           │
4: ───Z────────────────────iSwap───────────
''',
    )
    alphaclops.testing.assert_has_diagram(
        expected,
        '''
0: ───────────────X['nocompile']───────X───iSwap───
                                           │
1: ───────────────iSwap['nocompile']───────iSwap───
                  │
2: ───────────────iSwap────────────────────────────

3: ───────iSwap────────────────────────X───────────
          │
4: ───Z───iSwap────────────────────────────────────
''',
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.stratified_circuit(
            input_circuit,
            categories=[alphaclops.X, alphaclops.Z],
            context=alphaclops.TransformerContext(tags_to_ignore=("nocompile",)),
        ),
        expected,
    )


def test_does_not_move_ccos_behind_measurement():
    q = alphaclops.LineQubit.range(3)
    c_orig = alphaclops.Circuit(
        alphaclops.measure(q[0], key='m'),
        alphaclops.X(q[1]).with_classical_controls('m'),
        alphaclops.Moment(alphaclops.X.on_each(q[1], q[2])),
    )
    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───M───────────
      ║
1: ───╫───X───X───
      ║   ║
2: ───╫───╫───X───
      ║   ║
m: ═══@═══^═══════
''',
    )
    c_out = alphaclops.stratified_circuit(
        c_orig, categories=[alphaclops.GateOperation, alphaclops.ClassicallyControlledOperation]
    )
    alphaclops.testing.assert_has_diagram(
        c_out,
        '''
      ┌──┐
0: ────M─────────────
       ║
1: ────╫─────X───X───
       ║     ║
2: ────╫X────╫───────
       ║     ║
m: ════@═════^═══════
      └──┘
''',
    )


def test_heterogeneous_circuit():
    """Tests that a circuit that is very heterogeneous is correctly optimized"""
    q1, q2, q3, q4, q5, q6 = alphaclops.LineQubit.range(6)
    input_circuit = alphaclops.Circuit(
        alphaclops.Moment([alphaclops.X(q1), alphaclops.X(q2), alphaclops.ISWAP(q3, q4), alphaclops.ISWAP(q5, q6)]),
        alphaclops.Moment([alphaclops.ISWAP(q1, q2), alphaclops.ISWAP(q3, q4), alphaclops.X(q5), alphaclops.X(q6)]),
        alphaclops.Moment([alphaclops.X(q1), alphaclops.Z(q2), alphaclops.X(q3), alphaclops.Z(q4), alphaclops.X(q5), alphaclops.Z(q6)]),
    )
    expected = alphaclops.Circuit(
        alphaclops.Moment([alphaclops.ISWAP(q3, q4), alphaclops.ISWAP(q5, q6)]),
        alphaclops.Moment([alphaclops.X(q1), alphaclops.X(q2), alphaclops.X(q5), alphaclops.X(q6)]),
        alphaclops.Moment([alphaclops.ISWAP(q1, q2), alphaclops.ISWAP(q3, q4)]),
        alphaclops.Moment([alphaclops.Z(q2), alphaclops.Z(q4), alphaclops.Z(q6)]),
        alphaclops.Moment([alphaclops.X(q1), alphaclops.X(q3), alphaclops.X(q5)]),
    )

    alphaclops.testing.assert_same_circuits(
        alphaclops.stratified_circuit(input_circuit, categories=[alphaclops.X, alphaclops.Z]), expected
    )


def test_surface_code_cycle_stratifies_without_growing():
    g = alphaclops.TensorCircuit
    circuit = alphaclops.Circuit(
        alphaclops.H(g(9, 11)),
        alphaclops.H(g(11, 12)),
        alphaclops.H(g(12, 9)),
        alphaclops.H(g(9, 8)),
        alphaclops.H(g(8, 11)),
        alphaclops.H(g(11, 9)),
        alphaclops.H(g(10, 9)),
        alphaclops.H(g(10, 8)),
        alphaclops.H(g(11, 10)),
        alphaclops.H(g(12, 10)),
        alphaclops.H(g(9, 9)),
        alphaclops.H(g(9, 10)),
        alphaclops.H(g(10, 11)),
        alphaclops.CZ(g(10, 9), g(9, 9)),
        alphaclops.CZ(g(10, 11), g(9, 11)),
        alphaclops.CZ(g(9, 10), g(8, 10)),
        alphaclops.CZ(g(11, 10), g(10, 10)),
        alphaclops.CZ(g(12, 9), g(11, 9)),
        alphaclops.CZ(g(11, 12), g(10, 12)),
        alphaclops.H(g(9, 11)),
        alphaclops.H(g(9, 9)),
        alphaclops.H(g(10, 10)),
        alphaclops.H(g(11, 9)),
        alphaclops.H(g(10, 12)),
        alphaclops.H(g(8, 10)),
        alphaclops.CZ(g(11, 10), g(11, 11)),
        alphaclops.CZ(g(10, 9), g(10, 8)),
        alphaclops.CZ(g(12, 9), g(12, 10)),
        alphaclops.CZ(g(10, 11), g(10, 10)),
        alphaclops.CZ(g(9, 8), g(9, 9)),
        alphaclops.CZ(g(9, 10), g(9, 11)),
        alphaclops.CZ(g(8, 11), g(8, 10)),
        alphaclops.CZ(g(11, 10), g(11, 9)),
        alphaclops.CZ(g(11, 12), g(11, 11)),
        alphaclops.H(g(10, 8)),
        alphaclops.H(g(12, 10)),
        alphaclops.H(g(12, 9)),
        alphaclops.CZ(g(9, 10), g(9, 9)),
        alphaclops.CZ(g(10, 9), g(10, 10)),
        alphaclops.CZ(g(10, 11), g(10, 12)),
        alphaclops.H(g(11, 11)),
        alphaclops.H(g(9, 11)),
        alphaclops.H(g(11, 9)),
        alphaclops.CZ(g(9, 8), g(10, 8)),
        alphaclops.CZ(g(11, 10), g(12, 10)),
        alphaclops.H(g(11, 12)),
        alphaclops.H(g(8, 10)),
        alphaclops.H(g(10, 10)),
        alphaclops.CZ(g(8, 11), g(9, 11)),
        alphaclops.CZ(g(10, 9), g(11, 9)),
        alphaclops.CZ(g(10, 11), g(11, 11)),
        alphaclops.H(g(9, 8)),
        alphaclops.H(g(10, 12)),
        alphaclops.H(g(11, 10)),
        alphaclops.CZ(g(9, 10), g(10, 10)),
        alphaclops.H(g(11, 11)),
        alphaclops.H(g(9, 11)),
        alphaclops.H(g(8, 11)),
        alphaclops.H(g(11, 9)),
        alphaclops.H(g(10, 9)),
        alphaclops.H(g(10, 11)),
        alphaclops.H(g(9, 10)),
    )
    assert len(circuit) == 8
    stratified = alphaclops.stratified_circuit(circuit, categories=[alphaclops.H, alphaclops.CZ])
    # Ideally, this would not grow at all, but for now the algorithm has it
    # grow to a 9. Note that this optimizer uses a fairly simple algorithm
    # that is known not to be optimal - optimal stratification is a CSP
    # problem with high dimensionality that quickly becomes intractable. See
    # https://github.com/quantumlib/alphaclops/pull/2772/ for some discussion on
    # this, as well as a more optimal but much more complex and slow solution.
    assert len(stratified) == 9


def test_unclassified_ops():
    op = alphaclops.X(alphaclops.q(0))
    classifiers = []
    with pytest.raises(ValueError, match='not identified by any classifier'):
        alphaclops.transformers.stratify._get_op_class(op, classifiers)
