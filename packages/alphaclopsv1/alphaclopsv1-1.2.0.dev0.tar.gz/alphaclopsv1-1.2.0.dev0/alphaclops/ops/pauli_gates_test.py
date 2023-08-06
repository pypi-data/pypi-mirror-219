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

import numpy as np
import pytest
import alphaclops


def test_equals():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(alphaclops.X, alphaclops.ops.pauli_gates.X, alphaclops.XPowGate())
    eq.add_equality_group(alphaclops.Y, alphaclops.ops.pauli_gates.Y, alphaclops.YPowGate())
    eq.add_equality_group(alphaclops.Z, alphaclops.ops.pauli_gates.Z, alphaclops.ZPowGate())


def test_phased_pauli_product():
    assert alphaclops.X.phased_pauli_product(alphaclops.I) == (1, alphaclops.X)
    assert alphaclops.X.phased_pauli_product(alphaclops.X) == (1, alphaclops.I)
    assert alphaclops.X.phased_pauli_product(alphaclops.Y) == (1j, alphaclops.Z)
    assert alphaclops.X.phased_pauli_product(alphaclops.Z) == (-1j, alphaclops.Y)

    assert alphaclops.Y.phased_pauli_product(alphaclops.I) == (1, alphaclops.Y)
    assert alphaclops.Y.phased_pauli_product(alphaclops.X) == (-1j, alphaclops.Z)
    assert alphaclops.Y.phased_pauli_product(alphaclops.Y) == (1, alphaclops.I)
    assert alphaclops.Y.phased_pauli_product(alphaclops.Z) == (1j, alphaclops.X)

    assert alphaclops.Z.phased_pauli_product(alphaclops.I) == (1, alphaclops.Z)
    assert alphaclops.Z.phased_pauli_product(alphaclops.X) == (1j, alphaclops.Y)
    assert alphaclops.Z.phased_pauli_product(alphaclops.Y) == (-1j, alphaclops.X)
    assert alphaclops.Z.phased_pauli_product(alphaclops.Z) == (1, alphaclops.I)


def test_isinstance():
    assert isinstance(alphaclops.X, alphaclops.XPowGate)
    assert isinstance(alphaclops.Y, alphaclops.YPowGate)
    assert isinstance(alphaclops.Z, alphaclops.ZPowGate)

    assert not isinstance(alphaclops.X, alphaclops.YPowGate)
    assert not isinstance(alphaclops.X, alphaclops.ZPowGate)

    assert not isinstance(alphaclops.Y, alphaclops.XPowGate)
    assert not isinstance(alphaclops.Y, alphaclops.ZPowGate)

    assert not isinstance(alphaclops.Z, alphaclops.XPowGate)
    assert not isinstance(alphaclops.Z, alphaclops.YPowGate)


def test_by_index():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(alphaclops.X, *[alphaclops.Pauli.by_index(i) for i in (-3, 0, 3, 6)])
    eq.add_equality_group(alphaclops.Y, *[alphaclops.Pauli.by_index(i) for i in (-2, 1, 4, 7)])
    eq.add_equality_group(alphaclops.Z, *[alphaclops.Pauli.by_index(i) for i in (-1, 2, 5, 8)])


def test_relative_index():
    assert alphaclops.X.relative_index(alphaclops.X) == 0
    assert alphaclops.X.relative_index(alphaclops.Y) == -1
    assert alphaclops.X.relative_index(alphaclops.Z) == 1
    assert alphaclops.Y.relative_index(alphaclops.X) == 1
    assert alphaclops.Y.relative_index(alphaclops.Y) == 0
    assert alphaclops.Y.relative_index(alphaclops.Z) == -1
    assert alphaclops.Z.relative_index(alphaclops.X) == -1
    assert alphaclops.Z.relative_index(alphaclops.Y) == 1
    assert alphaclops.Z.relative_index(alphaclops.Z) == 0


