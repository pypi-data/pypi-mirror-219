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

import random

import numpy as np
import pytest

import alphaclops
from alphaclops import value
from alphaclops import unitary_eig

X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
H = np.array([[1, 1], [1, -1]]) * np.sqrt(0.5)
SQRT_X = np.array([[1, 1j], [1j, 1]])
c = np.exp(1j * np.pi / 4)
SQRT_SQRT_X = np.array([[1 + c, 1 - c], [1 - c, 1 + c]]) / 2
SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
CZ = np.diag([1, 1, 1, -1])


def assert_kronecker_factorization_within_tolerance(matrix, g, f1, f2):
    restored = g * alphaclops.linalg.combinators.kron(f1, f2)
    assert not np.any(np.isnan(restored)), "NaN in kronecker product."
    assert np.allclose(restored, matrix), "Can't factor kronecker product."


def assert_kronecker_factorization_not_within_tolerance(matrix, g, f1, f2):
    restored = g * alphaclops.linalg.combinators.kron(f1, f2)
    assert np.any(np.isnan(restored) or not np.allclose(restored, matrix))


def assert_magic_su2_within_tolerance(mat, a, b):
    M = alphaclops.linalg.decompositions.MAGIC
    MT = alphaclops.linalg.decompositions.MAGIC_CONJ_T
    recon = alphaclops.linalg.combinators.dot(MT, alphaclops.linalg.combinators.kron(a, b), M)
    assert np.allclose(recon, mat), "Failed to decompose within tolerance."


@pytest.mark.parametrize('matrix', [X, alphaclops.kron(X, X), alphaclops.kron(X, Y), alphaclops.kron(X, np.eye(2))])
def test_map_eigenvalues_identity(matrix):
    identity_mapped = alphaclops.map_eigenvalues(matrix, lambda e: e)
    assert np.allclose(matrix, identity_mapped)


@pytest.mark.parametrize(
    'matrix,exponent,desired',
    [
        [X, 2, np.eye(2)],
        [X, 3, X],
        [Z, 2, np.eye(2)],
        [H, 2, np.eye(2)],
        [Z, 0.5, np.diag([1, 1j])],
        [X, 0.5, np.array([[1j, 1], [1, 1j]]) * (1 - 1j) / 2],
    ],
)
def test_map_eigenvalues_raise(matrix, exponent, desired):
    exp_mapped = alphaclops.map_eigenvalues(matrix, lambda e: complex(e) ** exponent)
    assert np.allclose(desired, exp_mapped)


def _random_unitary_with_close_eigenvalues():
    U = alphaclops.testing.random_unitary(4)
    d = np.diag(np.exp([-0.2312j, -0.2312j, -0.2332j, -0.2322j]))
    return U @ d @ U.conj().T


@pytest.mark.parametrize(
    'matrix',
    [
        X,
        np.eye(4),
        np.diag(np.exp([-1j * np.pi * 1.23, -1j * np.pi * 1.23, -1j * np.pi * 1.23])),
        # a global phase with a tiny perturbation
        np.diag(np.exp([-0.2312j, -0.2312j, -0.2312j, -0.2312j]))
        + np.random.random((4, 4)) * 1e-100,
        # also after a similarity transformation, demonstrating
        # that the effect is due to close eigenvalues, not diagonality
        _random_unitary_with_close_eigenvalues(),
    ],
)
def test_unitary_eig(matrix):
    # np.linalg.eig(matrix) won't work for the perturbed matrix
    d, vecs = unitary_eig(matrix)

    # test both unitarity and correctness of decomposition
    np.testing.assert_allclose(matrix, vecs @ np.diag(d) @ vecs.conj().T, atol=1e-14)


def test_non_unitary_eig():
    with pytest.raises(Exception):
        unitary_eig(np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 0, 1, 2], [3, 4, 5, 6]]))


