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

from typing import Optional

import alphaclops
import pytest
import sympy
import numpy as np


def all_gates_of_type(m: alphaclops.Moment, g: alphaclops.Gateset):
    for op in m:
        if op not in g:
            return False
    return True


def assert_optimizes(before: alphaclops.Circuit, expected: alphaclops.Circuit, **kwargs):
    alphaclops.testing.assert_same_circuits(
        alphaclops.optimize_for_target_gateset(
            before, gateset=alphaclops.SqrtIswapTargetGateset(**kwargs), ignore_failures=False
        ),
        expected,
    )


def assert_optimization_not_broken(
    circuit: alphaclops.Circuit, required_sqrt_iswap_count: Optional[int] = None
):
    c_new = alphaclops.optimize_for_target_gateset(
        circuit,
        gateset=alphaclops.SqrtIswapTargetGateset(required_sqrt_iswap_count=required_sqrt_iswap_count),
        ignore_failures=False,
    )
    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        circuit, c_new, atol=1e-6
    )
    c_new = alphaclops.optimize_for_target_gateset(
        circuit,
        gateset=alphaclops.SqrtIswapTargetGateset(
            use_sqrt_iswap_inv=True, required_sqrt_iswap_count=required_sqrt_iswap_count
        ),
        ignore_failures=False,
    )
    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        circuit, c_new, atol=1e-6
    )


def test_convert_to_sqrt_iswap_preserving_moment_structure():
    q = alphaclops.LineQubit.range(5)
    op = lambda q0, q1: alphaclops.H(q1).controlled_by(q0)
    c_orig = alphaclops.Circuit(
        alphaclops.Moment(alphaclops.X(q[2])),
        alphaclops.Moment(op(q[0], q[1]), op(q[2], q[3])),
        alphaclops.Moment(op(q[2], q[1]), op(q[4], q[3])),
        alphaclops.Moment(op(q[1], q[2]), op(q[3], q[4])),
        alphaclops.Moment(op(q[3], q[2]), op(q[1], q[0])),
        alphaclops.measure(*q[:2], key="m"),
        alphaclops.X(q[2]).with_classical_controls("m"),
        alphaclops.CZ(*q[3:]).with_classical_controls("m"),
    )
    # Classically controlled operations are not part of the gateset, so failures should be ignored
    # during compilation.
    c_new = alphaclops.optimize_for_target_gateset(
        c_orig, gateset=alphaclops.SqrtIswapTargetGateset(), ignore_failures=True
    )

    assert c_orig[-2:] == c_new[-2:]
    c_orig, c_new = c_orig[:-2], c_new[:-2]

    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_orig, c_new, atol=1e-6)
    assert all(
        (
            all_gates_of_type(m, alphaclops.Gateset(alphaclops.PhasedXZGate))
            or all_gates_of_type(m, alphaclops.Gateset(alphaclops.SQRT_ISWAP))
        )
        for m in c_new
    )

    c_new = alphaclops.optimize_for_target_gateset(
        c_orig, gateset=alphaclops.SqrtIswapTargetGateset(use_sqrt_iswap_inv=True), ignore_failures=False
    )
    alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(c_orig, c_new, atol=1e-6)
    assert all(
        (
            all_gates_of_type(m, alphaclops.Gateset(alphaclops.PhasedXZGate))
            or all_gates_of_type(m, alphaclops.Gateset(alphaclops.SQRT_ISWAP_INV))
        )
        for m in c_new
    )


@pytest.mark.parametrize(
    'gate',
    [
        alphaclops.CNotPowGate(exponent=sympy.Symbol('t')),
        alphaclops.PhasedFSimGate(theta=sympy.Symbol('t'), chi=sympy.Symbol('t'), phi=sympy.Symbol('t')),
    ],
)
@pytest.mark.parametrize('use_sqrt_iswap_inv', [True, False])
def test_two_qubit_gates_with_symbols(gate: alphaclops.Gate, use_sqrt_iswap_inv: bool):
    # Note that even though these gates are not natively supported by
    # `alphaclops.parameterized_2q_op_to_sqrt_iswap_operations`, the transformation succeeds because
    # `alphaclops.optimize_for_target_gateset` also relies on `alphaclops.decompose` as a fallback.

    c_orig = alphaclops.Circuit(gate(*alphaclops.LineQubit.range(2)))
    c_new = alphaclops.optimize_for_target_gateset(
        c_orig,
        gateset=alphaclops.SqrtIswapTargetGateset(
            use_sqrt_iswap_inv=use_sqrt_iswap_inv,
            additional_gates=[alphaclops.XPowGate, alphaclops.YPowGate, alphaclops.ZPowGate],
        ),
        ignore_failures=False,
    )

    # Check that `c_new` only contains sqrt iswap as the 2q entangling gate.
    sqrt_iswap_gate = alphaclops.SQRT_ISWAP_INV if use_sqrt_iswap_inv else alphaclops.SQRT_ISWAP
    for op in c_new.all_operations():
        if alphaclops.num_qubits(op) == 2:
            assert op.gate == sqrt_iswap_gate

    # Check if unitaries are the same
    for val in np.linspace(0, 2 * np.pi, 10):
        alphaclops.testing.assert_circuits_with_terminal_measurements_are_equivalent(
            alphaclops.resolve_parameters(c_orig, {'t': val}),
            alphaclops.resolve_parameters(c_new, {'t': val}),
            atol=1e-6,
        )


