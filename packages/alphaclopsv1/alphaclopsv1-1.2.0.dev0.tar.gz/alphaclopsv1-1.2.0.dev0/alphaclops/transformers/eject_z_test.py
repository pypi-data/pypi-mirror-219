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

import dataclasses

import pytest
import numpy as np
import sympy

import alphaclops
from alphaclops.transformers.eject_z import _is_swaplike


def assert_optimizes(
    before: alphaclops.Circuit,
    expected: alphaclops.Circuit,
    eject_parameterized: bool = False,
    *,
    with_context: bool = False,
):
    if alphaclops.has_unitary(before):
        alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            before, expected, atol=1e-8
        )
    context = alphaclops.TransformerContext(tags_to_ignore=("nocompile",)) if with_context else None
    circuit = alphaclops.eject_z(before, eject_parameterized=eject_parameterized, context=context)
    expected = alphaclops.eject_z(expected, eject_parameterized=eject_parameterized, context=context)
    alphaclops.testing.assert_same_circuits(circuit, expected)

    # And it should be idempotent.
    circuit = alphaclops.eject_z(before, eject_parameterized=eject_parameterized, context=context)
    alphaclops.testing.assert_same_circuits(circuit, expected)

    # Nested sub-circuits should also get optimized.
    q = before.all_qubits()
    c_nested = alphaclops.Circuit(
        [(alphaclops.Z ** 0.5).on_each(*q), (alphaclops.Y ** 0.25).on_each(*q)],
        alphaclops.Moment(alphaclops.CircuitOperation(before.freeze()).repeat(2).with_tags("ignore")),
        [(alphaclops.Z ** 0.5).on_each(*q), (alphaclops.Y ** 0.25).on_each(*q)],
        alphaclops.Moment(alphaclops.CircuitOperation(before.freeze()).repeat(3).with_tags("preserve_tag")),
    )
    c_expected = alphaclops.Circuit(
        alphaclops.PhasedXPowGate(phase_exponent=0, exponent=0.25).on_each(*q),
        (alphaclops.Z ** 0.5).on_each(*q),
        alphaclops.Moment(alphaclops.CircuitOperation(before.freeze()).repeat(2).with_tags("ignore")),
        alphaclops.PhasedXPowGate(phase_exponent=0, exponent=0.25).on_each(*q),
        (alphaclops.Z ** 0.5).on_each(*q),
        alphaclops.Moment(alphaclops.CircuitOperation(expected.freeze()).repeat(3).with_tags("preserve_tag")),
    )
    if context is None:
        context = alphaclops.TransformerContext(tags_to_ignore=("ignore",), deep=True)
    else:
        context = dataclasses.replace(
            context, tags_to_ignore=context.tags_to_ignore + ("ignore",), deep=True
        )
    c_nested = alphaclops.eject_z(c_nested, context=context, eject_parameterized=eject_parameterized)
    alphaclops.testing.assert_same_circuits(c_nested, c_expected)
    c_nested = alphaclops.eject_z(c_nested, context=context, eject_parameterized=eject_parameterized)
    alphaclops.testing.assert_same_circuits(c_nested, c_expected)


def assert_removes_all_z_gates(circuit: alphaclops.Circuit, eject_parameterized: bool = True):
    optimized = alphaclops.eject_z(circuit, eject_parameterized=eject_parameterized)
    for op in optimized.all_operations():
        # assert _try_get_known_z_half_turns(op, eject_parameterized) is None
        if isinstance(op.gate, alphaclops.PhasedXZGate) and (
            eject_parameterized or not alphaclops.is_parameterized(op.gate.z_exponent)
        ):
            assert op.gate.z_exponent == 0

    if alphaclops.is_parameterized(circuit):
        for a in (0, 0.1, 0.5, 1.0, -1.0, 3.0):
            (
                alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(
                    alphaclops.resolve_parameters(circuit, {'a': a}),
                    alphaclops.resolve_parameters(optimized, {'a': a}),
                    atol=1e-8,
                )
            )
    else:
        alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            circuit, optimized, atol=1e-8
        )


def test_single_z_stays():
    q = alphaclops.NamedQubit('q')
    assert_optimizes(
        before=alphaclops.Circuit([alphaclops.Moment([alphaclops.Z(q) ** 0.5])]),
        expected=alphaclops.Circuit([alphaclops.Moment([alphaclops.Z(q) ** 0.5])]),
    )


