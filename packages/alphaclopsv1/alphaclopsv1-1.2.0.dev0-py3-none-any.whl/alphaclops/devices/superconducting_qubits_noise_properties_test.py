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

from typing import Dict, List, Set, Tuple
import numpy as np
import alphaclops
import pytest

from alphaclops.devices.noise_properties import NoiseModelFromNoiseProperties
from alphaclops.devices.superconducting_qubits_noise_properties import (
    SuperconductingQubitsNoiseProperties,
)
from alphaclops.devices.noise_utils import OpIdentifier, PHYSICAL_GATE_TAG


DEFAULT_GATE_NS: Dict[type, float] = {
    alphaclops.ZPowGate: 25.0,
    alphaclops.MeasurementGate: 4000.0,
    alphaclops.ResetChannel: 250.0,
    alphaclops.PhasedXZGate: 25.0,
    alphaclops.FSimGate: 32.0,
    alphaclops.PhasedFSimGate: 32.0,
    alphaclops.ISwapPowGate: 32.0,
    alphaclops.CZPowGate: 32.0,
    # alphaclops.WaitGate is a special case.
}


def default_props(system_qubits: List[alphaclops.Qid], qubit_pairs: List[Tuple[alphaclops.Qid, alphaclops.Qid]]):
    return {
        'gate_times_ns': DEFAULT_GATE_NS,
        't1_ns': {q: 1e5 for q in system_qubits},
        'tphi_ns': {q: 2e5 for q in system_qubits},
        'readout_errors': {q: [0.001, 0.01] for q in system_qubits},
        'gate_pauli_errors': {
            **{
                OpIdentifier(g, q): 0.001
                for g in ExampleNoiseProperties.single_qubit_gates()
                for q in system_qubits
            },
            **{
                OpIdentifier(g, q0, q1): 0.01
                for g in ExampleNoiseProperties.two_qubit_gates()
                for q0, q1 in qubit_pairs
            },
        },
    }


class ExampleNoiseProperties(SuperconductingQubitsNoiseProperties):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def single_qubit_gates(cls) -> Set[type]:
        return {alphaclops.ZPowGate, alphaclops.PhasedXZGate, alphaclops.MeasurementGate, alphaclops.ResetChannel}

    @classmethod
    def symmetric_two_qubit_gates(cls) -> Set[type]:
        return {alphaclops.FSimGate, alphaclops.PhasedFSimGate, alphaclops.ISwapPowGate, alphaclops.CZPowGate}

    @classmethod
    def asymmetric_two_qubit_gates(cls) -> Set[type]:
        return set()


def test_init_validation():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    with pytest.raises(ValueError, match='Keys specified for T1 and Tphi are not identical.'):
        _ = ExampleNoiseProperties(
            gate_times_ns=DEFAULT_GATE_NS,
            t1_ns={},
            tphi_ns={q0: 1},
            readout_errors={q0: [0.1, 0.2]},
            gate_pauli_errors={},
        )

    with pytest.raises(ValueError, match='Symmetric errors can only apply to 2-qubit gates.'):
        _ = ExampleNoiseProperties(
            gate_times_ns=DEFAULT_GATE_NS,
            t1_ns={q0: 1},
            tphi_ns={q0: 1},
            readout_errors={q0: [0.1, 0.2]},
            gate_pauli_errors={OpIdentifier(alphaclops.CCNOT, q0, q1, q2): 0.1},
        )

    with pytest.raises(ValueError, match='does not appear in the symmetric or asymmetric'):
        _ = ExampleNoiseProperties(
            gate_times_ns=DEFAULT_GATE_NS,
            t1_ns={q0: 1},
            tphi_ns={q0: 1},
            readout_errors={q0: [0.1, 0.2]},
            gate_pauli_errors={
                OpIdentifier(alphaclops.CNOT, q0, q1): 0.1,
                OpIdentifier(alphaclops.CNOT, q1, q0): 0.1,
            },
        )

    with pytest.raises(ValueError, match='has errors but its symmetric id'):
        _ = ExampleNoiseProperties(
            gate_times_ns=DEFAULT_GATE_NS,
            t1_ns={q0: 1},
            tphi_ns={q0: 1},
            readout_errors={q0: [0.1, 0.2]},
            gate_pauli_errors={OpIdentifier(alphaclops.CZPowGate, q0, q1): 0.1},
        )

    # Single-qubit gates are ignored in symmetric-gate validation.
    test_props = ExampleNoiseProperties(
        gate_times_ns=DEFAULT_GATE_NS,
        t1_ns={q0: 1},
        tphi_ns={q0: 1},
        readout_errors={q0: [0.1, 0.2]},
        gate_pauli_errors={
            OpIdentifier(alphaclops.ZPowGate, q0): 0.1,
            OpIdentifier(alphaclops.CZPowGate, q0, q1): 0.1,
            OpIdentifier(alphaclops.CZPowGate, q1, q0): 0.1,
        },
    )
    assert test_props.expected_gates() == (
        ExampleNoiseProperties.single_qubit_gates()
        | ExampleNoiseProperties.symmetric_two_qubit_gates()
    )

    # All errors are ignored if validation is disabled.
    _ = ExampleNoiseProperties(
        gate_times_ns=DEFAULT_GATE_NS,
        t1_ns={},
        tphi_ns={q0: 1},
        readout_errors={q0: [0.1, 0.2]},
        gate_pauli_errors={
            OpIdentifier(alphaclops.CCNOT, q0, q1, q2): 0.1,
            OpIdentifier(alphaclops.CNOT, q0, q1): 0.1,
        },
        validate=False,
    )