def test_by_relative_index():
    assert alphaclops.Pauli.by_relative_index(alphaclops.X, -1) == alphaclops.Z
    assert alphaclops.Pauli.by_relative_index(alphaclops.X, 0) == alphaclops.X
    assert alphaclops.Pauli.by_relative_index(alphaclops.X, 1) == alphaclops.Y
    assert alphaclops.Pauli.by_relative_index(alphaclops.X, 2) == alphaclops.Z
    assert alphaclops.Pauli.by_relative_index(alphaclops.X, 3) == alphaclops.X
    assert alphaclops.Pauli.by_relative_index(alphaclops.Y, -1) == alphaclops.X
    assert alphaclops.Pauli.by_relative_index(alphaclops.Y, 0) == alphaclops.Y
    assert alphaclops.Pauli.by_relative_index(alphaclops.Y, 1) == alphaclops.Z
    assert alphaclops.Pauli.by_relative_index(alphaclops.Y, 2) == alphaclops.X
    assert alphaclops.Pauli.by_relative_index(alphaclops.Y, 3) == alphaclops.Y
    assert alphaclops.Pauli.by_relative_index(alphaclops.Z, -1) == alphaclops.Y
    assert alphaclops.Pauli.by_relative_index(alphaclops.Z, 0) == alphaclops.Z
    assert alphaclops.Pauli.by_relative_index(alphaclops.Z, 1) == alphaclops.X
    assert alphaclops.Pauli.by_relative_index(alphaclops.Z, 2) == alphaclops.Y
    assert alphaclops.Pauli.by_relative_index(alphaclops.Z, 3) == alphaclops.Z


def test_too_many_qubits():
    a, b = alphaclops.LineQubit.range(2)
    with pytest.raises(ValueError, match='single qubit'):
        _ = alphaclops.X.on(a, b)

    x = alphaclops.X(a)
    with pytest.raises(ValueError, match=r'len\(new_qubits\)'):
        _ = x.with_qubits(a, b)


def test_relative_index_consistency():
    for pauli_1 in (alphaclops.X, alphaclops.Y, alphaclops.Z):
        for pauli_2 in (alphaclops.X, alphaclops.Y, alphaclops.Z):
            shift = pauli_2.relative_index(pauli_1)
            assert alphaclops.Pauli.by_relative_index(pauli_1, shift) == pauli_2


def test_gt():
    assert not alphaclops.X > alphaclops.X
    assert not alphaclops.X > alphaclops.Y
    assert alphaclops.X > alphaclops.Z
    assert alphaclops.Y > alphaclops.X
    assert not alphaclops.Y > alphaclops.Y
    assert not alphaclops.Y > alphaclops.Z
    assert not alphaclops.Z > alphaclops.X
    assert alphaclops.Z > alphaclops.Y
    assert not alphaclops.Z > alphaclops.Z


def test_gt_other_type():
    with pytest.raises(TypeError):
        _ = alphaclops.X > object()


def test_lt():
    assert not alphaclops.X < alphaclops.X
    assert alphaclops.X < alphaclops.Y
    assert not alphaclops.X < alphaclops.Z
    assert not alphaclops.Y < alphaclops.X
    assert not alphaclops.Y < alphaclops.Y
    assert alphaclops.Y < alphaclops.Z
    assert alphaclops.Z < alphaclops.X
    assert not alphaclops.Z < alphaclops.Y
    assert not alphaclops.Z < alphaclops.Z


def test_lt_other_type():
    with pytest.raises(TypeError):
        _ = alphaclops.X < object()


def test_str():
    assert str(alphaclops.X) == 'X'
    assert str(alphaclops.Y) == 'Y'
    assert str(alphaclops.Z) == 'Z'


def test_repr():
    assert repr(alphaclops.X) == 'alphaclops.X'
    assert repr(alphaclops.Y) == 'alphaclops.Y'
    assert repr(alphaclops.Z) == 'alphaclops.Z'


