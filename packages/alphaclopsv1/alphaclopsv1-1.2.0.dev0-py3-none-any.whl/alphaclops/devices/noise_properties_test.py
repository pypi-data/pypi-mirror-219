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

from typing import List, Tuple
import alphaclops

from alphaclops.devices.insertion_noise_model import InsertionNoiseModel
from alphaclops.devices.noise_properties import NoiseProperties, NoiseModelFromNoiseProperties
from alphaclops.devices.noise_utils import OpIdentifier, PHYSICAL_GATE_TAG


# These properties are for testing purposes only - they are not representative
# of device behavior for any existing hardware.
class SampleNoiseProperties(NoiseProperties):
    def __init__(self, system_qubits: List[alphaclops.Qid], qubit_pairs: List[Tuple[alphaclops.Qid, alphaclops.Qid]]):
        self.qubits = system_qubits
        self.qubit_pairs = qubit_pairs

    def build_noise_models(self):
        add_h = InsertionNoiseModel({OpIdentifier(alphaclops.Gate, q): alphaclops.H(q) for q in self.qubits})
        add_iswap = InsertionNoiseModel(
            {OpIdentifier(alphaclops.Gate, *qs): alphaclops.ISWAP(*qs) for qs in self.qubit_pairs}
        )
        return [add_h, add_iswap]


def test_sample_model():
    q0, q1 = alphaclops.LineQubit.range(2)
    props = SampleNoiseProperties([q0, q1], [(q0, q1), (q1, q0)])
    model = NoiseModelFromNoiseProperties(props)
    circuit = alphaclops.Circuit(
        alphaclops.X(q0), alphaclops.CNOT(q0, q1), alphaclops.Z(q1), alphaclops.measure(q0, q1, key='meas')
    )
    noisy_circuit = circuit.with_noise(model)
    expected_circuit = alphaclops.Circuit(
        alphaclops.Moment(alphaclops.X(q0).with_tags(PHYSICAL_GATE_TAG)),
        alphaclops.Moment(alphaclops.H(q0)),
        alphaclops.Moment(alphaclops.CNOT(q0, q1).with_tags(PHYSICAL_GATE_TAG)),
        alphaclops.Moment(alphaclops.ISWAP(q0, q1)),
        alphaclops.Moment(alphaclops.Z(q1).with_tags(PHYSICAL_GATE_TAG)),
        alphaclops.Moment(alphaclops.H(q1)),
        alphaclops.Moment(alphaclops.measure(q0, q1, key='meas')),
        alphaclops.Moment(alphaclops.H(q0), alphaclops.H(q1)),
    )
    assert noisy_circuit == expected_circuit
