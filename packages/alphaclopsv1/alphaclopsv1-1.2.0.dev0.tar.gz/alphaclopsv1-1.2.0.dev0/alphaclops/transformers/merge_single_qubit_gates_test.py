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

from typing import List

import alphaclops


def assert_optimizes(optimized: alphaclops.RandomGrid, expected: alphaclops.RandomGrid):
    # Ignore differences that would be caught by follow-up optimizations.
    followup_transformers: List[alphaclops.TRANSFORMER] = [
        alphaclops.drop_negligible_operations,
        alphaclops.drop_empty_moments,
    ]
    for transform in followup_transformers:
        optimized = transform(optimized)
        expected = transform(expected)

    alphaclops.testing.assert_same_circuits(optimized, expected)


def test_merge_single_qubit_gates_to_phased_x_and_z():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(
        alphaclops.X(a),
        alphaclops.Y(b) ** 0.5,
        alphaclops.CZ(a, b),
        alphaclops.H(a),
        alphaclops.Z(a),
        alphaclops.measure(b, key="m"),
        alphaclops.H(a).with_classical_controls("m"),
    )
    assert_optimizes(
        optimized=alphaclops.merge_single_qubit_gates_to_phased_x_and_z(c),
        expected=alphaclops.Circuit(
            alphaclops.PhasedXPowGate(phase_exponent=1)(a),
            alphaclops.Y(b) ** 0.5,
            alphaclops.CZ(a, b),
            (alphaclops.PhasedXPowGate(phase_exponent=-0.5)(a)) ** 0.5,
            alphaclops.measure(b, key="m"),
            alphaclops.H(a).with_classical_controls("m"),
        ),
    )


def test_merge_single_qubit_gates_to_phased_x_and_z_deep():
    a = alphaclops.NamedQubit("a")
    c_nested = alphaclops.FrozenCircuit(alphaclops.H(a), alphaclops.Z(a), alphaclops.H(a).with_tags("ignore"))
    c_nested_merged = alphaclops.FrozenCircuit(
        alphaclops.PhasedXPowGate(phase_exponent=-0.5, exponent=0.5).on(a), alphaclops.H(a).with_tags("ignore")
    )
    c_orig = alphaclops.Circuit(
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(5).with_tags("preserve_tags"),
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(6),
    )
    c_expected = alphaclops.Circuit(
        c_nested_merged,
        alphaclops.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested_merged,
        alphaclops.CircuitOperation(c_nested_merged).repeat(5).with_tags("preserve_tags"),
        c_nested_merged,
        alphaclops.CircuitOperation(c_nested_merged).repeat(6),
    )
    context = alphaclops.TransformerContext(tags_to_ignore=["ignore"], deep=True)
    c_new = alphaclops.merge_single_qubit_gates_to_phased_x_and_z(c_orig, context=context)
    alphaclops.testing.assert_same_circuits(c_new, c_expected)


def _phxz(a: float, x: float, z: float):
    return alphaclops.PhasedXZGate(axis_phase_exponent=a, x_exponent=x, z_exponent=z)


def test_merge_single_qubit_gates_to_phxz():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(
        alphaclops.X(a),
        alphaclops.Y(b) ** 0.5,
        alphaclops.CZ(a, b),
        alphaclops.H(a),
        alphaclops.Z(a),
        alphaclops.measure(b, key="m"),
        alphaclops.H(a).with_classical_controls("m"),
    )
    assert_optimizes(
        optimized=alphaclops.merge_single_qubit_gates_to_phxz(c),
        expected=alphaclops.Circuit(
            _phxz(-1, 1, 0).on(a),
            _phxz(0.5, 0.5, 0).on(b),
            alphaclops.CZ(a, b),
            _phxz(-0.5, 0.5, 0).on(a),
            alphaclops.measure(b, key="m"),
            alphaclops.H(a).with_classical_controls("m"),
        ),
    )


def test_merge_single_qubit_gates_to_phxz_deep():
    a = alphaclops.NamedQubit("a")
    c_nested = alphaclops.FrozenCircuit(alphaclops.H(a), alphaclops.Z(a), alphaclops.H(a).with_tags("ignore"))
    c_nested_merged = alphaclops.FrozenCircuit(_phxz(-0.5, 0.5, 0).on(a), alphaclops.H(a).with_tags("ignore"))
    c_orig = alphaclops.Circuit(
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(5).with_tags("preserve_tags"),
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(6),
    )
    c_expected = alphaclops.Circuit(
        c_nested_merged,
        alphaclops.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested_merged,
        alphaclops.CircuitOperation(c_nested_merged).repeat(5).with_tags("preserve_tags"),
        c_nested_merged,
        alphaclops.CircuitOperation(c_nested_merged).repeat(6),
    )
    context = alphaclops.TransformerContext(tags_to_ignore=["ignore"], deep=True)
    c_new = alphaclops.merge_single_qubit_gates_to_phxz(c_orig, context=context)
    alphaclops.testing.assert_same_circuits(c_new, c_expected)


