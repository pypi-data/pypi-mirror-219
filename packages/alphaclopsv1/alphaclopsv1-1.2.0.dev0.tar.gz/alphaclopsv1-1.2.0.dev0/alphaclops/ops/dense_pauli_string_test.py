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
import numbers
from typing import List

import numpy as np
import pytest
import sympy

import alphaclops
from alphaclops.ops.dense_pauli_string import _vectorized_pauli_mul_phase


def test_init():
    mask = np.array([0, 3, 1, 2], dtype=np.uint8)
    p = alphaclops.DensePauliString(coefficient=2, pauli_mask=mask)
    m = alphaclops.MutableDensePauliString(coefficient=3, pauli_mask=mask)
    assert p.coefficient == 2
    assert m.coefficient == 3
    np.testing.assert_allclose(p.pauli_mask, [0, 3, 1, 2])
    np.testing.assert_allclose(m.pauli_mask, [0, 3, 1, 2])

    # The non-mutable initializer makes a copy.
    assert m.pauli_mask is mask
    assert p.pauli_mask is not mask
    mask[:] = 0
    assert m.pauli_mask[2] == 0
    assert p.pauli_mask[2] == 1

    # Copies and converts non-uint8 arrays.
    p2 = alphaclops.DensePauliString(coefficient=2, pauli_mask=[1, 2, 3])
    m2 = alphaclops.DensePauliString(coefficient=2, pauli_mask=[1, 2, 3])
    assert p2.pauli_mask.dtype == m2.pauli_mask.dtype == np.uint8
    assert list(p2.pauli_mask) == list(m2.pauli_mask) == [1, 2, 3]

    # Mixed types.
    assert alphaclops.DensePauliString([1, 'X', alphaclops.X]) == alphaclops.DensePauliString('XXX')
    assert list(alphaclops.DensePauliString('XXX')) == [alphaclops.X, alphaclops.X, alphaclops.X]
    with pytest.raises(TypeError, match='Expected a alphaclops.PAULI_GATE_LIKE'):
        _ = alphaclops.DensePauliString([object()])


def test_value_to_char_correspondence():
    d = alphaclops.DensePauliString
    assert [d.I_VAL, d.X_VAL, d.Y_VAL, d.Z_VAL] == [0, 1, 2, 3]
    assert list(d([alphaclops.I, alphaclops.X, alphaclops.Y, alphaclops.Z]).pauli_mask) == [0, 1, 2, 3]
    assert list(d("IXYZ").pauli_mask) == [0, 1, 2, 3]
    assert list(d([d.I_VAL, d.X_VAL, d.Y_VAL, d.Z_VAL]).pauli_mask) == [0, 1, 2, 3]

    assert d('Y') * d('Z') == 1j * d('X')
    assert d('Z') * d('X') == 1j * d('Y')
    assert d('X') * d('Y') == 1j * d('Z')

    assert d('Y') * d('X') == -1j * d('Z')
    assert d('X') * d('Z') == -1j * d('Y')
    assert d('Z') * d('Y') == -1j * d('X')


def test_from_text():
    d = alphaclops.DensePauliString
    m = alphaclops.MutableDensePauliString

    assert d('') == d(pauli_mask=[])
    assert m('') == m(pauli_mask=[])

    assert d('YYXYY') == d([2, 2, 1, 2, 2])
    assert d('XYZI') == d([1, 2, 3, 0])
    assert d('III', coefficient=-1) == d([0, 0, 0], coefficient=-1)
    assert d('XXY', coefficient=1j) == d([1, 1, 2], coefficient=1j)
    assert d('ixyz') == d([0, 1, 2, 3])
    assert d(['i', 'x', 'y', 'z']) == d([0, 1, 2, 3])
    with pytest.raises(TypeError, match='Expected a alphaclops.PAULI_GATE_LIKE'):
        _ = d('2')


