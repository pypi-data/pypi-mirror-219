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
import pytest

import alphaclops


class NoMethod:
    pass


class ReturnsNotImplemented:
    def _pauli_expansion_(self):
        return NotImplemented


class ReturnsExpansion:
    def __init__(self, expansion: alphaclops.LinearDict[str]) -> None:
        self._expansion = expansion

    def _pauli_expansion_(self) -> alphaclops.LinearDict[str]:
        return self._expansion


class HasUnitary:
    def __init__(self, unitary: np.ndarray):
        self._unitary = unitary

    def _unitary_(self) -> np.ndarray:
        return self._unitary


class HasQuditUnitary:
    def _qid_shape_(self):
        return (3,)

    def _unitary_(self) -> np.ndarray:
        raise NotImplementedError


@pytest.mark.parametrize(
    'val', (NoMethod(), ReturnsNotImplemented(), HasQuditUnitary(), 123, np.eye(2), object(), alphaclops)
)
def test_raises_no_pauli_expansion(val):
    assert alphaclops.pauli_expansion(val, default=None) is None
    with pytest.raises(TypeError, match='No Pauli expansion'):
        alphaclops.pauli_expansion(val)


@pytest.mark.parametrize(
    'val, expected_expansion',
    (
        (
                ReturnsExpansion(alphaclops.LinearDict({'X': 1, 'Y': 2, 'Z': 3})),
                alphaclops.LinearDict({'X': 1, 'Y': 2, 'Z': 3}),
        ),
        (HasUnitary(np.eye(2)), alphaclops.LinearDict({'I': 1})),
        (HasUnitary(np.array([[1, -1j], [1j, -1]])), alphaclops.LinearDict({'Y': 1, 'Z': 1})),
        (HasUnitary(np.array([[0.0, 1.0], [0.0, 0.0]])), alphaclops.LinearDict({'X': 0.5, 'Y': 0.5j})),
        (HasUnitary(np.eye(16)), alphaclops.LinearDict({'IIII': 1.0})),
        (alphaclops.H, alphaclops.LinearDict({'X': np.sqrt(0.5), 'Z': np.sqrt(0.5)})),
        (
                alphaclops.ry(np.pi / 2),
                alphaclops.LinearDict({'I': np.cos(np.pi / 4), 'Y': -1j * np.sin(np.pi / 4)}),
        ),
    ),
)
def test_pauli_expansion(val, expected_expansion):
    actual_expansion = alphaclops.pauli_expansion(val)
    assert alphaclops.approx_eq(actual_expansion, expected_expansion, atol=1e-12)
    assert set(actual_expansion.keys()) == set(expected_expansion.keys())
    for name in actual_expansion.keys():
        assert np.abs(actual_expansion[name] - expected_expansion[name]) < 1e-12