@pytest.mark.parametrize(
    'f1,f2',
    [
        (H, X),
        (H * 1j, X),
        (H, SQRT_X),
        (H, SQRT_SQRT_X),
        (H, H),
        (SQRT_SQRT_X, H),
        (X, np.eye(2)),
        (1j * X, np.eye(2)),
        (X, 1j * np.eye(2)),
        (-X, 1j * np.eye(2)),
        (X, X),
    ]
    + [(alphaclops.testing.random_unitary(2), alphaclops.testing.random_unitary(2)) for _ in range(10)],
)
def test_kron_factor(f1, f2):
    p = alphaclops.kron(f1, f2)
    g, g1, g2 = alphaclops.kron_factor_4x4_to_2x2s(p)
    assert abs(np.linalg.det(g1) - 1) < 0.00001
    assert abs(np.linalg.det(g2) - 1) < 0.00001
    assert np.allclose(g * alphaclops.kron(g1, g2), p)
    assert_kronecker_factorization_within_tolerance(p, g, g1, g2)


@pytest.mark.parametrize(
    'f1,f2',
    [
        (alphaclops.testing.random_special_unitary(2), alphaclops.testing.random_special_unitary(2))
        for _ in range(10)
    ],
)
def test_kron_factor_special_unitaries(f1, f2):
    p = alphaclops.kron(f1, f2)
    g, g1, g2 = alphaclops.kron_factor_4x4_to_2x2s(p)
    assert np.allclose(alphaclops.kron(g1, g2), p)
    assert abs(g - 1) < 0.000001
    assert alphaclops.is_special_unitary(g1)
    assert alphaclops.is_special_unitary(g2)
    assert_kronecker_factorization_within_tolerance(p, g, g1, g2)


def test_kron_factor_fail():
    mat = alphaclops.kron_with_controls(alphaclops.CONTROL_TAG, X)
    g, f1, f2 = alphaclops.kron_factor_4x4_to_2x2s(mat)
    with pytest.raises(ValueError):
        assert_kronecker_factorization_not_within_tolerance(mat, g, f1, f2)
    mat = alphaclops.kron_factor_4x4_to_2x2s(np.diag([1, 1, 1, 1j]))
    with pytest.raises(ValueError):
        assert_kronecker_factorization_not_within_tolerance(mat, g, f1, f2)


