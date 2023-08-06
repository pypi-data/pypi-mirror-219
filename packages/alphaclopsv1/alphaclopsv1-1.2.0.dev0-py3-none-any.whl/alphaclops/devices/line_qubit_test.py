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


def test_init():
    q = alphaclops.LineQubit(1)
    assert q.x == 1

    q = alphaclops.LineQid(1, dimension=3)
    assert q.x == 1
    assert q.dimension == 3


def test_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.make_equality_group(lambda: alphaclops.LineQubit(1), lambda: alphaclops.LineQid(1, dimension=2))
    eq.add_equality_group(alphaclops.LineQubit(2))
    eq.add_equality_group(alphaclops.LineQubit(0))
    eq.add_equality_group(alphaclops.LineQid(1, dimension=3))


def test_str():
    assert str(alphaclops.LineQubit(5)) == 'q(5)'
    assert str(alphaclops.LineQid(5, dimension=3)) == 'q(5) (d=3)'


def test_repr():
    alphaclops.testing.assert_equivalent_repr(alphaclops.LineQubit(5))
    alphaclops.testing.assert_equivalent_repr(alphaclops.LineQid(5, dimension=3))


def test_cmp():
    order = alphaclops.testing.OrderTester()
    order.add_ascending_equivalence_group(alphaclops.LineQubit(0), alphaclops.LineQid(0, 2))
    order.add_ascending(
        alphaclops.LineQid(0, dimension=3),
        alphaclops.LineQid(1, dimension=1),
        alphaclops.LineQubit(1),
        alphaclops.LineQid(1, dimension=3),
        alphaclops.LineQid(2, dimension=1),
    )


def test_cmp_failure():
    with pytest.raises(TypeError, match='not supported between instances'):
        _ = 0 < alphaclops.LineQubit(1)
    with pytest.raises(TypeError, match='not supported between instances'):
        _ = alphaclops.LineQubit(1) < 0
    with pytest.raises(TypeError, match='not supported between instances'):
        _ = 0 < alphaclops.LineQid(1, 3)
    with pytest.raises(TypeError, match='not supported between instances'):
        _ = alphaclops.LineQid(1, 3) < 0


def test_is_adjacent():
    assert alphaclops.LineQubit(1).is_adjacent(alphaclops.LineQubit(2))
    assert alphaclops.LineQubit(1).is_adjacent(alphaclops.LineQubit(0))
    assert alphaclops.LineQubit(2).is_adjacent(alphaclops.LineQubit(3))
    assert not alphaclops.LineQubit(1).is_adjacent(alphaclops.LineQubit(3))
    assert not alphaclops.LineQubit(2).is_adjacent(alphaclops.LineQubit(0))

    assert alphaclops.LineQubit(2).is_adjacent(alphaclops.LineQid(3, 3))
    assert not alphaclops.LineQubit(2).is_adjacent(alphaclops.LineQid(0, 3))


def test_neighborhood():
    assert alphaclops.LineQubit(1).neighbors() == {alphaclops.LineQubit(0), alphaclops.LineQubit(2)}
    restricted_qubits = [alphaclops.LineQubit(2), alphaclops.LineQubit(3)]
    assert alphaclops.LineQubit(1).neighbors(restricted_qubits) == {alphaclops.LineQubit(2)}


def test_range():
    assert alphaclops.LineQubit.range(0) == []
    assert alphaclops.LineQubit.range(1) == [alphaclops.LineQubit(0)]
    assert alphaclops.LineQubit.range(2) == [alphaclops.LineQubit(0), alphaclops.LineQubit(1)]
    assert alphaclops.LineQubit.range(5) == [
        alphaclops.LineQubit(0),
        alphaclops.LineQubit(1),
        alphaclops.LineQubit(2),
        alphaclops.LineQubit(3),
        alphaclops.LineQubit(4),
    ]

    assert alphaclops.LineQubit.range(0, 0) == []
    assert alphaclops.LineQubit.range(0, 1) == [alphaclops.LineQubit(0)]
    assert alphaclops.LineQubit.range(1, 4) == [alphaclops.LineQubit(1), alphaclops.LineQubit(2), alphaclops.LineQubit(3)]

    assert alphaclops.LineQubit.range(3, 1, -1) == [alphaclops.LineQubit(3), alphaclops.LineQubit(2)]
    assert alphaclops.LineQubit.range(3, 5, -1) == []
    assert alphaclops.LineQubit.range(1, 5, 2) == [alphaclops.LineQubit(1), alphaclops.LineQubit(3)]


