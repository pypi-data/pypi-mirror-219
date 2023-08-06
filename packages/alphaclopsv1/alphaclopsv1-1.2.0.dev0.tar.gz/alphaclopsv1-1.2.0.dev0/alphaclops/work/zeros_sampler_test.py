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

import numpy as np
import pytest
import sympy

import alphaclops


def test_run_sweep():
    a, b, c = [alphaclops.NamedQubit(s) for s in ['a', 'b', 'c']]
    circuit = alphaclops.Circuit([alphaclops.measure(a)], [alphaclops.measure(b, c)])
    sampler = alphaclops.ZerosSampler()

    result = sampler.run_sweep(circuit, None, 3)

    assert len(result) == 1
    assert result[0].measurements.keys() == {'a', 'b,c'}
    assert result[0].measurements['a'].shape == (3, 1)
    assert np.all(result[0].measurements['a'] == 0)
    assert result[0].measurements['b,c'].shape == (3, 2)
    assert np.all(result[0].measurements['b,c'] == 0)


def test_sample():
    # Create a circuit whose measurements are always zeros, and check that
    # results of ZeroSampler on this circuit are identical to results of
    # actual simulation.
    qs = alphaclops.LineQubit.range(6)
    c = alphaclops.Circuit([alphaclops.CNOT(qs[0], qs[1]), alphaclops.X(qs[2]), alphaclops.X(qs[2])])
    c += alphaclops.Z(qs[3]) ** sympy.Symbol('p')
    c += [alphaclops.measure(q) for q in qs[0:3]]
    c += alphaclops.measure(qs[4], qs[5])
    # Z to even power is an identity.
    params = alphaclops.Points(sympy.Symbol('p'), [0, 2, 4, 6])

    result1 = alphaclops.ZerosSampler().sample(c, repetitions=10, params=params)
    result2 = alphaclops.Simulator().sample(c, repetitions=10, params=params)

    assert np.all(result1 == result2)


def test_repeated_keys():
    q0, q1, q2 = alphaclops.LineQubit.range(3)

    c = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.measure(q1, q2, key='b'),
        alphaclops.measure(q0, key='a'),
        alphaclops.measure(q1, q2, key='b'),
        alphaclops.measure(q1, q2, key='b'),
    )
    result = alphaclops.ZerosSampler().run(c, repetitions=10)
    assert result.records['a'].shape == (10, 2, 1)
    assert result.records['b'].shape == (10, 3, 2)

    c2 = alphaclops.Circuit(alphaclops.measure(q0, key='a'), alphaclops.measure(q1, q2, key='a'))
    with pytest.raises(ValueError, match="Different qid shapes for repeated measurement"):
        alphaclops.ZerosSampler().run(c2, repetitions=10)


class OnlyMeasurementsDevice(alphaclops.Device):
    def validate_operation(self, operation: 'alphaclops.Operation') -> None:
        if not alphaclops.is_measurement(operation):
            raise ValueError(f'{operation} is not a measurement and this device only measures!')


def test_validate_device():
    device = OnlyMeasurementsDevice()
    sampler = alphaclops.ZerosSampler(device)

    a, b, c = [alphaclops.NamedQubit(s) for s in ['a', 'b', 'c']]
    circuit = alphaclops.Circuit(alphaclops.measure(a), alphaclops.measure(b, c))

    _ = sampler.run_sweep(circuit, None, 3)

    circuit = alphaclops.Circuit(alphaclops.measure(a), alphaclops.X(b))
    with pytest.raises(ValueError, match=r'X\(b\) is not a measurement'):
        _ = sampler.run_sweep(circuit, None, 3)
