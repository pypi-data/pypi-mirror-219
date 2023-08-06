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

import pytest

import alphaclops


Q, Q2, Q3 = alphaclops.LineQubit.range(3)


@pytest.mark.parametrize(
    "op,expected",
    [
        (alphaclops.H(Q), False),
        (alphaclops.HPowGate(exponent=0.5)(Q), False),
        (alphaclops.PhasedXPowGate(exponent=0.25, phase_exponent=0.125)(Q), True),
        (alphaclops.XPowGate(exponent=0.5)(Q), True),
        (alphaclops.YPowGate(exponent=0.25)(Q), True),
        (alphaclops.ZPowGate(exponent=0.125)(Q), True),
        (alphaclops.CZPowGate(exponent=0.5)(Q, Q2), False),
        (alphaclops.CZ(Q, Q2), True),
        (alphaclops.CNOT(Q, Q2), True),
        (alphaclops.SWAP(Q, Q2), False),
        (alphaclops.ISWAP(Q, Q2), False),
        (alphaclops.CCNOT(Q, Q2, Q3), True),
        (alphaclops.CCZ(Q, Q2, Q3), True),
        (alphaclops.ParallelGate(alphaclops.X, num_copies=3)(Q, Q2, Q3), True),
        (alphaclops.ParallelGate(alphaclops.Y, num_copies=3)(Q, Q2, Q3), True),
        (alphaclops.ParallelGate(alphaclops.Z, num_copies=3)(Q, Q2, Q3), True),
        (alphaclops.X(Q).controlled_by(Q2, Q3), True),
        (alphaclops.Z(Q).controlled_by(Q2, Q3), True),
        (alphaclops.ZPowGate(exponent=0.5)(Q).controlled_by(Q2, Q3), False),
    ],
)
def test_gateset(op: alphaclops.Operation, expected: bool):
    assert alphaclops.is_native_neutral_atom_op(op) == expected
    if op.gate is not None:
        assert alphaclops.is_native_neutral_atom_gate(op.gate) == expected
