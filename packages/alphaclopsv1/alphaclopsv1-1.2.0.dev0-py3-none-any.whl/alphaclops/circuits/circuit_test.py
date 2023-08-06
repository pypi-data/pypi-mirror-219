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
import os
import time
from collections import defaultdict
from random import randint, random, sample, randrange
from typing import Iterator, Optional, Tuple, TYPE_CHECKING

import numpy as np
import pytest
import sympy

import alphaclops
import alphaclops.testing
from alphaclops import circuits
from alphaclops import ops
from alphaclops.testing.devices import ValidatingTestDevice


class _Foxy(ValidatingTestDevice):
    pass


FOXY = _Foxy(
    allowed_qubit_types=(alphaclops.TensorCircuit,),
    allowed_gates=(ops.CZPowGate, ops.XPowGate, ops.YPowGate, ops.ZPowGate),
    qubits=set(alphaclops.TensorCircuit.rect(2, 7)),
    name=f'{__name__}.FOXY',
    auto_decompose_gates=(ops.CCXPowGate,),
    validate_locality=True,
)


BCONE = ValidatingTestDevice(
    allowed_qubit_types=(alphaclops.TensorCircuit,),
    allowed_gates=(ops.XPowGate,),
    qubits={alphaclops.TensorCircuit(0, 6)},
    name=f'{__name__}.BCONE',
)


if TYPE_CHECKING:
    import alphaclops

q0, q1, q2, q3 = alphaclops.LineQubit.range(4)


class _MomentAndOpTypeValidatingDeviceType(alphaclops.Device):
    def validate_operation(self, operation):
        if not isinstance(operation, alphaclops.Operation):
            raise ValueError(f'not isinstance({operation!r}, {alphaclops.Operation!r})')

    def validate_moment(self, moment):
        if not isinstance(moment, alphaclops.Moment):
            raise ValueError(f'not isinstance({moment!r}, {alphaclops.Moment!r})')


moment_and_op_type_validating_device = _MomentAndOpTypeValidatingDeviceType()


def test_from_moments():
    a, b, c, d = alphaclops.LineQubit.range(4)
    assert alphaclops.Circuit.from_moments(
        [alphaclops.X(a), alphaclops.Y(b)],
        [alphaclops.X(c)],
        [],
        alphaclops.Z(d),
        [alphaclops.measure(a, b, key='ab'), alphaclops.measure(c, d, key='cd')],
    ) == alphaclops.Circuit(
        alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b)),
        alphaclops.Moment(alphaclops.X(c)),
        alphaclops.Moment(),
        alphaclops.Moment(alphaclops.Z(d)),
        alphaclops.Moment(alphaclops.measure(a, b, key='ab'), alphaclops.measure(c, d, key='cd')),
    )


def test_alignment():
    assert repr(alphaclops.LineSteam.LEFT) == 'alphaclops.LineSteam.LEFT'
    assert repr(alphaclops.LineSteam.RIGHT) == 'alphaclops.LineSteam.RIGHT'


def test_setitem():
    circuit = alphaclops.Circuit([alphaclops.Moment(), alphaclops.Moment()])

    circuit[1] = alphaclops.Moment([alphaclops.X(alphaclops.LineQubit(0))])
    assert circuit == alphaclops.Circuit([alphaclops.Moment(), alphaclops.Moment([alphaclops.X(alphaclops.LineQubit(0))])])

    circuit[1:1] = (
        alphaclops.Moment([alphaclops.Y(alphaclops.LineQubit(0))]),
        alphaclops.Moment([alphaclops.Z(alphaclops.LineQubit(0))]),
    )
    assert circuit == alphaclops.Circuit(
        [
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.Y(alphaclops.LineQubit(0))]),
            alphaclops.Moment([alphaclops.Z(alphaclops.LineQubit(0))]),
            alphaclops.Moment([alphaclops.X(alphaclops.LineQubit(0))]),
        ]
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_equality(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    eq = alphaclops.testing.EqualsTester()

    # Default is empty. Iterables get listed.
    eq.add_equality_group(circuit_cls(), circuit_cls([]), circuit_cls(()))
    eq.add_equality_group(circuit_cls([alphaclops.Moment()]), circuit_cls((alphaclops.Moment(),)))

    # Equality depends on structure and contents.
    eq.add_equality_group(circuit_cls([alphaclops.Moment([alphaclops.X(a)])]))
    eq.add_equality_group(circuit_cls([alphaclops.Moment([alphaclops.X(b)])]))
    eq.add_equality_group(circuit_cls([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(b)])]))
    eq.add_equality_group(circuit_cls([alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)])]))

    # Big case.
    eq.add_equality_group(
        circuit_cls(
            [
                alphaclops.Moment([alphaclops.H(a), alphaclops.H(b)]),
                alphaclops.Moment([alphaclops.CZ(a, b)]),
                alphaclops.Moment([alphaclops.H(b)]),
            ]
        )
    )
    eq.add_equality_group(circuit_cls([alphaclops.Moment([alphaclops.H(a)]), alphaclops.Moment([alphaclops.CNOT(a, b)])]))


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_approx_eq(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    assert not alphaclops.approx_eq(circuit_cls([alphaclops.Moment([alphaclops.X(a)])]), alphaclops.Moment([alphaclops.X(a)]))

    assert alphaclops.approx_eq(
        circuit_cls([alphaclops.Moment([alphaclops.X(a)])]), circuit_cls([alphaclops.Moment([alphaclops.X(a)])])
    )
    assert not alphaclops.approx_eq(
        circuit_cls([alphaclops.Moment([alphaclops.X(a)])]), circuit_cls([alphaclops.Moment([alphaclops.X(b)])])
    )

    assert alphaclops.approx_eq(
        circuit_cls([alphaclops.Moment([alphaclops.XPowGate(exponent=0)(a)])]),
        circuit_cls([alphaclops.Moment([alphaclops.XPowGate(exponent=1e-9)(a)])]),
    )

    assert not alphaclops.approx_eq(
        circuit_cls([alphaclops.Moment([alphaclops.XPowGate(exponent=0)(a)])]),
        circuit_cls([alphaclops.Moment([alphaclops.XPowGate(exponent=1e-7)(a)])]),
    )
    assert alphaclops.approx_eq(
        circuit_cls([alphaclops.Moment([alphaclops.XPowGate(exponent=0)(a)])]),
        circuit_cls([alphaclops.Moment([alphaclops.XPowGate(exponent=1e-7)(a)])]),
        atol=1e-6,
    )


def test_append_single():
    a = alphaclops.NamedQubit('a')

    c = alphaclops.Circuit()
    c.append(())
    assert c == alphaclops.Circuit()

    c = alphaclops.Circuit()
    c.append(alphaclops.X(a))
    assert c == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a)])])

    c = alphaclops.Circuit()
    c.append([alphaclops.X(a)])
    assert c == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a)])])

    c = alphaclops.Circuit(alphaclops.H(a))
    c.append(c)
    assert c == alphaclops.Circuit(
        [alphaclops.Moment(alphaclops.H(alphaclops.NamedQubit('a'))), alphaclops.Moment(alphaclops.H(alphaclops.NamedQubit('a')))]
    )


def test_append_control_key():
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    c = alphaclops.Circuit()
    c.append(alphaclops.measure(q0, key='a'))
    c.append(alphaclops.X(q1).with_classical_controls('a'))
    assert len(c) == 2

    c = alphaclops.Circuit()
    c.append(alphaclops.measure(q0, key='a'))
    c.append(alphaclops.X(q1).with_classical_controls('b'))
    c.append(alphaclops.X(q2).with_classical_controls('b'))
    assert len(c) == 1


def test_append_multiple():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    c = alphaclops.Circuit()
    c.append([alphaclops.X(a), alphaclops.X(b)], alphaclops.InsertStrategy.NEW)
    assert c == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(b)])])

    c = alphaclops.Circuit()
    c.append([alphaclops.X(a), alphaclops.X(b)], alphaclops.InsertStrategy.EARLIEST)
    assert c == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)])])

    c = alphaclops.Circuit()
    c.append(alphaclops.X(a), alphaclops.InsertStrategy.EARLIEST)
    c.append(alphaclops.X(b), alphaclops.InsertStrategy.EARLIEST)
    assert c == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)])])


def test_append_control_key_subcircuit():
    q0, q1 = alphaclops.LineQubit.range(2)

    c = alphaclops.Circuit()
    c.append(alphaclops.measure(q0, key='a'))
    c.append(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.ClassicallyControlledOperation(alphaclops.X(q1), 'a'))
        )
    )
    assert len(c) == 2

    c = alphaclops.Circuit()
    c.append(alphaclops.measure(q0, key='a'))
    c.append(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.ClassicallyControlledOperation(alphaclops.X(q1), 'b'))
        )
    )
    assert len(c) == 1

    c = alphaclops.Circuit()
    c.append(alphaclops.measure(q0, key='a'))
    c.append(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.ClassicallyControlledOperation(alphaclops.X(q1), 'b'))
        ).with_measurement_key_mapping({'b': 'a'})
    )
    assert len(c) == 2

    c = alphaclops.Circuit()
    c.append(alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.measure(q0, key='a'))))
    c.append(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.ClassicallyControlledOperation(alphaclops.X(q1), 'b'))
        ).with_measurement_key_mapping({'b': 'a'})
    )
    assert len(c) == 2

    c = alphaclops.Circuit()
    c.append(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.measure(q0, key='a'))
        ).with_measurement_key_mapping({'a': 'c'})
    )
    c.append(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.ClassicallyControlledOperation(alphaclops.X(q1), 'b'))
        ).with_measurement_key_mapping({'b': 'c'})
    )
    assert len(c) == 2

    c = alphaclops.Circuit()
    c.append(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.measure(q0, key='a'))
        ).with_measurement_key_mapping({'a': 'b'})
    )
    c.append(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.ClassicallyControlledOperation(alphaclops.X(q1), 'b'))
        ).with_measurement_key_mapping({'b': 'a'})
    )
    assert len(c) == 1


def test_measurement_key_paths():
    a = alphaclops.LineQubit(0)
    circuit1 = alphaclops.Circuit(alphaclops.measure(a, key='A'))
    assert alphaclops.measurement_key_names(circuit1) == {'A'}
    circuit2 = alphaclops.with_key_path(circuit1, ('B',))
    assert alphaclops.measurement_key_names(circuit2) == {'B:A'}
    circuit3 = alphaclops.with_key_path_prefix(circuit2, ('C',))
    assert alphaclops.measurement_key_names(circuit3) == {'C:B:A'}


def test_append_moments():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    c = alphaclops.Circuit()
    c.append(alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]), alphaclops.InsertStrategy.NEW)
    assert c == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)])])

    c = alphaclops.Circuit()
    c.append(
        [alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]), alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)])],
        alphaclops.InsertStrategy.NEW,
    )
    assert c == alphaclops.Circuit(
        [alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]), alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)])]
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_add_op_tree(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    c = circuit_cls()
    assert c + [alphaclops.X(a), alphaclops.Y(b)] == circuit_cls([alphaclops.Moment([alphaclops.X(a), alphaclops.Y(b)])])

    assert c + alphaclops.X(a) == circuit_cls(alphaclops.X(a))
    assert c + [alphaclops.X(a)] == circuit_cls(alphaclops.X(a))
    assert c + [[[alphaclops.X(a)], []]] == circuit_cls(alphaclops.X(a))
    assert c + (alphaclops.X(a),) == circuit_cls(alphaclops.X(a))
    assert c + (alphaclops.X(a) for _ in range(1)) == circuit_cls(alphaclops.X(a))
    with pytest.raises(TypeError):
        _ = c + alphaclops.X


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_radd_op_tree(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    c = circuit_cls()
    assert [alphaclops.X(a), alphaclops.Y(b)] + c == circuit_cls([alphaclops.Moment([alphaclops.X(a), alphaclops.Y(b)])])

    assert alphaclops.X(a) + c == circuit_cls(alphaclops.X(a))
    assert [alphaclops.X(a)] + c == circuit_cls(alphaclops.X(a))
    assert [[[alphaclops.X(a)], []]] + c == circuit_cls(alphaclops.X(a))
    assert (alphaclops.X(a),) + c == circuit_cls(alphaclops.X(a))
    assert (alphaclops.X(a) for _ in range(1)) + c == circuit_cls(alphaclops.X(a))
    with pytest.raises(AttributeError):
        _ = alphaclops.X + c
    with pytest.raises(TypeError):
        _ = 0 + c

    # non-empty circuit addition
    if circuit_cls == alphaclops.FrozenCircuit:
        d = alphaclops.FrozenCircuit(alphaclops.Y(b))
    else:
        d = alphaclops.Circuit()
        d.append(alphaclops.Y(b))
    assert [alphaclops.X(a)] + d == circuit_cls([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.Y(b)])])
    assert alphaclops.Moment([alphaclops.X(a)]) + d == circuit_cls(
        [alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.Y(b)])]
    )


def test_add_iadd_equivalence():
    q0, q1 = alphaclops.LineQubit.range(2)
    iadd_circuit = alphaclops.Circuit(alphaclops.X(q0))
    iadd_circuit += alphaclops.H(q1)

    add_circuit = alphaclops.Circuit(alphaclops.X(q0)) + alphaclops.H(q1)
    assert iadd_circuit == add_circuit


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_bool(circuit_cls):
    assert not circuit_cls()
    assert circuit_cls(alphaclops.X(alphaclops.NamedQubit('a')))


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_repr(circuit_cls):
    assert repr(circuit_cls()) == f'alphaclops.{circuit_cls.__name__}()'

    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = circuit_cls(
        [alphaclops.Moment([alphaclops.H(a), alphaclops.H(b)]), alphaclops.Moment(), alphaclops.Moment([alphaclops.CZ(a, b)])]
    )
    alphaclops.testing.assert_equivalent_repr(c)
    assert (
        repr(c)
        == f"""alphaclops.{circuit_cls.__name__}([
    alphaclops.Moment(
        alphaclops.H(alphaclops.NamedQubit('a')),
        alphaclops.H(alphaclops.NamedQubit('b')),
    ),
    alphaclops.Moment(),
    alphaclops.Moment(
        alphaclops.CZ(alphaclops.NamedQubit('a'), alphaclops.NamedQubit('b')),
    ),
])"""
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_empty_moments(circuit_cls):
    # 1-qubit test
    op = alphaclops.X(alphaclops.NamedQubit('a'))
    op_moment = alphaclops.Moment([op])
    circuit = circuit_cls([op_moment, op_moment, alphaclops.Moment(), op_moment])

    alphaclops.testing.assert_has_diagram(circuit, "a: ───X───X───────X───", use_unicode_characters=True)
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a
│
X
│
X
│
│
│
X
│
""",
        use_unicode_characters=True,
        transpose=True,
    )

    # 1-qubit ascii-only test
    alphaclops.testing.assert_has_diagram(circuit, "a: ---X---X-------X---", use_unicode_characters=False)
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a
|
X
|
X
|
|
|
X
|
""",
        use_unicode_characters=False,
        transpose=True,
    )

    # 2-qubit test
    op = alphaclops.CNOT(alphaclops.NamedQubit('a'), alphaclops.NamedQubit('b'))
    op_moment = alphaclops.Moment([op])
    circuit = circuit_cls([op_moment, op_moment, alphaclops.Moment(), op_moment])

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a: ───@───@───────@───
      │   │       │
b: ───X───X───────X───""",
        use_unicode_characters=True,
    )
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a b
│ │
@─X
│ │
@─X
│ │
│ │
│ │
@─X
│ │
""",
        use_unicode_characters=True,
        transpose=True,
    )

    # 2-qubit ascii-only test
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a: ---@---@-------@---
      |   |       |
b: ---X---X-------X---""",
        use_unicode_characters=False,
    )
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a b
| |
@-X
| |
@-X
| |
| |
| |
@-X
| |
""",
        use_unicode_characters=False,
        transpose=True,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_symbol_addition_in_gate_exponent(circuit_cls):
    # 1-qubit test
    qubit = alphaclops.NamedQubit('a')
    circuit = circuit_cls(
        alphaclops.X(qubit) ** 0.5,
        alphaclops.YPowGate(exponent=sympy.Symbol('a') + sympy.Symbol('b')).on(qubit),
    )
    alphaclops.testing.assert_has_diagram(
        circuit, 'a: ───X^0.5───Y^(a + b)───', use_unicode_characters=True
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a
│
X^0.5
│
Y^(a + b)
│
""",
        use_unicode_characters=True,
        transpose=True,
    )

    alphaclops.testing.assert_has_diagram(
        circuit, 'a: ---X^0.5---Y^(a + b)---', use_unicode_characters=False
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a
|
X^0.5
|
Y^(a + b)
|

 """,
        use_unicode_characters=False,
        transpose=True,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_slice(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = circuit_cls(
        [
            alphaclops.Moment([alphaclops.H(a), alphaclops.H(b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.H(b)]),
        ]
    )
    assert c[0:1] == circuit_cls([alphaclops.Moment([alphaclops.H(a), alphaclops.H(b)])])
    assert c[::2] == circuit_cls([alphaclops.Moment([alphaclops.H(a), alphaclops.H(b)]), alphaclops.Moment([alphaclops.H(b)])])
    assert c[0:1:2] == circuit_cls([alphaclops.Moment([alphaclops.H(a), alphaclops.H(b)])])
    assert c[1:3:] == circuit_cls([alphaclops.Moment([alphaclops.CZ(a, b)]), alphaclops.Moment([alphaclops.H(b)])])
    assert c[::-1] == circuit_cls(
        [
            alphaclops.Moment([alphaclops.H(b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.H(a), alphaclops.H(b)]),
        ]
    )
    assert c[3:0:-1] == circuit_cls([alphaclops.Moment([alphaclops.H(b)]), alphaclops.Moment([alphaclops.CZ(a, b)])])
    assert c[0:2:-1] == circuit_cls()


def test_concatenate():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    c = alphaclops.Circuit()
    d = alphaclops.Circuit([alphaclops.Moment([alphaclops.X(b)])])
    e = alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)])])

    assert c + d == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(b)])])
    assert d + c == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(b)])])
    assert e + d == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]), alphaclops.Moment([alphaclops.X(b)])])

    d += c
    assert d == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(b)])])

    c += d
    assert c == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(b)])])

    f = e + d
    f += e
    assert f == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
            alphaclops.Moment([alphaclops.X(b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    with pytest.raises(TypeError):
        _ = c + 'a'


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_multiply(circuit_cls):
    a = alphaclops.NamedQubit('a')

    c = circuit_cls()
    d = circuit_cls([alphaclops.Moment([alphaclops.X(a)])])

    assert c * 0 == circuit_cls()
    assert d * 0 == circuit_cls()
    assert d * 2 == circuit_cls([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(a)])])

    twice_copied_circuit = circuit_cls([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(a)])])
    for num in [np.int64(2), np.ushort(2), np.int8(2), np.int32(2), np.short(2)]:
        assert num * d == twice_copied_circuit
        assert d * num == twice_copied_circuit

    assert np.array([2])[0] * d == circuit_cls([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(a)])])
    assert 1 * c == circuit_cls()
    assert -1 * d == circuit_cls()
    assert 1 * d == circuit_cls([alphaclops.Moment([alphaclops.X(a)])])

    d *= 3
    assert d == circuit_cls(
        [alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(a)])]
    )

    with pytest.raises(TypeError):
        _ = c * 'a'
    with pytest.raises(TypeError):
        _ = 'a' * c
    with pytest.raises(TypeError):
        c *= 'a'


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_container_methods(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = circuit_cls(
        [
            alphaclops.Moment([alphaclops.H(a), alphaclops.H(b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.H(b)]),
        ]
    )
    assert list(c) == list(c._moments)
    # __iter__
    assert list(iter(c)) == list(c._moments)
    # __reversed__ for free.
    assert list(reversed(c)) == list(reversed(c._moments))
    # __contains__ for free.
    assert alphaclops.Moment([alphaclops.H(b)]) in c

    assert len(c) == 3


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_bad_index(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = circuit_cls([alphaclops.Moment([alphaclops.H(a), alphaclops.H(b)])])
    with pytest.raises(TypeError):
        _ = c['string']


def test_append_strategies():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    stream = [alphaclops.X(a), alphaclops.CZ(a, b), alphaclops.X(b), alphaclops.X(b), alphaclops.X(a)]

    c = alphaclops.Circuit()
    c.append(stream, alphaclops.InsertStrategy.NEW)
    assert c == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(b)]),
            alphaclops.Moment([alphaclops.X(b)]),
            alphaclops.Moment([alphaclops.X(a)]),
        ]
    )

    c = alphaclops.Circuit()
    c.append(stream, alphaclops.InsertStrategy.INLINE)
    assert c == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(b)]),
            alphaclops.Moment([alphaclops.X(b), alphaclops.X(a)]),
        ]
    )

    c = alphaclops.Circuit()
    c.append(stream, alphaclops.InsertStrategy.EARLIEST)
    assert c == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(b), alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.X(b)]),
        ]
    )


