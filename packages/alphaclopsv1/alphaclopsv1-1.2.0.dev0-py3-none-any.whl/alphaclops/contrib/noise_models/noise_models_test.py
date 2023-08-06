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

import alphaclops
import alphaclops.contrib.noise_models as ccn
from alphaclops import ops
from alphaclops.testing import assert_equivalent_op_tree


def test_depol_noise():
    noise_model = ccn.DepolarizingNoiseModel(depol_prob=0.005)
    qubits = alphaclops.LineQubit.range(2)
    moment = alphaclops.Moment([alphaclops.X(qubits[0]), alphaclops.Y(qubits[1])])
    noisy_mom = noise_model.noisy_moment(moment, system_qubits=qubits)
    assert len(noisy_mom) == 2
    assert noisy_mom[0] == moment
    for g in noisy_mom[1]:
        assert isinstance(g.gate, alphaclops.DepolarizingChannel)


def test_depol_noise_prepend():
    noise_model = ccn.DepolarizingNoiseModel(depol_prob=0.005, prepend=True)
    qubits = alphaclops.LineQubit.range(2)
    moment = alphaclops.Moment([alphaclops.X(qubits[0]), alphaclops.Y(qubits[1])])
    noisy_mom = noise_model.noisy_moment(moment, system_qubits=qubits)
    assert len(noisy_mom) == 2
    assert noisy_mom[1] == moment
    for g in noisy_mom[0]:
        assert isinstance(g.gate, alphaclops.DepolarizingChannel)


