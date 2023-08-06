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

from typing import Optional, Sequence, Type
import pytest
import alphaclops
import sympy
import numpy as np


def all_gates_of_type(m: alphaclops.Moment, g: alphaclops.Gateset):
    for op in m:
        if op not in g:
            return False
    return True


def assert_optimizes(
    before: alphaclops.Circuit,
    expected: alphaclops.Circuit,
    additional_gates: Optional[Sequence[Type[alphaclops.Gate]]] = None,
):
    if additional_gates is None:
        gateset = alphaclops.CZTargetGateset()
    else:
        gateset = alphaclops.CZTargetGateset(additional_gates=additional_gates)

    alphaclops.testing.assert_same_circuits(
        alphaclops.optimize_for_target_gateset(before, gateset=gateset, ignore_failures=False), expected
    )


def assert_optimization_not_broken(circuit: alphaclops.Circuit):
    c_new = alphaclops.optimize_for_target_gateset(circuit, gateset=alphaclops.CZTargetGateset())
    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        circuit, c_new, atol=1e-6
    )
    c_new = alphaclops.optimize_for_target_gateset(
        circuit, gateset=alphaclops.CZTargetGateset(allow_partial_czs=True), ignore_failures=False
    )
    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        circuit, c_new, atol=1e-6
    )


def test_convert_to_cz_preserving_moment_structure():
    q = alphaclops.LineQubit.range(5)
    op = lambda q0, q1: alphaclops.H(q1).controlled_by(q0)
    c_orig = alphaclops.Circuit(
        alphaclops.Moment(alphaclops.X(q[2])),
        alphaclops.Moment(op(q[0], q[1]), op(q[2], q[3])),
        alphaclops.Moment(op(q[2], q[1]), op(q[4], q[3])),
        alphaclops.Moment(op(q[1], q[2]), op(q[3], q[4])),
        alphaclops.Moment(op(q[3], q[2]), op(q[1], q[0])),
        alphaclops.measure(*q[:2], key="m"),
        alphaclops.X(q[2]).with_classical_controls("m"),
        alphaclops.CZ(*q[3:]).with_classical_controls("m"),
    )
    # Classically controlled operations are not part of the gateset, so failures should be ignored
    # during compilation.
    c_new = alphaclops.optimize_for_target_gateset(
        c_orig, gateset=alphaclops.CZTargetGateset(), ignore_failures=True
    )

    assert c_orig[-2:] == c_new[-2:]
    c_orig, c_new = c_orig[:-2], c_new[:-2]

    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_orig, c_new, atol=1e-6)
    assert all(
        (
            all_gates_of_type(m, alphaclops.Gateset(alphaclops.PhasedXZGate))
            or all_gates_of_type(m, alphaclops.Gateset(alphaclops.CZ))
        )
        for m in c_new
    )

    c_new = alphaclops.optimize_for_target_gateset(
        c_orig, gateset=alphaclops.CZTargetGateset(allow_partial_czs=True), ignore_failures=False
    )
    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_orig, c_new, atol=1e-6)
    assert all(
        (
            all_gates_of_type(m, alphaclops.Gateset(alphaclops.PhasedXZGate))
            or all_gates_of_type(m, alphaclops.Gateset(alphaclops.CZPowGate))
        )
        for m in c_new
    )


def test_clears_paired_cnot():
    a, b = alphaclops.LineQubit.range(2)
    assert_optimizes(
        before=alphaclops.Circuit(alphaclops.Moment(alphaclops.CNOT(a, b)), alphaclops.Moment(alphaclops.CNOT(a, b))),
        expected=alphaclops.Circuit(),
    )