def test_single_phased_xz_stays():
    gate = alphaclops.PhasedXZGate(axis_phase_exponent=0.2, x_exponent=0.3, z_exponent=0.4)
    q = alphaclops.NamedQubit('q')
    assert_optimizes(before=alphaclops.Circuit(gate(q)), expected=alphaclops.Circuit(gate(q)))


def test_ignores_xz_and_cz():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    assert_optimizes(
        before=alphaclops.Circuit(
            [
                alphaclops.Moment([alphaclops.X(a) ** 0.5]),
                alphaclops.Moment([alphaclops.Y(b) ** 0.5]),
                alphaclops.Moment([alphaclops.CZ(a, b) ** 0.25]),
                alphaclops.Moment([alphaclops.Y(a) ** 0.5]),
                alphaclops.Moment([alphaclops.X(b) ** 0.5]),
            ]
        ),
        expected=alphaclops.Circuit(
            [
                alphaclops.Moment([alphaclops.X(a) ** 0.5]),
                alphaclops.Moment([alphaclops.Y(b) ** 0.5]),
                alphaclops.Moment([alphaclops.CZ(a, b) ** 0.25]),
                alphaclops.Moment([alphaclops.Y(a) ** 0.5]),
                alphaclops.Moment([alphaclops.X(b) ** 0.5]),
            ]
        ),
    )


def test_early_z():
    q = alphaclops.NamedQubit('q')
    assert_optimizes(
        before=alphaclops.Circuit([alphaclops.Moment([alphaclops.Z(q) ** 0.5]), alphaclops.Moment(), alphaclops.Moment()]),
        expected=alphaclops.Circuit([alphaclops.Moment([alphaclops.Z(q) ** 0.5]), alphaclops.Moment(), alphaclops.Moment()]),
    )


def test_multi_z_merges():
    q = alphaclops.NamedQubit('q')
    assert_optimizes(
        before=alphaclops.Circuit([alphaclops.Moment([alphaclops.Z(q) ** 0.5]), alphaclops.Moment([alphaclops.Z(q) ** 0.25])]),
        expected=alphaclops.Circuit([alphaclops.Moment(), alphaclops.Moment([alphaclops.Z(q) ** 0.75])]),
    )


def test_z_pushes_past_xy_and_phases_it():
    q = alphaclops.NamedQubit('q')
    assert_optimizes(
        before=alphaclops.Circuit([alphaclops.Moment([alphaclops.Z(q) ** 0.5]), alphaclops.Moment([alphaclops.Y(q) ** 0.25])]),
        expected=alphaclops.Circuit(
            [alphaclops.Moment(), alphaclops.Moment([alphaclops.X(q) ** 0.25]), alphaclops.Moment([alphaclops.Z(q) ** 0.5])]
        ),
    )


def test_z_pushes_past_cz():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    assert_optimizes(
        before=alphaclops.Circuit(
            [alphaclops.Moment([alphaclops.Z(a) ** 0.5]), alphaclops.Moment([alphaclops.CZ(a, b) ** 0.25])]
        ),
        expected=alphaclops.Circuit(
            [alphaclops.Moment(), alphaclops.Moment([alphaclops.CZ(a, b) ** 0.25]), alphaclops.Moment([alphaclops.Z(a) ** 0.5])]
        ),
    )


def test_measurement_consumes_zs():
    q = alphaclops.NamedQubit('q')
    assert_optimizes(
        before=alphaclops.Circuit(
            [
                alphaclops.Moment([alphaclops.Z(q) ** 0.5]),
                alphaclops.Moment([alphaclops.Z(q) ** 0.25]),
                alphaclops.Moment([alphaclops.measure(q)]),
            ]
        ),
        expected=alphaclops.Circuit([alphaclops.Moment(), alphaclops.Moment(), alphaclops.Moment([alphaclops.measure(q)])]),
    )


