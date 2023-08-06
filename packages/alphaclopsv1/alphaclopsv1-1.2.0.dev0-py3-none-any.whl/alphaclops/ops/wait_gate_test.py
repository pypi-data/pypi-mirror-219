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
import datetime

import pytest
import sympy

import alphaclops


def test_init():
    g = alphaclops.WaitGate(datetime.timedelta(0, 0, 5))
    assert g.duration == alphaclops.Duration(micros=5)

    g = alphaclops.WaitGate(alphaclops.Duration(nanos=4))
    assert g.duration == alphaclops.Duration(nanos=4)

    g = alphaclops.WaitGate(0)
    assert g.duration == alphaclops.Duration(0)

    with pytest.raises(ValueError, match='duration < 0'):
        _ = alphaclops.WaitGate(alphaclops.Duration(nanos=-4))

    with pytest.raises(TypeError, match='Not a `alphaclops.DURATION_LIKE`'):
        _ = alphaclops.WaitGate(2)


def test_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(alphaclops.WaitGate(0), alphaclops.WaitGate(alphaclops.Duration()))
    eq.make_equality_group(lambda: alphaclops.WaitGate(alphaclops.Duration(nanos=4)))


def test_protocols():
    t = sympy.Symbol('t')
    p = alphaclops.WaitGate(alphaclops.Duration(millis=5 * t))
    c = alphaclops.WaitGate(alphaclops.Duration(millis=2))
    q = alphaclops.LineQubit(0)

    alphaclops.testing.assert_implements_consistent_protocols(alphaclops.wait(q, nanos=0))
    alphaclops.testing.assert_implements_consistent_protocols(c.on(q))
    alphaclops.testing.assert_implements_consistent_protocols(p.on(q))

    assert alphaclops.has_unitary(p)
    assert alphaclops.has_unitary(c)
    assert alphaclops.is_parameterized(p)
    assert not alphaclops.is_parameterized(c)
    assert alphaclops.resolve_parameters(p, {'t': 2}) == alphaclops.WaitGate(alphaclops.Duration(millis=10))
    assert alphaclops.resolve_parameters(c, {'t': 2}) == c
    assert alphaclops.resolve_parameters_once(c, {'t': 2}) == c
    assert alphaclops.trace_distance_bound(p) == 0
    assert alphaclops.trace_distance_bound(c) == 0
    assert alphaclops.inverse(c) == c
    assert alphaclops.inverse(p) == p
    assert alphaclops.decompose(c.on(q)) == []
    assert alphaclops.decompose(p.on(q)) == []


def test_qid_shape():
    assert alphaclops.qid_shape(alphaclops.WaitGate(0, qid_shape=(2, 3))) == (2, 3)
    assert alphaclops.qid_shape(alphaclops.WaitGate(0, num_qubits=3)) == (2, 2, 2)
    with pytest.raises(ValueError, match='empty set of qubits'):
        alphaclops.WaitGate(0, num_qubits=0)
    with pytest.raises(ValueError, match='num_qubits'):
        alphaclops.WaitGate(0, qid_shape=(2, 2), num_qubits=1)


@pytest.mark.parametrize('num_qubits', [1, 2, 3])
def test_resolve_parameters(num_qubits: int) -> None:
    gate = alphaclops.WaitGate(duration=alphaclops.Duration(nanos=sympy.Symbol('t_ns')), num_qubits=num_qubits)
    resolved = alphaclops.resolve_parameters(gate, {'t_ns': 10})
    assert resolved.duration == alphaclops.Duration(nanos=10)
    assert alphaclops.num_qubits(resolved) == num_qubits


def test_json():
    q0, q1 = alphaclops.TensorCircuit.rect(1, 2)
    qtrit = alphaclops.GridQid(1, 2, dimension=3)
    alphaclops.testing.assert_json_roundtrip_works(alphaclops.wait(q0, nanos=10))
    alphaclops.testing.assert_json_roundtrip_works(alphaclops.wait(q0, q1, nanos=10))
    alphaclops.testing.assert_json_roundtrip_works(alphaclops.wait(qtrit, nanos=10))
    alphaclops.testing.assert_json_roundtrip_works(alphaclops.wait(qtrit, q1, nanos=10))


def test_str():
    assert str(alphaclops.WaitGate(alphaclops.Duration(nanos=5))) == 'WaitGate(5 ns)'
