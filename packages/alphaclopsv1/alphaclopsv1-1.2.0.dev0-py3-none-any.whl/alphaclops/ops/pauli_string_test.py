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
import math
from typing import List

import numpy as np
import pytest
import sympy

import alphaclops
import alphaclops.testing


def _make_qubits(n):
    return [alphaclops.NamedQubit(f'q{i}') for i in range(n)]


def _sample_qubit_pauli_maps():
    """All combinations of having a Pauli or nothing on 3 qubits.
    Yields 64 qubit pauli maps
    """
    qubits = _make_qubits(3)
    paulis_or_none = (None, alphaclops.X, alphaclops.Y, alphaclops.Z)
    for paulis in itertools.product(paulis_or_none, repeat=len(qubits)):
        yield {qubit: pauli for qubit, pauli in zip(qubits, paulis) if pauli is not None}


def _small_sample_qubit_pauli_maps():
    """A few representative samples of qubit maps.

    Only tests 10 combinations of Paulis to speed up testing.
    """
    qubits = _make_qubits(3)
    yield {}
    yield {qubits[0]: alphaclops.X}
    yield {qubits[1]: alphaclops.X}
    yield {qubits[2]: alphaclops.X}
    yield {qubits[1]: alphaclops.Z}

    yield {qubits[0]: alphaclops.Y, qubits[1]: alphaclops.Z}
    yield {qubits[1]: alphaclops.Z, qubits[2]: alphaclops.X}
    yield {qubits[0]: alphaclops.X, qubits[1]: alphaclops.X, qubits[2]: alphaclops.X}
    yield {qubits[0]: alphaclops.X, qubits[1]: alphaclops.Y, qubits[2]: alphaclops.Z}
    yield {qubits[0]: alphaclops.Z, qubits[1]: alphaclops.X, qubits[2]: alphaclops.Y}


def test_eq_ne_hash():
    q0, q1, q2 = _make_qubits(3)
    eq = alphaclops.testing.EqualsTester()
    eq.make_equality_group(
        lambda: alphaclops.PauliString(),
        lambda: alphaclops.PauliString(qubit_pauli_map={}),
        lambda: alphaclops.PauliString(qubit_pauli_map={}, coefficient=+1),
    )
    eq.add_equality_group(alphaclops.PauliString(qubit_pauli_map={}, coefficient=-1))
    for q, pauli in itertools.product((q0, q1), (alphaclops.X, alphaclops.Y, alphaclops.Z)):
        eq.add_equality_group(alphaclops.PauliString(qubit_pauli_map={q: pauli}, coefficient=+1))
        eq.add_equality_group(alphaclops.PauliString(qubit_pauli_map={q: pauli}, coefficient=-1))
    for q, p0, p1 in itertools.product(
        (q0, q1), (alphaclops.X, alphaclops.Y, alphaclops.Z), (alphaclops.X, alphaclops.Y, alphaclops.Z)
    ):
        eq.add_equality_group(alphaclops.PauliString(qubit_pauli_map={q: p0, q2: p1}, coefficient=+1))


def test_equal_up_to_coefficient():
    (q0,) = _make_qubits(1)
    assert alphaclops.PauliString({}, +1).equal_up_to_coefficient(alphaclops.PauliString({}, +1))
    assert alphaclops.PauliString({}, -1).equal_up_to_coefficient(alphaclops.PauliString({}, -1))
    assert alphaclops.PauliString({}, +1).equal_up_to_coefficient(alphaclops.PauliString({}, -1))
    assert alphaclops.PauliString({}, +1).equal_up_to_coefficient(alphaclops.PauliString({}, 2j))

    assert alphaclops.PauliString({q0: alphaclops.X}, +1).equal_up_to_coefficient(
        alphaclops.PauliString({q0: alphaclops.X}, +1)
    )
    assert alphaclops.PauliString({q0: alphaclops.X}, -1).equal_up_to_coefficient(
        alphaclops.PauliString({q0: alphaclops.X}, -1)
    )
    assert alphaclops.PauliString({q0: alphaclops.X}, +1).equal_up_to_coefficient(
        alphaclops.PauliString({q0: alphaclops.X}, -1)
    )

    assert not alphaclops.PauliString({q0: alphaclops.X}, +1).equal_up_to_coefficient(
        alphaclops.PauliString({q0: alphaclops.Y}, +1)
    )
    assert not alphaclops.PauliString({q0: alphaclops.X}, +1).equal_up_to_coefficient(
        alphaclops.PauliString({q0: alphaclops.Y}, 1j)
    )
    assert not alphaclops.PauliString({q0: alphaclops.X}, -1).equal_up_to_coefficient(
        alphaclops.PauliString({q0: alphaclops.Y}, -1)
    )
    assert not alphaclops.PauliString({q0: alphaclops.X}, +1).equal_up_to_coefficient(
        alphaclops.PauliString({q0: alphaclops.Y}, -1)
    )

    assert not alphaclops.PauliString({q0: alphaclops.X}, +1).equal_up_to_coefficient(alphaclops.PauliString({}, +1))
    assert not alphaclops.PauliString({q0: alphaclops.X}, -1).equal_up_to_coefficient(alphaclops.PauliString({}, -1))
    assert not alphaclops.PauliString({q0: alphaclops.X}, +1).equal_up_to_coefficient(alphaclops.PauliString({}, -1))


def test_exponentiation_as_exponent():
    a, b = alphaclops.LineQubit.range(2)
    p = alphaclops.PauliString({a: alphaclops.X, b: alphaclops.Y})

    with pytest.raises(NotImplementedError, match='non-Hermitian'):
        _ = math.e ** (math.pi * p)

    with pytest.raises(TypeError, match='unsupported'):
        _ = 'test' ** p

    assert alphaclops.approx_eq(
        math.e ** (-0.5j * math.pi * p),
        alphaclops.PauliStringPhasor(p, exponent_neg=0.5, exponent_pos=-0.5),
    )

    assert alphaclops.approx_eq(
        math.e ** (0.25j * math.pi * p),
        alphaclops.PauliStringPhasor(p, exponent_neg=-0.25, exponent_pos=0.25),
    )

    assert alphaclops.approx_eq(
        2 ** (0.25j * math.pi * p),
        alphaclops.PauliStringPhasor(
            p, exponent_neg=-0.25 * math.log(2), exponent_pos=0.25 * math.log(2)
        ),
    )

    assert alphaclops.approx_eq(
        np.exp(0.25j * math.pi * p),
        alphaclops.PauliStringPhasor(p, exponent_neg=-0.25, exponent_pos=0.25),
    )


def test_exponentiate_single_value_as_exponent():
    q = alphaclops.LineQubit(0)

    assert alphaclops.approx_eq(math.e ** (-0.125j * math.pi * alphaclops.X(q)), alphaclops.rx(0.25 * math.pi).on(q))

    assert alphaclops.approx_eq(math.e ** (-0.125j * math.pi * alphaclops.Y(q)), alphaclops.ry(0.25 * math.pi).on(q))

    assert alphaclops.approx_eq(math.e ** (-0.125j * math.pi * alphaclops.Z(q)), alphaclops.rz(0.25 * math.pi).on(q))

    assert alphaclops.approx_eq(np.exp(-0.15j * math.pi * alphaclops.X(q)), alphaclops.rx(0.3 * math.pi).on(q))

    assert alphaclops.approx_eq(alphaclops.X(q) ** 0.5, alphaclops.XPowGate(exponent=0.5).on(q))

    assert alphaclops.approx_eq(alphaclops.Y(q) ** 0.5, alphaclops.YPowGate(exponent=0.5).on(q))

    assert alphaclops.approx_eq(alphaclops.Z(q) ** 0.5, alphaclops.ZPowGate(exponent=0.5).on(q))


def test_exponentiation_as_base():
    a, b = alphaclops.LineQubit.range(2)
    p = alphaclops.PauliString({a: alphaclops.X, b: alphaclops.Y})

    with pytest.raises(TypeError, match='unsupported'):
        _ = (2 * p) ** 5

    with pytest.raises(TypeError, match='unsupported'):
        _ = p ** 'test'

    with pytest.raises(TypeError, match='unsupported'):
        _ = p**1j

    assert p**-1 == p

    assert alphaclops.approx_eq(p ** 0.5, alphaclops.PauliStringPhasor(p, exponent_neg=0.5, exponent_pos=0))

    assert alphaclops.approx_eq(p ** -0.5, alphaclops.PauliStringPhasor(p, exponent_neg=-0.5, exponent_pos=0))

    assert alphaclops.approx_eq(
        math.e ** (0.25j * math.pi * p),
        alphaclops.PauliStringPhasor(p, exponent_neg=-0.25, exponent_pos=0.25),
    )

    assert alphaclops.approx_eq(
        2 ** (0.25j * math.pi * p),
        alphaclops.PauliStringPhasor(
            p, exponent_neg=-0.25 * math.log(2), exponent_pos=0.25 * math.log(2)
        ),
    )

    assert alphaclops.approx_eq(
        np.exp(0.25j * math.pi * p),
        alphaclops.PauliStringPhasor(p, exponent_neg=-0.25, exponent_pos=0.25),
    )

    np.testing.assert_allclose(
        alphaclops.unitary(np.exp(0.5j * math.pi * alphaclops.Z(a))),
        np.diag([np.exp(0.5j * math.pi), np.exp(-0.5j * math.pi)]),
        atol=1e-8,
    )


@pytest.mark.parametrize('pauli', (alphaclops.X, alphaclops.Y, alphaclops.Z))
def test_list_op_constructor_matches_mapping(pauli):
    (q0,) = _make_qubits(1)
    op = pauli.on(q0)
    assert alphaclops.PauliString([op]) == alphaclops.PauliString({q0: pauli})


def test_constructor_flexibility():
    a, b = alphaclops.LineQubit.range(2)
    with pytest.raises(TypeError, match='alphaclops.PAULI_STRING_LIKE'):
        _ = alphaclops.PauliString(alphaclops.CZ(a, b))
    with pytest.raises(TypeError, match='alphaclops.PAULI_STRING_LIKE'):
        _ = alphaclops.PauliString('test')
    with pytest.raises(TypeError, match='S is not a Pauli'):
        _ = alphaclops.PauliString(qubit_pauli_map={a: alphaclops.S})
    with pytest.raises(TypeError, match="alphaclops.PAULI_STRING_LIKE"):
        _ = alphaclops.PauliString(alphaclops.Z(a) + alphaclops.Z(b))

    assert alphaclops.PauliString(alphaclops.X(a)) == alphaclops.PauliString(qubit_pauli_map={a: alphaclops.X})
    assert alphaclops.PauliString([alphaclops.X(a)]) == alphaclops.PauliString(qubit_pauli_map={a: alphaclops.X})
    assert alphaclops.PauliString([[[alphaclops.X(a)]]]) == alphaclops.PauliString(qubit_pauli_map={a: alphaclops.X})
    assert alphaclops.PauliString([[[alphaclops.I(a)]]]) == alphaclops.PauliString()

    assert alphaclops.PauliString(1, 2, 3, alphaclops.X(a), alphaclops.Y(a)) == alphaclops.PauliString(
        qubit_pauli_map={a: alphaclops.Z}, coefficient=6j
    )

    assert alphaclops.PauliString(alphaclops.X(a), alphaclops.X(a)) == alphaclops.PauliString()
    assert alphaclops.PauliString(alphaclops.X(a), alphaclops.X(b)) == alphaclops.PauliString(
        qubit_pauli_map={a: alphaclops.X, b: alphaclops.X}
    )

    assert alphaclops.PauliString(0) == alphaclops.PauliString(coefficient=0)

    assert alphaclops.PauliString(1, 2, 3, {a: alphaclops.X}, alphaclops.Y(a)) == alphaclops.PauliString(
        qubit_pauli_map={a: alphaclops.Z}, coefficient=6j
    )