def test_sqrt_iswap_gateset_raises():
    with pytest.raises(ValueError, match="`required_sqrt_iswap_count` must be 0, 1, 2, or 3"):
        _ = alphaclops.SqrtIswapTargetGateset(required_sqrt_iswap_count=4)


def test_sqrt_iswap_gateset_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(
        alphaclops.SqrtIswapTargetGateset(), alphaclops.SqrtIswapTargetGateset(use_sqrt_iswap_inv=False)
    )
    eq.add_equality_group(
        alphaclops.SqrtIswapTargetGateset(atol=1e-6, required_sqrt_iswap_count=0, use_sqrt_iswap_inv=True)
    )
    eq.add_equality_group(
        alphaclops.SqrtIswapTargetGateset(atol=1e-6, required_sqrt_iswap_count=3, use_sqrt_iswap_inv=True)
    )
    eq.add_equality_group(alphaclops.SqrtIswapTargetGateset(additional_gates=[alphaclops.XPowGate]))


@pytest.mark.parametrize(
    'gateset',
    [
        alphaclops.SqrtIswapTargetGateset(),
        alphaclops.SqrtIswapTargetGateset(
            atol=1e-6,
            required_sqrt_iswap_count=2,
            use_sqrt_iswap_inv=True,
            additional_gates=[
                alphaclops.CZ,
                alphaclops.XPowGate,
                alphaclops.YPowGate,
                alphaclops.GateFamily(alphaclops.ZPowGate, tags_to_accept=['test_tag']),
            ],
        ),
        alphaclops.SqrtIswapTargetGateset(additional_gates=()),
    ],
)
def test_sqrt_iswap_gateset_repr(gateset):
    alphaclops.testing.assert_equivalent_repr(gateset)


def test_simplifies_sqrt_iswap():
    a, b = alphaclops.LineQubit.range(2)
    assert_optimizes(
        before=alphaclops.Circuit(
            [
                # SQRT_ISWAP**8 == Identity
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
            ]
        ),
        expected=alphaclops.Circuit([alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)])]),
    )


def test_simplifies_sqrt_iswap_inv():
    a, b = alphaclops.LineQubit.range(2)
    assert_optimizes(
        use_sqrt_iswap_inv=True,
        before=alphaclops.Circuit(
            [
                # SQRT_ISWAP**8 == Identity
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP_INV(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)]),
            ]
        ),
        expected=alphaclops.Circuit([alphaclops.Moment([alphaclops.SQRT_ISWAP_INV(a, b)])]),
    )


def test_works_with_tags():
    a, b = alphaclops.LineQubit.range(2)
    assert_optimizes(
        before=alphaclops.Circuit(
            [
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b).with_tags('mytag1')]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b).with_tags('mytag2')]),
                alphaclops.Moment([alphaclops.SQRT_ISWAP_INV(a, b).with_tags('mytag3')]),
            ]
        ),
        expected=alphaclops.Circuit([alphaclops.Moment([alphaclops.SQRT_ISWAP(a, b)])]),
    )


def test_no_touch_single_sqrt_iswap():
    a, b = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        [
            alphaclops.Moment(
                [alphaclops.ISwapPowGate(exponent=0.5, global_shift=-0.5).on(a, b).with_tags('mytag')]
            )
        ]
    )
    assert_optimizes(before=circuit, expected=circuit)


def test_no_touch_single_sqrt_iswap_inv():
    a, b = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        [
            alphaclops.Moment(
                [alphaclops.ISwapPowGate(exponent=-0.5, global_shift=-0.5).on(a, b).with_tags('mytag')]
            )
        ]
    )
    assert_optimizes(before=circuit, expected=circuit, use_sqrt_iswap_inv=True)


def test_cnots_separated_by_single_gates_correct():
    a, b = alphaclops.LineQubit.range(2)
    assert_optimization_not_broken(alphaclops.Circuit(alphaclops.CNOT(a, b), alphaclops.H(b), alphaclops.CNOT(a, b)))


def test_czs_separated_by_single_gates_correct():
    a, b = alphaclops.LineQubit.range(2)
    assert_optimization_not_broken(
        alphaclops.Circuit(alphaclops.CZ(a, b), alphaclops.X(b), alphaclops.X(b), alphaclops.X(b), alphaclops.CZ(a, b))
    )


