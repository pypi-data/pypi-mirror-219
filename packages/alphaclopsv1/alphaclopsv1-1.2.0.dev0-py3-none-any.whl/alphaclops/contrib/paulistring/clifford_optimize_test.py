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

from alphaclops.contrib.paulistring import clifford_optimized_circuit, CliffordTargetGateset


def test_optimize():
    q0, q1 = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(
        alphaclops.X(q1) ** 0.5,
        alphaclops.CZ(q0, q1),
        alphaclops.Z(q0) ** 0.25,
        alphaclops.X(q1) ** 0.25,
        alphaclops.CZ(q0, q1),
        alphaclops.X(q1) ** -0.5,
    )
    c_expected = alphaclops.optimize_for_target_gateset(
        alphaclops.Circuit(alphaclops.CZ(q0, q1), alphaclops.Z(q0) ** 0.25, alphaclops.X(q1) ** 0.25, alphaclops.CZ(q0, q1)),
        gateset=CliffordTargetGateset(),
        ignore_failures=True,
    )

    c_opt = clifford_optimized_circuit(c_orig)

    alphaclops.testing.assert_allclose_up_to_global_phase(c_orig.unitary(), c_opt.unitary(), atol=1e-7)

    assert c_opt == c_expected

    alphaclops.testing.assert_has_diagram(
        c_opt,
        """
0: ───@───[Z]^0.25───@───
      │              │
1: ───@───[X]^0.25───@───
""",
    )


def test_remove_czs():
    q0, q1 = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(alphaclops.CZ(q0, q1), alphaclops.Z(q0) ** 0.5, alphaclops.CZ(q0, q1))
    c_expected = alphaclops.optimize_for_target_gateset(
        alphaclops.Circuit(alphaclops.Z(q0) ** 0.5), gateset=CliffordTargetGateset(), ignore_failures=True
    )

    c_opt = clifford_optimized_circuit(c_orig)

    alphaclops.testing.assert_allclose_up_to_global_phase(
        c_orig.unitary(), c_opt.unitary(qubits_that_should_be_present=(q0, q1)), atol=1e-7
    )

    assert c_opt == c_expected

    alphaclops.testing.assert_has_diagram(
        c_opt,
        """
0: ───Z^0.5───
""",
    )


def test_remove_staggered_czs():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    c_orig = alphaclops.Circuit(alphaclops.CZ(q0, q1), alphaclops.CZ(q1, q2), alphaclops.CZ(q0, q1))
    c_expected = alphaclops.optimize_for_target_gateset(
        alphaclops.Circuit(alphaclops.CZ(q1, q2)), gateset=CliffordTargetGateset(), ignore_failures=True
    )

    c_opt = clifford_optimized_circuit(c_orig)

    alphaclops.testing.assert_allclose_up_to_global_phase(
        c_orig.unitary(), c_opt.unitary(qubits_that_should_be_present=(q0, q1, q2)), atol=1e-7
    )

    assert c_opt == c_expected

    alphaclops.testing.assert_has_diagram(
        c_opt,
        """
1: ───@───
      │
2: ───@───
""",
    )


def test_with_measurements():
    q0, q1 = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(alphaclops.X(q0), alphaclops.CZ(q0, q1), alphaclops.measure(q0, q1, key='m'))
    c_expected = alphaclops.optimize_for_target_gateset(
        alphaclops.Circuit(alphaclops.CZ(q0, q1), alphaclops.X(q0), alphaclops.Z(q1), alphaclops.measure(q0, q1, key='m')),
        gateset=CliffordTargetGateset(),
        ignore_failures=True,
    )
    c_opt = clifford_optimized_circuit(c_orig)

    alphaclops.testing.assert_allclose_up_to_global_phase(c_orig.unitary(), c_opt.unitary(), atol=1e-7)

    assert c_opt == c_expected

    alphaclops.testing.assert_has_diagram(
        c_opt,
        """
0: ───@───X───M('m')───
      │       │
1: ───@───Z───M────────
""",
    )


def test_optimize_large_circuit():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    c_orig = alphaclops.testing.nonoptimal_toffoli_circuit(q0, q1, q2)

    c_opt = clifford_optimized_circuit(c_orig)

    alphaclops.testing.assert_allclose_up_to_global_phase(c_orig.unitary(), c_opt.unitary(), atol=1e-7)
