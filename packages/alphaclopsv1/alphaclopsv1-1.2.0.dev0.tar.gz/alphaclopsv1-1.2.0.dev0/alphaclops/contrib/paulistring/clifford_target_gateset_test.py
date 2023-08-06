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

import pytest
import sympy

import alphaclops
from alphaclops.contrib.paulistring.clifford_target_gateset import CliffordTargetGateset


@pytest.mark.parametrize(
    'op,expected_ops',
    (
        lambda q0, q1: (
            (alphaclops.X(q0), alphaclops.SingleQubitCliffordGate.X(q0)),
            (alphaclops.Y(q0), alphaclops.SingleQubitCliffordGate.Y(q0)),
            (alphaclops.Z(q0), alphaclops.SingleQubitCliffordGate.Z(q0)),
            (alphaclops.X(q0) ** 0.5, alphaclops.SingleQubitCliffordGate.X_sqrt(q0)),
            (alphaclops.Y(q0) ** 0.5, alphaclops.SingleQubitCliffordGate.Y_sqrt(q0)),
            (alphaclops.Z(q0) ** 0.5, alphaclops.SingleQubitCliffordGate.Z_sqrt(q0)),
            (alphaclops.X(q0) ** -0.5, alphaclops.SingleQubitCliffordGate.X_nsqrt(q0)),
            (alphaclops.Y(q0) ** -0.5, alphaclops.SingleQubitCliffordGate.Y_nsqrt(q0)),
            (alphaclops.Z(q0) ** -0.5, alphaclops.SingleQubitCliffordGate.Z_nsqrt(q0)),
            (alphaclops.X(q0) ** 0.25, alphaclops.PauliStringPhasor(alphaclops.PauliString([alphaclops.X.on(q0)])) ** 0.25),
            (alphaclops.Y(q0) ** 0.25, alphaclops.PauliStringPhasor(alphaclops.PauliString([alphaclops.Y.on(q0)])) ** 0.25),
            (alphaclops.Z(q0) ** 0.25, alphaclops.PauliStringPhasor(alphaclops.PauliString([alphaclops.Z.on(q0)])) ** 0.25),
            (alphaclops.X(q0) ** 0, ()),
            (alphaclops.CZ(q0, q1), alphaclops.CZ(q0, q1)),
            (alphaclops.measure(q0, q1, key='key'), alphaclops.measure(q0, q1, key='key')),
        )
    )(alphaclops.LineQubit(0), alphaclops.LineQubit(1)),
)
def test_converts_various_ops(op, expected_ops):
    before = alphaclops.Circuit(op)
    expected = alphaclops.Circuit(expected_ops, strategy=alphaclops.InsertStrategy.EARLIEST)
    after = alphaclops.optimize_for_target_gateset(
        before, gateset=CliffordTargetGateset(), ignore_failures=False
    )
    assert after == expected
    alphaclops.testing.assert_allclose_up_to_global_phase(
        before.unitary(), after.unitary(qubits_that_should_be_present=op.qubits), atol=1e-7
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        after.unitary(qubits_that_should_be_present=op.qubits),
        expected.unitary(qubits_that_should_be_present=op.qubits),
        atol=1e-7,
    )


def test_degenerate_single_qubit_decompose():
    q0 = alphaclops.LineQubit(0)

    before = alphaclops.Circuit(alphaclops.Z(q0) ** 0.1, alphaclops.X(q0) ** 1.0000000001, alphaclops.Z(q0) ** 0.1)
    expected = alphaclops.Circuit(alphaclops.SingleQubitCliffordGate.X(q0))

    after = alphaclops.optimize_for_target_gateset(
        before, gateset=CliffordTargetGateset(), ignore_failures=False
    )
    assert after == expected
    alphaclops.testing.assert_allclose_up_to_global_phase(before.unitary(), after.unitary(), atol=1e-7)
    alphaclops.testing.assert_allclose_up_to_global_phase(after.unitary(), expected.unitary(), atol=1e-7)


