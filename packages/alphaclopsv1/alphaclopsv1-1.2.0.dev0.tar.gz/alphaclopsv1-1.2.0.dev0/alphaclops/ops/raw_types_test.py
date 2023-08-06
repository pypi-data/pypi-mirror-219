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

from typing import AbstractSet, Iterator, Any

import pytest
import numpy as np
import sympy

import alphaclops


class ValidQubit(alphaclops.Qid):
    def __init__(self, name):
        self._name = name

    @property
    def dimension(self):
        return 2

    def _comparison_key(self):
        return self._name

    def __repr__(self):
        return f'ValidQubit({self._name!r})'

    def __str__(self):
        return f'TQ_{self._name!s}'


class ValidQid(alphaclops.Qid):
    def __init__(self, name, dimension):
        self._name = name
        self._dimension = dimension
        self.validate_dimension(dimension)

    @property
    def dimension(self):
        return self._dimension

    def with_dimension(self, dimension):
        return ValidQid(self._name, dimension)

    def _comparison_key(self):
        return self._name


def test_wrapped_qid():
    assert type(ValidQubit('a').with_dimension(3)) is not ValidQubit
    assert type(ValidQubit('a').with_dimension(2)) is ValidQubit
    assert type(ValidQubit('a').with_dimension(5).with_dimension(2)) is ValidQubit
    assert ValidQubit('a').with_dimension(3).with_dimension(4) == ValidQubit('a').with_dimension(4)
    assert ValidQubit('a').with_dimension(3).qubit == ValidQubit('a')
    assert ValidQubit('a').with_dimension(3) == ValidQubit('a').with_dimension(3)
    assert ValidQubit('a').with_dimension(3) < ValidQubit('a').with_dimension(4)
    assert ValidQubit('a').with_dimension(3) < ValidQubit('b').with_dimension(3)
    assert ValidQubit('a').with_dimension(4) < ValidQubit('b').with_dimension(3)

    alphaclops.testing.assert_equivalent_repr(
        ValidQubit('a').with_dimension(3), global_vals={'ValidQubit': ValidQubit}
    )
    assert str(ValidQubit('a').with_dimension(3)) == 'TQ_a (d=3)'

    assert ValidQubit('zz').with_dimension(3)._json_dict_() == {
        'qubit': ValidQubit('zz'),
        'dimension': 3,
    }


def test_qid_dimension():
    assert ValidQubit('a').dimension == 2
    assert ValidQubit('a').with_dimension(3).dimension == 3
    with pytest.raises(ValueError, match='Wrong qid dimension'):
        _ = ValidQubit('a').with_dimension(0)
    with pytest.raises(ValueError, match='Wrong qid dimension'):
        _ = ValidQubit('a').with_dimension(-3)

    assert ValidQid('a', 3).dimension == 3
    assert ValidQid('a', 3).with_dimension(2).dimension == 2
    assert ValidQid('a', 3).with_dimension(4) == ValidQid('a', 4)
    with pytest.raises(ValueError, match='Wrong qid dimension'):
        _ = ValidQid('a', 3).with_dimension(0)
    with pytest.raises(ValueError, match='Wrong qid dimension'):
        _ = ValidQid('a', 3).with_dimension(-3)


class ValiGate(alphaclops.Gate):
    def _num_qubits_(self):
        return 2

    def validate_args(self, qubits):
        if len(qubits) == 1:
            return  # Bypass check for some tests
        super().validate_args(qubits)

    def _has_mixture_(self):
        return True


def test_gate():
    a, b, c = alphaclops.LineQubit.range(3)

    g = ValiGate()
    assert alphaclops.num_qubits(g) == 2

    _ = g.on(a, c)
    with pytest.raises(ValueError, match='Wrong number'):
        _ = g.on(a, c, b)

    _ = g(a)  # Bypassing validate_args
    _ = g(a, c)
    with pytest.raises(ValueError, match='Wrong number'):
        _ = g(c, b, a)
    with pytest.raises(ValueError, match='Wrong shape'):
        _ = g(a, b.with_dimension(3))

    assert g.controlled(0) is g


def test_op():
    a, b, c, d = alphaclops.LineQubit.range(4)
    g = ValiGate()
    op = g(a, b)
    assert op.controlled_by() is op
    controlled_op = op.controlled_by(c, d)
    assert controlled_op.sub_operation == op
    assert controlled_op.controls == (c, d)