def test_unphaseable_causes_earlier_merge_without_size_increase():
    class UnknownGate(alphaclops.testing.SingleQubitGate):
        pass

    u = UnknownGate()

    # pylint: disable=not-callable
    q = alphaclops.NamedQubit('q')
    assert_optimizes(
        before=alphaclops.Circuit(
            [
                alphaclops.Moment([alphaclops.Z(q)]),
                alphaclops.Moment([u(q)]),
                alphaclops.Moment([alphaclops.Z(q) ** 0.5]),
                alphaclops.Moment([alphaclops.X(q)]),
                alphaclops.Moment([alphaclops.Z(q) ** 0.25]),
                alphaclops.Moment([alphaclops.X(q)]),
                alphaclops.Moment([u(q)]),
            ]
        ),
        expected=alphaclops.Circuit(
            [
                alphaclops.Moment([alphaclops.Z(q)]),
                alphaclops.Moment([u(q)]),
                alphaclops.Moment(),
                alphaclops.Moment([alphaclops.PhasedXPowGate(phase_exponent=-0.5)(q)]),
                alphaclops.Moment(),
                alphaclops.Moment([alphaclops.PhasedXPowGate(phase_exponent=-0.75).on(q)]),
                alphaclops.Moment([alphaclops.Z(q) ** 0.75]),
                alphaclops.Moment([u(q)]),
            ]
        ),
    )


@pytest.mark.parametrize('sym', [sympy.Symbol('a'), sympy.Symbol('a') + 1])
def test_symbols_block(sym):
    q = alphaclops.NamedQubit('q')
    assert_optimizes(
        before=alphaclops.Circuit(
            [
                alphaclops.Moment([alphaclops.Z(q)]),
                alphaclops.Moment([alphaclops.Z(q) ** sym]),
                alphaclops.Moment([alphaclops.Z(q) ** 0.25]),
            ]
        ),
        expected=alphaclops.Circuit(
            [alphaclops.Moment(), alphaclops.Moment([alphaclops.Z(q) ** sym]), alphaclops.Moment([alphaclops.Z(q) ** 1.25])]
        ),
    )


@pytest.mark.parametrize('sym', [sympy.Symbol('a'), sympy.Symbol('a') + 1])
def test_symbols_eject(sym):
    q = alphaclops.NamedQubit('q')
    assert_optimizes(
        before=alphaclops.Circuit(
            [
                alphaclops.Moment([alphaclops.Z(q)]),
                alphaclops.Moment([alphaclops.Z(q) ** sym]),
                alphaclops.Moment([alphaclops.Z(q) ** 0.25]),
            ]
        ),
        expected=alphaclops.Circuit(
            [alphaclops.Moment(), alphaclops.Moment(), alphaclops.Moment([alphaclops.Z(q) ** (sym + 1.25)])]
        ),
        eject_parameterized=True,
    )


def test_removes_zs():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    assert_removes_all_z_gates(alphaclops.Circuit(alphaclops.Z(a), alphaclops.measure(a)))

    assert_removes_all_z_gates(alphaclops.Circuit(alphaclops.Z(a), alphaclops.measure(a, b)))

    assert_removes_all_z_gates(alphaclops.Circuit(alphaclops.Z(a), alphaclops.Z(a), alphaclops.measure(a)))

    assert_removes_all_z_gates(alphaclops.Circuit(alphaclops.Z(a), alphaclops.measure(a, key='k')))

    assert_removes_all_z_gates(alphaclops.Circuit(alphaclops.Z(a), alphaclops.X(a), alphaclops.measure(a)))

    assert_removes_all_z_gates(alphaclops.Circuit(alphaclops.Z(a), alphaclops.X(a), alphaclops.X(a), alphaclops.measure(a)))

    assert_removes_all_z_gates(
        alphaclops.Circuit(alphaclops.Z(a), alphaclops.Z(b), alphaclops.CZ(a, b), alphaclops.CZ(a, b), alphaclops.measure(a, b))
    )

    assert_removes_all_z_gates(
        alphaclops.Circuit(
            alphaclops.PhasedXZGate(axis_phase_exponent=0, x_exponent=0, z_exponent=1).on(a),
            alphaclops.measure(a),
        )
    )

    assert_removes_all_z_gates(
        alphaclops.Circuit(
            alphaclops.Z(a) ** sympy.Symbol('a'),
            alphaclops.Z(b) ** (sympy.Symbol('a') + 1),
            alphaclops.CZ(a, b),
            alphaclops.CZ(a, b),
            alphaclops.measure(a, b),
        ),
        eject_parameterized=True,
    )


