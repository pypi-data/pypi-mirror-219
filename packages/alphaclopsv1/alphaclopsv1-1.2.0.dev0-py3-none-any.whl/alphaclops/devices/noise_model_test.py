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

from typing import Sequence

import numpy as np
import pytest

import alphaclops
from alphaclops import ops
from alphaclops.devices.noise_model import validate_all_measurements
from alphaclops.testing import assert_equivalent_op_tree


def assert_equivalent_op_tree_sequence(x: Sequence[alphaclops.OP_TREE], y: Sequence[alphaclops.OP_TREE]):
    assert len(x) == len(y)
    for a, b in zip(x, y):
        assert_equivalent_op_tree(a, b)


def test_requires_one_override():
    class C(alphaclops.NoiseModel):
        pass

    with pytest.raises(TypeError, match='abstract'):
        _ = C()


def test_infers_other_methods():
    q = alphaclops.LineQubit(0)

    class NoiseModelWithNoisyMomentListMethod(alphaclops.NoiseModel):
        def noisy_moments(self, moments, system_qubits):
            result = []
            for moment in moments:
                if moment.operations:
                    result.append(
                        alphaclops.X(moment.operations[0].qubits[0]).with_tags(ops.VirtualTag())
                    )
                else:
                    result.append([])
            return result

    a = NoiseModelWithNoisyMomentListMethod()
    assert_equivalent_op_tree(a.noisy_operation(alphaclops.H(q)), alphaclops.X(q).with_tags(ops.VirtualTag()))
    assert_equivalent_op_tree(
        a.noisy_moment(alphaclops.Moment([alphaclops.H(q)]), [q]), alphaclops.X(q).with_tags(ops.VirtualTag())
    )
    assert_equivalent_op_tree_sequence(
        a.noisy_moments([alphaclops.Moment(), alphaclops.Moment([alphaclops.H(q)])], [q]),
        [[], alphaclops.X(q).with_tags(ops.VirtualTag())],
    )

    class NoiseModelWithNoisyMomentMethod(alphaclops.NoiseModel):
        def noisy_moment(self, moment, system_qubits):
            return [y.with_tags(ops.VirtualTag()) for y in alphaclops.Y.on_each(*moment.qubits)]

    b = NoiseModelWithNoisyMomentMethod()
    assert_equivalent_op_tree(b.noisy_operation(alphaclops.H(q)), alphaclops.Y(q).with_tags(ops.VirtualTag()))
    assert_equivalent_op_tree(
        b.noisy_moment(alphaclops.Moment([alphaclops.H(q)]), [q]), alphaclops.Y(q).with_tags(ops.VirtualTag())
    )
    assert_equivalent_op_tree_sequence(
        b.noisy_moments([alphaclops.Moment(), alphaclops.Moment([alphaclops.H(q)])], [q]),
        [[], alphaclops.Y(q).with_tags(ops.VirtualTag())],
    )

    class NoiseModelWithNoisyOperationMethod(alphaclops.NoiseModel):
        def noisy_operation(self, operation: 'alphaclops.Operation'):
            return alphaclops.Z(operation.qubits[0]).with_tags(ops.VirtualTag())

    c = NoiseModelWithNoisyOperationMethod()
    assert_equivalent_op_tree(c.noisy_operation(alphaclops.H(q)), alphaclops.Z(q).with_tags(ops.VirtualTag()))
    assert_equivalent_op_tree(
        c.noisy_moment(alphaclops.Moment([alphaclops.H(q)]), [q]), alphaclops.Z(q).with_tags(ops.VirtualTag())
    )
    assert_equivalent_op_tree_sequence(
        c.noisy_moments([alphaclops.Moment(), alphaclops.Moment([alphaclops.H(q)])], [q]),
        [[], alphaclops.Z(q).with_tags(ops.VirtualTag())],
    )


