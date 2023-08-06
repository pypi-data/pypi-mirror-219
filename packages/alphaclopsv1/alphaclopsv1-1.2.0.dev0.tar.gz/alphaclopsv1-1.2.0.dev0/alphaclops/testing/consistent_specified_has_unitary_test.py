# Copyright 2019 The alphaclops Developers
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
import numpy as np

import alphaclops


def test_assert_specifies_has_unitary_if_unitary_from_matrix():
    class Bad:
        def _unitary_(self):
            return np.array([[1]])

    assert alphaclops.has_unitary(Bad())
    with pytest.raises(AssertionError, match='specify a _has_unitary_ method'):
        alphaclops.testing.assert_specifies_has_unitary_if_unitary(Bad())


def test_assert_specifies_has_unitary_if_unitary_from_apply():
    class Bad(alphaclops.Operation):
        @property
        def qubits(self):
            # coverage: ignore
            return ()

        def with_qubits(self, *new_qubits):
            # coverage: ignore
            return self

        def _apply_unitary_(self, args):
            return args.target_tensor

    assert alphaclops.has_unitary(Bad())
    with pytest.raises(AssertionError, match='specify a _has_unitary_ method'):
        alphaclops.testing.assert_specifies_has_unitary_if_unitary(Bad())


def test_assert_specifies_has_unitary_if_unitary_from_decompose():
    class Bad:
        def _decompose_(self):
            return []

    assert alphaclops.has_unitary(Bad())
    with pytest.raises(AssertionError, match='specify a _has_unitary_ method'):
        alphaclops.testing.assert_specifies_has_unitary_if_unitary(Bad())

    class Bad2:
        def _decompose_(self):
            return [alphaclops.X(alphaclops.LineQubit(0))]

    assert alphaclops.has_unitary(Bad2())
    with pytest.raises(AssertionError, match='specify a _has_unitary_ method'):
        alphaclops.testing.assert_specifies_has_unitary_if_unitary(Bad2())

    class Okay:
        def _decompose_(self):
            return [alphaclops.depolarize(0.5).on(alphaclops.LineQubit(0))]

    assert not alphaclops.has_unitary(Okay())
    alphaclops.testing.assert_specifies_has_unitary_if_unitary(Okay())


def test_assert_specifies_has_unitary_if_unitary_pass():
    class Good:
        def _has_unitary_(self):
            return True

    assert alphaclops.has_unitary(Good())
    alphaclops.testing.assert_specifies_has_unitary_if_unitary(Good())
