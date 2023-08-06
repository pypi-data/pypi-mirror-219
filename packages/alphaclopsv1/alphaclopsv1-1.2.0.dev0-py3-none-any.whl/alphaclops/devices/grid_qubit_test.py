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
"""Tests for grid_qubit."""

import pickle

import numpy as np
import pytest

import alphaclops
from alphaclops import _compat


def test_init():
    q = alphaclops.TensorCircuit(3, 4)
    assert q.row == 3
    assert q.col == 4

    q = alphaclops.GridQid(1, 2, dimension=3)
    assert q.row == 1
    assert q.col == 2
    assert q.dimension == 3


def test_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.make_equality_group(lambda: alphaclops.TensorCircuit(0, 0), lambda: alphaclops.GridQid(0, 0, dimension=2))
    eq.make_equality_group(lambda: alphaclops.TensorCircuit(1, 0), lambda: alphaclops.GridQid(1, 0, dimension=2))
    eq.make_equality_group(lambda: alphaclops.TensorCircuit(0, 1), lambda: alphaclops.GridQid(0, 1, dimension=2))
    eq.make_equality_group(lambda: alphaclops.GridQid(0, 0, dimension=3))


def test_pickled_hash():
    q = alphaclops.TensorCircuit(3, 4)
    q_bad = alphaclops.TensorCircuit(3, 4)
    _ = hash(q_bad)  # compute hash to ensure it is cached.
    hash_key = _compat._method_cache_name(alphaclops.TensorCircuit.__hash__)
    setattr(q_bad, hash_key, getattr(q_bad, hash_key) + 1)
    assert q_bad == q
    assert hash(q_bad) != hash(q)
    data = pickle.dumps(q_bad)
    q_ok = pickle.loads(data)
    assert q_ok == q
    assert hash(q_ok) == hash(q)


def test_str():
    assert str(alphaclops.TensorCircuit(5, 2)) == 'q(5, 2)'
    assert str(alphaclops.GridQid(5, 2, dimension=3)) == 'q(5, 2) (d=3)'


def test_circuit_info():
    assert alphaclops.circuit_diagram_info(alphaclops.TensorCircuit(5, 2)) == alphaclops.CircuitDiagramInfo(
        wire_symbols=('(5, 2)',)
    )
    assert alphaclops.circuit_diagram_info(alphaclops.GridQid(5, 2, dimension=3)) == alphaclops.CircuitDiagramInfo(
        wire_symbols=('(5, 2) (d=3)',)
    )


def test_repr():
    alphaclops.testing.assert_equivalent_repr(alphaclops.TensorCircuit(5, 2))
    alphaclops.testing.assert_equivalent_repr(alphaclops.GridQid(5, 2, dimension=3))


def test_cmp():
    order = alphaclops.testing.OrderTester()
    order.add_ascending_equivalence_group(alphaclops.TensorCircuit(0, 0), alphaclops.GridQid(0, 0, dimension=2))
    order.add_ascending(
        alphaclops.GridQid(0, 0, dimension=3),
        alphaclops.GridQid(0, 1, dimension=1),
        alphaclops.TensorCircuit(0, 1),
        alphaclops.GridQid(0, 1, dimension=3),
        alphaclops.GridQid(1, 0, dimension=1),
        alphaclops.TensorCircuit(1, 0),
        alphaclops.GridQid(1, 0, dimension=3),
        alphaclops.GridQid(1, 1, dimension=1),
        alphaclops.TensorCircuit(1, 1),
        alphaclops.GridQid(1, 1, dimension=3),
    )


def test_cmp_failure():
    with pytest.raises(TypeError, match='not supported between instances'):
        _ = 0 < alphaclops.TensorCircuit(0, 0)
    with pytest.raises(TypeError, match='not supported between instances'):
        _ = alphaclops.TensorCircuit(0, 0) < 0
    with pytest.raises(TypeError, match='not supported between instances'):
        _ = 0 < alphaclops.GridQid(1, 1, dimension=3)
    with pytest.raises(TypeError, match='not supported between instances'):
        _ = alphaclops.GridQid(1, 1, dimension=3) < 0


