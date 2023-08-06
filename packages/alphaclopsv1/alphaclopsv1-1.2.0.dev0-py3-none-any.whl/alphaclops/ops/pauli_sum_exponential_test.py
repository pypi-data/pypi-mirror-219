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

import numpy as np
import pytest

import sympy

import alphaclops
import alphaclops.testing

q0, q1, q2, q3 = alphaclops.LineQubit.range(4)


def test_raises_for_non_commuting_paulis():
    with pytest.raises(ValueError, match='commuting'):
        alphaclops.PauliSumExponential(alphaclops.X(q0) + alphaclops.Z(q0), np.pi / 2)


def test_raises_for_non_hermitian_pauli():
    with pytest.raises(ValueError, match='hermitian'):
        alphaclops.PauliSumExponential(alphaclops.X(q0) + 1j * alphaclops.Z(q1), np.pi / 2)


@pytest.mark.parametrize(
    'psum_exp, expected_qubits',
    (
        (alphaclops.PauliSumExponential(alphaclops.Z(q1), np.pi / 2), (q1,)),
        (
                alphaclops.PauliSumExponential(2j * alphaclops.X(q0) + 3j * alphaclops.Y(q2), sympy.Symbol("theta")),
                (q0, q2),
        ),
        (
                alphaclops.PauliSumExponential(alphaclops.X(q0) * alphaclops.Y(q1) + alphaclops.Y(q2) * alphaclops.Z(q3), np.pi),
                (q0, q1, q2, q3),
        ),
    ),
)
def test_pauli_sum_exponential_qubits(psum_exp, expected_qubits):
    assert psum_exp.qubits == expected_qubits


@pytest.mark.parametrize(
    'psum_exp, expected_psum_exp',
    (
        (
                alphaclops.PauliSumExponential(alphaclops.Z(q0), np.pi / 2),
                alphaclops.PauliSumExponential(alphaclops.Z(q1), np.pi / 2),
        ),
        (
                alphaclops.PauliSumExponential(2j * alphaclops.X(q0) + 3j * alphaclops.Y(q2), sympy.Symbol("theta")),
                alphaclops.PauliSumExponential(2j * alphaclops.X(q1) + 3j * alphaclops.Y(q3), sympy.Symbol("theta")),
        ),
        (
                alphaclops.PauliSumExponential(alphaclops.X(q0) * alphaclops.Y(q1) + alphaclops.Y(q1) * alphaclops.Z(q3), np.pi),
                alphaclops.PauliSumExponential(alphaclops.X(q1) * alphaclops.Y(q2) + alphaclops.Y(q2) * alphaclops.Z(q3), np.pi),
        ),
    ),
)
def test_pauli_sum_exponential_with_qubits(psum_exp, expected_psum_exp):
    assert psum_exp.with_qubits(*expected_psum_exp.qubits) == expected_psum_exp


@pytest.mark.parametrize(
    'psum, exp',
    (
        (alphaclops.Z(q0), np.pi / 2),
        (2 * alphaclops.X(q0) + 3 * alphaclops.Y(q2), 1),
        (alphaclops.X(q0) * alphaclops.Y(q1) + alphaclops.Y(q1) * alphaclops.Z(q3), np.pi),
    ),
)
def test_with_parameters_resolved_by(psum, exp):
    psum_exp = alphaclops.PauliSumExponential(psum, sympy.Symbol("theta"))
    resolver = alphaclops.ParamResolver({"theta": exp})
    actual = alphaclops.resolve_parameters(psum_exp, resolver)
    expected = alphaclops.PauliSumExponential(psum, exp)
    assert actual == expected


def test_pauli_sum_exponential_parameterized_matrix_raises():
    with pytest.raises(ValueError, match='parameterized'):
        alphaclops.PauliSumExponential(alphaclops.X(q0) + alphaclops.Z(q1), sympy.Symbol("theta")).matrix()


@pytest.mark.parametrize(
    'psum_exp, expected_unitary',
    (
        (alphaclops.PauliSumExponential(alphaclops.X(q0), np.pi / 2), np.array([[0, 1j], [1j, 0]])),
        (
                alphaclops.PauliSumExponential(2j * alphaclops.X(q0) + 3j * alphaclops.Z(q1), np.pi / 2),
                np.array([[1j, 0, 0, 0], [0, -1j, 0, 0], [0, 0, 1j, 0], [0, 0, 0, -1j]]),
        ),
    ),
)
def test_pauli_sum_exponential_has_correct_unitary(psum_exp, expected_unitary):
    assert alphaclops.has_unitary(psum_exp)
    assert np.allclose(alphaclops.unitary(psum_exp), expected_unitary)


@pytest.mark.parametrize(
    'psum_exp, power, expected_psum',
    (
        (
                alphaclops.PauliSumExponential(alphaclops.Z(q1), np.pi / 2),
                5,
                alphaclops.PauliSumExponential(alphaclops.Z(q1), 5 * np.pi / 2),
        ),
        (
                alphaclops.PauliSumExponential(2j * alphaclops.X(q0) + 3j * alphaclops.Y(q2), sympy.Symbol("theta")),
                5,
                alphaclops.PauliSumExponential(2j * alphaclops.X(q0) + 3j * alphaclops.Y(q2), 5 * sympy.Symbol("theta")),
        ),
        (
                alphaclops.PauliSumExponential(alphaclops.X(q0) * alphaclops.Y(q1) + alphaclops.Y(q2) * alphaclops.Z(q3), np.pi),
                5,
                alphaclops.PauliSumExponential(alphaclops.X(q0) * alphaclops.Y(q1) + alphaclops.Y(q2) * alphaclops.Z(q3), 5 * np.pi),
        ),
    ),
)
def test_pauli_sum_exponential_pow(psum_exp, power, expected_psum):
    assert psum_exp**power == expected_psum


@pytest.mark.parametrize(
    'psum_exp',
    (
        (alphaclops.PauliSumExponential(0, np.pi / 2)),
        (alphaclops.PauliSumExponential(2j * alphaclops.X(q0) + 3j * alphaclops.Z(q1), np.pi / 2)),
    ),
)
def test_pauli_sum_exponential_repr(psum_exp):
    alphaclops.testing.assert_equivalent_repr(psum_exp)


@pytest.mark.parametrize(
    'psum_exp, expected_str',
    (
        (alphaclops.PauliSumExponential(0, np.pi / 2), 'exp(j * 1.5707963267948966 * (0.000))'),
        (
                alphaclops.PauliSumExponential(2j * alphaclops.X(q0) + 4j * alphaclops.Y(q1), 2),
            'exp(2 * (2.000j*X(q(0))+4.000j*Y(q(1))))',
        ),
        (
                alphaclops.PauliSumExponential(0.5 * alphaclops.X(q0) + 0.6 * alphaclops.Y(q1), sympy.Symbol("theta")),
            'exp(j * theta * (0.500*X(q(0))+0.600*Y(q(1))))',
        ),
    ),
)
def test_pauli_sum_exponential_formatting(psum_exp, expected_str):
    assert str(psum_exp) == expected_str