@pytest.mark.parametrize('qubit_pauli_map', _sample_qubit_pauli_maps())
def test_getitem(qubit_pauli_map):
    other = alphaclops.NamedQubit('other')
    pauli_string = alphaclops.PauliString(qubit_pauli_map=qubit_pauli_map)
    for key in qubit_pauli_map:
        assert qubit_pauli_map[key] == pauli_string[key]
    with pytest.raises(KeyError):
        _ = qubit_pauli_map[other]
    with pytest.raises(KeyError):
        _ = pauli_string[other]


@pytest.mark.parametrize('qubit_pauli_map', _sample_qubit_pauli_maps())
def test_get(qubit_pauli_map):
    other = alphaclops.NamedQubit('other')
    pauli_string = alphaclops.PauliString(qubit_pauli_map)
    for key in qubit_pauli_map:
        assert qubit_pauli_map.get(key) == pauli_string.get(key)
    assert qubit_pauli_map.get(other) is None
    assert pauli_string.get(other) is None
    # pylint: disable=too-many-function-args
    assert qubit_pauli_map.get(other, 5) == pauli_string.get(other, 5) == 5
    # pylint: enable=too-many-function-args


@pytest.mark.parametrize('qubit_pauli_map', _sample_qubit_pauli_maps())
def test_contains(qubit_pauli_map):
    other = alphaclops.NamedQubit('other')
    pauli_string = alphaclops.PauliString(qubit_pauli_map)
    for key in qubit_pauli_map:
        assert key in pauli_string
    assert other not in pauli_string


@pytest.mark.parametrize('qubit_pauli_map', _sample_qubit_pauli_maps())
def test_basic_functionality(qubit_pauli_map):
    pauli_string = alphaclops.PauliString(qubit_pauli_map)
    # Test items
    assert len(qubit_pauli_map.items()) == len(pauli_string.items())
    assert set(qubit_pauli_map.items()) == set(pauli_string.items())

    # Test values
    assert len(qubit_pauli_map.values()) == len(pauli_string.values())
    assert set(qubit_pauli_map.values()) == set(pauli_string.values())

    # Test length
    assert len(qubit_pauli_map) == len(pauli_string)

    # Test keys
    assert len(qubit_pauli_map.keys()) == len(pauli_string.keys()) == len(pauli_string.qubits)
    assert set(qubit_pauli_map.keys()) == set(pauli_string.keys()) == set(pauli_string.qubits)

    # Test iteration
    assert len(tuple(qubit_pauli_map)) == len(tuple(pauli_string))
    assert set(tuple(qubit_pauli_map)) == set(tuple(pauli_string))


def test_repr():
    q0, q1, q2 = _make_qubits(3)
    pauli_string = alphaclops.PauliString({q2: alphaclops.X, q1: alphaclops.Y, q0: alphaclops.Z})
    alphaclops.testing.assert_equivalent_repr(pauli_string)
    alphaclops.testing.assert_equivalent_repr(-pauli_string)
    alphaclops.testing.assert_equivalent_repr(1j * pauli_string)
    alphaclops.testing.assert_equivalent_repr(2 * pauli_string)
    alphaclops.testing.assert_equivalent_repr(alphaclops.PauliString())


def test_repr_preserves_qubit_order():
    q0, q1, q2 = _make_qubits(3)
    pauli_string = alphaclops.PauliString({q2: alphaclops.X, q1: alphaclops.Y, q0: alphaclops.Z})
    assert eval(repr(pauli_string)).qubits == pauli_string.qubits

    pauli_string = alphaclops.PauliString(alphaclops.X(q2), alphaclops.Y(q1), alphaclops.Z(q0))
    assert eval(repr(pauli_string)).qubits == pauli_string.qubits

    pauli_string = alphaclops.PauliString(alphaclops.Z(q0), alphaclops.Y(q1), alphaclops.X(q2))
    assert eval(repr(pauli_string)).qubits == pauli_string.qubits


def test_repr_coefficient_of_one():
    pauli_string = alphaclops.Z(alphaclops.LineQubit(0)) * 1
    assert type(pauli_string) == type(eval(repr(pauli_string)))
    alphaclops.testing.assert_equivalent_repr(pauli_string)


def test_str():
    q0, q1, q2 = _make_qubits(3)
    pauli_string = alphaclops.PauliString({q2: alphaclops.X, q1: alphaclops.Y, q0: alphaclops.Z})
    assert str(alphaclops.PauliString({})) == 'I'
    assert str(-alphaclops.PauliString({})) == '-I'
    assert str(pauli_string) == 'Z(q0)*Y(q1)*X(q2)'
    assert str(-pauli_string) == '-Z(q0)*Y(q1)*X(q2)'
    assert str(1j * pauli_string) == '1j*Z(q0)*Y(q1)*X(q2)'
    assert str(pauli_string * -1j) == '-1j*Z(q0)*Y(q1)*X(q2)'


@pytest.mark.parametrize(
    'map1,map2,out',
    (
        lambda q0, q1, q2: (
            ({}, {}, {}),
            ({q0: alphaclops.X}, {q0: alphaclops.Y}, {q0: (alphaclops.X, alphaclops.Y)}),
            ({q0: alphaclops.X}, {q1: alphaclops.X}, {}),
            ({q0: alphaclops.Y, q1: alphaclops.Z}, {q1: alphaclops.Y, q2: alphaclops.X}, {q1: (alphaclops.Z, alphaclops.Y)}),
            ({q0: alphaclops.X, q1: alphaclops.Y, q2: alphaclops.Z}, {}, {}),
            (
                {q0: alphaclops.X, q1: alphaclops.Y, q2: alphaclops.Z},
                {q0: alphaclops.Y, q1: alphaclops.Z},
                {q0: (alphaclops.X, alphaclops.Y), q1: (alphaclops.Y, alphaclops.Z)},
            ),
        )
    )(*_make_qubits(3)),
)
def test_zip_items(map1, map2, out):
    ps1 = alphaclops.PauliString(map1)
    ps2 = alphaclops.PauliString(map2)
    out_actual = tuple(ps1.zip_items(ps2))
    assert len(out_actual) == len(out)
    assert dict(out_actual) == out


@pytest.mark.parametrize(
    'map1,map2,out',
    (
        lambda q0, q1, q2: (
            ({}, {}, ()),
            ({q0: alphaclops.X}, {q0: alphaclops.Y}, ((alphaclops.X, alphaclops.Y),)),
            ({q0: alphaclops.X}, {q1: alphaclops.X}, ()),
            ({q0: alphaclops.Y, q1: alphaclops.Z}, {q1: alphaclops.Y, q2: alphaclops.X}, ((alphaclops.Z, alphaclops.Y),)),
            ({q0: alphaclops.X, q1: alphaclops.Y, q2: alphaclops.Z}, {}, ()),
            (
                {q0: alphaclops.X, q1: alphaclops.Y, q2: alphaclops.Z},
                {q0: alphaclops.Y, q1: alphaclops.Z},
                # Order not necessary
                ((alphaclops.X, alphaclops.Y), (alphaclops.Y, alphaclops.Z)),
            ),
        )
    )(*_make_qubits(3)),
)
def test_zip_paulis(map1, map2, out):
    ps1 = alphaclops.PauliString(map1)
    ps2 = alphaclops.PauliString(map2)
    out_actual = tuple(ps1.zip_paulis(ps2))
    assert len(out_actual) == len(out)
    if len(out) <= 1:
        assert out_actual == out
    assert set(out_actual) == set(out)  # Ignore output order


def test_commutes():
    qubits = _make_qubits(3)

    ps1 = alphaclops.PauliString([alphaclops.X(qubits[0])])
    with pytest.raises(TypeError):
        alphaclops.commutes(ps1, 'X')
    assert alphaclops.commutes(ps1, 'X', default='default') == 'default'
    for A, commutes in [(alphaclops.X, True), (alphaclops.Y, False)]:
        assert alphaclops.commutes(ps1, alphaclops.PauliString([A(qubits[0])])) == commutes
        assert alphaclops.commutes(ps1, alphaclops.PauliString([A(qubits[1])]))

    ps1 = alphaclops.PauliString(dict(zip(qubits, (alphaclops.X, alphaclops.Y))))

    for paulis, commutes in {
        (alphaclops.X, alphaclops.Y): True,
        (alphaclops.X, alphaclops.Z): False,
        (alphaclops.Y, alphaclops.X): True,
        (alphaclops.Y, alphaclops.Z): True,
        (alphaclops.X, alphaclops.Y, alphaclops.Z): True,
        (alphaclops.X, alphaclops.Z, alphaclops.Z): False,
        (alphaclops.Y, alphaclops.X, alphaclops.Z): True,
        (alphaclops.Y, alphaclops.Z, alphaclops.X): True,
    }.items():
        ps2 = alphaclops.PauliString(dict(zip(qubits, paulis)))
        assert alphaclops.commutes(ps1, ps2) == commutes

    for paulis, commutes in {
        (alphaclops.Y, alphaclops.X): True,
        (alphaclops.Z, alphaclops.X): False,
        (alphaclops.X, alphaclops.Y): False,
        (alphaclops.Z, alphaclops.Y): False,
    }.items():
        ps2 = alphaclops.PauliString(dict(zip(qubits[1:], paulis)))
        assert alphaclops.commutes(ps1, ps2) == commutes


def test_negate():
    q0, q1 = _make_qubits(2)
    qubit_pauli_map = {q0: alphaclops.X, q1: alphaclops.Y}
    ps1 = alphaclops.PauliString(qubit_pauli_map)
    ps2 = alphaclops.PauliString(qubit_pauli_map, -1)
    assert -ps1 == ps2
    assert ps1 == -ps2
    neg_ps1 = -ps1
    assert -neg_ps1 == ps1

    m = ps1.mutable_copy()
    assert -m == -1 * m
    assert -m is not m
    assert isinstance(-m, alphaclops.MutablePauliString)


def test_mul_scalar():
    a, b = alphaclops.LineQubit.range(2)
    p = alphaclops.PauliString({a: alphaclops.X, b: alphaclops.Y})
    assert -p == -1 * p == -1.0 * p == p * -1 == p * complex(-1)
    assert -p != 1j * p
    assert +p == 1 * p

    assert p * alphaclops.I(a) == p
    assert alphaclops.I(a) * p == p

    with pytest.raises(TypeError, match="sequence by non-int of type 'PauliString'"):
        _ = p * 'test'
    with pytest.raises(TypeError, match="sequence by non-int of type 'PauliString'"):
        _ = 'test' * p


def test_div_scalar():
    a, b = alphaclops.LineQubit.range(2)
    p = alphaclops.PauliString({a: alphaclops.X, b: alphaclops.Y})
    assert -p == p / -1 == p / -1.0 == p / (-1 + 0j)
    assert -p != p / 1j
    assert +p == p / 1
    assert p * 2 == p / 0.5
    with pytest.raises(TypeError):
        _ = p / 'test'
    with pytest.raises(TypeError):
        # noinspection PyUnresolvedReferences
        _ = 'test' / p


def test_mul_strings():
    a, b, c, d = alphaclops.LineQubit.range(4)
    p1 = alphaclops.PauliString({a: alphaclops.X, b: alphaclops.Y, c: alphaclops.Z})
    p2 = alphaclops.PauliString({b: alphaclops.X, c: alphaclops.Y, d: alphaclops.Z})
    assert p1 * p2 == -alphaclops.PauliString({a: alphaclops.X, b: alphaclops.Z, c: alphaclops.X, d: alphaclops.Z})

    assert alphaclops.X(a) * alphaclops.PauliString({a: alphaclops.X}) == alphaclops.PauliString()
    assert alphaclops.PauliString({a: alphaclops.X}) * alphaclops.X(a) == alphaclops.PauliString()
    assert alphaclops.X(a) * alphaclops.X(a) == alphaclops.PauliString()
    assert -alphaclops.X(a) * -alphaclops.X(a) == alphaclops.PauliString()

    with pytest.raises(TypeError, match='unsupported'):
        _ = alphaclops.X(a) * object()
    with pytest.raises(TypeError, match='unsupported'):
        # noinspection PyUnresolvedReferences
        _ = object() * alphaclops.X(a)
    assert -alphaclops.X(a) == -alphaclops.PauliString({a: alphaclops.X})


