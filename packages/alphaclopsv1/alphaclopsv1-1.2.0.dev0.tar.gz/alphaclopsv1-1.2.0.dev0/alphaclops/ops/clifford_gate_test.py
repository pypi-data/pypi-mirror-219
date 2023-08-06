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

import functools
import itertools
from typing import Tuple, Type

import numpy as np
import pytest

import alphaclops
from alphaclops.protocols.act_on_protocol_test import DummySimulationState
from alphaclops.testing import EqualsTester, assert_allclose_up_to_global_phase

_bools = (False, True)
_paulis = (alphaclops.X, alphaclops.Y, alphaclops.Z)


def _assert_not_mirror(gate) -> None:
    trans_x = gate.pauli_tuple(alphaclops.X)
    trans_y = gate.pauli_tuple(alphaclops.Y)
    trans_z = gate.pauli_tuple(alphaclops.Z)
    right_handed = (
        trans_x[1] ^ trans_y[1] ^ trans_z[1] ^ (trans_x[0].relative_index(trans_y[0]) != 1)
    )
    assert right_handed, 'Mirrors'


def _assert_no_collision(gate) -> None:
    trans_x = gate.pauli_tuple(alphaclops.X)
    trans_y = gate.pauli_tuple(alphaclops.Y)
    trans_z = gate.pauli_tuple(alphaclops.Z)
    assert trans_x[0] != trans_y[0], 'Collision'
    assert trans_y[0] != trans_z[0], 'Collision'
    assert trans_z[0] != trans_x[0], 'Collision'


def _all_rotations():
    for (pauli, flip) in itertools.product(_paulis, _bools):
        yield (pauli, flip)


def _all_rotation_pairs():
    for px, flip_x, pz, flip_z in itertools.product(_paulis, _bools, _paulis, _bools):
        if px == pz:
            continue
        yield (px, flip_x), (pz, flip_z)


@functools.lru_cache()
def _all_clifford_gates() -> Tuple['alphaclops.SingleQubitCliffordGate', ...]:
    return tuple(
        alphaclops.SingleQubitCliffordGate.from_xz_map(trans_x, trans_z)
        for trans_x, trans_z in _all_rotation_pairs()
    )


@pytest.mark.parametrize('pauli,flip_x,flip_z', itertools.product(_paulis, _bools, _bools))
def test_init_value_error(pauli, flip_x, flip_z):
    with pytest.raises(ValueError):
        alphaclops.SingleQubitCliffordGate.from_xz_map((pauli, flip_x), (pauli, flip_z))


@pytest.mark.parametrize('trans_x,trans_z', _all_rotation_pairs())
def test_init_from_xz(trans_x, trans_z):
    gate = alphaclops.SingleQubitCliffordGate.from_xz_map(trans_x, trans_z)
    assert gate.pauli_tuple(alphaclops.X) == trans_x
    assert gate.pauli_tuple(alphaclops.Z) == trans_z
    _assert_not_mirror(gate)
    _assert_no_collision(gate)


def test_dense_pauli_string():
    gate = alphaclops.SingleQubitCliffordGate.from_xz_map((alphaclops.X, True), (alphaclops.Y, False))
    assert gate.dense_pauli_string(alphaclops.X) == alphaclops.DensePauliString('X', coefficient=-1)
    assert gate.dense_pauli_string(alphaclops.Z) == alphaclops.DensePauliString('Y')


@pytest.mark.parametrize(
    'trans1,trans2,from1',
    (
        (trans1, trans2, from1)
        for trans1, trans2, from1 in itertools.product(_all_rotations(), _all_rotations(), _paulis)
        if trans1[0] != trans2[0]
    ),
)
def test_init_from_double_map_vs_kwargs(trans1, trans2, from1):
    from2 = alphaclops.Pauli.by_relative_index(from1, 1)
    from1_str, from2_str = (str(frm).lower() + '_to' for frm in (from1, from2))
    gate_kw = alphaclops.SingleQubitCliffordGate.from_double_map(**{from1_str: trans1, from2_str: trans2})
    gate_map = alphaclops.SingleQubitCliffordGate.from_double_map({from1: trans1, from2: trans2})
    # Test initializes the same gate
    assert gate_kw == gate_map

    # Test initializes what was expected
    assert gate_map.pauli_tuple(from1) == trans1
    assert gate_map.pauli_tuple(from2) == trans2
    _assert_not_mirror(gate_map)
    _assert_no_collision(gate_map)


@pytest.mark.parametrize(
    'trans1,from1',
    ((trans1, from1) for trans1, from1 in itertools.product(_all_rotations(), _paulis)),
)
def test_init_from_double_invalid(trans1, from1):
    from2 = alphaclops.Pauli.by_relative_index(from1, 1)
    # Test throws on invalid arguments
    with pytest.raises(ValueError):
        alphaclops.SingleQubitCliffordGate.from_double_map({from1: trans1, from2: trans1})


@pytest.mark.parametrize('trans,frm', itertools.product(_all_rotations(), _paulis))
def test_init_from_single_map_vs_kwargs(trans, frm):
    from_str = str(frm).lower() + '_to'
    # pylint: disable=unexpected-keyword-arg
    gate_kw = alphaclops.SingleQubitCliffordGate.from_single_map(**{from_str: trans})
    gate_map = alphaclops.SingleQubitCliffordGate.from_single_map({frm: trans})
    assert gate_kw == gate_map