def recompose_so4(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    assert a.shape == (2, 2)
    assert b.shape == (2, 2)
    assert alphaclops.is_special_unitary(a)
    assert alphaclops.is_special_unitary(b)

    magic = np.array([[1, 0, 0, 1j], [0, 1j, 1, 0], [0, 1j, -1, 0], [1, 0, 0, -1j]]) * np.sqrt(0.5)
    result = np.real(alphaclops.dot(np.conj(magic.T), alphaclops.kron(a, b), magic))
    assert alphaclops.is_orthogonal(result)
    return result


@pytest.mark.parametrize('m', [alphaclops.testing.random_special_orthogonal(4) for _ in range(10)])
def test_so4_to_magic_su2s(m):
    a, b = alphaclops.so4_to_magic_su2s(m)
    m2 = recompose_so4(a, b)
    assert_magic_su2_within_tolerance(m2, a, b)
    assert np.allclose(m, m2)


@pytest.mark.parametrize(
    'a,b',
    [
        (alphaclops.testing.random_special_unitary(2), alphaclops.testing.random_special_unitary(2))
        for _ in range(10)
    ],
)
def test_so4_to_magic_su2s_known_factors(a, b):
    m = recompose_so4(a, b)
    a2, b2 = alphaclops.so4_to_magic_su2s(m)
    m2 = recompose_so4(a2, b2)

    assert np.allclose(m2, m)

    # Account for kron(A, B) = kron(-A, -B).
    if np.linalg.norm(a + a2) > np.linalg.norm(a - a2):
        assert np.allclose(a2, a)
        assert np.allclose(b2, b)
    else:
        assert np.allclose(a2, -a)
        assert np.allclose(b2, -b)


@pytest.mark.parametrize(
    'mat',
    [
        np.diag([0, 1, 1, 1]),
        np.diag([0.5, 2, 1, 1]),
        np.diag([1, 1j, 1, 1]),
        np.diag([1, 1, 1, -1]),
    ],
)
def test_so4_to_magic_su2s_fail(mat):
    with pytest.raises(ValueError):
        _ = alphaclops.so4_to_magic_su2s(mat)


@pytest.mark.parametrize(
    'x,y,z', [[(random.random() * 2 - 1) * np.pi * 2 for _ in range(3)] for _ in range(10)]
)
def test_kak_canonicalize_vector(x, y, z):
    i = np.eye(2)
    m = alphaclops.unitary(
        alphaclops.KakDecomposition(
            global_phase=1,
            single_qubit_operations_after=(i, i),
            interaction_coefficients=(x, y, z),
            single_qubit_operations_before=(i, i),
        )
    )

    kak = alphaclops.kak_canonicalize_vector(x, y, z, atol=1e-10)
    a1, a0 = kak.single_qubit_operations_after
    x2, y2, z2 = kak.interaction_coefficients
    b1, b0 = kak.single_qubit_operations_before
    m2 = alphaclops.unitary(kak)

    assert 0.0 <= x2 <= np.pi / 4
    assert 0.0 <= y2 <= np.pi / 4
    assert -np.pi / 4 < z2 <= np.pi / 4
    assert abs(x2) >= abs(y2) >= abs(z2)
    assert x2 < np.pi / 4 - 1e-10 or z2 >= 0
    assert alphaclops.is_special_unitary(a1)
    assert alphaclops.is_special_unitary(a0)
    assert alphaclops.is_special_unitary(b1)
    assert alphaclops.is_special_unitary(b0)
    assert np.allclose(m, m2)


def test_kak_vector_empty():
    assert len(alphaclops.kak_vector([])) == 0


@pytest.mark.usefixtures('closefigures')
def test_kak_plot_empty():
    alphaclops.scatter_plot_normalized_kak_interaction_coefficients([])


@pytest.mark.parametrize(
    'target',
    [np.eye(4), SWAP, SWAP * 1j, CZ, CNOT, SWAP @ CZ]
    + [alphaclops.testing.random_unitary(4) for _ in range(10)],
)
def test_kak_decomposition(target):
    kak = alphaclops.kak_decomposition(target)
    np.testing.assert_allclose(alphaclops.unitary(kak), target, atol=1e-8)


def test_kak_decomposition_unitary_object():
    op = alphaclops.ISWAP(*alphaclops.LineQubit.range(2)) ** 0.5
    kak = alphaclops.kak_decomposition(op)
    np.testing.assert_allclose(alphaclops.unitary(kak), alphaclops.unitary(op), atol=1e-8)
    assert alphaclops.kak_decomposition(kak) is kak


def test_kak_decomposition_invalid_object():
    with pytest.raises(TypeError, match='unitary effect'):
        _ = alphaclops.kak_decomposition('test')

    with pytest.raises(ValueError, match='4x4 unitary matrix'):
        _ = alphaclops.kak_decomposition(np.eye(3))

    with pytest.raises(ValueError, match='4x4 unitary matrix'):
        _ = alphaclops.kak_decomposition(np.eye(8))

    with pytest.raises(ValueError, match='4x4 unitary matrix'):
        _ = alphaclops.kak_decomposition(np.ones((4, 4)))

    with pytest.raises(ValueError, match='4x4 unitary matrix'):
        _ = alphaclops.kak_decomposition(np.zeros((4, 4)))

    nil = alphaclops.kak_decomposition(np.zeros((4, 4)), check_preconditions=False)
    np.testing.assert_allclose(alphaclops.unitary(nil), np.eye(4), atol=1e-8)


def test_kak_decomposition_eq():
    eq = alphaclops.testing.EqualsTester()

    eq.make_equality_group(
        lambda: alphaclops.KakDecomposition(
            global_phase=1,
            single_qubit_operations_before=(alphaclops.unitary(alphaclops.X), alphaclops.unitary(alphaclops.Y)),
            interaction_coefficients=(0.3, 0.2, 0.1),
            single_qubit_operations_after=(np.eye(2), alphaclops.unitary(alphaclops.Z)),
        )
    )

    eq.add_equality_group(
        alphaclops.KakDecomposition(
            global_phase=-1,
            single_qubit_operations_before=(alphaclops.unitary(alphaclops.X), alphaclops.unitary(alphaclops.Y)),
            interaction_coefficients=(0.3, 0.2, 0.1),
            single_qubit_operations_after=(np.eye(2), alphaclops.unitary(alphaclops.Z)),
        )
    )

    eq.add_equality_group(
        alphaclops.KakDecomposition(
            global_phase=1,
            single_qubit_operations_before=(np.eye(2), np.eye(2)),
            interaction_coefficients=(0.3, 0.2, 0.1),
            single_qubit_operations_after=(np.eye(2), np.eye(2)),
        ),
        alphaclops.KakDecomposition(interaction_coefficients=(0.3, 0.2, 0.1)),
    )

    eq.make_equality_group(
        lambda: alphaclops.KakDecomposition(
            global_phase=1,
            single_qubit_operations_before=(alphaclops.unitary(alphaclops.X), alphaclops.unitary(alphaclops.H)),
            interaction_coefficients=(0.3, 0.2, 0.1),
            single_qubit_operations_after=(np.eye(2), alphaclops.unitary(alphaclops.Z)),
        )
    )

    eq.make_equality_group(
        lambda: alphaclops.KakDecomposition(
            global_phase=1,
            single_qubit_operations_before=(alphaclops.unitary(alphaclops.X), alphaclops.unitary(alphaclops.Y)),
            interaction_coefficients=(0.5, 0.2, 0.1),
            single_qubit_operations_after=(np.eye(2), alphaclops.unitary(alphaclops.Z)),
        )
    )


def test_kak_repr():
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.KakDecomposition(
            global_phase=1j,
            single_qubit_operations_before=(alphaclops.unitary(alphaclops.X), alphaclops.unitary(alphaclops.Y)),
            interaction_coefficients=(0.3, 0.2, 0.1),
            single_qubit_operations_after=(np.eye(2), alphaclops.unitary(alphaclops.Z)),
        )
    )

    assert (
        repr(
            alphaclops.KakDecomposition(
                global_phase=1,
                single_qubit_operations_before=(alphaclops.unitary(alphaclops.X), alphaclops.unitary(alphaclops.Y)),
                interaction_coefficients=(0.5, 0.25, 0),
                single_qubit_operations_after=(np.eye(2), alphaclops.unitary(alphaclops.Z)),
            )
        )
        == """
alphaclops.KakDecomposition(
    interaction_coefficients=(0.5, 0.25, 0),
    single_qubit_operations_before=(
        np.array([[0j, (1+0j)], [(1+0j), 0j]], dtype=np.dtype('complex128')),
        np.array([[0j, -1j], [1j, 0j]], dtype=np.dtype('complex128')),
    ),
    single_qubit_operations_after=(
        np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.dtype('float64')),
        np.array([[(1+0j), 0j], [0j, (-1+0j)]], dtype=np.dtype('complex128')),
    ),
    global_phase=1)
""".strip()
    )


