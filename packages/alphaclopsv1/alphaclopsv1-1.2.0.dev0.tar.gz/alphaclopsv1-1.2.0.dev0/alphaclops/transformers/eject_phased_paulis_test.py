# Copyright 2022 The alphaclops Developers
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
from typing import cast, Iterable

import dataclasses
import numpy as np
import pytest
import sympy

import alphaclops


def assert_optimizes(
    before: alphaclops.Circuit,
    expected: alphaclops.Circuit,
    compare_unitaries: bool = True,
    eject_parameterized: bool = False,
    *,
    with_context: bool = False,
):
    context = alphaclops.TransformerContext(tags_to_ignore=("nocompile",)) if with_context else None
    circuit = alphaclops.eject_phased_paulis(
        before, eject_parameterized=eject_parameterized, context=context
    )

    # They should have equivalent effects.
    if compare_unitaries:
        if alphaclops.is_parameterized(circuit):
            for a in (0, 0.1, 0.5, -1.0, np.pi, np.pi / 2):
                params: alphaclops.ParamDictType = {'x': a, 'y': a / 2, 'z': -2 * a}
                (
                    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(
                        alphaclops.resolve_parameters(circuit, params),
                        alphaclops.resolve_parameters(expected, params),
                        1e-8,
                    )
                )
        else:
            (
                alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(
                    circuit, expected, 1e-8
                )
            )

    # And match the expected circuit.
    alphaclops.testing.assert_same_circuits(circuit, expected)

    # And it should be idempotent.
    circuit = alphaclops.eject_phased_paulis(
        circuit, eject_parameterized=eject_parameterized, context=context
    )
    alphaclops.testing.assert_same_circuits(circuit, expected)

    # Nested sub-circuits should also get optimized.
    q = before.all_qubits()
    c_nested = alphaclops.Circuit(
        [alphaclops.PhasedXPowGate(phase_exponent=0.5).on_each(*q), (alphaclops.Z ** 0.5).on_each(*q)],
        alphaclops.CircuitOperation(before.freeze()).repeat(2).with_tags("ignore"),
        [alphaclops.Y.on_each(*q), alphaclops.X.on_each(*q)],
        alphaclops.CircuitOperation(before.freeze()).repeat(3).with_tags("preserve_tag"),
    )
    c_expected = alphaclops.Circuit(
        alphaclops.PhasedXPowGate(phase_exponent=0.75).on_each(*q),
        alphaclops.Moment(alphaclops.CircuitOperation(before.freeze()).repeat(2).with_tags("ignore")),
        alphaclops.Z.on_each(*q),
        alphaclops.Moment(alphaclops.CircuitOperation(expected.freeze()).repeat(3).with_tags("preserve_tag")),
    )
    if context is None:
        context = alphaclops.TransformerContext(tags_to_ignore=("ignore",), deep=True)
    else:
        context = dataclasses.replace(
            context, tags_to_ignore=context.tags_to_ignore + ("ignore",), deep=True
        )
    c_nested = alphaclops.eject_phased_paulis(
        c_nested, context=context, eject_parameterized=eject_parameterized
    )
    alphaclops.testing.assert_same_circuits(c_nested, c_expected)
    c_nested = alphaclops.eject_phased_paulis(
        c_nested, context=context, eject_parameterized=eject_parameterized
    )
    alphaclops.testing.assert_same_circuits(c_nested, c_expected)


def quick_circuit(*moments: Iterable[alphaclops.OP_TREE]) -> alphaclops.Circuit:
    return alphaclops.Circuit(
        [alphaclops.Moment(cast(Iterable[alphaclops.Operation], alphaclops.flatten_op_tree(m))) for m in moments]
    )


def test_absorbs_z():
    q = alphaclops.NamedQubit('q')
    x = sympy.Symbol('x')

    # Full Z.
    assert_optimizes(
        before=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.125).on(q)], [alphaclops.Z(q)]),
        expected=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.625).on(q)]),
    )

    # PhasedXZGate
    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.125).on(q)],
            [alphaclops.PhasedXZGate(x_exponent=0, axis_phase_exponent=0, z_exponent=1).on(q)],
        ),
        expected=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.625).on(q)]),
    )

    # Partial Z. PhasedXZGate with z_exponent = 0.
    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXZGate(x_exponent=1, axis_phase_exponent=0.125, z_exponent=0).on(q)],
            [alphaclops.S(q)],
        ),
        expected=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.375).on(q)]),
    )

    # parameterized Z.
    assert_optimizes(
        before=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.125).on(q)], [alphaclops.Z(q) ** x]),
        expected=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.125 + x / 2).on(q)]),
        eject_parameterized=True,
    )
    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.125).on(q)], [alphaclops.Z(q) ** (x + 1)]
        ),
        expected=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.625 + x / 2).on(q)]),
        eject_parameterized=True,
    )

    # Multiple Zs.
    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.125).on(q)], [alphaclops.S(q)], [alphaclops.T(q) ** -1]
        ),
        expected=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.25).on(q)]),
    )

    # Multiple Parameterized Zs.
    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.125).on(q)], [alphaclops.S(q) ** x], [alphaclops.T(q) ** -x]
        ),
        expected=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.125 + x * 0.125).on(q)]),
        eject_parameterized=True,
    )

    # Parameterized Phase and Partial Z
    assert_optimizes(
        before=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=x).on(q)], [alphaclops.S(q)]),
        expected=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=x + 0.25).on(q)]),
        eject_parameterized=True,
    )