def test_immutable_eq():
    eq = alphaclops.testing.EqualsTester()

    # Immutables
    eq.make_equality_group(lambda: alphaclops.DensePauliString(coefficient=2, pauli_mask=[1]))
    eq.add_equality_group(lambda: alphaclops.DensePauliString(coefficient=3, pauli_mask=[1]))
    eq.make_equality_group(lambda: alphaclops.DensePauliString(coefficient=2, pauli_mask=[]))
    eq.add_equality_group(lambda: alphaclops.DensePauliString(coefficient=2, pauli_mask=[0]))
    eq.make_equality_group(lambda: alphaclops.DensePauliString(coefficient=2, pauli_mask=[2]))

    # Mutables
    eq.make_equality_group(lambda: alphaclops.MutableDensePauliString(coefficient=2, pauli_mask=[1]))
    eq.add_equality_group(lambda: alphaclops.MutableDensePauliString(coefficient=3, pauli_mask=[1]))
    eq.make_equality_group(lambda: alphaclops.MutableDensePauliString(coefficient=2, pauli_mask=[]))
    eq.make_equality_group(lambda: alphaclops.MutableDensePauliString(coefficient=2, pauli_mask=[2]))


def test_eye():
    f = alphaclops.DensePauliString
    m = alphaclops.MutableDensePauliString
    assert alphaclops.BaseDensePauliString.eye(4) == f('IIII')
    assert alphaclops.DensePauliString.eye(4) == f('IIII')
    assert alphaclops.MutableDensePauliString.eye(4) == m('IIII')


def test_sparse():
    a, b, c = alphaclops.LineQubit.range(3)
    p = -alphaclops.DensePauliString('XYZ')
    assert p.sparse() == alphaclops.PauliString(-1, alphaclops.X(a), alphaclops.Y(b), alphaclops.Z(c))
    assert p.sparse([c, b, a]) == alphaclops.PauliString(-1, alphaclops.X(c), alphaclops.Y(b), alphaclops.Z(a))
    with pytest.raises(ValueError, match='number of qubits'):
        _ = p.sparse([])
    with pytest.raises(ValueError, match='number of qubits'):
        _ = p.sparse(alphaclops.TensorCircuit.rect(2, 2))


def test_mul_vectorized_pauli_mul_phase():
    f = _vectorized_pauli_mul_phase
    paulis = [alphaclops.I, alphaclops.X, alphaclops.Y, alphaclops.Z]
    q = alphaclops.LineQubit(0)

    # Check single qubit cases.
    for i in range(4):
        for j in range(4):
            sparse1 = alphaclops.PauliString(paulis[i].on(q))
            sparse2 = alphaclops.PauliString(paulis[j].on(q))
            assert f(i, j) == (sparse1 * sparse2).coefficient

    # Check a vector case.
    assert (
        _vectorized_pauli_mul_phase(
            np.array([0, 1, 3, 2], dtype=np.uint8), np.array([0, 1, 2, 0], dtype=np.uint8)
        )
        == -1j
    )
    assert (
        _vectorized_pauli_mul_phase(np.array([], dtype=np.uint8), np.array([], dtype=np.uint8)) == 1
    )