def test_qid_range():
    assert alphaclops.LineQid.range(0, dimension=3) == []
    assert alphaclops.LineQid.range(1, dimension=3) == [alphaclops.LineQid(0, 3)]
    assert alphaclops.LineQid.range(2, dimension=3) == [alphaclops.LineQid(0, 3), alphaclops.LineQid(1, 3)]
    assert alphaclops.LineQid.range(5, dimension=3) == [
        alphaclops.LineQid(0, 3),
        alphaclops.LineQid(1, 3),
        alphaclops.LineQid(2, 3),
        alphaclops.LineQid(3, 3),
        alphaclops.LineQid(4, 3),
    ]

    assert alphaclops.LineQid.range(0, 0, dimension=4) == []
    assert alphaclops.LineQid.range(0, 1, dimension=4) == [alphaclops.LineQid(0, 4)]
    assert alphaclops.LineQid.range(1, 4, dimension=4) == [
        alphaclops.LineQid(1, 4),
        alphaclops.LineQid(2, 4),
        alphaclops.LineQid(3, 4),
    ]

    assert alphaclops.LineQid.range(3, 1, -1, dimension=1) == [alphaclops.LineQid(3, 1), alphaclops.LineQid(2, 1)]
    assert alphaclops.LineQid.range(3, 5, -1, dimension=2) == []
    assert alphaclops.LineQid.range(1, 5, 2, dimension=2) == [alphaclops.LineQid(1, 2), alphaclops.LineQid(3, 2)]


def test_for_qid_shape():
    assert alphaclops.LineQid.for_qid_shape(()) == []
    assert alphaclops.LineQid.for_qid_shape((4, 2, 3, 1)) == [
        alphaclops.LineQid(0, 4),
        alphaclops.LineQid(1, 2),
        alphaclops.LineQid(2, 3),
        alphaclops.LineQid(3, 1),
    ]
    assert alphaclops.LineQid.for_qid_shape((4, 2, 3, 1), start=5) == [
        alphaclops.LineQid(5, 4),
        alphaclops.LineQid(6, 2),
        alphaclops.LineQid(7, 3),
        alphaclops.LineQid(8, 1),
    ]
    assert alphaclops.LineQid.for_qid_shape((4, 2, 3, 1), step=2) == [
        alphaclops.LineQid(0, 4),
        alphaclops.LineQid(2, 2),
        alphaclops.LineQid(4, 3),
        alphaclops.LineQid(6, 1),
    ]
    assert alphaclops.LineQid.for_qid_shape((4, 2, 3, 1), start=5, step=-1) == [
        alphaclops.LineQid(5, 4),
        alphaclops.LineQid(4, 2),
        alphaclops.LineQid(3, 3),
        alphaclops.LineQid(2, 1),
    ]


def test_addition_subtraction():
    assert alphaclops.LineQubit(1) + 2 == alphaclops.LineQubit(3)
    assert alphaclops.LineQubit(3) - 1 == alphaclops.LineQubit(2)
    assert 1 + alphaclops.LineQubit(4) == alphaclops.LineQubit(5)
    assert 5 - alphaclops.LineQubit(3) == alphaclops.LineQubit(2)

    assert alphaclops.LineQid(1, 3) + 2 == alphaclops.LineQid(3, 3)
    assert alphaclops.LineQid(3, 3) - 1 == alphaclops.LineQid(2, 3)
    assert 1 + alphaclops.LineQid(4, 3) == alphaclops.LineQid(5, 3)
    assert 5 - alphaclops.LineQid(3, 3) == alphaclops.LineQid(2, 3)

    assert alphaclops.LineQid(1, dimension=3) + alphaclops.LineQid(3, dimension=3) == alphaclops.LineQid(
        4, dimension=3
    )
    assert alphaclops.LineQid(3, dimension=3) - alphaclops.LineQid(2, dimension=3) == alphaclops.LineQid(
        1, dimension=3
    )