@pytest.mark.parametrize(
    'trans,frm',
    (
        (trans, frm)
        for trans, frm in itertools.product(_all_rotations(), _paulis)
        if trans[0] != frm
    ),
)
def test_init_90rot_from_single(trans, frm):
    gate = alphaclops.SingleQubitCliffordGate.from_single_map({frm: trans})
    assert gate.pauli_tuple(frm) == trans
    _assert_not_mirror(gate)
    _assert_no_collision(gate)
    # Check that it decomposes to one gate
    assert len(gate.decompose_rotation()) == 1
    # Check that this is a 90 degree rotation gate
    assert (
            gate.merged_with(gate).merged_with(gate).merged_with(gate) == alphaclops.SingleQubitCliffordGate.I
    )
    # Check that flipping the transform produces the inverse rotation
    trans_rev = (trans[0], not trans[1])
    gate_rev = alphaclops.SingleQubitCliffordGate.from_single_map({frm: trans_rev})
    assert gate**-1 == gate_rev


@pytest.mark.parametrize(
    'trans,frm',
    (
        (trans, frm)
        for trans, frm in itertools.product(_all_rotations(), _paulis)
        if trans[0] == frm and trans[1]
    ),
)
def test_init_180rot_from_single(trans, frm):
    gate = alphaclops.SingleQubitCliffordGate.from_single_map({frm: trans})
    assert gate.pauli_tuple(frm) == trans
    _assert_not_mirror(gate)
    _assert_no_collision(gate)
    # Check that it decomposes to one gate
    assert len(gate.decompose_rotation()) == 1
    # Check that this is a 180 degree rotation gate
    assert gate.merged_with(gate) == alphaclops.SingleQubitCliffordGate.I


@pytest.mark.parametrize(
    'trans,frm',
    (
        (trans, frm)
        for trans, frm in itertools.product(_all_rotations(), _paulis)
        if trans[0] == frm and not trans[1]
    ),
)
def test_init_ident_from_single(trans, frm):
    gate = alphaclops.SingleQubitCliffordGate.from_single_map({frm: trans})
    assert gate.pauli_tuple(frm) == trans
    _assert_not_mirror(gate)
    _assert_no_collision(gate)
    # Check that it decomposes to zero gates
    assert len(gate.decompose_rotation()) == 0
    # Check that this is an identity gate
    assert gate == alphaclops.SingleQubitCliffordGate.I


@pytest.mark.parametrize(
    'pauli,sqrt,expected',
    (
        (alphaclops.X, False, alphaclops.SingleQubitCliffordGate.X),
        (alphaclops.Y, False, alphaclops.SingleQubitCliffordGate.Y),
        (alphaclops.Z, False, alphaclops.SingleQubitCliffordGate.Z),
        (alphaclops.X, True, alphaclops.SingleQubitCliffordGate.X_sqrt),
        (alphaclops.Y, True, alphaclops.SingleQubitCliffordGate.Y_sqrt),
        (alphaclops.Z, True, alphaclops.SingleQubitCliffordGate.Z_sqrt),
    ),
)
def test_init_from_pauli(pauli, sqrt, expected):
    gate = alphaclops.SingleQubitCliffordGate.from_pauli(pauli, sqrt=sqrt)
    assert gate == expected


def test_pow():
    assert alphaclops.SingleQubitCliffordGate.X ** -1 == alphaclops.SingleQubitCliffordGate.X
    assert alphaclops.SingleQubitCliffordGate.H ** -1 == alphaclops.SingleQubitCliffordGate.H
    assert alphaclops.SingleQubitCliffordGate.X_sqrt == alphaclops.SingleQubitCliffordGate.X ** 0.5
    assert alphaclops.SingleQubitCliffordGate.Y_sqrt == alphaclops.SingleQubitCliffordGate.Y ** 0.5
    assert alphaclops.SingleQubitCliffordGate.Z_sqrt == alphaclops.SingleQubitCliffordGate.Z ** 0.5
    assert alphaclops.SingleQubitCliffordGate.X_nsqrt == alphaclops.SingleQubitCliffordGate.X ** -0.5
    assert alphaclops.SingleQubitCliffordGate.Y_nsqrt == alphaclops.SingleQubitCliffordGate.Y ** -0.5
    assert alphaclops.SingleQubitCliffordGate.Z_nsqrt == alphaclops.SingleQubitCliffordGate.Z ** -0.5
    assert alphaclops.SingleQubitCliffordGate.X_sqrt ** -1 == alphaclops.SingleQubitCliffordGate.X_nsqrt
    assert alphaclops.inverse(alphaclops.SingleQubitCliffordGate.X_nsqrt) == (
        alphaclops.SingleQubitCliffordGate.X_sqrt
    )
    with pytest.raises(TypeError):
        _ = alphaclops.SingleQubitCliffordGate.Z ** 0.25


def test_init_from_quarter_turns():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.X, 0),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Y, 0),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Z, 0),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.X, 4),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Y, 4),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Z, 4),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.X, 8),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Y, 8),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Z, 8),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.X, -4),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Y, -4),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Z, -4),
    )
    eq.add_equality_group(
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.X, 1),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.X, 5),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.X, 9),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.X, -3),
    )
    eq.add_equality_group(
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Y, 1),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Y, 5),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Y, 9),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Y, -3),
    )
    eq.add_equality_group(
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Z, 1),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Z, 5),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Z, 9),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.Z, -3),
    )
    eq.add_equality_group(
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.X, 2),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.X, 6),
    )
    eq.add_equality_group(
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.X, 3),
        alphaclops.SingleQubitCliffordGate.from_quarter_turns(alphaclops.X, 7),
    )


@pytest.mark.parametrize('gate', _all_clifford_gates())
def test_init_from_quarter_turns_reconstruct(gate):
    new_gate = functools.reduce(
        alphaclops.SingleQubitCliffordGate.merged_with,
        (
            alphaclops.SingleQubitCliffordGate.from_quarter_turns(pauli, qt)
            for pauli, qt in gate.decompose_rotation()
        ),
        alphaclops.SingleQubitCliffordGate.I,
    )
    assert gate == new_gate