def test_mul():
    f = alphaclops.DensePauliString

    # Scalar.
    assert -1 * f('XXX') == -1.0 * f('XXX') == f('XXX', coefficient=-1)
    assert 2 * f('XXX') == f('XXX') * 2 == (2 + 0j) * f('XXX')
    assert 2 * f('XXX') == f('XXX', coefficient=2)

    # Pair.
    assert f('') * f('') == f('')
    assert -f('X') * (1j * f('X')) == -1j * f('I')
    assert f('IXYZ') * f('XXXX') == f('XIZY')
    assert f('IXYX') * f('XXXX') == -1j * f('XIZI')
    assert f('XXXX') * f('IXYX') == 1j * f('XIZI')

    # Pauli operations.
    assert f('IXYZ') * alphaclops.X(alphaclops.LineQubit(0)) == f('XXYZ')
    assert -f('IXYZ') * alphaclops.X(alphaclops.LineQubit(1)) == -f('IIYZ')
    assert f('IXYZ') * alphaclops.X(alphaclops.LineQubit(2)) == -1j * f('IXZZ')
    assert alphaclops.X(alphaclops.LineQubit(0)) * f('IXYZ') == f('XXYZ')
    assert alphaclops.X(alphaclops.LineQubit(1)) * -f('IXYZ') == -f('IIYZ')
    assert alphaclops.X(alphaclops.LineQubit(2)) * f('IXYZ') == 1j * f('IXZZ')
    with pytest.raises(ValueError, match='other than `alphaclops.LineQubit'):
        _ = f('III') * alphaclops.X(alphaclops.NamedQubit('tmp'))

    # Mixed types.
    m = alphaclops.MutableDensePauliString
    assert m('X') * m('Z') == -1j * m('Y')
    assert m('X') * f('Z') == -1j * m('Y')
    assert f('X') * m('Z') == -1j * m('Y')
    assert isinstance(f('') * f(''), alphaclops.DensePauliString)
    assert isinstance(m('') * m(''), alphaclops.MutableDensePauliString)
    assert isinstance(m('') * f(''), alphaclops.MutableDensePauliString)
    assert isinstance(f('') * m(''), alphaclops.MutableDensePauliString)

    # Different lengths.
    assert f('I') * f('III') == f('III')
    assert f('X') * f('XXX') == f('IXX')
    assert f('XXX') * f('X') == f('IXX')

    with pytest.raises(TypeError):
        _ = f('I') * object()
    with pytest.raises(TypeError):
        _ = object() * f('I')

    # Unknown number type
    class UnknownNumber(numbers.Number):
        pass

    with pytest.raises(TypeError):
        _ = UnknownNumber() * f('I')


def test_imul():
    f = alphaclops.DensePauliString
    m = alphaclops.MutableDensePauliString

    # Immutable not modified by imul.
    p = f('III')
    p2 = p
    p2 *= 2
    assert p.coefficient == 1
    assert p is not p2

    # Mutable is modified by imul.
    p = m('III')
    p2 = p
    p2 *= 2
    assert p.coefficient == 2
    assert p is p2

    p *= f('X')
    assert p == m('XII', coefficient=2)

    p *= m('XY')
    assert p == m('IYI', coefficient=2)

    p *= 1j
    assert p == m('IYI', coefficient=2j)

    p *= 0.5
    assert p == m('IYI', coefficient=1j)

    p *= alphaclops.X(alphaclops.LineQubit(1))
    assert p == m('IZI')

    with pytest.raises(ValueError, match='smaller than'):
        p *= f('XXXXXXXXXXXX')
    with pytest.raises(TypeError):
        p *= object()

    # Unknown number type
    class UnknownNumber(numbers.Number):
        pass

    with pytest.raises(TypeError):
        p *= UnknownNumber()


def test_pos_neg():
    p = 1j * alphaclops.DensePauliString('XYZ')
    assert +p == p
    assert -p == -1 * p


def test_abs():
    f = alphaclops.DensePauliString
    m = alphaclops.DensePauliString
    assert abs(-f('XX')) == f('XX')
    assert abs(2j * f('XX')) == 2 * f('XX')
    assert abs(2j * m('XX')) == 2 * f('XX')


def test_approx_eq():
    f = alphaclops.DensePauliString
    m = alphaclops.MutableDensePauliString

    # Tolerance matters.
    assert alphaclops.approx_eq(1.00001 * f('X'), f('X'), atol=1e-4)
    assert alphaclops.approx_eq(m('X', coefficient=1.00001), m('X'), atol=1e-4)
    assert not alphaclops.approx_eq(1.00001 * f('X'), f('X'), atol=1e-8)
    assert not alphaclops.approx_eq(1.00001 * m('X'), m('X'), atol=1e-8)

    # Must be same type.
    assert not alphaclops.approx_eq(f('X'), m('X'), atol=1e-4)

    # Differing paulis ignores tolerance.
    assert not alphaclops.approx_eq(f('X'), f('YYY'), atol=1e-8)
    assert not alphaclops.approx_eq(f('X'), f('Y'), atol=1e-8)
    assert not alphaclops.approx_eq(f('X'), f('Y'), atol=500)