def test_merge_single_qubit_moments_to_phxz():
    q = alphaclops.LineQubit.range(3)
    c_orig = alphaclops.Circuit(
        alphaclops.Moment(alphaclops.X.on_each(*q[:2])),
        alphaclops.Moment(alphaclops.T.on_each(*q[1:])),
        alphaclops.Moment(alphaclops.Y.on_each(*q[:2])),
        alphaclops.Moment(alphaclops.CZ(*q[:2]), alphaclops.Y(q[2])),
        alphaclops.Moment(alphaclops.X.on_each(*q[:2])),
        alphaclops.Moment(alphaclops.T.on_each(*q[1:])),
        alphaclops.Moment(alphaclops.Y.on_each(*q[:2])),
        alphaclops.Moment(alphaclops.Y(q[0]).with_tags("nocompile"), alphaclops.Z.on_each(*q[1:])),
        alphaclops.Moment(alphaclops.X.on_each(q[0])),
        alphaclops.Moment(alphaclops.measure(q[0], key="a")),
        alphaclops.Moment(alphaclops.X(q[1]).with_classical_controls("a")),
        alphaclops.Moment(alphaclops.X.on_each(q[1])),
    )
    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───X───────Y───@───X───────Y───Y['nocompile']───X───M───────────
                  │                                    ║
1: ───X───T───Y───@───X───T───Y───Z────────────────────╫───X───X───
                                                       ║   ║
2: ───────T───────Y───────T───────Z────────────────────╫───╫───────
                                                       ║   ║
a: ════════════════════════════════════════════════════@═══^═══════
''',
    )
    context = alphaclops.TransformerContext(tags_to_ignore=("nocompile",))
    c_new = alphaclops.merge_single_qubit_moments_to_phxz(c_orig, context=context)
    alphaclops.testing.assert_has_diagram(
        c_new,
        '''
0: ───PhXZ(a=-0.5,x=0,z=-1)──────@───PhXZ(a=-0.5,x=0,z=-1)──────Y['nocompile']───X───M───────────
                                 │                                                   ║
1: ───PhXZ(a=-0.25,x=0,z=0.75)───@───PhXZ(a=-0.25,x=0,z=0.75)───Z────────────────────╫───X───X───
                                                                                     ║   ║
2: ───PhXZ(a=0.25,x=0,z=0.25)────Y───PhXZ(a=0.25,x=0,z=0.25)────Z────────────────────╫───╫───────
                                                                                     ║   ║
a: ══════════════════════════════════════════════════════════════════════════════════@═══^═══════
''',
    )


def test_merge_single_qubit_moments_to_phxz_deep():
    q = alphaclops.LineQubit.range(3)
    x_t_y = alphaclops.FrozenCircuit(
        alphaclops.Moment(alphaclops.X.on_each(*q[:2])),
        alphaclops.Moment(alphaclops.T.on_each(*q[1:])),
        alphaclops.Moment(alphaclops.Y.on_each(*q[:2])),
    )
    c_nested = alphaclops.FrozenCircuit(
        x_t_y,
        alphaclops.Moment(alphaclops.CZ(*q[:2]), alphaclops.Y(q[2])),
        x_t_y,
        alphaclops.Moment(alphaclops.Y(q[0]).with_tags("ignore"), alphaclops.Z.on_each(*q[1:])),
    )

    c_nested_merged = alphaclops.FrozenCircuit(
        [_phxz(-0.25, 0.0, 0.75)(q[1]), _phxz(0.25, 0.0, 0.25)(q[2]), _phxz(-0.5, 0.0, -1.0)(q[0])],
        [alphaclops.CZ(q[0], q[1]), alphaclops.Y(q[2])],
        [_phxz(-0.25, 0.0, 0.75)(q[1]), _phxz(0.25, 0.0, 0.25)(q[2]), _phxz(-0.5, 0.0, -1.0)(q[0])],
        alphaclops.Moment(alphaclops.Y(q[0]).with_tags("ignore"), alphaclops.Z.on_each(*q[1:])),
    )
    c_orig = alphaclops.Circuit(
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(5).with_tags("preserve_tags"),
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(6),
    )
    c_expected = alphaclops.Circuit(
        c_nested_merged,
        alphaclops.CircuitOperation(c_nested).repeat(4).with_tags("ignore"),
        c_nested_merged,
        alphaclops.CircuitOperation(c_nested_merged).repeat(5).with_tags("preserve_tags"),
        c_nested_merged,
        alphaclops.CircuitOperation(c_nested_merged).repeat(6),
    )
    context = alphaclops.TransformerContext(tags_to_ignore=["ignore"], deep=True)
    c_new = alphaclops.merge_single_qubit_moments_to_phxz(c_orig, context=context)
    alphaclops.testing.assert_allclose_up_to_global_phase(
        c_new.unitary(), c_expected.unitary(), atol=1e-7
    )


def test_merge_single_qubit_moments_to_phxz_global_phase():
    c = alphaclops.Circuit(alphaclops.GlobalPhaseGate(1j).on())
    c2 = alphaclops.merge_single_qubit_gates_to_phxz(c)
    assert c == c2


def test_merge_single_qubit_moments_to_phased_x_and_z_global_phase():
    c = alphaclops.Circuit(alphaclops.GlobalPhaseGate(1j).on())
    c2 = alphaclops.merge_single_qubit_gates_to_phased_x_and_z(c)
    assert c == c2