def test_kak_str():
    v = alphaclops.KakDecomposition(
        interaction_coefficients=(0.3 * np.pi / 4, 0.2 * np.pi / 4, 0.1 * np.pi / 4),
        single_qubit_operations_before=(alphaclops.unitary(alphaclops.I), alphaclops.unitary(alphaclops.X)),
        single_qubit_operations_after=(alphaclops.unitary(alphaclops.Y), alphaclops.unitary(alphaclops.Z)),
        global_phase=1j,
    )
    assert (
        str(v)
        == """KAK {
    xyz*(4/π): 0.3, 0.2, 0.1
    before: (0*π around X) ⊗ (1*π around X)
    after: (1*π around Y) ⊗ (1*π around Z)
}"""
    )


def test_axis_angle_decomposition_eq():
    eq = alphaclops.testing.EqualsTester()

    eq.make_equality_group(
        lambda: alphaclops.AxisAngleDecomposition(angle=1, axis=(0.8, 0.6, 0), global_phase=-1)
    )
    eq.add_equality_group(alphaclops.AxisAngleDecomposition(angle=5, axis=(0.8, 0.6, 0), global_phase=-1))
    eq.add_equality_group(alphaclops.AxisAngleDecomposition(angle=1, axis=(0.8, 0, 0.6), global_phase=-1))
    eq.add_equality_group(alphaclops.AxisAngleDecomposition(angle=1, axis=(0.8, 0.6, 0), global_phase=1))