def test_pow():
    f = alphaclops.DensePauliString
    m = alphaclops.DensePauliString
    p = 1j * f('IXYZ')
    assert p ** 0 == p ** 4 == p ** 8 == alphaclops.DensePauliString.eye(4)
    assert p**1 == p**5 == p**-3 == p == p**101
    assert p**2 == p**-2 == p**6 == -f('IIII')
    assert p**3 == p**-1 == p**7 == -1j * f('IXYZ')

    p = -f('IXYZ')
    assert p == p**1 == p**-1 == p**-3 == p**-303
    assert p**0 == p**2 == p**-2 == p**-4 == p**102

    p = 2 * f('XX')
    assert p**-1 == (0.5 + 0j) * f('XX')
    assert p**0 == f('II')
    assert p**1 == 2 * f('XX')
    assert p**2 == 4 * f('II')
    assert p**3 == 8 * f('XX')
    assert p**4 == 16 * f('II')

    p = -1j * f('XY')
    assert p**101 == p == p**-103

    p = 2j * f('XY')
    assert (p**-1) ** -1 == p
    assert p**-2 == f('II') / -4

    p = f('XY')
    assert p**-100 == p**0 == p**100 == f('II')
    assert p**-101 == p**1 == p**101 == f('XY')

    # Becomes an immutable copy.
    assert m('X') ** 3 == f('X')


def test_div():
    f = alphaclops.DensePauliString
    t = sympy.Symbol('t')
    assert f('X') / 2 == 0.5 * f('X')
    assert f('X') / t == (1 / t) * f('X')
    with pytest.raises(TypeError):
        _ = f('X') / object()


def test_str():
    f = alphaclops.DensePauliString
    m = alphaclops.MutableDensePauliString

    assert str(f('')) == '+'
    assert str(f('XXX')) == '+XXX'
    assert str(m('XXX')) == '+XXX (mutable)'
    assert str(2 * f('')) == '(2+0j)*'
    assert str((1 + 1j) * f('XXX')) == '(1+1j)*XXX'
    assert str(1j * f('XXX')) == '1j*XXX'
    assert str(-f('IXYZ')) == '-IXYZ'
    assert str(f('XX', coefficient=sympy.Symbol('t') + 2)) == '(t + 2)*XX'
    assert str(f('XX', coefficient=sympy.Symbol('t'))) == 't*XX'


def test_repr():
    f = alphaclops.DensePauliString
    m = alphaclops.MutableDensePauliString
    alphaclops.testing.assert_equivalent_repr(f(''))
    alphaclops.testing.assert_equivalent_repr(-f('X'))
    alphaclops.testing.assert_equivalent_repr(1j * f('XYZII'))
    alphaclops.testing.assert_equivalent_repr(m(''))
    alphaclops.testing.assert_equivalent_repr(-m('X'))
    alphaclops.testing.assert_equivalent_repr(1j * m('XYZII'))
    alphaclops.testing.assert_equivalent_repr(f(coefficient=sympy.Symbol('c'), pauli_mask=[0, 3, 2, 1]))
    alphaclops.testing.assert_equivalent_repr(m(coefficient=sympy.Symbol('c'), pauli_mask=[0, 3, 2, 1]))