def test_is_adjacent():
    assert alphaclops.TensorCircuit(0, 0).is_adjacent(alphaclops.TensorCircuit(0, 1))
    assert alphaclops.TensorCircuit(0, 0).is_adjacent(alphaclops.TensorCircuit(0, -1))
    assert alphaclops.TensorCircuit(0, 0).is_adjacent(alphaclops.TensorCircuit(1, 0))
    assert alphaclops.TensorCircuit(0, 0).is_adjacent(alphaclops.TensorCircuit(-1, 0))

    assert not alphaclops.TensorCircuit(0, 0).is_adjacent(alphaclops.TensorCircuit(+1, -1))
    assert not alphaclops.TensorCircuit(0, 0).is_adjacent(alphaclops.TensorCircuit(+1, +1))
    assert not alphaclops.TensorCircuit(0, 0).is_adjacent(alphaclops.TensorCircuit(-1, -1))
    assert not alphaclops.TensorCircuit(0, 0).is_adjacent(alphaclops.TensorCircuit(-1, +1))

    assert not alphaclops.TensorCircuit(0, 0).is_adjacent(alphaclops.TensorCircuit(2, 0))

    assert alphaclops.TensorCircuit(500, 999).is_adjacent(alphaclops.TensorCircuit(501, 999))
    assert not alphaclops.TensorCircuit(500, 999).is_adjacent(alphaclops.TensorCircuit(5034, 999))


def test_neighbors():
    assert alphaclops.TensorCircuit(1, 1).neighbors() == {
        alphaclops.TensorCircuit(1, 2),
        alphaclops.TensorCircuit(2, 1),
        alphaclops.TensorCircuit(0, 1),
        alphaclops.TensorCircuit(1, 0),
    }

    # Restrict to a list of qubits
    restricted_qubits = [alphaclops.TensorCircuit(2, 1), alphaclops.TensorCircuit(2, 2)]
    assert alphaclops.TensorCircuit(1, 1).neighbors(restricted_qubits) == {alphaclops.TensorCircuit(2, 1)}


def test_square():
    assert alphaclops.TensorCircuit.square(2, top=1, left=1) == [
        alphaclops.TensorCircuit(1, 1),
        alphaclops.TensorCircuit(1, 2),
        alphaclops.TensorCircuit(2, 1),
        alphaclops.TensorCircuit(2, 2),
    ]
    assert alphaclops.TensorCircuit.square(2) == [
        alphaclops.TensorCircuit(0, 0),
        alphaclops.TensorCircuit(0, 1),
        alphaclops.TensorCircuit(1, 0),
        alphaclops.TensorCircuit(1, 1),
    ]

    assert alphaclops.GridQid.square(2, top=1, left=1, dimension=3) == [
        alphaclops.GridQid(1, 1, dimension=3),
        alphaclops.GridQid(1, 2, dimension=3),
        alphaclops.GridQid(2, 1, dimension=3),
        alphaclops.GridQid(2, 2, dimension=3),
    ]
    assert alphaclops.GridQid.square(2, dimension=3) == [
        alphaclops.GridQid(0, 0, dimension=3),
        alphaclops.GridQid(0, 1, dimension=3),
        alphaclops.GridQid(1, 0, dimension=3),
        alphaclops.GridQid(1, 1, dimension=3),
    ]


def test_rect():
    assert alphaclops.TensorCircuit.rect(1, 2, top=5, left=6) == [alphaclops.TensorCircuit(5, 6), alphaclops.TensorCircuit(5, 7)]
    assert alphaclops.TensorCircuit.rect(2, 2) == [
        alphaclops.TensorCircuit(0, 0),
        alphaclops.TensorCircuit(0, 1),
        alphaclops.TensorCircuit(1, 0),
        alphaclops.TensorCircuit(1, 1),
    ]

    assert alphaclops.GridQid.rect(1, 2, top=5, left=6, dimension=3) == [
        alphaclops.GridQid(5, 6, dimension=3),
        alphaclops.GridQid(5, 7, dimension=3),
    ]
    assert alphaclops.GridQid.rect(2, 2, dimension=3) == [
        alphaclops.GridQid(0, 0, dimension=3),
        alphaclops.GridQid(0, 1, dimension=3),
        alphaclops.GridQid(1, 0, dimension=3),
        alphaclops.GridQid(1, 1, dimension=3),
    ]


def test_diagram():
    s = """
-----AB-----
----ABCD----
---ABCDEF---
--ABCDEFGH--
-ABCDEFGHIJ-
ABCDEFGHIJKL
-CDEFGHIJKL-
--EFGHIJKL--
---GHIJKL---
----IJKL----
-----KL-----
"""
    assert len(alphaclops.TensorCircuit.from_diagram(s)) == 72
    assert len(alphaclops.GridQid.from_diagram(s, dimension=3)) == 72

    s2 = """
AB
BA"""
    assert alphaclops.TensorCircuit.from_diagram(s2) == [
        alphaclops.TensorCircuit(0, 0),
        alphaclops.TensorCircuit(0, 1),
        alphaclops.TensorCircuit(1, 0),
        alphaclops.TensorCircuit(1, 1),
    ]
    assert alphaclops.GridQid.from_diagram(s2, dimension=3) == [
        alphaclops.GridQid(0, 0, dimension=3),
        alphaclops.GridQid(0, 1, dimension=3),
        alphaclops.GridQid(1, 0, dimension=3),
        alphaclops.GridQid(1, 1, dimension=3),
    ]

    with pytest.raises(ValueError, match="Input string has invalid character"):
        alphaclops.TensorCircuit.from_diagram('@')