def test_qubits():
    q0 = alphaclops.LineQubit(0)
    props = ExampleNoiseProperties(**default_props([q0], []))
    assert props.qubits == [q0]
    # Confirm memoization behavior.
    assert props.qubits == [q0]


def test_depol_memoization():
    # Verify that depolarizing error is memoized.
    q0 = alphaclops.LineQubit(0)
    props = ExampleNoiseProperties(**default_props([q0], []))
    depol_error_a = props._depolarizing_error
    depol_error_b = props._depolarizing_error
    assert depol_error_a == depol_error_b
    assert depol_error_a is depol_error_b


def test_depol_validation():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    # Create unvalidated properties with too many qubits on a Z gate.
    z_2q_props = ExampleNoiseProperties(
        gate_times_ns=DEFAULT_GATE_NS,
        t1_ns={q0: 1},
        tphi_ns={q0: 1},
        readout_errors={q0: [0.1, 0.2]},
        gate_pauli_errors={OpIdentifier(alphaclops.ZPowGate, q0, q1): 0.1},
        validate=False,
    )
    with pytest.raises(ValueError, match='takes 1 qubit'):
        _ = z_2q_props._depolarizing_error

    # Create unvalidated properties with too many qubits on a CZ gate.
    cz_3q_props = ExampleNoiseProperties(
        gate_times_ns=DEFAULT_GATE_NS,
        t1_ns={q0: 1},
        tphi_ns={q0: 1},
        readout_errors={q0: [0.1, 0.2]},
        gate_pauli_errors={OpIdentifier(alphaclops.CZPowGate, q0, q1, q2): 0.1},
        validate=False,
    )
    with pytest.raises(ValueError, match='takes 2 qubit'):
        _ = cz_3q_props._depolarizing_error

    # Unsupported gates are only checked in constructor.
    toffoli_props = ExampleNoiseProperties(
        gate_times_ns=DEFAULT_GATE_NS,
        t1_ns={q0: 1},
        tphi_ns={q0: 1},
        readout_errors={q0: [0.1, 0.2]},
        gate_pauli_errors={OpIdentifier(alphaclops.CCXPowGate, q0, q1, q2): 0.1},
        validate=False,
    )
    with pytest.raises(ValueError):
        _ = toffoli_props._depolarizing_error


@pytest.mark.parametrize(
    'op',
    [
        alphaclops.Z(alphaclops.LineQubit(0)) ** 0.3,
        alphaclops.PhasedXZGate(x_exponent=0.8, z_exponent=0.2, axis_phase_exponent=0.1).on(
            alphaclops.LineQubit(0)
        ),
    ],
)
def test_single_qubit_gates(op):
    q0 = alphaclops.LineQubit(0)
    props = ExampleNoiseProperties(**default_props([q0], []))
    model = NoiseModelFromNoiseProperties(props)
    circuit = alphaclops.Circuit(op)
    noisy_circuit = circuit.with_noise(model)
    assert len(noisy_circuit.moments) == 3
    assert len(noisy_circuit.moments[0].operations) == 1
    assert noisy_circuit.moments[0].operations[0] == op.with_tags(PHYSICAL_GATE_TAG)

    # Depolarizing noise
    assert len(noisy_circuit.moments[1].operations) == 1
    depol_op = noisy_circuit.moments[1].operations[0]
    assert isinstance(depol_op.gate, alphaclops.DepolarizingChannel)
    assert np.isclose(depol_op.gate.p, 0.00081252)

    # Thermal noise
    assert len(noisy_circuit.moments[2].operations) == 1
    thermal_op = noisy_circuit.moments[2].operations[0]
    assert isinstance(thermal_op.gate, alphaclops.KrausChannel)
    thermal_choi = alphaclops.kraus_to_choi(alphaclops.kraus(thermal_op))
    assert np.allclose(
        thermal_choi,
        [
            [1, 0, 0, 9.99750031e-01],
            [0, 2.49968753e-04, 0, 0],
            [0, 0, 0, 0],
            [9.99750031e-01, 0, 0, 9.99750031e-01],
        ],
    )