def test_init_invalid():
    with pytest.raises(ValueError):
        alphaclops.SingleQubitCliffordGate.from_single_map()
    with pytest.raises(ValueError):
        alphaclops.SingleQubitCliffordGate.from_single_map({})
    with pytest.raises(ValueError):
        alphaclops.SingleQubitCliffordGate.from_single_map(
            {alphaclops.X: (alphaclops.X, False)}, y_to=(alphaclops.Y, False)
        )
    with pytest.raises(ValueError):
        alphaclops.SingleQubitCliffordGate.from_single_map(
            {alphaclops.X: (alphaclops.X, False), alphaclops.Y: (alphaclops.Y, False)}
        )
    with pytest.raises(ValueError):
        alphaclops.SingleQubitCliffordGate.from_double_map()
    with pytest.raises(ValueError):
        alphaclops.SingleQubitCliffordGate.from_double_map({})
    with pytest.raises(ValueError):
        alphaclops.SingleQubitCliffordGate.from_double_map({alphaclops.X: (alphaclops.X, False)})
    with pytest.raises(ValueError):
        alphaclops.SingleQubitCliffordGate.from_double_map(x_to=(alphaclops.X, False))
    with pytest.raises(ValueError):
        alphaclops.SingleQubitCliffordGate.from_single_map(
            {alphaclops.X: (alphaclops.Y, False), alphaclops.Y: (alphaclops.Z, False), alphaclops.Z: (alphaclops.X, False)}
        )
    with pytest.raises(ValueError):
        alphaclops.SingleQubitCliffordGate.from_single_map(
            {alphaclops.X: (alphaclops.X, False), alphaclops.Y: (alphaclops.X, False)}
        )


def test_eq_ne_and_hash():
    eq = EqualsTester()
    for trans_x, trans_z in _all_rotation_pairs():
        gate_gen = lambda: alphaclops.SingleQubitCliffordGate.from_xz_map(trans_x, trans_z)
        eq.make_equality_group(gate_gen)


@pytest.mark.parametrize(
    'gate',
    (
            alphaclops.SingleQubitCliffordGate.I,
            alphaclops.SingleQubitCliffordGate.H,
            alphaclops.SingleQubitCliffordGate.X,
            alphaclops.SingleQubitCliffordGate.X_sqrt,
    ),
)
def test_repr_gate(gate):
    alphaclops.testing.assert_equivalent_repr(gate)


def test_repr_operation():
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.SingleQubitCliffordGate.from_pauli(alphaclops.Z).on(alphaclops.LineQubit(2))
    )


@pytest.mark.parametrize(
    'gate,trans_y',
    (
        (alphaclops.SingleQubitCliffordGate.I, (alphaclops.Y, False)),
        (alphaclops.SingleQubitCliffordGate.H, (alphaclops.Y, True)),
        (alphaclops.SingleQubitCliffordGate.X, (alphaclops.Y, True)),
        (alphaclops.SingleQubitCliffordGate.Y, (alphaclops.Y, False)),
        (alphaclops.SingleQubitCliffordGate.Z, (alphaclops.Y, True)),
        (alphaclops.SingleQubitCliffordGate.X_sqrt, (alphaclops.Z, False)),
        (alphaclops.SingleQubitCliffordGate.X_nsqrt, (alphaclops.Z, True)),
        (alphaclops.SingleQubitCliffordGate.Y_sqrt, (alphaclops.Y, False)),
        (alphaclops.SingleQubitCliffordGate.Y_nsqrt, (alphaclops.Y, False)),
        (alphaclops.SingleQubitCliffordGate.Z_sqrt, (alphaclops.X, True)),
        (alphaclops.SingleQubitCliffordGate.Z_nsqrt, (alphaclops.X, False)),
    ),
)
def test_y_rotation(gate, trans_y):
    assert gate.pauli_tuple(alphaclops.Y) == trans_y


@pytest.mark.parametrize(
    'gate,gate_equiv',
    (
        (alphaclops.SingleQubitCliffordGate.I, alphaclops.X ** 0),
        (alphaclops.SingleQubitCliffordGate.H, alphaclops.H),
        (alphaclops.SingleQubitCliffordGate.X, alphaclops.X),
        (alphaclops.SingleQubitCliffordGate.Y, alphaclops.Y),
        (alphaclops.SingleQubitCliffordGate.Z, alphaclops.Z),
        (alphaclops.SingleQubitCliffordGate.X_sqrt, alphaclops.X ** 0.5),
        (alphaclops.SingleQubitCliffordGate.X_nsqrt, alphaclops.X ** -0.5),
        (alphaclops.SingleQubitCliffordGate.Y_sqrt, alphaclops.Y ** 0.5),
        (alphaclops.SingleQubitCliffordGate.Y_nsqrt, alphaclops.Y ** -0.5),
        (alphaclops.SingleQubitCliffordGate.Z_sqrt, alphaclops.Z ** 0.5),
        (alphaclops.SingleQubitCliffordGate.Z_nsqrt, alphaclops.Z ** -0.5),
    ),
)
def test_decompose(gate, gate_equiv):
    q0 = alphaclops.NamedQubit('q0')
    mat = alphaclops.Circuit(gate(q0)).unitary()
    mat_check = alphaclops.Circuit(gate_equiv(q0)).unitary()
    assert_allclose_up_to_global_phase(mat, mat_check, rtol=1e-7, atol=1e-7)


