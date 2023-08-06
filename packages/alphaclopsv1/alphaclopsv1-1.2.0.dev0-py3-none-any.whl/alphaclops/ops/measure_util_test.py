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

import numpy as np
import pytest

import alphaclops


def test_measure_qubits():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    # Empty application.
    with pytest.raises(ValueError, match='empty set of qubits'):
        _ = alphaclops.measure()

    with pytest.raises(ValueError, match='empty set of qubits'):
        _ = alphaclops.measure([])

    assert alphaclops.measure(a) == alphaclops.MeasurementGate(num_qubits=1, key='a').on(a)
    assert alphaclops.measure([a]) == alphaclops.MeasurementGate(num_qubits=1, key='a').on(a)
    assert alphaclops.measure(a, b) == alphaclops.MeasurementGate(num_qubits=2, key='a,b').on(a, b)
    assert alphaclops.measure([a, b]) == alphaclops.MeasurementGate(num_qubits=2, key='a,b').on(a, b)
    qubit_generator = (q for q in (a, b))
    assert alphaclops.measure(qubit_generator) == alphaclops.MeasurementGate(num_qubits=2, key='a,b').on(a, b)
    assert alphaclops.measure(b, a) == alphaclops.MeasurementGate(num_qubits=2, key='b,a').on(b, a)
    assert alphaclops.measure(a, key='b') == alphaclops.MeasurementGate(num_qubits=1, key='b').on(a)
    assert alphaclops.measure(a, invert_mask=(True,)) == alphaclops.MeasurementGate(
        num_qubits=1, key='a', invert_mask=(True,)
    ).on(a)
    assert alphaclops.measure(*alphaclops.LineQid.for_qid_shape((1, 2, 3)), key='a') == alphaclops.MeasurementGate(
        num_qubits=3, key='a', qid_shape=(1, 2, 3)
    ).on(*alphaclops.LineQid.for_qid_shape((1, 2, 3)))
    assert alphaclops.measure(alphaclops.LineQid.for_qid_shape((1, 2, 3)), key='a') == alphaclops.MeasurementGate(
        num_qubits=3, key='a', qid_shape=(1, 2, 3)
    ).on(*alphaclops.LineQid.for_qid_shape((1, 2, 3)))
    cmap = {(0,): np.array([[0, 1], [1, 0]])}
    assert alphaclops.measure(a, confusion_map=cmap) == alphaclops.MeasurementGate(
        num_qubits=1, key='a', confusion_map=cmap
    ).on(a)

    with pytest.raises(ValueError, match='ndarray'):
        _ = alphaclops.measure(np.array([1, 0]))

    with pytest.raises(ValueError, match='Qid'):
        _ = alphaclops.measure("bork")

    with pytest.raises(ValueError, match='Qid'):
        _ = alphaclops.measure([a, [b]])

    with pytest.raises(ValueError, match='Qid'):
        _ = alphaclops.measure([a], [b])


def test_measure_each():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    assert alphaclops.measure_each() == []
    assert alphaclops.measure_each([]) == []
    assert alphaclops.measure_each(a) == [alphaclops.measure(a)]
    assert alphaclops.measure_each([a]) == [alphaclops.measure(a)]
    assert alphaclops.measure_each(a, b) == [alphaclops.measure(a), alphaclops.measure(b)]
    assert alphaclops.measure_each([a, b]) == [alphaclops.measure(a), alphaclops.measure(b)]
    qubit_generator = (q for q in (a, b))
    assert alphaclops.measure_each(qubit_generator) == [alphaclops.measure(a), alphaclops.measure(b)]
    assert alphaclops.measure_each(a.with_dimension(3), b.with_dimension(3)) == [
        alphaclops.measure(a.with_dimension(3)),
        alphaclops.measure(b.with_dimension(3)),
    ]

    assert alphaclops.measure_each(a, b, key_func=lambda e: e.name + '!') == [
        alphaclops.measure(a, key='a!'),
        alphaclops.measure(b, key='b!'),
    ]


def test_measure_single_paulistring():
    # Correct application
    q = alphaclops.LineQubit.range(3)
    ps = alphaclops.X(q[0]) * alphaclops.Y(q[1]) * alphaclops.Z(q[2])
    assert alphaclops.measure_single_paulistring(ps, key='a') == alphaclops.PauliMeasurementGate(
        ps.values(), key='a'
    ).on(*ps.keys())

    # Test with negative coefficient
    ps_neg = -alphaclops.Y(alphaclops.LineQubit(0)) * alphaclops.Y(alphaclops.LineQubit(1))
    assert alphaclops.measure_single_paulistring(ps_neg, key='1').gate == alphaclops.PauliMeasurementGate(
        alphaclops.DensePauliString('YY', coefficient=-1), key='1'
    )

    # Empty application
    with pytest.raises(ValueError, match='should be an instance of alphaclops.PauliString'):
        _ = alphaclops.measure_single_paulistring(alphaclops.I(q[0]) * alphaclops.I(q[1]))

    # Wrong type
    with pytest.raises(ValueError, match='should be an instance of alphaclops.PauliString'):
        _ = alphaclops.measure_single_paulistring(q)

    # Coefficient != +1 or -1
    with pytest.raises(ValueError, match='must have a coefficient'):
        _ = alphaclops.measure_single_paulistring(-2 * ps)


def test_measure_paulistring_terms():
    # Correct application
    q = alphaclops.LineQubit.range(3)
    ps = alphaclops.X(q[0]) * alphaclops.Y(q[1]) * alphaclops.Z(q[2])
    assert alphaclops.measure_paulistring_terms(ps) == [
        alphaclops.PauliMeasurementGate([alphaclops.X], key=str(q[0])).on(q[0]),
        alphaclops.PauliMeasurementGate([alphaclops.Y], key=str(q[1])).on(q[1]),
        alphaclops.PauliMeasurementGate([alphaclops.Z], key=str(q[2])).on(q[2]),
    ]

    # Empty application
    with pytest.raises(ValueError, match='should be an instance of alphaclops.PauliString'):
        _ = alphaclops.measure_paulistring_terms(alphaclops.I(q[0]) * alphaclops.I(q[1]))

    # Wrong type
    with pytest.raises(ValueError, match='should be an instance of alphaclops.PauliString'):
        _ = alphaclops.measure_paulistring_terms(q)