def test_op_equivalence():
    a, b = alphaclops.LineQubit.range(2)
    various_x = [
        alphaclops.X(a),
        alphaclops.PauliString({a: alphaclops.X}),
        alphaclops.PauliString([alphaclops.X.on(a)]),
        alphaclops.SingleQubitPauliStringGateOperation(alphaclops.X, a),
        alphaclops.GateOperation(alphaclops.X, [a]),
    ]

    for x in various_x:
        alphaclops.testing.assert_equivalent_repr(x)

    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(*various_x)
    eq.add_equality_group(alphaclops.Y(a), alphaclops.PauliString({a: alphaclops.Y}))
    eq.add_equality_group(-alphaclops.PauliString({a: alphaclops.X}))
    eq.add_equality_group(alphaclops.Z(a), alphaclops.PauliString({a: alphaclops.Z}))
    eq.add_equality_group(alphaclops.Z(b), alphaclops.PauliString({b: alphaclops.Z}))


def test_op_product():
    a, b = alphaclops.LineQubit.range(2)

    assert alphaclops.X(a) * alphaclops.X(b) == alphaclops.PauliString({a: alphaclops.X, b: alphaclops.X})
    assert alphaclops.X(a) * alphaclops.Y(b) == alphaclops.PauliString({a: alphaclops.X, b: alphaclops.Y})
    assert alphaclops.Z(a) * alphaclops.Y(b) == alphaclops.PauliString({a: alphaclops.Z, b: alphaclops.Y})

    assert alphaclops.X(a) * alphaclops.X(a) == alphaclops.PauliString()
    assert alphaclops.X(a) * alphaclops.Y(a) == 1j * alphaclops.PauliString({a: alphaclops.Z})
    assert alphaclops.Y(a) * alphaclops.Z(b) * alphaclops.X(a) == -1j * alphaclops.PauliString({a: alphaclops.Z, b: alphaclops.Z})


def test_pos():
    q0, q1 = _make_qubits(2)
    qubit_pauli_map = {q0: alphaclops.X, q1: alphaclops.Y}
    ps1 = alphaclops.PauliString(qubit_pauli_map)
    assert ps1 == +ps1

    m = ps1.mutable_copy()
    assert +m == m
    assert +m is not m
    assert isinstance(+m, alphaclops.MutablePauliString)


def test_pow():
    a, b = alphaclops.LineQubit.range(2)

    assert alphaclops.PauliString({a: alphaclops.X}) ** 0.25 == alphaclops.X(a) ** 0.25
    assert alphaclops.PauliString({a: alphaclops.Y}) ** 0.25 == alphaclops.Y(a) ** 0.25
    assert alphaclops.PauliString({a: alphaclops.Z}) ** 0.25 == alphaclops.Z(a) ** 0.25

    p = alphaclops.PauliString({a: alphaclops.X, b: alphaclops.Y})
    assert p**1 == p
    assert p**-1 == p
    assert (-p) ** 1 == -p
    assert (-p) ** -1 == -p
    assert (1j * p) ** 1 == 1j * p
    assert (1j * p) ** -1 == -1j * p


def test_rpow():
    a, b = alphaclops.LineQubit.range(2)

    u = alphaclops.unitary(np.exp(1j * np.pi / 2 * alphaclops.Z(a) * alphaclops.Z(b)))
    np.testing.assert_allclose(u, np.diag([1j, -1j, -1j, 1j]), atol=1e-8)

    u = alphaclops.unitary(np.exp(-1j * np.pi / 4 * alphaclops.Z(a) * alphaclops.Z(b)))
    alphaclops.testing.assert_allclose_up_to_global_phase(u, np.diag([1, 1j, 1j, 1]), atol=1e-8)

    u = alphaclops.unitary(np.e ** (1j * np.pi * alphaclops.Z(a) * alphaclops.Z(b)))
    np.testing.assert_allclose(u, np.diag([-1, -1, -1, -1]), atol=1e-8)


def test_numpy_ufunc():
    with pytest.raises(TypeError, match="returned NotImplemented"):
        _ = np.sin(alphaclops.PauliString())
    with pytest.raises(NotImplementedError, match="non-Hermitian"):
        _ = np.exp(alphaclops.PauliString())
    x = np.exp(1j * np.pi * alphaclops.PauliString())
    assert x is not None


def test_map_qubits():
    a, b = (alphaclops.NamedQubit(name) for name in 'ab')
    q0, q1 = _make_qubits(2)
    qubit_pauli_map1 = {a: alphaclops.X, b: alphaclops.Y}
    qubit_pauli_map2 = {q0: alphaclops.X, q1: alphaclops.Y}
    qubit_map = {a: q0, b: q1}
    ps1 = alphaclops.PauliString(qubit_pauli_map1)
    ps2 = alphaclops.PauliString(qubit_pauli_map2)
    assert ps1.map_qubits(qubit_map) == ps2


def test_map_qubits_raises():
    q = alphaclops.LineQubit.range(3)
    pauli_string = alphaclops.X(q[0]) * alphaclops.Y(q[1]) * alphaclops.Z(q[2])
    with pytest.raises(ValueError, match='must have a key for every qubit'):
        pauli_string.map_qubits({q[0]: q[1]})


def test_to_z_basis_ops():
    x0 = np.array([1, 1]) / np.sqrt(2)
    x1 = np.array([1, -1]) / np.sqrt(2)
    y0 = np.array([1, 1j]) / np.sqrt(2)
    y1 = np.array([1, -1j]) / np.sqrt(2)
    z0 = np.array([1, 0])
    z1 = np.array([0, 1])

    q0, q1, q2, q3, q4, q5 = _make_qubits(6)
    pauli_string = alphaclops.PauliString(
        {q0: alphaclops.X, q1: alphaclops.X, q2: alphaclops.Y, q3: alphaclops.Y, q4: alphaclops.Z, q5: alphaclops.Z}
    )
    circuit = alphaclops.Circuit(pauli_string.to_z_basis_ops())

    initial_state = alphaclops.kron(x0, x1, y0, y1, z0, z1, shape_len=1)
    z_basis_state = circuit.final_state_vector(
        initial_state=initial_state, ignore_terminal_measurements=False, dtype=np.complex64
    )

    expected_state = np.zeros(2**6)
    expected_state[0b010101] = 1

    alphaclops.testing.assert_allclose_up_to_global_phase(
        z_basis_state, expected_state, rtol=1e-7, atol=1e-7
    )


def test_to_z_basis_ops_product_state():
    q0, q1, q2, q3, q4, q5 = _make_qubits(6)
    pauli_string = alphaclops.PauliString(
        {q0: alphaclops.X, q1: alphaclops.X, q2: alphaclops.Y, q3: alphaclops.Y, q4: alphaclops.Z, q5: alphaclops.Z}
    )
    circuit = alphaclops.Circuit(pauli_string.to_z_basis_ops())

    initial_state = (
            alphaclops.KET_PLUS(q0)
            * alphaclops.KET_MINUS(q1)
            * alphaclops.KET_IMAG(q2)
            * alphaclops.KET_MINUS_IMAG(q3)
            * alphaclops.KET_ZERO(q4)
            * alphaclops.KET_ONE(q5)
    )
    z_basis_state = circuit.final_state_vector(
        initial_state=initial_state, ignore_terminal_measurements=False, dtype=np.complex64
    )

    expected_state = np.zeros(2**6)
    expected_state[0b010101] = 1

    alphaclops.testing.assert_allclose_up_to_global_phase(
        z_basis_state, expected_state, rtol=1e-7, atol=1e-7
    )


def _assert_pass_over(ops: List[alphaclops.Operation], before: alphaclops.PauliString, after: alphaclops.PauliString):
    assert before.pass_operations_over(ops[::-1]) == after
    assert after.pass_operations_over(ops, after_to_before=True) == before


@pytest.mark.parametrize('shift,sign', itertools.product(range(3), (-1, +1)))
def test_pass_operations_over_single(shift: int, sign: int):
    q0, q1 = _make_qubits(2)
    X, Y, Z = (alphaclops.Pauli.by_relative_index(pauli, shift) for pauli in (alphaclops.X, alphaclops.Y, alphaclops.Z))

    op0 = alphaclops.SingleQubitCliffordGate.from_pauli(Y)(q1)
    ps_before: alphaclops.PauliString[alphaclops.Qid] = alphaclops.PauliString({q0: X}, sign)
    ps_after = ps_before
    _assert_pass_over([op0], ps_before, ps_after)

    op0 = alphaclops.SingleQubitCliffordGate.from_pauli(X)(q0)
    op1 = alphaclops.SingleQubitCliffordGate.from_pauli(Y)(q1)
    ps_before = alphaclops.PauliString({q0: X, q1: Y}, sign)
    ps_after = ps_before
    _assert_pass_over([op0, op1], ps_before, ps_after)

    op0 = alphaclops.SingleQubitCliffordGate.from_double_map({Z: (X, False), X: (Z, False)})(q0)
    ps_before = alphaclops.PauliString({q0: X, q1: Y}, sign)
    ps_after = alphaclops.PauliString({q0: Z, q1: Y}, sign)
    _assert_pass_over([op0], ps_before, ps_after)

    op1 = alphaclops.SingleQubitCliffordGate.from_pauli(X)(q1)
    ps_before = alphaclops.PauliString({q0: X, q1: Y}, sign)
    ps_after = -ps_before
    _assert_pass_over([op1], ps_before, ps_after)

    ps_after = alphaclops.PauliString({q0: Z, q1: Y}, -sign)
    _assert_pass_over([op0, op1], ps_before, ps_after)

    op0 = alphaclops.SingleQubitCliffordGate.from_pauli(Z, True)(q0)
    op1 = alphaclops.SingleQubitCliffordGate.from_pauli(X, True)(q0)
    ps_before = alphaclops.PauliString({q0: X}, sign)
    ps_after = alphaclops.PauliString({q0: Y}, -sign)
    _assert_pass_over([op0, op1], ps_before, ps_after)


@pytest.mark.parametrize(
    'shift,t_or_f1, t_or_f2,neg', itertools.product(range(3), *((True, False),) * 3)
)
def test_pass_operations_over_double(shift: int, t_or_f1: bool, t_or_f2: bool, neg: bool):
    sign = -1 if neg else +1
    q0, q1, q2 = _make_qubits(3)
    X, Y, Z = (alphaclops.Pauli.by_relative_index(pauli, shift) for pauli in (alphaclops.X, alphaclops.Y, alphaclops.Z))

    op0 = alphaclops.PauliInteractionGate(Z, t_or_f1, X, t_or_f2)(q0, q1)
    ps_before = alphaclops.PauliString(qubit_pauli_map={q0: Z, q2: Y}, coefficient=sign)
    ps_after = alphaclops.PauliString(qubit_pauli_map={q0: Z, q2: Y}, coefficient=sign)
    _assert_pass_over([op0], ps_before, ps_after)

    op0 = alphaclops.PauliInteractionGate(Y, t_or_f1, X, t_or_f2)(q0, q1)
    ps_before = alphaclops.PauliString({q0: Z, q2: Y}, sign)
    ps_after = alphaclops.PauliString({q0: Z, q2: Y, q1: X}, sign)
    _assert_pass_over([op0], ps_before, ps_after)

    op0 = alphaclops.PauliInteractionGate(Z, t_or_f1, X, t_or_f2)(q0, q1)
    ps_before = alphaclops.PauliString({q0: Z, q1: Y}, sign)
    ps_after = alphaclops.PauliString({q1: Y}, sign)
    _assert_pass_over([op0], ps_before, ps_after)

    op0 = alphaclops.PauliInteractionGate(Y, t_or_f1, X, t_or_f2)(q0, q1)
    ps_before = alphaclops.PauliString({q0: Z, q1: Y}, sign)
    ps_after = alphaclops.PauliString({q0: X, q1: Z}, -1 if neg ^ t_or_f1 ^ t_or_f2 else +1)
    _assert_pass_over([op0], ps_before, ps_after)

    op0 = alphaclops.PauliInteractionGate(X, t_or_f1, X, t_or_f2)(q0, q1)
    ps_before = alphaclops.PauliString({q0: Z, q1: Y}, sign)
    ps_after = alphaclops.PauliString({q0: Y, q1: Z}, +1 if neg ^ t_or_f1 ^ t_or_f2 else -1)
    _assert_pass_over([op0], ps_before, ps_after)