def test_insert_op_tree_new():
    a = alphaclops.NamedQubit('alice')
    b = alphaclops.NamedQubit('bob')
    c = alphaclops.Circuit()

    op_tree_list = [
        (-10, 0, alphaclops.CZ(a, b), a),
        (-20, 0, alphaclops.X(a), a),
        (20, 2, alphaclops.X(b), b),
        (2, 2, alphaclops.H(b), b),
        (-3, 1, alphaclops.H(a), a),
    ]

    for given_index, actual_index, operation, qubit in op_tree_list:
        c.insert(given_index, operation, alphaclops.InsertStrategy.NEW)
        assert c.operation_at(qubit, actual_index) == operation

    c.insert(1, (), alphaclops.InsertStrategy.NEW)
    assert c == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.H(a)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.H(b)]),
            alphaclops.Moment([alphaclops.X(b)]),
        ]
    )

    BAD_INSERT = alphaclops.InsertStrategy('BAD', 'Bad strategy for testing.')
    with pytest.raises(ValueError):
        c.insert(1, alphaclops.X(a), BAD_INSERT)


def test_insert_op_tree_newinline():
    a = alphaclops.NamedQubit('alice')
    b = alphaclops.NamedQubit('bob')
    c = alphaclops.Circuit()

    op_tree_list = [
        (-5, 0, [alphaclops.H(a), alphaclops.X(b)], [a, b]),
        (-15, 0, [alphaclops.CZ(a, b)], [a]),
        (15, 2, [alphaclops.H(b), alphaclops.X(a)], [b, a]),
    ]

    for given_index, actual_index, op_list, qubits in op_tree_list:
        c.insert(given_index, op_list, alphaclops.InsertStrategy.NEW_THEN_INLINE)
        for i in range(len(op_list)):
            assert c.operation_at(qubits[i], actual_index) == op_list[i]

    c2 = alphaclops.Circuit()
    c2.insert(
        0,
        [alphaclops.CZ(a, b), alphaclops.H(a), alphaclops.X(b), alphaclops.H(b), alphaclops.X(a)],
        alphaclops.InsertStrategy.NEW_THEN_INLINE,
    )
    assert c == c2


def test_insert_op_tree_inline():
    a = alphaclops.NamedQubit('alice')
    b = alphaclops.NamedQubit('bob')
    c = alphaclops.Circuit([alphaclops.Moment([alphaclops.H(a)])])

    op_tree_list = [
        (1, 1, [alphaclops.H(a), alphaclops.X(b)], [a, b]),
        (0, 0, [alphaclops.X(b)], [b]),
        (4, 3, [alphaclops.H(b)], [b]),
        (5, 3, [alphaclops.H(a)], [a]),
        (-2, 0, [alphaclops.X(b)], [b]),
        (-5, 0, [alphaclops.CZ(a, b)], [a]),
    ]

    for given_index, actual_index, op_list, qubits in op_tree_list:
        c.insert(given_index, op_list, alphaclops.InsertStrategy.INLINE)
        for i in range(len(op_list)):
            assert c.operation_at(qubits[i], actual_index) == op_list[i]


def test_insert_op_tree_earliest():
    a = alphaclops.NamedQubit('alice')
    b = alphaclops.NamedQubit('bob')
    c = alphaclops.Circuit([alphaclops.Moment([alphaclops.H(a)])])

    op_tree_list = [
        (5, [1, 0], [alphaclops.X(a), alphaclops.X(b)], [a, b]),
        (1, [1], [alphaclops.H(b)], [b]),
        (-4, [0], [alphaclops.X(b)], [b]),
    ]

    for given_index, actual_index, op_list, qubits in op_tree_list:
        c.insert(given_index, op_list, alphaclops.InsertStrategy.EARLIEST)
        for i in range(len(op_list)):
            assert c.operation_at(qubits[i], actual_index[i]) == op_list[i]


def test_insert_moment():
    a = alphaclops.NamedQubit('alice')
    b = alphaclops.NamedQubit('bob')
    c = alphaclops.Circuit()

    moment_list = [
        (-10, 0, [alphaclops.CZ(a, b)], a, alphaclops.InsertStrategy.NEW_THEN_INLINE),
        (-20, 0, [alphaclops.X(a)], a, alphaclops.InsertStrategy.NEW),
        (20, 2, [alphaclops.X(b)], b, alphaclops.InsertStrategy.INLINE),
        (2, 2, [alphaclops.H(b)], b, alphaclops.InsertStrategy.EARLIEST),
        (-3, 1, [alphaclops.H(a)], a, alphaclops.InsertStrategy.EARLIEST),
    ]

    for given_index, actual_index, operation, qubit, strat in moment_list:
        c.insert(given_index, alphaclops.Moment(operation), strat)
        assert c.operation_at(qubit, actual_index) == operation[0]


def test_circuit_length_inference():
    # tests that `get_earliest_accommodating_moment_index` properly computes circuit length
    circuit = alphaclops.Circuit(alphaclops.X(alphaclops.q(0)))
    qubit_indices = {alphaclops.q(0): 0}
    mkey_indices = {}
    ckey_indices = {}
    assert circuits.circuit.get_earliest_accommodating_moment_index(
        alphaclops.Moment(), qubit_indices, mkey_indices, ckey_indices
    ) == len(circuit)


def test_insert_inline_near_start():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    c = alphaclops.Circuit([alphaclops.Moment(), alphaclops.Moment()])

    c.insert(1, alphaclops.X(a), strategy=alphaclops.InsertStrategy.INLINE)
    assert c == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment()])

    c.insert(1, alphaclops.Y(a), strategy=alphaclops.InsertStrategy.INLINE)
    assert c == alphaclops.Circuit([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.Y(a)]), alphaclops.Moment()])

    c.insert(0, alphaclops.Z(b), strategy=alphaclops.InsertStrategy.INLINE)
    assert c == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.Z(b)]),
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.Y(a)]),
            alphaclops.Moment(),
        ]
    )


def test_insert_at_frontier_init():
    x = alphaclops.NamedQubit('x')
    op = alphaclops.X(x)
    circuit = alphaclops.Circuit(op)
    actual_frontier = circuit.insert_at_frontier(op, 3)
    expected_circuit = alphaclops.Circuit(
        [alphaclops.Moment([op]), alphaclops.Moment(), alphaclops.Moment(), alphaclops.Moment([op])]
    )
    assert circuit == expected_circuit
    expected_frontier = defaultdict(lambda: 0)
    expected_frontier[x] = 4
    assert actual_frontier == expected_frontier

    with pytest.raises(ValueError):
        circuit = alphaclops.Circuit([alphaclops.Moment(), alphaclops.Moment([op])])
        frontier = {x: 2}
        circuit.insert_at_frontier(op, 0, frontier)


def test_insert_at_frontier():
    class Replacer(alphaclops.PointOptimizer):
        def __init__(self, replacer=(lambda x: x)):
            super().__init__()
            self.replacer = replacer

        def optimization_at(
            self, circuit: 'alphaclops.Circuit', index: int, op: 'alphaclops.Operation'
        ) -> Optional['alphaclops.PointOptimizationSummary']:
            new_ops = self.replacer(op)
            return alphaclops.PointOptimizationSummary(
                clear_span=1, clear_qubits=op.qubits, new_operations=new_ops
            )

    replacer = lambda op: ((alphaclops.Z(op.qubits[0]),) * 2 + (op, alphaclops.Y(op.qubits[0])))
    prepend_two_Xs_append_one_Y = Replacer(replacer)
    qubits = [alphaclops.NamedQubit(s) for s in 'abcdef']
    a, b, c = qubits[:3]

    circuit = alphaclops.Circuit(
        [alphaclops.Moment([alphaclops.CZ(a, b)]), alphaclops.Moment([alphaclops.CZ(b, c)]), alphaclops.Moment([alphaclops.CZ(a, b)])]
    )

    prepend_two_Xs_append_one_Y.optimize_circuit(circuit)

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a: ───Z───Z───@───Y───────────────Z───Z───@───Y───
              │                           │
b: ───────────@───Z───Z───@───Y───────────@───────
                          │
c: ───────────────────────@───────────────────────
""",
    )

    prepender = lambda op: (alphaclops.X(op.qubits[0]),) * 3 + (op,)
    prepend_3_Xs = Replacer(prepender)
    circuit = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.CNOT(a, b)]),
            alphaclops.Moment([alphaclops.CNOT(b, c)]),
            alphaclops.Moment([alphaclops.CNOT(c, b)]),
        ]
    )
    prepend_3_Xs.optimize_circuit(circuit)
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a: ───X───X───X───@───────────────────────────────────
                  │
b: ───────────────X───X───X───X───@───────────────X───
                                  │               │
c: ───────────────────────────────X───X───X───X───@───
""",
    )

    duplicate = Replacer(lambda op: (op,) * 2)
    circuit = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.CZ(qubits[j], qubits[j + 1]) for j in range(i % 2, 5, 2)])
            for i in range(4)
        ]
    )

    duplicate.optimize_circuit(circuit)
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a: ───@───@───────────@───@───────────
      │   │           │   │
b: ───@───@───@───@───@───@───@───@───
              │   │           │   │
c: ───@───@───@───@───@───@───@───@───
      │   │           │   │
d: ───@───@───@───@───@───@───@───@───
              │   │           │   │
e: ───@───@───@───@───@───@───@───@───
      │   │           │   │
f: ───@───@───────────@───@───────────
""",
    )

    circuit = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.CZ(*qubits[2:4]), alphaclops.CNOT(*qubits[:2])]),
            alphaclops.Moment([alphaclops.CNOT(*qubits[1::-1])]),
        ]
    )

    duplicate.optimize_circuit(circuit)
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
a: ───@───@───X───X───
      │   │   │   │
b: ───X───X───@───@───

c: ───@───────@───────
      │       │
d: ───@───────@───────
""",
    )