def test_one_hot():
    f = alphaclops.DensePauliString
    m = alphaclops.MutableDensePauliString

    assert alphaclops.DensePauliString.one_hot(index=3, length=5, pauli=alphaclops.X) == f('IIIXI')
    assert alphaclops.MutableDensePauliString.one_hot(index=3, length=5, pauli=alphaclops.X) == m('IIIXI')

    assert alphaclops.BaseDensePauliString.one_hot(index=0, length=5, pauli='X') == f('XIIII')
    assert alphaclops.BaseDensePauliString.one_hot(index=0, length=5, pauli='Y') == f('YIIII')
    assert alphaclops.BaseDensePauliString.one_hot(index=0, length=5, pauli='Z') == f('ZIIII')
    assert alphaclops.BaseDensePauliString.one_hot(index=0, length=5, pauli='I') == f('IIIII')
    assert alphaclops.BaseDensePauliString.one_hot(index=0, length=5, pauli=alphaclops.X) == f('XIIII')
    assert alphaclops.BaseDensePauliString.one_hot(index=0, length=5, pauli=alphaclops.Y) == f('YIIII')
    assert alphaclops.BaseDensePauliString.one_hot(index=0, length=5, pauli=alphaclops.Z) == f('ZIIII')
    assert alphaclops.BaseDensePauliString.one_hot(index=0, length=5, pauli=alphaclops.I) == f('IIIII')

    with pytest.raises(IndexError):
        _ = alphaclops.BaseDensePauliString.one_hot(index=50, length=5, pauli=alphaclops.X)

    with pytest.raises(IndexError):
        _ = alphaclops.BaseDensePauliString.one_hot(index=0, length=0, pauli=alphaclops.X)


def test_protocols():
    t = sympy.Symbol('t')
    alphaclops.testing.assert_implements_consistent_protocols(alphaclops.DensePauliString('Y'))
    alphaclops.testing.assert_implements_consistent_protocols(-alphaclops.DensePauliString('Z'))
    alphaclops.testing.assert_implements_consistent_protocols(1j * alphaclops.DensePauliString('X'))
    alphaclops.testing.assert_implements_consistent_protocols(2 * alphaclops.DensePauliString('X'))
    alphaclops.testing.assert_implements_consistent_protocols(
        t * alphaclops.DensePauliString('XYIZ'), ignore_decompose_to_default_gateset=True
    )
    alphaclops.testing.assert_implements_consistent_protocols(
        alphaclops.DensePauliString('XYIZ', coefficient=t + 2), ignore_decompose_to_default_gateset=True
    )
    alphaclops.testing.assert_implements_consistent_protocols(-alphaclops.DensePauliString('XYIZ'))
    alphaclops.testing.assert_implements_consistent_protocols(
        alphaclops.MutableDensePauliString('XYIZ', coefficient=-1)
    )

    # Unitarity and shape.
    assert alphaclops.has_unitary(1j * alphaclops.DensePauliString('X'))
    assert not alphaclops.has_unitary(2j * alphaclops.DensePauliString('X'))
    assert not alphaclops.has_unitary(alphaclops.DensePauliString('X') * t)
    p = -alphaclops.DensePauliString('XYIZ')
    assert alphaclops.num_qubits(p) == len(p) == 4


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_parameterizable(resolve_fn):
    t = sympy.Symbol('t')
    x = alphaclops.DensePauliString('X')
    xt = x * t
    x2 = x * 2
    q = alphaclops.LineQubit(0)
    assert not alphaclops.is_parameterized(x)
    assert not alphaclops.is_parameterized(x * 2)
    assert alphaclops.is_parameterized(x * t)
    assert resolve_fn(xt, {'t': 2}) == x2
    assert resolve_fn(x * 3, {'t': 2}) == x * 3
    assert resolve_fn(xt(q), {'t': 2}).gate == x2
    assert resolve_fn(xt(q).gate, {'t': 2}) == x2


def test_item_immutable():
    p = -alphaclops.DensePauliString('XYIZ')
    assert p[-1] == alphaclops.Z
    assert p[0] == alphaclops.X
    assert p[1] == alphaclops.Y
    assert p[2] == alphaclops.I
    assert p[3] == alphaclops.Z

    with pytest.raises(TypeError):
        _ = p["test"]
    with pytest.raises(IndexError):
        _ = p[4]
    with pytest.raises(TypeError):
        p[2] = alphaclops.X
    with pytest.raises(TypeError):
        p[:] = p

    assert p[:] == abs(p)
    assert p[1:] == alphaclops.DensePauliString('YIZ')
    assert p[::2] == alphaclops.DensePauliString('XI')