def test_pass_operations_over_cz():
    q0, q1 = _make_qubits(2)
    op0 = alphaclops.CZ(q0, q1)
    ps_before = alphaclops.PauliString({q0: alphaclops.Z, q1: alphaclops.Y})
    ps_after = alphaclops.PauliString({q1: alphaclops.Y})
    _assert_pass_over([op0], ps_before, ps_after)


def test_pass_operations_over_no_common_qubits():
    class DummyGate(alphaclops.testing.SingleQubitGate):
        pass

    q0, q1 = _make_qubits(2)
    op0 = DummyGate()(q1)
    ps_before = alphaclops.PauliString({q0: alphaclops.Z})
    ps_after = alphaclops.PauliString({q0: alphaclops.Z})
    _assert_pass_over([op0], ps_before, ps_after)


def test_pass_unsupported_operations_over():
    (q0,) = _make_qubits(1)
    pauli_string = alphaclops.PauliString({q0: alphaclops.X})
    with pytest.raises(TypeError, match='not a known Clifford'):
        pauli_string.pass_operations_over([alphaclops.T(q0)])


def test_with_qubits():
    old_qubits = alphaclops.LineQubit.range(9)
    new_qubits = alphaclops.LineQubit.range(9, 18)
    qubit_pauli_map = {q: alphaclops.Pauli.by_index(q.x) for q in old_qubits}
    pauli_string = alphaclops.PauliString(qubit_pauli_map, -1)
    new_pauli_string = pauli_string.with_qubits(*new_qubits)

    assert new_pauli_string.qubits == tuple(new_qubits)
    for q in new_qubits:
        assert new_pauli_string[q] == alphaclops.Pauli.by_index(q.x)
    assert new_pauli_string.coefficient == -1


def test_with_qubits_raises():
    q = alphaclops.LineQubit.range(3)
    pauli_string = alphaclops.X(q[0]) * alphaclops.Y(q[1]) * alphaclops.Z(q[2])
    with pytest.raises(ValueError, match='does not match'):
        pauli_string.with_qubits(q[:2])


def test_with_coefficient():
    qubits = alphaclops.LineQubit.range(4)
    qubit_pauli_map = {q: alphaclops.Pauli.by_index(q.x) for q in qubits}
    pauli_string = alphaclops.PauliString(qubit_pauli_map, 1.23)
    ps2 = pauli_string.with_coefficient(1.0)
    assert ps2.coefficient == 1.0
    assert ps2.equal_up_to_coefficient(pauli_string)
    assert pauli_string != ps2
    assert pauli_string.coefficient == 1.23


@pytest.mark.parametrize('qubit_pauli_map', _small_sample_qubit_pauli_maps())
def test_consistency(qubit_pauli_map):
    pauli_string = alphaclops.PauliString(qubit_pauli_map)
    alphaclops.testing.assert_implements_consistent_protocols(pauli_string)


def test_scaled_unitary_consistency():
    a, b = alphaclops.LineQubit.range(2)
    alphaclops.testing.assert_implements_consistent_protocols(2 * alphaclops.X(a) * alphaclops.Y(b))
    alphaclops.testing.assert_implements_consistent_protocols(1j * alphaclops.X(a) * alphaclops.Y(b))


def test_bool():
    a = alphaclops.LineQubit(0)
    assert not bool(alphaclops.PauliString({}))
    assert bool(alphaclops.PauliString({a: alphaclops.X}))


def _pauli_string_matrix_cases():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    return (
        (alphaclops.X(q0) * 2, None, np.array([[0, 2], [2, 0]])),
        (alphaclops.X(q0) * alphaclops.Y(q1), (q0,), np.array([[0, 1], [1, 0]])),
        (alphaclops.X(q0) * alphaclops.Y(q1), (q1,), np.array([[0, -1j], [1j, 0]])),
        (
            alphaclops.X(q0) * alphaclops.Y(q1),
            None,
            np.array([[0, 0, 0, -1j], [0, 0, 1j, 0], [0, -1j, 0, 0], [1j, 0, 0, 0]]),
        ),
        (
            alphaclops.X(q0) * alphaclops.Y(q1),
            (q0, q1),
            np.array([[0, 0, 0, -1j], [0, 0, 1j, 0], [0, -1j, 0, 0], [1j, 0, 0, 0]]),
        ),
        (
            alphaclops.X(q0) * alphaclops.Y(q1),
            (q1, q0),
            np.array([[0, 0, 0, -1j], [0, 0, -1j, 0], [0, 1j, 0, 0], [1j, 0, 0, 0]]),
        ),
        (alphaclops.X(q0) * alphaclops.Y(q1), (q2,), np.eye(2)),
        (
            alphaclops.X(q0) * alphaclops.Y(q1),
            (q2, q1),
            np.array([[0, -1j, 0, 0], [1j, 0, 0, 0], [0, 0, 0, -1j], [0, 0, 1j, 0]]),
        ),
        (
            alphaclops.X(q0) * alphaclops.Y(q1),
            (q2, q0, q1),
            np.array(
                [
                    [0, 0, 0, -1j, 0, 0, 0, 0],
                    [0, 0, 1j, 0, 0, 0, 0, 0],
                    [0, -1j, 0, 0, 0, 0, 0, 0],
                    [1j, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, -1j],
                    [0, 0, 0, 0, 0, 0, 1j, 0],
                    [0, 0, 0, 0, 0, -1j, 0, 0],
                    [0, 0, 0, 0, 1j, 0, 0, 0],
                ]
            ),
        ),
    )


@pytest.mark.parametrize('pauli_string, qubits, expected_matrix', _pauli_string_matrix_cases())
def test_matrix(pauli_string, qubits, expected_matrix):
    assert np.allclose(pauli_string.matrix(qubits), expected_matrix)


def test_unitary_matrix():
    a, b = alphaclops.LineQubit.range(2)
    assert not alphaclops.has_unitary(2 * alphaclops.X(a) * alphaclops.Z(b))
    assert alphaclops.unitary(2 * alphaclops.X(a) * alphaclops.Z(b), default=None) is None
    # fmt: off
    np.testing.assert_allclose(
        alphaclops.unitary(alphaclops.X(a) * alphaclops.Z(b)),
        np.array(
            [
                [0, 0, 1, 0],
                [0, 0, 0, -1],
                [1, 0, 0, 0],
                [0, -1, 0, 0],
            ]
        ),
    )
    np.testing.assert_allclose(
        alphaclops.unitary(1j * alphaclops.X(a) * alphaclops.Z(b)),
        np.array(
            [
                [0, 0, 1j, 0],
                [0, 0, 0, -1j],
                [1j, 0, 0, 0],
                [0, -1j, 0, 0],
            ]
        ),
    )
    # fmt: on


def test_decompose():
    a, b = alphaclops.LineQubit.range(2)
    assert alphaclops.decompose_once(2 * alphaclops.X(a) * alphaclops.Z(b), default=None) is None
    assert alphaclops.decompose_once(1j * alphaclops.X(a) * alphaclops.Z(b)) == [
        alphaclops.global_phase_operation(1j),
        alphaclops.X(a),
        alphaclops.Z(b),
    ]
    assert alphaclops.decompose_once(alphaclops.Y(b) * alphaclops.Z(a)) == [alphaclops.Y(b), alphaclops.Z(a)]


def test_rejects_non_paulis():
    q = alphaclops.NamedQubit('q')
    with pytest.raises(TypeError):
        _ = alphaclops.PauliString({q: alphaclops.S})


def test_cannot_multiply_by_non_paulis():
    q = alphaclops.NamedQubit('q')
    with pytest.raises(TypeError):
        _ = alphaclops.X(q) * alphaclops.Z(q) ** 0.5
    with pytest.raises(TypeError):
        _ = alphaclops.Z(q) ** 0.5 * alphaclops.X(q)
    with pytest.raises(TypeError):
        _ = alphaclops.Y(q) * alphaclops.S(q)


def test_filters_identities():
    q1, q2 = alphaclops.LineQubit.range(2)
    assert alphaclops.PauliString({q1: alphaclops.I, q2: alphaclops.X}) == alphaclops.PauliString({q2: alphaclops.X})


def test_expectation_from_state_vector_invalid_input():
    q0, q1, q2, q3 = _make_qubits(4)
    ps = alphaclops.PauliString({q0: alphaclops.X, q1: alphaclops.Y})
    wf = np.array([1, 0, 0, 0], dtype=np.complex64)
    q_map = {q0: 0, q1: 1}

    im_ps = (1j + 1) * ps
    with pytest.raises(NotImplementedError, match='non-Hermitian'):
        im_ps.expectation_from_state_vector(wf, q_map)

    with pytest.raises(TypeError, match='dtype'):
        ps.expectation_from_state_vector(np.array([1, 0], dtype=int), q_map)

    with pytest.raises(TypeError, match='mapping'):
        # noinspection PyTypeChecker
        ps.expectation_from_state_vector(wf, "bad type")
    with pytest.raises(TypeError, match='mapping'):
        # noinspection PyTypeChecker
        ps.expectation_from_state_vector(wf, {"bad key": 1})
    with pytest.raises(TypeError, match='mapping'):
        # noinspection PyTypeChecker
        ps.expectation_from_state_vector(wf, {q0: "bad value"})
    with pytest.raises(ValueError, match='complete'):
        ps.expectation_from_state_vector(wf, {q0: 0})
    with pytest.raises(ValueError, match='complete'):
        ps.expectation_from_state_vector(wf, {q0: 0, q2: 2})
    with pytest.raises(ValueError, match='indices'):
        ps.expectation_from_state_vector(wf, {q0: -1, q1: 1})
    with pytest.raises(ValueError, match='indices'):
        ps.expectation_from_state_vector(wf, {q0: 0, q1: 3})
    with pytest.raises(ValueError, match='indices'):
        ps.expectation_from_state_vector(wf, {q0: 0, q1: 0})
    # Excess keys are ignored.
    _ = ps.expectation_from_state_vector(wf, {q0: 0, q1: 1, q2: 0})

    # Incorrectly shaped state_vector input.
    with pytest.raises(ValueError, match='7'):
        ps.expectation_from_state_vector(np.arange(7, dtype=np.complex64), q_map)
    q_map_2 = {q0: 0, q1: 1, q2: 2, q3: 3}
    with pytest.raises(ValueError, match='normalized'):
        ps.expectation_from_state_vector(np.arange(16, dtype=np.complex64), q_map_2)

    # The ambiguous case: Density matrices satisfying L2 normalization.
    rho_or_wf = 0.5 * np.ones((2, 2), dtype=np.complex64)
    _ = ps.expectation_from_state_vector(rho_or_wf, q_map)

    wf = np.arange(16, dtype=np.complex64) / np.linalg.norm(np.arange(16))
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_state_vector(wf.reshape((16, 1)), q_map_2)
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_state_vector(wf.reshape((4, 4, 1)), q_map_2)


def test_expectation_from_state_vector_check_preconditions():
    q0, q1, q2, q3 = _make_qubits(4)
    ps = alphaclops.PauliString({q0: alphaclops.X, q1: alphaclops.Y})
    q_map = {q0: 0, q1: 1, q2: 2, q3: 3}

    with pytest.raises(ValueError, match='normalized'):
        ps.expectation_from_state_vector(np.arange(16, dtype=np.complex64), q_map)

    _ = ps.expectation_from_state_vector(
        np.arange(16, dtype=np.complex64), q_map, check_preconditions=False
    )


