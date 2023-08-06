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

"""Tests sampling/simulation methods that delegate to appropriate simulators."""
import collections

import numpy as np
import pytest
import sympy

import alphaclops
import alphaclops.testing


def test_sample():
    q = alphaclops.NamedQubit('q')

    with pytest.raises(ValueError, match="no measurements"):
        alphaclops.sample(alphaclops.Circuit(alphaclops.X(q)))
    # Unitary.
    results = alphaclops.sample(alphaclops.Circuit(alphaclops.X(q), alphaclops.measure(q)))
    assert results.histogram(key=q) == collections.Counter({1: 1})

    # Intermediate measurements.
    results = alphaclops.sample(alphaclops.Circuit(alphaclops.measure(q, key='drop'), alphaclops.X(q), alphaclops.measure(q)))
    assert results.histogram(key='drop') == collections.Counter({0: 1})
    assert results.histogram(key=q) == collections.Counter({1: 1})

    # Overdamped everywhere.
    results = alphaclops.sample(
        alphaclops.Circuit(alphaclops.measure(q, key='drop'), alphaclops.X(q), alphaclops.measure(q)),
        noise=alphaclops.ConstantQubitNoiseModel(alphaclops.amplitude_damp(1)),
    )
    assert results.histogram(key='drop') == collections.Counter({0: 1})
    assert results.histogram(key=q) == collections.Counter({0: 1})


def test_sample_seed_unitary():
    q = alphaclops.NamedQubit('q')
    circuit = alphaclops.Circuit(alphaclops.X(q) ** 0.2, alphaclops.measure(q))
    result = alphaclops.sample(circuit, repetitions=10, seed=1234)
    measurements = result.measurements['q']
    assert np.all(
        measurements
        == [[False], [False], [False], [False], [False], [False], [False], [False], [True], [False]]
    )


def test_sample_seed_non_unitary():
    q = alphaclops.NamedQubit('q')
    circuit = alphaclops.Circuit(alphaclops.depolarize(0.5).on(q), alphaclops.measure(q))
    result = alphaclops.sample(circuit, repetitions=10, seed=1234)
    assert np.all(
        result.measurements['q']
        == [[False], [False], [False], [True], [True], [False], [False], [True], [True], [True]]
    )


def test_sample_sweep():
    q = alphaclops.NamedQubit('q')
    c = alphaclops.Circuit(alphaclops.X(q), alphaclops.Y(q) ** sympy.Symbol('t'), alphaclops.measure(q))

    # Unitary.
    results = alphaclops.sample_sweep(c, alphaclops.Linspace('t', 0, 1, 2), repetitions=3)
    assert len(results) == 2
    assert results[0].histogram(key=q) == collections.Counter({1: 3})
    assert results[1].histogram(key=q) == collections.Counter({0: 3})

    # Overdamped.
    c = alphaclops.Circuit(
        alphaclops.X(q), alphaclops.amplitude_damp(1).on(q), alphaclops.Y(q) ** sympy.Symbol('t'), alphaclops.measure(q)
    )
    results = alphaclops.sample_sweep(c, alphaclops.Linspace('t', 0, 1, 2), repetitions=3)
    assert len(results) == 2
    assert results[0].histogram(key=q) == collections.Counter({0: 3})
    assert results[1].histogram(key=q) == collections.Counter({1: 3})

    # Overdamped everywhere.
    c = alphaclops.Circuit(alphaclops.X(q), alphaclops.Y(q) ** sympy.Symbol('t'), alphaclops.measure(q))
    results = alphaclops.sample_sweep(
        c,
        alphaclops.Linspace('t', 0, 1, 2),
        noise=alphaclops.ConstantQubitNoiseModel(alphaclops.amplitude_damp(1)),
        repetitions=3,
    )
    assert len(results) == 2
    assert results[0].histogram(key=q) == collections.Counter({0: 3})
    assert results[1].histogram(key=q) == collections.Counter({0: 3})