def test_axis_angle_decomposition_repr():
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.AxisAngleDecomposition(angle=1, axis=(0, 0.6, 0.8), global_phase=-1)
    )


def test_axis_angle_decomposition_str():
    assert str(alphaclops.axis_angle(alphaclops.unitary(alphaclops.X))) == '1*π around X'
    assert str(alphaclops.axis_angle(alphaclops.unitary(alphaclops.Y))) == '1*π around Y'
    assert str(alphaclops.axis_angle(alphaclops.unitary(alphaclops.Z))) == '1*π around Z'
    assert str(alphaclops.axis_angle(alphaclops.unitary(alphaclops.H))) == '1*π around 0.707*X+0.707*Z'
    assert str(alphaclops.axis_angle(alphaclops.unitary(alphaclops.H ** 0.5))) == '0.5*π around 0.707*X+0.707*Z'
    assert (
        str(
            alphaclops.axis_angle(
                alphaclops.unitary(alphaclops.X ** 0.25)
                @ alphaclops.unitary(alphaclops.Y ** 0.25)
                @ alphaclops.unitary(alphaclops.Z ** 0.25)
            )
        )
        == '0.477*π around 0.679*X+0.281*Y+0.679*Z'
    )


def test_axis_angle_decomposition_unitary():
    u = alphaclops.testing.random_unitary(2)
    u = alphaclops.unitary(alphaclops.T)
    a = alphaclops.axis_angle(u)
    np.testing.assert_allclose(u, alphaclops.unitary(a), atol=1e-8)


def test_axis_angle():
    assert alphaclops.approx_eq(
        alphaclops.axis_angle(alphaclops.unitary(alphaclops.ry(1e-10))),
        alphaclops.AxisAngleDecomposition(angle=0, axis=(1, 0, 0), global_phase=1),
        atol=1e-8,
    )
    assert alphaclops.approx_eq(
        alphaclops.axis_angle(alphaclops.unitary(alphaclops.rx(np.pi))),
        alphaclops.AxisAngleDecomposition(angle=np.pi, axis=(1, 0, 0), global_phase=1),
        atol=1e-8,
    )
    assert alphaclops.approx_eq(
        alphaclops.axis_angle(alphaclops.unitary(alphaclops.X)),
        alphaclops.AxisAngleDecomposition(angle=np.pi, axis=(1, 0, 0), global_phase=1j),
        atol=1e-8,
    )
    assert alphaclops.approx_eq(
        alphaclops.axis_angle(alphaclops.unitary(alphaclops.X ** 0.5)),
        alphaclops.AxisAngleDecomposition(
            angle=np.pi / 2, axis=(1, 0, 0), global_phase=np.exp(1j * np.pi / 4)
        ),
        atol=1e-8,
    )
    assert alphaclops.approx_eq(
        alphaclops.axis_angle(alphaclops.unitary(alphaclops.X ** -0.5)),
        alphaclops.AxisAngleDecomposition(
            angle=-np.pi / 2, axis=(1, 0, 0), global_phase=np.exp(-1j * np.pi / 4)
        ),
    )

    assert alphaclops.approx_eq(
        alphaclops.axis_angle(alphaclops.unitary(alphaclops.Y)),
        alphaclops.AxisAngleDecomposition(angle=np.pi, axis=(0, 1, 0), global_phase=1j),
        atol=1e-8,
    )

    assert alphaclops.approx_eq(
        alphaclops.axis_angle(alphaclops.unitary(alphaclops.Z)),
        alphaclops.AxisAngleDecomposition(angle=np.pi, axis=(0, 0, 1), global_phase=1j),
        atol=1e-8,
    )

    assert alphaclops.approx_eq(
        alphaclops.axis_angle(alphaclops.unitary(alphaclops.H)),
        alphaclops.AxisAngleDecomposition(
            angle=np.pi, axis=(np.sqrt(0.5), 0, np.sqrt(0.5)), global_phase=1j
        ),
        atol=1e-8,
    )

    assert alphaclops.approx_eq(
        alphaclops.axis_angle(alphaclops.unitary(alphaclops.H ** 0.5)),
        alphaclops.AxisAngleDecomposition(
            angle=np.pi / 2,
            axis=(np.sqrt(0.5), 0, np.sqrt(0.5)),
            global_phase=np.exp(1j * np.pi / 4),
        ),
        atol=1e-8,
    )