def test_expectation_from_state_vector_basis_states():
    q0 = alphaclops.LineQubit(0)
    x0 = alphaclops.PauliString({q0: alphaclops.X})
    q_map = {q0: 0}

    np.testing.assert_allclose(
        x0.expectation_from_state_vector(np.array([1, 0], dtype=complex), q_map), 0, atol=1e-7
    )
    np.testing.assert_allclose(
        x0.expectation_from_state_vector(np.array([0, 1], dtype=complex), q_map), 0, atol=1e-7
    )
    np.testing.assert_allclose(
        x0.expectation_from_state_vector(np.array([1, 1], dtype=complex) / np.sqrt(2), q_map),
        1,
        atol=1e-7,
    )
    np.testing.assert_allclose(
        x0.expectation_from_state_vector(np.array([1, -1], dtype=complex) / np.sqrt(2), q_map),
        -1,
        atol=1e-7,
    )

    y0 = alphaclops.PauliString({q0: alphaclops.Y})
    np.testing.assert_allclose(
        y0.expectation_from_state_vector(np.array([1, 1j], dtype=complex) / np.sqrt(2), q_map),
        1,
        atol=1e-7,
    )
    np.testing.assert_allclose(
        y0.expectation_from_state_vector(np.array([1, -1j], dtype=complex) / np.sqrt(2), q_map),
        -1,
        atol=1e-7,
    )
    np.testing.assert_allclose(
        y0.expectation_from_state_vector(np.array([1, 1], dtype=complex) / np.sqrt(2), q_map),
        0,
        atol=1e-7,
    )
    np.testing.assert_allclose(
        y0.expectation_from_state_vector(np.array([1, -1], dtype=complex) / np.sqrt(2), q_map),
        0,
        atol=1e-7,
    )