def test_third():
    assert alphaclops.X.third(alphaclops.Y) == alphaclops.Z
    assert alphaclops.Y.third(alphaclops.X) == alphaclops.Z
    assert alphaclops.Y.third(alphaclops.Z) == alphaclops.X
    assert alphaclops.Z.third(alphaclops.Y) == alphaclops.X
    assert alphaclops.Z.third(alphaclops.X) == alphaclops.Y
    assert alphaclops.X.third(alphaclops.Z) == alphaclops.Y

    assert alphaclops.X.third(alphaclops.X) == alphaclops.X
    assert alphaclops.Y.third(alphaclops.Y) == alphaclops.Y
    assert alphaclops.Z.third(alphaclops.Z) == alphaclops.Z


def test_commutes():
    for A, B in itertools.product([alphaclops.X, alphaclops.Y, alphaclops.Z], repeat=2):
        assert alphaclops.commutes(A, B) == (A == B)
    with pytest.raises(TypeError):
        assert alphaclops.commutes(alphaclops.X, 'X')
    assert alphaclops.commutes(alphaclops.X, 'X', default='default') == 'default'
    assert alphaclops.commutes(alphaclops.Z, alphaclops.read_json(json_text=alphaclops.to_json(alphaclops.Z)))


def test_unitary():
    np.testing.assert_equal(alphaclops.unitary(alphaclops.X), alphaclops.unitary(alphaclops.X))
    np.testing.assert_equal(alphaclops.unitary(alphaclops.Y), alphaclops.unitary(alphaclops.Y))
    np.testing.assert_equal(alphaclops.unitary(alphaclops.Z), alphaclops.unitary(alphaclops.Z))


def test_apply_unitary():
    alphaclops.testing.assert_has_consistent_apply_unitary(alphaclops.X)
    alphaclops.testing.assert_has_consistent_apply_unitary(alphaclops.Y)
    alphaclops.testing.assert_has_consistent_apply_unitary(alphaclops.Z)


def test_identity_multiplication():
    a, b, c = alphaclops.LineQubit.range(3)
    assert alphaclops.X(a) * alphaclops.I(a) == alphaclops.X(a)
    assert alphaclops.X(a) * alphaclops.I(b) == alphaclops.X(a)
    assert alphaclops.X(a) * alphaclops.Y(b) * alphaclops.I(c) == alphaclops.X(a) * alphaclops.Y(b)
    assert alphaclops.I(c) * alphaclops.X(a) * alphaclops.Y(b) == alphaclops.X(a) * alphaclops.Y(b)
    with pytest.raises(TypeError):
        _ = alphaclops.H(c) * alphaclops.X(a) * alphaclops.Y(b)
    with pytest.raises(TypeError):
        _ = alphaclops.X(a) * alphaclops.Y(b) * alphaclops.H(c)
    with pytest.raises(TypeError):
        _ = alphaclops.I(a) * str(alphaclops.Y(b))


def test_powers():
    assert isinstance(alphaclops.X, alphaclops.Pauli)
    assert isinstance(alphaclops.Y, alphaclops.Pauli)
    assert isinstance(alphaclops.Z, alphaclops.Pauli)
    assert not isinstance(alphaclops.X ** -0.5, alphaclops.Pauli)
    assert not isinstance(alphaclops.Y ** 0.2, alphaclops.Pauli)
    assert not isinstance(alphaclops.Z ** 0.5, alphaclops.Pauli)
    assert isinstance(alphaclops.X ** -0.5, alphaclops.XPowGate)
    assert isinstance(alphaclops.Y ** 0.2, alphaclops.YPowGate)
    assert isinstance(alphaclops.Z ** 0.5, alphaclops.ZPowGate)

    assert isinstance(alphaclops.X ** 1, alphaclops.Pauli)
    assert isinstance(alphaclops.Y ** 1, alphaclops.Pauli)
    assert isinstance(alphaclops.Z ** 1, alphaclops.Pauli)