def test_ignores_czs_separated_by_parameterized():
    a, b = alphaclops.LineQubit.range(2)
    assert_optimizes(
        before=alphaclops.Circuit(
            [
                alphaclops.Moment(alphaclops.CZ(a, b)),
                alphaclops.Moment(alphaclops.Z(a) ** sympy.Symbol('boo')),
                alphaclops.Moment(alphaclops.CZ(a, b)),
            ]
        ),
        expected=alphaclops.Circuit(
            [
                alphaclops.Moment(alphaclops.CZ(a, b)),
                alphaclops.Moment(alphaclops.Z(a) ** sympy.Symbol('boo')),
                alphaclops.Moment(alphaclops.CZ(a, b)),
            ]
        ),
        additional_gates=[alphaclops.ZPowGate],
    )


def test_cnots_separated_by_single_gates_correct():
    a, b = alphaclops.LineQubit.range(2)
    assert_optimization_not_broken(alphaclops.Circuit(alphaclops.CNOT(a, b), alphaclops.H(b), alphaclops.CNOT(a, b)))


def test_czs_separated_by_single_gates_correct():
    a, b = alphaclops.LineQubit.range(2)
    assert_optimization_not_broken(
        alphaclops.Circuit(alphaclops.CZ(a, b), alphaclops.X(b), alphaclops.X(b), alphaclops.X(b), alphaclops.CZ(a, b))
    )


def test_inefficient_circuit_correct():
    t = 0.1
    v = 0.11
    a, b = alphaclops.LineQubit.range(2)
    assert_optimization_not_broken(
        alphaclops.Circuit(
            alphaclops.H(b),
            alphaclops.CNOT(a, b),
            alphaclops.H(b),
            alphaclops.CNOT(a, b),
            alphaclops.CNOT(b, a),
            alphaclops.H(a),
            alphaclops.CNOT(a, b),
            alphaclops.Z(a) ** t,
            alphaclops.Z(b) ** -t,
            alphaclops.CNOT(a, b),
            alphaclops.H(a),
            alphaclops.Z(b) ** v,
            alphaclops.CNOT(a, b),
            alphaclops.Z(a) ** -v,
            alphaclops.Z(b) ** -v,
        )
    )


def test_optimizes_single_iswap():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.ISWAP(a, b))
    assert_optimization_not_broken(c)
    c = alphaclops.optimize_for_target_gateset(c, gateset=alphaclops.CZTargetGateset(), ignore_failures=False)
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 2


def test_optimizes_tagged_partial_cz():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit((alphaclops.CZ ** 0.5)(a, b).with_tags('mytag'))
    assert_optimization_not_broken(c)
    c = alphaclops.optimize_for_target_gateset(c, gateset=alphaclops.CZTargetGateset(), ignore_failures=False)
    assert (
        len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 2
    ), 'It should take 2 CZ gates to decompose a CZ**0.5 gate'


def test_not_decompose_czs():
    circuit = alphaclops.Circuit(
        alphaclops.CZPowGate(exponent=1, global_shift=-0.5).on(*alphaclops.LineQubit.range(2))
    )
    assert_optimizes(before=circuit, expected=circuit)


@pytest.mark.parametrize(
    'circuit',
    (
            alphaclops.Circuit(alphaclops.CZPowGate(exponent=0.1)(*alphaclops.LineQubit.range(2))),
            alphaclops.Circuit(
            alphaclops.CZPowGate(exponent=0.2)(*alphaclops.LineQubit.range(2)),
            alphaclops.CZPowGate(exponent=0.3, global_shift=-0.5)(*alphaclops.LineQubit.range(2)),
        ),
    ),
)
def test_decompose_partial_czs(circuit):
    circuit = alphaclops.optimize_for_target_gateset(
        circuit, gateset=alphaclops.CZTargetGateset(), ignore_failures=False
    )
    cz_gates = [
        op.gate
        for op in circuit.all_operations()
        if isinstance(op, alphaclops.GateOperation) and isinstance(op.gate, alphaclops.CZPowGate)
    ]
    num_full_cz = sum(1 for cz in cz_gates if cz.exponent % 2 == 1)
    num_part_cz = sum(1 for cz in cz_gates if cz.exponent % 2 != 1)
    assert num_full_cz == 2
    assert num_part_cz == 0


