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
import itertools
import random
from typing import Type

from unittest import mock
import numpy as np
import pytest
import sympy

import alphaclops


def test_invalid_dtype():
    with pytest.raises(ValueError, match='complex'):
        alphaclops.Simulator(dtype=np.int32)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_no_measurements(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)

    circuit = alphaclops.Circuit(alphaclops.X(q0), alphaclops.X(q1))
    with pytest.raises(ValueError, match="no measurements"):
        simulator.run(circuit)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_no_results(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)

    circuit = alphaclops.Circuit(alphaclops.X(q0), alphaclops.X(q1))
    with pytest.raises(ValueError, match="no measurements"):
        simulator.run(circuit)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_empty_circuit(dtype: Type[np.complexfloating], split: bool):
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    with pytest.raises(ValueError, match="no measurements"):
        simulator.run(alphaclops.Circuit())


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_reset(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQid.for_qid_shape((2, 3))
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = alphaclops.Circuit(
        alphaclops.H(q0),
        alphaclops.XPowGate(dimension=3)(q1) ** 2,
        alphaclops.reset(q0),
        alphaclops.measure(q0, key='m0'),
        alphaclops.measure(q1, key='m1a'),
        alphaclops.reset(q1),
        alphaclops.measure(q1, key='m1b'),
    )
    meas = simulator.run(circuit, repetitions=100).measurements
    assert np.array_equal(meas['m0'], np.zeros((100, 1)))
    assert np.array_equal(meas['m1a'], np.full((100, 1), 2))
    assert np.array_equal(meas['m1b'], np.zeros((100, 1)))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_bit_flips(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = alphaclops.Circuit(
                (alphaclops.X ** b0)(q0), (alphaclops.X ** b1)(q1), alphaclops.measure(q0), alphaclops.measure(q1)
            )
            result = simulator.run(circuit)
            np.testing.assert_equal(result.measurements, {'q(0)': [[b0]], 'q(1)': [[b1]]})


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_measure_at_end_no_repetitions(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                circuit = alphaclops.Circuit(
                    (alphaclops.X ** b0)(q0), (alphaclops.X ** b1)(q1), alphaclops.measure(q0), alphaclops.measure(q1)
                )
                result = simulator.run(circuit, repetitions=0)
                np.testing.assert_equal(
                    result.measurements, {'q(0)': np.empty([0, 1]), 'q(1)': np.empty([0, 1])}
                )
                assert result.repetitions == 0
        assert mock_sim.call_count == 0


def test_run_repetitions_terminal_measurement_stochastic():
    q = alphaclops.LineQubit(0)
    c = alphaclops.Circuit(alphaclops.H(q), alphaclops.measure(q, key='q'))
    results = alphaclops.Simulator().run(c, repetitions=10000)
    assert 1000 <= sum(v[0] for v in results.measurements['q']) < 9000


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_repetitions_measure_at_end(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                circuit = alphaclops.Circuit(
                    (alphaclops.X ** b0)(q0), (alphaclops.X ** b1)(q1), alphaclops.measure(q0), alphaclops.measure(q1)
                )
                result = simulator.run(circuit, repetitions=3)
                np.testing.assert_equal(
                    result.measurements, {'q(0)': [[b0]] * 3, 'q(1)': [[b1]] * 3}
                )
                assert result.repetitions == 3
        # We expect one call per b0,b1.
        assert mock_sim.call_count == 8


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_invert_mask_measure_not_terminal(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                circuit = alphaclops.Circuit(
                    (alphaclops.X ** b0)(q0),
                    (alphaclops.X ** b1)(q1),
                    alphaclops.measure(q0, q1, key='m', invert_mask=(True, False)),
                    alphaclops.X(q0),
                )
                result = simulator.run(circuit, repetitions=3)
                np.testing.assert_equal(result.measurements, {'m': [[1 - b0, b1]] * 3})
                assert result.repetitions == 3
        # We expect repeated calls per b0,b1 instead of one call.
        assert mock_sim.call_count > 4


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_partial_invert_mask_measure_not_terminal(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                circuit = alphaclops.Circuit(
                    (alphaclops.X ** b0)(q0),
                    (alphaclops.X ** b1)(q1),
                    alphaclops.measure(q0, q1, key='m', invert_mask=(True,)),
                    alphaclops.X(q0),
                )
                result = simulator.run(circuit, repetitions=3)
                np.testing.assert_equal(result.measurements, {'m': [[1 - b0, b1]] * 3})
                assert result.repetitions == 3
        # We expect repeated calls per b0,b1 instead of one call.
        assert mock_sim.call_count > 4


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_measurement_not_terminal_no_repetitions(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                circuit = alphaclops.Circuit(
                    (alphaclops.X ** b0)(q0),
                    (alphaclops.X ** b1)(q1),
                    alphaclops.measure(q0),
                    alphaclops.measure(q1),
                    alphaclops.H(q0),
                    alphaclops.H(q1),
                )
                result = simulator.run(circuit, repetitions=0)
                np.testing.assert_equal(
                    result.measurements, {'q(0)': np.empty([0, 1]), 'q(1)': np.empty([0, 1])}
                )
                assert result.repetitions == 0
        assert mock_sim.call_count == 0


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_repetitions_measurement_not_terminal(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    with mock.patch.object(simulator, '_core_iterator', wraps=simulator._core_iterator) as mock_sim:
        for b0 in [0, 1]:
            for b1 in [0, 1]:
                circuit = alphaclops.Circuit(
                    (alphaclops.X ** b0)(q0),
                    (alphaclops.X ** b1)(q1),
                    alphaclops.measure(q0),
                    alphaclops.measure(q1),
                    alphaclops.H(q0),
                    alphaclops.H(q1),
                )
                result = simulator.run(circuit, repetitions=3)
                np.testing.assert_equal(
                    result.measurements, {'q(0)': [[b0]] * 3, 'q(1)': [[b1]] * 3}
                )
                assert result.repetitions == 3
        # We expect repeated calls per b0,b1 instead of one call.
        assert mock_sim.call_count > 4


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_param_resolver(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = alphaclops.Circuit(
                (alphaclops.X ** sympy.Symbol('b0'))(q0),
                (alphaclops.X ** sympy.Symbol('b1'))(q1),
                alphaclops.measure(q0),
                alphaclops.measure(q1),
            )
            param_resolver = alphaclops.ParamResolver({'b0': b0, 'b1': b1})
            result = simulator.run(circuit, param_resolver=param_resolver)
            np.testing.assert_equal(result.measurements, {'q(0)': [[b0]], 'q(1)': [[b1]]})
            np.testing.assert_equal(result.params, param_resolver)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_mixture(dtype: Type[np.complexfloating], split: bool):
    q0 = alphaclops.LineQubit(0)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = alphaclops.Circuit(alphaclops.bit_flip(0.5)(q0), alphaclops.measure(q0))
    result = simulator.run(circuit, repetitions=100)
    assert 20 < sum(result.measurements['q(0)'])[0] < 80


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_mixture_with_gates(dtype: Type[np.complexfloating], split: bool):
    q0 = alphaclops.LineQubit(0)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split, seed=23)
    circuit = alphaclops.Circuit(alphaclops.H(q0), alphaclops.phase_flip(0.5)(q0), alphaclops.H(q0), alphaclops.measure(q0))
    result = simulator.run(circuit, repetitions=100)
    assert sum(result.measurements['q(0)'])[0] < 80
    assert sum(result.measurements['q(0)'])[0] > 20


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_correlations(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = alphaclops.Circuit(alphaclops.H(q0), alphaclops.CNOT(q0, q1), alphaclops.measure(q0, q1))
    for _ in range(10):
        result = simulator.run(circuit)
        bits = result.measurements['q(0),q(1)'][0]
        assert bits[0] == bits[1]


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_measure_multiple_qubits(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = alphaclops.Circuit((alphaclops.X ** b0)(q0), (alphaclops.X ** b1)(q1), alphaclops.measure(q0, q1))
            result = simulator.run(circuit, repetitions=3)
            np.testing.assert_equal(result.measurements, {'q(0),q(1)': [[b0, b1]] * 3})


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_run_sweeps_param_resolvers(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = alphaclops.Circuit(
                (alphaclops.X ** sympy.Symbol('b0'))(q0),
                (alphaclops.X ** sympy.Symbol('b1'))(q1),
                alphaclops.measure(q0),
                alphaclops.measure(q1),
            )
            params = [
                alphaclops.ParamResolver({'b0': b0, 'b1': b1}),
                alphaclops.ParamResolver({'b0': b1, 'b1': b0}),
            ]
            results = simulator.run_sweep(circuit, params=params)

            assert len(results) == 2
            np.testing.assert_equal(results[0].measurements, {'q(0)': [[b0]], 'q(1)': [[b1]]})
            np.testing.assert_equal(results[1].measurements, {'q(0)': [[b1]], 'q(1)': [[b0]]})
            assert results[0].params == params[0]
            assert results[1].params == params[1]


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_random_unitary(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for _ in range(10):
        random_circuit = alphaclops.testing.random_circuit(qubits=[q0, q1], n_moments=8, op_density=0.99)
        circuit_unitary = []
        for x in range(4):
            result = simulator.simulate(random_circuit, qubit_order=[q0, q1], initial_state=x)
            circuit_unitary.append(result.final_state_vector)
        np.testing.assert_almost_equal(
            np.transpose(np.array(circuit_unitary)),
            random_circuit.unitary(qubit_order=[q0, q1]),
            decimal=6,
        )


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_no_circuit(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = alphaclops.Circuit()
    result = simulator.simulate(circuit, qubit_order=[q0, q1])
    np.testing.assert_almost_equal(result.final_state_vector, np.array([1, 0, 0, 0]))
    assert len(result.measurements) == 0


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = alphaclops.Circuit(alphaclops.H(q0), alphaclops.H(q1))
    result = simulator.simulate(circuit, qubit_order=[q0, q1])
    np.testing.assert_almost_equal(result.final_state_vector, np.array([0.5, 0.5, 0.5, 0.5]))
    assert len(result.measurements) == 0


class _TestMixture(alphaclops.Gate):
    def __init__(self, gate_options):
        self.gate_options = gate_options

    def _qid_shape_(self):
        return alphaclops.qid_shape(self.gate_options[0], ())

    def _mixture_(self):
        return [(1 / len(self.gate_options), alphaclops.unitary(g)) for g in self.gate_options]


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_qudits(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQid.for_qid_shape((3, 4))
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = alphaclops.Circuit(alphaclops.XPowGate(dimension=3)(q0), alphaclops.XPowGate(dimension=4)(q1) ** 3)
    result = simulator.simulate(circuit, qubit_order=[q0, q1])
    expected = np.zeros(12)
    expected[4 * 1 + 3] = 1
    np.testing.assert_almost_equal(result.final_state_vector, expected)
    assert len(result.measurements) == 0


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_mixtures(dtype: Type[np.complexfloating], split: bool):
    q0 = alphaclops.LineQubit(0)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    circuit = alphaclops.Circuit(alphaclops.bit_flip(0.5)(q0), alphaclops.measure(q0))
    count = 0
    for _ in range(100):
        result = simulator.simulate(circuit, qubit_order=[q0])
        if result.measurements['q(0)']:
            np.testing.assert_almost_equal(result.final_state_vector, np.array([0, 1]))
            count += 1
        else:
            np.testing.assert_almost_equal(result.final_state_vector, np.array([1, 0]))
    assert count < 80 and count > 20


@pytest.mark.parametrize(
    'dtype, split', itertools.product([np.complex64, np.complex128], [True, False])
)
def test_simulate_qudit_mixtures(dtype: Type[np.complexfloating], split: bool):
    q0 = alphaclops.LineQid(0, 3)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    mixture = _TestMixture(
        [
            alphaclops.XPowGate(dimension=3) ** 0,
            alphaclops.XPowGate(dimension=3),
            alphaclops.XPowGate(dimension=3) ** 2,
        ]
    )
    circuit = alphaclops.Circuit(mixture(q0), alphaclops.measure(q0))
    counts = {0: 0, 1: 0, 2: 0}
    for _ in range(300):
        result = simulator.simulate(circuit, qubit_order=[q0])
        meas = result.measurements['q(0) (d=3)'][0]
        counts[meas] += 1
        np.testing.assert_almost_equal(
            result.final_state_vector, np.array([meas == 0, meas == 1, meas == 2])
        )
    assert counts[0] < 160 and counts[0] > 40
    assert counts[1] < 160 and counts[1] > 40
    assert counts[2] < 160 and counts[2] > 40


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_bit_flips(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = alphaclops.Circuit(
                (alphaclops.X ** b0)(q0), (alphaclops.X ** b1)(q1), alphaclops.measure(q0), alphaclops.measure(q1)
            )
            result = simulator.simulate(circuit)
            np.testing.assert_equal(result.measurements, {'q(0)': [b0], 'q(1)': [b1]})
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b0][b1] = 1.0
            np.testing.assert_equal(result.final_state_vector, np.reshape(expected_state, 4))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_initial_state(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = alphaclops.Circuit((alphaclops.X ** b0)(q0), (alphaclops.X ** b1)(q1))
            result = simulator.simulate(circuit, initial_state=1)
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b0][1 - b1] = 1.0
            np.testing.assert_equal(result.final_state_vector, np.reshape(expected_state, 4))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulation_state(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = alphaclops.Circuit((alphaclops.X ** b0)(q0), (alphaclops.X ** b1)(q1))
            args = simulator._create_simulation_state(initial_state=1, qubits=(q0, q1))
            result = simulator.simulate(circuit, initial_state=args)
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b0][1 - b1] = 1.0
            np.testing.assert_equal(result.final_state_vector, np.reshape(expected_state, 4))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_qubit_order(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = alphaclops.Circuit((alphaclops.X ** b0)(q0), (alphaclops.X ** b1)(q1))
            result = simulator.simulate(circuit, qubit_order=[q1, q0])
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b1][b0] = 1.0
            np.testing.assert_equal(result.final_state_vector, np.reshape(expected_state, 4))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_param_resolver(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = alphaclops.Circuit(
                (alphaclops.X ** sympy.Symbol('b0'))(q0), (alphaclops.X ** sympy.Symbol('b1'))(q1)
            )
            resolver = {'b0': b0, 'b1': b1}
            result = simulator.simulate(circuit, param_resolver=resolver)  # type: ignore
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b0][b1] = 1.0
            np.testing.assert_equal(result.final_state_vector, np.reshape(expected_state, 4))
            assert result.params == alphaclops.ParamResolver(resolver)  # type: ignore
            assert len(result.measurements) == 0


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_measure_multiple_qubits(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = alphaclops.Circuit((alphaclops.X ** b0)(q0), (alphaclops.X ** b1)(q1), alphaclops.measure(q0, q1))
            result = simulator.simulate(circuit)
            np.testing.assert_equal(result.measurements, {'q(0),q(1)': [b0, b1]})


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_sweeps_param_resolver(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for b0 in [0, 1]:
        for b1 in [0, 1]:
            circuit = alphaclops.Circuit(
                (alphaclops.X ** sympy.Symbol('b0'))(q0), (alphaclops.X ** sympy.Symbol('b1'))(q1)
            )
            params = [
                alphaclops.ParamResolver({'b0': b0, 'b1': b1}),
                alphaclops.ParamResolver({'b0': b1, 'b1': b0}),
            ]
            results = simulator.simulate_sweep(circuit, params=params)
            expected_state = np.zeros(shape=(2, 2))
            expected_state[b0][b1] = 1.0
            np.testing.assert_equal(results[0].final_state_vector, np.reshape(expected_state, 4))

            expected_state = np.zeros(shape=(2, 2))
            expected_state[b1][b0] = 1.0
            np.testing.assert_equal(results[1].final_state_vector, np.reshape(expected_state, 4))

            assert results[0].params == params[0]
            assert results[1].params == params[1]


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(alphaclops.H(q0), alphaclops.H(q1), alphaclops.H(q0), alphaclops.H(q1))
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        if i == 0:
            np.testing.assert_almost_equal(step.state_vector(copy=True), np.array([0.5] * 4))
        else:
            np.testing.assert_almost_equal(step.state_vector(copy=True), np.array([1, 0, 0, 0]))


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps_empty_circuit(dtype: Type[np.complexfloating], split: bool):
    circuit = alphaclops.Circuit()
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    step = None
    for step in simulator.simulate_moment_steps(circuit):
        pass
    assert np.allclose(step.state_vector(copy=True), np.array([1]))
    assert not step.qubit_map


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps_sample(dtype: Type[np.complexfloating], split: bool):
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(alphaclops.H(q0), alphaclops.CNOT(q0, q1))
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        if i == 0:
            samples = step.sample([q0, q1], repetitions=10)
            for sample in samples:
                assert np.array_equal(sample, [True, False]) or np.array_equal(
                    sample, [False, False]
                )
        else:
            samples = step.sample([q0, q1], repetitions=10)
            for sample in samples:
                assert np.array_equal(sample, [True, True]) or np.array_equal(
                    sample, [False, False]
                )


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_moment_steps_intermediate_measurement(
    dtype: Type[np.complexfloating], split: bool
):
    q0 = alphaclops.LineQubit(0)
    circuit = alphaclops.Circuit(alphaclops.H(q0), alphaclops.measure(q0), alphaclops.H(q0))
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    for i, step in enumerate(simulator.simulate_moment_steps(circuit)):
        if i == 1:
            result = int(step.measurements['q(0)'][0])
            expected = np.zeros(2)
            expected[result] = 1
            np.testing.assert_almost_equal(step.state_vector(copy=True), expected)
        if i == 2:
            expected = np.array([np.sqrt(0.5), np.sqrt(0.5) * (-1) ** result])
            np.testing.assert_almost_equal(step.state_vector(copy=True), expected)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_expectation_values(dtype: Type[np.complexfloating], split: bool):
    # Compare with test_expectation_from_state_vector_two_qubit_states
    # in file: alphaclops/ops/linear_combinations_test.py
    q0, q1 = alphaclops.LineQubit.range(2)
    psum1 = alphaclops.Z(q0) + 3.2 * alphaclops.Z(q1)
    psum2 = -1 * alphaclops.X(q0) + 2 * alphaclops.X(q1)
    c1 = alphaclops.Circuit(alphaclops.I(q0), alphaclops.X(q1))
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    result = simulator.simulate_expectation_values(c1, [psum1, psum2])
    assert alphaclops.approx_eq(result[0], -2.2, atol=1e-6)
    assert alphaclops.approx_eq(result[1], 0, atol=1e-6)

    c2 = alphaclops.Circuit(alphaclops.H(q0), alphaclops.H(q1))
    result = simulator.simulate_expectation_values(c2, [psum1, psum2])
    assert alphaclops.approx_eq(result[0], 0, atol=1e-6)
    assert alphaclops.approx_eq(result[1], 1, atol=1e-6)

    psum3 = alphaclops.Z(q0) + alphaclops.X(q1)
    c3 = alphaclops.Circuit(alphaclops.I(q0), alphaclops.H(q1))
    result = simulator.simulate_expectation_values(c3, psum3)
    assert alphaclops.approx_eq(result[0], 2, atol=1e-6)


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_expectation_values_terminal_measure(dtype: Type[np.complexfloating], split: bool):
    q0 = alphaclops.LineQubit(0)
    circuit = alphaclops.Circuit(alphaclops.H(q0), alphaclops.measure(q0))
    obs = alphaclops.Z(q0)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)
    with pytest.raises(ValueError):
        _ = simulator.simulate_expectation_values(circuit, obs)

    results = {-1: 0, 1: 0}
    for _ in range(100):
        result = simulator.simulate_expectation_values(
            circuit, obs, permit_terminal_measurements=True
        )
        if alphaclops.approx_eq(result[0], -1, atol=1e-6):
            results[-1] += 1
        if alphaclops.approx_eq(result[0], 1, atol=1e-6):
            results[1] += 1

    # With a measurement after H, the Z-observable expects a specific state.
    assert results[-1] > 0
    assert results[1] > 0
    assert results[-1] + results[1] == 100

    circuit = alphaclops.Circuit(alphaclops.H(q0))
    results = {0: 0}
    for _ in range(100):
        result = simulator.simulate_expectation_values(
            circuit, obs, permit_terminal_measurements=True
        )
        if alphaclops.approx_eq(result[0], 0, atol=1e-6):
            results[0] += 1

    # Without measurement after H, the Z-observable is indeterminate.
    assert results[0] == 100


@pytest.mark.parametrize('dtype', [np.complex64, np.complex128])
@pytest.mark.parametrize('split', [True, False])
def test_simulate_expectation_values_qubit_order(dtype: Type[np.complexfloating], split: bool):
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(alphaclops.H(q0), alphaclops.H(q1), alphaclops.X(q2))
    obs = alphaclops.X(q0) + alphaclops.X(q1) - alphaclops.Z(q2)
    simulator = alphaclops.Simulator(dtype=dtype, split_untangled_states=split)

    result = simulator.simulate_expectation_values(circuit, obs)
    assert alphaclops.approx_eq(result[0], 3, atol=1e-6)

    # Adjusting the qubit order has no effect on the observables.
    result_flipped = simulator.simulate_expectation_values(circuit, obs, qubit_order=[q1, q2, q0])
    assert alphaclops.approx_eq(result_flipped[0], 3, atol=1e-6)


def test_invalid_run_no_unitary():
    class NoUnitary(alphaclops.testing.SingleQubitGate):
        pass

    q0 = alphaclops.LineQubit(0)
    simulator = alphaclops.Simulator()
    circuit = alphaclops.Circuit(NoUnitary()(q0))
    circuit.append([alphaclops.measure(q0, key='meas')])
    with pytest.raises(TypeError, match='unitary'):
        simulator.run(circuit)


def test_allocates_new_state():
    class NoUnitary(alphaclops.testing.SingleQubitGate):
        def _has_unitary_(self):
            return True

        def _apply_unitary_(self, args: alphaclops.ApplyUnitaryArgs):
            return np.copy(args.target_tensor)

    q0 = alphaclops.LineQubit(0)
    simulator = alphaclops.Simulator()
    circuit = alphaclops.Circuit(NoUnitary()(q0))

    initial_state = np.array([np.sqrt(0.5), np.sqrt(0.5)], dtype=np.complex64)
    result = simulator.simulate(circuit, initial_state=initial_state)
    np.testing.assert_array_almost_equal(result.state_vector(), initial_state)
    assert not initial_state is result.state_vector()


def test_does_not_modify_initial_state():
    q0 = alphaclops.LineQubit(0)
    simulator = alphaclops.Simulator()

    class InPlaceUnitary(alphaclops.testing.SingleQubitGate):
        def _has_unitary_(self):
            return True

        def _apply_unitary_(self, args: alphaclops.ApplyUnitaryArgs):
            args.target_tensor[0], args.target_tensor[1] = (
                args.target_tensor[1],
                args.target_tensor[0],
            )
            return args.target_tensor

    circuit = alphaclops.Circuit(InPlaceUnitary()(q0))

    initial_state = np.array([1, 0], dtype=np.complex64)
    result = simulator.simulate(circuit, initial_state=initial_state)
    np.testing.assert_array_almost_equal(np.array([1, 0], dtype=np.complex64), initial_state)
    np.testing.assert_array_almost_equal(
        result.state_vector(), np.array([0, 1], dtype=np.complex64)
    )


def test_simulator_step_state_mixin():
    qubits = alphaclops.LineQubit.range(2)
    args = alphaclops.StateVectorSimulationState(
        available_buffer=np.array([0, 1, 0, 0]).reshape((2, 2)),
        prng=alphaclops.value.parse_random_state(0),
        qubits=qubits,
        initial_state=np.array([0, 1, 0, 0], dtype=np.complex64).reshape((2, 2)),
        dtype=np.complex64,
    )
    result = alphaclops.SparseSimulatorStep(sim_state=args, dtype=np.complex64)
    rho = np.array([[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    np.testing.assert_array_almost_equal(rho, result.density_matrix_of(qubits))
    bloch = np.array([0, 0, -1])
    np.testing.assert_array_almost_equal(bloch, result.bloch_vector_of(qubits[1]))

    assert result.dirac_notation() == '|01⟩'


def test_sparse_simulator_repr():
    qubits = alphaclops.LineQubit.range(2)
    args = alphaclops.StateVectorSimulationState(
        available_buffer=np.array([0, 1, 0, 0]).reshape((2, 2)),
        prng=alphaclops.value.parse_random_state(0),
        qubits=qubits,
        initial_state=np.array([0, 1, 0, 0], dtype=np.complex64).reshape((2, 2)),
        dtype=np.complex64,
    )
    step = alphaclops.SparseSimulatorStep(sim_state=args, dtype=np.complex64)
    # No equality so cannot use alphaclops.testing.assert_equivalent_repr
    assert (
        repr(step) == "alphaclops.SparseSimulatorStep(sim_state=alphaclops.StateVectorSimulationState("
        "initial_state=np.array([[0j, (1+0j)], [0j, 0j]], dtype=np.dtype('complex64')), "
        "qubits=(alphaclops.LineQubit(0), alphaclops.LineQubit(1)), "
        "classical_data=alphaclops.ClassicalDataDictionaryStore()), dtype=np.dtype('complex64'))"
    )


class MultiHTestGate(alphaclops.testing.TwoQubitGate):
    def _decompose_(self, qubits):
        return alphaclops.H.on_each(*qubits)


def test_simulates_composite():
    c = alphaclops.Circuit(MultiHTestGate().on(*alphaclops.LineQubit.range(2)))
    expected = np.array([0.5] * 4)
    np.testing.assert_allclose(
        c.final_state_vector(ignore_terminal_measurements=False, dtype=np.complex64), expected
    )
    np.testing.assert_allclose(alphaclops.Simulator().simulate(c).state_vector(), expected)


def test_simulate_measurement_inversions():
    q = alphaclops.NamedQubit('q')

    c = alphaclops.Circuit(alphaclops.measure(q, key='q', invert_mask=(True,)))
    assert alphaclops.Simulator().simulate(c).measurements == {'q': np.array([True])}

    c = alphaclops.Circuit(alphaclops.measure(q, key='q', invert_mask=(False,)))
    assert alphaclops.Simulator().simulate(c).measurements == {'q': np.array([False])}


def test_works_on_pauli_string_phasor():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(np.exp(0.5j * np.pi * alphaclops.X(a) * alphaclops.X(b)))
    sim = alphaclops.Simulator()
    result = sim.simulate(c).state_vector()
    np.testing.assert_allclose(result.reshape(4), np.array([0, 0, 0, 1j]), atol=1e-8)


def test_works_on_pauli_string():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.X(a) * alphaclops.X(b))
    sim = alphaclops.Simulator()
    result = sim.simulate(c).state_vector()
    np.testing.assert_allclose(result.reshape(4), np.array([0, 0, 0, 1]), atol=1e-8)


def test_measure_at_end_invert_mask():
    simulator = alphaclops.Simulator()
    a = alphaclops.NamedQubit('a')
    circuit = alphaclops.Circuit(alphaclops.measure(a, key='a', invert_mask=(True,)))
    result = simulator.run(circuit, repetitions=4)
    np.testing.assert_equal(result.measurements['a'], np.array([[1]] * 4))


def test_measure_at_end_invert_mask_multiple_qubits():
    simulator = alphaclops.Simulator()
    a, b, c = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(
        alphaclops.measure(a, key='a', invert_mask=(True,)),
        alphaclops.measure(b, c, key='bc', invert_mask=(False, True)),
    )
    result = simulator.run(circuit, repetitions=4)
    np.testing.assert_equal(result.measurements['a'], np.array([[True]] * 4))
    np.testing.assert_equal(result.measurements['bc'], np.array([[0, 1]] * 4))


def test_measure_at_end_invert_mask_partial():
    simulator = alphaclops.Simulator()
    a, _, c = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(alphaclops.measure(a, c, key='ac', invert_mask=(True,)))
    result = simulator.run(circuit, repetitions=4)
    np.testing.assert_equal(result.measurements['ac'], np.array([[1, 0]] * 4))


def test_qudit_invert_mask():
    q0, q1, q2, q3, q4 = alphaclops.LineQid.for_qid_shape((2, 3, 3, 3, 4))
    c = alphaclops.Circuit(
        alphaclops.XPowGate(dimension=2)(q0),
        alphaclops.XPowGate(dimension=3)(q2),
        alphaclops.XPowGate(dimension=3)(q3) ** 2,
        alphaclops.XPowGate(dimension=4)(q4) ** 3,
        alphaclops.measure(q0, q1, q2, q3, q4, key='a', invert_mask=(True,) * 4),
    )
    assert np.all(alphaclops.Simulator().run(c).measurements['a'] == [[0, 1, 0, 2, 3]])


def test_compute_amplitudes():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.X(a), alphaclops.H(a), alphaclops.H(b))
    sim = alphaclops.Simulator()

    result = sim.compute_amplitudes(c, [0])
    np.testing.assert_allclose(np.array(result), np.array([0.5]))

    result = sim.compute_amplitudes(c, [1, 2, 3])
    np.testing.assert_allclose(np.array(result), np.array([0.5, -0.5, -0.5]))

    result = sim.compute_amplitudes(c, (1, 2, 3), qubit_order=(b, a))
    np.testing.assert_allclose(np.array(result), np.array([-0.5, 0.5, -0.5]))


def test_compute_amplitudes_bad_input():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.X(a), alphaclops.H(a), alphaclops.H(b))
    sim = alphaclops.Simulator()

    with pytest.raises(ValueError, match='1-dimensional'):
        _ = sim.compute_amplitudes(c, np.array([[0, 0]]))


def test_sample_from_amplitudes():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(alphaclops.H(q0), alphaclops.CNOT(q0, q1), alphaclops.X(q1))
    sim = alphaclops.Simulator(seed=1)
    result = sim.sample_from_amplitudes(circuit, {}, sim._prng, repetitions=100)
    assert 40 < result[1] < 60
    assert 40 < result[2] < 60
    assert 0 not in result
    assert 3 not in result


def test_sample_from_amplitudes_teleport():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    # Initialize q0 to some state, teleport it to q2, then clean up.
    circuit = alphaclops.Circuit(
        alphaclops.H(q1),
        alphaclops.CNOT(q1, q2),
        alphaclops.X(q0) ** sympy.Symbol('t'),
        alphaclops.CNOT(q0, q1),
        alphaclops.H(q0),
        alphaclops.CNOT(q1, q2),
        alphaclops.CZ(q0, q2),
        alphaclops.H(q0),
        alphaclops.H(q1),
    )
    sim = alphaclops.Simulator(seed=1)

    # Full X, always produces |1) state
    result_a = sim.sample_from_amplitudes(circuit, {'t': 1}, sim._prng, repetitions=100)
    assert result_a == {1: 100}

    # sqrt of X, produces 50:50 state
    result_b = sim.sample_from_amplitudes(circuit, {'t': 0.5}, sim._prng, repetitions=100)
    assert 40 < result_b[0] < 60
    assert 40 < result_b[1] < 60

    # X^(1/4), produces ~85:15 state
    result_c = sim.sample_from_amplitudes(circuit, {'t': 0.25}, sim._prng, repetitions=100)
    assert 80 < result_c[0]
    assert result_c[1] < 20


def test_sample_from_amplitudes_nonunitary_fails():
    q0, q1 = alphaclops.LineQubit.range(2)
    sim = alphaclops.Simulator(seed=1)

    circuit1 = alphaclops.Circuit(alphaclops.H(q0), alphaclops.measure(q0, key='m'))
    with pytest.raises(ValueError, match='does not support intermediate measurement'):
        _ = sim.sample_from_amplitudes(circuit1, {}, sim._prng)

    circuit2 = alphaclops.Circuit(
        alphaclops.H(q0), alphaclops.CNOT(q0, q1), alphaclops.amplitude_damp(0.01)(q0), alphaclops.amplitude_damp(0.01)(q1)
    )
    with pytest.raises(ValueError, match='does not support non-unitary'):
        _ = sim.sample_from_amplitudes(circuit2, {}, sim._prng)


def test_run_sweep_parameters_not_resolved():
    a = alphaclops.LineQubit(0)
    simulator = alphaclops.Simulator()
    circuit = alphaclops.Circuit(alphaclops.XPowGate(exponent=sympy.Symbol('a'))(a), alphaclops.measure(a))
    with pytest.raises(ValueError, match='symbols were not specified'):
        _ = simulator.run_sweep(circuit, alphaclops.ParamResolver({}))


def test_simulate_sweep_parameters_not_resolved():
    a = alphaclops.LineQubit(0)
    simulator = alphaclops.Simulator()
    circuit = alphaclops.Circuit(alphaclops.XPowGate(exponent=sympy.Symbol('a'))(a), alphaclops.measure(a))
    with pytest.raises(ValueError, match='symbols were not specified'):
        _ = simulator.simulate_sweep(circuit, alphaclops.ParamResolver({}))


def test_random_seed():
    a = alphaclops.NamedQubit('a')
    circuit = alphaclops.Circuit(alphaclops.X(a) ** 0.5, alphaclops.measure(a))

    sim = alphaclops.Simulator(seed=1234)
    result = sim.run(circuit, repetitions=10)
    assert np.all(
        result.measurements['a']
        == [[False], [True], [False], [True], [True], [False], [False], [True], [True], [True]]
    )

    sim = alphaclops.Simulator(seed=np.random.RandomState(1234))
    result = sim.run(circuit, repetitions=10)
    assert np.all(
        result.measurements['a']
        == [[False], [True], [False], [True], [True], [False], [False], [True], [True], [True]]
    )


def test_random_seed_does_not_modify_global_state_terminal_measurements():
    a = alphaclops.NamedQubit('a')
    circuit = alphaclops.Circuit(alphaclops.X(a) ** 0.5, alphaclops.measure(a))

    sim = alphaclops.Simulator(seed=1234)
    result1 = sim.run(circuit, repetitions=50)

    sim = alphaclops.Simulator(seed=1234)
    _ = np.random.random()
    _ = random.random()
    result2 = sim.run(circuit, repetitions=50)

    assert result1 == result2


def test_random_seed_does_not_modify_global_state_non_terminal_measurements():
    a = alphaclops.NamedQubit('a')
    circuit = alphaclops.Circuit(
        alphaclops.X(a) ** 0.5, alphaclops.measure(a, key='a0'), alphaclops.X(a) ** 0.5, alphaclops.measure(a, key='a1')
    )

    sim = alphaclops.Simulator(seed=1234)
    result1 = sim.run(circuit, repetitions=50)

    sim = alphaclops.Simulator(seed=1234)
    _ = np.random.random()
    _ = random.random()
    result2 = sim.run(circuit, repetitions=50)

    assert result1 == result2


def test_random_seed_does_not_modify_global_state_mixture():
    a = alphaclops.NamedQubit('a')
    circuit = alphaclops.Circuit(alphaclops.depolarize(0.5).on(a), alphaclops.measure(a))

    sim = alphaclops.Simulator(seed=1234)
    result1 = sim.run(circuit, repetitions=50)

    sim = alphaclops.Simulator(seed=1234)
    _ = np.random.random()
    _ = random.random()
    result2 = sim.run(circuit, repetitions=50)

    assert result1 == result2


def test_random_seed_terminal_measurements_deterministic():
    a = alphaclops.NamedQubit('a')
    circuit = alphaclops.Circuit(alphaclops.X(a) ** 0.5, alphaclops.measure(a, key='a'))
    sim = alphaclops.Simulator(seed=1234)
    result1 = sim.run(circuit, repetitions=30)
    result2 = sim.run(circuit, repetitions=30)
    assert np.all(
        result1.measurements['a']
        == [
            [0],
            [1],
            [0],
            [1],
            [1],
            [0],
            [0],
            [1],
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
            [0],
            [0],
            [1],
            [1],
            [0],
            [1],
            [0],
            [1],
        ]
    )
    assert np.all(
        result2.measurements['a']
        == [
            [1],
            [0],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
            [0],
            [1],
            [0],
            [0],
            [0],
            [1],
            [1],
            [1],
            [0],
            [1],
            [0],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
        ]
    )


def test_random_seed_non_terminal_measurements_deterministic():
    a = alphaclops.NamedQubit('a')
    circuit = alphaclops.Circuit(
        alphaclops.X(a) ** 0.5, alphaclops.measure(a, key='a'), alphaclops.X(a) ** 0.5, alphaclops.measure(a, key='b')
    )
    sim = alphaclops.Simulator(seed=1234)
    result = sim.run(circuit, repetitions=30)
    assert np.all(
        result.measurements['a']
        == [
            [0],
            [0],
            [1],
            [0],
            [1],
            [0],
            [1],
            [0],
            [1],
            [1],
            [0],
            [0],
            [1],
            [0],
            [0],
            [1],
            [1],
            [1],
            [0],
            [0],
            [0],
            [0],
            [1],
            [0],
            [0],
            [0],
            [1],
            [1],
            [1],
            [1],
        ]
    )
    assert np.all(
        result.measurements['b']
        == [
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
            [0],
            [0],
            [1],
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
        ]
    )


def test_random_seed_mixture_deterministic():
    a = alphaclops.NamedQubit('a')
    circuit = alphaclops.Circuit(
        alphaclops.depolarize(0.9).on(a),
        alphaclops.depolarize(0.9).on(a),
        alphaclops.depolarize(0.9).on(a),
        alphaclops.depolarize(0.9).on(a),
        alphaclops.depolarize(0.9).on(a),
        alphaclops.measure(a, key='a'),
    )
    sim = alphaclops.Simulator(seed=1234)
    result = sim.run(circuit, repetitions=30)
    assert np.all(
        result.measurements['a']
        == [
            [1],
            [0],
            [0],
            [0],
            [1],
            [0],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
            [0],
            [1],
            [0],
            [0],
            [0],
            [0],
            [0],
            [1],
            [0],
            [1],
            [1],
            [0],
            [1],
            [1],
            [1],
            [1],
            [1],
            [0],
        ]
    )


def test_entangled_reset_does_not_break_randomness():
    """Test for bad assumptions on caching the wave function on general channels.

    A previous version of alphaclops made the mistake of assuming that it was okay to
    cache the wavefunction produced by general channels on unrelated qubits
    before repeatedly sampling measurements. This test checks for that mistake.
    """

    a, b = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.H(a), alphaclops.CNOT(a, b), alphaclops.ResetChannel().on(a), alphaclops.measure(b, key='out')
    )
    samples = alphaclops.Simulator().sample(circuit, repetitions=100)['out']
    counts = samples.value_counts()
    assert len(counts) == 2
    assert 10 <= counts[0] <= 90
    assert 10 <= counts[1] <= 90


def test_overlapping_measurements_at_end():
    a, b = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.H(a),
        alphaclops.CNOT(a, b),
        # These measurements are not on independent qubits but they commute.
        alphaclops.measure(a, key='a'),
        alphaclops.measure(a, key='not a', invert_mask=(True,)),
        alphaclops.measure(b, key='b'),
        alphaclops.measure(a, b, key='ab'),
    )

    samples = alphaclops.Simulator().sample(circuit, repetitions=100)
    np.testing.assert_array_equal(samples['a'].values, samples['not a'].values ^ 1)
    np.testing.assert_array_equal(
        samples['a'].values * 2 + samples['b'].values, samples['ab'].values
    )

    counts = samples['b'].value_counts()
    assert len(counts) == 2
    assert 10 <= counts[0] <= 90
    assert 10 <= counts[1] <= 90


def test_separated_measurements():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(
        [
            alphaclops.H(a),
            alphaclops.H(b),
            alphaclops.CZ(a, b),
            alphaclops.measure(a, key='a'),
            alphaclops.CZ(a, b),
            alphaclops.H(b),
            alphaclops.measure(b, key='zero'),
        ]
    )
    sample = alphaclops.Simulator().sample(c, repetitions=10)
    np.testing.assert_array_equal(sample['zero'].values, [0] * 10)


def test_state_vector_copy():
    sim = alphaclops.Simulator(split_untangled_states=False)

    class InplaceGate(alphaclops.testing.SingleQubitGate):
        """A gate that modifies the target tensor in place, multiply by -1."""

        def _apply_unitary_(self, args):
            args.target_tensor *= -1.0
            return args.target_tensor

    q = alphaclops.LineQubit(0)
    circuit = alphaclops.Circuit(InplaceGate()(q), InplaceGate()(q))

    vectors = []
    for step in sim.simulate_moment_steps(circuit):
        vectors.append(step.state_vector(copy=True))
    for x, y in itertools.combinations(vectors, 2):
        assert not np.shares_memory(x, y)

    # If the state vector is not copied, then applying second InplaceGate
    # causes old state to be modified.
    vectors = []
    copy_of_vectors = []
    for step in sim.simulate_moment_steps(circuit):
        state_vector = step.state_vector()
        vectors.append(state_vector)
        copy_of_vectors.append(state_vector.copy())
    assert any(not np.array_equal(x, y) for x, y in zip(vectors, copy_of_vectors))


def test_final_state_vector_is_not_last_object():
    sim = alphaclops.Simulator()

    q = alphaclops.LineQubit(0)
    initial_state = np.array([1, 0], dtype=np.complex64)
    circuit = alphaclops.Circuit(alphaclops.wait(q))
    result = sim.simulate(circuit, initial_state=initial_state)
    assert result.state_vector() is not initial_state
    assert not np.shares_memory(result.state_vector(), initial_state)
    np.testing.assert_equal(result.state_vector(), initial_state)


def test_deterministic_gate_noise():
    q = alphaclops.LineQubit(0)
    circuit = alphaclops.Circuit(alphaclops.I(q), alphaclops.measure(q))

    simulator1 = alphaclops.Simulator(noise=alphaclops.X)
    result1 = simulator1.run(circuit, repetitions=10)

    simulator2 = alphaclops.Simulator(noise=alphaclops.X)
    result2 = simulator2.run(circuit, repetitions=10)

    assert result1 == result2

    simulator3 = alphaclops.Simulator(noise=alphaclops.Z)
    result3 = simulator3.run(circuit, repetitions=10)

    assert result1 != result3


def test_nondeterministic_mixture_noise():
    q = alphaclops.LineQubit(0)
    circuit = alphaclops.Circuit(alphaclops.I(q), alphaclops.measure(q))

    simulator = alphaclops.Simulator(noise=alphaclops.ConstantQubitNoiseModel(alphaclops.depolarize(0.5)))
    result1 = simulator.run(circuit, repetitions=50)
    result2 = simulator.run(circuit, repetitions=50)

    assert result1 != result2


def test_pure_state_creation():
    sim = alphaclops.Simulator()
    qids = alphaclops.LineQubit.range(3)
    shape = alphaclops.qid_shape(qids)
    args = sim._create_simulation_state(1, qids)
    values = list(args.values())
    arg = (
        values[0]
        .kronecker_product(values[1])
        .kronecker_product(values[2])
        .transpose_to_qubit_order(qids)
    )
    expected = alphaclops.to_valid_state_vector(1, len(qids), qid_shape=shape)
    np.testing.assert_allclose(arg.target_tensor, expected.reshape(shape))


def test_noise_model():
    q = alphaclops.LineQubit(0)
    circuit = alphaclops.Circuit(alphaclops.H(q), alphaclops.measure(q))

    noise_model = alphaclops.NoiseModel.from_noise_model_like(alphaclops.depolarize(p=0.01))
    simulator = alphaclops.Simulator(noise=noise_model)
    result = simulator.run(circuit, repetitions=100)

    assert 20 <= sum(result.measurements['q(0)'])[0] < 80


def test_separated_states_str_does_not_merge():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0), alphaclops.measure(q1), alphaclops.H(q0), alphaclops.global_phase_operation(0 + 1j)
    )

    result = alphaclops.Simulator().simulate(circuit)
    assert (
        str(result)
        == """measurements: q(0)=0 q(1)=0

qubits: (alphaclops.LineQubit(0),)
output vector: 0.707|0⟩ + 0.707|1⟩

qubits: (alphaclops.LineQubit(1),)
output vector: |0⟩

phase:
output vector: 1j|⟩"""
    )


def test_separable_non_dirac_str():
    circuit = alphaclops.Circuit()
    for i in range(4):
        circuit.append(alphaclops.H(alphaclops.LineQubit(i)))
        circuit.append(alphaclops.CX(alphaclops.LineQubit(0), alphaclops.LineQubit(i + 1)))

    result = alphaclops.Simulator().simulate(circuit)
    assert '+0.j' in str(result)


def test_unseparated_states_str():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0), alphaclops.measure(q1), alphaclops.H(q0), alphaclops.global_phase_operation(0 + 1j)
    )

    result = alphaclops.Simulator(split_untangled_states=False).simulate(circuit)
    assert (
        str(result)
        == """measurements: q(0)=0 q(1)=0

qubits: (alphaclops.LineQubit(0), alphaclops.LineQubit(1))
output vector: 0.707j|00⟩ + 0.707j|10⟩"""
    )


@pytest.mark.parametrize('split', [True, False])
def test_measurement_preserves_phase(split: bool):
    c1, c2, t = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(
        alphaclops.H(t),
        alphaclops.measure(t, key='t'),
        alphaclops.CZ(c1, c2).with_classical_controls('t'),
        alphaclops.reset(t),
    )
    simulator = alphaclops.Simulator(split_untangled_states=split)
    # Run enough times that both options of |110> - |111> are likely measured.
    for _ in range(20):
        result = simulator.simulate(circuit, initial_state=(1, 1, 1), qubit_order=(c1, c2, t))
        assert result.dirac_notation() == '|110⟩'