@pytest.mark.parametrize(
    'gate,gate_equiv',
    (
        (alphaclops.SingleQubitCliffordGate.I, alphaclops.X ** 0),
        (alphaclops.SingleQubitCliffordGate.H, alphaclops.H),
        (alphaclops.SingleQubitCliffordGate.X, alphaclops.X),
        (alphaclops.SingleQubitCliffordGate.Y, alphaclops.Y),
        (alphaclops.SingleQubitCliffordGate.Z, alphaclops.Z),
        (alphaclops.SingleQubitCliffordGate.X_sqrt, alphaclops.X ** 0.5),
        (alphaclops.SingleQubitCliffordGate.X_nsqrt, alphaclops.X ** -0.5),
        (alphaclops.SingleQubitCliffordGate.Y_sqrt, alphaclops.Y ** 0.5),
        (alphaclops.SingleQubitCliffordGate.Y_nsqrt, alphaclops.Y ** -0.5),
        (alphaclops.SingleQubitCliffordGate.Z_sqrt, alphaclops.Z ** 0.5),
        (alphaclops.SingleQubitCliffordGate.Z_nsqrt, alphaclops.Z ** -0.5),
    ),
)
def test_known_matrix(gate, gate_equiv):
    assert alphaclops.has_unitary(gate)
    mat = alphaclops.unitary(gate)
    mat_check = alphaclops.unitary(gate_equiv)
    assert_allclose_up_to_global_phase(mat, mat_check, rtol=1e-7, atol=1e-7)


@pytest.mark.parametrize(
    'name, expected_cls',
    [
        ('I', alphaclops.SingleQubitCliffordGate),
        ('H', alphaclops.SingleQubitCliffordGate),
        ('X', alphaclops.SingleQubitCliffordGate),
        ('Y', alphaclops.SingleQubitCliffordGate),
        ('Z', alphaclops.SingleQubitCliffordGate),
        ('S', alphaclops.SingleQubitCliffordGate),
        ('X_sqrt', alphaclops.SingleQubitCliffordGate),
        ('X_nsqrt', alphaclops.SingleQubitCliffordGate),
        ('Y_sqrt', alphaclops.SingleQubitCliffordGate),
        ('Y_nsqrt', alphaclops.SingleQubitCliffordGate),
        ('Z_sqrt', alphaclops.SingleQubitCliffordGate),
        ('Z_nsqrt', alphaclops.SingleQubitCliffordGate),
        ('CNOT', alphaclops.CliffordGate),
        ('CZ', alphaclops.CliffordGate),
        ('SWAP', alphaclops.CliffordGate),
    ],
)
def test_common_clifford_types(name: str, expected_cls: Type) -> None:
    assert isinstance(getattr(alphaclops.CliffordGate, name), expected_cls)
    assert isinstance(getattr(alphaclops.SingleQubitCliffordGate, name), expected_cls)


@pytest.mark.parametrize('gate', _all_clifford_gates())
def test_inverse(gate):
    assert gate == alphaclops.inverse(alphaclops.inverse(gate))


@pytest.mark.parametrize('gate', _all_clifford_gates())
def test_inverse_matrix(gate):
    q0 = alphaclops.NamedQubit('q0')
    mat = alphaclops.Circuit(gate(q0)).unitary()
    mat_inv = alphaclops.Circuit(alphaclops.inverse(gate)(q0)).unitary()
    assert_allclose_up_to_global_phase(mat, mat_inv.T.conj(), rtol=1e-7, atol=1e-7)


def test_commutes_notimplemented_type():
    with pytest.raises(TypeError):
        alphaclops.commutes(alphaclops.SingleQubitCliffordGate.X, 'X')
    assert alphaclops.commutes(alphaclops.SingleQubitCliffordGate.X, 'X', default='default') == 'default'

    with pytest.raises(TypeError):
        alphaclops.commutes(alphaclops.CliffordGate.X, 'X')
    assert alphaclops.commutes(alphaclops.CliffordGate.X, 'X', default='default') == 'default'


@pytest.mark.parametrize('gate,other', itertools.combinations(_all_clifford_gates(), r=2))
def test_commutes_single_qubit_gate(gate, other):
    q0 = alphaclops.NamedQubit('q0')
    gate_op = gate(q0)
    other_op = other(q0)
    mat = alphaclops.Circuit(gate_op, other_op).unitary()
    mat_swap = alphaclops.Circuit(other_op, gate_op).unitary()
    commutes = alphaclops.commutes(gate, other)
    commutes_check = alphaclops.allclose_up_to_global_phase(mat, mat_swap)
    assert commutes == commutes_check

    # Test after switching order
    mat_swap = alphaclops.Circuit(gate.equivalent_gate_before(other)(q0), gate_op).unitary()
    assert_allclose_up_to_global_phase(mat, mat_swap, rtol=1e-7, atol=1e-7)


@pytest.mark.parametrize('gate', _all_clifford_gates())
def test_parses_single_qubit_gate(gate):
    assert gate == alphaclops.read_json(json_text=(alphaclops.to_json(gate)))


@pytest.mark.parametrize(
    'gate,pauli,half_turns',
    itertools.product(_all_clifford_gates(), _paulis, (1.0, 0.25, 0.5, -0.5)),
)
def test_commutes_pauli(gate, pauli, half_turns):
    pauli_gate = pauli if half_turns == 1 else pauli**half_turns
    q0 = alphaclops.NamedQubit('q0')
    mat = alphaclops.Circuit(gate(q0), pauli_gate(q0)).unitary()
    mat_swap = alphaclops.Circuit(pauli_gate(q0), gate(q0)).unitary()
    commutes = alphaclops.commutes(gate, pauli_gate)
    commutes_check = np.allclose(mat, mat_swap)
    assert commutes == commutes_check, f"gate: {gate}, pauli {pauli}"


def test_to_clifford_tableau_util_function():

    tableau = alphaclops.ops.clifford_gate._to_clifford_tableau(
        x_to=(alphaclops.X, False), z_to=(alphaclops.Z, False)
    )
    assert tableau == alphaclops.CliffordTableau(num_qubits=1, initial_state=0)

    tableau = alphaclops.ops.clifford_gate._to_clifford_tableau(x_to=(alphaclops.X, False), z_to=(alphaclops.Z, True))
    assert tableau == alphaclops.CliffordTableau(num_qubits=1, initial_state=1)

    tableau = alphaclops.ops.clifford_gate._to_clifford_tableau(
        rotation_map={alphaclops.X: (alphaclops.X, False), alphaclops.Z: (alphaclops.Z, False)}
    )
    assert tableau == alphaclops.CliffordTableau(num_qubits=1, initial_state=0)

    tableau = alphaclops.ops.clifford_gate._to_clifford_tableau(
        rotation_map={alphaclops.X: (alphaclops.X, False), alphaclops.Z: (alphaclops.Z, True)}
    )
    assert tableau == alphaclops.CliffordTableau(num_qubits=1, initial_state=1)

    with pytest.raises(ValueError):
        alphaclops.ops.clifford_gate._to_clifford_tableau()