def test_no_noise():
    q = alphaclops.LineQubit(0)
    m = alphaclops.Moment([alphaclops.X(q)])
    assert alphaclops.NO_NOISE.noisy_operation(alphaclops.X(q)) == alphaclops.X(q)
    assert alphaclops.NO_NOISE.noisy_moment(m, [q]) is m
    assert alphaclops.NO_NOISE.noisy_moments([m, m], [q]) == [m, m]
    assert alphaclops.NO_NOISE == alphaclops.NO_NOISE
    assert str(alphaclops.NO_NOISE) == '(no noise)'
    alphaclops.testing.assert_equivalent_repr(alphaclops.NO_NOISE)


def test_constant_qubit_noise():
    a, b, c = alphaclops.LineQubit.range(3)
    damp = alphaclops.amplitude_damp(0.5)
    damp_all = alphaclops.ConstantQubitNoiseModel(damp)
    actual = damp_all.noisy_moments([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment()], [a, b, c])
    expected = [
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment(d.with_tags(ops.VirtualTag()) for d in [damp(a), damp(b), damp(c)]),
        ],
        [
            alphaclops.Moment(),
            alphaclops.Moment(d.with_tags(ops.VirtualTag()) for d in [damp(a), damp(b), damp(c)]),
        ],
    ]
    assert actual == expected
    alphaclops.testing.assert_equivalent_repr(damp_all)

    with pytest.raises(ValueError, match='num_qubits'):
        _ = alphaclops.ConstantQubitNoiseModel(alphaclops.CNOT ** 0.01)


def test_constant_qubit_noise_prepend():
    a, b, c = alphaclops.LineQubit.range(3)
    damp = alphaclops.amplitude_damp(0.5)
    damp_all = alphaclops.ConstantQubitNoiseModel(damp, prepend=True)
    actual = damp_all.noisy_moments([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment()], [a, b, c])
    expected = [
        [
            alphaclops.Moment(d.with_tags(ops.VirtualTag()) for d in [damp(a), damp(b), damp(c)]),
            alphaclops.Moment([alphaclops.X(a)]),
        ],
        [
            alphaclops.Moment(d.with_tags(ops.VirtualTag()) for d in [damp(a), damp(b), damp(c)]),
            alphaclops.Moment(),
        ],
    ]
    assert actual == expected
    alphaclops.testing.assert_equivalent_repr(damp_all)


def test_noise_composition():
    # Verify that noise models can be composed without regard to ordering, as
    # long as the noise operators commute with one another.
    a, b, c = alphaclops.LineQubit.range(3)
    noise_z = alphaclops.ConstantQubitNoiseModel(alphaclops.Z)
    noise_inv_s = alphaclops.ConstantQubitNoiseModel(alphaclops.S ** -1)
    base_moments = [alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.Y(b)]), alphaclops.Moment([alphaclops.H(c)])]
    circuit_z = alphaclops.Circuit(noise_z.noisy_moments(base_moments, [a, b, c]))
    circuit_s = alphaclops.Circuit(noise_inv_s.noisy_moments(base_moments, [a, b, c]))
    actual_zs = alphaclops.Circuit(noise_inv_s.noisy_moments(circuit_z.moments, [a, b, c]))
    actual_sz = alphaclops.Circuit(noise_z.noisy_moments(circuit_s.moments, [a, b, c]))

    expected_circuit = alphaclops.Circuit(
        alphaclops.Moment([alphaclops.X(a)]),
        alphaclops.Moment([alphaclops.S(a), alphaclops.S(b), alphaclops.S(c)]),
        alphaclops.Moment([alphaclops.Y(b)]),
        alphaclops.Moment([alphaclops.S(a), alphaclops.S(b), alphaclops.S(c)]),
        alphaclops.Moment([alphaclops.H(c)]),
        alphaclops.Moment([alphaclops.S(a), alphaclops.S(b), alphaclops.S(c)]),
    )

    # All of the gates will be the same, just out of order. Merging fixes this.
    actual_zs = alphaclops.merge_single_qubit_gates_to_phased_x_and_z(actual_zs)
    actual_sz = alphaclops.merge_single_qubit_gates_to_phased_x_and_z(actual_sz)
    expected_circuit = alphaclops.merge_single_qubit_gates_to_phased_x_and_z(expected_circuit)
    assert_equivalent_op_tree(actual_zs, actual_sz)
    assert_equivalent_op_tree(actual_zs, expected_circuit)