def test_expectation_from_state_vector_entangled_states():
    q0, q1 = _make_qubits(2)
    z0z1_pauli_map = {q0: alphaclops.Z, q1: alphaclops.Z}
    z0z1 = alphaclops.PauliString(z0z1_pauli_map)
    x0x1_pauli_map = {q0: alphaclops.X, q1: alphaclops.X}
    x0x1 = alphaclops.PauliString(x0x1_pauli_map)
    q_map = {q0: 0, q1: 1}
    wf1 = np.array([0, 1, 1, 0], dtype=complex) / np.sqrt(2)
    for state in [wf1, wf1.reshape((2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_state_vector(state, q_map), -1)
        np.testing.assert_allclose(x0x1.expectation_from_state_vector(state, q_map), 1)

    wf2 = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
    for state in [wf2, wf2.reshape((2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_state_vector(state, q_map), 1)
        np.testing.assert_allclose(x0x1.expectation_from_state_vector(state, q_map), 1)

    wf3 = np.array([1, 1, 1, 1], dtype=complex) / 2
    for state in [wf3, wf3.reshape((2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_state_vector(state, q_map), 0)
        np.testing.assert_allclose(x0x1.expectation_from_state_vector(state, q_map), 1)


def test_expectation_from_state_vector_qubit_map():
    q0, q1, q2 = _make_qubits(3)
    z = alphaclops.PauliString({q0: alphaclops.Z})
    wf = np.array([0, 1, 0, 1, 0, 0, 0, 0], dtype=complex) / np.sqrt(2)
    for state in [wf, wf.reshape((2, 2, 2))]:
        np.testing.assert_allclose(
            z.expectation_from_state_vector(state, {q0: 0, q1: 1, q2: 2}), 1, atol=1e-8
        )
        np.testing.assert_allclose(
            z.expectation_from_state_vector(state, {q0: 0, q1: 2, q2: 1}), 1, atol=1e-8
        )
        np.testing.assert_allclose(
            z.expectation_from_state_vector(state, {q0: 1, q1: 0, q2: 2}), 0, atol=1e-8
        )
        np.testing.assert_allclose(
            z.expectation_from_state_vector(state, {q0: 1, q1: 2, q2: 0}), 0, atol=1e-9
        )
        np.testing.assert_allclose(
            z.expectation_from_state_vector(state, {q0: 2, q1: 0, q2: 1}), -1, atol=1e-8
        )
        np.testing.assert_allclose(
            z.expectation_from_state_vector(state, {q0: 2, q1: 1, q2: 0}), -1, atol=1e-8
        )


def test_pauli_string_expectation_from_state_vector_pure_state():
    qubits = alphaclops.LineQubit.range(4)
    q_map = {q: i for i, q in enumerate(qubits)}

    circuit = alphaclops.Circuit(
        alphaclops.X(qubits[1]), alphaclops.H(qubits[2]), alphaclops.X(qubits[3]), alphaclops.H(qubits[3])
    )
    wf = circuit.final_state_vector(
        qubit_order=qubits, ignore_terminal_measurements=False, dtype=np.complex128
    )

    z0z1 = alphaclops.PauliString({qubits[0]: alphaclops.Z, qubits[1]: alphaclops.Z})
    z0z2 = alphaclops.PauliString({qubits[0]: alphaclops.Z, qubits[2]: alphaclops.Z})
    z0z3 = alphaclops.PauliString({qubits[0]: alphaclops.Z, qubits[3]: alphaclops.Z})
    z0x1 = alphaclops.PauliString({qubits[0]: alphaclops.Z, qubits[1]: alphaclops.X})
    z1x2 = alphaclops.PauliString({qubits[1]: alphaclops.Z, qubits[2]: alphaclops.X})
    x0z1 = alphaclops.PauliString({qubits[0]: alphaclops.X, qubits[1]: alphaclops.Z})
    x3 = alphaclops.PauliString({qubits[3]: alphaclops.X})

    for state in [wf, wf.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_state_vector(state, q_map), -1, atol=1e-8)
        np.testing.assert_allclose(z0z2.expectation_from_state_vector(state, q_map), 0, atol=1e-8)
        np.testing.assert_allclose(z0z3.expectation_from_state_vector(state, q_map), 0, atol=1e-8)
        np.testing.assert_allclose(z0x1.expectation_from_state_vector(state, q_map), 0, atol=1e-8)
        np.testing.assert_allclose(z1x2.expectation_from_state_vector(state, q_map), -1, atol=1e-8)
        np.testing.assert_allclose(x0z1.expectation_from_state_vector(state, q_map), 0, atol=1e-8)
        np.testing.assert_allclose(x3.expectation_from_state_vector(state, q_map), -1, atol=1e-8)


def test_pauli_string_expectation_from_state_vector_pure_state_with_coef():
    qs = alphaclops.LineQubit.range(4)
    q_map = {q: i for i, q in enumerate(qs)}

    circuit = alphaclops.Circuit(alphaclops.X(qs[1]), alphaclops.H(qs[2]), alphaclops.X(qs[3]), alphaclops.H(qs[3]))
    wf = circuit.final_state_vector(
        qubit_order=qs, ignore_terminal_measurements=False, dtype=np.complex128
    )

    z0z1 = alphaclops.Z(qs[0]) * alphaclops.Z(qs[1]) * 0.123
    z0z2 = alphaclops.Z(qs[0]) * alphaclops.Z(qs[2]) * -1
    z1x2 = -alphaclops.Z(qs[1]) * alphaclops.X(qs[2])

    for state in [wf, wf.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(
            z0z1.expectation_from_state_vector(state, q_map), -0.123, atol=1e-8
        )
        np.testing.assert_allclose(z0z2.expectation_from_state_vector(state, q_map), 0, atol=1e-8)
        np.testing.assert_allclose(z1x2.expectation_from_state_vector(state, q_map), 1, atol=1e-8)


def test_expectation_from_density_matrix_invalid_input():
    q0, q1, q2, q3 = _make_qubits(4)
    ps = alphaclops.PauliString({q0: alphaclops.X, q1: alphaclops.Y})
    wf = alphaclops.testing.random_superposition(4)
    rho = np.kron(wf.conjugate().T, wf).reshape((4, 4))
    q_map = {q0: 0, q1: 1}

    im_ps = (1j + 1) * ps
    with pytest.raises(NotImplementedError, match='non-Hermitian'):
        im_ps.expectation_from_density_matrix(rho, q_map)

    with pytest.raises(TypeError, match='dtype'):
        ps.expectation_from_density_matrix(0.5 * np.eye(2, dtype=int), q_map)

    with pytest.raises(TypeError, match='mapping'):
        # noinspection PyTypeChecker
        ps.expectation_from_density_matrix(rho, "bad type")
    with pytest.raises(TypeError, match='mapping'):
        # noinspection PyTypeChecker
        ps.expectation_from_density_matrix(rho, {"bad key": 1})
    with pytest.raises(TypeError, match='mapping'):
        # noinspection PyTypeChecker
        ps.expectation_from_density_matrix(rho, {q0: "bad value"})
    with pytest.raises(ValueError, match='complete'):
        ps.expectation_from_density_matrix(rho, {q0: 0})
    with pytest.raises(ValueError, match='complete'):
        ps.expectation_from_density_matrix(rho, {q0: 0, q2: 2})
    with pytest.raises(ValueError, match='indices'):
        ps.expectation_from_density_matrix(rho, {q0: -1, q1: 1})
    with pytest.raises(ValueError, match='indices'):
        ps.expectation_from_density_matrix(rho, {q0: 0, q1: 3})
    with pytest.raises(ValueError, match='indices'):
        ps.expectation_from_density_matrix(rho, {q0: 0, q1: 0})
    # Excess keys are ignored.
    _ = ps.expectation_from_density_matrix(rho, {q0: 0, q1: 1, q2: 0})

    with pytest.raises(ValueError, match='hermitian'):
        ps.expectation_from_density_matrix(1j * np.eye(4), q_map)
    with pytest.raises(ValueError, match='trace'):
        ps.expectation_from_density_matrix(np.eye(4, dtype=np.complex64), q_map)
    with pytest.raises(ValueError, match='semidefinite'):
        ps.expectation_from_density_matrix(
            np.array(
                [[1.1, 0, 0, 0], [0, -0.1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=np.complex64
            ),
            q_map,
        )

    # Incorrectly shaped density matrix input.
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_density_matrix(np.ones((4, 5), dtype=np.complex64), q_map)
    q_map_2 = {q0: 0, q1: 1, q2: 2, q3: 3}
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_density_matrix(rho.reshape((4, 4, 1)), q_map_2)
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_density_matrix(rho.reshape((-1)), q_map_2)

    # Correctly shaped state_vectors.
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_density_matrix(np.array([1, 0], dtype=np.complex64), q_map)
    with pytest.raises(ValueError, match='shape'):
        ps.expectation_from_density_matrix(wf, q_map)

    # The ambiguous cases: state_vectors satisfying trace normalization.
    # This also throws an unrelated warning, which is a bug. See #2041.
    rho_or_wf = 0.25 * np.ones((4, 4), dtype=np.complex64)
    _ = ps.expectation_from_density_matrix(rho_or_wf, q_map)


def test_expectation_from_density_matrix_check_preconditions():
    q0, q1 = _make_qubits(2)
    ps = alphaclops.PauliString({q0: alphaclops.X, q1: alphaclops.Y})
    q_map = {q0: 0, q1: 1}

    with pytest.raises(ValueError, match='semidefinite'):
        ps.expectation_from_density_matrix(
            np.array(
                [[1.1, 0, 0, 0], [0, -0.1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=np.complex64
            ),
            q_map,
        )

    _ = ps.expectation_from_density_matrix(
        np.array([[1.1, 0, 0, 0], [0, -0.1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=np.complex64),
        q_map,
        check_preconditions=False,
    )


def test_expectation_from_density_matrix_basis_states():
    q0 = alphaclops.LineQubit(0)
    x0_pauli_map = {q0: alphaclops.X}
    x0 = alphaclops.PauliString(x0_pauli_map)
    q_map = {q0: 0}
    np.testing.assert_allclose(
        x0.expectation_from_density_matrix(np.array([[1, 0], [0, 0]], dtype=complex), q_map), 0
    )
    np.testing.assert_allclose(
        x0.expectation_from_density_matrix(np.array([[0, 0], [0, 1]], dtype=complex), q_map), 0
    )
    np.testing.assert_allclose(
        x0.expectation_from_density_matrix(np.array([[1, 1], [1, 1]], dtype=complex) / 2, q_map), 1
    )
    np.testing.assert_allclose(
        x0.expectation_from_density_matrix(np.array([[1, -1], [-1, 1]], dtype=complex) / 2, q_map),
        -1,
    )


def test_expectation_from_density_matrix_entangled_states():
    q0, q1 = _make_qubits(2)
    z0z1_pauli_map = {q0: alphaclops.Z, q1: alphaclops.Z}
    z0z1 = alphaclops.PauliString(z0z1_pauli_map)
    x0x1_pauli_map = {q0: alphaclops.X, q1: alphaclops.X}
    x0x1 = alphaclops.PauliString(x0x1_pauli_map)
    q_map = {q0: 0, q1: 1}

    wf1 = np.array([0, 1, 1, 0], dtype=complex) / np.sqrt(2)
    rho1 = np.kron(wf1, wf1).reshape((4, 4))
    for state in [rho1, rho1.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_density_matrix(state, q_map), -1)
        np.testing.assert_allclose(x0x1.expectation_from_density_matrix(state, q_map), 1)

    wf2 = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
    rho2 = np.kron(wf2, wf2).reshape((4, 4))
    for state in [rho2, rho2.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_density_matrix(state, q_map), 1)
        np.testing.assert_allclose(x0x1.expectation_from_density_matrix(state, q_map), 1)

    wf3 = np.array([1, 1, 1, 1], dtype=complex) / 2
    rho3 = np.kron(wf3, wf3).reshape((4, 4))
    for state in [rho3, rho3.reshape((2, 2, 2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_density_matrix(state, q_map), 0)
        np.testing.assert_allclose(x0x1.expectation_from_density_matrix(state, q_map), 1)


def test_expectation_from_density_matrix_qubit_map():
    q0, q1, q2 = _make_qubits(3)
    z = alphaclops.PauliString({q0: alphaclops.Z})
    wf = np.array([0, 1, 0, 1, 0, 0, 0, 0], dtype=complex) / np.sqrt(2)
    rho = np.kron(wf, wf).reshape((8, 8))

    for state in [rho, rho.reshape((2, 2, 2, 2, 2, 2))]:
        np.testing.assert_allclose(
            z.expectation_from_density_matrix(state, {q0: 0, q1: 1, q2: 2}), 1
        )
        np.testing.assert_allclose(
            z.expectation_from_density_matrix(state, {q0: 0, q1: 2, q2: 1}), 1
        )
        np.testing.assert_allclose(
            z.expectation_from_density_matrix(state, {q0: 1, q1: 0, q2: 2}), 0
        )
        np.testing.assert_allclose(
            z.expectation_from_density_matrix(state, {q0: 1, q1: 2, q2: 0}), 0
        )
        np.testing.assert_allclose(
            z.expectation_from_density_matrix(state, {q0: 2, q1: 0, q2: 1}), -1
        )
        np.testing.assert_allclose(
            z.expectation_from_density_matrix(state, {q0: 2, q1: 1, q2: 0}), -1
        )


def test_pauli_string_expectation_from_density_matrix_pure_state():
    qubits = alphaclops.LineQubit.range(4)
    q_map = {q: i for i, q in enumerate(qubits)}

    circuit = alphaclops.Circuit(
        alphaclops.X(qubits[1]), alphaclops.H(qubits[2]), alphaclops.X(qubits[3]), alphaclops.H(qubits[3])
    )
    state_vector = circuit.final_state_vector(
        qubit_order=qubits, ignore_terminal_measurements=False, dtype=np.complex128
    )
    rho = np.outer(state_vector, np.conj(state_vector))

    z0z1 = alphaclops.PauliString({qubits[0]: alphaclops.Z, qubits[1]: alphaclops.Z})
    z0z2 = alphaclops.PauliString({qubits[0]: alphaclops.Z, qubits[2]: alphaclops.Z})
    z0z3 = alphaclops.PauliString({qubits[0]: alphaclops.Z, qubits[3]: alphaclops.Z})
    z0x1 = alphaclops.PauliString({qubits[0]: alphaclops.Z, qubits[1]: alphaclops.X})
    z1x2 = alphaclops.PauliString({qubits[1]: alphaclops.Z, qubits[2]: alphaclops.X})
    x0z1 = alphaclops.PauliString({qubits[0]: alphaclops.X, qubits[1]: alphaclops.Z})
    x3 = alphaclops.PauliString({qubits[3]: alphaclops.X})

    for state in [rho, rho.reshape((2, 2, 2, 2, 2, 2, 2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_density_matrix(state, q_map), -1)
        np.testing.assert_allclose(z0z2.expectation_from_density_matrix(state, q_map), 0)
        np.testing.assert_allclose(z0z3.expectation_from_density_matrix(state, q_map), 0)
        np.testing.assert_allclose(z0x1.expectation_from_density_matrix(state, q_map), 0)
        np.testing.assert_allclose(z1x2.expectation_from_density_matrix(state, q_map), -1)
        np.testing.assert_allclose(x0z1.expectation_from_density_matrix(state, q_map), 0)
        np.testing.assert_allclose(x3.expectation_from_density_matrix(state, q_map), -1)


def test_pauli_string_expectation_from_density_matrix_pure_state_with_coef():
    qs = alphaclops.LineQubit.range(4)
    q_map = {q: i for i, q in enumerate(qs)}

    circuit = alphaclops.Circuit(alphaclops.X(qs[1]), alphaclops.H(qs[2]), alphaclops.X(qs[3]), alphaclops.H(qs[3]))
    state_vector = circuit.final_state_vector(
        qubit_order=qs, ignore_terminal_measurements=False, dtype=np.complex128
    )
    rho = np.outer(state_vector, np.conj(state_vector))

    z0z1 = alphaclops.Z(qs[0]) * alphaclops.Z(qs[1]) * 0.123
    z0z2 = alphaclops.Z(qs[0]) * alphaclops.Z(qs[2]) * -1
    z1x2 = -alphaclops.Z(qs[1]) * alphaclops.X(qs[2])

    for state in [rho, rho.reshape((2, 2, 2, 2, 2, 2, 2, 2))]:
        np.testing.assert_allclose(z0z1.expectation_from_density_matrix(state, q_map), -0.123)
        np.testing.assert_allclose(z0z2.expectation_from_density_matrix(state, q_map), 0)
        np.testing.assert_allclose(z1x2.expectation_from_density_matrix(state, q_map), 1)


def test_pauli_string_expectation_from_state_vector_mixed_state_linearity():
    n_qubits = 6

    state_vector1 = alphaclops.testing.random_superposition(2 ** n_qubits)
    state_vector2 = alphaclops.testing.random_superposition(2 ** n_qubits)
    rho1 = np.outer(state_vector1, np.conj(state_vector1))
    rho2 = np.outer(state_vector2, np.conj(state_vector2))
    density_matrix = rho1 / 2 + rho2 / 2

    qubits = alphaclops.LineQubit.range(n_qubits)
    q_map = {q: i for i, q in enumerate(qubits)}
    paulis = [alphaclops.X, alphaclops.Y, alphaclops.Z]
    pauli_string = alphaclops.PauliString({q: np.random.choice(paulis) for q in qubits})

    a = pauli_string.expectation_from_state_vector(state_vector1, q_map)
    b = pauli_string.expectation_from_state_vector(state_vector2, q_map)
    c = pauli_string.expectation_from_density_matrix(density_matrix, q_map)
    np.testing.assert_allclose(0.5 * (a + b), c)


def test_conjugated_by_normal_gates():
    a = alphaclops.LineQubit(0)

    assert alphaclops.X(a).conjugated_by(alphaclops.H(a)) == alphaclops.Z(a)
    assert alphaclops.Y(a).conjugated_by(alphaclops.H(a)) == -alphaclops.Y(a)
    assert alphaclops.Z(a).conjugated_by(alphaclops.H(a)) == alphaclops.X(a)

    assert alphaclops.X(a).conjugated_by(alphaclops.S(a)) == -alphaclops.Y(a)
    assert alphaclops.Y(a).conjugated_by(alphaclops.S(a)) == alphaclops.X(a)
    assert alphaclops.Z(a).conjugated_by(alphaclops.S(a)) == alphaclops.Z(a)


def test_dense():
    a, b, c, d, e = alphaclops.LineQubit.range(5)
    p = alphaclops.PauliString([alphaclops.X(a), alphaclops.Y(b), alphaclops.Z(c)])
    assert p.dense([a, b, c, d]) == alphaclops.DensePauliString('XYZI')
    assert p.dense([d, e, a, b, c]) == alphaclops.DensePauliString('IIXYZ')
    assert -p.dense([a, b, c, d]) == -alphaclops.DensePauliString('XYZI')

    with pytest.raises(ValueError, match=r'not self.keys\(\) <= set\(qubits\)'):
        _ = p.dense([a, b])
    with pytest.raises(ValueError, match=r'not self.keys\(\) <= set\(qubits\)'):
        _ = p.dense([a, b, d])


@pytest.mark.parametrize('qubits', [*itertools.permutations(alphaclops.LineQubit.range(3))])
def test_gate_consistent(qubits):
    g = alphaclops.DensePauliString('XYZ')
    assert g == g(*qubits).gate
    a, b, c = alphaclops.TensorCircuit.rect(1, 3)
    ps = alphaclops.X(a) * alphaclops.Y(b) * alphaclops.Z(c)
    assert ps.gate == ps.with_qubits(*qubits).gate


def test_conjugated_by_incorrectly_powered_cliffords():
    a, b = alphaclops.LineQubit.range(2)
    p = alphaclops.PauliString([alphaclops.X(a), alphaclops.Z(b)])
    cliffords = [
        alphaclops.H(a),
        alphaclops.X(a),
        alphaclops.Y(a),
        alphaclops.Z(a),
        alphaclops.H(a),
        alphaclops.CNOT(a, b),
        alphaclops.CZ(a, b),
        alphaclops.SWAP(a, b),
        alphaclops.ISWAP(a, b),
        alphaclops.XX(a, b),
        alphaclops.YY(a, b),
        alphaclops.ZZ(a, b),
    ]
    for c in cliffords:
        with pytest.raises(TypeError, match='not a known Clifford'):
            _ = p.conjugated_by(c**0.1)
        with pytest.raises(TypeError, match='not a known Clifford'):
            _ = p.conjugated_by(c ** sympy.Symbol('t'))


def test_conjugated_by_global_phase():
    a = alphaclops.LineQubit(0)
    assert alphaclops.X(a).conjugated_by(alphaclops.global_phase_operation(1j)) == alphaclops.X(a)
    assert alphaclops.Z(a).conjugated_by(alphaclops.global_phase_operation(np.exp(1.1j))) == alphaclops.Z(a)

    class DecomposeGlobal(alphaclops.Gate):
        def num_qubits(self):
            return 1

        def _decompose_(self, qubits):
            yield alphaclops.global_phase_operation(1j)

    assert alphaclops.X(a).conjugated_by(DecomposeGlobal().on(a)) == alphaclops.X(a)


def test_conjugated_by_composite_with_disjoint_sub_gates():
    a, b = alphaclops.LineQubit.range(2)

    class DecomposeDisjoint(alphaclops.Gate):
        def num_qubits(self):
            return 2

        def _decompose_(self, qubits):
            yield alphaclops.H(qubits[1])

    assert alphaclops.X(a).conjugated_by(DecomposeDisjoint().on(a, b)) == alphaclops.X(a)
    assert alphaclops.X(a).pass_operations_over([DecomposeDisjoint().on(a, b)]) == alphaclops.X(a)


def test_conjugated_by_clifford_composite():
    class UnknownGate(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 4

        def _decompose_(self, qubits):
            # Involved.
            yield alphaclops.SWAP(qubits[0], qubits[1])
            # Uninvolved.
            yield alphaclops.SWAP(qubits[2], qubits[3])

    a, b, c, d = alphaclops.LineQubit.range(4)
    p = alphaclops.X(a) * alphaclops.Z(b)
    u = UnknownGate()
    assert p.conjugated_by(u(a, b, c, d)) == alphaclops.Z(a) * alphaclops.X(b)


def test_conjugated_by_move_into_uninvolved():
    a, b, c, d = alphaclops.LineQubit.range(4)
    p = alphaclops.X(a) * alphaclops.Z(b)
    assert p.conjugated_by([alphaclops.SWAP(c, d), alphaclops.SWAP(b, c)]) == alphaclops.X(a) * alphaclops.Z(d)
    assert p.conjugated_by([alphaclops.SWAP(b, c), alphaclops.SWAP(c, d)]) == alphaclops.X(a) * alphaclops.Z(c)


def test_conjugated_by_common_single_qubit_gates():
    a, b = alphaclops.LineQubit.range(2)

    base_single_qubit_gates = [
        alphaclops.I,
        alphaclops.X,
        alphaclops.Y,
        alphaclops.Z,
        alphaclops.X ** -0.5,
        alphaclops.Y ** -0.5,
        alphaclops.Z ** -0.5,
        alphaclops.X ** 0.5,
        alphaclops.Y ** 0.5,
        alphaclops.Z ** 0.5,
        alphaclops.H,
    ]
    single_qubit_gates = [g**i for i in range(4) for g in base_single_qubit_gates]
    for p in [alphaclops.X, alphaclops.Y, alphaclops.Z]:
        for g in single_qubit_gates:
            assert p.on(a).conjugated_by(g.on(b)) == p.on(a)

            actual = alphaclops.unitary(p.on(a).conjugated_by(g.on(a)))
            u = alphaclops.unitary(g)
            expected = np.conj(u.T) @ alphaclops.unitary(p) @ u
            assert alphaclops.allclose_up_to_global_phase(actual, expected, atol=1e-8)


def test_conjugated_by_common_two_qubit_gates():
    class OrderSensitiveGate(alphaclops.Gate):
        def num_qubits(self):
            return 2

        def _decompose_(self, qubits):
            return [alphaclops.Y(qubits[0]) ** -0.5, alphaclops.CNOT(*qubits)]

    a, b, c, d = alphaclops.LineQubit.range(4)
    two_qubit_gates = [
        alphaclops.CNOT,
        alphaclops.CZ,
        alphaclops.ISWAP,
        alphaclops.ISWAP_INV,
        alphaclops.SWAP,
        alphaclops.XX ** 0.5,
        alphaclops.YY ** 0.5,
        alphaclops.ZZ ** 0.5,
        alphaclops.XX,
        alphaclops.YY,
        alphaclops.ZZ,
        alphaclops.XX ** -0.5,
        alphaclops.YY ** -0.5,
        alphaclops.ZZ ** -0.5,
    ]
    two_qubit_gates.extend([OrderSensitiveGate()])
    for p1 in [alphaclops.I, alphaclops.X, alphaclops.Y, alphaclops.Z]:
        for p2 in [alphaclops.I, alphaclops.X, alphaclops.Y, alphaclops.Z]:
            pd = alphaclops.DensePauliString([p1, p2])
            p = pd.sparse()
            for g in two_qubit_gates:
                assert p.conjugated_by(g.on(c, d)) == p

                actual = alphaclops.unitary(p.conjugated_by(g.on(a, b)).dense([a, b]))
                u = alphaclops.unitary(g)
                expected = np.conj(u.T) @ alphaclops.unitary(pd) @ u
                np.testing.assert_allclose(actual, expected, atol=1e-8)


def test_conjugated_by_ordering():
    class OrderSensitiveGate(alphaclops.Gate):
        def num_qubits(self):
            return 2

        def _decompose_(self, qubits):
            return [alphaclops.Y(qubits[0]) ** -0.5, alphaclops.CNOT(*qubits)]

    a, b = alphaclops.LineQubit.range(2)
    inp = alphaclops.Z(b)
    out1 = inp.conjugated_by(OrderSensitiveGate().on(a, b))
    out2 = inp.conjugated_by([alphaclops.H(a), alphaclops.CNOT(a, b)])
    out3 = inp.conjugated_by(alphaclops.CNOT(a, b)).conjugated_by(alphaclops.H(a))
    assert out1 == out2 == out3 == alphaclops.X(a) * alphaclops.Z(b)


def test_pass_operations_over_ordering():
    class OrderSensitiveGate(alphaclops.Gate):
        def num_qubits(self):
            return 2

        def _decompose_(self, qubits):
            return [alphaclops.Y(qubits[0]) ** -0.5, alphaclops.CNOT(*qubits)]

    a, b = alphaclops.LineQubit.range(2)
    inp = alphaclops.Z(b)
    out1 = inp.pass_operations_over([OrderSensitiveGate().on(a, b)])
    out2 = inp.pass_operations_over([alphaclops.CNOT(a, b), alphaclops.Y(a) ** -0.5])
    out3 = inp.pass_operations_over([alphaclops.CNOT(a, b)]).pass_operations_over([alphaclops.Y(a) ** -0.5])
    assert out1 == out2 == out3 == alphaclops.X(a) * alphaclops.Z(b)


def test_pass_operations_over_ordering_reversed():
    class OrderSensitiveGate(alphaclops.Gate):
        def num_qubits(self):
            return 2

        def _decompose_(self, qubits):
            return [alphaclops.Y(qubits[0]) ** -0.5, alphaclops.CNOT(*qubits)]

    a, b = alphaclops.LineQubit.range(2)
    inp = alphaclops.X(a) * alphaclops.Z(b)
    out1 = inp.pass_operations_over([OrderSensitiveGate().on(a, b)], after_to_before=True)
    out2 = inp.pass_operations_over([alphaclops.Y(a) ** -0.5, alphaclops.CNOT(a, b)], after_to_before=True)
    out3 = inp.pass_operations_over([alphaclops.Y(a) ** -0.5], after_to_before=True).pass_operations_over(
        [alphaclops.CNOT(a, b)], after_to_before=True
    )
    assert out1 == out2 == out3 == alphaclops.Z(b)


def test_pretty_print():
    a, b, c = alphaclops.LineQubit.range(3)
    result = alphaclops.PauliString({a: 'x', b: 'y', c: 'z'})

    # Test Jupyter console output from
    class FakePrinter:
        def __init__(self):
            self.text_pretty = ''

        def text(self, to_print):
            self.text_pretty += to_print

    p = FakePrinter()
    result._repr_pretty_(p, False)
    assert p.text_pretty == 'X(q(0))*Y(q(1))*Z(q(2))'

    # Test cycle handling
    p = FakePrinter()
    result._repr_pretty_(p, True)
    assert p.text_pretty == 'alphaclops.PauliString(...)'


# pylint: disable=line-too-long
def test_circuit_diagram_info():
    a, b, c = alphaclops.LineQubit.range(3)

    assert alphaclops.circuit_diagram_info(alphaclops.PauliString(), default=None) is None

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            alphaclops.PauliString({a: alphaclops.X}),
            -alphaclops.PauliString({a: alphaclops.X}),
            alphaclops.X(a) * alphaclops.Z(c),
            1j * alphaclops.X(a) * alphaclops.Y(b),
            -1j * alphaclops.Y(b),
            1j ** 0.5 * alphaclops.X(a) * alphaclops.Y(b),
        ),
        """
0: ───PauliString(+X)───PauliString(-X)───PauliString(+X)───PauliString(iX)──────────────────────PauliString((0.707+0.707i)*X)───
                                          │                 │                                    │
1: ───────────────────────────────────────┼─────────────────Y─────────────────PauliString(-iY)───Y───────────────────────────────
                                          │
2: ───────────────────────────────────────Z──────────────────────────────────────────────────────────────────────────────────────
        """,
    )


# pylint: enable=line-too-long


def test_mutable_pauli_string_init_raises():
    q = alphaclops.LineQubit.range(3)
    with pytest.raises(ValueError, match='must be between 1 and 3'):
        _ = alphaclops.MutablePauliString(pauli_int_dict={q[0]: 0, q[1]: 1, q[2]: 2})


def test_mutable_pauli_string_equality():
    eq = alphaclops.testing.EqualsTester()
    a, b, c = alphaclops.LineQubit.range(3)

    eq.add_equality_group(
        alphaclops.MutablePauliString(),
        alphaclops.MutablePauliString(),
        alphaclops.MutablePauliString(1),
        alphaclops.MutablePauliString(-1, -1),
        alphaclops.MutablePauliString({a: 0}),
        alphaclops.MutablePauliString({a: "I"}),
        alphaclops.MutablePauliString({a: alphaclops.I}),
        alphaclops.MutablePauliString(alphaclops.I(a)),
        alphaclops.MutablePauliString(alphaclops.I(b)),
    )

    eq.add_equality_group(
        alphaclops.MutablePauliString({a: "X"}),
        alphaclops.MutablePauliString({a: 1}),
        alphaclops.MutablePauliString({a: alphaclops.X}),
        alphaclops.MutablePauliString(alphaclops.X(a)),
    )

    eq.add_equality_group(
        alphaclops.MutablePauliString({b: "X"}),
        alphaclops.MutablePauliString({b: 1}),
        alphaclops.MutablePauliString({b: alphaclops.X}),
        alphaclops.MutablePauliString(alphaclops.X(b)),
        alphaclops.MutablePauliString(-1j, alphaclops.Y(b), alphaclops.Z(b)),
    )

    eq.add_equality_group(
        alphaclops.MutablePauliString({a: "X", b: "Y", c: "Z"}),
        alphaclops.MutablePauliString({a: 1, b: 2, c: 3}),
        alphaclops.MutablePauliString({a: alphaclops.X, b: alphaclops.Y, c: alphaclops.Z}),
        alphaclops.MutablePauliString(alphaclops.X(a) * alphaclops.Y(b) * alphaclops.Z(c)),
        alphaclops.MutablePauliString(alphaclops.MutablePauliString(alphaclops.X(a) * alphaclops.Y(b) * alphaclops.Z(c))),
        alphaclops.MutablePauliString(alphaclops.MutablePauliString(alphaclops.X(a), alphaclops.Y(b), alphaclops.Z(c))),
    )

    # Cross-type equality. (Can't use tester because hashability differs.)
    p = alphaclops.X(a) * alphaclops.Y(b)
    assert p == alphaclops.MutablePauliString(p)

    with pytest.raises(TypeError, match="alphaclops.PAULI_STRING_LIKE"):
        _ = alphaclops.MutablePauliString("test")
    with pytest.raises(TypeError, match="alphaclops.PAULI_STRING_LIKE"):
        # noinspection PyTypeChecker
        _ = alphaclops.MutablePauliString(object())


def test_mutable_pauli_string_inplace_multiplication():
    a, b, c = alphaclops.LineQubit.range(3)
    p = alphaclops.MutablePauliString()
    original = p

    # Support for *=.
    p *= alphaclops.X(a)
    assert p == alphaclops.X(a) and p is original

    # Bad operand.
    with pytest.raises(TypeError, match="alphaclops.PAULI_STRING_LIKE"):
        p.inplace_left_multiply_by([alphaclops.X(a), alphaclops.CZ(a, b), alphaclops.Z(b)])
    with pytest.raises(TypeError, match="alphaclops.PAULI_STRING_LIKE"):
        p.inplace_left_multiply_by(alphaclops.CZ(a, b))
    with pytest.raises(TypeError, match="alphaclops.PAULI_STRING_LIKE"):
        p.inplace_right_multiply_by([alphaclops.X(a), alphaclops.CZ(a, b), alphaclops.Z(b)])
    with pytest.raises(TypeError, match="alphaclops.PAULI_STRING_LIKE"):
        p.inplace_right_multiply_by(alphaclops.CZ(a, b))
    assert p == alphaclops.X(a) and p is original

    # Correct order of *=.
    p *= alphaclops.Y(a)
    assert p == -1j * alphaclops.Z(a) and p is original
    p *= alphaclops.Y(a)
    assert p == alphaclops.X(a) and p is original

    # Correct order of inplace_left_multiply_by.
    p.inplace_left_multiply_by(alphaclops.Y(a))
    assert p == 1j * alphaclops.Z(a) and p is original
    p.inplace_left_multiply_by(alphaclops.Y(a))
    assert p == alphaclops.X(a) and p is original

    # Correct order of inplace_right_multiply_by.
    p.inplace_right_multiply_by(alphaclops.Y(a))
    assert p == -1j * alphaclops.Z(a) and p is original
    p.inplace_right_multiply_by(alphaclops.Y(a))
    assert p == alphaclops.X(a) and p is original

    # Multi-qubit case.
    p *= -1 * alphaclops.X(a) * alphaclops.X(b)
    assert p == -alphaclops.X(b) and p is original

    # Support for PAULI_STRING_LIKE
    p.inplace_left_multiply_by({c: 'Z'})
    assert p == -alphaclops.X(b) * alphaclops.Z(c) and p is original
    p.inplace_right_multiply_by({c: 'Z'})
    assert p == -alphaclops.X(b) and p is original


def test_mutable_frozen_copy():
    a, b, c = alphaclops.LineQubit.range(3)
    p = -alphaclops.X(a) * alphaclops.Y(b) * alphaclops.Z(c)

    pf = p.frozen()
    pm = p.mutable_copy()
    pmm = pm.mutable_copy()
    pmf = pm.frozen()

    assert isinstance(p, alphaclops.PauliString)
    assert isinstance(pf, alphaclops.PauliString)
    assert isinstance(pm, alphaclops.MutablePauliString)
    assert isinstance(pmm, alphaclops.MutablePauliString)
    assert isinstance(pmf, alphaclops.PauliString)

    assert p is pf
    assert pm is not pmm
    assert p == pf == pm == pmm == pmf


def test_mutable_pauli_string_inplace_conjugate_by():
    a, b, c = alphaclops.LineQubit.range(3)
    p = alphaclops.MutablePauliString(alphaclops.X(a))

    class NoOp(alphaclops.Operation):
        def __init__(self, *qubits):
            self._qubits = qubits

        @property
        def qubits(self):
            # coverage: ignore
            return self._qubits

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

        def _decompose_(self):
            return []

    # No-ops
    p2 = p.inplace_after(alphaclops.global_phase_operation(1j))
    assert p2 is p and p == alphaclops.X(a)
    p2 = p.inplace_after(NoOp(a, b))
    assert p2 is p and p == alphaclops.X(a)

    # After H and back.
    p2 = p.inplace_after(alphaclops.H(a))
    assert p2 is p and p == alphaclops.Z(a)
    p2 = p.inplace_before(alphaclops.H(a))
    assert p2 is p and p == alphaclops.X(a)

    # After S and back.
    p2 = p.inplace_after(alphaclops.S(a))
    assert p2 is p and p == alphaclops.Y(a)
    p2 = p.inplace_before(alphaclops.S(a))
    assert p2 is p and p == alphaclops.X(a)

    # Before S and back.
    p2 = p.inplace_before(alphaclops.S(a))
    assert p2 is p and p == -alphaclops.Y(a)
    p2 = p.inplace_after(alphaclops.S(a))
    assert p2 is p and p == alphaclops.X(a)

    # After inverse S and back.
    p2 = p.inplace_after(alphaclops.S(a) ** -1)
    assert p2 is p and p == -alphaclops.Y(a)
    p2 = p.inplace_before(alphaclops.S(a) ** -1)
    assert p2 is p and p == alphaclops.X(a)

    # On other qubit.
    p2 = p.inplace_after(alphaclops.S(b))
    assert p2 is p and p == alphaclops.X(a)

    # Two qubit operation.
    p2 = p.inplace_after(alphaclops.CZ(a, b))
    assert p2 is p and p == alphaclops.X(a) * alphaclops.Z(b)
    p2 = p.inplace_after(alphaclops.CZ(a, c))
    assert p2 is p and p == alphaclops.X(a) * alphaclops.Z(b) * alphaclops.Z(c)
    p2 = p.inplace_after(alphaclops.H(b))
    assert p2 is p and p == alphaclops.X(a) * alphaclops.X(b) * alphaclops.Z(c)
    p2 = p.inplace_after(alphaclops.CNOT(b, c))
    assert p2 is p and p == -alphaclops.X(a) * alphaclops.Y(b) * alphaclops.Y(c)

    # Inverted interactions.
    p = alphaclops.MutablePauliString(alphaclops.X(a))
    p2 = p.inplace_after(alphaclops.PauliInteractionGate(alphaclops.Y, True, alphaclops.Z, False).on(a, b))
    assert p2 is p and p == alphaclops.X(a) * alphaclops.Z(b)
    p = alphaclops.MutablePauliString(alphaclops.X(a))
    p2 = p.inplace_after(alphaclops.PauliInteractionGate(alphaclops.X, False, alphaclops.Z, True).on(a, b))
    assert p2 is p and p == alphaclops.X(a)
    p = alphaclops.MutablePauliString(alphaclops.X(a))
    p2 = p.inplace_after(alphaclops.PauliInteractionGate(alphaclops.Y, False, alphaclops.Z, True).on(a, b))
    assert p2 is p and p == -alphaclops.X(a) * alphaclops.Z(b)
    p = alphaclops.MutablePauliString(alphaclops.X(a))
    p2 = p.inplace_after(alphaclops.PauliInteractionGate(alphaclops.Z, False, alphaclops.Y, True).on(a, b))
    assert p2 is p and p == -alphaclops.X(a) * alphaclops.Y(b)
    p = alphaclops.MutablePauliString(alphaclops.X(a))
    p2 = p.inplace_after(alphaclops.PauliInteractionGate(alphaclops.Z, True, alphaclops.X, False).on(a, b))
    assert p2 is p and p == alphaclops.X(a) * alphaclops.X(b)
    p = alphaclops.MutablePauliString(alphaclops.X(a))
    p2 = p.inplace_after(alphaclops.PauliInteractionGate(alphaclops.Z, True, alphaclops.Y, False).on(a, b))
    assert p2 is p and p == alphaclops.X(a) * alphaclops.Y(b)


def test_after_before_vs_conjugate_by():
    a, b, c = alphaclops.LineQubit.range(3)
    p = alphaclops.X(a) * alphaclops.Y(b) * alphaclops.Z(c)
    assert p.before(alphaclops.S(b)) == p.conjugated_by(alphaclops.S(b))
    assert p.after(alphaclops.S(b) ** -1) == p.conjugated_by(alphaclops.S(b))
    assert (
            p.before(alphaclops.CNOT(a, b)) == p.conjugated_by(alphaclops.CNOT(a, b)) == (p.after(alphaclops.CNOT(a, b)))
    )


def test_mutable_pauli_string_dict_functionality():
    a, b, c = alphaclops.LineQubit.range(3)
    p = alphaclops.MutablePauliString()
    with pytest.raises(KeyError):
        _ = p[a]
    assert p.get(a) is None
    assert a not in p
    assert not bool(p)
    p[a] = alphaclops.X
    assert bool(p)
    assert a in p
    assert p[a] == alphaclops.X

    p[a] = "Y"
    assert p[a] == alphaclops.Y
    p[a] = 3
    assert p[a] == alphaclops.Z
    p[a] = "I"
    assert a not in p
    p[a] = 0
    assert a not in p

    assert len(p) == 0
    p[b] = "Y"
    p[a] = "X"
    p[c] = "Z"
    assert len(p) == 3
    assert list(iter(p)) == [b, a, c]
    assert list(p.values()) == [alphaclops.Y, alphaclops.X, alphaclops.Z]
    assert list(p.keys()) == [b, a, c]
    assert p.keys() == {a, b, c}
    assert p.keys() ^ {c} == {a, b}

    del p[b]
    assert b not in p


@pytest.mark.parametrize(
    'pauli', (alphaclops.X, alphaclops.Y, alphaclops.Z, alphaclops.I, "I", "X", "Y", "Z", "i", "x", "y", "z", 0, 1, 2, 3)
)
def test_mutable_pauli_string_dict_pauli_like(pauli):
    p = alphaclops.MutablePauliString()
    # Check that is successfully converts.
    p[0] = pauli


def test_mutable_pauli_string_dict_pauli_like_not_pauli_like():
    p = alphaclops.MutablePauliString()
    # Check error string includes terms like "X" in error message.
    with pytest.raises(TypeError, match="PAULI_GATE_LIKE.*X"):
        p[0] = 1.2


def test_mutable_pauli_string_text():
    p = alphaclops.MutablePauliString(alphaclops.X(alphaclops.LineQubit(0)) * alphaclops.Y(alphaclops.LineQubit(1)))
    assert str(alphaclops.MutablePauliString()) == "mutable I"
    assert str(p) == "mutable X(q(0))*Y(q(1))"
    alphaclops.testing.assert_equivalent_repr(p)


def test_mutable_pauli_string_mul():
    a, b = alphaclops.LineQubit.range(2)
    p = alphaclops.X(a).mutable_copy()
    q = alphaclops.Y(b).mutable_copy()
    pq = alphaclops.X(a) * alphaclops.Y(b)
    assert p * q == pq
    assert isinstance(p * q, alphaclops.PauliString)
    assert 2 * p == alphaclops.X(a) * 2 == p * 2
    assert isinstance(p * 2, alphaclops.PauliString)
    assert isinstance(2 * p, alphaclops.PauliString)


def test_mutable_can_override_mul():
    class LMul:
        def __mul__(self, other):
            return "Yay!"

    class RMul:
        def __rmul__(self, other):
            return "Yay!"

    assert alphaclops.MutablePauliString() * RMul() == "Yay!"
    assert LMul() * alphaclops.MutablePauliString() == "Yay!"


def test_coefficient_precision():
    qs = alphaclops.LineQubit.range(4 * 10 ** 3)
    r = alphaclops.MutablePauliString({q: alphaclops.X for q in qs})
    r2 = alphaclops.MutablePauliString({q: alphaclops.Y for q in qs})
    r2 *= r
    assert r2.coefficient == 1


def test_transform_qubits():
    a, b, c = alphaclops.LineQubit.range(3)
    p = alphaclops.X(a) * alphaclops.Z(b)
    p2 = alphaclops.X(b) * alphaclops.Z(c)
    m = p.mutable_copy()
    m2 = m.transform_qubits(lambda q: q + 1)
    assert m is not m2
    assert m == p
    assert m2 == p2

    m2 = m.transform_qubits(lambda q: q + 1, inplace=False)
    assert m is not m2
    assert m == p
    assert m2 == p2

    m2 = m.transform_qubits(lambda q: q + 1, inplace=True)
    assert m is m2
    assert m == p2
    assert m2 == p2


def test_parameterization():
    t = sympy.Symbol('t')
    q = alphaclops.LineQubit(0)
    pst = alphaclops.PauliString({q: 'x'}, coefficient=t)
    assert alphaclops.is_parameterized(pst)
    assert alphaclops.parameter_names(pst) == {'t'}
    assert pst.coefficient == 1.0 * t
    assert not alphaclops.has_unitary(pst)
    assert not alphaclops.is_parameterized(pst.with_coefficient(2))
    with pytest.raises(TypeError):
        alphaclops.decompose_once(pst)
    with pytest.raises(NotImplementedError, match='parameterized'):
        pst.expectation_from_state_vector(np.array([]), {})
    with pytest.raises(NotImplementedError, match='parameterized'):
        pst.expectation_from_density_matrix(np.array([]), {})
    with pytest.raises(NotImplementedError, match='as matrix when parameterized'):
        pst.matrix()
    assert pst**1 == pst
    assert pst**-1 == pst.with_coefficient(1.0 / t)
    assert (-pst) ** 1 == -pst
    assert (-pst) ** -1 == -pst.with_coefficient(1.0 / t)
    assert (1j * pst) ** 1 == 1j * pst
    assert (1j * pst) ** -1 == -1j * pst.with_coefficient(1.0 / t)
    with pytest.raises(TypeError):
        _ = pst**2
    with pytest.raises(TypeError):
        _ = 1**pst
    alphaclops.testing.assert_has_diagram(alphaclops.Circuit(pst), '0: ───PauliString((1.0*t)*X)───')


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_resolve(resolve_fn):
    t = sympy.Symbol('t')
    q = alphaclops.LineQubit(0)
    pst = alphaclops.PauliString({q: 'x'}, coefficient=t)
    ps1 = alphaclops.PauliString({q: 'x'}, coefficient=1j)
    assert resolve_fn(pst, {'t': 1j}) == ps1