def test_inefficient_circuit_correct():
    t = 0.1
    v = 0.11
    a, b = alphaclops.LineQubit.range(2)
    assert_optimization_not_broken(
        alphaclops.Circuit(
            alphaclops.H(b),
            alphaclops.CNOT(a, b),
            alphaclops.H(b),
            alphaclops.CNOT(a, b),
            alphaclops.CNOT(b, a),
            alphaclops.H(a),
            alphaclops.CNOT(a, b),
            alphaclops.Z(a) ** t,
            alphaclops.Z(b) ** -t,
            alphaclops.CNOT(a, b),
            alphaclops.H(a),
            alphaclops.Z(b) ** v,
            alphaclops.CNOT(a, b),
            alphaclops.Z(a) ** -v,
            alphaclops.Z(b) ** -v,
        )
    )


def test_optimizes_single_iswap():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.ISWAP(a, b))
    assert_optimization_not_broken(c)
    c = alphaclops.optimize_for_target_gateset(
        c, gateset=alphaclops.SqrtIswapTargetGateset(), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 2


def test_optimizes_single_inv_sqrt_iswap():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.SQRT_ISWAP_INV(a, b))
    assert_optimization_not_broken(c)
    c = alphaclops.optimize_for_target_gateset(
        c, gateset=alphaclops.SqrtIswapTargetGateset(), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 1


def test_optimizes_single_iswap_require0():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.CNOT(a, b), alphaclops.CNOT(a, b))  # Minimum 0 sqrt-iSWAP
    assert_optimization_not_broken(c, required_sqrt_iswap_count=0)
    c = alphaclops.optimize_for_target_gateset(
        c, gateset=alphaclops.SqrtIswapTargetGateset(required_sqrt_iswap_count=0), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 0


def test_optimizes_single_iswap_require0_raises():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.CNOT(a, b))  # Minimum 2 sqrt-iSWAP
    with pytest.raises(ValueError, match='cannot be decomposed into exactly 0 sqrt-iSWAP gates'):
        _ = alphaclops.optimize_for_target_gateset(
            c,
            gateset=alphaclops.SqrtIswapTargetGateset(required_sqrt_iswap_count=0),
            ignore_failures=False,
        )


def test_optimizes_single_iswap_require1():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.SQRT_ISWAP_INV(a, b))  # Minimum 1 sqrt-iSWAP
    assert_optimization_not_broken(c, required_sqrt_iswap_count=1)
    c = alphaclops.optimize_for_target_gateset(
        c, gateset=alphaclops.SqrtIswapTargetGateset(required_sqrt_iswap_count=1), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 1


def test_optimizes_single_iswap_require1_raises():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.CNOT(a, b))  # Minimum 2 sqrt-iSWAP
    with pytest.raises(ValueError, match='cannot be decomposed into exactly 1 sqrt-iSWAP gates'):
        c = alphaclops.optimize_for_target_gateset(
            c,
            gateset=alphaclops.SqrtIswapTargetGateset(required_sqrt_iswap_count=1),
            ignore_failures=False,
        )


def test_optimizes_single_iswap_require2():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.SQRT_ISWAP_INV(a, b))  # Minimum 1 sqrt-iSWAP but 2 possible
    assert_optimization_not_broken(c, required_sqrt_iswap_count=2)
    c = alphaclops.optimize_for_target_gateset(
        c, gateset=alphaclops.SqrtIswapTargetGateset(required_sqrt_iswap_count=2), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 2


def test_optimizes_single_iswap_require2_raises():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.SWAP(a, b))  # Minimum 3 sqrt-iSWAP
    with pytest.raises(ValueError, match='cannot be decomposed into exactly 2 sqrt-iSWAP gates'):
        c = alphaclops.optimize_for_target_gateset(
            c,
            gateset=alphaclops.SqrtIswapTargetGateset(required_sqrt_iswap_count=2),
            ignore_failures=False,
        )


def test_optimizes_single_iswap_require3():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.ISWAP(a, b))  # Minimum 2 sqrt-iSWAP but 3 possible
    assert_optimization_not_broken(c, required_sqrt_iswap_count=3)
    c = alphaclops.optimize_for_target_gateset(
        c, gateset=alphaclops.SqrtIswapTargetGateset(required_sqrt_iswap_count=3), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 3


def test_optimizes_single_inv_sqrt_iswap_require3():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.SQRT_ISWAP_INV(a, b))
    assert_optimization_not_broken(c, required_sqrt_iswap_count=3)
    c = alphaclops.optimize_for_target_gateset(
        c, gateset=alphaclops.SqrtIswapTargetGateset(required_sqrt_iswap_count=3), ignore_failures=False
    )
    assert len([1 for op in c.all_operations() if len(op.qubits) == 2]) == 3
