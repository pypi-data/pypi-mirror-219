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
import pytest
import alphaclops
from alphaclops.protocols.decompose_protocol import DecomposeResult


def test_compilation_target_gateset():
    class DummyTargetGateset(alphaclops.CompilationTargetGateset):
        def __init__(self):
            super().__init__(alphaclops.AnyUnitaryGateFamily(2))

        @property
        def num_qubits(self) -> int:
            return 2

        def decompose_to_target_gateset(self, op: 'alphaclops.Operation', _) -> DecomposeResult:
            return op if alphaclops.num_qubits(op) == 2 and alphaclops.has_unitary(op) else NotImplemented

        @property
        def preprocess_transformers(self) -> List[alphaclops.TRANSFORMER]:
            return []

    gateset = DummyTargetGateset()

    q = alphaclops.LineQubit.range(2)
    assert alphaclops.X(q[0]) not in gateset
    assert alphaclops.CNOT(*q) in gateset
    assert alphaclops.measure(*q) not in gateset
    circuit_op = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.CZ(*q), alphaclops.CNOT(*q), alphaclops.CZ(*q)))
    assert circuit_op in gateset
    assert circuit_op.with_tags(gateset._intermediate_result_tag) not in gateset

    assert gateset.num_qubits == 2
    assert gateset.decompose_to_target_gateset(alphaclops.X(q[0]), 1) is NotImplemented
    assert gateset.decompose_to_target_gateset(alphaclops.CNOT(*q), 2) == alphaclops.CNOT(*q)
    assert gateset.decompose_to_target_gateset(alphaclops.measure(*q), 3) is NotImplemented

    assert gateset.preprocess_transformers == []
    assert gateset.postprocess_transformers == [
        alphaclops.merge_single_qubit_moments_to_phxz,
        alphaclops.drop_negligible_operations,
        alphaclops.drop_empty_moments,
    ]


class DummyCXTargetGateset(alphaclops.TwoQubitCompilationTargetGateset):
    def __init__(self):
        super().__init__(alphaclops.AnyUnitaryGateFamily(1), alphaclops.CNOT)

    def _decompose_two_qubit_operation(self, op: 'alphaclops.Operation', _) -> DecomposeResult:
        if not alphaclops.has_unitary(op):
            return NotImplemented

        assert self._intermediate_result_tag in op.tags
        q0, q1 = op.qubits
        return [
            alphaclops.X.on_each(q0, q1),
            alphaclops.CNOT(q0, q1),
            alphaclops.Y.on_each(q0, q1),
            alphaclops.CNOT(q0, q1),
            alphaclops.Z.on_each(q0, q1),
        ]

    def _decompose_single_qubit_operation(self, op: 'alphaclops.Operation', _) -> DecomposeResult:
        if not alphaclops.has_unitary(op):
            return NotImplemented
        assert self._intermediate_result_tag in op.tags
        op_untagged = op.untagged
        assert isinstance(op_untagged, alphaclops.CircuitOperation)
        return (
            alphaclops.decompose(op_untagged.circuit)
            if len(op_untagged.circuit) == 1
            else super()._decompose_single_qubit_operation(op, _)
        )


def test_two_qubit_compilation_leaves_single_gates_in_gateset():
    q = alphaclops.LineQubit.range(2)
    gateset = DummyCXTargetGateset()

    c = alphaclops.Circuit(alphaclops.X(q[0]) ** 0.5)
    alphaclops.testing.assert_same_circuits(alphaclops.optimize_for_target_gateset(c, gateset=gateset), c)

    c = alphaclops.Circuit(alphaclops.CNOT(*q[:2]))
    alphaclops.testing.assert_same_circuits(alphaclops.optimize_for_target_gateset(c, gateset=gateset), c)


def test_two_qubit_compilation_merges_runs_of_single_qubit_gates():
    q = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.CNOT(*q), alphaclops.X(q[0]), alphaclops.Y(q[0]), alphaclops.CNOT(*q))
    alphaclops.testing.assert_same_circuits(
        alphaclops.optimize_for_target_gateset(c, gateset=DummyCXTargetGateset()),
        alphaclops.Circuit(
            alphaclops.CNOT(*q),
            alphaclops.PhasedXZGate(axis_phase_exponent=-0.5, x_exponent=0, z_exponent=-1).on(q[0]),
            alphaclops.CNOT(*q),
        ),
    )


def test_two_qubit_compilation_decompose_operation_not_implemented():
    gateset = DummyCXTargetGateset()
    q = alphaclops.LineQubit.range(3)
    assert gateset.decompose_to_target_gateset(alphaclops.measure(q[0]), 1) is NotImplemented
    assert gateset.decompose_to_target_gateset(alphaclops.measure(*q[:2]), 1) is NotImplemented
    assert (
        gateset.decompose_to_target_gateset(alphaclops.X(q[0]).with_classical_controls("m"), 1)
        is NotImplemented
    )
    assert gateset.decompose_to_target_gateset(alphaclops.CCZ(*q), 1) is NotImplemented