def test_unknown_operation_blocks():
    q = alphaclops.NamedQubit('q')

    class UnknownOp(alphaclops.Operation):
        @property
        def qubits(self):
            return [q]

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

    u = UnknownOp()

    assert_optimizes(
        before=alphaclops.Circuit([alphaclops.Moment([alphaclops.Z(q)]), alphaclops.Moment([u])]),
        expected=alphaclops.Circuit([alphaclops.Moment([alphaclops.Z(q)]), alphaclops.Moment([u])]),
    )


def test_tagged_nocompile_operation_blocks():
    q = alphaclops.NamedQubit('q')
    u = alphaclops.Z(q).with_tags("nocompile")
    assert_optimizes(
        before=alphaclops.Circuit([alphaclops.Moment([alphaclops.Z(q)]), alphaclops.Moment([u])]),
        expected=alphaclops.Circuit([alphaclops.Moment([alphaclops.Z(q)]), alphaclops.Moment([u])]),
        with_context=True,
    )


def test_swap():
    a, b = alphaclops.LineQubit.range(2)
    original = alphaclops.Circuit([alphaclops.rz(0.123).on(a), alphaclops.SWAP(a, b)])
    optimized = original.copy()

    optimized = alphaclops.eject_z(optimized)
    optimized = alphaclops.drop_empty_moments(optimized)

    assert optimized[0].operations == (alphaclops.SWAP(a, b),)
    # Note: EjectZ drops `global_phase` from Rz turning it into a Z
    assert optimized[1].operations == (alphaclops.Z(b) ** (0.123 / np.pi),)
    alphaclops.testing.assert_allclose_up_to_global_phase(
        alphaclops.unitary(original), alphaclops.unitary(optimized), atol=1e-8
    )


@pytest.mark.parametrize('exponent', (0, 2, 1.1, -2, -1.6))
def test_not_a_swap(exponent):
    a, b = alphaclops.LineQubit.range(2)
    assert not _is_swaplike(alphaclops.SWAP(a, b) ** exponent)


@pytest.mark.parametrize('theta', (np.pi / 2, -np.pi / 2, np.pi / 2 + 5 * np.pi))
def test_swap_fsim(theta):
    a, b = alphaclops.LineQubit.range(2)
    original = alphaclops.Circuit([alphaclops.rz(0.123).on(a), alphaclops.FSimGate(theta=theta, phi=0.123).on(a, b)])
    optimized = original.copy()

    optimized = alphaclops.eject_z(optimized)
    optimized = alphaclops.drop_empty_moments(optimized)

    assert optimized[0].operations == (alphaclops.FSimGate(theta=theta, phi=0.123).on(a, b),)
    # Note: EjectZ drops `global_phase` from Rz turning it into a Z
    assert optimized[1].operations == (alphaclops.Z(b) ** (0.123 / np.pi),)
    alphaclops.testing.assert_allclose_up_to_global_phase(
        alphaclops.unitary(original), alphaclops.unitary(optimized), atol=1e-8
    )


@pytest.mark.parametrize('theta', (0, 5 * np.pi, -np.pi))
def test_not_a_swap_fsim(theta):
    a, b = alphaclops.LineQubit.range(2)
    assert not _is_swaplike(alphaclops.FSimGate(theta=theta, phi=0.456).on(a, b))


@pytest.mark.parametrize('exponent', (1, -1))
def test_swap_iswap(exponent):
    a, b = alphaclops.LineQubit.range(2)
    original = alphaclops.Circuit([alphaclops.rz(0.123).on(a), alphaclops.ISWAP(a, b) ** exponent])
    optimized = original.copy()

    optimized = alphaclops.eject_z(optimized)
    optimized = alphaclops.drop_empty_moments(optimized)

    assert optimized[0].operations == (alphaclops.ISWAP(a, b) ** exponent,)
    # Note: EjectZ drops `global_phase` from Rz turning it into a Z
    assert optimized[1].operations == (alphaclops.Z(b) ** (0.123 / np.pi),)
    alphaclops.testing.assert_allclose_up_to_global_phase(
        alphaclops.unitary(original), alphaclops.unitary(optimized), atol=1e-8
    )