def test_converts_single_qubit_series():
    q0 = alphaclops.LineQubit(0)

    before = alphaclops.Circuit(
        alphaclops.X(q0),
        alphaclops.Y(q0),
        alphaclops.Z(q0),
        alphaclops.X(q0) ** 0.5,
        alphaclops.Y(q0) ** 0.5,
        alphaclops.Z(q0) ** 0.5,
        alphaclops.X(q0) ** -0.5,
        alphaclops.Y(q0) ** -0.5,
        alphaclops.Z(q0) ** -0.5,
        alphaclops.X(q0) ** 0.25,
        alphaclops.Y(q0) ** 0.25,
        alphaclops.Z(q0) ** 0.25,
    )

    after = alphaclops.optimize_for_target_gateset(
        before, gateset=CliffordTargetGateset(), ignore_failures=False
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(before.unitary(), after.unitary(), atol=1e-7)


def test_converts_single_qubit_then_two():
    q0, q1 = alphaclops.LineQubit.range(2)

    before = alphaclops.Circuit(alphaclops.X(q0), alphaclops.Y(q0), alphaclops.CZ(q0, q1))

    after = alphaclops.optimize_for_target_gateset(
        before, gateset=CliffordTargetGateset(), ignore_failures=False
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(before.unitary(), after.unitary(), atol=1e-7)


def test_converts_large_circuit():
    q0, q1, q2 = alphaclops.LineQubit.range(3)

    before = alphaclops.Circuit(
        alphaclops.X(q0),
        alphaclops.Y(q0),
        alphaclops.Z(q0),
        alphaclops.X(q0) ** 0.5,
        alphaclops.Y(q0) ** 0.5,
        alphaclops.Z(q0) ** 0.5,
        alphaclops.X(q0) ** -0.5,
        alphaclops.Y(q0) ** -0.5,
        alphaclops.Z(q0) ** -0.5,
        alphaclops.H(q0),
        alphaclops.CZ(q0, q1),
        alphaclops.CZ(q1, q2),
        alphaclops.X(q0) ** 0.25,
        alphaclops.Y(q0) ** 0.25,
        alphaclops.Z(q0) ** 0.25,
        alphaclops.CZ(q0, q1),
    )

    after = alphaclops.optimize_for_target_gateset(
        before, gateset=CliffordTargetGateset(), ignore_failures=False
    )

    alphaclops.testing.assert_allclose_up_to_global_phase(before.unitary(), after.unitary(), atol=1e-7)

    alphaclops.testing.assert_has_diagram(
        after,
        '''
0: ───Y^0.5───@───[Z]^-0.304───[X]^(1/3)───[Z]^0.446───────@───
              │                                            │
1: ───────────@────────────────────────────────────────@───@───
                                                       │
2: ────────────────────────────────────────────────────@───────
''',
    )


def test_convert_to_pauli_string_phasors():
    q0, q1 = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(alphaclops.X(q0), alphaclops.Y(q1) ** 0.25, alphaclops.Z(q0) ** 0.125, alphaclops.H(q1))
    c_new = alphaclops.optimize_for_target_gateset(
        c_orig,
        gateset=CliffordTargetGateset(
            single_qubit_target=CliffordTargetGateset.SingleQubitTarget.PAULI_STRING_PHASORS
        ),
    )

    alphaclops.testing.assert_allclose_up_to_global_phase(c_new.unitary(), c_orig.unitary(), atol=1e-7)
    alphaclops.testing.assert_has_diagram(
        c_new,
        """
0: ───[X]─────────[Z]^(1/8)───

1: ───[Y]^-0.25───[Z]─────────
""",
    )


def test_already_converted():
    q0 = alphaclops.LineQubit(0)
    c_orig = alphaclops.Circuit(alphaclops.PauliStringPhasor(alphaclops.X.on(q0)))
    c_new = alphaclops.optimize_for_target_gateset(
        c_orig,
        gateset=CliffordTargetGateset(
            single_qubit_target=CliffordTargetGateset.SingleQubitTarget.PAULI_STRING_PHASORS
        ),
        ignore_failures=False,
    )
    assert c_new == c_orig


def test_ignore_unsupported_gate():
    class UnsupportedDummy(alphaclops.testing.TwoQubitGate):
        pass

    q0, q1 = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(UnsupportedDummy()(q0, q1), alphaclops.X(q0) ** sympy.Symbol("theta"))
    c_new = alphaclops.optimize_for_target_gateset(
        c_orig, gateset=CliffordTargetGateset(), ignore_failures=True
    )
    assert c_new == c_orig


def test_fail_unsupported_gate():
    class UnsupportedDummy(alphaclops.testing.TwoQubitGate):
        pass

    q0, q1 = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(UnsupportedDummy()(q0, q1))
    with pytest.raises(ValueError):
        _ = alphaclops.optimize_for_target_gateset(
            c_orig, gateset=CliffordTargetGateset(), ignore_failures=False
        )


def test_convert_to_single_qubit_cliffords():
    q0, q1 = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(
        alphaclops.X(q0), alphaclops.Y(q1) ** 0.5, alphaclops.Z(q0) ** -0.5, alphaclops.Z(q1) ** 0, alphaclops.H(q0)
    )
    c_new = alphaclops.optimize_for_target_gateset(
        c_orig,
        gateset=CliffordTargetGateset(
            single_qubit_target=CliffordTargetGateset.SingleQubitTarget.SINGLE_QUBIT_CLIFFORDS
        ),
        ignore_failures=True,
    )

    assert all(isinstance(op.gate, alphaclops.SingleQubitCliffordGate) for op in c_new.all_operations())

    alphaclops.testing.assert_allclose_up_to_global_phase(c_new.unitary(), c_orig.unitary(), atol=1e-7)

    alphaclops.testing.assert_has_diagram(
        c_new,
        """
0: ───(X^-0.5-Z^0.5)───

1: ───Y^0.5────────────
""",
    )


def test_convert_to_single_qubit_cliffords_ignores_non_clifford():
    q0 = alphaclops.LineQubit(0)
    c_orig = alphaclops.Circuit(alphaclops.Z(q0) ** 0.25)
    c_new = alphaclops.optimize_for_target_gateset(
        c_orig,
        gateset=CliffordTargetGateset(
            single_qubit_target=CliffordTargetGateset.SingleQubitTarget.SINGLE_QUBIT_CLIFFORDS
        ),
        ignore_failures=True,
    )
    assert c_orig == c_new
