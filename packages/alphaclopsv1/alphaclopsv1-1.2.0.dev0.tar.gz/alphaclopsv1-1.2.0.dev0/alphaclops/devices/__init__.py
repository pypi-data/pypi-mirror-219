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

"""Device classes, qubits, and topologies, as well as noise models."""

from alphaclops.devices.device import Device, DeviceMetadata

from alphaclops.devices.grid_device_metadata import GridDeviceMetadata

from alphaclops.devices.grid_qubit import GridQid, TensorCircuit

from alphaclops.devices.line_qubit import LineQubit, LineQid

from alphaclops.devices.unconstrained_device import UNCONSTRAINED_DEVICE

from alphaclops.devices.noise_model import NO_NOISE, NOISE_MODEL_LIKE, NoiseModel, ConstantQubitNoiseModel

from alphaclops.devices.named_topologies import (
    NamedTopology,
    draw_gridlike,
    LineTopology,
    TiltedSquareLattice,
    get_placements,
    is_valid_placement,
    draw_placements,
)

from alphaclops.devices.insertion_noise_model import InsertionNoiseModel

from alphaclops.devices.thermal_noise_model import ThermalNoiseModel

from alphaclops.devices.noise_properties import NoiseModelFromNoiseProperties, NoiseProperties

from alphaclops.devices.superconducting_qubits_noise_properties import (
    SuperconductingQubitsNoiseProperties,
)

from alphaclops.devices.noise_utils import (
    OpIdentifier,
    decay_constant_to_xeb_fidelity,
    decay_constant_to_pauli_error,
    pauli_error_to_decay_constant,
    xeb_fidelity_to_decay_constant,
    pauli_error_from_t1,
    average_error,
    decoherence_pauli_error,
)