def test_axis_angle_canonicalize():
    a = alphaclops.AxisAngleDecomposition(
        angle=np.pi * 2.3, axis=(1, 0, 0), global_phase=1j
    ).canonicalize()
    assert a.global_phase == -1j
    assert a.axis == (1, 0, 0)
    np.testing.assert_allclose(a.angle, np.pi * 0.3, atol=1e-8)

    a = alphaclops.AxisAngleDecomposition(
        angle=np.pi / 2, axis=(-1, 0, 0), global_phase=1j
    ).canonicalize()
    assert a.global_phase == 1j
    assert a.axis == (1, 0, 0)
    assert a.angle == -np.pi / 2

    a = alphaclops.AxisAngleDecomposition(
        angle=np.pi + 0.01, axis=(1, 0, 0), global_phase=1j
    ).canonicalize(atol=0.1)
    assert a.global_phase == 1j
    assert a.axis == (1, 0, 0)
    assert a.angle == np.pi + 0.01

    a = alphaclops.AxisAngleDecomposition(
        angle=np.pi + 0.01, axis=(1, 0, 0), global_phase=1j
    ).canonicalize(atol=0.001)
    assert a.global_phase == -1j
    assert a.axis == (1, 0, 0)
    assert np.isclose(a.angle, -np.pi + 0.01)


def test_axis_angle_canonicalize_approx_equal():
    a1 = alphaclops.AxisAngleDecomposition(angle=np.pi, axis=(1, 0, 0), global_phase=1)
    a2 = alphaclops.AxisAngleDecomposition(angle=-np.pi, axis=(1, 0, 0), global_phase=-1)
    b1 = alphaclops.AxisAngleDecomposition(angle=np.pi, axis=(1, 0, 0), global_phase=-1)
    assert alphaclops.approx_eq(a1, a2, atol=1e-8)
    assert not alphaclops.approx_eq(a1, b1, atol=1e-8)


def test_axis_angle_init():
    a = alphaclops.AxisAngleDecomposition(angle=1, axis=(0, 1, 0), global_phase=1j)
    assert a.angle == 1
    assert a.axis == (0, 1, 0)
    assert a.global_phase == 1j

    with pytest.raises(ValueError, match='normalize'):
        alphaclops.AxisAngleDecomposition(angle=1, axis=(0, 0.5, 0), global_phase=1)


@pytest.mark.usefixtures('closefigures')
def test_scatter_plot_normalized_kak_interaction_coefficients():
    a, b = alphaclops.LineQubit.range(2)
    data = [
        alphaclops.kak_decomposition(alphaclops.unitary(alphaclops.CZ)),
        alphaclops.unitary(alphaclops.CZ),
        alphaclops.CZ,
        alphaclops.Circuit(alphaclops.H(a), alphaclops.CNOT(a, b)),
    ]
    ax = alphaclops.scatter_plot_normalized_kak_interaction_coefficients(data)
    assert ax is not None
    ax2 = alphaclops.scatter_plot_normalized_kak_interaction_coefficients(
        data, s=1, c='blue', ax=ax, include_frame=False, label='test'
    )
    assert ax2 is ax

    ax3 = alphaclops.scatter_plot_normalized_kak_interaction_coefficients(data[1], ax=ax)
    assert ax3 is ax


def _vector_kron(first: np.ndarray, second: np.ndarray) -> np.ndarray:
    """Vectorized implementation of kron for square matrices."""
    s_0, s_1 = first.shape[-2:], second.shape[-2:]
    assert s_0[0] == s_0[1]
    assert s_1[0] == s_1[1]
    out = np.einsum('...ab,...cd->...acbd', first, second)
    s_v = out.shape[:-4]
    return out.reshape(s_v + (s_0[0] * s_1[0],) * 2)