def test_item_mutable():
    m = alphaclops.MutableDensePauliString
    p = m('XYIZ', coefficient=-1)
    assert p[-1] == alphaclops.Z
    assert p[0] == alphaclops.X
    assert p[1] == alphaclops.Y
    assert p[2] == alphaclops.I
    assert p[3] == alphaclops.Z
    with pytest.raises(IndexError):
        _ = p[4]
    with pytest.raises(TypeError):
        _ = p["test"]
    with pytest.raises(TypeError):
        p["test"] = 'X'

    p[2] = alphaclops.X
    assert p == m('XYXZ', coefficient=-1)
    p[3] = 'X'
    p[0] = 'I'
    assert p == m('IYXX', coefficient=-1)
    p[2:] = p[:2]
    assert p == m('IYIY', coefficient=-1)
    p[2:] = 'ZZ'
    assert p == m('IYZZ', coefficient=-1)
    p[2:] = 'IY'
    assert p == m('IYIY', coefficient=-1)

    # Aliased views.
    q = p[:2]
    assert q == m('IY')
    q[0] = alphaclops.Z
    assert q == m('ZY')
    assert p == m('ZYIY', coefficient=-1)

    with pytest.raises(ValueError, match='coefficient is not 1'):
        p[:] = p

    assert p[:] == m('ZYIY')
    assert p[1:] == m('YIY')
    assert p[::2] == m('ZI')

    p[2:] = 'XX'
    assert p == m('ZYXX', coefficient=-1)


def test_tensor_product():
    f = alphaclops.DensePauliString
    m = alphaclops.MutableDensePauliString
    assert (2 * f('XX')).tensor_product(-f('XI')) == -2 * f('XXXI')
    assert m('XX', coefficient=2).tensor_product(-f('XI')) == -2 * m('XXXI')
    assert f('XX', coefficient=2).tensor_product(-m('XI')) == -2 * f('XXXI')
    assert m('XX', coefficient=2).tensor_product(m('XI', coefficient=-1)) == -2 * m('XXXI')


def test_commutes():
    f = alphaclops.DensePauliString
    m = alphaclops.MutableDensePauliString

    assert alphaclops.commutes(f('XX'), m('ZZ'))
    assert alphaclops.commutes(2 * f('XX'), m('ZZ', coefficient=3))
    assert alphaclops.commutes(2 * f('IX'), 3 * f('IX'))
    assert not alphaclops.commutes(f('IX'), f('IZ'))
    assert alphaclops.commutes(f('IIIXII'), alphaclops.X(alphaclops.LineQubit(3)))
    assert alphaclops.commutes(f('IIIXII'), alphaclops.X(alphaclops.LineQubit(2)))
    assert not alphaclops.commutes(f('IIIXII'), alphaclops.Z(alphaclops.LineQubit(3)))
    assert alphaclops.commutes(f('IIIXII'), alphaclops.Z(alphaclops.LineQubit(2)))

    assert alphaclops.commutes(f('XX'), "test", default=NotImplemented) is NotImplemented


def test_copy():
    p = -alphaclops.DensePauliString('XYZ')
    m = alphaclops.MutableDensePauliString('XYZ', coefficient=-1)

    # Immutable copies.
    assert p.copy() is p
    assert p.frozen() is p
    assert p.mutable_copy() is not p
    assert p.mutable_copy() == m

    # Mutable copies.
    assert m.copy() is not m
    assert m.copy() == m
    assert m.frozen() == p
    assert m.mutable_copy() is not m
    assert m.mutable_copy() == m

    # Copy immutable with modifications.
    assert p.copy(coefficient=-1) is p
    assert p.copy(coefficient=-2) is not p
    assert p.copy(coefficient=-2) == -2 * alphaclops.DensePauliString('XYZ')
    assert p.copy(coefficient=-2, pauli_mask=[3]) == -2 * alphaclops.DensePauliString('Z')

    # Copy mutable with modifications.
    assert m.copy(coefficient=-1) is not m
    assert m.copy(coefficient=-2) is not m
    assert m.copy(coefficient=-2) == alphaclops.MutableDensePauliString('XYZ', coefficient=-2)
    assert m.copy(coefficient=-2, pauli_mask=[2]) == alphaclops.MutableDensePauliString(
        'Y', coefficient=-2
    )

    # Aliasing of the mask attribute when copying with modifications.
    mask = np.array([1, 2, 3], dtype=np.uint8)
    assert alphaclops.MutableDensePauliString(mask).copy().pauli_mask is not mask
    assert alphaclops.MutableDensePauliString(mask).copy(pauli_mask=mask).pauli_mask is mask
    assert alphaclops.MutableDensePauliString('XYZ').copy(pauli_mask=mask).pauli_mask is mask