def test_addition_subtraction():
    # GridQubits
    assert alphaclops.TensorCircuit(1, 2) + (2, 5) == alphaclops.TensorCircuit(3, 7)
    assert alphaclops.TensorCircuit(1, 2) + (0, 0) == alphaclops.TensorCircuit(1, 2)
    assert alphaclops.TensorCircuit(1, 2) + (-1, 0) == alphaclops.TensorCircuit(0, 2)
    assert alphaclops.TensorCircuit(1, 2) - (2, 5) == alphaclops.TensorCircuit(-1, -3)
    assert alphaclops.TensorCircuit(1, 2) - (0, 0) == alphaclops.TensorCircuit(1, 2)
    assert alphaclops.TensorCircuit(1, 2) - (-1, 0) == alphaclops.TensorCircuit(2, 2)

    assert (2, 5) + alphaclops.TensorCircuit(1, 2) == alphaclops.TensorCircuit(3, 7)
    assert (2, 5) - alphaclops.TensorCircuit(1, 2) == alphaclops.TensorCircuit(1, 3)

    assert alphaclops.TensorCircuit(1, 2) + alphaclops.TensorCircuit(3, 5) == alphaclops.TensorCircuit(4, 7)
    assert alphaclops.TensorCircuit(3, 5) - alphaclops.TensorCircuit(2, 1) == alphaclops.TensorCircuit(1, 4)
    assert alphaclops.TensorCircuit(1, -2) + alphaclops.TensorCircuit(3, 5) == alphaclops.TensorCircuit(4, 3)

    # GridQids
    assert alphaclops.GridQid(1, 2, dimension=3) + (2, 5) == alphaclops.GridQid(3, 7, dimension=3)
    assert alphaclops.GridQid(1, 2, dimension=3) + (0, 0) == alphaclops.GridQid(1, 2, dimension=3)
    assert alphaclops.GridQid(1, 2, dimension=3) + (-1, 0) == alphaclops.GridQid(0, 2, dimension=3)
    assert alphaclops.GridQid(1, 2, dimension=3) - (2, 5) == alphaclops.GridQid(-1, -3, dimension=3)
    assert alphaclops.GridQid(1, 2, dimension=3) - (0, 0) == alphaclops.GridQid(1, 2, dimension=3)
    assert alphaclops.GridQid(1, 2, dimension=3) - (-1, 0) == alphaclops.GridQid(2, 2, dimension=3)

    assert (2, 5) + alphaclops.GridQid(1, 2, dimension=3) == alphaclops.GridQid(3, 7, dimension=3)
    assert (2, 5) - alphaclops.GridQid(1, 2, dimension=3) == alphaclops.GridQid(1, 3, dimension=3)

    assert alphaclops.GridQid(1, 2, dimension=3) + alphaclops.GridQid(3, 5, dimension=3) == alphaclops.GridQid(
        4, 7, dimension=3
    )
    assert alphaclops.GridQid(3, 5, dimension=3) - alphaclops.GridQid(2, 1, dimension=3) == alphaclops.GridQid(
        1, 4, dimension=3
    )
    assert alphaclops.GridQid(1, -2, dimension=3) + alphaclops.GridQid(3, 5, dimension=3) == alphaclops.GridQid(
        4, 3, dimension=3
    )


