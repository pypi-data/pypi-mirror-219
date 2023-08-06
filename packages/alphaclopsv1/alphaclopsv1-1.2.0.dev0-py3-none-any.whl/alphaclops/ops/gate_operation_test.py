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
import collections.abc
import pathlib

import numpy as np
import pytest
import sympy

import alphaclops
import alphaclops.testing


def test_gate_operation_init():
    q = alphaclops.NamedQubit('q')
    g = alphaclops.testing.SingleQubitGate()
    v = alphaclops.GateOperation(g, (q,))
    assert v.gate == g
    assert v.qubits == (q,)


def test_invalid_gate_operation():
    three_qubit_gate = alphaclops.testing.ThreeQubitGate()
    single_qubit = [alphaclops.TensorCircuit(0, 0)]
    with pytest.raises(ValueError, match="number of qubits"):
        alphaclops.GateOperation(three_qubit_gate, single_qubit)


def test_immutable():
    a, b = alphaclops.LineQubit.range(2)
    op = alphaclops.X(a)

    # Match one of two strings. The second one is message returned since python 3.11.
    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|"
        "(property 'gate' of 'SingleQubitPauliStringGateOperation' object has no setter)",
    ):
        op.gate = alphaclops.Y

    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|"
        "(property 'qubits' of 'SingleQubitPauliStringGateOperation' object has no setter)",
    ):
        op.qubits = [b]


def test_gate_operation_eq():
    g1 = alphaclops.testing.SingleQubitGate()
    g2 = alphaclops.testing.SingleQubitGate()
    g3 = alphaclops.testing.TwoQubitGate()
    r1 = [alphaclops.NamedQubit('r1')]
    r2 = [alphaclops.NamedQubit('r2')]
    r12 = r1 + r2
    r21 = r2 + r1

    eq = alphaclops.testing.EqualsTester()
    eq.make_equality_group(lambda: alphaclops.GateOperation(g1, r1))
    eq.make_equality_group(lambda: alphaclops.GateOperation(g2, r1))
    eq.make_equality_group(lambda: alphaclops.GateOperation(g1, r2))
    eq.make_equality_group(lambda: alphaclops.GateOperation(g3, r12))
    eq.make_equality_group(lambda: alphaclops.GateOperation(g3, r21))
    eq.add_equality_group(alphaclops.GateOperation(alphaclops.CZ, r21), alphaclops.GateOperation(alphaclops.CZ, r12))

    @alphaclops.value_equality
    class PairGate(alphaclops.Gate, alphaclops.InterchangeableQubitsGate):
        """Interchangeable subsets."""

        def __init__(self, num_qubits):
            self._num_qubits = num_qubits

        def num_qubits(self) -> int:
            return self._num_qubits

        def qubit_index_to_equivalence_group_key(self, index: int):
            return index // 2

        def _value_equality_values_(self):
            return (self.num_qubits(),)

    def p(*q):
        return PairGate(len(q)).on(*q)

    a0, a1, b0, b1, c0 = alphaclops.LineQubit.range(5)
    eq.add_equality_group(p(a0, a1, b0, b1), p(a1, a0, b1, b0))
    eq.add_equality_group(p(b0, b1, a0, a1))
    eq.add_equality_group(p(a0, a1, b0, b1, c0), p(a1, a0, b1, b0, c0))
    eq.add_equality_group(p(a0, b0, a1, b1, c0))
    eq.add_equality_group(p(a0, c0, b0, b1, a1))
    eq.add_equality_group(p(b0, a1, a0, b1, c0))


def test_gate_operation_approx_eq():
    a = [alphaclops.NamedQubit('r1')]
    b = [alphaclops.NamedQubit('r2')]

    assert alphaclops.approx_eq(
        alphaclops.GateOperation(alphaclops.XPowGate(), a), alphaclops.GateOperation(alphaclops.XPowGate(), a)
    )
    assert not alphaclops.approx_eq(
        alphaclops.GateOperation(alphaclops.XPowGate(), a), alphaclops.GateOperation(alphaclops.XPowGate(), b)
    )

    assert alphaclops.approx_eq(
        alphaclops.GateOperation(alphaclops.XPowGate(exponent=0), a),
        alphaclops.GateOperation(alphaclops.XPowGate(exponent=1e-9), a),
    )
    assert not alphaclops.approx_eq(
        alphaclops.GateOperation(alphaclops.XPowGate(exponent=0), a),
        alphaclops.GateOperation(alphaclops.XPowGate(exponent=1e-7), a),
    )
    assert alphaclops.approx_eq(
        alphaclops.GateOperation(alphaclops.XPowGate(exponent=0), a),
        alphaclops.GateOperation(alphaclops.XPowGate(exponent=1e-7), a),
        atol=1e-6,
    )


