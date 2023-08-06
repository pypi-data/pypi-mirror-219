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

import alphaclops


def test_produces_samples():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.H(a), alphaclops.CNOT(a, b), alphaclops.measure(a, key='a'), alphaclops.measure(b, key='b'))

    result = alphaclops.StabilizerSampler().sample(c, repetitions=100)
    assert 5 < sum(result['a']) < 95
    assert np.all(result['a'] ^ result['b'] == 0)


def test_reset():
    q = alphaclops.LineQubit(0)
    sampler = alphaclops.StabilizerSampler()
    c = alphaclops.Circuit(alphaclops.X(q), alphaclops.reset(q), alphaclops.measure(q))
    assert sampler.sample(c)['q(0)'][0] == 0
    c = alphaclops.Circuit(alphaclops.H(q), alphaclops.reset(q), alphaclops.measure(q))
    assert sampler.sample(c)['q(0)'][0] == 0
    c = alphaclops.Circuit(alphaclops.reset(q), alphaclops.measure(q))
    assert sampler.sample(c)['q(0)'][0] == 0
