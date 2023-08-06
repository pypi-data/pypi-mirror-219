# Copyright 2021 The alphaclops Developers
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


def test_default():
    a2 = alphaclops.NamedQubit('a2')
    a10 = alphaclops.NamedQubit('a10')
    b = alphaclops.NamedQubit('b')
    q4 = alphaclops.LineQubit(4)
    q5 = alphaclops.LineQubit(5)
    assert alphaclops.QubitOrder.DEFAULT.order_for([]) == ()
    assert alphaclops.QubitOrder.DEFAULT.order_for([a10, a2, b]) == (a2, a10, b)
    assert sorted([]) == []
    assert sorted([a10, a2, b]) == [a2, a10, b]
    assert sorted([q5, a10, a2, b, q4]) == [q4, q5, a2, a10, b]


def test_default_grouping():
    presorted = (
        alphaclops.TensorCircuit(0, 1),
        alphaclops.TensorCircuit(1, 0),
        alphaclops.TensorCircuit(999, 999),
        alphaclops.LineQubit(0),
        alphaclops.LineQubit(1),
        alphaclops.LineQubit(999),
        alphaclops.NamedQubit(''),
        alphaclops.NamedQubit('0'),
        alphaclops.NamedQubit('1'),
        alphaclops.NamedQubit('999'),
        alphaclops.NamedQubit('a'),
    )
    assert alphaclops.QubitOrder.DEFAULT.order_for(presorted) == presorted
    assert alphaclops.QubitOrder.DEFAULT.order_for(reversed(presorted)) == presorted


def test_explicit():
    a2 = alphaclops.NamedQubit('a2')
    a10 = alphaclops.NamedQubit('a10')
    b = alphaclops.NamedQubit('b')
    with pytest.raises(ValueError):
        _ = alphaclops.QubitOrder.explicit([b, b])
    q = alphaclops.QubitOrder.explicit([a10, a2, b])
    assert q.order_for([b]) == (a10, a2, b)
    assert q.order_for([a2]) == (a10, a2, b)
    assert q.order_for([]) == (a10, a2, b)
    with pytest.raises(ValueError):
        _ = q.order_for([alphaclops.NamedQubit('c')])


def test_explicit_with_fallback():
    a2 = alphaclops.NamedQubit('a2')
    a10 = alphaclops.NamedQubit('a10')
    b = alphaclops.NamedQubit('b')
    q = alphaclops.QubitOrder.explicit([b], fallback=alphaclops.QubitOrder.DEFAULT)
    assert q.order_for([]) == (b,)
    assert q.order_for([b]) == (b,)
    assert q.order_for([b, a2]) == (b, a2)
    assert q.order_for([a2]) == (b, a2)
    assert q.order_for([a10, a2]) == (b, a2, a10)


def test_sorted_by():
    a = alphaclops.NamedQubit('2')
    b = alphaclops.NamedQubit('10')
    c = alphaclops.NamedQubit('-5')

    q = alphaclops.QubitOrder.sorted_by(lambda e: -int(str(e)))
    assert q.order_for([]) == ()
    assert q.order_for([a]) == (a,)
    assert q.order_for([a, b]) == (b, a)
    assert q.order_for([a, b, c]) == (b, a, c)


def test_map():
    b = alphaclops.NamedQubit('b!')
    q = alphaclops.QubitOrder.explicit([alphaclops.NamedQubit('b')]).map(
        internalize=lambda e: alphaclops.NamedQubit(e.name[:-1]),
        externalize=lambda e: alphaclops.NamedQubit(e.name + '!'),
    )

    assert q.order_for([]) == (b,)
    assert q.order_for([b]) == (b,)


def test_qubit_order_or_list():
    b = alphaclops.NamedQubit('b')

    implied_by_list = alphaclops.QubitOrder.as_qubit_order([b])
    assert implied_by_list.order_for([]) == (b,)

    implied_by_generator = alphaclops.QubitOrder.as_qubit_order(
        alphaclops.NamedQubit(e.name + '!') for e in [b]
    )
    assert implied_by_generator.order_for([]) == (alphaclops.NamedQubit('b!'),)
    assert implied_by_generator.order_for([]) == (alphaclops.NamedQubit('b!'),)

    ordered = alphaclops.QubitOrder.sorted_by(repr)
    passed_through = alphaclops.QubitOrder.as_qubit_order(ordered)
    assert ordered is passed_through


def test_qubit_order_iterator():
    generator = (q for q in alphaclops.LineQubit.range(5))
    assert alphaclops.QubitOrder.explicit(generator).order_for((alphaclops.LineQubit(3),)) == tuple(
        alphaclops.LineQubit.range(5)
    )

    generator = (q for q in alphaclops.LineQubit.range(5))
    assert alphaclops.QubitOrder.as_qubit_order(generator).order_for((alphaclops.LineQubit(3),)) == tuple(
        alphaclops.LineQubit.range(5)
    )


def test_qubit_order_invalid():
    with pytest.raises(ValueError, match="Don't know how to interpret <5> as a Basis."):
        _ = alphaclops.QubitOrder.as_qubit_order(5)
