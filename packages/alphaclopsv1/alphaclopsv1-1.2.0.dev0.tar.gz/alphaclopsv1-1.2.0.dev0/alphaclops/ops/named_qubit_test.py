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

import alphaclops
from alphaclops.ops.named_qubit import _pad_digits


def test_init():
    q = alphaclops.NamedQubit('a')
    assert q.name == 'a'

    q = alphaclops.NamedQid('a', dimension=3)
    assert q.name == 'a'
    assert q.dimension == 3


def test_named_qubit_str():
    q = alphaclops.NamedQubit('a')
    assert q.name == 'a'
    assert str(q) == 'a'
    qid = alphaclops.NamedQid('a', dimension=3)
    assert qid.name == 'a'
    assert str(qid) == 'a (d=3)'


def test_named_qubit_repr():
    q = alphaclops.NamedQubit('a')
    assert repr(q) == "alphaclops.NamedQubit('a')"
    qid = alphaclops.NamedQid('a', dimension=3)
    assert repr(qid) == "alphaclops.NamedQid('a', dimension=3)"


def test_named_qubit_order():
    order = alphaclops.testing.OrderTester()
    order.add_ascending(
        alphaclops.NamedQid('', dimension=1),
        alphaclops.NamedQubit(''),
        alphaclops.NamedQid('', dimension=3),
        alphaclops.NamedQid('1', dimension=1),
        alphaclops.NamedQubit('1'),
        alphaclops.NamedQid('1', dimension=3),
        alphaclops.NamedQid('a', dimension=1),
        alphaclops.NamedQubit('a'),
        alphaclops.NamedQid('a', dimension=3),
        alphaclops.NamedQid('a00000000', dimension=1),
        alphaclops.NamedQubit('a00000000'),
        alphaclops.NamedQid('a00000000', dimension=3),
        alphaclops.NamedQid('a00000000:8', dimension=1),
        alphaclops.NamedQubit('a00000000:8'),
        alphaclops.NamedQid('a00000000:8', dimension=3),
        alphaclops.NamedQid('a9', dimension=1),
        alphaclops.NamedQubit('a9'),
        alphaclops.NamedQid('a9', dimension=3),
        alphaclops.NamedQid('a09', dimension=1),
        alphaclops.NamedQubit('a09'),
        alphaclops.NamedQid('a09', dimension=3),
        alphaclops.NamedQid('a10', dimension=1),
        alphaclops.NamedQubit('a10'),
        alphaclops.NamedQid('a10', dimension=3),
        alphaclops.NamedQid('a11', dimension=1),
        alphaclops.NamedQubit('a11'),
        alphaclops.NamedQid('a11', dimension=3),
        alphaclops.NamedQid('aa', dimension=1),
        alphaclops.NamedQubit('aa'),
        alphaclops.NamedQid('aa', dimension=3),
        alphaclops.NamedQid('ab', dimension=1),
        alphaclops.NamedQubit('ab'),
        alphaclops.NamedQid('ab', dimension=3),
        alphaclops.NamedQid('b', dimension=1),
        alphaclops.NamedQubit('b'),
        alphaclops.NamedQid('b', dimension=3),
    )
    order.add_ascending_equivalence_group(
        alphaclops.NamedQubit('c'),
        alphaclops.NamedQubit('c'),
        alphaclops.NamedQid('c', dimension=2),
        alphaclops.NamedQid('c', dimension=2),
    )


def test_pad_digits():
    assert _pad_digits('') == ''
    assert _pad_digits('a') == 'a'
    assert _pad_digits('a0') == 'a00000000:1'
    assert _pad_digits('a00') == 'a00000000:2'
    assert _pad_digits('a1bc23') == 'a00000001:1bc00000023:2'
    assert _pad_digits('a9') == 'a00000009:1'
    assert _pad_digits('a09') == 'a00000009:2'
    assert _pad_digits('a00000000:8') == 'a00000000:8:00000008:1'


def test_named_qubit_range():
    qubits = alphaclops.NamedQubit.range(2, prefix='a')
    assert qubits == [alphaclops.NamedQubit('a0'), alphaclops.NamedQubit('a1')]

    qubits = alphaclops.NamedQubit.range(-1, 4, 2, prefix='a')
    assert qubits == [alphaclops.NamedQubit('a-1'), alphaclops.NamedQubit('a1'), alphaclops.NamedQubit('a3')]


def test_named_qid_range():
    qids = alphaclops.NamedQid.range(2, prefix='a', dimension=3)
    assert qids == [alphaclops.NamedQid('a0', dimension=3), alphaclops.NamedQid('a1', dimension=3)]

    qids = alphaclops.NamedQid.range(-1, 4, 2, prefix='a', dimension=3)
    assert qids == [
        alphaclops.NamedQid('a-1', dimension=3),
        alphaclops.NamedQid('a1', dimension=3),
        alphaclops.NamedQid('a3', dimension=3),
    ]

    qids = alphaclops.NamedQid.range(2, prefix='a', dimension=4)
    assert qids == [alphaclops.NamedQid('a0', dimension=4), alphaclops.NamedQid('a1', dimension=4)]

    qids = alphaclops.NamedQid.range(-1, 4, 2, prefix='a', dimension=4)
    assert qids == [
        alphaclops.NamedQid('a-1', dimension=4),
        alphaclops.NamedQid('a1', dimension=4),
        alphaclops.NamedQid('a3', dimension=4),
    ]


def test_to_json():
    assert alphaclops.NamedQubit('c')._json_dict_() == {'name': 'c'}

    assert alphaclops.NamedQid('c', dimension=3)._json_dict_() == {'name': 'c', 'dimension': 3}