@pytest.mark.parametrize(
    'gate,sym,exp',
    (
        (alphaclops.SingleQubitCliffordGate.I, 'I', 1),
        (alphaclops.SingleQubitCliffordGate.H, 'H', 1),
        (alphaclops.SingleQubitCliffordGate.X, 'X', 1),
        (alphaclops.SingleQubitCliffordGate.X_sqrt, 'X', 0.5),
        (alphaclops.SingleQubitCliffordGate.X_nsqrt, 'X', -0.5),
        (
                alphaclops.SingleQubitCliffordGate.from_xz_map((alphaclops.Y, False), (alphaclops.X, True)),
            '(X^-0.5-Z^0.5)',
                1,
        ),
    ),
)
def test_text_diagram_info(gate, sym, exp):
    assert alphaclops.circuit_diagram_info(gate) == alphaclops.CircuitDiagramInfo(
        wire_symbols=(sym,), exponent=exp
    )


@pytest.mark.parametrize("clifford_gate", alphaclops.SingleQubitCliffordGate.all_single_qubit_cliffords)
def test_from_unitary(clifford_gate):
    u = alphaclops.unitary(clifford_gate)
    result_gate = alphaclops.SingleQubitCliffordGate.from_unitary(u)
    assert result_gate == clifford_gate

    result_gate2, global_phase = alphaclops.SingleQubitCliffordGate.from_unitary_with_global_phase(u)
    assert result_gate2 == result_gate
    assert np.allclose(alphaclops.unitary(result_gate2) * global_phase, u)


def test_from_unitary_with_phase_shift():
    u = np.exp(0.42j) * alphaclops.unitary(alphaclops.SingleQubitCliffordGate.Y_sqrt)
    gate = alphaclops.SingleQubitCliffordGate.from_unitary(u)

    assert gate == alphaclops.SingleQubitCliffordGate.Y_sqrt

    gate2, global_phase = alphaclops.SingleQubitCliffordGate.from_unitary_with_global_phase(u)
    assert gate2 == gate
    assert np.allclose(alphaclops.unitary(gate2) * global_phase, u)


def test_from_unitary_not_clifford():
    # Not a single-qubit gate.
    u = alphaclops.unitary(alphaclops.CNOT)
    assert alphaclops.SingleQubitCliffordGate.from_unitary(u) is None
    assert alphaclops.SingleQubitCliffordGate.from_unitary_with_global_phase(u) is None

    # Not an unitary matrix.
    u = 2 * alphaclops.unitary(alphaclops.X)
    assert alphaclops.SingleQubitCliffordGate.from_unitary(u) is None
    assert alphaclops.SingleQubitCliffordGate.from_unitary_with_global_phase(u) is None

    # Not a Clifford gate.
    u = alphaclops.unitary(alphaclops.T)
    assert alphaclops.SingleQubitCliffordGate.from_unitary(u) is None
    assert alphaclops.SingleQubitCliffordGate.from_unitary_with_global_phase(u) is None


@pytest.mark.parametrize("clifford_gate", alphaclops.SingleQubitCliffordGate.all_single_qubit_cliffords)
def test_decompose_gate(clifford_gate):
    gates = clifford_gate.decompose_gate()
    u = functools.reduce(np.dot, [np.eye(2), *(alphaclops.unitary(gate) for gate in reversed(gates))])
    assert np.allclose(u, alphaclops.unitary(clifford_gate))  # No global phase difference.


@pytest.mark.parametrize('trans_x,trans_z', _all_rotation_pairs())
def test_to_phased_xz_gate(trans_x, trans_z):
    gate = alphaclops.SingleQubitCliffordGate.from_xz_map(trans_x, trans_z)
    actual_phased_xz_gate = gate.to_phased_xz_gate()._canonical()
    expect_phased_xz_gates = alphaclops.PhasedXZGate.from_matrix(alphaclops.unitary(gate))

    assert np.isclose(actual_phased_xz_gate.x_exponent, expect_phased_xz_gates.x_exponent)
    assert np.isclose(actual_phased_xz_gate.z_exponent, expect_phased_xz_gates.z_exponent)
    assert np.isclose(
        actual_phased_xz_gate.axis_phase_exponent, expect_phased_xz_gates.axis_phase_exponent
    )


def test_from_xz_to_clifford_tableau():
    seen_tableau = []
    for trans_x, trans_z in _all_rotation_pairs():
        tableau = alphaclops.SingleQubitCliffordGate.from_xz_map(trans_x, trans_z).clifford_tableau
        tableau_number = sum(2**i * t for i, t in enumerate(tableau.matrix().ravel()))
        tableau_number = tableau_number * 4 + 2 * tableau.rs[0] + tableau.rs[1]
        seen_tableau.append(tableau_number)
        # Satisfy the symplectic property
        assert sum(tableau.matrix()[0, :2] * tableau.matrix()[1, 1::-1]) % 2 == 1

    # Should not have any duplication.
    assert len(set(seen_tableau)) == 24


