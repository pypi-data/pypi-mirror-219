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

"""Protocols (structural subtyping) supported in alphaclops."""

from alphaclops.protocols.act_on_protocol import act_on, SupportsActOn, SupportsActOnQubits
from alphaclops.protocols.apply_unitary_protocol import (
    apply_unitaries,
    apply_unitary,
    ApplyUnitaryArgs,
    SupportsConsistentApplyUnitary,
)
from alphaclops.protocols.apply_channel_protocol import (
    apply_channel,
    ApplyChannelArgs,
    SupportsApplyChannel,
)
from alphaclops.protocols.apply_mixture_protocol import (
    apply_mixture,
    ApplyMixtureArgs,
    SupportsApplyMixture,
)
from alphaclops.protocols.approximate_equality_protocol import approx_eq, SupportsApproximateEquality
from alphaclops.protocols.kraus_protocol import kraus, has_kraus, SupportsKraus
from alphaclops.protocols.commutes_protocol import commutes, definitely_commutes, SupportsCommutes
from alphaclops.protocols.control_key_protocol import (
    control_keys,
    measurement_keys_touched,
    SupportsControlKey,
)
from alphaclops.protocols.circuit_diagram_info_protocol import (
    circuit_diagram_info,
    CircuitDiagramInfo,
    CircuitDiagramInfoArgs,
    LabelEntity,
    SupportsCircuitDiagramInfo,
)
from alphaclops.protocols.decompose_protocol import (
    decompose,
    decompose_once,
    decompose_once_with_qubits,
    DecompositionContext,
    SupportsDecompose,
    SupportsDecomposeWithQubits,
)
from alphaclops.protocols.equal_up_to_global_phase_protocol import (
    equal_up_to_global_phase,
    SupportsEqualUpToGlobalPhase,
)
from alphaclops.protocols.has_stabilizer_effect_protocol import has_stabilizer_effect
from alphaclops.protocols.has_unitary_protocol import has_unitary, SupportsExplicitHasUnitary
from alphaclops.protocols.inverse_protocol import inverse
from alphaclops.protocols.json_serialization import (
    alphaclops_type_from_json,
    DEFAULT_RESOLVERS,
    HasJSONNamespace,
    JsonResolver,
    json_alphaclops_type,
    json_namespace,
    to_json_gzip,
    read_json_gzip,
    to_json,
    read_json,
    obj_to_dict_helper,
    dataclass_json_dict,
    SerializableByKey,
    SupportsJSON,
)
from alphaclops.protocols.measurement_key_protocol import (
    is_measurement,
    measurement_key_name,
    measurement_key_obj,
    measurement_key_names,
    measurement_key_objs,
    with_key_path,
    with_key_path_prefix,
    with_measurement_key_mapping,
    with_rescoped_keys,
    SupportsMeasurementKey,
)
from alphaclops.protocols.mixture_protocol import has_mixture, mixture, SupportsMixture, validate_mixture
from alphaclops.protocols.mul_protocol import mul
from alphaclops.protocols.pauli_expansion_protocol import pauli_expansion, SupportsPauliExpansion

# pylint: disable=redefined-builtin
from alphaclops.protocols.pow_protocol import pow

# pylint: enable=redefined-builtin
from alphaclops.protocols.qasm import (
    qasm,
    QasmArgs,
    SupportsQasm,
    SupportsQasmWithArgs,
    SupportsQasmWithArgsAndQubits,
)
from alphaclops.protocols.trace_distance_bound import (
    SupportsTraceDistanceBound,
    trace_distance_bound,
    trace_distance_from_angle_list,
)
from alphaclops.protocols.resolve_parameters import (
    is_parameterized,
    parameter_names,
    parameter_symbols,
    resolve_parameters,
    resolve_parameters_once,
    SupportsParameterization,
)
from alphaclops.protocols.phase_protocol import phase_by, SupportsPhase
from alphaclops.protocols.qid_shape_protocol import (
    num_qubits,
    qid_shape,
    SupportsExplicitQidShape,
    SupportsExplicitNumQubits,
)
from alphaclops.protocols.unitary_protocol import SupportsUnitary, unitary
