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


import alphaclops

from alphaclops.contrib.paulistring import pauli_string_optimized_circuit, CliffordTargetGateset


def test_optimize():
    q0, q1 = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(
        alphaclops.X(q0) ** 0.25, alphaclops.H(q0), alphaclops.CZ(q0, q1), alphaclops.H(q0), alphaclops.X(q0) ** 0.125
    )
    c_expected = alphaclops.optimize_for_target_gateset(
        alphaclops.Circuit(
            alphaclops.Y(q0) ** -0.5,
            alphaclops.CZ(q0, q1),
            alphaclops.Z(q0) ** -0.125,
            alphaclops.X(q0) ** 0.5,
            alphaclops.Z(q0) ** 0.5,
        ),
        gateset=CliffordTargetGateset(
            single_qubit_target=CliffordTargetGateset.SingleQubitTarget.PAULI_STRING_PHASORS
        ),
    )

    c_opt = pauli_string_optimized_circuit(c_orig)

    alphaclops.testing.assert_allclose_up_to_global_phase(
        c_orig.unitary(), c_expected.unitary(), atol=1e-7
    )

    alphaclops.testing.assert_has_diagram(
        c_opt,
        """
0: ───[Y]^-0.5───@───[Z]^(-1/8)───[X]^0.5───[Z]^0.5───
                 │
1: ──────────────@────────────────────────────────────
""",
    )


def test_handles_measurement_gate():
    q0, q1 = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(
        alphaclops.X(q0) ** 0.25,
        alphaclops.H(q0),
        alphaclops.CZ(q0, q1),
        alphaclops.H(q0),
        alphaclops.X(q0) ** 0.125,
        alphaclops.measure(q1, key='m1'),
        alphaclops.measure(q0, key='m0'),
    )
    c_opt = pauli_string_optimized_circuit(c_orig)

    alphaclops.testing.assert_allclose_up_to_global_phase(c_orig.unitary(), c_opt.unitary(), atol=1e-7)

    alphaclops.testing.assert_has_diagram(
        c_opt,
        """
0: ───[Y]^-0.5───@───[Z]^(-1/8)───[X]^0.5───[Z]^0.5───M('m0')───
                 │
1: ──────────────@───M('m1')────────────────────────────────────
""",
    )


def test_optimize_large_circuit():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    c_orig = alphaclops.testing.nonoptimal_toffoli_circuit(q0, q1, q2)

    c_opt = pauli_string_optimized_circuit(c_orig)

    alphaclops.testing.assert_allclose_up_to_global_phase(c_orig.unitary(), c_opt.unitary(), atol=1e-7)