def test_two_qubit_compilation_merge_and_replace_to_target_gateset():
    q = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(
        alphaclops.Moment(alphaclops.Z(q[1]), alphaclops.X(q[0])),
        alphaclops.Moment(alphaclops.CZ(*q).with_tags("no_compile")),
        alphaclops.Moment(alphaclops.Z.on_each(*q)),
        alphaclops.Moment(alphaclops.X(q[0])),
        alphaclops.Moment(alphaclops.CZ(*q)),
        alphaclops.Moment(alphaclops.Z.on_each(*q)),
        alphaclops.Moment(alphaclops.X(q[0])),
    )
    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───X───@['no_compile']───Z───X───@───Z───X───
          │                         │
1: ───Z───@─────────────────Z───────@───Z───────
''',
    )
    c_new = alphaclops.optimize_for_target_gateset(
        c_orig,
        gateset=DummyCXTargetGateset(),
        context=alphaclops.TransformerContext(tags_to_ignore=("no_compile",)),
    )
    alphaclops.testing.assert_has_diagram(
        c_new,
        '''
0: ───X───@['no_compile']───X───@───Y───@───Z───
          │                     │       │
1: ───Z───@─────────────────X───X───Y───X───Z───
''',
    )


def test_two_qubit_compilation_merge_and_replace_inefficient_component():
    q = alphaclops.LineQubit.range(2)
    c_orig = alphaclops.Circuit(
        alphaclops.Moment(alphaclops.X(q[0])),
        alphaclops.Moment(alphaclops.CNOT(*q)),
        alphaclops.Moment(alphaclops.X(q[0])),
        alphaclops.Moment(alphaclops.CZ(*q).with_tags("no_compile")),
        alphaclops.Moment(alphaclops.Z.on_each(*q)),
        alphaclops.Moment(alphaclops.X(q[0])),
        alphaclops.Moment(alphaclops.CNOT(*q)),
        alphaclops.Moment(alphaclops.CNOT(*q)),
        alphaclops.Moment(alphaclops.Z.on_each(*q)),
        alphaclops.Moment(alphaclops.X(q[0])),
        alphaclops.Moment(alphaclops.CNOT(*q)),
        alphaclops.measure(q[0], key="m"),
        alphaclops.X(q[1]).with_classical_controls("m"),
    )
    alphaclops.testing.assert_has_diagram(
        c_orig,
        '''
0: ───X───@───X───@['no_compile']───Z───X───@───@───Z───X───@───M───────
          │       │                         │   │           │   ║
1: ───────X───────@─────────────────Z───────X───X───Z───────X───╫───X───
                                                                ║   ║
m: ═════════════════════════════════════════════════════════════@═══^═══
''',
    )
    c_new = alphaclops.optimize_for_target_gateset(
        c_orig,
        gateset=DummyCXTargetGateset(),
        context=alphaclops.TransformerContext(tags_to_ignore=("no_compile",)),
    )
    alphaclops.testing.assert_has_diagram(
        c_new,
        '''
0: ───X───@───X───@['no_compile']───X───@───Y───@───Z───M───────
          │       │                     │       │       ║
1: ───────X───────@─────────────────X───X───Y───X───Z───╫───X───
                                                        ║   ║
m: ═════════════════════════════════════════════════════@═══^═══
''',
    )


def test_two_qubit_compilation_replaces_only_if_2q_gate_count_is_less():
    class DummyTargetGateset(alphaclops.TwoQubitCompilationTargetGateset):
        def __init__(self):
            super().__init__(alphaclops.X, alphaclops.CNOT)

        def _decompose_two_qubit_operation(self, op: 'alphaclops.Operation', _) -> DecomposeResult:
            q0, q1 = op.qubits
            return [alphaclops.X.on_each(q0, q1), alphaclops.CNOT(q0, q1)] * 10

        def _decompose_single_qubit_operation(self, op: 'alphaclops.Operation', _) -> DecomposeResult:
            return alphaclops.X(*op.qubits) if op.gate == alphaclops.Y else NotImplemented

    q = alphaclops.LineQubit.range(2)
    ops = [alphaclops.Y.on_each(*q), alphaclops.CNOT(*q), alphaclops.Z.on_each(*q)]
    c_orig = alphaclops.Circuit(ops)
    c_expected = alphaclops.Circuit(alphaclops.X.on_each(*q), ops[-2:])
    c_new = alphaclops.optimize_for_target_gateset(c_orig, gateset=DummyTargetGateset())
    alphaclops.testing.assert_same_circuits(c_new, c_expected)


def test_create_transformer_with_kwargs_raises():
    with pytest.raises(SyntaxError, match="must not contain `context`"):
        alphaclops.create_transformer_with_kwargs(
            alphaclops.merge_k_qubit_unitaries, k=2, context=alphaclops.TransformerContext()
        )
