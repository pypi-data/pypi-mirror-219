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
import numpy as np

import alphaclops
import alphaclops.testing as ct
from alphaclops.testing import consistent_qasm as cq
from alphaclops.contrib.qasm_import import circuit_from_qasm


def test_consistency_with_qasm_output_and_qiskit():
    qubits = [alphaclops.NamedQubit(f'q_{i}') for i in range(4)]
    a, b, c, d = qubits
    circuit1 = alphaclops.Circuit(
        alphaclops.rx(np.pi / 2).on(a),
        alphaclops.ry(np.pi / 2).on(b),
        alphaclops.rz(np.pi / 2).on(b),
        alphaclops.X.on(a),
        alphaclops.Y.on(b),
        alphaclops.Z.on(c),
        alphaclops.H.on(d),
        alphaclops.S.on(a),
        alphaclops.T.on(b),
        alphaclops.S.on(c) ** -1,
        alphaclops.T.on(d) ** -1,
        alphaclops.X.on(d) ** 0.125,
        alphaclops.TOFFOLI.on(a, b, c),
        alphaclops.CSWAP.on(d, a, b),
        alphaclops.SWAP.on(c, d),
        alphaclops.CX.on(a, b),
        alphaclops.ControlledGate(alphaclops.Y).on(c, d),
        alphaclops.CZ.on(a, b),
        alphaclops.ControlledGate(alphaclops.H).on(b, c),
        alphaclops.IdentityGate(1).on(c),
        alphaclops.circuits.qasm_output.QasmUGate(1.0, 2.0, 3.0).on(d),
    )

    qasm = alphaclops.qasm(circuit1)

    circuit2 = circuit_from_qasm(qasm)

    alphaclops_unitary = alphaclops.unitary(circuit2)
    ct.assert_allclose_up_to_global_phase(alphaclops_unitary, alphaclops.unitary(circuit1), atol=1e-8)

    cq.assert_qiskit_parsed_qasm_consistent_with_unitary(qasm, alphaclops_unitary)