def test_op_validate():
    op = alphaclops.X(alphaclops.LineQid(0, 2))
    op2 = alphaclops.CNOT(*alphaclops.LineQid.range(2, dimension=2))
    op.validate_args([alphaclops.LineQid(1, 2)])  # Valid
    op2.validate_args(alphaclops.LineQid.range(1, 3, dimension=2))  # Valid
    with pytest.raises(ValueError, match='Wrong shape'):
        op.validate_args([alphaclops.LineQid(1, 9)])
    with pytest.raises(ValueError, match='Wrong number'):
        op.validate_args([alphaclops.LineQid(1, 2), alphaclops.LineQid(2, 2)])
    with pytest.raises(ValueError, match='Duplicate'):
        op2.validate_args([alphaclops.LineQid(1, 2), alphaclops.LineQid(1, 2)])


def test_disable_op_validation():
    q0, q1 = alphaclops.LineQubit.range(2)
    h_op = alphaclops.H(q0)

    # Fails normally.
    with pytest.raises(ValueError, match='Wrong number'):
        _ = alphaclops.H(q0, q1)
    with pytest.raises(ValueError, match='Wrong number'):
        h_op.validate_args([q0, q1])

    # Passes, skipping validation.
    with alphaclops.with_debug(False):
        op = alphaclops.H(q0, q1)
        assert op.qubits == (q0, q1)
        h_op.validate_args([q0, q1])

    # Fails again when validation is re-enabled.
    with pytest.raises(ValueError, match='Wrong number'):
        _ = alphaclops.H(q0, q1)
    with pytest.raises(ValueError, match='Wrong number'):
        h_op.validate_args([q0, q1])


def test_default_validation_and_inverse():
    class TestGate(alphaclops.Gate):
        def _num_qubits_(self):
            return 2

        def _decompose_(self, qubits):
            a, b = qubits
            yield alphaclops.Z(a)
            yield alphaclops.S(b)
            yield alphaclops.X(a)

        def __eq__(self, other):
            return isinstance(other, TestGate)

        def __repr__(self):
            return 'TestGate()'

    a, b = alphaclops.LineQubit.range(2)

    with pytest.raises(ValueError, match='number of qubits'):
        TestGate().on(a)

    t = TestGate().on(a, b)
    i = t**-1
    assert i**-1 == t
    assert t**-1 == i
    assert alphaclops.decompose(i) == [alphaclops.X(a), alphaclops.S(b) ** -1, alphaclops.Z(a)]
    assert [*i._decompose_()] == [alphaclops.X(a), alphaclops.S(b) ** -1, alphaclops.Z(a)]
    assert [*i.gate._decompose_([a, b])] == [alphaclops.X(a), alphaclops.S(b) ** -1, alphaclops.Z(a)]
    alphaclops.testing.assert_allclose_up_to_global_phase(
        alphaclops.unitary(i), alphaclops.unitary(t).conj().T, atol=1e-8
    )

    alphaclops.testing.assert_implements_consistent_protocols(i, local_vals={'TestGate': TestGate})


def test_default_inverse():
    class TestGate(alphaclops.Gate):
        def _num_qubits_(self):
            return 3

        def _decompose_(self, qubits):
            return (alphaclops.X ** 0.1).on_each(*qubits)

    assert alphaclops.inverse(TestGate(), None) is not None
    alphaclops.testing.assert_has_consistent_qid_shape(alphaclops.inverse(TestGate()))
    alphaclops.testing.assert_has_consistent_qid_shape(
        alphaclops.inverse(TestGate().on(*alphaclops.LineQubit.range(3)))
    )


def test_no_inverse_if_not_unitary():
    class TestGate(alphaclops.Gate):
        def _num_qubits_(self):
            return 1

        def _decompose_(self, qubits):
            return alphaclops.amplitude_damp(0.5).on(qubits[0])

    assert alphaclops.inverse(TestGate(), None) is None


def test_default_qudit_inverse():
    class TestGate(alphaclops.Gate):
        def _qid_shape_(self):
            return (1, 2, 3)

        def _decompose_(self, qubits):
            return (alphaclops.X ** 0.1).on(qubits[1])

    assert alphaclops.qid_shape(alphaclops.inverse(TestGate(), None)) == (1, 2, 3)
    alphaclops.testing.assert_has_consistent_qid_shape(alphaclops.inverse(TestGate()))


@pytest.mark.parametrize(
    'expression, expected_result',
    (
        (alphaclops.X * 2, 2 * alphaclops.X),
        (alphaclops.Y * 2, alphaclops.Y + alphaclops.Y),
        (alphaclops.Z - alphaclops.Z + alphaclops.Z, alphaclops.Z.wrap_in_linear_combination()),
        (1j * alphaclops.S * 1j, -alphaclops.S),
        (alphaclops.CZ * 1, alphaclops.CZ / 1),
        (-alphaclops.CSWAP * 1j, alphaclops.CSWAP / 1j),
        (alphaclops.TOFFOLI * 0.5, alphaclops.TOFFOLI / 2),
    ),
)
def test_gate_algebra(expression, expected_result):
    assert expression == expected_result