@pytest.mark.parametrize(
    'clifford_gate,standard_gate',
    [
        (alphaclops.CliffordGate.I, alphaclops.I),
        (alphaclops.CliffordGate.X, alphaclops.X),
        (alphaclops.CliffordGate.Y, alphaclops.Y),
        (alphaclops.CliffordGate.Z, alphaclops.Z),
        (alphaclops.CliffordGate.H, alphaclops.H),
        (alphaclops.CliffordGate.S, alphaclops.S),
        (alphaclops.CliffordGate.CNOT, alphaclops.CNOT),
        (alphaclops.CliffordGate.CZ, alphaclops.CZ),
        (alphaclops.CliffordGate.SWAP, alphaclops.SWAP),
    ],
)
def test_common_clifford_gate(clifford_gate, standard_gate):
    # alphaclops.unitary is relied on the _decompose_ methods.
    u_c = alphaclops.unitary(clifford_gate)
    u_s = alphaclops.unitary(standard_gate)
    alphaclops.testing.assert_allclose_up_to_global_phase(u_c, u_s, atol=1e-8)


@pytest.mark.parametrize('property_name', ("all_single_qubit_cliffords", "CNOT", "CZ", "SWAP"))
def test_common_clifford_gate_caching(property_name):
    cache_name = f"_{property_name}"
    delattr(alphaclops.CliffordGate, cache_name)
    assert not hasattr(alphaclops.CliffordGate, cache_name)
    _ = getattr(alphaclops.CliffordGate, property_name)
    assert hasattr(alphaclops.CliffordGate, cache_name)


def test_multi_qubit_clifford_pow():
    assert alphaclops.CliffordGate.X ** -1 == alphaclops.CliffordGate.X
    assert alphaclops.CliffordGate.H ** -1 == alphaclops.CliffordGate.H
    assert alphaclops.CliffordGate.S ** 2 == alphaclops.CliffordGate.Z
    assert alphaclops.CliffordGate.S ** -1 == alphaclops.CliffordGate.S ** 3
    assert alphaclops.CliffordGate.S ** -3 == alphaclops.CliffordGate.S
    assert alphaclops.CliffordGate.CNOT ** 3 == alphaclops.CliffordGate.CNOT
    assert alphaclops.CliffordGate.CNOT ** -3 == alphaclops.CliffordGate.CNOT
    with pytest.raises(TypeError):
        _ = alphaclops.CliffordGate.Z ** 0.25


def test_stabilizer_effec():
    assert alphaclops.has_stabilizer_effect(alphaclops.CliffordGate.X)
    assert alphaclops.has_stabilizer_effect(alphaclops.CliffordGate.H)
    assert alphaclops.has_stabilizer_effect(alphaclops.CliffordGate.S)
    assert alphaclops.has_stabilizer_effect(alphaclops.CliffordGate.CNOT)
    assert alphaclops.has_stabilizer_effect(alphaclops.CliffordGate.CZ)
    qubits = alphaclops.LineQubit.range(2)
    gate = alphaclops.CliffordGate.from_op_list(
        [alphaclops.H(qubits[1]), alphaclops.CZ(*qubits), alphaclops.H(qubits[1])], qubits
    )
    assert alphaclops.has_stabilizer_effect(gate)


def test_clifford_gate_from_op_list():
    # Since from_op_list() ==> _act_on_() ==> tableau.then() and then() has already covered
    # lots of random circuit cases, here we just test a few well-known relationships.
    qubit = alphaclops.NamedQubit('test')
    gate = alphaclops.CliffordGate.from_op_list([alphaclops.X(qubit), alphaclops.Z(qubit)], [qubit])
    assert gate == alphaclops.CliffordGate.Y  # The tableau ignores the global phase

    gate = alphaclops.CliffordGate.from_op_list([alphaclops.Z(qubit), alphaclops.X(qubit)], [qubit])
    assert gate == alphaclops.CliffordGate.Y  # The tableau ignores the global phase

    gate = alphaclops.CliffordGate.from_op_list([alphaclops.X(qubit), alphaclops.Y(qubit)], [qubit])
    assert gate == alphaclops.CliffordGate.Z  # The tableau ignores the global phase

    gate = alphaclops.CliffordGate.from_op_list([alphaclops.Z(qubit), alphaclops.X(qubit)], [qubit])
    assert gate == alphaclops.CliffordGate.Y  # The tableau ignores the global phase

    # Two qubits gates
    qubits = alphaclops.LineQubit.range(2)
    gate = alphaclops.CliffordGate.from_op_list(
        [alphaclops.H(qubits[1]), alphaclops.CZ(*qubits), alphaclops.H(qubits[1])], qubits
    )
    assert gate == alphaclops.CliffordGate.CNOT

    gate = alphaclops.CliffordGate.from_op_list(
        [alphaclops.H(qubits[1]), alphaclops.CNOT(*qubits), alphaclops.H(qubits[1])], qubits
    )
    assert gate == alphaclops.CliffordGate.CZ

    # Note the order of qubits matters
    gate = alphaclops.CliffordGate.from_op_list(
        [alphaclops.H(qubits[0]), alphaclops.CZ(qubits[1], qubits[0]), alphaclops.H(qubits[0])], qubits
    )
    assert gate != alphaclops.CliffordGate.CNOT
    # But if we reverse the qubit_order, they will equal again.
    gate = alphaclops.CliffordGate.from_op_list(
        [alphaclops.H(qubits[0]), alphaclops.CZ(qubits[1], qubits[0]), alphaclops.H(qubits[0])], qubits[::-1]
    )
    assert gate == alphaclops.CliffordGate.CNOT

    with pytest.raises(
        ValueError, match="only be constructed from the operations that has stabilizer effect"
    ):
        alphaclops.CliffordGate.from_op_list([alphaclops.T(qubit)], [qubit])