def test_crosses_czs():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    z = sympy.Symbol('z')

    # Full CZ.
    assert_optimizes(
        before=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.25).on(a)], [alphaclops.CZ(a, b)]),
        expected=quick_circuit(
            [alphaclops.Z(b)], [alphaclops.CZ(a, b)], [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(a)]
        ),
    )
    assert_optimizes(
        before=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.125).on(a)], [alphaclops.CZ(b, a)]),
        expected=quick_circuit(
            [alphaclops.Z(b)], [alphaclops.CZ(a, b)], [alphaclops.PhasedXPowGate(phase_exponent=0.125).on(a)]
        ),
    )
    assert_optimizes(
        before=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=x).on(a)], [alphaclops.CZ(b, a)]),
        expected=quick_circuit(
            [alphaclops.Z(b)], [alphaclops.CZ(a, b)], [alphaclops.PhasedXPowGate(phase_exponent=x).on(a)]
        ),
        eject_parameterized=True,
    )

    # Partial CZ.
    assert_optimizes(
        before=quick_circuit([alphaclops.X(a)], [alphaclops.CZ(a, b) ** 0.25]),
        expected=quick_circuit([alphaclops.Z(b) ** 0.25], [alphaclops.CZ(a, b) ** -0.25], [alphaclops.X(a)]),
    )
    assert_optimizes(
        before=quick_circuit([alphaclops.X(a)], [alphaclops.CZ(a, b) ** x]),
        expected=quick_circuit([alphaclops.Z(b) ** x], [alphaclops.CZ(a, b) ** -x], [alphaclops.X(a)]),
        eject_parameterized=True,
    )

    # Double cross.
    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.125).on(a)],
            [alphaclops.PhasedXPowGate(phase_exponent=0.375).on(b)],
            [alphaclops.CZ(a, b) ** 0.25],
        ),
        expected=quick_circuit(
            [alphaclops.CZ(a, b) ** 0.25],
            [
                alphaclops.PhasedXPowGate(phase_exponent=0.5).on(b),
                alphaclops.PhasedXPowGate(phase_exponent=0.25).on(a),
            ],
        ),
    )
    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=x).on(a)],
            [alphaclops.PhasedXPowGate(phase_exponent=y).on(b)],
            [alphaclops.CZ(a, b) ** z],
        ),
        expected=quick_circuit(
            [alphaclops.CZ(a, b) ** z],
            [
                alphaclops.PhasedXPowGate(phase_exponent=y + z / 2).on(b),
                alphaclops.PhasedXPowGate(phase_exponent=x + z / 2).on(a),
            ],
        ),
        eject_parameterized=True,
    )


def test_toggles_measurements():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    x = sympy.Symbol('x')

    # Single.
    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(a)], [alphaclops.measure(a, b)]
        ),
        expected=quick_circuit([alphaclops.measure(a, b, invert_mask=(True,))]),
    )
    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(b)], [alphaclops.measure(a, b)]
        ),
        expected=quick_circuit([alphaclops.measure(a, b, invert_mask=(False, True))]),
    )
    assert_optimizes(
        before=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=x).on(b)], [alphaclops.measure(a, b)]),
        expected=quick_circuit([alphaclops.measure(a, b, invert_mask=(False, True))]),
        eject_parameterized=True,
    )

    # Multiple.
    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(a)],
            [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(b)],
            [alphaclops.measure(a, b)],
        ),
        expected=quick_circuit([alphaclops.measure(a, b, invert_mask=(True, True))]),
    )

    # Xmon.
    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(a)], [alphaclops.measure(a, b, key='t')]
        ),
        expected=quick_circuit([alphaclops.measure(a, b, invert_mask=(True,), key='t')]),
    )

    # CCOs
    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(a)],
            [alphaclops.measure(a, key="m")],
            [alphaclops.X(b).with_classical_controls("m")],
        ),
        expected=quick_circuit(
            [alphaclops.measure(a, invert_mask=(True,), key="m")],
            [alphaclops.X(b).with_classical_controls("m")],
        ),
        compare_unitaries=False,
    )


def test_eject_phased_xz():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.Circuit(
        alphaclops.PhasedXZGate(x_exponent=1, z_exponent=0.5, axis_phase_exponent=0.5).on(a),
        alphaclops.CZ(a, b) ** 0.25,
    )
    c_expected = alphaclops.Circuit(
        alphaclops.CZ(a, b) ** -0.25, alphaclops.PhasedXPowGate(phase_exponent=0.75).on(a), alphaclops.T(b)
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.eject_z(alphaclops.eject_phased_paulis(alphaclops.eject_z(c))), c_expected
    )
    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(c, c_expected, 1e-8)