def test_gate_shape():
    class ShapeGate(alphaclops.Gate):
        def _qid_shape_(self):
            return (1, 2, 3, 4)

    class QubitGate(alphaclops.Gate):
        def _num_qubits_(self):
            return 3

    class DeprecatedGate(alphaclops.Gate):
        def num_qubits(self):
            return 3

    shape_gate = ShapeGate()
    assert alphaclops.qid_shape(shape_gate) == (1, 2, 3, 4)
    assert alphaclops.num_qubits(shape_gate) == 4
    assert shape_gate.num_qubits() == 4

    qubit_gate = QubitGate()
    assert alphaclops.qid_shape(qubit_gate) == (2, 2, 2)
    assert alphaclops.num_qubits(qubit_gate) == 3
    assert qubit_gate.num_qubits() == 3

    dep_gate = DeprecatedGate()
    assert alphaclops.qid_shape(dep_gate) == (2, 2, 2)
    assert alphaclops.num_qubits(dep_gate) == 3
    assert dep_gate.num_qubits() == 3


def test_gate_shape_protocol():
    """This test is only needed while the `_num_qubits_` and `_qid_shape_`
    methods are implemented as alternatives.  This can be removed once the
    deprecated `num_qubits` method is removed."""

    class NotImplementedGate1(alphaclops.Gate):
        def _num_qubits_(self):
            return NotImplemented

        def _qid_shape_(self):
            return NotImplemented

    class NotImplementedGate2(alphaclops.Gate):
        def _num_qubits_(self):
            return NotImplemented

    class NotImplementedGate3(alphaclops.Gate):
        def _qid_shape_(self):
            return NotImplemented

    class ShapeGate(alphaclops.Gate):
        def _num_qubits_(self):
            return NotImplemented

        def _qid_shape_(self):
            return (1, 2, 3)

    class QubitGate(alphaclops.Gate):
        def _num_qubits_(self):
            return 2

        def _qid_shape_(self):
            return NotImplemented

    with pytest.raises(TypeError, match='returned NotImplemented'):
        alphaclops.qid_shape(NotImplementedGate1())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        alphaclops.num_qubits(NotImplementedGate1())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = NotImplementedGate1().num_qubits()  # Deprecated
    with pytest.raises(TypeError, match='returned NotImplemented'):
        alphaclops.qid_shape(NotImplementedGate2())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        alphaclops.num_qubits(NotImplementedGate2())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = NotImplementedGate2().num_qubits()  # Deprecated
    with pytest.raises(TypeError, match='returned NotImplemented'):
        alphaclops.qid_shape(NotImplementedGate3())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        alphaclops.num_qubits(NotImplementedGate3())
    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = NotImplementedGate3().num_qubits()  # Deprecated
    assert alphaclops.qid_shape(ShapeGate()) == (1, 2, 3)
    assert alphaclops.num_qubits(ShapeGate()) == 3
    assert ShapeGate().num_qubits() == 3  # Deprecated
    assert alphaclops.qid_shape(QubitGate()) == (2, 2)
    assert alphaclops.num_qubits(QubitGate()) == 2
    assert QubitGate().num_qubits() == 2  # Deprecated


def test_operation_shape():
    class FixedQids(alphaclops.Operation):
        def with_qubits(self, *new_qids):
            raise NotImplementedError  # coverage: ignore

    class QubitOp(FixedQids):
        @property
        def qubits(self):
            return alphaclops.LineQubit.range(2)

    class NumQubitOp(FixedQids):
        @property
        def qubits(self):
            return alphaclops.LineQubit.range(3)

        def _num_qubits_(self):
            return 3

    class ShapeOp(FixedQids):
        @property
        def qubits(self):
            return alphaclops.LineQubit.range(4)

        def _qid_shape_(self):
            return (1, 2, 3, 4)

    qubit_op = QubitOp()
    assert len(qubit_op.qubits) == 2
    assert alphaclops.qid_shape(qubit_op) == (2, 2)
    assert alphaclops.num_qubits(qubit_op) == 2

    num_qubit_op = NumQubitOp()
    assert len(num_qubit_op.qubits) == 3
    assert alphaclops.qid_shape(num_qubit_op) == (2, 2, 2)
    assert alphaclops.num_qubits(num_qubit_op) == 3

    shape_op = ShapeOp()
    assert len(shape_op.qubits) == 4
    assert alphaclops.qid_shape(shape_op) == (1, 2, 3, 4)
    assert alphaclops.num_qubits(shape_op) == 4