def test_insert_into_range():
    x = alphaclops.NamedQubit('x')
    y = alphaclops.NamedQubit('y')
    c = alphaclops.Circuit([alphaclops.Moment([alphaclops.X(x)])] * 4)
    c.insert_into_range([alphaclops.Z(x), alphaclops.CZ(x, y)], 2, 2)
    alphaclops.testing.assert_has_diagram(
        c,
        """
x: ───X───X───Z───@───X───X───
                  │
y: ───────────────@───────────
""",
    )

    c.insert_into_range([alphaclops.Y(y), alphaclops.Y(y), alphaclops.Y(y), alphaclops.CX(y, x)], 1, 4)
    alphaclops.testing.assert_has_diagram(
        c,
        """
x: ───X───X───Z───@───X───X───X───
                  │       │
y: ───────Y───Y───@───Y───@───────
""",
    )

    c.insert_into_range([alphaclops.H(y), alphaclops.H(y)], 6, 7)
    alphaclops.testing.assert_has_diagram(
        c,
        """
x: ───X───X───Z───@───X───X───X───────
                  │       │
y: ───────Y───Y───@───Y───@───H───H───
""",
    )

    c.insert_into_range([alphaclops.T(y)], 0, 1)
    alphaclops.testing.assert_has_diagram(
        c,
        """
x: ───X───X───Z───@───X───X───X───────
                  │       │
y: ───T───Y───Y───@───Y───@───H───H───
""",
    )

    with pytest.raises(IndexError):
        c.insert_into_range([alphaclops.CZ(x, y)], 10, 10)


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_next_moment_operating_on(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    c = circuit_cls()
    assert c.next_moment_operating_on([a]) is None
    assert c.next_moment_operating_on([a], 0) is None
    assert c.next_moment_operating_on([a], 102) is None

    c = circuit_cls([alphaclops.Moment([alphaclops.X(a)])])
    assert c.next_moment_operating_on([a]) == 0
    assert c.next_moment_operating_on([a], 0) == 0
    assert c.next_moment_operating_on([a, b]) == 0
    assert c.next_moment_operating_on([a], 1) is None
    assert c.next_moment_operating_on([b]) is None

    c = circuit_cls(
        [alphaclops.Moment(), alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment(), alphaclops.Moment([alphaclops.CZ(a, b)])]
    )

    assert c.next_moment_operating_on([a], 0) == 1
    assert c.next_moment_operating_on([a], 1) == 1
    assert c.next_moment_operating_on([a], 2) == 3
    assert c.next_moment_operating_on([a], 3) == 3
    assert c.next_moment_operating_on([a], 4) is None

    assert c.next_moment_operating_on([b], 0) == 3
    assert c.next_moment_operating_on([b], 1) == 3
    assert c.next_moment_operating_on([b], 2) == 3
    assert c.next_moment_operating_on([b], 3) == 3
    assert c.next_moment_operating_on([b], 4) is None

    assert c.next_moment_operating_on([a, b], 0) == 1
    assert c.next_moment_operating_on([a, b], 1) == 1
    assert c.next_moment_operating_on([a, b], 2) == 3
    assert c.next_moment_operating_on([a, b], 3) == 3
    assert c.next_moment_operating_on([a, b], 4) is None


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_next_moment_operating_on_distance(circuit_cls):
    a = alphaclops.NamedQubit('a')

    c = circuit_cls(
        [
            alphaclops.Moment(),
            alphaclops.Moment(),
            alphaclops.Moment(),
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment(),
        ]
    )

    assert c.next_moment_operating_on([a], 0, max_distance=4) is None
    assert c.next_moment_operating_on([a], 1, max_distance=3) is None
    assert c.next_moment_operating_on([a], 2, max_distance=2) is None
    assert c.next_moment_operating_on([a], 3, max_distance=1) is None
    assert c.next_moment_operating_on([a], 4, max_distance=0) is None

    assert c.next_moment_operating_on([a], 0, max_distance=5) == 4
    assert c.next_moment_operating_on([a], 1, max_distance=4) == 4
    assert c.next_moment_operating_on([a], 2, max_distance=3) == 4
    assert c.next_moment_operating_on([a], 3, max_distance=2) == 4
    assert c.next_moment_operating_on([a], 4, max_distance=1) == 4

    assert c.next_moment_operating_on([a], 5, max_distance=0) is None
    assert c.next_moment_operating_on([a], 1, max_distance=5) == 4
    assert c.next_moment_operating_on([a], 3, max_distance=5) == 4
    assert c.next_moment_operating_on([a], 1, max_distance=500) == 4

    # Huge max distances should be handled quickly due to capping.
    assert c.next_moment_operating_on([a], 5, max_distance=10**100) is None

    with pytest.raises(ValueError, match='Negative max_distance'):
        c.next_moment_operating_on([a], 0, max_distance=-1)


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_prev_moment_operating_on(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    c = circuit_cls()
    assert c.prev_moment_operating_on([a]) is None
    assert c.prev_moment_operating_on([a], 0) is None
    assert c.prev_moment_operating_on([a], 102) is None

    c = circuit_cls([alphaclops.Moment([alphaclops.X(a)])])
    assert c.prev_moment_operating_on([a]) == 0
    assert c.prev_moment_operating_on([a], 1) == 0
    assert c.prev_moment_operating_on([a, b]) == 0
    assert c.prev_moment_operating_on([a], 0) is None
    assert c.prev_moment_operating_on([b]) is None

    c = circuit_cls(
        [alphaclops.Moment([alphaclops.CZ(a, b)]), alphaclops.Moment(), alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment()]
    )

    assert c.prev_moment_operating_on([a], 4) == 2
    assert c.prev_moment_operating_on([a], 3) == 2
    assert c.prev_moment_operating_on([a], 2) == 0
    assert c.prev_moment_operating_on([a], 1) == 0
    assert c.prev_moment_operating_on([a], 0) is None

    assert c.prev_moment_operating_on([b], 4) == 0
    assert c.prev_moment_operating_on([b], 3) == 0
    assert c.prev_moment_operating_on([b], 2) == 0
    assert c.prev_moment_operating_on([b], 1) == 0
    assert c.prev_moment_operating_on([b], 0) is None

    assert c.prev_moment_operating_on([a, b], 4) == 2
    assert c.prev_moment_operating_on([a, b], 3) == 2
    assert c.prev_moment_operating_on([a, b], 2) == 0
    assert c.prev_moment_operating_on([a, b], 1) == 0
    assert c.prev_moment_operating_on([a, b], 0) is None

    with pytest.raises(ValueError, match='Negative max_distance'):
        assert c.prev_moment_operating_on([a, b], 4, max_distance=-1)


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_prev_moment_operating_on_distance(circuit_cls):
    a = alphaclops.NamedQubit('a')

    c = circuit_cls(
        [
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment(),
            alphaclops.Moment(),
            alphaclops.Moment(),
            alphaclops.Moment(),
        ]
    )

    assert c.prev_moment_operating_on([a], max_distance=4) is None
    assert c.prev_moment_operating_on([a], 6, max_distance=4) is None
    assert c.prev_moment_operating_on([a], 5, max_distance=3) is None
    assert c.prev_moment_operating_on([a], 4, max_distance=2) is None
    assert c.prev_moment_operating_on([a], 3, max_distance=1) is None
    assert c.prev_moment_operating_on([a], 2, max_distance=0) is None
    assert c.prev_moment_operating_on([a], 1, max_distance=0) is None
    assert c.prev_moment_operating_on([a], 0, max_distance=0) is None

    assert c.prev_moment_operating_on([a], 6, max_distance=5) == 1
    assert c.prev_moment_operating_on([a], 5, max_distance=4) == 1
    assert c.prev_moment_operating_on([a], 4, max_distance=3) == 1
    assert c.prev_moment_operating_on([a], 3, max_distance=2) == 1
    assert c.prev_moment_operating_on([a], 2, max_distance=1) == 1

    assert c.prev_moment_operating_on([a], 6, max_distance=10) == 1
    assert c.prev_moment_operating_on([a], 6, max_distance=100) == 1
    assert c.prev_moment_operating_on([a], 13, max_distance=500) == 1

    # Huge max distances should be handled quickly due to capping.
    assert c.prev_moment_operating_on([a], 1, max_distance=10**100) is None

    with pytest.raises(ValueError, match='Negative max_distance'):
        c.prev_moment_operating_on([a], 6, max_distance=-1)


def test_earliest_available_moment():
    q = alphaclops.LineQubit.range(3)
    c = alphaclops.Circuit(
        alphaclops.Moment(alphaclops.measure(q[0], key="m")),
        alphaclops.Moment(alphaclops.X(q[1]).with_classical_controls("m")),
    )
    assert c.earliest_available_moment(alphaclops.Y(q[0])) == 1
    assert c.earliest_available_moment(alphaclops.Y(q[1])) == 2
    assert c.earliest_available_moment(alphaclops.Y(q[2])) == 0
    assert c.earliest_available_moment(alphaclops.Y(q[2]).with_classical_controls("m")) == 1
    assert (
        c.earliest_available_moment(alphaclops.Y(q[2]).with_classical_controls("m"), end_moment_index=1)
        == 1
    )

    # Returns `end_moment_index` by default without verifying if an operation already exists there.
    assert (
        c.earliest_available_moment(alphaclops.Y(q[1]).with_classical_controls("m"), end_moment_index=1)
        == 1
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_operation_at(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    c = circuit_cls()
    assert c.operation_at(a, 0) is None
    assert c.operation_at(a, -1) is None
    assert c.operation_at(a, 102) is None

    c = circuit_cls([alphaclops.Moment()])
    assert c.operation_at(a, 0) is None

    c = circuit_cls([alphaclops.Moment([alphaclops.X(a)])])
    assert c.operation_at(b, 0) is None
    assert c.operation_at(a, 1) is None
    assert c.operation_at(a, 0) == alphaclops.X(a)

    c = circuit_cls([alphaclops.Moment(), alphaclops.Moment([alphaclops.CZ(a, b)])])
    assert c.operation_at(a, 0) is None
    assert c.operation_at(a, 1) == alphaclops.CZ(a, b)


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_findall_operations(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    xa = alphaclops.X.on(a)
    xb = alphaclops.X.on(b)
    za = alphaclops.Z.on(a)
    zb = alphaclops.Z.on(b)

    def is_x(op: alphaclops.Operation) -> bool:
        return isinstance(op, alphaclops.GateOperation) and isinstance(op.gate, alphaclops.XPowGate)

    c = circuit_cls()
    assert list(c.findall_operations(is_x)) == []

    c = circuit_cls(xa)
    assert list(c.findall_operations(is_x)) == [(0, xa)]

    c = circuit_cls(za)
    assert list(c.findall_operations(is_x)) == []

    c = circuit_cls([za, zb] * 8)
    assert list(c.findall_operations(is_x)) == []

    c = circuit_cls(xa, xb)
    assert list(c.findall_operations(is_x)) == [(0, xa), (0, xb)]

    c = circuit_cls(xa, zb)
    assert list(c.findall_operations(is_x)) == [(0, xa)]

    c = circuit_cls(xa, za)
    assert list(c.findall_operations(is_x)) == [(0, xa)]

    c = circuit_cls([xa] * 8)
    assert list(c.findall_operations(is_x)) == list(enumerate([xa] * 8))

    c = circuit_cls(za, zb, xa, xb)
    assert list(c.findall_operations(is_x)) == [(1, xa), (1, xb)]

    c = circuit_cls(xa, zb, za, xb)
    assert list(c.findall_operations(is_x)) == [(0, xa), (1, xb)]


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_findall_operations_with_gate(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = circuit_cls(
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.Z(a), alphaclops.Z(b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.measure(a), alphaclops.measure(b)]),
        ]
    )
    assert list(c.findall_operations_with_gate_type(alphaclops.XPowGate)) == [
        (0, alphaclops.X(a), alphaclops.X),
        (2, alphaclops.X(a), alphaclops.X),
        (2, alphaclops.X(b), alphaclops.X),
    ]
    assert list(c.findall_operations_with_gate_type(alphaclops.CZPowGate)) == [
        (3, alphaclops.CZ(a, b), alphaclops.CZ)
    ]
    assert list(c.findall_operations_with_gate_type(alphaclops.MeasurementGate)) == [
        (4, alphaclops.MeasurementGate(1, key='a').on(a), alphaclops.MeasurementGate(1, key='a')),
        (4, alphaclops.MeasurementGate(1, key='b').on(b), alphaclops.MeasurementGate(1, key='b')),
    ]


def assert_findall_operations_until_blocked_as_expected(
    circuit=None, start_frontier=None, is_blocker=None, expected_ops=None
):
    if circuit is None:
        circuit = alphaclops.Circuit()
    if start_frontier is None:
        start_frontier = {}
    kwargs = {} if is_blocker is None else {'is_blocker': is_blocker}
    found_ops = circuit.findall_operations_until_blocked(start_frontier, **kwargs)

    for i, op in found_ops:
        assert i >= min((start_frontier[q] for q in op.qubits if q in start_frontier), default=0)
        assert set(op.qubits).intersection(start_frontier)

    if expected_ops is None:
        return
    assert sorted(found_ops) == sorted(expected_ops)


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_findall_operations_until_blocked(circuit_cls):
    a, b, c, d = alphaclops.LineQubit.range(4)

    assert_findall_operations_until_blocked_as_expected()

    circuit = circuit_cls(
        alphaclops.H(a),
        alphaclops.CZ(a, b),
        alphaclops.H(b),
        alphaclops.CZ(b, c),
        alphaclops.H(c),
        alphaclops.CZ(c, d),
        alphaclops.H(d),
        alphaclops.CZ(c, d),
        alphaclops.H(c),
        alphaclops.CZ(b, c),
        alphaclops.H(b),
        alphaclops.CZ(a, b),
        alphaclops.H(a),
    )
    expected_diagram = """
0: ───H───@───────────────────────────────────────@───H───
          │                                       │
1: ───────@───H───@───────────────────────@───H───@───────
                  │                       │
2: ───────────────@───H───@───────@───H───@───────────────
                          │       │
3: ───────────────────────@───H───@───────────────────────
""".strip()
    #     0   1   2   3   4   5   6   7   8   9   10  11  12
    alphaclops.testing.assert_has_diagram(circuit, expected_diagram)

    # Always return true to test basic features
    go_to_end = lambda op: False
    stop_if_op = lambda op: True
    stop_if_h_on_a = lambda op: op.gate == alphaclops.H and a in op.qubits

    # Empty cases.
    assert_findall_operations_until_blocked_as_expected(is_blocker=go_to_end, expected_ops=[])
    assert_findall_operations_until_blocked_as_expected(
        circuit=circuit, is_blocker=go_to_end, expected_ops=[]
    )

    # Clamped input cases. (out of bounds)
    assert_findall_operations_until_blocked_as_expected(
        start_frontier={a: 5}, is_blocker=stop_if_op, expected_ops=[]
    )
    assert_findall_operations_until_blocked_as_expected(
        start_frontier={a: -100}, is_blocker=stop_if_op, expected_ops=[]
    )
    assert_findall_operations_until_blocked_as_expected(
        circuit=circuit, start_frontier={a: 100}, is_blocker=stop_if_op, expected_ops=[]
    )

    # Test if all operations are blocked
    for idx in range(15):
        for q in (a, b, c, d):
            assert_findall_operations_until_blocked_as_expected(
                circuit=circuit, start_frontier={q: idx}, is_blocker=stop_if_op, expected_ops=[]
            )
        assert_findall_operations_until_blocked_as_expected(
            circuit=circuit,
            start_frontier={a: idx, b: idx, c: idx, d: idx},
            is_blocker=stop_if_op,
            expected_ops=[],
        )

    # Cases where nothing is blocked, it goes to the end
    a_ending_ops = [(11, alphaclops.CZ.on(a, b)), (12, alphaclops.H.on(a))]
    for idx in range(2, 10):
        assert_findall_operations_until_blocked_as_expected(
            circuit=circuit,
            start_frontier={a: idx},
            is_blocker=go_to_end,
            expected_ops=a_ending_ops,
        )

    # Block on H, but pick up the CZ
    for idx in range(2, 10):
        assert_findall_operations_until_blocked_as_expected(
            circuit=circuit,
            start_frontier={a: idx},
            is_blocker=stop_if_h_on_a,
            expected_ops=[(11, alphaclops.CZ.on(a, b))],
        )

    circuit = circuit_cls([alphaclops.CZ(a, b), alphaclops.CZ(a, b), alphaclops.CZ(b, c)])
    expected_diagram = """
0: ───@───@───────
      │   │
1: ───@───@───@───
              │
2: ───────────@───
""".strip()
    #     0   1   2
    alphaclops.testing.assert_has_diagram(circuit, expected_diagram)

    start_frontier = {a: 0, b: 0}
    is_blocker = lambda next_op: sorted(next_op.qubits) != [a, b]
    expected_ops = [(0, alphaclops.CZ(a, b)), (1, alphaclops.CZ(a, b))]
    assert_findall_operations_until_blocked_as_expected(
        circuit=circuit,
        start_frontier=start_frontier,
        is_blocker=is_blocker,
        expected_ops=expected_ops,
    )

    circuit = circuit_cls([alphaclops.ZZ(a, b), alphaclops.ZZ(b, c)])
    expected_diagram = """
0: ───ZZ────────
      │
1: ───ZZ───ZZ───
           │
2: ────────ZZ───
""".strip()
    #     0    1
    alphaclops.testing.assert_has_diagram(circuit, expected_diagram)

    start_frontier = {a: 0, b: 0, c: 0}
    is_blocker = lambda op: a in op.qubits
    assert_findall_operations_until_blocked_as_expected(
        circuit=circuit, start_frontier=start_frontier, is_blocker=is_blocker, expected_ops=[]
    )

    circuit = circuit_cls([alphaclops.ZZ(a, b), alphaclops.XX(c, d), alphaclops.ZZ(b, c), alphaclops.Z(b)])
    expected_diagram = """
0: ───ZZ────────────
      │
1: ───ZZ───ZZ───Z───
           │
2: ───XX───ZZ───────
      │
3: ───XX────────────
""".strip()
    #     0    1    2
    alphaclops.testing.assert_has_diagram(circuit, expected_diagram)

    start_frontier = {a: 0, b: 0, c: 0, d: 0}
    is_blocker = lambda op: isinstance(op.gate, alphaclops.XXPowGate)
    assert_findall_operations_until_blocked_as_expected(
        circuit=circuit,
        start_frontier=start_frontier,
        is_blocker=is_blocker,
        expected_ops=[(0, alphaclops.ZZ(a, b))],
    )

    circuit = circuit_cls([alphaclops.XX(a, b), alphaclops.Z(a), alphaclops.ZZ(b, c), alphaclops.ZZ(c, d), alphaclops.Z(d)])
    expected_diagram = """
0: ───XX───Z─────────────
      │
1: ───XX───ZZ────────────
           │
2: ────────ZZ───ZZ───────
                │
3: ─────────────ZZ───Z───
""".strip()
    #     0    1    2    3
    alphaclops.testing.assert_has_diagram(circuit, expected_diagram)

    start_frontier = {a: 0, d: 0}
    assert_findall_operations_until_blocked_as_expected(
        circuit=circuit, start_frontier=start_frontier, is_blocker=is_blocker, expected_ops=[]
    )


@pytest.mark.parametrize('seed', [randint(0, 2**31)])
@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_findall_operations_until_blocked_docstring_examples(seed, circuit_cls):
    prng = np.random.RandomState(seed)

    class ExampleGate(alphaclops.Gate):
        def __init__(self, n_qubits, label):
            self.n_qubits = n_qubits
            self.label = label

        def num_qubits(self):
            return self.n_qubits

        def _circuit_diagram_info_(self, args):
            return alphaclops.CircuitDiagramInfo(wire_symbols=[self.label] * self.n_qubits)

    def is_blocker(op):
        if op.gate.label == 'F':
            return False
        if op.gate.label == 'T':
            return True
        return prng.rand() < 0.5

    F2 = ExampleGate(2, 'F')
    T2 = ExampleGate(2, 'T')
    M2 = ExampleGate(2, 'M')
    a, b, c, d = alphaclops.LineQubit.range(4)

    circuit = circuit_cls([F2(a, b), F2(a, b), T2(b, c)])
    start = {a: 0, b: 0}
    expected_diagram = """
0: ───F───F───────
      │   │
1: ───F───F───T───
              │
2: ───────────T───
    """
    alphaclops.testing.assert_has_diagram(circuit, expected_diagram)
    expected_ops = [(0, F2(a, b)), (1, F2(a, b))]
    new_circuit = circuit_cls([op for _, op in expected_ops])
    expected_diagram = """
0: ───F───F───
      │   │
1: ───F───F───
    """
    alphaclops.testing.assert_has_diagram(new_circuit, expected_diagram)
    assert circuit.findall_operations_until_blocked(start, is_blocker) == expected_ops

    circuit = circuit_cls([M2(a, b), M2(b, c), F2(a, b), M2(c, d)])
    start = {a: 2, b: 2}
    expected_diagram = """
0: ───M───────F───
      │       │
1: ───M───M───F───
          │
2: ───────M───M───
              │
3: ───────────M───
    """
    alphaclops.testing.assert_has_diagram(circuit, expected_diagram)
    expected_ops = [(2, F2(a, b))]
    new_circuit = circuit_cls([op for _, op in expected_ops])
    expected_diagram = """
0: ───F───
      │
1: ───F───
    """
    alphaclops.testing.assert_has_diagram(new_circuit, expected_diagram)
    assert circuit.findall_operations_until_blocked(start, is_blocker) == expected_ops

    circuit = circuit_cls([M2(a, b), T2(b, c), M2(a, b), M2(c, d)])
    start = {a: 1, b: 1}
    expected_diagram = """
0: ───M───────M───
      │       │
1: ───M───T───M───
          │
2: ───────T───M───
              │
3: ───────────M───
    """
    alphaclops.testing.assert_has_diagram(circuit, expected_diagram)
    assert circuit.findall_operations_until_blocked(start, is_blocker) == []

    ops = [(0, F2(a, b)), (1, F2(a, b))]
    circuit = circuit_cls([op for _, op in ops])
    start = {a: 0, b: 1}
    expected_diagram = """
0: ───F───F───
      │   │
1: ───F───F───
    """
    alphaclops.testing.assert_has_diagram(circuit, expected_diagram)
    assert circuit.findall_operations_until_blocked(start, is_blocker) == ops

    ops = [F2(a, b), F2(b, c), F2(c, d)]
    circuit = circuit_cls(ops)
    start = {a: 0, d: 0}
    expected_diagram = """
0: ───F───────────
      │
1: ───F───F───────
          │
2: ───────F───F───
              │
3: ───────────F───
    """
    alphaclops.testing.assert_has_diagram(circuit, expected_diagram)
    assert circuit.findall_operations_until_blocked(start, is_blocker) == [
        (0, F2(a, b)),
        (2, F2(c, d)),
    ]


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_has_measurements(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    xa = alphaclops.X.on(a)
    xb = alphaclops.X.on(b)

    ma = alphaclops.measure(a)
    mb = alphaclops.measure(b)

    c = circuit_cls()
    assert not c.has_measurements()

    c = circuit_cls(xa, xb)
    assert not c.has_measurements()

    c = circuit_cls(ma)
    assert c.has_measurements()

    c = circuit_cls(ma, mb)
    assert c.has_measurements()

    c = circuit_cls(xa, ma)
    assert c.has_measurements()

    c = circuit_cls(xa, ma, xb, mb)
    assert c.has_measurements()

    c = circuit_cls(ma, xa)
    assert c.has_measurements()

    c = circuit_cls(ma, xa, mb)
    assert c.has_measurements()

    c = circuit_cls(xa, ma, xb, xa)
    assert c.has_measurements()

    c = circuit_cls(ma, ma)
    assert c.has_measurements()

    c = circuit_cls(xa, ma, xa)
    assert c.has_measurements()


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_are_all_or_any_measurements_terminal(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    xa = alphaclops.X.on(a)
    xb = alphaclops.X.on(b)

    ma = alphaclops.measure(a)
    mb = alphaclops.measure(b)

    c = circuit_cls()
    assert c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()

    c = circuit_cls(xa, xb)
    assert c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()

    c = circuit_cls(ma)
    assert c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = circuit_cls(ma, mb)
    assert c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = circuit_cls(xa, ma)
    assert c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = circuit_cls(xa, ma, xb, mb)
    assert c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = circuit_cls(ma, xa)
    assert not c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()

    c = circuit_cls(ma, xa, mb)
    assert not c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = circuit_cls(xa, ma, xb, xa)
    assert not c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()

    c = circuit_cls(ma, ma)
    assert not c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = circuit_cls(xa, ma, xa)
    assert not c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_all_or_any_terminal(circuit_cls):
    def is_x_pow_gate(op):
        return isinstance(op.gate, alphaclops.XPowGate)

    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    xa = alphaclops.X.on(a)
    xb = alphaclops.X.on(b)

    ya = alphaclops.Y.on(a)
    yb = alphaclops.Y.on(b)

    c = circuit_cls()
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert not c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(xa)
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(xb)
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(ya)
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert not c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(ya, yb)
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert not c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(ya, yb, xa)
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(ya, yb, xa, xb)
    assert c.are_all_matches_terminal(is_x_pow_gate)
    assert c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(xa, xa)
    assert not c.are_all_matches_terminal(is_x_pow_gate)
    assert c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(xa, ya)
    assert not c.are_all_matches_terminal(is_x_pow_gate)
    assert not c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(xb, ya, yb)
    assert not c.are_all_matches_terminal(is_x_pow_gate)
    assert not c.are_any_matches_terminal(is_x_pow_gate)

    c = circuit_cls(xa, ya, xa)
    assert not c.are_all_matches_terminal(is_x_pow_gate)
    assert c.are_any_matches_terminal(is_x_pow_gate)

    def is_circuit_op(op):
        isinstance(op, alphaclops.CircuitOperation)

    cop_1 = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(xa, ya))
    cop_2 = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(cop_1, xb))
    c = circuit_cls(cop_2, yb)
    # are_all_matches_terminal treats CircuitOperations as transparent.
    assert c.are_all_matches_terminal(is_circuit_op)
    assert not c.are_any_matches_terminal(is_circuit_op)


def test_clear_operations_touching():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    c = alphaclops.Circuit()
    c.clear_operations_touching([a, b], range(10))
    assert c == alphaclops.Circuit()

    c = alphaclops.Circuit(
        [
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.X(b)]),
            alphaclops.Moment(),
        ]
    )
    c.clear_operations_touching([a], [1, 3, 4, 6, 7])
    assert c == alphaclops.Circuit(
        [
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.X(b)]),
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment(),
            alphaclops.Moment(),
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.X(b)]),
            alphaclops.Moment(),
        ]
    )

    c = alphaclops.Circuit(
        [
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.X(b)]),
            alphaclops.Moment(),
        ]
    )
    c.clear_operations_touching([a, b], [1, 3, 4, 6, 7])
    assert c == alphaclops.Circuit(
        [
            alphaclops.Moment(),
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment(),
            alphaclops.Moment(),
            alphaclops.Moment(),
            alphaclops.Moment(),
            alphaclops.Moment(),
        ]
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_all_qubits(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    c = circuit_cls([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(b)])])
    assert c.all_qubits() == {a, b}

    c = circuit_cls([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(a)])])
    assert c.all_qubits() == {a}

    c = circuit_cls([alphaclops.Moment([alphaclops.CZ(a, b)])])
    assert c.all_qubits() == {a, b}

    c = circuit_cls([alphaclops.Moment([alphaclops.CZ(a, b)]), alphaclops.Moment([alphaclops.X(a)])])
    assert c.all_qubits() == {a, b}


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_all_operations(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    c = circuit_cls([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(b)])])
    assert list(c.all_operations()) == [alphaclops.X(a), alphaclops.X(b)]

    c = circuit_cls([alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)])])
    assert list(c.all_operations()) == [alphaclops.X(a), alphaclops.X(b)]

    c = circuit_cls([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(a)])])
    assert list(c.all_operations()) == [alphaclops.X(a), alphaclops.X(a)]

    c = circuit_cls([alphaclops.Moment([alphaclops.CZ(a, b)])])
    assert list(c.all_operations()) == [alphaclops.CZ(a, b)]

    c = circuit_cls([alphaclops.Moment([alphaclops.CZ(a, b)]), alphaclops.Moment([alphaclops.X(a)])])
    assert list(c.all_operations()) == [alphaclops.CZ(a, b), alphaclops.X(a)]

    c = circuit_cls(
        [
            alphaclops.Moment([]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.Y(b)]),
            alphaclops.Moment([]),
            alphaclops.Moment([alphaclops.CNOT(a, b)]),
            alphaclops.Moment([alphaclops.Z(b), alphaclops.H(a)]),  # Different qubit order
            alphaclops.Moment([]),
        ]
    )

    assert list(c.all_operations()) == [alphaclops.X(a), alphaclops.Y(b), alphaclops.CNOT(a, b), alphaclops.Z(b), alphaclops.H(a)]


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_qid_shape_qubit(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')

    circuit = circuit_cls([alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(b)])])

    assert alphaclops.qid_shape(circuit) == (2, 2)
    assert alphaclops.num_qubits(circuit) == 2
    assert circuit.qid_shape() == (2, 2)
    assert circuit.qid_shape(qubit_order=[c, a, b]) == (2, 2, 2)
    with pytest.raises(ValueError, match='extra qubits'):
        _ = circuit.qid_shape(qubit_order=[a])


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_qid_shape_qudit(circuit_cls):
    class PlusOneMod3Gate(alphaclops.testing.SingleQubitGate):
        def _qid_shape_(self):
            return (3,)

    class C2NotGate(alphaclops.Gate):
        def _qid_shape_(self):
            return (3, 2)

    class IdentityGate(alphaclops.testing.SingleQubitGate):
        def _qid_shape_(self):
            return (1,)

    a, b, c = alphaclops.LineQid.for_qid_shape((3, 2, 1))

    circuit = circuit_cls(PlusOneMod3Gate().on(a), C2NotGate().on(a, b), IdentityGate().on_each(c))

    assert alphaclops.num_qubits(circuit) == 3
    assert alphaclops.qid_shape(circuit) == (3, 2, 1)
    assert circuit.qid_shape() == (3, 2, 1)
    assert circuit.qid_shape()
    with pytest.raises(ValueError, match='extra qubits'):
        _ = circuit.qid_shape(qubit_order=[b, c])


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_to_text_diagram_teleportation_to_diagram(circuit_cls):
    ali = alphaclops.NamedQubit('(0, 0)')
    bob = alphaclops.NamedQubit('(0, 1)')
    msg = alphaclops.NamedQubit('(1, 0)')
    tmp = alphaclops.NamedQubit('(1, 1)')

    c = circuit_cls(
        [
            alphaclops.Moment([alphaclops.H(ali)]),
            alphaclops.Moment([alphaclops.CNOT(ali, bob)]),
            alphaclops.Moment([alphaclops.X(msg) ** 0.5]),
            alphaclops.Moment([alphaclops.CNOT(msg, ali)]),
            alphaclops.Moment([alphaclops.H(msg)]),
            alphaclops.Moment([alphaclops.measure(msg), alphaclops.measure(ali)]),
            alphaclops.Moment([alphaclops.CNOT(ali, bob)]),
            alphaclops.Moment([alphaclops.CNOT(msg, tmp)]),
            alphaclops.Moment([alphaclops.CZ(bob, tmp)]),
        ]
    )

    alphaclops.testing.assert_has_diagram(
        c,
        """
(0, 0): ───H───@───────────X───────M───@───────────
               │           │           │
(0, 1): ───────X───────────┼───────────X───────@───
                           │                   │
(1, 0): ───────────X^0.5───@───H───M───────@───┼───
                                           │   │
(1, 1): ───────────────────────────────────X───@───
""",
    )

    alphaclops.testing.assert_has_diagram(
        c,
        """
(0, 0): ---H---@-----------X-------M---@-----------
               |           |           |
(0, 1): -------X-----------|-----------X-------@---
                           |                   |
(1, 0): -----------X^0.5---@---H---M-------@---|---
                                           |   |
(1, 1): -----------------------------------X---@---
""",
        use_unicode_characters=False,
    )

    alphaclops.testing.assert_has_diagram(
        c,
        """
(0, 0) (0, 1) (1, 0) (1, 1)
|      |      |      |
H      |      |      |
|      |      |      |
@------X      |      |
|      |      |      |
|      |      X^0.5  |
|      |      |      |
X-------------@      |
|      |      |      |
|      |      H      |
|      |      |      |
M      |      M      |
|      |      |      |
@------X      |      |
|      |      |      |
|      |      @------X
|      |      |      |
|      @-------------@
|      |      |      |
""",
        use_unicode_characters=False,
        transpose=True,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_diagram_with_unknown_exponent(circuit_cls):
    class WeirdGate(alphaclops.testing.SingleQubitGate):
        def _circuit_diagram_info_(
            self, args: alphaclops.CircuitDiagramInfoArgs
        ) -> alphaclops.CircuitDiagramInfo:
            return alphaclops.CircuitDiagramInfo(wire_symbols=('B',), exponent='fancy')

    class WeirderGate(alphaclops.testing.SingleQubitGate):
        def _circuit_diagram_info_(
            self, args: alphaclops.CircuitDiagramInfoArgs
        ) -> alphaclops.CircuitDiagramInfo:
            return alphaclops.CircuitDiagramInfo(wire_symbols=('W',), exponent='fancy-that')

    c = circuit_cls(WeirdGate().on(alphaclops.NamedQubit('q')), WeirderGate().on(alphaclops.NamedQubit('q')))

    # The hyphen in the exponent should cause parens to appear.
    alphaclops.testing.assert_has_diagram(c, 'q: ───B^fancy───W^(fancy-that)───')


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_circuit_diagram_on_gate_without_info(circuit_cls):
    q = alphaclops.NamedQubit('(0, 0)')
    q2 = alphaclops.NamedQubit('(0, 1)')
    q3 = alphaclops.NamedQubit('(0, 2)')

    class FGate(alphaclops.Gate):
        def __init__(self, num_qubits=1):
            self._num_qubits = num_qubits

        def num_qubits(self) -> int:
            return self._num_qubits

        def __repr__(self):
            return 'python-object-FGate:arbitrary-digits'

    # Fallback to repr.
    f = FGate()
    alphaclops.testing.assert_has_diagram(
        circuit_cls([alphaclops.Moment([f.on(q)])]),
        """
(0, 0): ---python-object-FGate:arbitrary-digits---
""",
        use_unicode_characters=False,
    )

    f3 = FGate(3)
    # When used on multiple qubits, show the qubit order as a digit suffix.
    alphaclops.testing.assert_has_diagram(
        circuit_cls([alphaclops.Moment([f3.on(q, q3, q2)])]),
        """
(0, 0): ---python-object-FGate:arbitrary-digits---
           |
(0, 1): ---#3-------------------------------------
           |
(0, 2): ---#2-------------------------------------
""",
        use_unicode_characters=False,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_to_text_diagram_multi_qubit_gate(circuit_cls):
    q1 = alphaclops.NamedQubit('(0, 0)')
    q2 = alphaclops.NamedQubit('(0, 1)')
    q3 = alphaclops.NamedQubit('(0, 2)')
    c = circuit_cls(alphaclops.measure(q1, q2, q3, key='msg'))
    alphaclops.testing.assert_has_diagram(
        c,
        """
(0, 0): ───M('msg')───
           │
(0, 1): ───M──────────
           │
(0, 2): ───M──────────
""",
    )
    alphaclops.testing.assert_has_diagram(
        c,
        """
(0, 0): ---M('msg')---
           |
(0, 1): ---M----------
           |
(0, 2): ---M----------
""",
        use_unicode_characters=False,
    )
    alphaclops.testing.assert_has_diagram(
        c,
        """
(0, 0)   (0, 1) (0, 2)
│        │      │
M('msg')─M──────M
│        │      │
""",
        transpose=True,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_to_text_diagram_many_qubits_gate_but_multiple_wire_symbols(circuit_cls):
    class BadGate(alphaclops.testing.ThreeQubitGate):
        def _circuit_diagram_info_(self, args: alphaclops.CircuitDiagramInfoArgs) -> Tuple[str, str]:
            return 'a', 'a'

    q1 = alphaclops.NamedQubit('(0, 0)')
    q2 = alphaclops.NamedQubit('(0, 1)')
    q3 = alphaclops.NamedQubit('(0, 2)')
    c = circuit_cls([alphaclops.Moment([BadGate().on(q1, q2, q3)])])
    with pytest.raises(ValueError, match='BadGate'):
        c.to_text_diagram()


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_to_text_diagram_parameterized_value(circuit_cls):
    q = alphaclops.NamedQubit('cube')

    class PGate(alphaclops.testing.SingleQubitGate):
        def __init__(self, val):
            self.val = val

        def _circuit_diagram_info_(
            self, args: alphaclops.CircuitDiagramInfoArgs
        ) -> alphaclops.CircuitDiagramInfo:
            return alphaclops.CircuitDiagramInfo(('P',), self.val)

    c = circuit_cls(
        PGate(1).on(q),
        PGate(2).on(q),
        PGate(sympy.Symbol('a')).on(q),
        PGate(sympy.Symbol('%$&#*(')).on(q),
    )
    assert str(c).strip() == 'cube: ───P───P^2───P^a───P^(%$&#*()───'


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_to_text_diagram_custom_order(circuit_cls):
    qa = alphaclops.NamedQubit('2')
    qb = alphaclops.NamedQubit('3')
    qc = alphaclops.NamedQubit('4')

    c = circuit_cls([alphaclops.Moment([alphaclops.X(qa), alphaclops.X(qb), alphaclops.X(qc)])])
    alphaclops.testing.assert_has_diagram(
        c,
        """
3: ---X---

4: ---X---

2: ---X---
""",
        qubit_order=alphaclops.QubitOrder.sorted_by(lambda e: int(str(e)) % 3),
        use_unicode_characters=False,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_overly_precise_diagram(circuit_cls):
    # Test default precision of 3
    qa = alphaclops.NamedQubit('a')
    c = circuit_cls([alphaclops.Moment([alphaclops.X(qa) ** 0.12345678])])
    alphaclops.testing.assert_has_diagram(
        c,
        """
a: ---X^0.123---
""",
        use_unicode_characters=False,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_none_precision_diagram(circuit_cls):
    # Test default precision of 3
    qa = alphaclops.NamedQubit('a')
    c = circuit_cls([alphaclops.Moment([alphaclops.X(qa) ** 0.4921875])])
    alphaclops.testing.assert_has_diagram(
        c,
        """
a: ---X^0.4921875---
""",
        use_unicode_characters=False,
        precision=None,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_diagram_custom_precision(circuit_cls):
    qa = alphaclops.NamedQubit('a')
    c = circuit_cls([alphaclops.Moment([alphaclops.X(qa) ** 0.12341234])])
    alphaclops.testing.assert_has_diagram(
        c,
        """
a: ---X^0.12341---
""",
        use_unicode_characters=False,
        precision=5,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_diagram_wgate(circuit_cls):
    qa = alphaclops.NamedQubit('a')
    test_wgate = alphaclops.PhasedXPowGate(exponent=0.12341234, phase_exponent=0.43214321)
    c = circuit_cls([alphaclops.Moment([test_wgate.on(qa)])])
    alphaclops.testing.assert_has_diagram(
        c,
        """
a: ---PhX(0.43)^(1/8)---
""",
        use_unicode_characters=False,
        precision=2,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_diagram_wgate_none_precision(circuit_cls):
    qa = alphaclops.NamedQubit('a')
    test_wgate = alphaclops.PhasedXPowGate(exponent=0.12341234, phase_exponent=0.43214321)
    c = circuit_cls([alphaclops.Moment([test_wgate.on(qa)])])
    alphaclops.testing.assert_has_diagram(
        c,
        """
a: ---PhX(0.43214321)^0.12341234---
""",
        use_unicode_characters=False,
        precision=None,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_diagram_global_phase(circuit_cls):
    qa = alphaclops.NamedQubit('a')
    global_phase = alphaclops.global_phase_operation(coefficient=1j)
    c = circuit_cls([global_phase])
    alphaclops.testing.assert_has_diagram(
        c, "\n\nglobal phase:   0.5pi", use_unicode_characters=False, precision=2
    )
    alphaclops.testing.assert_has_diagram(
        c, "\n\nglobal phase:   0.5π", use_unicode_characters=True, precision=2
    )

    c = circuit_cls([alphaclops.X(qa), global_phase, global_phase])
    alphaclops.testing.assert_has_diagram(
        c,
        """\
a: ─────────────X───

global phase:   π""",
        use_unicode_characters=True,
        precision=2,
    )
    c = circuit_cls([alphaclops.X(qa), global_phase], alphaclops.Moment([alphaclops.X(qa), global_phase]))
    alphaclops.testing.assert_has_diagram(
        c,
        """\
a: ─────────────X──────X──────

global phase:   0.5π   0.5π
""",
        use_unicode_characters=True,
        precision=2,
    )

    c = circuit_cls(
        alphaclops.X(alphaclops.LineQubit(2)),
        alphaclops.CircuitOperation(
            circuit_cls(alphaclops.global_phase_operation(-1).with_tags("tag")).freeze()
        ),
    )
    alphaclops.testing.assert_has_diagram(
        c,
        """\
2: ───X──────────

      π['tag']""",
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_has_unitary(circuit_cls):
    class NonUnitary(alphaclops.testing.SingleQubitGate):
        pass

    class EventualUnitary(alphaclops.testing.SingleQubitGate):
        def _decompose_(self, qubits):
            return alphaclops.X.on_each(*qubits)

    q = alphaclops.NamedQubit('q')

    # Non-unitary operations cause a non-unitary circuit.
    assert alphaclops.has_unitary(circuit_cls(alphaclops.X(q)))
    assert not alphaclops.has_unitary(circuit_cls(NonUnitary().on(q)))

    # Terminal measurements are ignored, though.
    assert alphaclops.has_unitary(circuit_cls(alphaclops.measure(q)))
    assert not alphaclops.has_unitary(circuit_cls(alphaclops.measure(q), alphaclops.measure(q)))

    # Still unitary if operations decompose into unitary operations.
    assert alphaclops.has_unitary(circuit_cls(EventualUnitary().on(q)))


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_text_diagram_jupyter(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')
    circuit = circuit_cls((alphaclops.CNOT(a, b), alphaclops.CNOT(b, c), alphaclops.CNOT(c, a)) * 50)
    text_expected = circuit.to_text_diagram()

    # Test Jupyter console output from
    class FakePrinter:
        def __init__(self):
            self.text_pretty = ''

        def text(self, to_print):
            self.text_pretty += to_print

    p = FakePrinter()
    circuit._repr_pretty_(p, False)
    assert p.text_pretty == text_expected

    # Test cycle handling
    p = FakePrinter()
    circuit._repr_pretty_(p, True)
    assert p.text_pretty == f'{circuit_cls.__name__}(...)'

    # Test Jupyter notebook html output
    text_html = circuit._repr_html_()
    # Don't enforce specific html surrounding the diagram content
    assert text_expected in text_html


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_circuit_to_unitary_matrix(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    # Single qubit gates.
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.X(a) ** 0.5).unitary(),
        # fmt: off
        np.array(
            [
                [1j, 1],
                [1, 1j],
            ]
        )
        * np.sqrt(0.5),
        # fmt: on
        atol=1e-8,
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.Y(a) ** 0.25).unitary(), alphaclops.unitary(alphaclops.Y(a) ** 0.25), atol=1e-8
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.Z(a), alphaclops.X(b)).unitary(),
        # fmt: off
        np.array(
            [
                [0, 1, 0, 0],
                [1, 0, 0, 0],
                [0, 0, 0, -1],
                [0, 0, -1, 0],
            ]
        ),
        # fmt: on
        atol=1e-8,
    )

    # Single qubit gates and two qubit gate.
    # fmt: off
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.Z(a), alphaclops.X(b), alphaclops.CNOT(a, b)).unitary(),
        np.array(
            [
                [0, 1, 0, 0],
                [1, 0, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, -1],
            ]
        ),
        atol=1e-8,
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.H(b), alphaclops.CNOT(b, a) ** 0.5, alphaclops.Y(a) ** 0.5).unitary(),
        np.array(
            [
                [1, 1, -1, -1],
                [1j, -1j, -1j, 1j],
                [1, 1, 1, 1],
                [1, -1, 1, -1],
            ]
        )
        * np.sqrt(0.25),
        atol=1e-8,
    )
    # fmt: on

    # Measurement gate has no corresponding matrix.
    c = circuit_cls(alphaclops.measure(a))
    with pytest.raises(ValueError):
        _ = c.unitary(ignore_terminal_measurements=False)

    # Ignoring terminal measurements.
    c = circuit_cls(alphaclops.measure(a))
    alphaclops.testing.assert_allclose_up_to_global_phase(c.unitary(), np.eye(2), atol=1e-8)

    # Ignoring terminal measurements with further alphaclops.
    c = circuit_cls(alphaclops.Z(a), alphaclops.measure(a), alphaclops.Z(b))
    # fmt: off
    alphaclops.testing.assert_allclose_up_to_global_phase(
        c.unitary(), np.array(
            [
                [1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, 1],
            ]), atol=1e-8
    )
    # fmt: on

    # Optionally don't ignoring terminal measurements.
    c = circuit_cls(alphaclops.measure(a))
    with pytest.raises(ValueError, match="measurement"):
        _ = (c.unitary(ignore_terminal_measurements=False),)

    # Non-terminal measurements are not ignored.
    c = circuit_cls(alphaclops.measure(a), alphaclops.X(a))
    with pytest.raises(ValueError):
        _ = c.unitary()

    # Non-terminal measurements are not ignored (multiple qubits).
    c = circuit_cls(alphaclops.measure(a), alphaclops.measure(b), alphaclops.CNOT(a, b))
    with pytest.raises(ValueError):
        _ = c.unitary()

    # Gates without matrix or decomposition raise exception
    class MysteryGate(alphaclops.testing.TwoQubitGate):
        pass

    c = circuit_cls(MysteryGate()(a, b))
    with pytest.raises(TypeError):
        _ = c.unitary()

    # Accounts for measurement bit flipping.
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.measure(a, invert_mask=(True,))).unitary(), alphaclops.unitary(alphaclops.X), atol=1e-8
    )

    # dtype
    c = circuit_cls(alphaclops.X(a))
    assert c.unitary(dtype=np.complex64).dtype == np.complex64
    assert c.unitary(dtype=np.complex128).dtype == np.complex128
    assert c.unitary(dtype=np.float64).dtype == np.float64


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_circuit_unitary(circuit_cls):
    q = alphaclops.NamedQubit('q')

    with_inner_measure = circuit_cls(alphaclops.H(q), alphaclops.measure(q), alphaclops.H(q))
    assert not alphaclops.has_unitary(with_inner_measure)
    assert alphaclops.unitary(with_inner_measure, None) is None

    alphaclops.testing.assert_allclose_up_to_global_phase(
        alphaclops.unitary(circuit_cls(alphaclops.X(q) ** 0.5), alphaclops.measure(q)),
        np.array([[1j, 1], [1, 1j]]) * np.sqrt(0.5),
        atol=1e-8,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_simple_circuits_to_unitary_matrix(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    # Phase parity.
    c = circuit_cls(alphaclops.CNOT(a, b), alphaclops.Z(b), alphaclops.CNOT(a, b))
    assert alphaclops.has_unitary(c)
    m = c.unitary()
    # fmt: off
    alphaclops.testing.assert_allclose_up_to_global_phase(
        m,
        np.array(
            [
                [1, 0, 0, 0],
                [0, -1, 0, 0],
                [0, 0, -1, 0],
                [0, 0, 0, 1],
            ]
        ),
        atol=1e-8,
    )
    # fmt: on

    # 2-qubit matrix matches when qubits in order.
    for expected in [np.diag([1, 1j, -1, -1j]), alphaclops.unitary(alphaclops.CNOT)]:

        class Passthrough(alphaclops.testing.TwoQubitGate):
            def _unitary_(self) -> np.ndarray:
                return expected

        c = circuit_cls(Passthrough()(a, b))
        m = c.unitary()
        alphaclops.testing.assert_allclose_up_to_global_phase(m, expected, atol=1e-8)


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_composite_gate_to_unitary_matrix(circuit_cls):
    class CnotComposite(alphaclops.testing.TwoQubitGate):
        def _decompose_(self, qubits):
            q0, q1 = qubits
            return alphaclops.Y(q1) ** -0.5, alphaclops.CZ(q0, q1), alphaclops.Y(q1) ** 0.5

    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = circuit_cls(
        alphaclops.X(a), CnotComposite()(a, b), alphaclops.X(a), alphaclops.measure(a), alphaclops.X(b), alphaclops.measure(b)
    )
    assert alphaclops.has_unitary(c)

    mat = c.unitary()
    mat_expected = alphaclops.unitary(alphaclops.CNOT)

    alphaclops.testing.assert_allclose_up_to_global_phase(mat, mat_expected, atol=1e-8)


def test_circuit_superoperator_too_many_qubits():
    circuit = alphaclops.Circuit(alphaclops.IdentityGate(num_qubits=11).on(*alphaclops.LineQubit.range(11)))
    assert not circuit._has_superoperator_()
    with pytest.raises(ValueError, match="too many"):
        _ = circuit._superoperator_()


@pytest.mark.parametrize(
    'circuit, expected_superoperator',
    (
        (alphaclops.Circuit(alphaclops.I(q0)), np.eye(4)),
        (alphaclops.Circuit(alphaclops.IdentityGate(2).on(q0, q1)), np.eye(16)),
        (
                alphaclops.Circuit(alphaclops.H(q0)),
                # fmt: off
                np.array(
                [
                    [1, 1, 1, 1],
                    [1, -1, 1, -1],
                    [1, 1, -1, -1],
                    [1, -1, -1, 1]
                ]
            ) / 2,
            # fmt: on
        ),
        (alphaclops.Circuit(alphaclops.S(q0)), np.diag([1, -1j, 1j, 1])),
        (alphaclops.Circuit(alphaclops.depolarize(0.75).on(q0)), np.outer([1, 0, 0, 1], [1, 0, 0, 1]) / 2),
        (
                alphaclops.Circuit(alphaclops.X(q0), alphaclops.depolarize(0.75).on(q0)),
                np.outer([1, 0, 0, 1], [1, 0, 0, 1]) / 2,
        ),
        (
                alphaclops.Circuit(alphaclops.Y(q0), alphaclops.depolarize(0.75).on(q0)),
                np.outer([1, 0, 0, 1], [1, 0, 0, 1]) / 2,
        ),
        (
                alphaclops.Circuit(alphaclops.Z(q0), alphaclops.depolarize(0.75).on(q0)),
                np.outer([1, 0, 0, 1], [1, 0, 0, 1]) / 2,
        ),
        (
                alphaclops.Circuit(alphaclops.H(q0), alphaclops.depolarize(0.75).on(q0)),
                np.outer([1, 0, 0, 1], [1, 0, 0, 1]) / 2,
        ),
        (alphaclops.Circuit(alphaclops.H(q0), alphaclops.H(q0)), np.eye(4)),
        (
                alphaclops.Circuit(alphaclops.H(q0), alphaclops.CNOT(q1, q0), alphaclops.H(q0)),
                np.diag([1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, 1]),
        ),
    ),
)
def test_circuit_superoperator_fixed_values(circuit, expected_superoperator):
    """Tests Circuit._superoperator_() on a few simple circuits."""
    assert circuit._has_superoperator_()
    assert np.allclose(circuit._superoperator_(), expected_superoperator)


@pytest.mark.parametrize(
    'rs, n_qubits',
    (
        ([0.1, 0.2], 1),
        ([0.1, 0.2], 2),
        ([0.8, 0.9], 1),
        ([0.8, 0.9], 2),
        ([0.1, 0.2, 0.3], 1),
        ([0.1, 0.2, 0.3], 2),
        ([0.1, 0.2, 0.3], 3),
    ),
)
def test_circuit_superoperator_depolarizing_channel_compositions(rs, n_qubits):
    """Tests Circuit._superoperator_() on compositions of depolarizing channels."""

    def pauli_error_probability(r: float, n_qubits: int) -> float:
        """Computes Pauli error probability for given depolarization parameter.

        Pauli error is what alphaclops.depolarize takes as argument. Depolarization parameter
        makes it simple to compute the serial composition of depolarizing channels. It
        is multiplicative under channel composition.
        """
        d2 = 4**n_qubits
        return (1 - r) * (d2 - 1) / d2

    def depolarize(r: float, n_qubits: int) -> alphaclops.DepolarizingChannel:
        """Returns depolarization channel with given depolarization parameter."""
        return alphaclops.depolarize(pauli_error_probability(r, n_qubits=n_qubits), n_qubits=n_qubits)

    qubits = alphaclops.LineQubit.range(n_qubits)
    circuit1 = alphaclops.Circuit(depolarize(r, n_qubits).on(*qubits) for r in rs)
    circuit2 = alphaclops.Circuit(depolarize(np.prod(rs), n_qubits).on(*qubits))

    assert circuit1._has_superoperator_()
    assert circuit2._has_superoperator_()

    cm1 = circuit1._superoperator_()
    cm2 = circuit2._superoperator_()
    assert np.allclose(cm1, cm2)


def density_operator_basis(n_qubits: int) -> Iterator[np.ndarray]:
    """Yields operator basis consisting of density operators."""
    RHO_0 = np.array([[1, 0], [0, 0]], dtype=np.complex64)
    RHO_1 = np.array([[0, 0], [0, 1]], dtype=np.complex64)
    RHO_2 = np.array([[1, 1], [1, 1]], dtype=np.complex64) / 2
    RHO_3 = np.array([[1, -1j], [1j, 1]], dtype=np.complex64) / 2
    RHO_BASIS = (RHO_0, RHO_1, RHO_2, RHO_3)

    if n_qubits < 1:
        yield np.array(1)
        return
    for rho1 in RHO_BASIS:
        for rho2 in density_operator_basis(n_qubits - 1):
            yield np.kron(rho1, rho2)


@pytest.mark.parametrize(
    'circuit, initial_state',
    itertools.chain(
        itertools.product(
            [
                alphaclops.Circuit(alphaclops.I(q0)),
                alphaclops.Circuit(alphaclops.X(q0)),
                alphaclops.Circuit(alphaclops.Y(q0)),
                alphaclops.Circuit(alphaclops.Z(q0)),
                alphaclops.Circuit(alphaclops.S(q0)),
                alphaclops.Circuit(alphaclops.T(q0)),
            ],
            density_operator_basis(n_qubits=1),
        ),
        itertools.product(
            [
                alphaclops.Circuit(alphaclops.H(q0), alphaclops.CNOT(q0, q1)),
                alphaclops.Circuit(alphaclops.depolarize(0.2).on(q0), alphaclops.CNOT(q0, q1)),
                alphaclops.Circuit(
                    alphaclops.X(q0),
                    alphaclops.amplitude_damp(0.2).on(q0),
                    alphaclops.depolarize(0.1).on(q1),
                    alphaclops.CNOT(q0, q1),
                ),
            ],
            density_operator_basis(n_qubits=2),
        ),
        itertools.product(
            [
                alphaclops.Circuit(
                    alphaclops.depolarize(0.1, n_qubits=2).on(q0, q1),
                    alphaclops.H(q2),
                    alphaclops.CNOT(q1, q2),
                    alphaclops.phase_damp(0.1).on(q0),
                ),
                alphaclops.Circuit(alphaclops.H(q0), alphaclops.H(q1), alphaclops.TOFFOLI(q0, q1, q2)),
            ],
            density_operator_basis(n_qubits=3),
        ),
    ),
)
def test_compare_circuits_superoperator_to_simulation(circuit, initial_state):
    """Compares action of circuit superoperator and circuit simulation."""
    assert circuit._has_superoperator_()
    superoperator = circuit._superoperator_()
    vectorized_initial_state = initial_state.reshape(-1)
    vectorized_final_state = superoperator @ vectorized_initial_state
    actual_state = np.reshape(vectorized_final_state, initial_state.shape)

    sim = alphaclops.DensityMatrixSimulator()
    expected_state = sim.simulate(circuit, initial_state=initial_state).final_density_matrix

    assert np.allclose(actual_state, expected_state)


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_expanding_gate_symbols(circuit_cls):
    class MultiTargetCZ(alphaclops.Gate):
        def __init__(self, num_qubits):
            self._num_qubits = num_qubits

        def num_qubits(self) -> int:
            return self._num_qubits

        def _circuit_diagram_info_(self, args: alphaclops.CircuitDiagramInfoArgs) -> Tuple[str, ...]:
            assert args.known_qubit_count is not None
            return ('@',) + ('Z',) * (args.known_qubit_count - 1)

    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')
    t0 = circuit_cls(MultiTargetCZ(1).on(c))
    t1 = circuit_cls(MultiTargetCZ(2).on(c, a))
    t2 = circuit_cls(MultiTargetCZ(3).on(c, a, b))

    alphaclops.testing.assert_has_diagram(
        t0,
        """
c: ───@───
""",
    )

    alphaclops.testing.assert_has_diagram(
        t1,
        """
a: ───Z───
      │
c: ───@───
""",
    )

    alphaclops.testing.assert_has_diagram(
        t2,
        """
a: ───Z───
      │
b: ───Z───
      │
c: ───@───
""",
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_transposed_diagram_exponent_order(circuit_cls):
    a, b, c = alphaclops.LineQubit.range(3)
    circuit = circuit_cls(alphaclops.CZ(a, b) ** -0.5, alphaclops.CZ(a, c) ** 0.5, alphaclops.CZ(b, c) ** 0.125)
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0 1      2
│ │      │
@─@^-0.5 │
│ │      │
@─┼──────@^0.5
│ │      │
│ @──────@^(1/8)
│ │      │
""",
        transpose=True,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_transposed_diagram_can_depend_on_transpose(circuit_cls):
    class TestGate(alphaclops.Gate):
        def num_qubits(self):
            return 1

        def _circuit_diagram_info_(self, args):
            return alphaclops.CircuitDiagramInfo(wire_symbols=("t" if args.transpose else "r",))

    c = alphaclops.Circuit(TestGate()(alphaclops.NamedQubit("a")))

    alphaclops.testing.assert_has_diagram(c, "a: ───r───")
    alphaclops.testing.assert_has_diagram(
        c,
        """
a
│
t
│
""",
        transpose=True,
    )


def test_insert_moments():
    q = alphaclops.NamedQubit('q')
    c = alphaclops.Circuit()

    m0 = alphaclops.Moment([alphaclops.X(q)])
    c.append(m0)
    assert list(c) == [m0]
    assert c[0] == m0

    m1 = alphaclops.Moment([alphaclops.Y(q)])
    c.append(m1)
    assert list(c) == [m0, m1]
    assert c[1] == m1

    m2 = alphaclops.Moment([alphaclops.Z(q)])
    c.insert(0, m2)
    assert list(c) == [m2, m0, m1]
    assert c[0] == m2

    assert c._moments == [m2, m0, m1]
    assert c._moments[0] == m2


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_final_state_vector(circuit_cls):
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    # State ordering.
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.X(a) ** 0.5).final_state_vector(
            ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([1j, 1]) * np.sqrt(0.5),
        atol=1e-8,
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.X(a) ** 0.5).final_state_vector(
            initial_state=0, ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([1j, 1]) * np.sqrt(0.5),
        atol=1e-8,
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.X(a) ** 0.5).final_state_vector(
            initial_state=1, ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([1, 1j]) * np.sqrt(0.5),
        atol=1e-8,
    )

    # Vector state.
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.X(a) ** 0.5).final_state_vector(
            initial_state=np.array([1j, 1]) * np.sqrt(0.5),
            ignore_terminal_measurements=False,
            dtype=np.complex64,
        ),
        np.array([0, 1]),
        atol=1e-8,
    )

    # Qubit ordering.
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.CNOT(a, b)).final_state_vector(
            initial_state=0, ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([1, 0, 0, 0]),
        atol=1e-8,
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.CNOT(a, b)).final_state_vector(
            initial_state=1, ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([0, 1, 0, 0]),
        atol=1e-8,
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.CNOT(a, b)).final_state_vector(
            initial_state=2, ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([0, 0, 0, 1]),
        atol=1e-8,
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.CNOT(a, b)).final_state_vector(
            initial_state=3, ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([0, 0, 1, 0]),
        atol=1e-8,
    )

    # Product state
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.CNOT(a, b)).final_state_vector(
            initial_state=alphaclops.KET_ZERO(a) * alphaclops.KET_ZERO(b),
            ignore_terminal_measurements=False,
            dtype=np.complex64,
        ),
        np.array([1, 0, 0, 0]),
        atol=1e-8,
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.CNOT(a, b)).final_state_vector(
            initial_state=alphaclops.KET_ZERO(a) * alphaclops.KET_ONE(b),
            ignore_terminal_measurements=False,
            dtype=np.complex64,
        ),
        np.array([0, 1, 0, 0]),
        atol=1e-8,
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.CNOT(a, b)).final_state_vector(
            initial_state=alphaclops.KET_ONE(a) * alphaclops.KET_ZERO(b),
            ignore_terminal_measurements=False,
            dtype=np.complex64,
        ),
        np.array([0, 0, 0, 1]),
        atol=1e-8,
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.CNOT(a, b)).final_state_vector(
            initial_state=alphaclops.KET_ONE(a) * alphaclops.KET_ONE(b),
            ignore_terminal_measurements=False,
            dtype=np.complex64,
        ),
        np.array([0, 0, 1, 0]),
        atol=1e-8,
    )

    # Measurements.
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.measure(a)).final_state_vector(
            ignore_terminal_measurements=True, dtype=np.complex64
        ),
        np.array([1, 0]),
        atol=1e-8,
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.X(a), alphaclops.measure(a)).final_state_vector(
            ignore_terminal_measurements=True, dtype=np.complex64
        ),
        np.array([0, 1]),
        atol=1e-8,
    )
    with pytest.raises(ValueError):
        alphaclops.testing.assert_allclose_up_to_global_phase(
            circuit_cls(alphaclops.measure(a), alphaclops.X(a)).final_state_vector(
                ignore_terminal_measurements=True, dtype=np.complex64
            ),
            np.array([1, 0]),
            atol=1e-8,
        )
    with pytest.raises(ValueError):
        alphaclops.testing.assert_allclose_up_to_global_phase(
            circuit_cls(alphaclops.measure(a)).final_state_vector(
                ignore_terminal_measurements=False, dtype=np.complex64
            ),
            np.array([1, 0]),
            atol=1e-8,
        )

    # Qubit order.
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.Z(a), alphaclops.X(b)).final_state_vector(
            qubit_order=[a, b], ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([0, 1, 0, 0]),
        atol=1e-8,
    )
    alphaclops.testing.assert_allclose_up_to_global_phase(
        circuit_cls(alphaclops.Z(a), alphaclops.X(b)).final_state_vector(
            qubit_order=[b, a], ignore_terminal_measurements=False, dtype=np.complex64
        ),
        np.array([0, 0, 1, 0]),
        atol=1e-8,
    )

    # Dtypes.
    dtypes = [np.complex64, np.complex128]
    if hasattr(np, 'complex256'):  # Some systems don't support 128 bit floats.
        dtypes.append(np.complex256)
    for dt in dtypes:
        alphaclops.testing.assert_allclose_up_to_global_phase(
            circuit_cls(alphaclops.X(a) ** 0.5).final_state_vector(
                initial_state=np.array([1j, 1]) * np.sqrt(0.5),
                ignore_terminal_measurements=False,
                dtype=dt,
            ),
            np.array([0, 1]),
            atol=1e-8,
        )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_is_parameterized(circuit_cls, resolve_fn):
    a, b = alphaclops.LineQubit.range(2)
    circuit = circuit_cls(
        alphaclops.CZ(a, b) ** sympy.Symbol('u'),
        alphaclops.X(a) ** sympy.Symbol('v'),
        alphaclops.Y(b) ** sympy.Symbol('w'),
    )
    assert alphaclops.is_parameterized(circuit)

    circuit = resolve_fn(circuit, alphaclops.ParamResolver({'u': 0.1, 'v': 0.3}))
    assert alphaclops.is_parameterized(circuit)

    circuit = resolve_fn(circuit, alphaclops.ParamResolver({'w': 0.2}))
    assert not alphaclops.is_parameterized(circuit)


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_resolve_parameters(circuit_cls, resolve_fn):
    a, b = alphaclops.LineQubit.range(2)
    circuit = circuit_cls(
        alphaclops.CZ(a, b) ** sympy.Symbol('u'),
        alphaclops.X(a) ** sympy.Symbol('v'),
        alphaclops.Y(b) ** sympy.Symbol('w'),
    )
    resolved_circuit = resolve_fn(circuit, alphaclops.ParamResolver({'u': 0.1, 'v': 0.3, 'w': 0.2}))
    alphaclops.testing.assert_has_diagram(
        resolved_circuit,
        """
0: ───@───────X^0.3───
      │
1: ───@^0.1───Y^0.2───
""",
    )
    q = alphaclops.NamedQubit('q')
    # no-op parameter resolution
    circuit = circuit_cls([alphaclops.Moment(), alphaclops.Moment([alphaclops.X(q)])])
    resolved_circuit = resolve_fn(circuit, alphaclops.ParamResolver({}))
    alphaclops.testing.assert_same_circuits(circuit, resolved_circuit)
    # actually resolve something
    circuit = circuit_cls([alphaclops.Moment(), alphaclops.Moment([alphaclops.X(q) ** sympy.Symbol('x')])])
    resolved_circuit = resolve_fn(circuit, alphaclops.ParamResolver({'x': 0.2}))
    expected_circuit = circuit_cls([alphaclops.Moment(), alphaclops.Moment([alphaclops.X(q) ** 0.2])])
    alphaclops.testing.assert_same_circuits(expected_circuit, resolved_circuit)


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_resolve_parameters_no_change(circuit_cls, resolve_fn):
    a, b = alphaclops.LineQubit.range(2)
    circuit = circuit_cls(alphaclops.CZ(a, b), alphaclops.X(a), alphaclops.Y(b))
    resolved_circuit = resolve_fn(circuit, alphaclops.ParamResolver({'u': 0.1, 'v': 0.3, 'w': 0.2}))
    assert resolved_circuit is circuit

    circuit = circuit_cls(
        alphaclops.CZ(a, b) ** sympy.Symbol('u'),
        alphaclops.X(a) ** sympy.Symbol('v'),
        alphaclops.Y(b) ** sympy.Symbol('w'),
    )
    resolved_circuit = resolve_fn(circuit, alphaclops.ParamResolver({}))
    assert resolved_circuit is circuit


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_parameter_names(circuit_cls, resolve_fn):
    a, b = alphaclops.LineQubit.range(2)
    circuit = circuit_cls(
        alphaclops.CZ(a, b) ** sympy.Symbol('u'),
        alphaclops.X(a) ** sympy.Symbol('v'),
        alphaclops.Y(b) ** sympy.Symbol('w'),
    )
    resolved_circuit = resolve_fn(circuit, alphaclops.ParamResolver({'u': 0.1, 'v': 0.3, 'w': 0.2}))
    assert alphaclops.parameter_names(circuit) == {'u', 'v', 'w'}
    assert alphaclops.parameter_names(resolved_circuit) == set()


def test_items():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.Circuit()
    m1 = alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)])
    m2 = alphaclops.Moment([alphaclops.X(a)])
    m3 = alphaclops.Moment([])
    m4 = alphaclops.Moment([alphaclops.CZ(a, b)])

    c[:] = [m1, m2]
    alphaclops.testing.assert_same_circuits(c, alphaclops.Circuit([m1, m2]))

    assert c[0] == m1
    del c[0]
    alphaclops.testing.assert_same_circuits(c, alphaclops.Circuit([m2]))

    c.append(m1)
    c.append(m3)
    alphaclops.testing.assert_same_circuits(c, alphaclops.Circuit([m2, m1, m3]))

    assert c[0:2] == alphaclops.Circuit([m2, m1])
    c[0:2] = [m4]
    alphaclops.testing.assert_same_circuits(c, alphaclops.Circuit([m4, m3]))

    c[:] = [m1]
    alphaclops.testing.assert_same_circuits(c, alphaclops.Circuit([m1]))

    with pytest.raises(TypeError):
        c[:] = [m1, 1]
    with pytest.raises(TypeError):
        c[0] = 1


def test_copy():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.Circuit(alphaclops.X(a), alphaclops.CZ(a, b), alphaclops.Z(a), alphaclops.Z(b))
    assert c == c.copy() == c.__copy__()
    c2 = c.copy()
    assert c2 == c
    c2[:] = []
    assert c2 != c


def test_batch_remove():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    original = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.Z(b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    # Empty case.
    after = original.copy()
    after.batch_remove([])
    assert after == original

    # Delete one.
    after = original.copy()
    after.batch_remove([(0, alphaclops.X(a))])
    assert after == alphaclops.Circuit(
        [
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.Z(b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    # Out of range.
    after = original.copy()
    with pytest.raises(IndexError):
        after.batch_remove([(500, alphaclops.X(a))])
    assert after == original

    # Delete several.
    after = original.copy()
    after.batch_remove([(0, alphaclops.X(a)), (2, alphaclops.CZ(a, b))])
    assert after == alphaclops.Circuit(
        [
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.Z(b)]),
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    # Delete all.
    after = original.copy()
    after.batch_remove(
        [(0, alphaclops.X(a)), (1, alphaclops.Z(b)), (2, alphaclops.CZ(a, b)), (3, alphaclops.X(a)), (3, alphaclops.X(b))]
    )
    assert after == alphaclops.Circuit([alphaclops.Moment(), alphaclops.Moment(), alphaclops.Moment(), alphaclops.Moment()])

    # Delete moment partially.
    after = original.copy()
    after.batch_remove([(3, alphaclops.X(a))])
    assert after == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.Z(b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(b)]),
        ]
    )

    # Deleting something that's not there.
    after = original.copy()
    with pytest.raises(ValueError):
        after.batch_remove([(0, alphaclops.X(b))])
    assert after == original

    # Duplicate delete.
    after = original.copy()
    with pytest.raises(ValueError):
        after.batch_remove([(0, alphaclops.X(a)), (0, alphaclops.X(a))])
    assert after == original


def test_batch_replace():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    original = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.Z(b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    # Empty case.
    after = original.copy()
    after.batch_replace([])
    assert after == original

    # Replace one.
    after = original.copy()
    after.batch_replace([(0, alphaclops.X(a), alphaclops.Y(a))])
    assert after == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.Y(a)]),
            alphaclops.Moment([alphaclops.Z(b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    # Out of range.
    after = original.copy()
    with pytest.raises(IndexError):
        after.batch_replace([(500, alphaclops.X(a), alphaclops.Y(a))])
    assert after == original

    # Gate does not exist.
    after = original.copy()
    with pytest.raises(ValueError):
        after.batch_replace([(0, alphaclops.Z(a), alphaclops.Y(a))])
    assert after == original

    # Replace several.
    after = original.copy()
    after.batch_replace([(0, alphaclops.X(a), alphaclops.Y(a)), (2, alphaclops.CZ(a, b), alphaclops.CNOT(a, b))])
    assert after == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.Y(a)]),
            alphaclops.Moment([alphaclops.Z(b)]),
            alphaclops.Moment([alphaclops.CNOT(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )


def test_batch_insert_into():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')
    original = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    # Empty case.
    after = original.copy()
    after.batch_insert_into([])
    assert after == original

    # Add into non-empty moment.
    after = original.copy()
    after.batch_insert_into([(0, alphaclops.X(b))])
    assert after == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    # Add multiple operations into non-empty moment.
    after = original.copy()
    after.batch_insert_into([(0, [alphaclops.X(b), alphaclops.X(c)])])
    assert after == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b), alphaclops.X(c)]),
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    # Add into empty moment.
    after = original.copy()
    after.batch_insert_into([(1, alphaclops.Z(b))])
    assert after == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.Z(b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    # Add multiple operations into empty moment.
    after = original.copy()
    after.batch_insert_into([(1, [alphaclops.Z(a), alphaclops.Z(b)])])
    assert after == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([alphaclops.Z(a), alphaclops.Z(b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    # Add into two moments.
    after = original.copy()
    after.batch_insert_into([(1, alphaclops.Z(b)), (0, alphaclops.X(b))])
    assert after == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
            alphaclops.Moment([alphaclops.Z(b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    # Out of range.
    after = original.copy()
    with pytest.raises(IndexError):
        after.batch_insert_into([(500, alphaclops.X(a))])
    assert after == original

    # Collision.
    after = original.copy()
    with pytest.raises(ValueError):
        after.batch_insert_into([(0, alphaclops.X(a))])
    assert after == original

    # Collision with multiple operations.
    after = original.copy()
    with pytest.raises(ValueError):
        after.batch_insert_into([(0, [alphaclops.X(b), alphaclops.X(c), alphaclops.X(a)])])
    assert after == original

    # Duplicate insertion collision.
    after = original.copy()
    with pytest.raises(ValueError):
        after.batch_insert_into([(1, alphaclops.X(a)), (1, alphaclops.CZ(a, b))])
    assert after == original


def test_batch_insert():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    original = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(a)]),
            alphaclops.Moment([]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )

    # Empty case.
    after = original.copy()
    after.batch_insert([])
    assert after == original

    # Pushing.
    after = original.copy()
    after.batch_insert([(0, alphaclops.CZ(a, b)), (0, alphaclops.CNOT(a, b)), (1, alphaclops.Z(b))])
    assert after == alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.CNOT(a, b)]),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.Z(b)]),
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.CZ(a, b)]),
            alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]),
        ]
    )


def test_batch_insert_multiple_same_index():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit()
    c.batch_insert([(0, alphaclops.Z(a)), (0, alphaclops.Z(b)), (0, alphaclops.Z(a))])
    alphaclops.testing.assert_same_circuits(
        c, alphaclops.Circuit([alphaclops.Moment([alphaclops.Z(a), alphaclops.Z(b)]), alphaclops.Moment([alphaclops.Z(a)])])
    )


def test_batch_insert_reverses_order_for_same_index_inserts():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit()
    c.batch_insert([(0, alphaclops.Z(a)), (0, alphaclops.CZ(a, b)), (0, alphaclops.Z(b))])
    assert c == alphaclops.Circuit(alphaclops.Z(b), alphaclops.CZ(a, b), alphaclops.Z(a))


def test_batch_insert_maintains_order_despite_multiple_previous_inserts():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.H(a))
    c.batch_insert([(0, alphaclops.Z(a)), (0, alphaclops.Z(a)), (0, alphaclops.Z(a)), (1, alphaclops.CZ(a, b))])
    assert c == alphaclops.Circuit([alphaclops.Z(a)] * 3, alphaclops.H(a), alphaclops.CZ(a, b))


def test_batch_insert_doesnt_overshift_due_to_previous_shifts():
    a = alphaclops.NamedQubit('a')
    c = alphaclops.Circuit([alphaclops.H(a)] * 3)
    c.batch_insert([(0, alphaclops.Z(a)), (0, alphaclops.Z(a)), (1, alphaclops.X(a)), (2, alphaclops.Y(a))])
    assert c == alphaclops.Circuit(
        alphaclops.Z(a), alphaclops.Z(a), alphaclops.H(a), alphaclops.X(a), alphaclops.H(a), alphaclops.Y(a), alphaclops.H(a)
    )


def test_batch_insert_doesnt_overshift_due_to_inline_inserts():
    a, b = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.SWAP(a, b), alphaclops.SWAP(a, b), alphaclops.H(a), alphaclops.SWAP(a, b), alphaclops.SWAP(a, b))
    c.batch_insert([(0, alphaclops.X(a)), (3, alphaclops.X(b)), (4, alphaclops.Y(a))])
    assert c == alphaclops.Circuit(
        alphaclops.X(a),
        alphaclops.SWAP(a, b),
        alphaclops.SWAP(a, b),
        alphaclops.H(a),
        alphaclops.X(b),
        alphaclops.SWAP(a, b),
        alphaclops.Y(a),
        alphaclops.SWAP(a, b),
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_next_moments_operating_on(circuit_cls):
    for _ in range(20):
        n_moments = randint(1, 10)
        circuit = alphaclops.testing.random_circuit(randint(1, 20), n_moments, random())
        circuit_qubits = circuit.all_qubits()
        n_key_qubits = randint(int(bool(circuit_qubits)), len(circuit_qubits))
        key_qubits = sample(sorted(circuit_qubits), n_key_qubits)
        start = randrange(len(circuit))
        next_moments = circuit.next_moments_operating_on(key_qubits, start)
        for q, m in next_moments.items():
            if m == len(circuit):
                p = circuit.prev_moment_operating_on([q])
            else:
                p = circuit.prev_moment_operating_on([q], m - 1)
            assert (not p) or (p < start)


def test_pick_inserted_ops_moment_indices():
    for _ in range(20):
        n_moments = randint(1, 10)
        n_qubits = randint(1, 20)
        op_density = random()
        circuit = alphaclops.testing.random_circuit(n_qubits, n_moments, op_density)
        start = randrange(n_moments)
        first_half = alphaclops.Circuit(circuit[:start])
        second_half = alphaclops.Circuit(circuit[start:])
        operations = tuple(op for moment in second_half for op in moment.operations)
        squeezed_second_half = alphaclops.Circuit(operations, strategy=alphaclops.InsertStrategy.EARLIEST)
        expected_circuit = alphaclops.Circuit(first_half._moments + squeezed_second_half._moments)
        expected_circuit._moments += [
            alphaclops.Moment() for _ in range(len(circuit) - len(expected_circuit))
        ]
        insert_indices, _ = circuits.circuit._pick_inserted_ops_moment_indices(operations, start)
        actual_circuit = alphaclops.Circuit(
            first_half._moments + [alphaclops.Moment() for _ in range(n_moments - start)]
        )
        for op, insert_index in zip(operations, insert_indices):
            actual_circuit._moments[insert_index] = actual_circuit._moments[
                insert_index
            ].with_operation(op)
        assert actual_circuit == expected_circuit


def test_push_frontier_new_moments():
    operation = alphaclops.X(alphaclops.NamedQubit('q'))
    insertion_index = 3
    circuit = alphaclops.Circuit()
    circuit._insert_operations([operation], [insertion_index])
    assert circuit == alphaclops.Circuit(
        [alphaclops.Moment() for _ in range(insertion_index)] + [alphaclops.Moment([operation])]
    )


def test_push_frontier_random_circuit():
    for _ in range(20):
        n_moments = randint(1, 10)
        circuit = alphaclops.testing.random_circuit(randint(1, 20), n_moments, random())
        qubits = sorted(circuit.all_qubits())
        early_frontier = {q: randint(0, n_moments) for q in sample(qubits, randint(0, len(qubits)))}
        late_frontier = {q: randint(0, n_moments) for q in sample(qubits, randint(0, len(qubits)))}
        update_qubits = sample(qubits, randint(0, len(qubits)))

        orig_early_frontier = {q: f for q, f in early_frontier.items()}
        orig_moments = [m for m in circuit._moments]
        insert_index, n_new_moments = circuit._push_frontier(
            early_frontier, late_frontier, update_qubits
        )

        assert set(early_frontier.keys()) == set(orig_early_frontier.keys())
        for q in set(early_frontier).difference(update_qubits):
            assert early_frontier[q] == orig_early_frontier[q]
        for q, f in late_frontier.items():
            assert orig_early_frontier.get(q, 0) <= late_frontier[q] + n_new_moments
            if f != len(orig_moments):
                assert orig_moments[f] == circuit[f + n_new_moments]
        for q in set(update_qubits).intersection(early_frontier):
            if orig_early_frontier[q] == insert_index:
                assert orig_early_frontier[q] == early_frontier[q]
                assert (not n_new_moments) or (circuit._moments[early_frontier[q]] == alphaclops.Moment())
            elif orig_early_frontier[q] == len(orig_moments):
                assert early_frontier[q] == len(circuit)
            else:
                assert orig_moments[orig_early_frontier[q]] == circuit._moments[early_frontier[q]]


@pytest.mark.parametrize(
    'circuit', [alphaclops.testing.random_circuit(alphaclops.LineQubit.range(10), 10, 0.5) for _ in range(20)]
)
def test_insert_operations_random_circuits(circuit):
    n_moments = len(circuit)
    operations, insert_indices = [], []
    for moment_index, moment in enumerate(circuit):
        for op in moment.operations:
            operations.append(op)
            insert_indices.append(moment_index)
    other_circuit = alphaclops.Circuit([alphaclops.Moment() for _ in range(n_moments)])
    other_circuit._insert_operations(operations, insert_indices)
    assert circuit == other_circuit


def test_insert_operations_errors():
    a, b, c = (alphaclops.NamedQubit(s) for s in 'abc')
    with pytest.raises(ValueError):
        circuit = alphaclops.Circuit([alphaclops.Moment([alphaclops.Z(c)])])
        operations = [alphaclops.X(a), alphaclops.CZ(a, b)]
        insertion_indices = [0, 0]
        circuit._insert_operations(operations, insertion_indices)

    with pytest.raises(ValueError):
        circuit = alphaclops.Circuit(alphaclops.X(a))
        operations = [alphaclops.CZ(a, b)]
        insertion_indices = [0]
        circuit._insert_operations(operations, insertion_indices)

    with pytest.raises(ValueError):
        circuit = alphaclops.Circuit()
        operations = [alphaclops.X(a), alphaclops.CZ(a, b)]
        insertion_indices = []
        circuit._insert_operations(operations, insertion_indices)


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_to_qasm(circuit_cls):
    q0 = alphaclops.NamedQubit('q0')
    circuit = circuit_cls(alphaclops.X(q0))
    assert circuit.to_qasm() == alphaclops.qasm(circuit)
    assert (
        circuit.to_qasm()
        == f"""// Generated from alphaclops v{alphaclops.__version__}

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q0]
qreg q[1];


x q[0];
"""
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_save_qasm(tmpdir, circuit_cls):
    file_path = os.path.join(tmpdir, 'test.qasm')
    q0 = alphaclops.NamedQubit('q0')
    circuit = circuit_cls(alphaclops.X(q0))

    circuit.save_qasm(file_path)
    with open(file_path, 'r') as f:
        file_content = f.read()
    assert (
        file_content
        == f"""// Generated from alphaclops v{alphaclops.__version__}

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q0]
qreg q[1];


x q[0];
"""
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_findall_operations_between(circuit_cls):
    a, b, c, d = alphaclops.LineQubit.range(4)

    #    0: ───H───@───────────────────────────────────────@───H───
    #              │                                       │
    #    1: ───────@───H───@───────────────────────@───H───@───────
    #                      │                       │
    #    2: ───────────────@───H───@───────@───H───@───────────────
    #                              │       │
    #    3: ───────────────────────@───H───@───────────────────────
    #
    # moments: 0   1   2   3   4   5   6   7   8   9   10  11  12
    circuit = circuit_cls(
        alphaclops.H(a),
        alphaclops.CZ(a, b),
        alphaclops.H(b),
        alphaclops.CZ(b, c),
        alphaclops.H(c),
        alphaclops.CZ(c, d),
        alphaclops.H(d),
        alphaclops.CZ(c, d),
        alphaclops.H(c),
        alphaclops.CZ(b, c),
        alphaclops.H(b),
        alphaclops.CZ(a, b),
        alphaclops.H(a),
    )

    # Empty frontiers means no results.
    actual = circuit.findall_operations_between(start_frontier={}, end_frontier={})
    assert actual == []

    # Empty range is empty.
    actual = circuit.findall_operations_between(start_frontier={a: 5}, end_frontier={a: 5})
    assert actual == []

    # Default end_frontier value is len(circuit.
    actual = circuit.findall_operations_between(start_frontier={a: 5}, end_frontier={})
    assert actual == [(11, alphaclops.CZ(a, b)), (12, alphaclops.H(a))]

    # Default start_frontier value is 0.
    actual = circuit.findall_operations_between(start_frontier={}, end_frontier={a: 5})
    assert actual == [(0, alphaclops.H(a)), (1, alphaclops.CZ(a, b))]

    # omit_crossing_operations omits crossing operations.
    actual = circuit.findall_operations_between(
        start_frontier={a: 5}, end_frontier={}, omit_crossing_operations=True
    )
    assert actual == [(12, alphaclops.H(a))]

    # omit_crossing_operations keeps operations across included regions.
    actual = circuit.findall_operations_between(
        start_frontier={a: 5, b: 5}, end_frontier={}, omit_crossing_operations=True
    )
    assert actual == [(10, alphaclops.H(b)), (11, alphaclops.CZ(a, b)), (12, alphaclops.H(a))]

    # Regions are OR'd together, not AND'd together.
    actual = circuit.findall_operations_between(start_frontier={a: 5}, end_frontier={b: 5})
    assert actual == [
        (1, alphaclops.CZ(a, b)),
        (2, alphaclops.H(b)),
        (3, alphaclops.CZ(b, c)),
        (11, alphaclops.CZ(a, b)),
        (12, alphaclops.H(a)),
    ]

    # Regions are OR'd together, not AND'd together (2).
    actual = circuit.findall_operations_between(start_frontier={a: 5}, end_frontier={a: 5, b: 5})
    assert actual == [(1, alphaclops.CZ(a, b)), (2, alphaclops.H(b)), (3, alphaclops.CZ(b, c))]

    # Inclusive start, exclusive end.
    actual = circuit.findall_operations_between(start_frontier={c: 4}, end_frontier={c: 8})
    assert actual == [(4, alphaclops.H(c)), (5, alphaclops.CZ(c, d)), (7, alphaclops.CZ(c, d))]

    # Out of range is clamped.
    actual = circuit.findall_operations_between(start_frontier={a: -100}, end_frontier={a: +100})
    assert actual == [(0, alphaclops.H(a)), (1, alphaclops.CZ(a, b)), (11, alphaclops.CZ(a, b)), (12, alphaclops.H(a))]


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_reachable_frontier_from(circuit_cls):
    a, b, c, d = alphaclops.LineQubit.range(4)

    #    0: ───H───@───────────────────────────────────────@───H───
    #              │                                       │
    #    1: ───────@───H───@───────────────────────@───H───@───────
    #                      │                       │
    #    2: ───────────────@───H───@───────@───H───@───────────────
    #                              │       │
    #    3: ───────────────────────@───H───@───────────────────────
    #
    # moments: 0   1   2   3   4   5   6   7   8   9   10  11  12
    circuit = circuit_cls(
        alphaclops.H(a),
        alphaclops.CZ(a, b),
        alphaclops.H(b),
        alphaclops.CZ(b, c),
        alphaclops.H(c),
        alphaclops.CZ(c, d),
        alphaclops.H(d),
        alphaclops.CZ(c, d),
        alphaclops.H(c),
        alphaclops.CZ(b, c),
        alphaclops.H(b),
        alphaclops.CZ(a, b),
        alphaclops.H(a),
    )

    # Empty cases.
    assert circuit_cls().reachable_frontier_from(start_frontier={}) == {}
    assert circuit.reachable_frontier_from(start_frontier={}) == {}

    # Clamped input cases.
    assert circuit_cls().reachable_frontier_from(start_frontier={a: 5}) == {a: 5}
    assert circuit_cls().reachable_frontier_from(start_frontier={a: -100}) == {a: 0}
    assert circuit.reachable_frontier_from(start_frontier={a: 100}) == {a: 100}

    # Stopped by crossing outside case.
    assert circuit.reachable_frontier_from({a: -1}) == {a: 1}
    assert circuit.reachable_frontier_from({a: 0}) == {a: 1}
    assert circuit.reachable_frontier_from({a: 1}) == {a: 1}
    assert circuit.reachable_frontier_from({a: 2}) == {a: 11}
    assert circuit.reachable_frontier_from({a: 5}) == {a: 11}
    assert circuit.reachable_frontier_from({a: 10}) == {a: 11}
    assert circuit.reachable_frontier_from({a: 11}) == {a: 11}
    assert circuit.reachable_frontier_from({a: 12}) == {a: 13}
    assert circuit.reachable_frontier_from({a: 13}) == {a: 13}
    assert circuit.reachable_frontier_from({a: 14}) == {a: 14}

    # Inside crossing works only before blocked case.
    assert circuit.reachable_frontier_from({a: 0, b: 0}) == {a: 11, b: 3}
    assert circuit.reachable_frontier_from({a: 2, b: 2}) == {a: 11, b: 3}
    assert circuit.reachable_frontier_from({a: 0, b: 4}) == {a: 1, b: 9}
    assert circuit.reachable_frontier_from({a: 3, b: 4}) == {a: 11, b: 9}
    assert circuit.reachable_frontier_from({a: 3, b: 9}) == {a: 11, b: 9}
    assert circuit.reachable_frontier_from({a: 3, b: 10}) == {a: 13, b: 13}

    # Travelling shadow.
    assert circuit.reachable_frontier_from({a: 0, b: 0, c: 0}) == {a: 11, b: 9, c: 5}

    # Full circuit
    assert circuit.reachable_frontier_from({a: 0, b: 0, c: 0, d: 0}) == {a: 13, b: 13, c: 13, d: 13}

    # Blocker.
    assert circuit.reachable_frontier_from(
        {a: 0, b: 0, c: 0, d: 0}, is_blocker=lambda op: op == alphaclops.CZ(b, c)
    ) == {a: 11, b: 3, c: 3, d: 5}


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_submoments(circuit_cls):
    a, b, c, d, e, f = alphaclops.LineQubit.range(6)
    circuit = circuit_cls(
        alphaclops.H.on(a),
        alphaclops.H.on(d),
        alphaclops.CZ.on(a, d),
        alphaclops.CZ.on(b, c),
        (alphaclops.CNOT ** 0.5).on(a, d),
        (alphaclops.CNOT ** 0.5).on(b, e),
        (alphaclops.CNOT ** 0.5).on(c, f),
        alphaclops.H.on(c),
        alphaclops.H.on(e),
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
          ┌───────────┐   ┌──────┐
0: ───H────@───────────────@─────────
           │               │
1: ───@────┼@──────────────┼─────────
      │    ││              │
2: ───@────┼┼────@─────────┼────H────
           ││    │         │
3: ───H────@┼────┼─────────X^0.5─────
            │    │
4: ─────────X^0.5┼─────────H─────────
                 │
5: ──────────────X^0.5───────────────
          └───────────┘   └──────┘
""",
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
  0 1 2 3     4     5
  │ │ │ │     │     │
  H @─@ H     │     │
  │ │ │ │     │     │
┌╴│ │ │ │     │     │    ╶┐
│ @─┼─┼─@     │     │     │
│ │ @─┼─┼─────X^0.5 │     │
│ │ │ @─┼─────┼─────X^0.5 │
└╴│ │ │ │     │     │    ╶┘
  │ │ │ │     │     │
┌╴│ │ │ │     │     │    ╶┐
│ @─┼─┼─X^0.5 H     │     │
│ │ │ H │     │     │     │
└╴│ │ │ │     │     │    ╶┘
  │ │ │ │     │     │
""",
        transpose=True,
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        r"""
          /-----------\   /------\
0: ---H----@---------------@---------
           |               |
1: ---@----|@--------------|---------
      |    ||              |
2: ---@----||----@---------|----H----
           ||    |         |
3: ---H----@|----|---------X^0.5-----
            |    |
4: ---------X^0.5|---------H---------
                 |
5: --------------X^0.5---------------
          \-----------/   \------/
""",
        use_unicode_characters=False,
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        r"""
  0 1 2 3     4     5
  | | | |     |     |
  H @-@ H     |     |
  | | | |     |     |
/ | | | |     |     |     \
| @-----@     |     |     |
| | @---------X^0.5 |     |
| | | @-------------X^0.5 |
\ | | | |     |     |     /
  | | | |     |     |
/ | | | |     |     |     \
| @-----X^0.5 H     |     |
| | | H |     |     |     |
\ | | | |     |     |     /
  | | | |     |     |
""",
        use_unicode_characters=False,
        transpose=True,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_decompose(circuit_cls):
    a, b = alphaclops.LineQubit.range(2)
    assert alphaclops.decompose(circuit_cls(alphaclops.X(a), alphaclops.Y(b), alphaclops.CZ(a, b))) == [
        alphaclops.X(a),
        alphaclops.Y(b),
        alphaclops.CZ(a, b),
    ]


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_measurement_key_mapping(circuit_cls):
    a, b = alphaclops.LineQubit.range(2)
    c = circuit_cls(alphaclops.X(a), alphaclops.measure(a, key='m1'), alphaclops.measure(b, key='m2'))
    assert c.all_measurement_key_names() == {'m1', 'm2'}

    assert alphaclops.with_measurement_key_mapping(c, {'m1': 'p1'}).all_measurement_key_names() == {
        'p1',
        'm2',
    }

    assert alphaclops.with_measurement_key_mapping(
        c, {'m1': 'p1', 'm2': 'p2'}
    ).all_measurement_key_names() == {'p1', 'p2'}

    c_swapped = alphaclops.with_measurement_key_mapping(c, {'m1': 'm2', 'm2': 'm1'})
    assert c_swapped.all_measurement_key_names() == {'m1', 'm2'}

    # Verify that the keys were actually swapped.
    simulator = alphaclops.Simulator()
    assert simulator.run(c).measurements == {'m1': 1, 'm2': 0}
    assert simulator.run(c_swapped).measurements == {'m1': 0, 'm2': 1}

    assert alphaclops.with_measurement_key_mapping(c, {'x': 'z'}).all_measurement_key_names() == {
        'm1',
        'm2',
    }


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_measurement_key_mapping_preserves_moments(circuit_cls):
    a, b = alphaclops.LineQubit.range(2)
    c = circuit_cls(
        alphaclops.Moment(alphaclops.X(a)),
        alphaclops.Moment(),
        alphaclops.Moment(alphaclops.measure(a, key='m1')),
        alphaclops.Moment(alphaclops.measure(b, key='m2')),
    )

    key_map = {'m1': 'p1'}
    remapped_circuit = alphaclops.with_measurement_key_mapping(c, key_map)
    assert list(remapped_circuit.moments) == [
        alphaclops.with_measurement_key_mapping(moment, key_map) for moment in c.moments
    ]


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_inverse(circuit_cls):
    a, b = alphaclops.LineQubit.range(2)
    forward = circuit_cls((alphaclops.X ** 0.5)(a), (alphaclops.Y ** -0.2)(b), alphaclops.CZ(a, b))
    backward = circuit_cls((alphaclops.CZ ** (-1.0))(a, b), (alphaclops.X ** (-0.5))(a), (alphaclops.Y ** (0.2))(b))
    alphaclops.testing.assert_same_circuits(alphaclops.inverse(forward), backward)

    alphaclops.testing.assert_same_circuits(alphaclops.inverse(circuit_cls()), circuit_cls())

    no_inverse = circuit_cls(alphaclops.measure(a, b))
    with pytest.raises(TypeError, match='__pow__'):
        alphaclops.inverse(no_inverse)

    # Default when there is no inverse for an op.
    default = circuit_cls((alphaclops.X ** 0.5)(a), (alphaclops.Y ** -0.2)(b))
    alphaclops.testing.assert_same_circuits(alphaclops.inverse(no_inverse, default), default)
    assert alphaclops.inverse(no_inverse, None) is None


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_pow_valid_only_for_minus_1(circuit_cls):
    a, b = alphaclops.LineQubit.range(2)
    forward = circuit_cls((alphaclops.X ** 0.5)(a), (alphaclops.Y ** -0.2)(b), alphaclops.CZ(a, b))

    backward = circuit_cls((alphaclops.CZ ** (-1.0))(a, b), (alphaclops.X ** (-0.5))(a), (alphaclops.Y ** (0.2))(b))
    alphaclops.testing.assert_same_circuits(alphaclops.pow(forward, -1), backward)
    with pytest.raises(TypeError, match='__pow__'):
        alphaclops.pow(forward, 1)
    with pytest.raises(TypeError, match='__pow__'):
        alphaclops.pow(forward, 0)
    with pytest.raises(TypeError, match='__pow__'):
        alphaclops.pow(forward, -2.5)


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_moment_groups(circuit_cls):
    qubits = [alphaclops.TensorCircuit(x, y) for x in range(8) for y in range(8)]
    c0 = alphaclops.H(qubits[0])
    c7 = alphaclops.H(qubits[7])
    cz14 = alphaclops.CZ(qubits[1], qubits[4])
    cz25 = alphaclops.CZ(qubits[2], qubits[5])
    cz36 = alphaclops.CZ(qubits[3], qubits[6])
    moment1 = alphaclops.Moment([c0, cz14, cz25, c7])
    moment2 = alphaclops.Moment([c0, cz14, cz25, cz36, c7])
    moment3 = alphaclops.Moment([cz14, cz25, cz36])
    moment4 = alphaclops.Moment([cz25, cz36])
    circuit = circuit_cls((moment1, moment2, moment3, moment4))
    alphaclops.testing.assert_has_diagram(
        circuit,
        r"""
           ┌──┐   ┌───┐   ┌───┐   ┌──┐
(0, 0): ────H──────H─────────────────────

(0, 1): ────@──────@───────@─────────────
            │      │       │
(0, 2): ────┼@─────┼@──────┼@──────@─────
            ││     ││      ││      │
(0, 3): ────┼┼─────┼┼@─────┼┼@─────┼@────
            ││     │││     │││     ││
(0, 4): ────@┼─────@┼┼─────@┼┼─────┼┼────
             │      ││      ││     ││
(0, 5): ─────@──────@┼──────@┼─────@┼────
                     │       │      │
(0, 6): ─────────────@───────@──────@────

(0, 7): ────H──────H─────────────────────
           └──┘   └───┘   └───┘   └──┘
""",
        use_unicode_characters=True,
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_moments_property(circuit_cls):
    q = alphaclops.NamedQubit('q')
    c = circuit_cls(alphaclops.X(q), alphaclops.Y(q))
    assert c.moments[0] == alphaclops.Moment([alphaclops.X(q)])
    assert c.moments[1] == alphaclops.Moment([alphaclops.Y(q)])


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_json_dict(circuit_cls):
    q0, q1 = alphaclops.LineQubit.range(2)
    c = circuit_cls(alphaclops.CNOT(q0, q1))
    moments = [alphaclops.Moment([alphaclops.CNOT(q0, q1)])]
    if circuit_cls == alphaclops.FrozenCircuit:
        moments = tuple(moments)
    assert c._json_dict_() == {'moments': moments}


def test_with_noise():
    class Noise(alphaclops.NoiseModel):
        def noisy_operation(self, operation):
            yield operation
            if alphaclops.LineQubit(0) in operation.qubits:
                yield alphaclops.H(alphaclops.LineQubit(0))

    q0, q1 = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.X(q0), alphaclops.Y(q1), alphaclops.Z(q1), alphaclops.Moment([alphaclops.X(q0)]))
    c_expected = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(q0), alphaclops.Y(q1)]),
            alphaclops.Moment([alphaclops.H(q0)]),
            alphaclops.Moment([alphaclops.Z(q1)]),
            alphaclops.Moment([alphaclops.X(q0)]),
            alphaclops.Moment([alphaclops.H(q0)]),
        ]
    )
    c_noisy = c.with_noise(Noise())
    assert c_noisy == c_expected

    # Accepts NOISE_MODEL_LIKE.
    assert c.with_noise(None) == c
    assert c.with_noise(alphaclops.depolarize(0.1)) == alphaclops.Circuit(
        alphaclops.X(q0),
        alphaclops.Y(q1),
        alphaclops.Moment([d.with_tags(ops.VirtualTag()) for d in alphaclops.depolarize(0.1).on_each(q0, q1)]),
        alphaclops.Z(q1),
        alphaclops.Moment([d.with_tags(ops.VirtualTag()) for d in alphaclops.depolarize(0.1).on_each(q0, q1)]),
        alphaclops.Moment([alphaclops.X(q0)]),
        alphaclops.Moment([d.with_tags(ops.VirtualTag()) for d in alphaclops.depolarize(0.1).on_each(q0, q1)]),
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_init_contents(circuit_cls):
    a, b = alphaclops.LineQubit.range(2)

    # Moments are not subject to insertion rules.
    c = circuit_cls(
        alphaclops.Moment([alphaclops.H(a)]), alphaclops.Moment([alphaclops.X(b)]), alphaclops.Moment([alphaclops.CNOT(a, b)])
    )
    assert len(c.moments) == 3

    # Earliest packing by default.
    c = circuit_cls(alphaclops.H(a), alphaclops.X(b), alphaclops.CNOT(a, b))
    assert c == circuit_cls(alphaclops.Moment([alphaclops.H(a), alphaclops.X(b)]), alphaclops.Moment([alphaclops.CNOT(a, b)]))

    # Packing can be controlled.
    c = circuit_cls(alphaclops.H(a), alphaclops.X(b), alphaclops.CNOT(a, b), strategy=alphaclops.InsertStrategy.NEW)
    assert c == circuit_cls(
        alphaclops.Moment([alphaclops.H(a)]), alphaclops.Moment([alphaclops.X(b)]), alphaclops.Moment([alphaclops.CNOT(a, b)])
    )

    circuit_cls()


def test_transform_qubits():
    a, b, c = alphaclops.LineQubit.range(3)
    original = alphaclops.Circuit(
        alphaclops.X(a), alphaclops.CNOT(a, b), alphaclops.Moment(), alphaclops.Moment([alphaclops.CNOT(b, c)])
    )
    x, y, z = alphaclops.TensorCircuit.rect(3, 1, 10, 20)
    desired = alphaclops.Circuit(
        alphaclops.X(x), alphaclops.CNOT(x, y), alphaclops.Moment(), alphaclops.Moment([alphaclops.CNOT(y, z)])
    )
    assert original.transform_qubits(lambda q: alphaclops.TensorCircuit(10 + q.x, 20)) == desired
    assert (
        original.transform_qubits(
            {
                a: alphaclops.TensorCircuit(10 + a.x, 20),
                b: alphaclops.TensorCircuit(10 + b.x, 20),
                c: alphaclops.TensorCircuit(10 + c.x, 20),
            }
        )
        == desired
    )
    with pytest.raises(TypeError, match='must be a function or dict'):
        _ = original.transform_qubits('bad arg')


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_indexing_by_pair(circuit_cls):
    # 0: ───H───@───X───@───
    #           │       │
    # 1: ───────H───@───@───
    #               │   │
    # 2: ───────────H───X───
    q = alphaclops.LineQubit.range(3)
    c = circuit_cls(
        [
            alphaclops.H(q[0]),
            alphaclops.H(q[1]).controlled_by(q[0]),
            alphaclops.H(q[2]).controlled_by(q[1]),
            alphaclops.X(q[0]),
            alphaclops.CCNOT(*q),
        ]
    )

    # Indexing by single moment and qubit.
    assert c[0, q[0]] == c[0][q[0]] == alphaclops.H(q[0])
    assert c[1, q[0]] == c[1, q[1]] == alphaclops.H(q[1]).controlled_by(q[0])
    assert c[2, q[0]] == c[2][q[0]] == alphaclops.X(q[0])
    assert c[2, q[1]] == c[2, q[2]] == alphaclops.H(q[2]).controlled_by(q[1])
    assert c[3, q[0]] == c[3, q[1]] == c[3, q[2]] == alphaclops.CCNOT(*q)

    # Indexing by moment and qubit - throws if there is no operation.
    with pytest.raises(KeyError, match="Moment doesn't act on given qubit"):
        _ = c[0, q[1]]

    # Indexing by single moment and multiple qubits.
    assert c[0, q] == c[0]
    assert c[1, q] == c[1]
    assert c[2, q] == c[2]
    assert c[3, q] == c[3]
    assert c[0, q[0:2]] == c[0]
    assert c[0, q[1:3]] == alphaclops.Moment([])
    assert c[1, q[1:2]] == c[1]
    assert c[2, [q[0]]] == alphaclops.Moment([alphaclops.X(q[0])])
    assert c[2, q[1:3]] == alphaclops.Moment([alphaclops.H(q[2]).controlled_by(q[1])])
    assert c[np.int64(2), q[0:2]] == c[2]

    # Indexing by single qubit.
    assert c[:, q[0]] == circuit_cls(
        [
            alphaclops.Moment([alphaclops.H(q[0])]),
            alphaclops.Moment([alphaclops.H(q[1]).controlled_by(q[0])]),
            alphaclops.Moment([alphaclops.X(q[0])]),
            alphaclops.Moment([alphaclops.CCNOT(q[0], q[1], q[2])]),
        ]
    )
    assert c[:, q[1]] == circuit_cls(
        [
            alphaclops.Moment([]),
            alphaclops.Moment([alphaclops.H(q[1]).controlled_by(q[0])]),
            alphaclops.Moment([alphaclops.H(q[2]).controlled_by(q[1])]),
            alphaclops.Moment([alphaclops.CCNOT(q[0], q[1], q[2])]),
        ]
    )
    assert c[:, q[2]] == circuit_cls(
        [
            alphaclops.Moment([]),
            alphaclops.Moment([]),
            alphaclops.Moment([alphaclops.H(q[2]).controlled_by(q[1])]),
            alphaclops.Moment([alphaclops.CCNOT(q[0], q[1], q[2])]),
        ]
    )

    # Indexing by several qubits.
    assert c[:, q] == c[:, q[0:2]] == c[:, [q[0], q[2]]] == c
    assert c[:, q[1:3]] == circuit_cls(
        [
            alphaclops.Moment([]),
            alphaclops.Moment([alphaclops.H(q[1]).controlled_by(q[0])]),
            alphaclops.Moment([alphaclops.H(q[2]).controlled_by(q[1])]),
            alphaclops.Moment([alphaclops.CCNOT(q[0], q[1], q[2])]),
        ]
    )

    # Indexing by several moments and one qubit.
    assert c[1:3, q[0]] == circuit_cls([alphaclops.H(q[1]).controlled_by(q[0]), alphaclops.X(q[0])])
    assert c[1::2, q[2]] == circuit_cls([alphaclops.Moment([]), alphaclops.Moment([alphaclops.CCNOT(*q)])])

    # Indexing by several moments and several qubits.
    assert c[0:2, q[1:3]] == circuit_cls(
        [alphaclops.Moment([]), alphaclops.Moment([alphaclops.H(q[1]).controlled_by(q[0])])]
    )
    assert c[::2, q[0:2]] == circuit_cls(
        [alphaclops.Moment([alphaclops.H(q[0])]), alphaclops.Moment([alphaclops.H(q[2]).controlled_by(q[1]), alphaclops.X(q[0])])]
    )

    # Equivalent ways of indexing.
    assert c[0:2, q[1:3]] == c[0:2][:, q[1:3]] == c[:, q[1:3]][0:2]

    # Passing more than 2 items is forbidden.
    with pytest.raises(ValueError, match='If key is tuple, it must be a pair.'):
        _ = c[0, q[1], 0]

    # Can't swap indices.
    with pytest.raises(TypeError, match='indices must be integers or slices'):
        _ = c[q[1], 0]


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_indexing_by_numpy_integer(circuit_cls):
    q = alphaclops.NamedQubit('q')
    c = circuit_cls(alphaclops.X(q), alphaclops.Y(q))

    assert c[np.int32(1)] == alphaclops.Moment([alphaclops.Y(q)])
    assert c[np.int64(1)] == alphaclops.Moment([alphaclops.Y(q)])


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_all_measurement_key_names(circuit_cls):
    class Unknown(alphaclops.testing.SingleQubitGate):
        def _measurement_key_name_(self):
            return 'test'

    a, b = alphaclops.LineQubit.range(2)
    c = circuit_cls(
        alphaclops.X(a),
        alphaclops.CNOT(a, b),
        alphaclops.measure(a, key='x'),
        alphaclops.measure(b, key='y'),
        alphaclops.reset(a),
        alphaclops.measure(a, b, key='xy'),
        Unknown().on(a),
    )

    # Big case.
    assert c.all_measurement_key_names() == {'x', 'y', 'xy', 'test'}
    assert c.all_measurement_key_names() == alphaclops.measurement_key_names(c)
    assert c.all_measurement_key_names() == c.all_measurement_key_objs()

    # Empty case.
    assert circuit_cls().all_measurement_key_names() == set()

    # Order does not matter.
    assert circuit_cls(
        alphaclops.Moment([alphaclops.measure(a, key='x'), alphaclops.measure(b, key='y')])
    ).all_measurement_key_names() == {'x', 'y'}
    assert circuit_cls(
        alphaclops.Moment([alphaclops.measure(b, key='y'), alphaclops.measure(a, key='x')])
    ).all_measurement_key_names() == {'x', 'y'}


def test_zip():
    a, b, c, d = alphaclops.LineQubit.range(4)

    circuit1 = alphaclops.Circuit(alphaclops.H(a), alphaclops.CNOT(a, b))
    circuit2 = alphaclops.Circuit(alphaclops.X(c), alphaclops.Y(c), alphaclops.Z(c))
    circuit3 = alphaclops.Circuit(alphaclops.Moment(), alphaclops.Moment(alphaclops.S(d)))

    # Calling works both static-style and instance-style.
    assert circuit1.zip(circuit2) == alphaclops.Circuit.zip(circuit1, circuit2)

    # Empty cases.
    assert alphaclops.Circuit.zip() == alphaclops.Circuit()
    assert alphaclops.Circuit.zip(alphaclops.Circuit()) == alphaclops.Circuit()
    assert alphaclops.Circuit().zip(alphaclops.Circuit()) == alphaclops.Circuit()
    assert circuit1.zip(alphaclops.Circuit()) == circuit1
    assert alphaclops.Circuit(alphaclops.Moment()).zip(alphaclops.Circuit()) == alphaclops.Circuit(alphaclops.Moment())
    assert alphaclops.Circuit().zip(alphaclops.Circuit(alphaclops.Moment())) == alphaclops.Circuit(alphaclops.Moment())

    # Small cases.
    assert (
            circuit1.zip(circuit2)
            == circuit2.zip(circuit1)
            == alphaclops.Circuit(
            alphaclops.Moment(alphaclops.H(a), alphaclops.X(c)),
            alphaclops.Moment(alphaclops.CNOT(a, b), alphaclops.Y(c)),
            alphaclops.Moment(alphaclops.Z(c)),
        )
    )
    assert circuit1.zip(circuit2, circuit3) == alphaclops.Circuit(
        alphaclops.Moment(alphaclops.H(a), alphaclops.X(c)),
        alphaclops.Moment(alphaclops.CNOT(a, b), alphaclops.Y(c), alphaclops.S(d)),
        alphaclops.Moment(alphaclops.Z(c)),
    )

    # Overlapping operations.
    with pytest.raises(ValueError, match="moment index 1.*\n.*CNOT"):
        _ = alphaclops.Circuit.zip(
            alphaclops.Circuit(alphaclops.X(a), alphaclops.CNOT(a, b)), alphaclops.Circuit(alphaclops.X(b), alphaclops.Z(b))
        )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_zip_alignment(circuit_cls):
    a, b, c = alphaclops.LineQubit.range(3)

    circuit1 = circuit_cls([alphaclops.H(a)] * 5)
    circuit2 = circuit_cls([alphaclops.H(b)] * 3)
    circuit3 = circuit_cls([alphaclops.H(c)] * 2)

    c_start = circuit_cls.zip(circuit1, circuit2, circuit3, align='LEFT')
    assert c_start == circuit_cls(
        alphaclops.Moment(alphaclops.H(a), alphaclops.H(b), alphaclops.H(c)),
        alphaclops.Moment(alphaclops.H(a), alphaclops.H(b), alphaclops.H(c)),
        alphaclops.Moment(alphaclops.H(a), alphaclops.H(b)),
        alphaclops.Moment(alphaclops.H(a)),
        alphaclops.Moment(alphaclops.H(a)),
    )

    c_end = circuit_cls.zip(circuit1, circuit2, circuit3, align='RIGHT')
    assert c_end == circuit_cls(
        alphaclops.Moment(alphaclops.H(a)),
        alphaclops.Moment(alphaclops.H(a)),
        alphaclops.Moment(alphaclops.H(a), alphaclops.H(b)),
        alphaclops.Moment(alphaclops.H(a), alphaclops.H(b), alphaclops.H(c)),
        alphaclops.Moment(alphaclops.H(a), alphaclops.H(b), alphaclops.H(c)),
    )


@pytest.mark.parametrize('circuit_cls', [alphaclops.Circuit, alphaclops.FrozenCircuit])
def test_repr_html_escaping(circuit_cls):
    class TestGate(alphaclops.Gate):
        def num_qubits(self):
            return 2

        def _circuit_diagram_info_(self, args):
            return alphaclops.CircuitDiagramInfo(wire_symbols=["< ' F ' >", "< ' F ' >"])

    F2 = TestGate()
    a = alphaclops.LineQubit(1)
    c = alphaclops.NamedQubit("|c>")

    circuit = circuit_cls([F2(a, c)])

    # Escaping Special Characters in Gate names.
    assert '&lt; &#x27; F &#x27; &gt;' in circuit._repr_html_()

    # Escaping Special Characters in Qubit names.
    assert '|c&gt;' in circuit._repr_html_()


def test_concat_ragged():
    a, b = alphaclops.LineQubit.range(2)
    empty = alphaclops.Circuit()

    assert alphaclops.Circuit.concat_ragged(empty, empty) == empty
    assert alphaclops.Circuit.concat_ragged() == empty
    assert empty.concat_ragged(empty) == empty
    assert empty.concat_ragged(empty, empty) == empty

    ha = alphaclops.Circuit(alphaclops.H(a))
    hb = alphaclops.Circuit(alphaclops.H(b))
    assert ha.concat_ragged(hb) == ha.zip(hb)

    assert ha.concat_ragged(empty) == ha
    assert empty.concat_ragged(ha) == ha

    hac = alphaclops.Circuit(alphaclops.H(a), alphaclops.CNOT(a, b))
    assert hac.concat_ragged(hb) == hac + hb
    assert hb.concat_ragged(hac) == hb.zip(hac)

    zig = alphaclops.Circuit(alphaclops.H(a), alphaclops.CNOT(a, b), alphaclops.H(b))
    assert zig.concat_ragged(zig) == alphaclops.Circuit(
        alphaclops.H(a), alphaclops.CNOT(a, b), alphaclops.Moment(alphaclops.H(a), alphaclops.H(b)), alphaclops.CNOT(a, b), alphaclops.H(b)
    )

    zag = alphaclops.Circuit(alphaclops.H(a), alphaclops.H(a), alphaclops.CNOT(a, b), alphaclops.H(b), alphaclops.H(b))
    assert zag.concat_ragged(zag) == alphaclops.Circuit(
        alphaclops.H(a),
        alphaclops.H(a),
        alphaclops.CNOT(a, b),
        alphaclops.Moment(alphaclops.H(a), alphaclops.H(b)),
        alphaclops.Moment(alphaclops.H(a), alphaclops.H(b)),
        alphaclops.CNOT(a, b),
        alphaclops.H(b),
        alphaclops.H(b),
    )

    space = alphaclops.Circuit(alphaclops.Moment()) * 10
    f = alphaclops.Circuit.concat_ragged
    assert len(f(space, ha)) == 10
    assert len(f(space, ha, ha, ha)) == 10
    assert len(f(space, f(ha, ha, ha))) == 10
    assert len(f(space, ha, align='LEFT')) == 10
    assert len(f(space, ha, ha, ha, align='RIGHT')) == 12
    assert len(f(space, f(ha, ha, ha, align='LEFT'))) == 10
    assert len(f(space, f(ha, ha, ha, align='RIGHT'))) == 10
    assert len(f(space, f(ha, ha, ha), align='LEFT')) == 10
    assert len(f(space, f(ha, ha, ha), align='RIGHT')) == 10

    # L shape overlap (vary c1).
    assert 7 == len(
        f(
            alphaclops.Circuit(alphaclops.CZ(a, b), [alphaclops.H(a)] * 5),
            alphaclops.Circuit([alphaclops.H(b)] * 5, alphaclops.CZ(a, b)),
        )
    )
    assert 7 == len(
        f(
            alphaclops.Circuit(alphaclops.CZ(a, b), [alphaclops.H(a)] * 4),
            alphaclops.Circuit([alphaclops.H(b)] * 5, alphaclops.CZ(a, b)),
        )
    )
    assert 7 == len(
        f(
            alphaclops.Circuit(alphaclops.CZ(a, b), [alphaclops.H(a)] * 1),
            alphaclops.Circuit([alphaclops.H(b)] * 5, alphaclops.CZ(a, b)),
        )
    )
    assert 8 == len(
        f(
            alphaclops.Circuit(alphaclops.CZ(a, b), [alphaclops.H(a)] * 6),
            alphaclops.Circuit([alphaclops.H(b)] * 5, alphaclops.CZ(a, b)),
        )
    )
    assert 9 == len(
        f(
            alphaclops.Circuit(alphaclops.CZ(a, b), [alphaclops.H(a)] * 7),
            alphaclops.Circuit([alphaclops.H(b)] * 5, alphaclops.CZ(a, b)),
        )
    )

    # L shape overlap (vary c2).
    assert 7 == len(
        f(
            alphaclops.Circuit(alphaclops.CZ(a, b), [alphaclops.H(a)] * 5),
            alphaclops.Circuit([alphaclops.H(b)] * 5, alphaclops.CZ(a, b)),
        )
    )
    assert 7 == len(
        f(
            alphaclops.Circuit(alphaclops.CZ(a, b), [alphaclops.H(a)] * 5),
            alphaclops.Circuit([alphaclops.H(b)] * 4, alphaclops.CZ(a, b)),
        )
    )
    assert 7 == len(
        f(
            alphaclops.Circuit(alphaclops.CZ(a, b), [alphaclops.H(a)] * 5),
            alphaclops.Circuit([alphaclops.H(b)] * 1, alphaclops.CZ(a, b)),
        )
    )
    assert 8 == len(
        f(
            alphaclops.Circuit(alphaclops.CZ(a, b), [alphaclops.H(a)] * 5),
            alphaclops.Circuit([alphaclops.H(b)] * 6, alphaclops.CZ(a, b)),
        )
    )
    assert 9 == len(
        f(
            alphaclops.Circuit(alphaclops.CZ(a, b), [alphaclops.H(a)] * 5),
            alphaclops.Circuit([alphaclops.H(b)] * 7, alphaclops.CZ(a, b)),
        )
    )

    # When scanning sees a possible hit, continues scanning for earlier hit.
    assert 10 == len(
        f(
            alphaclops.Circuit(
                alphaclops.Moment(),
                alphaclops.Moment(),
                alphaclops.Moment(),
                alphaclops.Moment(),
                alphaclops.Moment(),
                alphaclops.Moment(alphaclops.H(a)),
                alphaclops.Moment(),
                alphaclops.Moment(),
                alphaclops.Moment(alphaclops.H(b)),
            ),
            alphaclops.Circuit(
                alphaclops.Moment(),
                alphaclops.Moment(),
                alphaclops.Moment(),
                alphaclops.Moment(alphaclops.H(a)),
                alphaclops.Moment(),
                alphaclops.Moment(alphaclops.H(b)),
            ),
        )
    )
    # Correct tie breaker when one operation sees two possible hits.
    for cz_order in [alphaclops.CZ(a, b), alphaclops.CZ(b, a)]:
        assert 3 == len(
            f(
                alphaclops.Circuit(alphaclops.Moment(cz_order), alphaclops.Moment(), alphaclops.Moment()),
                alphaclops.Circuit(alphaclops.Moment(alphaclops.H(a)), alphaclops.Moment(alphaclops.H(b))),
            )
        )

    # Types.
    v = ha.freeze().concat_ragged(empty)
    assert type(v) is alphaclops.FrozenCircuit and v == ha.freeze()
    v = ha.concat_ragged(empty.freeze())
    assert type(v) is alphaclops.Circuit and v == ha
    v = ha.freeze().concat_ragged(empty)
    assert type(v) is alphaclops.FrozenCircuit and v == ha.freeze()
    v = alphaclops.Circuit.concat_ragged(ha, empty)
    assert type(v) is alphaclops.Circuit and v == ha
    v = alphaclops.FrozenCircuit.concat_ragged(ha, empty)
    assert type(v) is alphaclops.FrozenCircuit and v == ha.freeze()


def test_concat_ragged_alignment():
    a, b = alphaclops.LineQubit.range(2)

    assert alphaclops.Circuit.concat_ragged(
        alphaclops.Circuit(alphaclops.X(a)), alphaclops.Circuit(alphaclops.Y(b)) * 4, alphaclops.Circuit(alphaclops.Z(a)), align='first'
    ) == alphaclops.Circuit(
        alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b)),
        alphaclops.Moment(alphaclops.Y(b)),
        alphaclops.Moment(alphaclops.Y(b)),
        alphaclops.Moment(alphaclops.Z(a), alphaclops.Y(b)),
    )

    assert alphaclops.Circuit.concat_ragged(
        alphaclops.Circuit(alphaclops.X(a)), alphaclops.Circuit(alphaclops.Y(b)) * 4, alphaclops.Circuit(alphaclops.Z(a)), align='left'
    ) == alphaclops.Circuit(
        alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b)),
        alphaclops.Moment(alphaclops.Z(a), alphaclops.Y(b)),
        alphaclops.Moment(alphaclops.Y(b)),
        alphaclops.Moment(alphaclops.Y(b)),
    )

    assert alphaclops.Circuit.concat_ragged(
        alphaclops.Circuit(alphaclops.X(a)), alphaclops.Circuit(alphaclops.Y(b)) * 4, alphaclops.Circuit(alphaclops.Z(a)), align='right'
    ) == alphaclops.Circuit(
        alphaclops.Moment(alphaclops.Y(b)),
        alphaclops.Moment(alphaclops.Y(b)),
        alphaclops.Moment(alphaclops.Y(b)),
        alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b)),
        alphaclops.Moment(alphaclops.Z(a)),
    )


def test_freeze_not_relocate_moments():
    q = alphaclops.q(0)
    c = alphaclops.Circuit(alphaclops.X(q), alphaclops.measure(q))
    f = c.freeze()
    assert [mc is fc for mc, fc in zip(c, f)] == [True, True]


def test_factorize_one_factor():
    circuit = alphaclops.Circuit()
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    circuit.append(
        [alphaclops.Moment([alphaclops.CZ(q0, q1), alphaclops.H(q2)]), alphaclops.Moment([alphaclops.H(q0), alphaclops.CZ(q1, q2)])]
    )
    factors = list(circuit.factorize())
    assert len(factors) == 1
    assert factors[0] == circuit
    desired = """
0: ───@───H───
      │
1: ───@───@───
          │
2: ───H───@───
"""
    alphaclops.testing.assert_has_diagram(factors[0], desired)


def test_factorize_simple_circuit_two_factors():
    circuit = alphaclops.Circuit()
    q0, q1, q2 = alphaclops.LineQubit.range(3)
    circuit.append([alphaclops.H(q1), alphaclops.CZ(q0, q1), alphaclops.H(q2), alphaclops.H(q0), alphaclops.H(q0)])
    factors = list(circuit.factorize())
    assert len(factors) == 2
    desired = [
        """
0: ───────@───H───H───
          │
1: ───H───@───────────
""",
        """
2: ───H───────────────
""",
    ]
    for f, d in zip(factors, desired):
        alphaclops.testing.assert_has_diagram(f, d)


def test_factorize_large_circuit():
    circuit = alphaclops.Circuit()
    qubits = alphaclops.TensorCircuit.rect(3, 3)
    circuit.append(alphaclops.Moment(alphaclops.X(q) for q in qubits))
    pairset = [[(0, 2), (4, 6)], [(1, 2), (4, 8)]]
    for pairs in pairset:
        circuit.append(alphaclops.Moment(alphaclops.CZ(qubits[a], qubits[b]) for (a, b) in pairs))
    circuit.append(alphaclops.Moment(alphaclops.Y(q) for q in qubits))
    # expect 5 factors
    factors = list(circuit.factorize())
    desired = [
        """
(0, 0): ───X───@───────Y───
               │
(0, 1): ───X───┼───@───Y───
               │   │
(0, 2): ───X───@───@───Y───
""",
        """
(1, 0): ───X───────────Y───
""",
        """
(1, 1): ───X───@───@───Y───
               │   │
(2, 0): ───X───@───┼───Y───
                   │
(2, 2): ───X───────@───Y───
""",
        """
(1, 2): ───X───────────Y───
""",
        """
(2, 1): ───X───────────Y───
    """,
    ]
    assert len(factors) == 5
    for f, d in zip(factors, desired):
        alphaclops.testing.assert_has_diagram(f, d)


def test_zero_target_operations_go_below_diagram():
    class CustomOperationAnnotation(alphaclops.Operation):
        def __init__(self, text: str):
            self.text = text

        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

        @property
        def qubits(self):
            return ()

        def _circuit_diagram_info_(self, args) -> str:
            return self.text

    class CustomOperationAnnotationNoInfo(alphaclops.Operation):
        def with_qubits(self, *new_qubits):
            raise NotImplementedError()

        @property
        def qubits(self):
            return ()

        def __str__(self):
            return "custom!"

    class CustomGateAnnotation(alphaclops.Gate):
        def __init__(self, text: str):
            self.text = text

        def _num_qubits_(self):
            return 0

        def _circuit_diagram_info_(self, args) -> str:
            return self.text

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            alphaclops.Moment(
                CustomOperationAnnotation("a"),
                CustomGateAnnotation("b").on(),
                CustomOperationAnnotation("c"),
            ),
            alphaclops.Moment(CustomOperationAnnotation("e"), CustomOperationAnnotation("d")),
        ),
        """
    a   e
    b   d
    c
    """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            alphaclops.Moment(
                alphaclops.H(alphaclops.LineQubit(0)),
                CustomOperationAnnotation("a"),
                alphaclops.global_phase_operation(1j),
            )
        ),
        """
0: ─────────────H──────

global phase:   0.5π
                a
    """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            alphaclops.Moment(
                alphaclops.H(alphaclops.LineQubit(0)),
                alphaclops.CircuitOperation(alphaclops.FrozenCircuit(CustomOperationAnnotation("a"))),
            )
        ),
        """
0: ───H───
      a
        """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(
            alphaclops.Moment(
                alphaclops.X(alphaclops.LineQubit(0)),
                CustomOperationAnnotation("a"),
                CustomGateAnnotation("b").on(),
                CustomOperationAnnotation("c"),
            ),
            alphaclops.Moment(CustomOperationAnnotation("eee"), CustomOperationAnnotation("d")),
            alphaclops.Moment(
                alphaclops.CNOT(alphaclops.LineQubit(0), alphaclops.LineQubit(2)),
                alphaclops.CNOT(alphaclops.LineQubit(1), alphaclops.LineQubit(3)),
                CustomOperationAnnotationNoInfo(),
                CustomOperationAnnotation("zzz"),
            ),
            alphaclops.Moment(alphaclops.H(alphaclops.LineQubit(2))),
        ),
        """
                ┌────────┐
0: ───X──────────@───────────────
                 │
1: ──────────────┼──────@────────
                 │      │
2: ──────────────X──────┼────H───
                        │
3: ─────────────────────X────────
      a   eee    custom!
      b   d      zzz
      c
                └────────┘
    """,
    )


def test_create_speed():
    # Added in https://github.com/quantumlib/alphaclops/pull/5332
    # Previously this took ~30s to run. Now it should take ~150ms. However the coverage test can
    # run this slowly, so allowing 2 sec to account for things like that. Feel free to increase the
    # buffer time or delete the test entirely if it ends up causing flakes.
    #
    # Updated in https://github.com/quantumlib/alphaclops/pull/5756
    # After several tiny overtime failures of the GitHub CI Pytest MacOS (3.7)
    # the timeout was increased to 4 sec.  A more thorough investigation or test
    # removal should be considered if this continues to time out.
    qs = 100
    moments = 500
    xs = [alphaclops.X(alphaclops.LineQubit(i)) for i in range(qs)]
    opa = [xs[i] for i in range(qs) for _ in range(moments)]
    t = time.perf_counter()
    c = alphaclops.Circuit(opa)
    assert len(c) == moments
    assert time.perf_counter() - t < 4