@pytest.mark.parametrize(
    'op', [alphaclops.ISWAP(*alphaclops.LineQubit.range(2)) ** 0.6, alphaclops.CZ(*alphaclops.LineQubit.range(2)) ** 0.3]
)
def test_two_qubit_gates(op):
    q0, q1 = alphaclops.LineQubit.range(2)
    props = ExampleNoiseProperties(**default_props([q0, q1], [(q0, q1), (q1, q0)]))
    model = NoiseModelFromNoiseProperties(props)
    circuit = alphaclops.Circuit(op)
    noisy_circuit = circuit.with_noise(model)
    assert len(noisy_circuit.moments) == 3
    assert len(noisy_circuit.moments[0].operations) == 1
    assert noisy_circuit.moments[0].operations[0] == op.with_tags(PHYSICAL_GATE_TAG)

    # Depolarizing noise
    assert len(noisy_circuit.moments[1].operations) == 1
    depol_op = noisy_circuit.moments[1].operations[0]
    assert isinstance(depol_op.gate, alphaclops.DepolarizingChannel)
    assert np.isclose(depol_op.gate.p, 0.00952008)

    # Thermal noise
    assert len(noisy_circuit.moments[2].operations) == 2
    thermal_op_0 = noisy_circuit.moments[2].operation_at(q0)
    thermal_op_1 = noisy_circuit.moments[2].operation_at(q1)
    assert isinstance(thermal_op_0.gate, alphaclops.KrausChannel)
    assert isinstance(thermal_op_1.gate, alphaclops.KrausChannel)
    thermal_choi_0 = alphaclops.kraus_to_choi(alphaclops.kraus(thermal_op_0))
    thermal_choi_1 = alphaclops.kraus_to_choi(alphaclops.kraus(thermal_op_1))
    expected_thermal_choi = np.array(
        [
            [1, 0, 0, 9.99680051e-01],
            [0, 3.19948805e-04, 0, 0],
            [0, 0, 0, 0],
            [9.99680051e-01, 0, 0, 9.99680051e-01],
        ]
    )
    assert np.allclose(thermal_choi_0, expected_thermal_choi)
    assert np.allclose(thermal_choi_1, expected_thermal_choi)


def test_measure_gates():
    q00, q01, q10, q11 = alphaclops.TensorCircuit.rect(2, 2)
    qubits = [q00, q01, q10, q11]
    props = ExampleNoiseProperties(
        **default_props(
            qubits,
            [
                (q00, q01),
                (q01, q00),
                (q10, q11),
                (q11, q10),
                (q00, q10),
                (q10, q00),
                (q01, q11),
                (q11, q01),
            ],
        )
    )
    model = NoiseModelFromNoiseProperties(props)
    op = alphaclops.measure(*qubits, key='m')
    circuit = alphaclops.Circuit(alphaclops.measure(*qubits, key='m'))
    noisy_circuit = circuit.with_noise(model)
    assert len(noisy_circuit.moments) == 2

    # Amplitude damping before measurement
    assert len(noisy_circuit.moments[0].operations) == 4
    for q in qubits:
        op = noisy_circuit.moments[0].operation_at(q)
        assert isinstance(op.gate, alphaclops.GeneralizedAmplitudeDampingChannel), q
        assert np.isclose(op.gate.p, 0.90909090), q
        assert np.isclose(op.gate.gamma, 0.011), q

    # Original measurement is after the noise.
    assert len(noisy_circuit.moments[1].operations) == 1
    # Measurements are untagged during reconstruction.
    assert noisy_circuit.moments[1] == circuit.moments[0]


def test_wait_gates():
    q0 = alphaclops.LineQubit(0)
    props = ExampleNoiseProperties(**default_props([q0], []))
    model = NoiseModelFromNoiseProperties(props)
    op = alphaclops.wait(q0, nanos=100)
    circuit = alphaclops.Circuit(op)
    noisy_circuit = circuit.with_noise(model)
    assert len(noisy_circuit.moments) == 2
    assert noisy_circuit.moments[0].operations[0] == op.with_tags(PHYSICAL_GATE_TAG)

    # No depolarizing noise because WaitGate has none.

    assert len(noisy_circuit.moments[1].operations) == 1
    thermal_op = noisy_circuit.moments[1].operations[0]
    assert isinstance(thermal_op.gate, alphaclops.KrausChannel)
    thermal_choi = alphaclops.kraus_to_choi(alphaclops.kraus(thermal_op))
    assert np.allclose(
        thermal_choi,
        [
            [1, 0, 0, 9.990005e-01],
            [0, 9.99500167e-04, 0, 0],
            [0, 0, 0, 0],
            [9.990005e-01, 0, 0, 9.990005e-01],
        ],
    )