def test_gate_json_dict():
    g = alphaclops.CSWAP  # not an eigen gate (which has its own _json_dict_)
    assert g._json_dict_() == {}


def test_inverse_composite_diagram_info():
    class Gate(alphaclops.Gate):
        def _decompose_(self, qubits):
            return alphaclops.S.on(qubits[0])

        def num_qubits(self) -> int:
            return 1

    c = alphaclops.inverse(Gate())
    assert alphaclops.circuit_diagram_info(c, default=None) is None

    class Gate2(alphaclops.Gate):
        def _decompose_(self, qubits):
            return alphaclops.S.on(qubits[0])

        def num_qubits(self) -> int:
            return 1

        def _circuit_diagram_info_(self, args):
            return 's!'

    c = alphaclops.inverse(Gate2())
    assert alphaclops.circuit_diagram_info(c) == alphaclops.CircuitDiagramInfo(
        wire_symbols=('s!',), exponent=-1
    )


def test_tagged_operation_equality():
    eq = alphaclops.testing.EqualsTester()
    q1 = alphaclops.TensorCircuit(1, 1)
    op = alphaclops.X(q1)
    op2 = alphaclops.Y(q1)

    eq.add_equality_group(op)
    eq.add_equality_group(op.with_tags('tag1'), alphaclops.TaggedOperation(op, 'tag1'))
    eq.add_equality_group(op2.with_tags('tag1'), alphaclops.TaggedOperation(op2, 'tag1'))
    eq.add_equality_group(op.with_tags('tag2'), alphaclops.TaggedOperation(op, 'tag2'))
    eq.add_equality_group(
        op.with_tags('tag1', 'tag2'),
        op.with_tags('tag1').with_tags('tag2'),
        alphaclops.TaggedOperation(op, 'tag1', 'tag2'),
    )


def test_tagged_operation():
    q1 = alphaclops.TensorCircuit(1, 1)
    q2 = alphaclops.TensorCircuit(2, 2)
    op = alphaclops.X(q1).with_tags('tag1')
    op_repr = "alphaclops.X(alphaclops.TensorCircuit(1, 1))"
    assert repr(op) == f"alphaclops.TaggedOperation({op_repr}, 'tag1')"

    assert op.qubits == (q1,)
    assert op.tags == ('tag1',)
    assert op.gate == alphaclops.X
    assert op.with_qubits(q2) == alphaclops.X(q2).with_tags('tag1')
    assert op.with_qubits(q2).qubits == (q2,)
    assert not alphaclops.is_measurement(op)


def test_with_tags_returns_same_instance_if_possible():
    untagged = alphaclops.X(alphaclops.TensorCircuit(1, 1))
    assert untagged.with_tags() is untagged

    tagged = untagged.with_tags('foo')
    assert tagged.with_tags() is tagged


def test_tagged_measurement():
    assert not alphaclops.is_measurement(alphaclops.global_phase_operation(coefficient=-1.0).with_tags('tag0'))

    a = alphaclops.LineQubit(0)
    op = alphaclops.measure(a, key='m').with_tags('tag')
    assert alphaclops.is_measurement(op)

    remap_op = alphaclops.with_measurement_key_mapping(op, {'m': 'k'})
    assert remap_op.tags == ('tag',)
    assert alphaclops.is_measurement(remap_op)
    assert alphaclops.measurement_key_names(remap_op) == {'k'}
    assert alphaclops.with_measurement_key_mapping(op, {'x': 'k'}) == op


def test_cannot_remap_non_measurement_gate():
    a = alphaclops.LineQubit(0)
    op = alphaclops.X(a).with_tags('tag')

    assert alphaclops.with_measurement_key_mapping(op, {'m': 'k'}) is NotImplemented


def test_circuit_diagram():
    class TaggyTag:
        """Tag with a custom repr function to test circuit diagrams."""

        def __repr__(self):
            return 'TaggyTag()'

    h = alphaclops.H(alphaclops.TensorCircuit(1, 1))
    tagged_h = h.with_tags('tag1')
    non_string_tag_h = h.with_tags(TaggyTag())

    expected = alphaclops.CircuitDiagramInfo(
        wire_symbols=("H['tag1']",),
        exponent=1.0,
        connected=True,
        exponent_qubit_index=None,
        auto_exponent_parens=True,
    )
    args = alphaclops.CircuitDiagramInfoArgs(None, None, None, None, None, False)
    assert alphaclops.circuit_diagram_info(tagged_h) == expected
    assert alphaclops.circuit_diagram_info(tagged_h, args) == alphaclops.circuit_diagram_info(h)

    c = alphaclops.Circuit(tagged_h)
    diagram_with_tags = "(1, 1): ───H['tag1']───"
    diagram_without_tags = "(1, 1): ───H───"
    assert str(alphaclops.Circuit(tagged_h)) == diagram_with_tags
    assert c.to_text_diagram() == diagram_with_tags
    assert c.to_text_diagram(include_tags=False) == diagram_without_tags

    c = alphaclops.Circuit(non_string_tag_h)
    diagram_with_non_string_tag = "(1, 1): ───H[TaggyTag()]───"
    assert c.to_text_diagram() == diagram_with_non_string_tag
    assert c.to_text_diagram(include_tags=False) == diagram_without_tags