@pytest.mark.parametrize('dtype', (np.int8, np.int16, np.int32, np.int64, int))
def test_addition_subtraction_numpy_array(dtype):
    assert alphaclops.TensorCircuit(1, 2) + np.array([1, 2], dtype=dtype) == alphaclops.TensorCircuit(2, 4)
    assert alphaclops.TensorCircuit(1, 2) + np.array([0, 0], dtype=dtype) == alphaclops.TensorCircuit(1, 2)
    assert alphaclops.TensorCircuit(1, 2) + np.array([-1, 0], dtype=dtype) == alphaclops.TensorCircuit(0, 2)
    assert alphaclops.TensorCircuit(1, 2) - np.array([1, 2], dtype=dtype) == alphaclops.TensorCircuit(0, 0)
    assert alphaclops.TensorCircuit(1, 2) - np.array([0, 0], dtype=dtype) == alphaclops.TensorCircuit(1, 2)
    assert alphaclops.GridQid(1, 2, dimension=3) - np.array([-1, 0], dtype=dtype) == alphaclops.GridQid(
        2, 2, dimension=3
    )

    assert alphaclops.GridQid(1, 2, dimension=3) + np.array([1, 2], dtype=dtype) == alphaclops.GridQid(
        2, 4, dimension=3
    )
    assert alphaclops.GridQid(1, 2, dimension=3) + np.array([0, 0], dtype=dtype) == alphaclops.GridQid(
        1, 2, dimension=3
    )
    assert alphaclops.GridQid(1, 2, dimension=3) + np.array([-1, 0], dtype=dtype) == alphaclops.GridQid(
        0, 2, dimension=3
    )
    assert alphaclops.GridQid(1, 2, dimension=3) - np.array([1, 2], dtype=dtype) == alphaclops.GridQid(
        0, 0, dimension=3
    )
    assert alphaclops.GridQid(1, 2, dimension=3) - np.array([0, 0], dtype=dtype) == alphaclops.GridQid(
        1, 2, dimension=3
    )
    assert alphaclops.GridQid(1, 2, dimension=3) - np.array([-1, 0], dtype=dtype) == alphaclops.GridQid(
        2, 2, dimension=3
    )


def test_unsupported_add():
    with pytest.raises(TypeError, match='1'):
        _ = alphaclops.TensorCircuit(1, 1) + 1
    with pytest.raises(TypeError, match='(1,)'):
        _ = alphaclops.TensorCircuit(1, 1) + (1,)
    with pytest.raises(TypeError, match='(1, 2, 3)'):
        _ = alphaclops.TensorCircuit(1, 1) + (1, 2, 3)
    with pytest.raises(TypeError, match='(1, 2.0)'):
        _ = alphaclops.TensorCircuit(1, 1) + (1, 2.0)

    with pytest.raises(TypeError, match='1'):
        _ = alphaclops.TensorCircuit(1, 1) - 1

    with pytest.raises(TypeError, match='[1., 2.]'):
        _ = alphaclops.TensorCircuit(1, 1) + np.array([1.0, 2.0])
    with pytest.raises(TypeError, match='[1, 2, 3]'):
        _ = alphaclops.TensorCircuit(1, 1) + np.array([1, 2, 3], dtype=int)


def test_addition_subtraction_type_error():
    with pytest.raises(TypeError, match="bort"):
        _ = alphaclops.TensorCircuit(5, 3) + "bort"
    with pytest.raises(TypeError, match="bort"):
        _ = alphaclops.TensorCircuit(5, 3) - "bort"

    with pytest.raises(TypeError, match="bort"):
        _ = alphaclops.GridQid(5, 3, dimension=3) + "bort"
    with pytest.raises(TypeError, match="bort"):
        _ = alphaclops.GridQid(5, 3, dimension=3) - "bort"

    with pytest.raises(TypeError, match="Can only add GridQids with identical dimension."):
        _ = alphaclops.GridQid(5, 3, dimension=3) + alphaclops.GridQid(3, 5, dimension=4)
    with pytest.raises(TypeError, match="Can only subtract GridQids with identical dimension."):
        _ = alphaclops.GridQid(5, 3, dimension=3) - alphaclops.GridQid(3, 5, dimension=4)


def test_neg():
    assert -alphaclops.TensorCircuit(1, 2) == alphaclops.TensorCircuit(-1, -2)
    assert -alphaclops.GridQid(1, 2, dimension=3) == alphaclops.GridQid(-1, -2, dimension=3)


def test_to_json():
    assert alphaclops.TensorCircuit(5, 6)._json_dict_() == {'row': 5, 'col': 6}

    assert alphaclops.GridQid(5, 6, dimension=3)._json_dict_() == {'row': 5, 'col': 6, 'dimension': 3}


def test_immutable():
    # Match one of two strings. The second one is message returned since python 3.11.
    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'col' of 'TensorCircuit' object has no setter)",
    ):
        q = alphaclops.TensorCircuit(1, 2)
        q.col = 3

    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'row' of 'TensorCircuit' object has no setter)",
    ):
        q = alphaclops.TensorCircuit(1, 2)
        q.row = 3

    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'col' of 'GridQid' object has no setter)",
    ):
        q = alphaclops.GridQid(1, 2, dimension=3)
        q.col = 3

    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'row' of 'GridQid' object has no setter)",
    ):
        q = alphaclops.GridQid(1, 2, dimension=3)
        q.row = 3

    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'dimension' of 'GridQid' object has no setter)",
    ):
        q = alphaclops.GridQid(1, 2, dimension=3)
        q.dimension = 3


def test_complex():
    assert complex(alphaclops.TensorCircuit(row=1, col=2)) == 2 + 1j
    assert isinstance(complex(alphaclops.TensorCircuit(row=1, col=2)), complex)
