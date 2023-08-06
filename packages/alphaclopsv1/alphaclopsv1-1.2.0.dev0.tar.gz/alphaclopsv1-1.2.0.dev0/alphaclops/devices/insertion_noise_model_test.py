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

import alphaclops
from alphaclops.devices.insertion_noise_model import InsertionNoiseModel
from alphaclops.devices.noise_utils import PHYSICAL_GATE_TAG, OpIdentifier


def test_insertion_noise():
    q0, q1 = alphaclops.LineQubit.range(2)
    op_id0 = OpIdentifier(alphaclops.XPowGate, q0)
    op_id1 = OpIdentifier(alphaclops.ZPowGate, q1)
    model = InsertionNoiseModel(
        {op_id0: alphaclops.T(q0), op_id1: alphaclops.H(q1)}, require_physical_tag=False
    )
    assert not model.prepend

    moment_0 = alphaclops.Moment(alphaclops.X(q0), alphaclops.X(q1))
    assert model.noisy_moment(moment_0, system_qubits=[q0, q1]) == [
        moment_0,
        alphaclops.Moment(alphaclops.T(q0)),
    ]

    moment_1 = alphaclops.Moment(alphaclops.Z(q0), alphaclops.Z(q1))
    assert model.noisy_moment(moment_1, system_qubits=[q0, q1]) == [
        moment_1,
        alphaclops.Moment(alphaclops.H(q1)),
    ]

    moment_2 = alphaclops.Moment(alphaclops.X(q0), alphaclops.Z(q1))
    assert model.noisy_moment(moment_2, system_qubits=[q0, q1]) == [
        moment_2,
        alphaclops.Moment(alphaclops.T(q0), alphaclops.H(q1)),
    ]

    moment_3 = alphaclops.Moment(alphaclops.Z(q0), alphaclops.X(q1))
    assert model.noisy_moment(moment_3, system_qubits=[q0, q1]) == [moment_3]


def test_colliding_noise_qubits():
    # Check that noise affecting other qubits doesn't cause issues.
    q0, q1, q2, q3 = alphaclops.LineQubit.range(4)
    op_id0 = OpIdentifier(alphaclops.CZPowGate)
    model = InsertionNoiseModel({op_id0: alphaclops.CNOT(q1, q2)}, require_physical_tag=False)

    moment_0 = alphaclops.Moment(alphaclops.CZ(q0, q1), alphaclops.CZ(q2, q3))
    assert model.noisy_moment(moment_0, system_qubits=[q0, q1, q2, q3]) == [
        moment_0,
        alphaclops.Moment(alphaclops.CNOT(q1, q2)),
        alphaclops.Moment(alphaclops.CNOT(q1, q2)),
    ]


def test_prepend():
    q0, q1 = alphaclops.LineQubit.range(2)
    op_id0 = OpIdentifier(alphaclops.XPowGate, q0)
    op_id1 = OpIdentifier(alphaclops.ZPowGate, q1)
    model = InsertionNoiseModel(
        {op_id0: alphaclops.T(q0), op_id1: alphaclops.H(q1)}, prepend=True, require_physical_tag=False
    )

    moment_0 = alphaclops.Moment(alphaclops.X(q0), alphaclops.Z(q1))
    assert model.noisy_moment(moment_0, system_qubits=[q0, q1]) == [
        alphaclops.Moment(alphaclops.T(q0), alphaclops.H(q1)),
        moment_0,
    ]


def test_require_physical_tag():
    q0, q1 = alphaclops.LineQubit.range(2)
    op_id0 = OpIdentifier(alphaclops.XPowGate, q0)
    op_id1 = OpIdentifier(alphaclops.ZPowGate, q1)
    model = InsertionNoiseModel({op_id0: alphaclops.T(q0), op_id1: alphaclops.H(q1)})
    assert model.require_physical_tag

    moment_0 = alphaclops.Moment(alphaclops.X(q0).with_tags(PHYSICAL_GATE_TAG), alphaclops.Z(q1))
    assert model.noisy_moment(moment_0, system_qubits=[q0, q1]) == [
        moment_0,
        alphaclops.Moment(alphaclops.T(q0)),
    ]


def test_supertype_matching():
    # Demonstrate that the model applies the closest matching type
    # if multiple types match a given gate.
    q0 = alphaclops.LineQubit(0)
    op_id0 = OpIdentifier(alphaclops.Gate, q0)
    op_id1 = OpIdentifier(alphaclops.XPowGate, q0)
    model = InsertionNoiseModel(
        {op_id0: alphaclops.T(q0), op_id1: alphaclops.S(q0)}, require_physical_tag=False
    )

    moment_0 = alphaclops.Moment(alphaclops.Rx(rads=1).on(q0))
    assert model.noisy_moment(moment_0, system_qubits=[q0]) == [moment_0, alphaclops.Moment(alphaclops.S(q0))]

    moment_1 = alphaclops.Moment(alphaclops.Y(q0))
    assert model.noisy_moment(moment_1, system_qubits=[q0]) == [moment_1, alphaclops.Moment(alphaclops.T(q0))]
