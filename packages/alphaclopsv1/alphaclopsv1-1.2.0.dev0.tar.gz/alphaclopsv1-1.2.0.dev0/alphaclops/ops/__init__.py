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
"""Gates (unitary and non-unitary), operations, base types, and gate sets.
"""

from alphaclops.ops.arithmetic_operation import ArithmeticGate

from alphaclops.ops.clifford_gate import CliffordGate, SingleQubitCliffordGate

from alphaclops.ops.dense_pauli_string import (
    BaseDensePauliString,
    DensePauliString,
    MutableDensePauliString,
)

from alphaclops.ops.boolean_hamiltonian import BooleanHamiltonianGate

from alphaclops.ops.common_channels import (
    amplitude_damp,
    AmplitudeDampingChannel,
    asymmetric_depolarize,
    AsymmetricDepolarizingChannel,
    bit_flip,
    BitFlipChannel,
    depolarize,
    DepolarizingChannel,
    generalized_amplitude_damp,
    GeneralizedAmplitudeDampingChannel,
    phase_damp,
    phase_flip,
    PhaseDampingChannel,
    PhaseFlipChannel,
    R,
    reset,
    reset_each,
    ResetChannel,
)

from alphaclops.ops.common_gates import (
    CNOT,
    CNotPowGate,
    cphase,
    CX,
    CXPowGate,
    CZ,
    CZPowGate,
    H,
    HPowGate,
    Rx,
    Ry,
    Rz,
    rx,
    ry,
    rz,
    S,
    T,
    XPowGate,
    YPowGate,
    ZPowGate,
)

from alphaclops.ops.common_gate_families import (
    AnyUnitaryGateFamily,
    AnyIntegerPowerGateFamily,
    ParallelGateFamily,
)

from alphaclops.ops.classically_controlled_operation import ClassicallyControlledOperation

from alphaclops.ops.controlled_gate import ControlledGate

from alphaclops.ops.diagonal_gate import DiagonalGate

from alphaclops.ops.eigen_gate import EigenGate

from alphaclops.ops.fourier_transform import PhaseGradientGate, qft, QuantumFourierTransformGate

from alphaclops.ops.fsim_gate import FSimGate, PhasedFSimGate

from alphaclops.ops.gate_features import InterchangeableQubitsGate

from alphaclops.ops.gate_operation import GateOperation

from alphaclops.ops.gateset import GateFamily, Gateset

from alphaclops.ops.identity import I, identity_each, IdentityGate

from alphaclops.ops.global_phase_op import GlobalPhaseGate, global_phase_operation

from alphaclops.ops.kraus_channel import KrausChannel

from alphaclops.ops.linear_combinations import (
    LinearCombinationOfGates,
    LinearCombinationOfOperations,
    PauliSum,
    PauliSumLike,
    ProjectorSum,
)

from alphaclops.ops.mixed_unitary_channel import MixedUnitaryChannel

from alphaclops.ops.pauli_sum_exponential import PauliSumExponential

from alphaclops.ops.pauli_measurement_gate import PauliMeasurementGate

from alphaclops.ops.parallel_gate import ParallelGate, parallel_gate_op

from alphaclops.ops.projector import ProjectorString

from alphaclops.ops.controlled_operation import ControlledOperation

from alphaclops.ops.qubit_manager import BorrowableQubit, CleanQubit, QubitManager, SimpleQubitManager

from alphaclops.ops.qubit_order import QubitOrder

from alphaclops.ops.qubit_order_or_list import QubitOrderOrList

from alphaclops.ops.matrix_gates import MatrixGate

from alphaclops.ops.measure_util import (
    M,
    measure,
    measure_each,
    measure_paulistring_terms,
    measure_single_paulistring,
)

from alphaclops.ops.measurement_gate import MeasurementGate

from alphaclops.ops.named_qubit import NamedQubit, NamedQid

from alphaclops.ops.op_tree import (
    flatten_op_tree,
    freeze_op_tree,
    flatten_to_ops,
    flatten_to_ops_or_moments,
    OP_TREE,
    transform_op_tree,
)

from alphaclops.ops.parity_gates import XX, XXPowGate, YY, YYPowGate, ZZ, ZZPowGate, MSGate, ms

from alphaclops.ops.pauli_gates import Pauli, X, Y, Z

from alphaclops.ops.pauli_interaction_gate import PauliInteractionGate

from alphaclops.ops.pauli_string import (
    MutablePauliString,
    PAULI_GATE_LIKE,
    PAULI_STRING_LIKE,
    PauliString,
    SingleQubitPauliStringGateOperation,
)

from alphaclops.ops.pauli_string_phasor import PauliStringPhasor, PauliStringPhasorGate

from alphaclops.ops.pauli_string_raw_types import PauliStringGateOperation

from alphaclops.ops.permutation_gate import QubitPermutationGate

from alphaclops.ops.phased_iswap_gate import givens, PhasedISwapPowGate

from alphaclops.ops.phased_x_gate import PhasedXPowGate

from alphaclops.ops.phased_x_z_gate import PhasedXZGate

from alphaclops.ops.qid_util import q

from alphaclops.ops.random_gate_channel import RandomGateChannel

from alphaclops.ops.raw_types import Gate, Operation, Qid, TaggedOperation

from alphaclops.ops.swap_gates import (
    ISWAP,
    ISwapPowGate,
    ISWAP_INV,
    riswap,
    SQRT_ISWAP,
    SQRT_ISWAP_INV,
    SWAP,
    SwapPowGate,
)

from alphaclops.ops.tags import RoutingSwapTag, VirtualTag

from alphaclops.ops.three_qubit_gates import (
    CCNOT,
    CCNotPowGate,
    CCX,
    CCXPowGate,
    CCZ,
    CCZPowGate,
    CSWAP,
    CSwapGate,
    FREDKIN,
    ThreeQubitDiagonalGate,
    TOFFOLI,
)

from alphaclops.ops.two_qubit_diagonal_gate import TwoQubitDiagonalGate

from alphaclops.ops.wait_gate import wait, WaitGate

from alphaclops.ops.state_preparation_channel import StatePreparationChannel

from alphaclops.ops.control_values import AbstractControlValues, ProductOfSums, SumOfProducts
