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

import duet

import alphaclops


@duet.sync
async def test_pauli_string_sample_collector():
    a, b = alphaclops.LineQubit.range(2)
    p = alphaclops.PauliSumCollector(
        circuit=alphaclops.Circuit(alphaclops.H(a), alphaclops.CNOT(a, b), alphaclops.X(a), alphaclops.Z(b)),
        observable=(1 + 0j) * alphaclops.X(a) * alphaclops.X(b)
                   - 16 * alphaclops.Y(a) * alphaclops.Y(b)
                   + 4 * alphaclops.Z(a) * alphaclops.Z(b)
                   + (1 - 0j),
        samples_per_term=100,
    )
    result = await p.collect_async(sampler=alphaclops.Simulator())
    assert result is None
    energy = p.estimated_energy()
    assert isinstance(energy, float) and energy == 12


@duet.sync
async def test_pauli_string_sample_single():
    a, b = alphaclops.LineQubit.range(2)
    p = alphaclops.PauliSumCollector(
        circuit=alphaclops.Circuit(alphaclops.H(a), alphaclops.CNOT(a, b), alphaclops.X(a), alphaclops.Z(b)),
        observable=alphaclops.X(a) * alphaclops.X(b),
        samples_per_term=100,
    )
    result = await p.collect_async(sampler=alphaclops.Simulator())
    assert result is None
    assert p.estimated_energy() == -1


def test_pauli_string_sample_collector_identity():
    p = alphaclops.PauliSumCollector(
        circuit=alphaclops.Circuit(), observable=alphaclops.PauliSum() + 2j, samples_per_term=100
    )
    p.collect(sampler=alphaclops.Simulator())
    assert p.estimated_energy() == 2j


def test_pauli_string_sample_collector_extra_qubit_z():
    a, b = alphaclops.LineQubit.range(2)
    p = alphaclops.PauliSumCollector(
        circuit=alphaclops.Circuit(alphaclops.H(a)), observable=3 * alphaclops.Z(b), samples_per_term=100
    )
    p.collect(sampler=alphaclops.Simulator())
    assert p.estimated_energy() == 3


def test_pauli_string_sample_collector_extra_qubit_x():
    a, b = alphaclops.LineQubit.range(2)
    p = alphaclops.PauliSumCollector(
        circuit=alphaclops.Circuit(alphaclops.H(a)), observable=3 * alphaclops.X(b), samples_per_term=10000
    )
    p.collect(sampler=alphaclops.Simulator())
    assert abs(p.estimated_energy()) < 0.5