# Composes depolarization noise with readout noise.
def test_readout_noise_after_moment():
    program = alphaclops.Circuit()
    qubits = alphaclops.LineQubit.range(3)
    program.append(
        [alphaclops.H(qubits[0]), alphaclops.CNOT(qubits[0], qubits[1]), alphaclops.CNOT(qubits[1], qubits[2])]
    )
    program.append(
        [
            alphaclops.measure(qubits[0], key='q0'),
            alphaclops.measure(qubits[1], key='q1'),
            alphaclops.measure(qubits[2], key='q2'),
        ],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )

    # Use noise model to generate circuit
    depol_noise = ccn.DepolarizingNoiseModel(depol_prob=0.01)
    readout_noise = ccn.ReadoutNoiseModel(bitflip_prob=0.05)
    noisy_circuit = alphaclops.Circuit(depol_noise.noisy_moments(program, qubits))
    noisy_circuit = alphaclops.Circuit(readout_noise.noisy_moments(noisy_circuit, qubits))

    # Insert channels explicitly
    true_noisy_program = alphaclops.Circuit()
    true_noisy_program.append([alphaclops.H(qubits[0])])
    true_noisy_program.append(
        [alphaclops.DepolarizingChannel(0.01).on(q).with_tags(ops.VirtualTag()) for q in qubits],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    true_noisy_program.append([alphaclops.CNOT(qubits[0], qubits[1])])
    true_noisy_program.append(
        [alphaclops.DepolarizingChannel(0.01).on(q).with_tags(ops.VirtualTag()) for q in qubits],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    true_noisy_program.append([alphaclops.CNOT(qubits[1], qubits[2])])
    true_noisy_program.append(
        [alphaclops.DepolarizingChannel(0.01).on(q).with_tags(ops.VirtualTag()) for q in qubits],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    true_noisy_program.append(
        [alphaclops.BitFlipChannel(0.05).on(q).with_tags(ops.VirtualTag()) for q in qubits]
    )
    true_noisy_program.append(
        [
            alphaclops.measure(qubits[0], key='q0'),
            alphaclops.measure(qubits[1], key='q1'),
            alphaclops.measure(qubits[2], key='q2'),
        ]
    )
    assert_equivalent_op_tree(true_noisy_program, noisy_circuit)


def test_readout_noise_no_prepend():
    noise_model = ccn.ReadoutNoiseModel(bitflip_prob=0.005, prepend=False)
    qubits = alphaclops.LineQubit.range(2)
    moment = alphaclops.Moment([alphaclops.measure(*qubits, key="meas")])
    noisy_mom = noise_model.noisy_moment(moment, system_qubits=qubits)
    assert len(noisy_mom) == 2
    assert noisy_mom[0] == moment
    for g in noisy_mom[1]:
        assert isinstance(g.gate, alphaclops.BitFlipChannel)


# Composes depolarization, damping, and readout noise (in that order).
def test_decay_noise_after_moment():
    program = alphaclops.Circuit()
    qubits = alphaclops.LineQubit.range(3)
    program.append(
        [alphaclops.H(qubits[0]), alphaclops.CNOT(qubits[0], qubits[1]), alphaclops.CNOT(qubits[1], qubits[2])]
    )
    program.append(
        [
            alphaclops.measure(qubits[0], key='q0'),
            alphaclops.measure(qubits[1], key='q1'),
            alphaclops.measure(qubits[2], key='q2'),
        ],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )

    # Use noise model to generate circuit
    depol_noise = ccn.DepolarizingNoiseModel(depol_prob=0.01)
    readout_noise = ccn.ReadoutNoiseModel(bitflip_prob=0.05)
    damping_noise = ccn.DampedReadoutNoiseModel(decay_prob=0.02)
    noisy_circuit = alphaclops.Circuit(depol_noise.noisy_moments(program, qubits))
    noisy_circuit = alphaclops.Circuit(damping_noise.noisy_moments(noisy_circuit, qubits))
    noisy_circuit = alphaclops.Circuit(readout_noise.noisy_moments(noisy_circuit, qubits))

    # Insert channels explicitly
    true_noisy_program = alphaclops.Circuit()
    true_noisy_program.append([alphaclops.H(qubits[0])])
    true_noisy_program.append(
        [alphaclops.DepolarizingChannel(0.01).on(q).with_tags(ops.VirtualTag()) for q in qubits],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    true_noisy_program.append([alphaclops.CNOT(qubits[0], qubits[1])])
    true_noisy_program.append(
        [alphaclops.DepolarizingChannel(0.01).on(q).with_tags(ops.VirtualTag()) for q in qubits],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    true_noisy_program.append([alphaclops.CNOT(qubits[1], qubits[2])])
    true_noisy_program.append(
        [alphaclops.DepolarizingChannel(0.01).on(q).with_tags(ops.VirtualTag()) for q in qubits],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    true_noisy_program.append(
        [alphaclops.AmplitudeDampingChannel(0.02).on(q).with_tags(ops.VirtualTag()) for q in qubits]
    )
    true_noisy_program.append(
        [alphaclops.BitFlipChannel(0.05).on(q).with_tags(ops.VirtualTag()) for q in qubits]
    )
    true_noisy_program.append(
        [
            alphaclops.measure(qubits[0], key='q0'),
            alphaclops.measure(qubits[1], key='q1'),
            alphaclops.measure(qubits[2], key='q2'),
        ]
    )
    assert_equivalent_op_tree(true_noisy_program, noisy_circuit)


def test_damped_readout_noise_no_prepend():
    noise_model = ccn.DampedReadoutNoiseModel(decay_prob=0.005, prepend=False)
    qubits = alphaclops.LineQubit.range(2)
    moment = alphaclops.Moment([alphaclops.measure(*qubits, key="meas")])
    noisy_mom = noise_model.noisy_moment(moment, system_qubits=qubits)
    assert len(noisy_mom) == 2
    assert noisy_mom[0] == moment
    for g in noisy_mom[1]:
        assert isinstance(g.gate, alphaclops.AmplitudeDampingChannel)


# Test the aggregate noise models.
def test_aggregate_readout_noise_after_moment():
    program = alphaclops.Circuit()
    qubits = alphaclops.LineQubit.range(3)
    program.append(
        [alphaclops.H(qubits[0]), alphaclops.CNOT(qubits[0], qubits[1]), alphaclops.CNOT(qubits[1], qubits[2])]
    )
    program.append(
        [
            alphaclops.measure(qubits[0], key='q0'),
            alphaclops.measure(qubits[1], key='q1'),
            alphaclops.measure(qubits[2], key='q2'),
        ],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )

    # Use noise model to generate circuit
    noise_model = ccn.DepolarizingWithReadoutNoiseModel(depol_prob=0.01, bitflip_prob=0.05)
    noisy_circuit = alphaclops.Circuit(noise_model.noisy_moments(program, qubits))

    # Insert channels explicitly
    true_noisy_program = alphaclops.Circuit()
    true_noisy_program.append([alphaclops.H(qubits[0])])
    true_noisy_program.append(
        [alphaclops.DepolarizingChannel(0.01).on(q) for q in qubits],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    true_noisy_program.append([alphaclops.CNOT(qubits[0], qubits[1])])
    true_noisy_program.append(
        [alphaclops.DepolarizingChannel(0.01).on(q) for q in qubits],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    true_noisy_program.append([alphaclops.CNOT(qubits[1], qubits[2])])
    true_noisy_program.append(
        [alphaclops.DepolarizingChannel(0.01).on(q) for q in qubits],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    true_noisy_program.append([alphaclops.BitFlipChannel(0.05).on(q) for q in qubits])
    true_noisy_program.append(
        [
            alphaclops.measure(qubits[0], key='q0'),
            alphaclops.measure(qubits[1], key='q1'),
            alphaclops.measure(qubits[2], key='q2'),
        ]
    )
    assert_equivalent_op_tree(true_noisy_program, noisy_circuit)


def test_aggregate_decay_noise_after_moment():
    program = alphaclops.Circuit()
    qubits = alphaclops.LineQubit.range(3)
    program.append(
        [alphaclops.H(qubits[0]), alphaclops.CNOT(qubits[0], qubits[1]), alphaclops.CNOT(qubits[1], qubits[2])]
    )
    program.append(
        [
            alphaclops.measure(qubits[0], key='q0'),
            alphaclops.measure(qubits[1], key='q1'),
            alphaclops.measure(qubits[2], key='q2'),
        ],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )

    # Use noise model to generate circuit
    noise_model = ccn.DepolarizingWithDampedReadoutNoiseModel(
        depol_prob=0.01, decay_prob=0.02, bitflip_prob=0.05
    )
    noisy_circuit = alphaclops.Circuit(noise_model.noisy_moments(program, qubits))

    # Insert channels explicitly
    true_noisy_program = alphaclops.Circuit()
    true_noisy_program.append([alphaclops.H(qubits[0])])
    true_noisy_program.append(
        [alphaclops.DepolarizingChannel(0.01).on(q) for q in qubits],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    true_noisy_program.append([alphaclops.CNOT(qubits[0], qubits[1])])
    true_noisy_program.append(
        [alphaclops.DepolarizingChannel(0.01).on(q) for q in qubits],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    true_noisy_program.append([alphaclops.CNOT(qubits[1], qubits[2])])
    true_noisy_program.append(
        [alphaclops.DepolarizingChannel(0.01).on(q) for q in qubits],
        strategy=alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    true_noisy_program.append([alphaclops.AmplitudeDampingChannel(0.02).on(q) for q in qubits])
    true_noisy_program.append([alphaclops.BitFlipChannel(0.05).on(q) for q in qubits])
    true_noisy_program.append(
        [
            alphaclops.measure(qubits[0], key='q0'),
            alphaclops.measure(qubits[1], key='q1'),
            alphaclops.measure(qubits[2], key='q2'),
        ]
    )
    assert_equivalent_op_tree(true_noisy_program, noisy_circuit)
