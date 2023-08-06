# Copyright 2019 The alphaclops Developers
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
import pytest

import alphaclops
from alphaclops.interop.quirk.cells.cell import Cell, ExplicitOperationsCell


def test_cell_defaults():
    class BasicCell(Cell):
        def with_line_qubits_mapped_to(self, qubits):
            raise NotImplementedError()

        def gate_count(self) -> int:
            raise NotImplementedError()

    c = BasicCell()
    assert c.operations() == ()
    assert c.basis_change() == ()
    assert c.controlled_by(alphaclops.LineQubit(0)) is c
    x = []
    c.modify_column(x)
    assert x == []


def test_cell_replace_utils():
    a, b, c = alphaclops.NamedQubit.range(3, prefix='q')
    assert Cell._replace_qubit(alphaclops.LineQubit(1), [a, b, c]) == b
    with pytest.raises(ValueError, match='only map from line qubits'):
        _ = Cell._replace_qubit(alphaclops.TensorCircuit(0, 0), [a, b, c])
    with pytest.raises(ValueError, match='not in range'):
        _ = Cell._replace_qubit(alphaclops.LineQubit(-1), [a, b, c])
    with pytest.raises(ValueError, match='not in range'):
        _ = Cell._replace_qubit(alphaclops.LineQubit(999), [a, b, c])


def test_explicit_operations_cell_equality():
    a = alphaclops.LineQubit(0)
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(ExplicitOperationsCell([], []), ExplicitOperationsCell([]))
    eq.add_equality_group(ExplicitOperationsCell([alphaclops.X(a)], []))
    eq.add_equality_group(ExplicitOperationsCell([], [alphaclops.Y(a)]))


def test_explicit_operations_cell():
    a, b = alphaclops.LineQubit.range(2)
    v = ExplicitOperationsCell([alphaclops.X(a)], [alphaclops.S(a)])
    assert v.operations() == (alphaclops.X(a),)
    assert v.basis_change() == (alphaclops.S(a),)
    assert v.controlled_by(b) == ExplicitOperationsCell([alphaclops.X(a).controlled_by(b)], [alphaclops.S(a)])