def test_sample_sweep_seed():
    q = alphaclops.NamedQubit('q')
    circuit = alphaclops.Circuit(alphaclops.X(q) ** sympy.Symbol('t'), alphaclops.measure(q))

    results = alphaclops.sample_sweep(
        circuit, [alphaclops.ParamResolver({'t': 0.5})] * 3, repetitions=2, seed=1234
    )
    assert np.all(results[0].measurements['q'] == [[False], [True]])
    assert np.all(results[1].measurements['q'] == [[False], [True]])
    assert np.all(results[2].measurements['q'] == [[True], [False]])

    results = alphaclops.sample_sweep(
        circuit,
        [alphaclops.ParamResolver({'t': 0.5})] * 3,
        repetitions=2,
        seed=np.random.RandomState(1234),
    )
    assert np.all(results[0].measurements['q'] == [[False], [True]])
    assert np.all(results[1].measurements['q'] == [[False], [True]])
    assert np.all(results[2].measurements['q'] == [[True], [False]])


def test_final_state_vector_different_program_types():
    a, b = alphaclops.LineQubit.range(2)

    np.testing.assert_allclose(alphaclops.final_state_vector(alphaclops.X), [0, 1], atol=1e-8)

    ops = [alphaclops.H(a), alphaclops.CNOT(a, b)]

    np.testing.assert_allclose(
        alphaclops.final_state_vector(ops), [np.sqrt(0.5), 0, 0, np.sqrt(0.5)], atol=1e-8
    )

    np.testing.assert_allclose(
        alphaclops.final_state_vector(alphaclops.Circuit(ops)), [np.sqrt(0.5), 0, 0, np.sqrt(0.5)], atol=1e-8
    )


def test_final_state_vector_initial_state():
    np.testing.assert_allclose(alphaclops.final_state_vector(alphaclops.X, initial_state=0), [0, 1], atol=1e-8)

    np.testing.assert_allclose(alphaclops.final_state_vector(alphaclops.X, initial_state=1), [1, 0], atol=1e-8)

    np.testing.assert_allclose(
        alphaclops.final_state_vector(alphaclops.X, initial_state=[np.sqrt(0.5), 1j * np.sqrt(0.5)]),
        [1j * np.sqrt(0.5), np.sqrt(0.5)],
        atol=1e-8,
    )


def test_final_state_vector_dtype_insensitive_to_initial_state():
    assert alphaclops.final_state_vector(alphaclops.X).dtype == np.complex64

    assert alphaclops.final_state_vector(alphaclops.X, initial_state=0).dtype == np.complex64

    assert (
            alphaclops.final_state_vector(alphaclops.X, initial_state=[np.sqrt(0.5), np.sqrt(0.5)]).dtype
            == np.complex64
    )

    assert (
            alphaclops.final_state_vector(alphaclops.X, initial_state=np.array([np.sqrt(0.5), np.sqrt(0.5)])).dtype
            == np.complex64
    )

    for t in [np.int32, np.float32, np.float64, np.complex64]:
        assert (
                alphaclops.final_state_vector(alphaclops.X, initial_state=np.array([1, 0], dtype=t)).dtype
                == np.complex64
        )

        assert (
                alphaclops.final_state_vector(
                alphaclops.X, initial_state=np.array([1, 0], dtype=t), dtype=np.complex128
            ).dtype
                == np.complex128
        )


def test_final_state_vector_param_resolver():
    s = sympy.Symbol('s')

    with pytest.raises(ValueError, match='not unitary'):
        _ = alphaclops.final_state_vector(alphaclops.X ** s)

    np.testing.assert_allclose(
        alphaclops.final_state_vector(alphaclops.X ** s, param_resolver={s: 0.5}), [0.5 + 0.5j, 0.5 - 0.5j]
    )


def test_final_state_vector_qubit_order():
    a, b = alphaclops.LineQubit.range(2)

    np.testing.assert_allclose(
        alphaclops.final_state_vector([alphaclops.X(a), alphaclops.X(b) ** 0.5], qubit_order=[a, b]),
        [0, 0, 0.5 + 0.5j, 0.5 - 0.5j],
    )

    np.testing.assert_allclose(
        alphaclops.final_state_vector([alphaclops.X(a), alphaclops.X(b) ** 0.5], qubit_order=[b, a]),
        [0, 0.5 + 0.5j, 0, 0.5 - 0.5j],
    )


def test_final_state_vector_ignore_terminal_measurement():
    a, b = alphaclops.LineQubit.range(2)

    np.testing.assert_allclose(
        alphaclops.final_state_vector(
            [alphaclops.X(a), alphaclops.X(b) ** 0.5, alphaclops.measure(a, b, key='m')],
            ignore_terminal_measurements=True,
        ),
        [0, 0, 0.5 + 0.5j, 0.5 - 0.5j],
    )
    with pytest.raises(ValueError, match='is not unitary'):
        _ = (
            alphaclops.final_state_vector(
                [alphaclops.X(a), alphaclops.amplitude_damp(0.1).on(b), alphaclops.measure(a, b, key='m')],
                ignore_terminal_measurements=True,
            ),
        )


