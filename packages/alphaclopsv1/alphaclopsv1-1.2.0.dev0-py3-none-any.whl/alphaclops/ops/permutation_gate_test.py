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
import numpy as np
from alphaclops.ops import QubitPermutationGate


def test_permutation_gate_equality():
    eq = alphaclops.testing.EqualsTester()
    eq.make_equality_group(
        lambda: QubitPermutationGate([0, 1]), lambda: QubitPermutationGate((0, 1))
    )
    eq.add_equality_group(QubitPermutationGate([1, 0]), QubitPermutationGate((1, 0)))


def test_permutation_gate_repr():
    alphaclops.testing.assert_equivalent_repr(QubitPermutationGate([0, 1]))


rs = np.random.RandomState(seed=1234)


@pytest.mark.parametrize('permutation', [rs.permutation(i) for i in range(3, 7)])
def test_permutation_gate_consistent_protocols(permutation):
    gate = QubitPermutationGate(list(permutation))
    alphaclops.testing.assert_implements_consistent_protocols(gate)


def test_permutation_gate_invalid_indices():
    with pytest.raises(ValueError, match="Invalid indices"):
        QubitPermutationGate([1, 0, 2, 4])
    with pytest.raises(ValueError, match="Invalid indices"):
        QubitPermutationGate([-1])


def test_permutation_gate_invalid_permutation():
    with pytest.raises(ValueError, match="Invalid permutation"):
        QubitPermutationGate([1, 1])
    with pytest.raises(ValueError, match="Invalid permutation"):
        QubitPermutationGate([])


def test_permutation_gate_diagram():
    q = alphaclops.LineQubit.range(6)
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(alphaclops.X(q[0]), alphaclops.X(q[5]), QubitPermutationGate([3, 2, 1, 0]).on(*q[1:5])),
        """
0: ───X───────

1: ───[0>3]───
      │
2: ───[1>2]───
      │
3: ───[2>1]───
      │
4: ───[3>0]───

5: ───X───────
""",
    )


def test_permutation_gate_json_dict():
    assert alphaclops.QubitPermutationGate([0, 1, 2])._json_dict_() == {'permutation': (0, 1, 2)}


@pytest.mark.parametrize(
    'maps, permutation',
    [
        [{0b0: 0b0}, [0]],
        [{0b00: 0b00, 0b01: 0b01, 0b10: 0b10}, [0, 1, 2]],
        [
            {
                0b_000: 0b_000,
                0b_001: 0b_100,
                0b_010: 0b_010,
                0b_100: 0b_001,
                0b_111: 0b_111,
                0b_101: 0b_101,
            },
            [2, 1, 0],
        ],
    ],
)
def test_permutation_gate_maps(maps, permutation):
    qs = alphaclops.LineQubit.range(len(permutation))
    permutationOp = alphaclops.QubitPermutationGate(permutation).on(*qs)
    circuit = alphaclops.Circuit(permutationOp)
    alphaclops.testing.assert_equivalent_computational_basis_map(maps, circuit)
    circuit = alphaclops.Circuit(alphaclops.I.on_each(*qs), alphaclops.decompose(permutationOp))
    alphaclops.testing.assert_equivalent_computational_basis_map(maps, circuit)