def _local_two_qubit_unitaries(samples, random_state):
    kl_0 = np.array(
        [alphaclops.testing.random_unitary(2, random_state=random_state) for _ in range(samples)]
    )
    kl_1 = np.array(
        [alphaclops.testing.random_unitary(2, random_state=random_state) for _ in range(samples)]
    )

    return _vector_kron(kl_0, kl_1)


_kak_gens = np.array([np.kron(X, X), np.kron(Y, Y), np.kron(Z, Z)])


def _random_two_qubit_unitaries(num_samples: int, random_state: 'alphaclops.RANDOM_STATE_OR_SEED_LIKE'):
    # Randomly generated two-qubit unitaries and the KAK vectors (not canonical)
    kl = _local_two_qubit_unitaries(num_samples, random_state)

    kr = _local_two_qubit_unitaries(num_samples, random_state)

    prng = value.parse_random_state(random_state)
    # Generate the non-local part by explict matrix exponentiation.
    kak_vecs = prng.rand(num_samples, 3) * np.pi
    gens = np.einsum('...a,abc->...bc', kak_vecs, _kak_gens)
    evals, evecs = np.linalg.eigh(gens)
    A = np.einsum('...ab,...b,...cb', evecs, np.exp(1j * evals), evecs.conj())

    return np.einsum('...ab,...bc,...cd', kl, A, kr), kak_vecs


def _local_invariants_from_kak(vector: np.ndarray) -> np.ndarray:
    r"""Local invariants of a two-qubit unitary from its KAK vector.

    Any 2 qubit unitary may be expressed as

    $U = k_l A k_r$
    where $k_l, k_r$ are single qubit (local) unitaries and

    $$
    A = \exp( i * \sum_{j=x,y,z} k_j \sigma_{(j,0)}\sigma_{(j,1)})
    $$

    Here $(k_x,k_y,k_z)$ is the KAK vector.

    Args:
        vector: Shape (...,3) tensor representing different KAK vectors.

    Returns:
        The local invariants associated with the given KAK vector. Shape
        (..., 3), where first two elements are the real and imaginary parts
        of G1 and the third is G2.

    References:
        "A geometric theory of non-local two-qubit operations"
        https://arxiv.org/abs/quant-ph/0209120
    """
    vector = np.asarray(vector)
    # See equation 30 in the above reference. Compared to their notation, the k
    # vector equals c/2.
    kx = vector[..., 0]
    ky = vector[..., 1]
    kz = vector[..., 2]
    cos, sin = np.cos, np.sin
    G1R = (cos(2 * kx) * cos(2 * ky) * cos(2 * kz)) ** 2
    G1R -= (sin(2 * kx) * sin(2 * ky) * sin(2 * kz)) ** 2

    G1I = 0.25 * sin(4 * kx) * sin(4 * ky) * sin(4 * kz)

    G2 = cos(4 * kx) + cos(4 * ky) + cos(4 * kz)
    return np.moveaxis(np.array([G1R, G1I, G2]), 0, -1)


_random_unitaries, _kak_vecs = _random_two_qubit_unitaries(100, random_state=11)


def test_kak_vector_matches_vectorized():
    actual = alphaclops.kak_vector(_random_unitaries)
    expected = np.array([alphaclops.kak_vector(u) for u in _random_unitaries])
    np.testing.assert_almost_equal(actual, expected)


def test_KAK_vector_local_invariants_random_input():
    actual = _local_invariants_from_kak(alphaclops.kak_vector(_random_unitaries))
    expected = _local_invariants_from_kak(_kak_vecs)

    np.testing.assert_almost_equal(actual, expected)


def test_kak_vector_on_weyl_chamber_face():
    # unitaries with KAK vectors from I to ISWAP
    theta_swap = np.linspace(0, np.pi / 4, 10)
    k_vecs = np.zeros((10, 3))
    k_vecs[:, (0, 1)] = theta_swap[:, np.newaxis]

    kwargs = dict(
        global_phase=1j,
        single_qubit_operations_before=(X, Y),
        single_qubit_operations_after=(Z, 1j * X),
    )
    unitaries = np.array(
        [
            alphaclops.unitary(alphaclops.KakDecomposition(interaction_coefficients=(t, t, 0), **kwargs))
            for t in theta_swap
        ]
    )

    actual = alphaclops.kak_vector(unitaries)
    np.testing.assert_almost_equal(actual, k_vecs)