def test_gaussian_elimination():
    def table(*rows: str) -> List[alphaclops.MutableDensePauliString]:
        coefs = {'i': 1j, '-': -1, '+': 1}
        return [
            alphaclops.MutableDensePauliString(row[1:].replace('.', 'I'), coefficient=coefs[row[0]])
            for row in rows
        ]

    f = alphaclops.MutableDensePauliString.inline_gaussian_elimination

    t = table()
    f(t)
    assert t == table()

    t = table('+X')
    f(t)
    assert t == table('+X')

    t = table("+.X.X", "+Z.Z.", "+X.XX", "+ZZ.Z")
    f(t)
    assert t == table("+X.XX", "+Z.Z.", "+.X.X", "+.ZZZ")

    t = table("+XXX", "+YYY")
    f(t)
    assert t == table("+XXX", "iZZZ")

    t = table("+XXXX", "+X...", "+..ZZ", "+.ZZ.")
    f(t)
    assert t == table("+X...", "+.XXX", "+.Z.Z", "+..ZZ")

    t = table(
        '+ZZZ.........',
        '+XX..........',
        '+X.X.........',
        '+...ZZZ......',
        '+...XX.......',
        '+...X.X......',
        '+......ZZ....',
        '+......XX....',
        '+........ZZ..',
        '+........XX..',
        '+..X....X....',
        '+..Z....Z....',
        '+.....X..X...',
        '+.....Z..Z...',
        '+.X........X.',
        '+.Z........Z.',
        '-X...X.......',
        '+Z...Z.......',
        '+...X.......X',
        '+...Z.......Z',
        '+......X..X..',
        '+......Z..Z..',
    )
    f(t)
    assert t == table(
        '-X..........X',
        '+Z........Z.Z',
        '-.X.........X',
        '+.Z.........Z',
        '-..X........X',
        '+..Z......Z..',
        '+...X.......X',
        '+...Z.......Z',
        '+....X......X',
        '+....Z....Z.Z',
        '+.....X.....X',
        '+.....Z...Z..',
        '-......X....X',
        '+......Z..Z..',
        '-.......X...X',
        '+.......Z.Z..',
        '+........X..X',
        '+........ZZ..',
        '+.........X.X',
        '-..........XX',
        '+..........ZZ',
        '-............',
    )


def test_idiv():
    p = alphaclops.MutableDensePauliString('XYZ', coefficient=2)
    p /= 2
    assert p == alphaclops.MutableDensePauliString('XYZ')

    with pytest.raises(TypeError):
        p /= object()


def test_symbolic():
    t = sympy.Symbol('t')
    r = sympy.Symbol('r')
    m = alphaclops.MutableDensePauliString('XYZ', coefficient=t)
    f = alphaclops.DensePauliString('XYZ', coefficient=t)
    assert f * r == alphaclops.DensePauliString('XYZ', coefficient=t * r)
    assert m * r == alphaclops.MutableDensePauliString('XYZ', coefficient=t * r)
    m *= r
    f *= r
    assert m == alphaclops.MutableDensePauliString('XYZ', coefficient=t * r)
    assert f == alphaclops.DensePauliString('XYZ', coefficient=t * r)
    m /= r
    f /= r
    assert m == alphaclops.MutableDensePauliString('XYZ', coefficient=t)
    assert f == alphaclops.DensePauliString('XYZ', coefficient=t)