def test_clifford_gate_from_tableau():
    t = alphaclops.CliffordGate.X.clifford_tableau
    assert alphaclops.CliffordGate.from_clifford_tableau(t) == alphaclops.CliffordGate.X

    t = alphaclops.CliffordGate.H.clifford_tableau
    assert alphaclops.CliffordGate.from_clifford_tableau(t) == alphaclops.CliffordGate.H

    t = alphaclops.CliffordGate.CNOT.clifford_tableau
    assert alphaclops.CliffordGate.from_clifford_tableau(t) == alphaclops.CliffordGate.CNOT

    with pytest.raises(ValueError, match='Input argument has to be a CliffordTableau instance.'):
        alphaclops.SingleQubitCliffordGate.from_clifford_tableau(123)

    with pytest.raises(ValueError, match="The number of qubit of input tableau should be 1"):
        t = alphaclops.CliffordTableau(num_qubits=2)
        alphaclops.SingleQubitCliffordGate.from_clifford_tableau(t)

    with pytest.raises(ValueError):
        t = alphaclops.CliffordTableau(num_qubits=1)
        t.xs = np.array([1, 1]).reshape(2, 1)
        t.zs = np.array([1, 1]).reshape(2, 1)  # This violates the sympletic property.
        alphaclops.CliffordGate.from_clifford_tableau(t)

    with pytest.raises(ValueError, match="Input argument has to be a CliffordTableau instance."):
        alphaclops.CliffordGate.from_clifford_tableau(1)


def test_multi_clifford_decompose_by_unitary():
    # Construct a random clifford gate:
    n, num_ops = 5, 20  # because we relied on unitary cannot test large-scale qubits
    gate_candidate = [alphaclops.X, alphaclops.Y, alphaclops.Z, alphaclops.H, alphaclops.S, alphaclops.CNOT, alphaclops.CZ]
    for _ in range(10):
        qubits = alphaclops.LineQubit.range(n)
        ops = []
        for _ in range(num_ops):
            g = np.random.randint(len(gate_candidate))
            indices = (np.random.randint(n),) if g < 5 else np.random.choice(n, 2, replace=False)
            ops.append(gate_candidate[g].on(*[qubits[i] for i in indices]))
        gate = alphaclops.CliffordGate.from_op_list(ops, qubits)
        decomposed_ops = alphaclops.decompose(gate.on(*qubits))
        circ = alphaclops.Circuit(decomposed_ops)
        circ.append(alphaclops.I.on_each(qubits))  # make sure the dimension aligned.
        alphaclops.testing.assert_allclose_up_to_global_phase(
            alphaclops.unitary(gate), alphaclops.unitary(circ), atol=1e-7
        )


def test_pad_tableau_bad_input():
    with pytest.raises(
        ValueError, match="Input axes of padding should match with the number of qubits"
    ):
        tableau = alphaclops.CliffordTableau(num_qubits=3)
        alphaclops.ops.clifford_gate._pad_tableau(tableau, num_qubits_after_padding=4, axes=[1, 2])

    with pytest.raises(
        ValueError, match='The number of qubits in the input tableau should not be larger than'
    ):
        tableau = alphaclops.CliffordTableau(num_qubits=3)
        alphaclops.ops.clifford_gate._pad_tableau(tableau, num_qubits_after_padding=2, axes=[0, 1, 2])


def test_pad_tableau():
    tableau = alphaclops.CliffordTableau(num_qubits=1)
    padded_tableau = alphaclops.ops.clifford_gate._pad_tableau(
        tableau, num_qubits_after_padding=2, axes=[0]
    )
    assert padded_tableau == alphaclops.CliffordTableau(num_qubits=2)

    tableau = alphaclops.CliffordTableau(num_qubits=1, initial_state=1)
    padded_tableau = alphaclops.ops.clifford_gate._pad_tableau(
        tableau, num_qubits_after_padding=1, axes=[0]
    )
    assert padded_tableau == alphaclops.CliffordGate.X.clifford_tableau

    # Tableau for H
    # [0 1 0]
    # [1 0 0]
    tableau = alphaclops.CliffordGate.H.clifford_tableau
    padded_tableau = alphaclops.ops.clifford_gate._pad_tableau(
        tableau, num_qubits_after_padding=2, axes=[0]
    )
    # fmt: off
    np.testing.assert_equal(
        padded_tableau.matrix().astype(np.int64),
        np.array([[0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1]]),
    )
    # fmt: on
    np.testing.assert_equal(padded_tableau.rs.astype(np.int64), np.zeros(4))
    # The tableau of H again but pad for another ax
    tableau = alphaclops.CliffordGate.H.clifford_tableau
    padded_tableau = alphaclops.ops.clifford_gate._pad_tableau(
        tableau, num_qubits_after_padding=2, axes=[1]
    )
    # fmt: off
    np.testing.assert_equal(
        padded_tableau.matrix().astype(np.int64),
        np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]),
    )
    # fmt: on
    np.testing.assert_equal(padded_tableau.rs.astype(np.int64), np.zeros(4))


def test_clifford_gate_act_on_small_case():
    # Note this is also covered by the `from_op_list` one, etc.

    qubits = alphaclops.LineQubit.range(5)
    args = alphaclops.CliffordTableauSimulationState(
        tableau=alphaclops.CliffordTableau(num_qubits=5), qubits=qubits, prng=np.random.RandomState()
    )
    expected_args = alphaclops.CliffordTableauSimulationState(
        tableau=alphaclops.CliffordTableau(num_qubits=5), qubits=qubits, prng=np.random.RandomState()
    )
    alphaclops.act_on(alphaclops.H, expected_args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.CliffordGate.H, args, qubits=[qubits[0]], allow_decompose=False)
    assert args.tableau == expected_args.tableau

    alphaclops.act_on(alphaclops.CNOT, expected_args, qubits=[qubits[0], qubits[1]], allow_decompose=False)
    alphaclops.act_on(alphaclops.CliffordGate.CNOT, args, qubits=[qubits[0], qubits[1]], allow_decompose=False)
    assert args.tableau == expected_args.tableau

    alphaclops.act_on(alphaclops.H, expected_args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.CliffordGate.H, args, qubits=[qubits[0]], allow_decompose=False)
    assert args.tableau == expected_args.tableau

    alphaclops.act_on(alphaclops.S, expected_args, qubits=[qubits[0]], allow_decompose=False)
    alphaclops.act_on(alphaclops.CliffordGate.S, args, qubits=[qubits[0]], allow_decompose=False)
    assert args.tableau == expected_args.tableau

    alphaclops.act_on(alphaclops.X, expected_args, qubits=[qubits[2]], allow_decompose=False)
    alphaclops.act_on(alphaclops.CliffordGate.X, args, qubits=[qubits[2]], allow_decompose=False)
    assert args.tableau == expected_args.tableau