@pytest.mark.parametrize(
    'unitary,expected',
    (
        (np.eye(4), (0, 0, 0)),
        (SWAP, [np.pi / 4] * 3),
        (SWAP * 1j, [np.pi / 4] * 3),
        (CNOT, [np.pi / 4, 0, 0]),
        (CZ, [np.pi / 4, 0, 0]),
        (CZ @ SWAP, [np.pi / 4, np.pi / 4, 0]),
        (np.kron(X, X), (0, 0, 0)),
    ),
)
def test_KAK_vector_weyl_chamber_vertices(unitary, expected):
    actual = alphaclops.kak_vector(unitary)
    np.testing.assert_almost_equal(actual, expected)


cases = [np.eye(3), SWAP.reshape((2, 8)), SWAP.ravel()]


@pytest.mark.parametrize('bad_input', cases)
def test_kak_vector_wrong_matrix_shape(bad_input):
    with pytest.raises(ValueError, match='to have shape'):
        alphaclops.kak_vector(bad_input)


def test_kak_vector_negative_atol():
    with pytest.raises(ValueError, match='must be positive'):
        alphaclops.kak_vector(np.eye(4), atol=-1.0)


def test_kak_vector_input_not_unitary():
    with pytest.raises(ValueError, match='must correspond to'):
        alphaclops.kak_vector(np.zeros((4, 4)))


@pytest.mark.parametrize(
    'unitary',
    [
        alphaclops.testing.random_unitary(4),
        alphaclops.unitary(alphaclops.IdentityGate(2)),
        alphaclops.unitary(alphaclops.SWAP),
        alphaclops.unitary(alphaclops.SWAP ** 0.25),
        alphaclops.unitary(alphaclops.ISWAP),
        alphaclops.unitary(alphaclops.CZ ** 0.5),
        alphaclops.unitary(alphaclops.CZ),
    ],
)
def test_kak_decompose(unitary: np.ndarray):
    kak = alphaclops.kak_decomposition(unitary)
    circuit = alphaclops.Circuit(kak._decompose_(alphaclops.LineQubit.range(2)))
    np.testing.assert_allclose(alphaclops.unitary(circuit), unitary, atol=1e-6)
    assert len(circuit) == 5
    assert len(list(circuit.all_operations())) == 8


def test_num_two_qubit_gates_required():
    for i in range(4):
        assert (
                alphaclops.num_cnots_required(
                alphaclops.testing.random_two_qubit_circuit_with_czs(i).unitary(), atol=1e-6
            )
                == i
        )

    assert alphaclops.num_cnots_required(np.eye(4)) == 0


def test_num_two_qubit_gates_required_invalid():
    with pytest.raises(ValueError, match="(4,4)"):
        alphaclops.num_cnots_required(np.array([[1]]))


@pytest.mark.parametrize(
    "u",
    [
        alphaclops.testing.random_two_qubit_circuit_with_czs(3).unitary(),
        # an example where gamma(special(u))=I, so the denominator becomes 0
        1
        / np.sqrt(2)
        * np.array(
            [
                [(1 - 1j) * 2 / np.sqrt(5), 0, 0, (1 - 1j) * 1 / np.sqrt(5)],
                [0, 0, 1 - 1j, 0],
                [0, 1 - 1j, 0, 0],
                [-(1 - 1j) * 1 / np.sqrt(5), 0, 0, (1 - 1j) * 2 / np.sqrt(5)],
            ],
            dtype=np.complex128,
        ),
    ],
)
def test_extract_right_diag(u):
    assert alphaclops.num_cnots_required(u) == 3
    diag = alphaclops.linalg.extract_right_diag(u)
    assert alphaclops.is_diagonal(diag)
    assert alphaclops.num_cnots_required(u @ diag) == 2