@pytest.mark.parametrize('repetitions', (0, 1, 100))
def test_repetitions(repetitions):
    a = alphaclops.LineQubit(0)
    c = alphaclops.Circuit(alphaclops.H(a), alphaclops.measure(a, key='m'))
    r = alphaclops.sample(c, repetitions=repetitions)
    samples = r.data['m'].to_numpy()
    assert samples.shape == (repetitions,)
    assert np.issubdtype(samples.dtype, np.integer)


def test_final_density_matrix_different_program_types():
    a, b = alphaclops.LineQubit.range(2)

    np.testing.assert_allclose(alphaclops.final_density_matrix(alphaclops.X), [[0, 0], [0, 1]], atol=1e-8)

    ops = [alphaclops.H(a), alphaclops.CNOT(a, b)]

    np.testing.assert_allclose(
        alphaclops.final_density_matrix(alphaclops.Circuit(ops)),
        [[0.5, 0, 0, 0.5], [0, 0, 0, 0], [0, 0, 0, 0], [0.5, 0, 0, 0.5]],
        atol=1e-8,
    )


def test_final_density_matrix_initial_state():
    np.testing.assert_allclose(
        alphaclops.final_density_matrix(alphaclops.X, initial_state=0), [[0, 0], [0, 1]], atol=1e-8
    )

    np.testing.assert_allclose(
        alphaclops.final_density_matrix(alphaclops.X, initial_state=1), [[1, 0], [0, 0]], atol=1e-8
    )

    np.testing.assert_allclose(
        alphaclops.final_density_matrix(alphaclops.X, initial_state=[np.sqrt(0.5), 1j * np.sqrt(0.5)]),
        [[0.5, 0.5j], [-0.5j, 0.5]],
        atol=1e-8,
    )


def test_final_density_matrix_dtype_insensitive_to_initial_state():
    assert alphaclops.final_density_matrix(alphaclops.X).dtype == np.complex64

    assert alphaclops.final_density_matrix(alphaclops.X, initial_state=0).dtype == np.complex64

    assert (
            alphaclops.final_density_matrix(alphaclops.X, initial_state=[np.sqrt(0.5), np.sqrt(0.5)]).dtype
            == np.complex64
    )

    assert (
            alphaclops.final_density_matrix(
            alphaclops.X, initial_state=np.array([np.sqrt(0.5), np.sqrt(0.5)])
        ).dtype
            == np.complex64
    )

    for t in [np.int32, np.float32, np.float64, np.complex64]:
        assert (
                alphaclops.final_density_matrix(alphaclops.X, initial_state=np.array([1, 0], dtype=t)).dtype
                == np.complex64
        )

        assert (
                alphaclops.final_density_matrix(
                alphaclops.X, initial_state=np.array([1, 0], dtype=t), dtype=np.complex128
            ).dtype
                == np.complex128
        )


def test_final_density_matrix_param_resolver():
    s = sympy.Symbol('s')

    with pytest.raises(ValueError, match='not specified in parameter sweep'):
        _ = alphaclops.final_density_matrix(alphaclops.X ** s)

    np.testing.assert_allclose(
        alphaclops.final_density_matrix(alphaclops.X ** s, param_resolver={s: 0.5}),
        [[0.5 - 0.0j, 0.0 + 0.5j], [0.0 - 0.5j, 0.5 - 0.0j]],
    )