def test_circuit_diagram_tagged_global_phase():
    # Tests global phase operation
    q = alphaclops.NamedQubit('a')
    global_phase = alphaclops.global_phase_operation(coefficient=-1.0).with_tags('tag0')

    # Just global phase in a circuit
    assert alphaclops.circuit_diagram_info(global_phase, default='default') == 'default'
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(global_phase), "\n\nglobal phase:   π['tag0']", use_unicode_characters=True
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(global_phase),
        "\n\nglobal phase:   π",
        use_unicode_characters=True,
        include_tags=False,
    )

    expected = alphaclops.CircuitDiagramInfo(
        wire_symbols=(),
        exponent=1.0,
        connected=True,
        exponent_qubit_index=None,
        auto_exponent_parens=True,
    )

    # Operation with no qubits and returns diagram info with no wire symbols
    class NoWireSymbols(alphaclops.GlobalPhaseGate):
        def _circuit_diagram_info_(
            self, args: 'alphaclops.CircuitDiagramInfoArgs'
        ) -> 'alphaclops.CircuitDiagramInfo':
            return expected

    no_wire_symbol_op = NoWireSymbols(coefficient=-1.0)().with_tags('tag0')
    assert alphaclops.circuit_diagram_info(no_wire_symbol_op, default='default') == expected
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(no_wire_symbol_op),
        "\n\nglobal phase:   π['tag0']",
        use_unicode_characters=True,
    )

    # Two global phases in one moment
    tag1 = alphaclops.global_phase_operation(coefficient=1j).with_tags('tag1')
    tag2 = alphaclops.global_phase_operation(coefficient=1j).with_tags('tag2')
    c = alphaclops.Circuit([alphaclops.X(q), tag1, tag2])
    alphaclops.testing.assert_has_diagram(
        c,
        """\
a: ─────────────X───────────────────

global phase:   π['tag1', 'tag2']""",
        use_unicode_characters=True,
        precision=2,
    )

    # Two moments with global phase, one with another tagged gate
    c = alphaclops.Circuit([alphaclops.X(q).with_tags('x_tag'), tag1])
    c.append(alphaclops.Moment([alphaclops.X(q), tag2]))
    alphaclops.testing.assert_has_diagram(
        c,
        """\
a: ─────────────X['x_tag']─────X──────────────

global phase:   0.5π['tag1']   0.5π['tag2']
""",
        use_unicode_characters=True,
        include_tags=True,
    )