def test_clifford_gate_act_on_large_case():
    n, num_ops = 50, 1000  # because we don't need unitary, it is fast.
    gate_candidate = [alphaclops.X, alphaclops.Y, alphaclops.Z, alphaclops.H, alphaclops.S, alphaclops.CNOT, alphaclops.CZ]
    for seed in range(10):
        prng = np.random.RandomState(seed)
        t1 = alphaclops.CliffordTableau(num_qubits=n)
        t2 = alphaclops.CliffordTableau(num_qubits=n)
        qubits = alphaclops.LineQubit.range(n)
        args1 = alphaclops.CliffordTableauSimulationState(tableau=t1, qubits=qubits, prng=prng)
        args2 = alphaclops.CliffordTableauSimulationState(tableau=t2, qubits=qubits, prng=prng)
        ops = []
        for _ in range(0, num_ops, 100):
            g = prng.randint(len(gate_candidate))
            indices = (prng.randint(n),) if g < 5 else prng.choice(n, 2, replace=False)
            alphaclops.act_on(
                gate_candidate[g], args1, qubits=[qubits[i] for i in indices], allow_decompose=False
            )
            ops.append(gate_candidate[g].on(*[qubits[i] for i in indices]))
        compiled_gate = alphaclops.CliffordGate.from_op_list(ops, qubits)
        alphaclops.act_on(compiled_gate, args2, qubits)

        assert args1.tableau == args2.tableau


def test_clifford_gate_act_on_ch_form():
    # Although we don't support CH_form from the _act_on_, it will fall back
    # to the decomposititon method and apply it through decomposed ops.
    # Here we run it for the coverage only.
    args = alphaclops.StabilizerChFormSimulationState(
        initial_state=alphaclops.StabilizerStateChForm(num_qubits=2, initial_state=1),
        qubits=alphaclops.LineQubit.range(2),
        prng=np.random.RandomState(),
    )
    alphaclops.act_on(alphaclops.CliffordGate.X, args, qubits=alphaclops.LineQubit.range(1))
    np.testing.assert_allclose(args.state.state_vector(), np.array([0, 0, 0, 1]))


def test_clifford_gate_act_on_fail():
    with pytest.raises(TypeError, match="Failed to act"):
        alphaclops.act_on(alphaclops.CliffordGate.X, DummySimulationState(), qubits=())


def test_all_single_qubit_clifford_unitaries():
    i = np.eye(2)
    x = np.array([[0, 1], [1, 0]])
    y = np.array([[0, -1j], [1j, 0]])
    z = np.diag([1, -1])

    cs = [alphaclops.unitary(c) for c in alphaclops.CliffordGate.all_single_qubit_cliffords]

    # Identity
    assert alphaclops.equal_up_to_global_phase(cs[0], i)
    # Paulis
    assert alphaclops.equal_up_to_global_phase(cs[1], x)
    assert alphaclops.equal_up_to_global_phase(cs[2], y)
    assert alphaclops.equal_up_to_global_phase(cs[3], z)
    # Square roots of Paulis
    assert alphaclops.equal_up_to_global_phase(cs[4], (i - 1j * x) / np.sqrt(2))
    assert alphaclops.equal_up_to_global_phase(cs[5], (i - 1j * y) / np.sqrt(2))
    assert alphaclops.equal_up_to_global_phase(cs[6], (i - 1j * z) / np.sqrt(2))
    # Negative square roots of Paulis
    assert alphaclops.equal_up_to_global_phase(cs[7], (i + 1j * x) / np.sqrt(2))
    assert alphaclops.equal_up_to_global_phase(cs[8], (i + 1j * y) / np.sqrt(2))
    assert alphaclops.equal_up_to_global_phase(cs[9], (i + 1j * z) / np.sqrt(2))
    # Hadamards
    assert alphaclops.equal_up_to_global_phase(cs[10], (z + x) / np.sqrt(2))
    assert alphaclops.equal_up_to_global_phase(cs[11], (x + y) / np.sqrt(2))
    assert alphaclops.equal_up_to_global_phase(cs[12], (y + z) / np.sqrt(2))
    assert alphaclops.equal_up_to_global_phase(cs[13], (z - x) / np.sqrt(2))
    assert alphaclops.equal_up_to_global_phase(cs[14], (x - y) / np.sqrt(2))
    assert alphaclops.equal_up_to_global_phase(cs[15], (y - z) / np.sqrt(2))
    # Order-3 Cliffords
    assert alphaclops.equal_up_to_global_phase(cs[16], (i - 1j * (x + y + z)) / 2)
    assert alphaclops.equal_up_to_global_phase(cs[17], (i - 1j * (x + y - z)) / 2)
    assert alphaclops.equal_up_to_global_phase(cs[18], (i - 1j * (x - y + z)) / 2)
    assert alphaclops.equal_up_to_global_phase(cs[19], (i - 1j * (x - y - z)) / 2)
    assert alphaclops.equal_up_to_global_phase(cs[20], (i - 1j * (-x + y + z)) / 2)
    assert alphaclops.equal_up_to_global_phase(cs[21], (i - 1j * (-x + y - z)) / 2)
    assert alphaclops.equal_up_to_global_phase(cs[22], (i - 1j * (-x - y + z)) / 2)
    assert alphaclops.equal_up_to_global_phase(cs[23], (i - 1j * (-x - y - z)) / 2)