def test_not_decompose_partial_czs():
    circuit = alphaclops.Circuit(
        alphaclops.CZPowGate(exponent=0.1, global_shift=-0.5)(*alphaclops.LineQubit.range(2))
    )
    alphaclops.optimize_for_target_gateset(circuit, gateset=alphaclops.CZTargetGateset(), ignore_failures=False)
    cz_gates = [
        op.gate
        for op in circuit.all_operations()
        if isinstance(op, alphaclops.GateOperation) and isinstance(op.gate, alphaclops.CZPowGate)
    ]
    num_full_cz = sum(1 for cz in cz_gates if cz.exponent % 2 == 1)
    num_part_cz = sum(1 for cz in cz_gates if cz.exponent % 2 != 1)
    assert num_full_cz == 0
    assert num_part_cz == 1


def test_avoids_decompose_when_matrix_available():
    class OtherXX(alphaclops.testing.TwoQubitGate):
        # coverage: ignore
        def _has_unitary_(self) -> bool:
            return True

        def _unitary_(self) -> np.ndarray:
            m = np.array([[0, 1], [1, 0]])
            return np.kron(m, m)

        def _decompose_(self, qubits):
            assert False

    class OtherOtherXX(alphaclops.testing.TwoQubitGate):
        # coverage: ignore
        def _has_unitary_(self) -> bool:
            return True

        def _unitary_(self) -> np.ndarray:
            m = np.array([[0, 1], [1, 0]])
            return np.kron(m, m)

        def _decompose_(self, qubits):
            assert False

    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(OtherXX()(a, b), OtherOtherXX()(a, b))
    c = alphaclops.optimize_for_target_gateset(c, gateset=alphaclops.CZTargetGateset(), ignore_failures=False)
    assert len(c) == 0


def test_composite_gates_without_matrix():
    class CompositeDummy(alphaclops.testing.SingleQubitGate):
        def _decompose_(self, qubits):
            yield alphaclops.X(qubits[0])
            yield alphaclops.Y(qubits[0]) ** 0.5

    class CompositeDummy2(alphaclops.testing.TwoQubitGate):
        def _decompose_(self, qubits):
            yield alphaclops.CZ(qubits[0], qubits[1])
            yield CompositeDummy()(qubits[1])

    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(CompositeDummy()(q0), CompositeDummy2()(q0, q1))
    expected = alphaclops.Circuit(
        alphaclops.X(q0), alphaclops.Y(q0) ** 0.5, alphaclops.CZ(q0, q1), alphaclops.X(q1), alphaclops.Y(q1) ** 0.5
    )
    c_new = alphaclops.optimize_for_target_gateset(
        circuit, gateset=alphaclops.CZTargetGateset(), ignore_failures=False
    )

    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        c_new, expected, atol=1e-6
    )
    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        c_new, circuit, atol=1e-6
    )


def test_unsupported_gate():
    class UnsupportedDummy(alphaclops.testing.TwoQubitGate):
        pass

    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(UnsupportedDummy()(q0, q1))
    assert circuit == alphaclops.optimize_for_target_gateset(circuit, gateset=alphaclops.CZTargetGateset())
    with pytest.raises(ValueError, match='Unable to convert'):
        _ = alphaclops.optimize_for_target_gateset(
            circuit, gateset=alphaclops.CZTargetGateset(), ignore_failures=False
        )


@pytest.mark.parametrize(
    'gateset',
    [
        alphaclops.CZTargetGateset(),
        alphaclops.CZTargetGateset(
            atol=1e-6,
            allow_partial_czs=True,
            additional_gates=[
                alphaclops.SQRT_ISWAP,
                alphaclops.XPowGate,
                alphaclops.YPowGate,
                alphaclops.GateFamily(alphaclops.ZPowGate, tags_to_accept=['test_tag']),
            ],
        ),
        alphaclops.CZTargetGateset(additional_gates=()),
    ],
)
def test_repr(gateset):
    alphaclops.testing.assert_equivalent_repr(gateset)