def test_circuit_diagram_no_circuit_diagram():
    class NoCircuitDiagram(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 1

        def __repr__(self):
            return 'guess-i-will-repr'

    q = alphaclops.TensorCircuit(1, 1)
    expected = "(1, 1): ───guess-i-will-repr───"
    assert alphaclops.Circuit(NoCircuitDiagram()(q)).to_text_diagram() == expected
    expected = "(1, 1): ───guess-i-will-repr['taggy']───"
    assert alphaclops.Circuit(NoCircuitDiagram()(q).with_tags('taggy')).to_text_diagram() == expected


def test_tagged_operation_forwards_protocols():
    """The results of all protocols applied to an operation with a tag should
    be equivalent to the result without tags.
    """
    q1 = alphaclops.TensorCircuit(1, 1)
    q2 = alphaclops.TensorCircuit(1, 2)
    h = alphaclops.H(q1)
    tag = 'tag1'
    tagged_h = alphaclops.H(q1).with_tags(tag)

    np.testing.assert_equal(alphaclops.unitary(tagged_h), alphaclops.unitary(h))
    assert alphaclops.has_unitary(tagged_h)
    assert alphaclops.decompose(tagged_h) == alphaclops.decompose(h)
    assert [*tagged_h._decompose_()] == alphaclops.decompose(h)
    assert alphaclops.pauli_expansion(tagged_h) == alphaclops.pauli_expansion(h)
    assert alphaclops.equal_up_to_global_phase(h, tagged_h)
    assert np.isclose(alphaclops.kraus(h), alphaclops.kraus(tagged_h)).all()

    assert alphaclops.measurement_key_name(alphaclops.measure(q1, key='blah').with_tags(tag)) == 'blah'
    assert alphaclops.measurement_key_obj(
        alphaclops.measure(q1, key='blah').with_tags(tag)
    ) == alphaclops.MeasurementKey('blah')

    parameterized_op = alphaclops.XPowGate(exponent=sympy.Symbol('t'))(q1).with_tags(tag)
    assert alphaclops.is_parameterized(parameterized_op)
    resolver = alphaclops.study.ParamResolver({'t': 0.25})
    assert alphaclops.resolve_parameters(parameterized_op, resolver) == alphaclops.XPowGate(exponent=0.25)(
        q1
    ).with_tags(tag)
    assert alphaclops.resolve_parameters_once(parameterized_op, resolver) == alphaclops.XPowGate(exponent=0.25)(
        q1
    ).with_tags(tag)
    assert parameterized_op._unitary_() is NotImplemented
    assert parameterized_op._mixture_() is NotImplemented
    assert parameterized_op._kraus_() is NotImplemented

    y = alphaclops.Y(q1)
    tagged_y = alphaclops.Y(q1).with_tags(tag)
    assert tagged_y ** 0.5 == alphaclops.YPowGate(exponent=0.5)(q1)
    assert tagged_y * 2 == (y * 2)
    assert 3 * tagged_y == (3 * y)
    assert alphaclops.phase_by(y, 0.125, 0) == alphaclops.phase_by(tagged_y, 0.125, 0)
    controlled_y = tagged_y.controlled_by(q2)
    assert controlled_y.qubits == (q2, q1)
    assert isinstance(controlled_y, alphaclops.Operation)
    assert not isinstance(controlled_y, alphaclops.TaggedOperation)
    classically_controlled_y = tagged_y.with_classical_controls("a")
    assert classically_controlled_y == y.with_classical_controls("a")
    assert isinstance(classically_controlled_y, alphaclops.Operation)
    assert not isinstance(classically_controlled_y, alphaclops.TaggedOperation)

    clifford_x = alphaclops.SingleQubitCliffordGate.X(q1)
    tagged_x = alphaclops.SingleQubitCliffordGate.X(q1).with_tags(tag)
    assert alphaclops.commutes(clifford_x, clifford_x)
    assert alphaclops.commutes(tagged_x, clifford_x)
    assert alphaclops.commutes(clifford_x, tagged_x)
    assert alphaclops.commutes(tagged_x, tagged_x)

    assert alphaclops.trace_distance_bound(y ** 0.001) == alphaclops.trace_distance_bound(
        (y**0.001).with_tags(tag)
    )

    flip = alphaclops.bit_flip(0.5)(q1)
    tagged_flip = alphaclops.bit_flip(0.5)(q1).with_tags(tag)
    assert alphaclops.has_mixture(tagged_flip)
    assert alphaclops.has_kraus(tagged_flip)

    flip_mixture = alphaclops.mixture(flip)
    tagged_mixture = alphaclops.mixture(tagged_flip)
    assert len(tagged_mixture) == 2
    assert len(tagged_mixture[0]) == 2
    assert len(tagged_mixture[1]) == 2
    assert tagged_mixture[0][0] == flip_mixture[0][0]
    assert np.isclose(tagged_mixture[0][1], flip_mixture[0][1]).all()
    assert tagged_mixture[1][0] == flip_mixture[1][0]
    assert np.isclose(tagged_mixture[1][1], flip_mixture[1][1]).all()

    qubit_map = {q1: 'q1'}
    qasm_args = alphaclops.QasmArgs(qubit_id_map=qubit_map)
    assert alphaclops.qasm(h, args=qasm_args) == alphaclops.qasm(tagged_h, args=qasm_args)

    alphaclops.testing.assert_has_consistent_apply_unitary(tagged_h)


class ParameterizableTag:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def _is_parameterized_(self) -> bool:
        return alphaclops.is_parameterized(self.value)

    def _parameter_names_(self) -> AbstractSet[str]:
        return alphaclops.parameter_names(self.value)

    def _resolve_parameters_(
        self, resolver: 'alphaclops.ParamResolver', recursive: bool
    ) -> 'ParameterizableTag':
        return ParameterizableTag(alphaclops.resolve_parameters(self.value, resolver, recursive))


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_tagged_operation_resolves_parameterized_tags(resolve_fn):
    q = alphaclops.TensorCircuit(0, 0)
    tag = ParameterizableTag(sympy.Symbol('t'))
    assert alphaclops.is_parameterized(tag)
    assert alphaclops.parameter_names(tag) == {'t'}
    op = alphaclops.Z(q).with_tags(tag)
    assert alphaclops.is_parameterized(op)
    assert alphaclops.parameter_names(op) == {'t'}
    resolved_op = resolve_fn(op, {'t': 10})
    assert resolved_op == alphaclops.Z(q).with_tags(ParameterizableTag(10))
    assert not alphaclops.is_parameterized(resolved_op)
    assert alphaclops.parameter_names(resolved_op) == set()


def test_inverse_composite_standards():
    @alphaclops.value_equality
    class Gate(alphaclops.Gate):
        def __init__(self, param: 'alphaclops.TParamVal'):
            self._param = param

        def _decompose_(self, qubits):
            return alphaclops.S.on(qubits[0])

        def num_qubits(self) -> int:
            return 1

        def _has_unitary_(self):
            return True

        def _value_equality_values_(self):
            return (self._param,)

        def _parameter_names_(self) -> AbstractSet[str]:
            return alphaclops.parameter_names(self._param)

        def _is_parameterized_(self) -> bool:
            return alphaclops.is_parameterized(self._param)

        def _resolve_parameters_(self, resolver: 'alphaclops.ParamResolver', recursive: bool) -> 'Gate':
            return Gate(alphaclops.resolve_parameters(self._param, resolver, recursive))

        def __repr__(self):
            return f'C({self._param})'

    a = sympy.Symbol("a")
    g = alphaclops.inverse(Gate(a))
    assert alphaclops.is_parameterized(g)
    assert alphaclops.parameter_names(g) == {'a'}
    assert alphaclops.resolve_parameters(g, {a: 0}) == Gate(0) ** -1
    alphaclops.testing.assert_implements_consistent_protocols(g, global_vals={'C': Gate, 'a': a})


def test_tagged_act_on():
    class YesActOn(alphaclops.Gate):
        def _num_qubits_(self) -> int:
            return 1

        def _act_on_(self, sim_state, qubits):
            return True

    class NoActOn(alphaclops.Gate):
        def _num_qubits_(self) -> int:
            return 1

        def _act_on_(self, sim_state, qubits):
            return NotImplemented

    class MissingActOn(alphaclops.Operation):
        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

        @property
        def qubits(self):
            pass

    q = alphaclops.LineQubit(1)
    from alphaclops.protocols.act_on_protocol_test import DummySimulationState

    args = DummySimulationState()
    alphaclops.act_on(YesActOn()(q).with_tags("test"), args)
    with pytest.raises(TypeError, match="Failed to act"):
        alphaclops.act_on(NoActOn()(q).with_tags("test"), args)
    with pytest.raises(TypeError, match="Failed to act"):
        alphaclops.act_on(MissingActOn().with_tags("test"), args)


def test_single_qubit_gate_validates_on_each():
    class Dummy(alphaclops.testing.SingleQubitGate):
        def matrix(self):
            pass

    g = Dummy()
    assert g.num_qubits() == 1

    test_qubits = [alphaclops.NamedQubit(str(i)) for i in range(3)]

    _ = g.on_each(*test_qubits)
    _ = g.on_each(test_qubits)

    test_non_qubits = [str(i) for i in range(3)]
    with pytest.raises(ValueError):
        _ = g.on_each(*test_non_qubits)

    with alphaclops.with_debug(False):
        assert g.on_each(*test_non_qubits)[0].qubits == ('0',)

    with pytest.raises(ValueError):
        _ = g.on_each(*test_non_qubits)


def test_on_each():
    class CustomGate(alphaclops.testing.SingleQubitGate):
        pass

    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = CustomGate()

    assert c.on_each() == []
    assert c.on_each(a) == [c(a)]
    assert c.on_each(a, b) == [c(a), c(b)]
    assert c.on_each(b, a) == [c(b), c(a)]

    assert c.on_each([]) == []
    assert c.on_each([a]) == [c(a)]
    assert c.on_each([a, b]) == [c(a), c(b)]
    assert c.on_each([b, a]) == [c(b), c(a)]
    assert c.on_each([a, [b, a], b]) == [c(a), c(b), c(a), c(b)]

    with pytest.raises(ValueError):
        c.on_each('abcd')
    with pytest.raises(ValueError):
        c.on_each(['abcd'])
    with pytest.raises(ValueError):
        c.on_each([a, 'abcd'])

    qubit_iterator = (q for q in [a, b, a, b])
    assert isinstance(qubit_iterator, Iterator)
    assert c.on_each(qubit_iterator) == [c(a), c(b), c(a), c(b)]


def test_on_each_two_qubits():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    g = alphaclops.testing.TwoQubitGate()

    assert g.on_each([]) == []
    assert g.on_each([(a, b)]) == [g(a, b)]
    assert g.on_each([[a, b]]) == [g(a, b)]
    assert g.on_each([(b, a)]) == [g(b, a)]
    assert g.on_each([(a, b), (b, a)]) == [g(a, b), g(b, a)]
    assert g.on_each(zip([a, b], [b, a])) == [g(a, b), g(b, a)]
    assert g.on_each() == []
    assert g.on_each((b, a)) == [g(b, a)]
    assert g.on_each((a, b), (a, b)) == [g(a, b), g(a, b)]
    assert g.on_each(*zip([a, b], [b, a])) == [g(a, b), g(b, a)]
    with pytest.raises(TypeError, match='object is not iterable'):
        g.on_each(a)
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        g.on_each(a, b)
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        g.on_each([12])
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        g.on_each([(a, b), 12])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([(a, b), [(a, b)]])
    with pytest.raises(ValueError, match='Expected 2 qubits'):
        g.on_each([()])
    with pytest.raises(ValueError, match='Expected 2 qubits'):
        g.on_each([(a,)])
    with pytest.raises(ValueError, match='Expected 2 qubits'):
        g.on_each([(a, b, a)])

    with alphaclops.with_debug(False):
        assert g.on_each([(a, b, a)])[0].qubits == (a, b, a)

    with pytest.raises(ValueError, match='Expected 2 qubits'):
        g.on_each(zip([a, a]))
    with pytest.raises(ValueError, match='Expected 2 qubits'):
        g.on_each(zip([a, a], [b, b], [a, a]))
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each('ab')
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each(('ab',))
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([('ab',)])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([(a, 'ab')])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([(a, 'b')])

    qubit_iterator = (qs for qs in [[a, b], [a, b]])
    assert isinstance(qubit_iterator, Iterator)
    assert g.on_each(qubit_iterator) == [g(a, b), g(a, b)]


def test_on_each_three_qubits():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')
    g = alphaclops.testing.ThreeQubitGate()

    assert g.on_each([]) == []
    assert g.on_each([(a, b, c)]) == [g(a, b, c)]
    assert g.on_each([[a, b, c]]) == [g(a, b, c)]
    assert g.on_each([(c, b, a)]) == [g(c, b, a)]
    assert g.on_each([(a, b, c), (c, b, a)]) == [g(a, b, c), g(c, b, a)]
    assert g.on_each(zip([a, c], [b, b], [c, a])) == [g(a, b, c), g(c, b, a)]
    assert g.on_each() == []
    assert g.on_each((c, b, a)) == [g(c, b, a)]
    assert g.on_each((a, b, c), (c, b, a)) == [g(a, b, c), g(c, b, a)]
    assert g.on_each(*zip([a, c], [b, b], [c, a])) == [g(a, b, c), g(c, b, a)]
    with pytest.raises(TypeError, match='object is not iterable'):
        g.on_each(a)
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        g.on_each(a, b, c)
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        g.on_each([12])
    with pytest.raises(ValueError, match='Inputs to multi-qubit gates must be Sequence'):
        g.on_each([(a, b, c), 12])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([(a, b, c), [(a, b, c)]])
    with pytest.raises(ValueError, match='Expected 3 qubits'):
        g.on_each([(a,)])
    with pytest.raises(ValueError, match='Expected 3 qubits'):
        g.on_each([(a, b)])
    with pytest.raises(ValueError, match='Expected 3 qubits'):
        g.on_each([(a, b, c, a)])
    with pytest.raises(ValueError, match='Expected 3 qubits'):
        g.on_each(zip([a, a], [b, b]))
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each('abc')
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each(('abc',))
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([('abc',)])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([(a, 'abc')])
    with pytest.raises(ValueError, match='All values in sequence should be Qids'):
        g.on_each([(a, 'bc')])

    qubit_iterator = (qs for qs in [[a, b, c], [a, b, c]])
    assert isinstance(qubit_iterator, Iterator)
    assert g.on_each(qubit_iterator) == [g(a, b, c), g(a, b, c)]


def test_on_each_iterable_qid():
    class QidIter(alphaclops.Qid):
        @property
        def dimension(self) -> int:
            return 2

        def _comparison_key(self) -> Any:
            return 1

        def __iter__(self):
            raise NotImplementedError()

    assert alphaclops.H.on_each(QidIter())[0] == alphaclops.H.on(QidIter())


@pytest.mark.parametrize(
    'op', [alphaclops.X(alphaclops.NamedQubit("q")), alphaclops.X(alphaclops.NamedQubit("q")).with_tags("tagged_op")]
)
def test_with_methods_return_self_on_empty_conditions(op):
    assert op is op.with_tags(*[])
    assert op is op.with_classical_controls(*[])
    assert op is op.controlled_by(*[])