def test_gate_operation_qid_shape():
    class ShapeGate(alphaclops.Gate):
        def _qid_shape_(self):
            return (1, 2, 3, 4)

    op = ShapeGate().on(*alphaclops.LineQid.for_qid_shape((1, 2, 3, 4)))
    assert alphaclops.qid_shape(op) == (1, 2, 3, 4)
    assert alphaclops.num_qubits(op) == 4


def test_gate_operation_num_qubits():
    class NumQubitsGate(alphaclops.Gate):
        def _num_qubits_(self):
            return 4

    op = NumQubitsGate().on(*alphaclops.LineQubit.range(4))
    assert alphaclops.qid_shape(op) == (2, 2, 2, 2)
    assert alphaclops.num_qubits(op) == 4


def test_gate_operation_pow():
    Y = alphaclops.Y
    q = alphaclops.NamedQubit('q')
    assert (Y**0.5)(q) == Y(q) ** 0.5


def test_with_qubits_and_transform_qubits():
    g = alphaclops.testing.ThreeQubitGate()
    g = alphaclops.testing.ThreeQubitGate()
    op = alphaclops.GateOperation(g, alphaclops.LineQubit.range(3))
    assert op.with_qubits(*alphaclops.LineQubit.range(3, 0, -1)) == alphaclops.GateOperation(
        g, alphaclops.LineQubit.range(3, 0, -1)
    )
    assert op.transform_qubits(lambda e: alphaclops.LineQubit(-e.x)) == alphaclops.GateOperation(
        g, [alphaclops.LineQubit(0), alphaclops.LineQubit(-1), alphaclops.LineQubit(-2)]
    )


def test_extrapolate():
    q = alphaclops.NamedQubit('q')

    # If the gate isn't extrapolatable, you get a type error.
    op0 = alphaclops.GateOperation(alphaclops.testing.SingleQubitGate(), [q])
    with pytest.raises(TypeError):
        _ = op0**0.5

    op1 = alphaclops.GateOperation(alphaclops.Y, [q])
    assert op1 ** 0.5 == alphaclops.GateOperation(alphaclops.Y ** 0.5, [q])
    assert (alphaclops.Y ** 0.5).on(q) == alphaclops.Y(q) ** 0.5


def test_inverse():
    q = alphaclops.NamedQubit('q')

    # If the gate isn't reversible, you get a type error.
    op0 = alphaclops.GateOperation(alphaclops.testing.SingleQubitGate(), [q])
    assert alphaclops.inverse(op0, None) is None

    op1 = alphaclops.GateOperation(alphaclops.S, [q])
    assert alphaclops.inverse(op1) == op1 ** -1 == alphaclops.GateOperation(alphaclops.S ** -1, [q])
    assert alphaclops.inverse(alphaclops.S).on(q) == alphaclops.inverse(alphaclops.S.on(q))


def test_text_diagrammable():
    q = alphaclops.NamedQubit('q')

    # If the gate isn't diagrammable, you get a type error.
    op0 = alphaclops.GateOperation(alphaclops.testing.SingleQubitGate(), [q])
    with pytest.raises(TypeError):
        _ = alphaclops.circuit_diagram_info(op0)

    op1 = alphaclops.GateOperation(alphaclops.S, [q])
    actual = alphaclops.circuit_diagram_info(op1)
    expected = alphaclops.circuit_diagram_info(alphaclops.S)
    assert actual == expected


