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
import pytest
import numpy as np
import sympy


import alphaclops


_bools = (False, True)
_paulis = (alphaclops.X, alphaclops.Y, alphaclops.Z)


def _all_interaction_gates(exponents=(1,)):
    for pauli0, invert0, pauli1, invert1, e in itertools.product(
        _paulis, _bools, _paulis, _bools, exponents
    ):
        yield alphaclops.PauliInteractionGate(pauli0, invert0, pauli1, invert1, exponent=e)


@pytest.mark.parametrize('gate', _all_interaction_gates())
def test_pauli_interaction_gates_consistent_protocols(gate):
    alphaclops.testing.assert_implements_consistent_protocols(gate)


def test_eq_ne_and_hash():
    eq = alphaclops.testing.EqualsTester()
    for pauli0, invert0, pauli1, invert1, e in itertools.product(
        _paulis, _bools, _paulis, _bools, (0.125, -0.25, 1)
    ):
        eq.add_equality_group(
            alphaclops.PauliInteractionGate(pauli0, invert0, pauli1, invert1, exponent=e)
        )


def test_exponent_shifts_are_equal():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(
        alphaclops.PauliInteractionGate(alphaclops.X, False, alphaclops.X, False, exponent=e)
        for e in [0.1, 0.1, 2.1, -1.9, 4.1]
    )
    eq.add_equality_group(
        alphaclops.PauliInteractionGate(alphaclops.X, True, alphaclops.X, False, exponent=e)
        for e in [0.1, 0.1, 2.1, -1.9, 4.1]
    )
    eq.add_equality_group(
        alphaclops.PauliInteractionGate(alphaclops.Y, False, alphaclops.Z, False, exponent=e)
        for e in [0.1, 0.1, 2.1, -1.9, 4.1]
    )
    eq.add_equality_group(
        alphaclops.PauliInteractionGate(alphaclops.Z, False, alphaclops.Y, True, exponent=e)
        for e in [0.1, 0.1, 2.1, -1.9, 4.1]
    )


@pytest.mark.parametrize('gate', _all_interaction_gates(exponents=(0.1, -0.25, 0.5, 1)))
def test_interchangeable_qubits(gate):
    q0, q1 = alphaclops.NamedQubit('q0'), alphaclops.NamedQubit('q1')
    op0 = gate(q0, q1)
    op1 = gate(q1, q0)
    mat0 = alphaclops.Circuit(op0).unitary()
    mat1 = alphaclops.Circuit(op1).unitary()
    same = op0 == op1
    same_check = alphaclops.allclose_up_to_global_phase(mat0, mat1)
    assert same == same_check


def test_exponent():
    cnot = alphaclops.PauliInteractionGate(alphaclops.Z, False, alphaclops.X, False)
    np.testing.assert_almost_equal(
        alphaclops.unitary(cnot ** 0.5),
        np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0.5 + 0.5j, 0.5 - 0.5j],
                [0, 0, 0.5 - 0.5j, 0.5 + 0.5j],
            ]
        ),
    )


def test_repr():
    cnot = alphaclops.PauliInteractionGate(alphaclops.Z, False, alphaclops.X, False)
    alphaclops.testing.assert_equivalent_repr(cnot)


def test_decomposes_despite_symbol():
    q0, q1 = alphaclops.NamedQubit('q0'), alphaclops.NamedQubit('q1')
    gate = alphaclops.PauliInteractionGate(alphaclops.Z, False, alphaclops.X, False, exponent=sympy.Symbol('x'))
    assert alphaclops.decompose_once_with_qubits(gate, [q0, q1])


def test_text_diagrams():
    q0, q1 = alphaclops.NamedQubit('q0'), alphaclops.NamedQubit('q1')
    circuit = alphaclops.Circuit(
        alphaclops.PauliInteractionGate(alphaclops.X, False, alphaclops.X, False)(q0, q1),
        alphaclops.PauliInteractionGate(alphaclops.X, True, alphaclops.X, False)(q0, q1),
        alphaclops.PauliInteractionGate(alphaclops.X, False, alphaclops.X, True)(q0, q1),
        alphaclops.PauliInteractionGate(alphaclops.X, True, alphaclops.X, True)(q0, q1),
        alphaclops.PauliInteractionGate(alphaclops.X, False, alphaclops.Y, False)(q0, q1),
        alphaclops.PauliInteractionGate(alphaclops.Y, False, alphaclops.Z, False)(q0, q1),
        alphaclops.PauliInteractionGate(alphaclops.Z, False, alphaclops.Y, False)(q0, q1),
        alphaclops.PauliInteractionGate(alphaclops.Y, True, alphaclops.Z, True)(q0, q1),
        alphaclops.PauliInteractionGate(alphaclops.Z, True, alphaclops.Y, True)(q0, q1),
    )
    assert (
        circuit.to_text_diagram().strip()
        == """
q0: ───X───(-X)───X──────(-X)───X───Y───@───(-Y)───(-@)───
       │   │      │      │      │   │   │   │      │
q1: ───X───X──────(-X)───(-X)───Y───@───Y───(-@)───(-Y)───
    """.strip()
    )