def test_final_density_matrix_qubit_order():
    a, b = alphaclops.LineQubit.range(2)

    np.testing.assert_allclose(
        alphaclops.final_density_matrix([alphaclops.X(a), alphaclops.X(b) ** 0.5], qubit_order=[a, b]),
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0.5, 0.5j], [0, 0, -0.5j, 0.5]],
    )

    np.testing.assert_allclose(
        alphaclops.final_density_matrix([alphaclops.X(a), alphaclops.X(b) ** 0.5], qubit_order=[b, a]),
        [[0, 0, 0, 0], [0, 0.5, 0, 0.5j], [0, 0, 0, 0], [0, -0.5j, 0, 0.5]],
    )

    np.testing.assert_allclose(
        alphaclops.final_density_matrix(
            [alphaclops.X(a), alphaclops.X(b) ** 0.5],
            qubit_order=[b, a],
            noise=alphaclops.ConstantQubitNoiseModel(alphaclops.amplitude_damp(1.0)),
        ),
        [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    )


def test_final_density_matrix_seed_with_dephasing():
    a = alphaclops.LineQubit(0)
    np.testing.assert_allclose(
        alphaclops.final_density_matrix([alphaclops.X(a) ** 0.5, alphaclops.measure(a)], seed=123),
        [[0.5 + 0.0j, 0.0 + 0.0j], [0.0 + 0.0j, 0.5 + 0.0j]],
        atol=1e-4,
    )
    np.testing.assert_allclose(
        alphaclops.final_density_matrix([alphaclops.X(a) ** 0.5, alphaclops.measure(a)], seed=124),
        [[0.5 + 0.0j, 0.0 + 0.0j], [0.0 + 0.0j, 0.5 + 0.0j]],
        atol=1e-4,
    )


def test_final_density_matrix_seed_with_collapsing():
    a = alphaclops.LineQubit(0)
    np.testing.assert_allclose(
        alphaclops.final_density_matrix(
            [alphaclops.X(a) ** 0.5, alphaclops.measure(a)], seed=123, ignore_measurement_results=False
        ),
        [[0, 0], [0, 1]],
        atol=1e-4,
    )
    np.testing.assert_allclose(
        alphaclops.final_density_matrix(
            [alphaclops.X(a) ** 0.5, alphaclops.measure(a)], seed=124, ignore_measurement_results=False
        ),
        [[1, 0], [0, 0]],
        atol=1e-4,
    )


def test_final_density_matrix_noise():
    a = alphaclops.LineQubit(0)
    np.testing.assert_allclose(
        alphaclops.final_density_matrix([alphaclops.H(a), alphaclops.Z(a), alphaclops.H(a), alphaclops.measure(a)]),
        [[0, 0], [0, 1]],
        atol=1e-4,
    )
    np.testing.assert_allclose(
        alphaclops.final_density_matrix(
            [alphaclops.H(a), alphaclops.Z(a), alphaclops.H(a), alphaclops.measure(a)],
            noise=alphaclops.ConstantQubitNoiseModel(alphaclops.amplitude_damp(1.0)),
        ),
        [[1, 0], [0, 0]],
        atol=1e-4,
    )


def test_ps_initial_state_wfn():
    q0, q1 = alphaclops.LineQubit.range(2)
    s00 = alphaclops.KET_ZERO(q0) * alphaclops.KET_ZERO(q1)
    sp0 = alphaclops.KET_PLUS(q0) * alphaclops.KET_ZERO(q1)

    np.testing.assert_allclose(
        alphaclops.final_state_vector(alphaclops.Circuit(alphaclops.I.on_each(q0, q1))),
        alphaclops.final_state_vector(alphaclops.Circuit(alphaclops.I.on_each(q0, q1)), initial_state=s00),
    )

    np.testing.assert_allclose(
        alphaclops.final_state_vector(alphaclops.Circuit(alphaclops.H(q0), alphaclops.I(q1))),
        alphaclops.final_state_vector(alphaclops.Circuit(alphaclops.I.on_each(q0, q1)), initial_state=sp0),
    )


def test_ps_initial_state_dmat():
    q0, q1 = alphaclops.LineQubit.range(2)
    s00 = alphaclops.KET_ZERO(q0) * alphaclops.KET_ZERO(q1)
    sp0 = alphaclops.KET_PLUS(q0) * alphaclops.KET_ZERO(q1)

    np.testing.assert_allclose(
        alphaclops.final_density_matrix(alphaclops.Circuit(alphaclops.I.on_each(q0, q1))),
        alphaclops.final_density_matrix(alphaclops.Circuit(alphaclops.I.on_each(q0, q1)), initial_state=s00),
    )

    np.testing.assert_allclose(
        alphaclops.final_density_matrix(alphaclops.Circuit(alphaclops.H(q0), alphaclops.I(q1))),
        alphaclops.final_density_matrix(alphaclops.Circuit(alphaclops.I.on_each(q0, q1)), initial_state=sp0),
    )
