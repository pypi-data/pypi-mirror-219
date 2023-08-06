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

import alphaclops
from alphaclops.interop.quirk.cells.testing import assert_url_to_circuit_returns


def test_controls():
    a, b = alphaclops.LineQubit.range(2)

    assert_url_to_circuit_returns('{"cols":[["•","X"]]}', alphaclops.Circuit(alphaclops.X(b).controlled_by(a)))
    assert_url_to_circuit_returns(
        '{"cols":[["◦","X"]]}', alphaclops.Circuit(alphaclops.X(a), alphaclops.X(b).controlled_by(a), alphaclops.X(a))
    )

    assert_url_to_circuit_returns(
        '{"cols":[["⊕","X"]]}',
        alphaclops.Circuit(alphaclops.Y(a) ** 0.5, alphaclops.X(b).controlled_by(a), alphaclops.Y(a) ** -0.5),
        output_amplitudes_from_quirk=[
            {"r": 0.5, "i": 0},
            {"r": -0.5, "i": 0},
            {"r": 0.5, "i": 0},
            {"r": 0.5, "i": 0},
        ],
    )
    assert_url_to_circuit_returns(
        '{"cols":[["⊖","X"]]}',
        alphaclops.Circuit(alphaclops.Y(a) ** -0.5, alphaclops.X(b).controlled_by(a), alphaclops.Y(a) ** +0.5),
        output_amplitudes_from_quirk=[
            {"r": 0.5, "i": 0},
            {"r": 0.5, "i": 0},
            {"r": 0.5, "i": 0},
            {"r": -0.5, "i": 0},
        ],
    )

    assert_url_to_circuit_returns(
        '{"cols":[["⊗","X"]]}',
        alphaclops.Circuit(alphaclops.X(a) ** -0.5, alphaclops.X(b).controlled_by(a), alphaclops.X(a) ** +0.5),
        output_amplitudes_from_quirk=[
            {"r": 0.5, "i": 0},
            {"r": 0, "i": -0.5},
            {"r": 0.5, "i": 0},
            {"r": 0, "i": 0.5},
        ],
    )
    assert_url_to_circuit_returns(
        '{"cols":[["(/)","X"]]}',
        alphaclops.Circuit(alphaclops.X(a) ** +0.5, alphaclops.X(b).controlled_by(a), alphaclops.X(a) ** -0.5),
        output_amplitudes_from_quirk=[
            {"r": 0.5, "i": 0},
            {"r": 0, "i": 0.5},
            {"r": 0.5, "i": 0},
            {"r": 0, "i": -0.5},
        ],
    )

    qs = alphaclops.LineQubit.range(8)
    assert_url_to_circuit_returns(
        '{"cols":[["X","•","◦","⊕","⊖","⊗","(/)","Z"]]}',
        alphaclops.Circuit(
            alphaclops.X(qs[2]),
            alphaclops.Y(qs[3]) ** 0.5,
            alphaclops.Y(qs[4]) ** -0.5,
            alphaclops.X(qs[5]) ** -0.5,
            alphaclops.X(qs[6]) ** 0.5,
            alphaclops.X(qs[0]).controlled_by(*qs[1:7]),
            alphaclops.Z(qs[7]).controlled_by(*qs[1:7]),
            alphaclops.X(qs[6]) ** -0.5,
            alphaclops.X(qs[5]) ** 0.5,
            alphaclops.Y(qs[4]) ** 0.5,
            alphaclops.Y(qs[3]) ** -0.5,
            alphaclops.X(qs[2]),
        ),
    )


def test_parity_controls():
    a, b, c, d, e = alphaclops.LineQubit.range(5)

    assert_url_to_circuit_returns(
        '{"cols":[["Y","xpar","ypar","zpar","Z"]]}',
        alphaclops.Circuit(
            alphaclops.Y(b) ** 0.5,
            alphaclops.X(c) ** -0.5,
            alphaclops.CNOT(c, b),
            alphaclops.CNOT(d, b),
            alphaclops.Y(a).controlled_by(b),
            alphaclops.Z(e).controlled_by(b),
            alphaclops.CNOT(d, b),
            alphaclops.CNOT(c, b),
            alphaclops.X(c) ** 0.5,
            alphaclops.Y(b) ** -0.5,
        ),
    )


def test_control_with_line_qubits_mapped_to():
    a, b = alphaclops.LineQubit.range(2)
    a2, b2 = alphaclops.NamedQubit.range(2, prefix='q')
    cell = alphaclops.interop.quirk.cells.control_cells.ControlCell(a, [alphaclops.Y(b) ** 0.5])
    mapped_cell = alphaclops.interop.quirk.cells.control_cells.ControlCell(a2, [alphaclops.Y(b2) ** 0.5])
    assert cell != mapped_cell
    assert cell.with_line_qubits_mapped_to([a2, b2]) == mapped_cell


def test_parity_control_with_line_qubits_mapped_to():
    a, b, c = alphaclops.LineQubit.range(3)
    a2, b2, c2 = alphaclops.NamedQubit.range(3, prefix='q')
    cell = alphaclops.interop.quirk.cells.control_cells.ParityControlCell([a, b], [alphaclops.Y(c) ** 0.5])
    mapped_cell = alphaclops.interop.quirk.cells.control_cells.ParityControlCell(
        [a2, b2], [alphaclops.Y(c2) ** 0.5]
    )
    assert cell != mapped_cell
    assert cell.with_line_qubits_mapped_to([a2, b2, c2]) == mapped_cell


def test_repr():
    a, b, c = alphaclops.LineQubit.range(3)
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.interop.quirk.cells.control_cells.ControlCell(a, [alphaclops.Y(b) ** 0.5])
    )
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.interop.quirk.cells.control_cells.ParityControlCell([a, b], [alphaclops.Y(c) ** 0.5])
    )
