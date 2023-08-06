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
"""Tests exclusively for FrozenCircuits.

Behavior shared with Circuit is tested with parameters in circuit_test.py.
"""

import pytest

import alphaclops


def test_from_moments():
    a, b, c, d = alphaclops.LineQubit.range(4)
    assert alphaclops.FrozenCircuit.from_moments(
        [alphaclops.X(a), alphaclops.Y(b)],
        [alphaclops.X(c)],
        [],
        alphaclops.Z(d),
        [alphaclops.measure(a, b, key='ab'), alphaclops.measure(c, d, key='cd')],
    ) == alphaclops.FrozenCircuit(
        alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b)),
        alphaclops.Moment(alphaclops.X(c)),
        alphaclops.Moment(),
        alphaclops.Moment(alphaclops.Z(d)),
        alphaclops.Moment(alphaclops.measure(a, b, key='ab'), alphaclops.measure(c, d, key='cd')),
    )


def test_freeze_and_unfreeze():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.X(a), alphaclops.H(b))

    f = c.freeze()
    # Circuits equal their frozen versions, similar to set(x) == frozenset(x).
    assert f == c
    assert alphaclops.approx_eq(f, c)

    # Freezing a FrozenCircuit will return the original.
    ff = f.freeze()
    assert ff is f

    unf = f.unfreeze()
    assert unf.moments == c.moments
    assert unf is not c

    # Unfreezing always returns a copy.
    cc = c.unfreeze()
    assert cc is not c

    fcc = cc.freeze()
    assert fcc.moments == f.moments
    assert fcc is not f


def test_immutable():
    q = alphaclops.LineQubit(0)
    c = alphaclops.FrozenCircuit(alphaclops.X(q), alphaclops.H(q))

    # Match one of two strings. The second one is message returned since python 3.11.
    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'moments' of 'FrozenCircuit' object has no setter)",
    ):
        c.moments = (alphaclops.Moment(alphaclops.H(q)), alphaclops.Moment(alphaclops.X(q)))