def test_addition_subtraction_type_error():
    with pytest.raises(TypeError, match='dave'):
        _ = alphaclops.LineQubit(1) + 'dave'
    with pytest.raises(TypeError, match='dave'):
        _ = alphaclops.LineQubit(1) - 'dave'

    with pytest.raises(TypeError, match='dave'):
        _ = alphaclops.LineQid(1, 3) + 'dave'
    with pytest.raises(TypeError, match='dave'):
        _ = alphaclops.LineQid(1, 3) - 'dave'

    with pytest.raises(TypeError, match="Can only add LineQids with identical dimension."):
        _ = alphaclops.LineQid(5, dimension=3) + alphaclops.LineQid(3, dimension=4)

    with pytest.raises(TypeError, match="Can only subtract LineQids with identical dimension."):
        _ = alphaclops.LineQid(5, dimension=3) - alphaclops.LineQid(3, dimension=4)


def test_neg():
    assert -alphaclops.LineQubit(1) == alphaclops.LineQubit(-1)
    assert -alphaclops.LineQid(1, dimension=3) == alphaclops.LineQid(-1, dimension=3)


def test_json_dict():
    assert alphaclops.LineQubit(5)._json_dict_() == {'x': 5}
    assert alphaclops.LineQid(5, 3)._json_dict_() == {'x': 5, 'dimension': 3}


def test_for_gate():
    class NoQidGate:
        def _qid_shape_(self):
            return ()

    class QuditGate:
        def _qid_shape_(self):
            return (4, 2, 3, 1)

    assert alphaclops.LineQid.for_gate(NoQidGate()) == []
    assert alphaclops.LineQid.for_gate(QuditGate()) == [
        alphaclops.LineQid(0, 4),
        alphaclops.LineQid(1, 2),
        alphaclops.LineQid(2, 3),
        alphaclops.LineQid(3, 1),
    ]
    assert alphaclops.LineQid.for_gate(QuditGate(), start=5) == [
        alphaclops.LineQid(5, 4),
        alphaclops.LineQid(6, 2),
        alphaclops.LineQid(7, 3),
        alphaclops.LineQid(8, 1),
    ]
    assert alphaclops.LineQid.for_gate(QuditGate(), step=2) == [
        alphaclops.LineQid(0, 4),
        alphaclops.LineQid(2, 2),
        alphaclops.LineQid(4, 3),
        alphaclops.LineQid(6, 1),
    ]
    assert alphaclops.LineQid.for_gate(QuditGate(), start=5, step=-1) == [
        alphaclops.LineQid(5, 4),
        alphaclops.LineQid(4, 2),
        alphaclops.LineQid(3, 3),
        alphaclops.LineQid(2, 1),
    ]


def test_immutable():
    # Match one of two strings. The second one is message returned since python 3.11.
    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'x' of 'LineQubit' object has no setter)",
    ):
        q = alphaclops.LineQubit(5)
        q.x = 6

    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'x' of 'LineQid' object has no setter)",
    ):
        q = alphaclops.LineQid(5, dimension=4)
        q.x = 6


def test_numeric():
    assert int(alphaclops.LineQubit(x=5)) == 5
    assert float(alphaclops.LineQubit(x=5)) == 5
    assert complex(alphaclops.LineQubit(x=5)) == 5 + 0j
    assert isinstance(int(alphaclops.LineQubit(x=5)), int)
    assert isinstance(float(alphaclops.LineQubit(x=5)), float)
    assert isinstance(complex(alphaclops.LineQubit(x=5)), complex)
