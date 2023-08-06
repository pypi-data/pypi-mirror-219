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

import sympy

import alphaclops
from alphaclops.interop.quirk.cells.testing import assert_url_to_circuit_returns


def test_fixed_single_qubit_rotations():
    a, b, c, d = alphaclops.LineQubit.range(4)

    assert_url_to_circuit_returns(
        '{"cols":[["H","X","Y","Z"]]}', alphaclops.Circuit(alphaclops.H(a), alphaclops.X(b), alphaclops.Y(c), alphaclops.Z(d))
    )

    assert_url_to_circuit_returns(
        '{"cols":[["X^½","X^⅓","X^¼"],'
        '["X^⅛","X^⅟₁₆","X^⅟₃₂"],'
        '["X^-½","X^-⅓","X^-¼"],'
        '["X^-⅛","X^-⅟₁₆","X^-⅟₃₂"]]}',
        alphaclops.Circuit(
            alphaclops.X(a) ** (1 / 2),
            alphaclops.X(b) ** (1 / 3),
            alphaclops.X(c) ** (1 / 4),
            alphaclops.X(a) ** (1 / 8),
            alphaclops.X(b) ** (1 / 16),
            alphaclops.X(c) ** (1 / 32),
            alphaclops.X(a) ** (-1 / 2),
            alphaclops.X(b) ** (-1 / 3),
            alphaclops.X(c) ** (-1 / 4),
            alphaclops.X(a) ** (-1 / 8),
            alphaclops.X(b) ** (-1 / 16),
            alphaclops.X(c) ** (-1 / 32),
        ),
    )

    assert_url_to_circuit_returns(
        '{"cols":[["Y^½","Y^⅓","Y^¼"],'
        '["Y^⅛","Y^⅟₁₆","Y^⅟₃₂"],'
        '["Y^-½","Y^-⅓","Y^-¼"],'
        '["Y^-⅛","Y^-⅟₁₆","Y^-⅟₃₂"]]}',
        alphaclops.Circuit(
            alphaclops.Y(a) ** (1 / 2),
            alphaclops.Y(b) ** (1 / 3),
            alphaclops.Y(c) ** (1 / 4),
            alphaclops.Y(a) ** (1 / 8),
            alphaclops.Y(b) ** (1 / 16),
            alphaclops.Y(c) ** (1 / 32),
            alphaclops.Y(a) ** (-1 / 2),
            alphaclops.Y(b) ** (-1 / 3),
            alphaclops.Y(c) ** (-1 / 4),
            alphaclops.Y(a) ** (-1 / 8),
            alphaclops.Y(b) ** (-1 / 16),
            alphaclops.Y(c) ** (-1 / 32),
        ),
    )

    assert_url_to_circuit_returns(
        '{"cols":[["Z^½","Z^⅓","Z^¼"],'
        '["Z^⅛","Z^⅟₁₆","Z^⅟₃₂"],'
        '["Z^⅟₆₄","Z^⅟₁₂₈"],'
        '["Z^-½","Z^-⅓","Z^-¼"],'
        '["Z^-⅛","Z^-⅟₁₆"]]}',
        alphaclops.Circuit(
            alphaclops.Z(a) ** (1 / 2),
            alphaclops.Z(b) ** (1 / 3),
            alphaclops.Z(c) ** (1 / 4),
            alphaclops.Z(a) ** (1 / 8),
            alphaclops.Z(b) ** (1 / 16),
            alphaclops.Z(c) ** (1 / 32),
            alphaclops.Z(a) ** (1 / 64),
            alphaclops.Z(b) ** (1 / 128),
            alphaclops.Moment([alphaclops.Z(a) ** (-1 / 2), alphaclops.Z(b) ** (-1 / 3), alphaclops.Z(c) ** (-1 / 4)]),
            alphaclops.Z(a) ** (-1 / 8),
            alphaclops.Z(b) ** (-1 / 16),
        ),
    )


def test_dynamic_single_qubit_rotations():
    a, b, c = alphaclops.LineQubit.range(3)
    t = sympy.Symbol('t')

    # Dynamic single qubit rotations.
    assert_url_to_circuit_returns(
        '{"cols":[["X^t","Y^t","Z^t"],["X^-t","Y^-t","Z^-t"]]}',
        alphaclops.Circuit(
            alphaclops.X(a) ** t,
            alphaclops.Y(b) ** t,
            alphaclops.Z(c) ** t,
            alphaclops.X(a) ** -t,
            alphaclops.Y(b) ** -t,
            alphaclops.Z(c) ** -t,
        ),
    )
    assert_url_to_circuit_returns(
        '{"cols":[["e^iXt","e^iYt","e^iZt"],["e^-iXt","e^-iYt","e^-iZt"]]}',
        alphaclops.Circuit(
            alphaclops.rx(2 * sympy.pi * t).on(a),
            alphaclops.ry(2 * sympy.pi * t).on(b),
            alphaclops.rz(2 * sympy.pi * t).on(c),
            alphaclops.rx(2 * sympy.pi * -t).on(a),
            alphaclops.ry(2 * sympy.pi * -t).on(b),
            alphaclops.rz(2 * sympy.pi * -t).on(c),
        ),
    )


def test_formulaic_gates():
    a, b = alphaclops.LineQubit.range(2)
    t = sympy.Symbol('t')

    assert_url_to_circuit_returns(
        '{"cols":[["X^ft",{"id":"X^ft","arg":"t*t"}]]}',
        alphaclops.Circuit(alphaclops.X(a) ** sympy.sin(sympy.pi * t), alphaclops.X(b) ** (t * t)),
    )
    assert_url_to_circuit_returns(
        '{"cols":[["Y^ft",{"id":"Y^ft","arg":"t*t"}]]}',
        alphaclops.Circuit(alphaclops.Y(a) ** sympy.sin(sympy.pi * t), alphaclops.Y(b) ** (t * t)),
    )
    assert_url_to_circuit_returns(
        '{"cols":[["Z^ft",{"id":"Z^ft","arg":"t*t"}]]}',
        alphaclops.Circuit(alphaclops.Z(a) ** sympy.sin(sympy.pi * t), alphaclops.Z(b) ** (t * t)),
    )
    assert_url_to_circuit_returns(
        '{"cols":[["Rxft",{"id":"Rxft","arg":"t*t"}]]}',
        alphaclops.Circuit(alphaclops.rx(sympy.pi * t * t).on(a), alphaclops.rx(t * t).on(b)),
    )
    assert_url_to_circuit_returns(
        '{"cols":[["Ryft",{"id":"Ryft","arg":"t*t"}]]}',
        alphaclops.Circuit(alphaclops.ry(sympy.pi * t * t).on(a), alphaclops.ry(t * t).on(b)),
    )
    assert_url_to_circuit_returns(
        '{"cols":[["Rzft",{"id":"Rzft","arg":"t*t"}]]}',
        alphaclops.Circuit(alphaclops.rz(sympy.pi * t * t).on(a), alphaclops.rz(t * t).on(b)),
    )
