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
"""Methods for resolving JSON types during serialization."""
import datetime
import functools
from typing import Dict, List, NamedTuple, Optional, Tuple, TYPE_CHECKING

from alphaclops.protocols.json_serialization import ObjectFactory

if TYPE_CHECKING:
    import alphaclops
    import alphaclops.ops.pauli_gates
    import alphaclops.devices.unconstrained_device


# Needed for backwards compatible named tuples of CrossEntropyResult
CrossEntropyPair = NamedTuple('CrossEntropyPair', [('num_cycle', int), ('xeb_fidelity', float)])
SpecklePurityPair = NamedTuple('SpecklePurityPair', [('num_cycle', int), ('purity', float)])
CrossEntropyResult = NamedTuple(
    'CrossEntropyResult',
    [
        ('data', List[CrossEntropyPair]),
        ('repetitions', int),
        ('purity_data', Optional[List[SpecklePurityPair]]),
    ],
)
CrossEntropyResultDict = NamedTuple(
    'CrossEntropyResultDict', [('results', Dict[Tuple['alphaclops.Qid', ...], CrossEntropyResult])]
)


@functools.lru_cache()
def _class_resolver_dictionary() -> Dict[str, ObjectFactory]:
    import alphaclops
    from alphaclops.ops import raw_types
    import pandas as pd
    import numpy as np
    from alphaclops.devices.noise_model import _NoNoiseModel
    from alphaclops.experiments import GridInteractionLayer
    from alphaclops.experiments.grid_parallel_two_qubit_xeb import GridParallelXEBMetadata

    def _boolean_hamiltonian_gate_op(qubit_map, boolean_strs, theta):
        return alphaclops.BooleanHamiltonianGate(
            parameter_names=list(qubit_map.keys()), boolean_strs=boolean_strs, theta=theta
        ).on(*qubit_map.values())

    def _identity_operation_from_dict(qubits, **kwargs):
        return alphaclops.identity_each(*qubits)

    def single_qubit_matrix_gate(matrix):
        if not isinstance(matrix, np.ndarray):
            matrix = np.array(matrix, dtype=np.complex128)
        return alphaclops.MatrixGate(matrix, qid_shape=(matrix.shape[0],))

    def two_qubit_matrix_gate(matrix):
        if not isinstance(matrix, np.ndarray):
            matrix = np.array(matrix, dtype=np.complex128)
        return alphaclops.MatrixGate(matrix, qid_shape=(2, 2))

    def _cross_entropy_result(data, repetitions, **kwargs) -> CrossEntropyResult:
        purity_data = kwargs.get('purity_data', None)
        if purity_data is not None:
            purity_data = [SpecklePurityPair(d, f) for d, f in purity_data]
        return CrossEntropyResult(
            data=[CrossEntropyPair(d, f) for d, f in data],
            repetitions=repetitions,
            purity_data=purity_data,
        )

    def _cross_entropy_result_dict(
        results: List[Tuple[List['alphaclops.Qid'], CrossEntropyResult]], **kwargs
    ) -> CrossEntropyResultDict:
        return CrossEntropyResultDict(results={tuple(qubits): result for qubits, result in results})

    def _parallel_gate_op(gate, qubits):
        return alphaclops.parallel_gate_op(gate, *qubits)

    def _datetime(timestamp: float) -> datetime.datetime:
        # We serialize datetimes (both with ("aware") and without ("naive") timezone information)
        # as unix timestamps. The deserialized datetime will always refer to the
        # same point in time, but will be re-constructed as a timezone-aware object.
        #
        # If `o` is a naive datetime,  o != read_json(to_json(o)) because Python doesn't
        # let you compare aware and naive datetimes.
        return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)

    def _symmetricalqidpair(qids):
        return frozenset(qids)

    import sympy

    return {
        'AmplitudeDampingChannel': alphaclops.AmplitudeDampingChannel,
        'AnyIntegerPowerGateFamily': alphaclops.AnyIntegerPowerGateFamily,
        'AnyUnitaryGateFamily': alphaclops.AnyUnitaryGateFamily,
        'AsymmetricDepolarizingChannel': alphaclops.AsymmetricDepolarizingChannel,
        'BitFlipChannel': alphaclops.BitFlipChannel,
        'BitstringAccumulator': alphaclops.work.BitstringAccumulator,
        'BooleanHamiltonianGate': alphaclops.BooleanHamiltonianGate,
        'CCNotPowGate': alphaclops.CCNotPowGate,
        'CCXPowGate': alphaclops.CCXPowGate,
        'CCZPowGate': alphaclops.CCZPowGate,
        'Circuit': alphaclops.Circuit,
        'CircuitOperation': alphaclops.CircuitOperation,
        'ClassicallyControlledOperation': alphaclops.ClassicallyControlledOperation,
        'ClassicalDataDictionaryStore': alphaclops.ClassicalDataDictionaryStore,
        'CliffordGate': alphaclops.CliffordGate,
        'CliffordState': alphaclops.CliffordState,
        'CliffordTableau': alphaclops.CliffordTableau,
        'CNotPowGate': alphaclops.CNotPowGate,
        'ConstantQubitNoiseModel': alphaclops.ConstantQubitNoiseModel,
        'ControlledGate': alphaclops.ControlledGate,
        'ControlledOperation': alphaclops.ControlledOperation,
        'CSwapGate': alphaclops.CSwapGate,
        'CXPowGate': alphaclops.CXPowGate,
        'CZPowGate': alphaclops.CZPowGate,
        'CZTargetGateset': alphaclops.CZTargetGateset,
        'DiagonalGate': alphaclops.DiagonalGate,
        'DensePauliString': alphaclops.DensePauliString,
        'DepolarizingChannel': alphaclops.DepolarizingChannel,
        'DeviceMetadata': alphaclops.DeviceMetadata,
        'Duration': alphaclops.Duration,
        'FrozenCircuit': alphaclops.FrozenCircuit,
        'FSimGate': alphaclops.FSimGate,
        'GateFamily': alphaclops.GateFamily,
        'GateOperation': alphaclops.GateOperation,
        'Gateset': alphaclops.Gateset,
        'GeneralizedAmplitudeDampingChannel': alphaclops.GeneralizedAmplitudeDampingChannel,
        'GlobalPhaseGate': alphaclops.GlobalPhaseGate,
        'GridDeviceMetadata': alphaclops.GridDeviceMetadata,
        'GridInteractionLayer': GridInteractionLayer,
        'GridParallelXEBMetadata': GridParallelXEBMetadata,
        'GridQid': alphaclops.GridQid,
        'TensorCircuit': alphaclops.TensorCircuit,
        'HPowGate': alphaclops.HPowGate,
        'ISwapPowGate': alphaclops.ISwapPowGate,
        'IdentityGate': alphaclops.IdentityGate,
        'InitObsSetting': alphaclops.work.InitObsSetting,
        'KeyCondition': alphaclops.KeyCondition,
        'KrausChannel': alphaclops.KrausChannel,
        'LinearDict': alphaclops.LinearDict,
        'LineQubit': alphaclops.LineQubit,
        'LineQid': alphaclops.LineQid,
        'LineTopology': alphaclops.LineTopology,
        'Linspace': alphaclops.Linspace,
        'ListSweep': alphaclops.ListSweep,
        'MatrixGate': alphaclops.MatrixGate,
        'MixedUnitaryChannel': alphaclops.MixedUnitaryChannel,
        'MeasurementKey': alphaclops.MeasurementKey,
        'MeasurementGate': alphaclops.MeasurementGate,
        'MeasurementType': alphaclops.MeasurementType,
        '_MeasurementSpec': alphaclops.work._MeasurementSpec,
        'Moment': alphaclops.Moment,
        'MutableDensePauliString': alphaclops.MutableDensePauliString,
        'MutablePauliString': alphaclops.MutablePauliString,
        '_NoNoiseModel': _NoNoiseModel,
        'NamedQubit': alphaclops.NamedQubit,
        'NamedQid': alphaclops.NamedQid,
        'NoIdentifierQubit': alphaclops.testing.NoIdentifierQubit,
        'ObservableMeasuredResult': alphaclops.work.ObservableMeasuredResult,
        'OpIdentifier': alphaclops.OpIdentifier,
        'ParamResolver': alphaclops.ParamResolver,
        'ParallelGate': alphaclops.ParallelGate,
        'ParallelGateFamily': alphaclops.ParallelGateFamily,
        'PauliInteractionGate': alphaclops.PauliInteractionGate,
        'PauliMeasurementGate': alphaclops.PauliMeasurementGate,
        'PauliString': alphaclops.PauliString,
        'PauliStringPhasor': alphaclops.PauliStringPhasor,
        'PauliStringPhasorGate': alphaclops.PauliStringPhasorGate,
        'PauliSum': alphaclops.PauliSum,
        '_PauliX': alphaclops.ops.pauli_gates._PauliX,
        '_PauliY': alphaclops.ops.pauli_gates._PauliY,
        '_PauliZ': alphaclops.ops.pauli_gates._PauliZ,
        'PhaseDampingChannel': alphaclops.PhaseDampingChannel,
        'PhaseFlipChannel': alphaclops.PhaseFlipChannel,
        'PhaseGradientGate': alphaclops.PhaseGradientGate,
        'PhasedFSimGate': alphaclops.PhasedFSimGate,
        'PhasedISwapPowGate': alphaclops.PhasedISwapPowGate,
        'PhasedXPowGate': alphaclops.PhasedXPowGate,
        'PhasedXZGate': alphaclops.PhasedXZGate,
        'Points': alphaclops.Points,
        'Product': alphaclops.Product,
        'ProductState': alphaclops.ProductState,
        'ProductOfSums': alphaclops.ProductOfSums,
        'ProjectorString': alphaclops.ProjectorString,
        'ProjectorSum': alphaclops.ProjectorSum,
        'QasmUGate': alphaclops.circuits.qasm_output.QasmUGate,
        '_QubitAsQid': raw_types._QubitAsQid,
        'QuantumFourierTransformGate': alphaclops.QuantumFourierTransformGate,
        'QubitPermutationGate': alphaclops.QubitPermutationGate,
        'RandomGateChannel': alphaclops.RandomGateChannel,
        'RepetitionsStoppingCriteria': alphaclops.work.RepetitionsStoppingCriteria,
        'ResetChannel': alphaclops.ResetChannel,
        'Result': alphaclops.ResultDict,  # Keep support for alphaclops < 0.14.
        'ResultDict': alphaclops.ResultDict,
        'RoutingSwapTag': alphaclops.RoutingSwapTag,
        'Rx': alphaclops.Rx,
        'Ry': alphaclops.Ry,
        'Rz': alphaclops.Rz,
        'SingleQubitCliffordGate': alphaclops.SingleQubitCliffordGate,
        'SingleQubitPauliStringGateOperation': alphaclops.SingleQubitPauliStringGateOperation,
        'SingleQubitReadoutCalibrationResult': alphaclops.experiments.SingleQubitReadoutCalibrationResult,
        'SqrtIswapTargetGateset': alphaclops.SqrtIswapTargetGateset,
        'StabilizerStateChForm': alphaclops.StabilizerStateChForm,
        'StatePreparationChannel': alphaclops.StatePreparationChannel,
        'SumOfProducts': alphaclops.SumOfProducts,
        'SwapPowGate': alphaclops.SwapPowGate,
        'SympyCondition': alphaclops.SympyCondition,
        'TaggedOperation': alphaclops.TaggedOperation,
        'TensoredConfusionMatrices': alphaclops.TensoredConfusionMatrices,
        'TiltedSquareLattice': alphaclops.TiltedSquareLattice,
        'ThreeQubitDiagonalGate': alphaclops.ThreeQubitDiagonalGate,
        'TrialResult': alphaclops.ResultDict,  # keep support for alphaclops < 0.11.
        'TwoQubitDiagonalGate': alphaclops.TwoQubitDiagonalGate,
        'TwoQubitGateTabulation': alphaclops.TwoQubitGateTabulation,
        '_UnconstrainedDevice': alphaclops.devices.unconstrained_device._UnconstrainedDevice,
        '_Unit': alphaclops.study.sweeps._Unit,
        'VarianceStoppingCriteria': alphaclops.work.VarianceStoppingCriteria,
        'VirtualTag': alphaclops.VirtualTag,
        'WaitGate': alphaclops.WaitGate,
        # The formatter keeps putting this back
        # pylint: disable=line-too-long
        'XEBPhasedFSimCharacterizationOptions': alphaclops.experiments.XEBPhasedFSimCharacterizationOptions,
        # pylint: enable=line-too-long
        '_XEigenState': alphaclops.value.product_state._XEigenState,
        'XPowGate': alphaclops.XPowGate,
        'XXPowGate': alphaclops.XXPowGate,
        '_YEigenState': alphaclops.value.product_state._YEigenState,
        'YPowGate': alphaclops.YPowGate,
        'YYPowGate': alphaclops.YYPowGate,
        '_ZEigenState': alphaclops.value.product_state._ZEigenState,
        'Zip': alphaclops.Zip,
        'ZipLongest': alphaclops.ZipLongest,
        'ZPowGate': alphaclops.ZPowGate,
        'ZZPowGate': alphaclops.ZZPowGate,
        # Old types, only supported for backwards-compatibility
        'BooleanHamiltonian': _boolean_hamiltonian_gate_op,  # Removed in v0.15
        'CrossEntropyResult': _cross_entropy_result,  # Removed in v0.16
        'CrossEntropyResultDict': _cross_entropy_result_dict,  # Removed in v0.16
        'IdentityOperation': _identity_operation_from_dict,
        'ParallelGateOperation': _parallel_gate_op,  # Removed in v0.14
        'SingleQubitMatrixGate': single_qubit_matrix_gate,
        'SymmetricalQidPair': _symmetricalqidpair,  # Removed in v0.15
        'TwoQubitMatrixGate': two_qubit_matrix_gate,
        'GlobalPhaseOperation': alphaclops.global_phase_operation,  # Removed in v0.16
        # not a alphaclops class, but treated as one:
        'pandas.DataFrame': pd.DataFrame,
        'pandas.Index': pd.Index,
        'pandas.MultiIndex': pd.MultiIndex.from_tuples,
        'sympy.Symbol': sympy.Symbol,
        'sympy.Add': lambda args: sympy.Add(*args),
        'sympy.Mul': lambda args: sympy.Mul(*args),
        'sympy.Pow': lambda args: sympy.Pow(*args),
        'sympy.GreaterThan': lambda args: sympy.GreaterThan(*args),
        'sympy.StrictGreaterThan': lambda args: sympy.StrictGreaterThan(*args),
        'sympy.LessThan': lambda args: sympy.LessThan(*args),
        'sympy.StrictLessThan': lambda args: sympy.StrictLessThan(*args),
        'sympy.Equality': lambda args: sympy.Equality(*args),
        'sympy.Unequality': lambda args: sympy.Unequality(*args),
        'sympy.Float': lambda approx: sympy.Float(approx),
        'sympy.Integer': sympy.Integer,
        'sympy.Rational': sympy.Rational,
        'sympy.pi': lambda: sympy.pi,
        'sympy.E': lambda: sympy.E,
        'sympy.EulerGamma': lambda: sympy.EulerGamma,
        'complex': complex,
        'datetime.datetime': _datetime,
    }