def test_cancels_other_full_w():
    q = alphaclops.NamedQubit('q')
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')

    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(q)],
            [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(q)],
        ),
        expected=quick_circuit(),
    )

    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=x).on(q)],
            [alphaclops.PhasedXPowGate(phase_exponent=x).on(q)],
        ),
        expected=quick_circuit(),
        eject_parameterized=True,
    )

    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(q)],
            [alphaclops.PhasedXPowGate(phase_exponent=0.125).on(q)],
        ),
        expected=quick_circuit([alphaclops.Z(q) ** -0.25]),
    )

    assert_optimizes(
        before=quick_circuit([alphaclops.X(q)], [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(q)]),
        expected=quick_circuit([alphaclops.Z(q) ** 0.5]),
    )

    assert_optimizes(
        before=quick_circuit([alphaclops.Y(q)], [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(q)]),
        expected=quick_circuit([alphaclops.Z(q) ** -0.5]),
    )

    assert_optimizes(
        before=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.25).on(q)], [alphaclops.X(q)]),
        expected=quick_circuit([alphaclops.Z(q) ** -0.5]),
    )

    assert_optimizes(
        before=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.25).on(q)], [alphaclops.Y(q)]),
        expected=quick_circuit([alphaclops.Z(q) ** 0.5]),
    )

    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=x).on(q)],
            [alphaclops.PhasedXPowGate(phase_exponent=y).on(q)],
        ),
        expected=quick_circuit([alphaclops.Z(q) ** (2 * (y - x))]),
        eject_parameterized=True,
    )


def test_phases_partial_ws():
    q = alphaclops.NamedQubit('q')
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    z = sympy.Symbol('z')

    assert_optimizes(
        before=quick_circuit(
            [alphaclops.X(q)], [alphaclops.PhasedXPowGate(phase_exponent=0.25, exponent=0.5).on(q)]
        ),
        expected=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=-0.25, exponent=0.5).on(q)], [alphaclops.X(q)]
        ),
    )

    assert_optimizes(
        before=quick_circuit([alphaclops.PhasedXPowGate(phase_exponent=0.25).on(q)], [alphaclops.X(q) ** 0.5]),
        expected=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.5, exponent=0.5).on(q)],
            [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(q)],
        ),
    )

    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(q)],
            [alphaclops.PhasedXPowGate(phase_exponent=0.5, exponent=0.75).on(q)],
        ),
        expected=quick_circuit(
            [alphaclops.X(q) ** 0.75], [alphaclops.PhasedXPowGate(phase_exponent=0.25).on(q)]
        ),
    )

    assert_optimizes(
        before=quick_circuit(
            [alphaclops.X(q)], [alphaclops.PhasedXPowGate(exponent=-0.25, phase_exponent=0.5).on(q)]
        ),
        expected=quick_circuit(
            [alphaclops.PhasedXPowGate(exponent=-0.25, phase_exponent=-0.5).on(q)], [alphaclops.X(q)]
        ),
    )

    assert_optimizes(
        before=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=x).on(q)],
            [alphaclops.PhasedXPowGate(phase_exponent=y, exponent=z).on(q)],
        ),
        expected=quick_circuit(
            [alphaclops.PhasedXPowGate(phase_exponent=2 * x - y, exponent=z).on(q)],
            [alphaclops.PhasedXPowGate(phase_exponent=x).on(q)],
        ),
        eject_parameterized=True,
    )


@pytest.mark.parametrize('sym', [sympy.Symbol('x'), sympy.Symbol('x') + 1])
def test_blocked_by_unknown_and_symbols(sym):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    assert_optimizes(
        before=quick_circuit([alphaclops.X(a)], [alphaclops.SWAP(a, b)], [alphaclops.X(a)]),
        expected=quick_circuit([alphaclops.X(a)], [alphaclops.SWAP(a, b)], [alphaclops.X(a)]),
    )

    assert_optimizes(
        before=quick_circuit([alphaclops.X(a)], [alphaclops.Z(a) ** sym], [alphaclops.X(a)]),
        expected=quick_circuit([alphaclops.X(a)], [alphaclops.Z(a) ** sym], [alphaclops.X(a)]),
        compare_unitaries=False,
    )

    assert_optimizes(
        before=quick_circuit([alphaclops.X(a)], [alphaclops.CZ(a, b) ** sym], [alphaclops.X(a)]),
        expected=quick_circuit([alphaclops.X(a)], [alphaclops.CZ(a, b) ** sym], [alphaclops.X(a)]),
        compare_unitaries=False,
    )


def test_blocked_by_nocompile_tag():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    assert_optimizes(
        before=quick_circuit([alphaclops.X(a)], [alphaclops.CZ(a, b).with_tags("nocompile")], [alphaclops.X(a)]),
        expected=quick_circuit([alphaclops.X(a)], [alphaclops.CZ(a, b).with_tags("nocompile")], [alphaclops.X(a)]),
        with_context=True,
    )


def test_zero_x_rotation():
    a = alphaclops.NamedQubit('a')

    assert_optimizes(before=quick_circuit([alphaclops.rx(0)(a)]), expected=quick_circuit([alphaclops.rx(0)(a)]))