def test_constant_qubit_noise_repr():
    alphaclops.testing.assert_equivalent_repr(alphaclops.ConstantQubitNoiseModel(alphaclops.X ** 0.01))


def test_wrap():
    class Forget(alphaclops.NoiseModel):
        def noisy_operation(self, operation):
            raise NotImplementedError()

    forget = Forget()

    assert alphaclops.NoiseModel.from_noise_model_like(None) is alphaclops.NO_NOISE
    assert alphaclops.NoiseModel.from_noise_model_like(
        alphaclops.depolarize(0.1)
    ) == alphaclops.ConstantQubitNoiseModel(alphaclops.depolarize(0.1))
    assert alphaclops.NoiseModel.from_noise_model_like(alphaclops.Z ** 0.01) == alphaclops.ConstantQubitNoiseModel(
        alphaclops.Z ** 0.01
    )
    assert alphaclops.NoiseModel.from_noise_model_like(forget) is forget

    with pytest.raises(TypeError, match='Expected a NOISE_MODEL_LIKE'):
        _ = alphaclops.NoiseModel.from_noise_model_like('test')

    with pytest.raises(ValueError, match='Multi-qubit gate'):
        _ = alphaclops.NoiseModel.from_noise_model_like(alphaclops.CZ ** 0.01)


def test_gate_substitution_noise_model():
    def _overrotation(op):
        if isinstance(op.gate, alphaclops.XPowGate):
            return alphaclops.XPowGate(exponent=op.gate.exponent + 0.1).on(*op.qubits)
        return op

    noise = alphaclops.devices.noise_model.GateSubstitutionNoiseModel(_overrotation)

    q0 = alphaclops.LineQubit(0)
    circuit = alphaclops.Circuit(alphaclops.X(q0) ** 0.5, alphaclops.Y(q0))
    circuit2 = alphaclops.Circuit(alphaclops.X(q0) ** 0.6, alphaclops.Y(q0))
    rho1 = alphaclops.final_density_matrix(circuit, noise=noise)
    rho2 = alphaclops.final_density_matrix(circuit2)
    np.testing.assert_allclose(rho1, rho2)


def test_moment_is_measurements():
    q = alphaclops.LineQubit.range(2)
    circ = alphaclops.Circuit([alphaclops.X(q[0]), alphaclops.X(q[1]), alphaclops.measure(*q, key='z')])
    assert not validate_all_measurements(circ[0])
    assert validate_all_measurements(circ[1])


def test_moment_is_measurements_mixed1():
    q = alphaclops.LineQubit.range(2)
    circ = alphaclops.Circuit([alphaclops.X(q[0]), alphaclops.X(q[1]), alphaclops.measure(q[0], key='z'), alphaclops.Z(q[1])])
    assert not validate_all_measurements(circ[0])
    with pytest.raises(ValueError) as e:
        validate_all_measurements(circ[1])
    assert e.match(".*must be homogeneous: all measurements.*")


def test_moment_is_measurements_mixed2():
    q = alphaclops.LineQubit.range(2)
    circ = alphaclops.Circuit([alphaclops.X(q[0]), alphaclops.X(q[1]), alphaclops.Z(q[0]), alphaclops.measure(q[1], key='z')])
    assert not validate_all_measurements(circ[0])
    with pytest.raises(ValueError) as e:
        validate_all_measurements(circ[1])
    assert e.match(".*must be homogeneous: all measurements.*")
