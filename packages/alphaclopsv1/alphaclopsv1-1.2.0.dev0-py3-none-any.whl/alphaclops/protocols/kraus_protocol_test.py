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

"""Tests for kraus_protocol.py."""

from typing import Iterable, List, Sequence, Tuple

import numpy as np
import pytest

import alphaclops


LOCAL_DEFAULT: List[np.ndarray] = [np.array([])]


def test_kraus_no_methods():
    class NoMethod:
        pass

    with pytest.raises(TypeError, match='no _kraus_ or _mixture_ or _unitary_ method'):
        _ = alphaclops.kraus(NoMethod())

    assert alphaclops.kraus(NoMethod(), None) is None
    assert alphaclops.kraus(NoMethod, NotImplemented) is NotImplemented
    assert alphaclops.kraus(NoMethod(), (1,)) == (1,)
    assert alphaclops.kraus(NoMethod(), LOCAL_DEFAULT) is LOCAL_DEFAULT

    assert not alphaclops.has_kraus(NoMethod())


def assert_not_implemented(val):
    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = alphaclops.kraus(val)

    assert alphaclops.kraus(val, None) is None
    assert alphaclops.kraus(val, NotImplemented) is NotImplemented
    assert alphaclops.kraus(val, (1,)) == (1,)
    assert alphaclops.kraus(val, LOCAL_DEFAULT) is LOCAL_DEFAULT

    assert not alphaclops.has_kraus(val)


def test_kraus_returns_not_implemented():
    class ReturnsNotImplemented:
        def _kraus_(self):
            return NotImplemented

    assert_not_implemented(ReturnsNotImplemented())


def test_mixture_returns_not_implemented():
    class ReturnsNotImplemented:
        def _mixture_(self):
            return NotImplemented

    assert_not_implemented(ReturnsNotImplemented())


def test_unitary_returns_not_implemented():
    class ReturnsNotImplemented:
        def _unitary_(self):
            return NotImplemented

    with pytest.raises(TypeError, match='returned NotImplemented'):
        _ = alphaclops.kraus(ReturnsNotImplemented())
    assert alphaclops.kraus(ReturnsNotImplemented(), None) is None
    assert alphaclops.kraus(ReturnsNotImplemented(), NotImplemented) is NotImplemented
    assert alphaclops.kraus(ReturnsNotImplemented(), (1,)) == (1,)
    assert alphaclops.kraus(ReturnsNotImplemented(), LOCAL_DEFAULT) is LOCAL_DEFAULT


def test_explicit_kraus():
    a0 = np.array([[0, 0], [1, 0]])
    a1 = np.array([[1, 0], [0, 0]])
    c = (a0, a1)

    class ReturnsKraus:
        def _kraus_(self) -> Sequence[np.ndarray]:
            return c

    assert alphaclops.kraus(ReturnsKraus()) is c
    assert alphaclops.kraus(ReturnsKraus(), None) is c
    assert alphaclops.kraus(ReturnsKraus(), NotImplemented) is c
    assert alphaclops.kraus(ReturnsKraus(), (1,)) is c
    assert alphaclops.kraus(ReturnsKraus(), LOCAL_DEFAULT) is c

    assert alphaclops.has_kraus(ReturnsKraus())


def test_kraus_fallback_to_mixture():
    m = ((0.3, alphaclops.unitary(alphaclops.X)), (0.4, alphaclops.unitary(alphaclops.Y)), (0.3, alphaclops.unitary(alphaclops.Z)))

    class ReturnsMixture:
        def _mixture_(self) -> Iterable[Tuple[float, np.ndarray]]:
            return m

    c = (
        np.sqrt(0.3) * alphaclops.unitary(alphaclops.X),
        np.sqrt(0.4) * alphaclops.unitary(alphaclops.Y),
        np.sqrt(0.3) * alphaclops.unitary(alphaclops.Z),
    )

    np.testing.assert_equal(alphaclops.kraus(ReturnsMixture()), c)
    np.testing.assert_equal(alphaclops.kraus(ReturnsMixture(), None), c)
    np.testing.assert_equal(alphaclops.kraus(ReturnsMixture(), NotImplemented), c)
    np.testing.assert_equal(alphaclops.kraus(ReturnsMixture(), (1,)), c)
    np.testing.assert_equal(alphaclops.kraus(ReturnsMixture(), LOCAL_DEFAULT), c)

    assert alphaclops.has_kraus(ReturnsMixture())


def test_kraus_fallback_to_unitary():
    u = np.array([[1, 0], [1, 0]])

    class ReturnsUnitary:
        def _unitary_(self) -> np.ndarray:
            return u

    np.testing.assert_equal(alphaclops.kraus(ReturnsUnitary()), (u,))
    np.testing.assert_equal(alphaclops.kraus(ReturnsUnitary(), None), (u,))
    np.testing.assert_equal(alphaclops.kraus(ReturnsUnitary(), NotImplemented), (u,))
    np.testing.assert_equal(alphaclops.kraus(ReturnsUnitary(), (1,)), (u,))
    np.testing.assert_equal(alphaclops.kraus(ReturnsUnitary(), LOCAL_DEFAULT), (u,))

    assert alphaclops.has_kraus(ReturnsUnitary())


class HasKraus(alphaclops.testing.SingleQubitGate):
    def _has_kraus_(self) -> bool:
        return True


class HasMixture(alphaclops.testing.SingleQubitGate):
    def _has_mixture_(self) -> bool:
        return True


class HasUnitary(alphaclops.testing.SingleQubitGate):
    def _has_unitary_(self) -> bool:
        return True


class HasKrausWhenDecomposed(alphaclops.testing.SingleQubitGate):
    def __init__(self, decomposed_cls):
        self.decomposed_cls = decomposed_cls

    def _decompose_(self, qubits):
        return [self.decomposed_cls().on(q) for q in qubits]


@pytest.mark.parametrize('cls', [HasKraus, HasMixture, HasUnitary])
def test_has_kraus(cls):
    assert alphaclops.has_kraus(cls())


@pytest.mark.parametrize('decomposed_cls', [HasKraus, HasMixture, HasUnitary])
def test_has_kraus_when_decomposed(decomposed_cls):
    op = HasKrausWhenDecomposed(decomposed_cls).on(alphaclops.NamedQubit('test'))
    assert alphaclops.has_kraus(op)
    assert not alphaclops.has_kraus(op, allow_decompose=False)
