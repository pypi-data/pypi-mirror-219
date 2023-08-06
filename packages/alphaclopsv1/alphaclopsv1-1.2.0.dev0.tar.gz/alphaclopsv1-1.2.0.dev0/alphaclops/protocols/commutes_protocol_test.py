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

import numpy as np
import pytest
import sympy

import alphaclops


def test_commutes_on_matrices():
    I, X, Y, Z = (alphaclops.unitary(A) for A in (alphaclops.I, alphaclops.X, alphaclops.Y, alphaclops.Z))
    IX, IY = (np.kron(I, A) for A in (X, Y))
    XI, YI, ZI = (np.kron(A, I) for A in (X, Y, Z))
    XX, YY, ZZ = (np.kron(A, A) for A in (X, Y, Z))
    for A in (X, Y, Z):
        assert alphaclops.commutes(I, A)
        assert alphaclops.commutes(A, A)
        assert alphaclops.commutes(I, XX, default='default') == 'default'
    for A, B in [(X, Y), (X, Z), (Z, Y), (IX, IY), (XI, ZI)]:
        assert not alphaclops.commutes(A, B)
        assert not alphaclops.commutes(A, B, atol=1)
        assert alphaclops.commutes(A, B, atol=2)
    for A, B in [(XX, YY), (XX, ZZ), (ZZ, YY), (IX, YI), (IX, IX), (ZI, IY)]:
        assert alphaclops.commutes(A, B)


def test_commutes_on_gates_and_gate_operations():
    X, Y, Z = tuple(alphaclops.unitary(A) for A in (alphaclops.X, alphaclops.Y, alphaclops.Z))
    XGate, YGate, ZGate = (alphaclops.MatrixGate(A) for A in (X, Y, Z))
    XXGate, YYGate, ZZGate = (alphaclops.MatrixGate(alphaclops.kron(A, A)) for A in (X, Y, Z))
    a, b = alphaclops.LineQubit.range(2)
    for A in (XGate, YGate, ZGate):
        assert alphaclops.commutes(A, A)
        assert A._commutes_on_qids_(a, A, atol=1e-8) is NotImplemented
        with pytest.raises(TypeError):
            alphaclops.commutes(A(a), A)
        with pytest.raises(TypeError):
            alphaclops.commutes(A, A(a))
        assert alphaclops.commutes(A(a), A(a))
        assert alphaclops.commutes(A, XXGate, default='default') == 'default'
    for A, B in [
        (XGate, YGate),
        (XGate, ZGate),
        (ZGate, YGate),
        (XGate, alphaclops.Y),
        (XGate, alphaclops.Z),
        (ZGate, alphaclops.Y),
    ]:
        assert not alphaclops.commutes(A, B)
        assert alphaclops.commutes(A(a), B(b))
        assert not alphaclops.commutes(A(a), B(a))
        with pytest.raises(TypeError):
            alphaclops.commutes(A, B(a))
        alphaclops.testing.assert_commutes_magic_method_consistent_with_unitaries(A, B)
    for A, B in [(XXGate, YYGate), (XXGate, ZZGate)]:
        assert alphaclops.commutes(A, B)
        with pytest.raises(TypeError):
            alphaclops.commutes(A(a, b), B)
        with pytest.raises(TypeError):
            alphaclops.commutes(A, B(a, b))
        assert alphaclops.commutes(A(a, b), B(a, b))
        assert alphaclops.definitely_commutes(A(a, b), B(a, b))
        alphaclops.testing.assert_commutes_magic_method_consistent_with_unitaries(A, B)
    for A, B in [(XGate, XXGate), (XGate, YYGate)]:
        with pytest.raises(TypeError):
            alphaclops.commutes(A, B(a, b))
        assert not alphaclops.definitely_commutes(A, B(a, b))
        with pytest.raises(TypeError):
            assert alphaclops.commutes(A(b), B)
        with pytest.raises(TypeError):
            assert alphaclops.commutes(A, B)
        alphaclops.testing.assert_commutes_magic_method_consistent_with_unitaries(A, B)
    with pytest.raises(TypeError):
        assert alphaclops.commutes(XGate, alphaclops.X ** sympy.Symbol('e'))
    with pytest.raises(TypeError):
        assert alphaclops.commutes(XGate(a), 'Gate')
    assert alphaclops.commutes(XGate(a), 'Gate', default='default') == 'default'


def test_operation_commutes_using_overlap_and_unitary():
    class CustomCnotGate(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 2

        def _unitary_(self):
            return alphaclops.unitary(alphaclops.CNOT)

    custom_cnot_gate = CustomCnotGate()

    class CustomCnotOp(alphaclops.Operation):
        def __init__(self, *qs: alphaclops.Qid):
            self.qs = qs

        def _unitary_(self):
            return alphaclops.unitary(alphaclops.CNOT)

        @property
        def qubits(self):
            return self.qs

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

    class NoDetails(alphaclops.Operation):
        def __init__(self, *qs: alphaclops.Qid):
            self.qs = qs

        @property
        def qubits(self):
            return self.qs

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

    a, b, c = alphaclops.LineQubit.range(3)

    # If ops overlap with known unitaries, fallback to matrix commutation.
    assert not alphaclops.commutes(CustomCnotOp(a, b), CustomCnotOp(b, a))
    assert not alphaclops.commutes(CustomCnotOp(a, b), CustomCnotOp(b, c))
    assert alphaclops.commutes(CustomCnotOp(a, b), CustomCnotOp(c, b))
    assert alphaclops.commutes(CustomCnotOp(a, b), CustomCnotOp(a, b))

    # If ops don't overlap, they commute. Even when no specified unitary.
    assert alphaclops.commutes(CustomCnotOp(a, b), NoDetails(c))

    # If ops overlap and there's no unitary, result is indeterminate.
    assert alphaclops.commutes(CustomCnotOp(a, b), NoDetails(a), default=None) is None

    # Same stuff works with custom gate, or mix of custom gate and custom op.
    assert alphaclops.commutes(custom_cnot_gate(a, b), CustomCnotOp(a, b))
    assert alphaclops.commutes(custom_cnot_gate(a, b), custom_cnot_gate(a, b))
    assert alphaclops.commutes(custom_cnot_gate(a, b), CustomCnotOp(c, b))
    assert alphaclops.commutes(custom_cnot_gate(a, b), custom_cnot_gate(c, b))
    assert not alphaclops.commutes(custom_cnot_gate(a, b), CustomCnotOp(b, a))
    assert not alphaclops.commutes(custom_cnot_gate(a, b), custom_cnot_gate(b, a))
    assert not alphaclops.commutes(custom_cnot_gate(a, b), CustomCnotOp(b, c))
    assert not alphaclops.commutes(custom_cnot_gate(a, b), custom_cnot_gate(b, c))