def test_bounded_effect():
    q = alphaclops.NamedQubit('q')

    # If the gate isn't bounded, you get a type error.
    op0 = alphaclops.GateOperation(alphaclops.testing.SingleQubitGate(), [q])
    assert alphaclops.trace_distance_bound(op0) >= 1
    op1 = alphaclops.GateOperation(alphaclops.Z ** 0.000001, [q])
    op1_bound = alphaclops.trace_distance_bound(op1)
    assert op1_bound == alphaclops.trace_distance_bound(alphaclops.Z ** 0.000001)


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_parameterizable_effect(resolve_fn):
    q = alphaclops.NamedQubit('q')
    r = alphaclops.ParamResolver({'a': 0.5})

    op1 = alphaclops.GateOperation(alphaclops.Z ** sympy.Symbol('a'), [q])
    assert alphaclops.is_parameterized(op1)
    op2 = resolve_fn(op1, r)
    assert not alphaclops.is_parameterized(op2)
    assert op2 == alphaclops.S.on(q)


def test_pauli_expansion():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    assert alphaclops.pauli_expansion(alphaclops.X(a)) == alphaclops.LinearDict({'X': 1})
    assert alphaclops.pauli_expansion(alphaclops.CNOT(a, b)) == alphaclops.pauli_expansion(alphaclops.CNOT)

    class No(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 1

    class Yes(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 1

        def _pauli_expansion_(self):
            return alphaclops.LinearDict({'X': 0.5})

    assert alphaclops.pauli_expansion(No().on(a), default=None) is None
    assert alphaclops.pauli_expansion(Yes().on(a)) == alphaclops.LinearDict({'X': 0.5})


def test_unitary():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    assert not alphaclops.has_unitary(alphaclops.measure(a))
    assert alphaclops.unitary(alphaclops.measure(a), None) is None
    np.testing.assert_allclose(alphaclops.unitary(alphaclops.X(a)), np.array([[0, 1], [1, 0]]), atol=1e-8)
    np.testing.assert_allclose(alphaclops.unitary(alphaclops.CNOT(a, b)), alphaclops.unitary(alphaclops.CNOT), atol=1e-8)


def test_channel():
    a = alphaclops.NamedQubit('a')
    op = alphaclops.bit_flip(0.5).on(a)
    np.testing.assert_allclose(alphaclops.kraus(op), alphaclops.kraus(op.gate))
    assert alphaclops.has_kraus(op)

    assert alphaclops.kraus(alphaclops.testing.SingleQubitGate()(a), None) is None
    assert not alphaclops.has_kraus(alphaclops.testing.SingleQubitGate()(a))


def test_measurement_key():
    a = alphaclops.NamedQubit('a')
    assert alphaclops.measurement_key_name(alphaclops.measure(a, key='lock')) == 'lock'


def assert_mixtures_equal(actual, expected):
    """Assert equal for tuple of mixed scalar and array types."""
    for a, e in zip(actual, expected):
        np.testing.assert_almost_equal(a[0], e[0])
        np.testing.assert_almost_equal(a[1], e[1])


def test_mixture():
    a = alphaclops.NamedQubit('a')
    op = alphaclops.bit_flip(0.5).on(a)
    assert_mixtures_equal(alphaclops.mixture(op), alphaclops.mixture(op.gate))
    assert alphaclops.has_mixture(op)

    assert alphaclops.has_mixture(alphaclops.X(a))
    m = alphaclops.mixture(alphaclops.X(a))
    assert len(m) == 1
    assert m[0][0] == 1
    np.testing.assert_allclose(m[0][1], alphaclops.unitary(alphaclops.X))


def test_repr():
    a, b = alphaclops.LineQubit.range(2)
    assert (
            repr(alphaclops.GateOperation(alphaclops.CZ, (a, b))) == 'alphaclops.CZ(alphaclops.LineQubit(0), alphaclops.LineQubit(1))'
    )

    class Inconsistent(alphaclops.testing.SingleQubitGate):
        def __repr__(self):
            return 'Inconsistent'

        def on(self, *qubits):
            return alphaclops.GateOperation(Inconsistent(), qubits)

    assert (
        repr(alphaclops.GateOperation(Inconsistent(), [a]))
        == 'alphaclops.GateOperation(gate=Inconsistent, qubits=[alphaclops.LineQubit(0)])'
    )


@pytest.mark.parametrize(
    'gate1,gate2,eq_up_to_global_phase',
    [
        (alphaclops.rz(0.3 * np.pi), alphaclops.Z ** 0.3, True),
        (alphaclops.rz(0.3), alphaclops.Z ** 0.3, False),
        (alphaclops.ZZPowGate(global_shift=0.5), alphaclops.ZZ, True),
        (alphaclops.ZPowGate(global_shift=0.5) ** sympy.Symbol('e'), alphaclops.Z, False),
        (alphaclops.Z ** sympy.Symbol('e'), alphaclops.Z ** sympy.Symbol('f'), False),
    ],
)
def test_equal_up_to_global_phase_on_gates(gate1, gate2, eq_up_to_global_phase):
    num_qubits1, num_qubits2 = (alphaclops.num_qubits(g) for g in (gate1, gate2))
    qubits = alphaclops.LineQubit.range(max(num_qubits1, num_qubits2) + 1)
    op1, op2 = gate1(*qubits[:num_qubits1]), gate2(*qubits[:num_qubits2])
    assert alphaclops.equal_up_to_global_phase(op1, op2) == eq_up_to_global_phase
    op2_on_diff_qubits = gate2(*qubits[1 : num_qubits2 + 1])
    assert not alphaclops.equal_up_to_global_phase(op1, op2_on_diff_qubits)


def test_equal_up_to_global_phase_on_diff_types():
    op = alphaclops.X(alphaclops.LineQubit(0))
    assert not alphaclops.equal_up_to_global_phase(op, 3)


def test_gate_on_operation_besides_gate_operation():
    a, b = alphaclops.LineQubit.range(2)

    op = -1j * alphaclops.X(a) * alphaclops.Y(b)
    assert isinstance(op.gate, alphaclops.DensePauliString)
    assert op.gate == -1j * alphaclops.DensePauliString('XY')
    assert not isinstance(op.gate, alphaclops.XPowGate)


def test_mul():
    class GateRMul(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 1

        def _rmul_with_qubits(self, qubits, other):
            if other == 2:
                return 3
            if isinstance(other, alphaclops.Operation) and isinstance(other.gate, GateRMul):
                return 4
            raise NotImplementedError()

    class GateMul(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 1

        def _mul_with_qubits(self, qubits, other):
            if other == 2:
                return 5
            if isinstance(other, alphaclops.Operation) and isinstance(other.gate, GateMul):
                return 6
            raise NotImplementedError()

    # Delegates right multiplication.
    q = alphaclops.LineQubit(0)
    r = GateRMul().on(q)
    assert 2 * r == 3
    with pytest.raises(TypeError):
        _ = r * 2

    # Delegates left multiplication.
    m = GateMul().on(q)
    assert m * 2 == 5
    with pytest.raises(TypeError):
        _ = 2 * m

    # Handles the symmetric type case correctly.
    assert m * m == 6
    assert r * r == 4


def test_with_gate():
    g1 = alphaclops.GateOperation(alphaclops.X, alphaclops.LineQubit.range(1))
    g2 = alphaclops.GateOperation(alphaclops.Y, alphaclops.LineQubit.range(1))
    assert g1.with_gate(alphaclops.X) is g1
    assert g1.with_gate(alphaclops.Y) == g2


def test_with_measurement_key_mapping():
    a = alphaclops.LineQubit(0)
    op = alphaclops.measure(a, key='m')

    remap_op = alphaclops.with_measurement_key_mapping(op, {'m': 'k'})
    assert alphaclops.measurement_key_names(remap_op) == {'k'}
    assert alphaclops.with_measurement_key_mapping(op, {'x': 'k'}) is op


def test_with_key_path():
    a = alphaclops.LineQubit(0)
    op = alphaclops.measure(a, key='m')

    remap_op = alphaclops.with_key_path(op, ('a', 'b'))
    assert alphaclops.measurement_key_names(remap_op) == {'a:b:m'}
    assert alphaclops.with_key_path(remap_op, ('a', 'b')) is remap_op

    assert alphaclops.with_key_path(op, tuple()) is op

    assert alphaclops.with_key_path(alphaclops.X(a), ('a', 'b')) is NotImplemented


def test_with_key_path_prefix():
    a = alphaclops.LineQubit(0)
    op = alphaclops.measure(a, key='m')
    remap_op = alphaclops.with_key_path_prefix(op, ('a', 'b'))
    assert alphaclops.measurement_key_names(remap_op) == {'a:b:m'}
    assert alphaclops.with_key_path_prefix(remap_op, tuple()) is remap_op
    assert alphaclops.with_key_path_prefix(op, tuple()) is op
    assert alphaclops.with_key_path_prefix(alphaclops.X(a), ('a', 'b')) is NotImplemented


def test_cannot_remap_non_measurement_gate():
    a = alphaclops.LineQubit(0)
    op = alphaclops.X(a)

    assert alphaclops.with_measurement_key_mapping(op, {'m': 'k'}) is NotImplemented


def test_is_parameterized():
    class No1(alphaclops.testing.SingleQubitGate):
        def num_qubits(self) -> int:
            return 1

    class No2(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 1

        def _is_parameterized_(self):
            return False

    class Yes(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 1

        def _is_parameterized_(self):
            return True

    q = alphaclops.LineQubit(0)
    assert not alphaclops.is_parameterized(No1().on(q))
    assert not alphaclops.is_parameterized(No2().on(q))
    assert alphaclops.is_parameterized(Yes().on(q))


def test_group_interchangeable_qubits_creates_tuples_with_unique_keys():
    class MyGate(alphaclops.Gate, alphaclops.InterchangeableQubitsGate):
        def __init__(self, num_qubits) -> None:
            self._num_qubits = num_qubits

        def num_qubits(self) -> int:
            return self._num_qubits

        def qubit_index_to_equivalence_group_key(self, index: int) -> int:
            if index % 2 == 0:
                return index
            return 0

    qubits = alphaclops.LineQubit.range(4)
    gate = MyGate(len(qubits))

    assert gate(qubits[0], qubits[1], qubits[2], qubits[3]) == gate(
        qubits[3], qubits[1], qubits[2], qubits[0]
    )


def test_gate_to_operation_to_gate_round_trips():
    def all_subclasses(cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in all_subclasses(c)]
        )

    # Only test gate subclasses in alphaclops-core.
    gate_subclasses = {
        g
        for g in all_subclasses(alphaclops.Gate)
        if "alphaclops." in g.__module__ and "contrib" not in g.__module__ and "test" not in g.__module__
    }

    test_module_spec = alphaclops.testing.json.spec_for("alphaclops.protocols")

    skip_classes = {
        # Abstract or private parent classes.
        alphaclops.ArithmeticGate,
        alphaclops.BaseDensePauliString,
        alphaclops.EigenGate,
        alphaclops.Pauli,
        # Private gates.
        alphaclops.transformers.analytical_decompositions.two_qubit_to_fsim._BGate,
        alphaclops.transformers.measurement_transformers._ConfusionChannel,
        alphaclops.transformers.measurement_transformers._ModAdd,
        alphaclops.transformers.routing.visualize_routed_circuit._SwapPrintGate,
        alphaclops.ops.raw_types._InverseCompositeGate,
        alphaclops.circuits.qasm_output.QasmTwoQubitGate,
        alphaclops.ops.MSGate,
        # Interop gates
        alphaclops.interop.quirk.QuirkQubitPermutationGate,
        alphaclops.interop.quirk.QuirkArithmeticGate,
    }

    skipped = set()
    for gate_cls in gate_subclasses:
        filename = test_module_spec.test_data_path.joinpath(f"{gate_cls.__name__}.json")
        if pathlib.Path(filename).is_file():
            gates = alphaclops.read_json(filename)
        else:
            if gate_cls in skip_classes:
                skipped.add(gate_cls)
                continue
            # coverage:ignore
            raise AssertionError(
                f"{gate_cls} has no json file, please add a json file or add to the list of "
                "classes to be skipped if there is a reason this gate should not round trip "
                "to a gate via creating an operation."
            )

        if not isinstance(gates, collections.abc.Iterable):
            gates = [gates]
        for gate in gates:
            if gate.num_qubits():
                qudits = [alphaclops.LineQid(i, d) for i, d in enumerate(alphaclops.qid_shape(gate))]
                assert gate.on(*qudits).gate == gate

    assert (
        skipped == skip_classes
    ), "A gate that was supposed to be skipped was not, please update the list of skipped gates."
