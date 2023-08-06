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
from alphaclops.contrib.paulistring import (
    convert_and_separate_circuit,
    pauli_string_dag_from_circuit,
    move_pauli_strings_into_circuit,
)


def _assert_no_multi_qubit_pauli_strings(circuit: alphaclops.Circuit) -> None:
    for op in circuit.all_operations():
        if isinstance(op, alphaclops.PauliStringGateOperation):
            assert len(op.pauli_string) == 1


def test_move_non_clifford_into_clifford():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    c_orig = alphaclops.testing.nonoptimal_toffoli_circuit(q0, q1, q2)

    c_left, c_right = convert_and_separate_circuit(c_orig)

    # Normally, c_left would be optimized here
    c_left_dag = pauli_string_dag_from_circuit(c_left)

    c_recombined1 = move_pauli_strings_into_circuit(c_left, c_right)
    c_recombined2 = move_pauli_strings_into_circuit(c_left_dag, c_right)

    _assert_no_multi_qubit_pauli_strings(c_recombined1)
    _assert_no_multi_qubit_pauli_strings(c_recombined2)

    gateset = alphaclops.CZTargetGateset()
    baseline_len = len(alphaclops.optimize_for_target_gateset(c_orig, gateset=gateset))
    opt_len1 = len(alphaclops.optimize_for_target_gateset(c_recombined1, gateset=gateset))
    opt_len2 = len(alphaclops.optimize_for_target_gateset(c_recombined2, gateset=gateset))
    assert opt_len1 <= baseline_len
    assert opt_len2 <= baseline_len
