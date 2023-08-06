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
import alphaclops.testing


def test_validation():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')
    d = alphaclops.NamedQubit('d')

    _ = alphaclops.Moment([])
    _ = alphaclops.Moment([alphaclops.X(a)])
    _ = alphaclops.Moment([alphaclops.CZ(a, b)])
    _ = alphaclops.Moment([alphaclops.CZ(b, d)])
    _ = alphaclops.Moment([alphaclops.CZ(a, b), alphaclops.CZ(c, d)])
    _ = alphaclops.Moment([alphaclops.CZ(a, c), alphaclops.CZ(b, d)])
    _ = alphaclops.Moment([alphaclops.CZ(a, c), alphaclops.X(b)])

    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.X(a), alphaclops.X(a)])
    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.CZ(a, c), alphaclops.X(c)])
    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.CZ(a, c), alphaclops.CZ(c, d)])


def test_equality():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')
    d = alphaclops.NamedQubit('d')

    eq = alphaclops.testing.EqualsTester()

    # Default is empty. Iterables get frozen into tuples.
    eq.add_equality_group(alphaclops.Moment(), alphaclops.Moment([]), alphaclops.Moment(()))
    eq.add_equality_group(alphaclops.Moment([alphaclops.X(d)]), alphaclops.Moment((alphaclops.X(d),)))

    # Equality depends on gate and qubits.
    eq.add_equality_group(alphaclops.Moment([alphaclops.X(a)]))
    eq.add_equality_group(alphaclops.Moment([alphaclops.X(b)]))
    eq.add_equality_group(alphaclops.Moment([alphaclops.Y(a)]))

    # Equality doesn't depend on order.
    eq.add_equality_group(alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]), alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]))

    # Two qubit gates.
    eq.make_equality_group(lambda: alphaclops.Moment([alphaclops.CZ(c, d)]))
    eq.make_equality_group(lambda: alphaclops.Moment([alphaclops.CZ(a, c)]))
    eq.make_equality_group(lambda: alphaclops.Moment([alphaclops.CZ(a, b), alphaclops.CZ(c, d)]))
    eq.make_equality_group(lambda: alphaclops.Moment([alphaclops.CZ(a, c), alphaclops.CZ(b, d)]))


def test_approx_eq():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    assert not alphaclops.approx_eq(alphaclops.Moment([alphaclops.X(a)]), alphaclops.X(a))

    # Default is empty. Iterables get frozen into tuples.
    assert alphaclops.approx_eq(alphaclops.Moment(), alphaclops.Moment([]))
    assert alphaclops.approx_eq(alphaclops.Moment([]), alphaclops.Moment(()))

    assert alphaclops.approx_eq(alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(a)]))
    assert not alphaclops.approx_eq(alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment([alphaclops.X(b)]))

    assert alphaclops.approx_eq(
        alphaclops.Moment([alphaclops.XPowGate(exponent=0)(a)]), alphaclops.Moment([alphaclops.XPowGate(exponent=1e-9)(a)])
    )
    assert not alphaclops.approx_eq(
        alphaclops.Moment([alphaclops.XPowGate(exponent=0)(a)]), alphaclops.Moment([alphaclops.XPowGate(exponent=1e-7)(a)])
    )
    assert alphaclops.approx_eq(
        alphaclops.Moment([alphaclops.XPowGate(exponent=0)(a)]),
        alphaclops.Moment([alphaclops.XPowGate(exponent=1e-7)(a)]),
        atol=1e-6,
    )


def test_operates_on_single_qubit():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')

    # Empty case.
    assert not alphaclops.Moment().operates_on_single_qubit(a)
    assert not alphaclops.Moment().operates_on_single_qubit(b)

    # One-qubit operation case.
    assert alphaclops.Moment([alphaclops.X(a)]).operates_on_single_qubit(a)
    assert not alphaclops.Moment([alphaclops.X(a)]).operates_on_single_qubit(b)

    # Two-qubit operation case.
    assert alphaclops.Moment([alphaclops.CZ(a, b)]).operates_on_single_qubit(a)
    assert alphaclops.Moment([alphaclops.CZ(a, b)]).operates_on_single_qubit(b)
    assert not alphaclops.Moment([alphaclops.CZ(a, b)]).operates_on_single_qubit(c)

    # Multiple operations case.
    assert alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).operates_on_single_qubit(a)
    assert alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).operates_on_single_qubit(b)
    assert not alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).operates_on_single_qubit(c)


def test_operates_on():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')

    # Empty case.
    assert not alphaclops.Moment().operates_on([])
    assert not alphaclops.Moment().operates_on([a])
    assert not alphaclops.Moment().operates_on([b])
    assert not alphaclops.Moment().operates_on([a, b])

    # One-qubit operation case.
    assert not alphaclops.Moment([alphaclops.X(a)]).operates_on([])
    assert alphaclops.Moment([alphaclops.X(a)]).operates_on([a])
    assert not alphaclops.Moment([alphaclops.X(a)]).operates_on([b])
    assert alphaclops.Moment([alphaclops.X(a)]).operates_on([a, b])

    # Two-qubit operation case.
    assert not alphaclops.Moment([alphaclops.CZ(a, b)]).operates_on([])
    assert alphaclops.Moment([alphaclops.CZ(a, b)]).operates_on([a])
    assert alphaclops.Moment([alphaclops.CZ(a, b)]).operates_on([b])
    assert alphaclops.Moment([alphaclops.CZ(a, b)]).operates_on([a, b])
    assert not alphaclops.Moment([alphaclops.CZ(a, b)]).operates_on([c])
    assert alphaclops.Moment([alphaclops.CZ(a, b)]).operates_on([a, c])
    assert alphaclops.Moment([alphaclops.CZ(a, b)]).operates_on([a, b, c])

    # Multiple operations case.
    assert not alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).operates_on([])
    assert alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).operates_on([a])
    assert alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).operates_on([b])
    assert alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).operates_on([a, b])
    assert not alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).operates_on([c])
    assert alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).operates_on([a, c])
    assert alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).operates_on([a, b, c])


def test_operation_at():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')

    # No operation on that qubit
    assert alphaclops.Moment().operation_at(a) is None

    # One Operation on the quibt
    assert alphaclops.Moment([alphaclops.X(a)]).operation_at(a) == alphaclops.X(a)

    # Multiple Operations on the qubits
    assert alphaclops.Moment([alphaclops.CZ(a, b), alphaclops.X(c)]).operation_at(a) == alphaclops.CZ(a, b)


def test_from_ops():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    assert alphaclops.Moment.from_ops(alphaclops.X(a), alphaclops.Y(b)) == alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b))


def test_with_operation():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    assert alphaclops.Moment().with_operation(alphaclops.X(a)) == alphaclops.Moment([alphaclops.X(a)])

    assert alphaclops.Moment([alphaclops.X(a)]).with_operation(alphaclops.X(b)) == alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)])

    # One-qubit operation case.
    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.X(a)]).with_operation(alphaclops.X(a))

    # Two-qubit operation case.
    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.CZ(a, b)]).with_operation(alphaclops.X(a))
    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.CZ(a, b)]).with_operation(alphaclops.X(b))

    # Multiple operations case.
    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).with_operation(alphaclops.X(a))
    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).with_operation(alphaclops.X(b))


def test_with_operations():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')

    assert alphaclops.Moment().with_operations(alphaclops.X(a)) == alphaclops.Moment([alphaclops.X(a)])
    assert alphaclops.Moment().with_operations(alphaclops.X(a), alphaclops.X(b)) == alphaclops.Moment(
        [alphaclops.X(a), alphaclops.X(b)]
    )

    assert alphaclops.Moment([alphaclops.X(a)]).with_operations(alphaclops.X(b)) == alphaclops.Moment(
        [alphaclops.X(a), alphaclops.X(b)]
    )
    assert alphaclops.Moment([alphaclops.X(a)]).with_operations(alphaclops.X(b), alphaclops.X(c)) == alphaclops.Moment(
        [alphaclops.X(a), alphaclops.X(b), alphaclops.X(c)]
    )

    # One-qubit operation case.
    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.X(a)]).with_operations(alphaclops.X(a))

    # Two-qubit operation case.
    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.CZ(a, b)]).with_operations(alphaclops.X(a))
    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.CZ(a, b)]).with_operations(alphaclops.X(b))

    # Multiple operations case.
    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).with_operations(alphaclops.X(a))
    with pytest.raises(ValueError):
        _ = alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).with_operations(alphaclops.X(b))


def test_without_operations_touching():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')

    # Empty case.
    assert alphaclops.Moment().without_operations_touching([]) == alphaclops.Moment()
    assert alphaclops.Moment().without_operations_touching([a]) == alphaclops.Moment()
    assert alphaclops.Moment().without_operations_touching([a, b]) == alphaclops.Moment()

    # One-qubit operation case.
    assert alphaclops.Moment([alphaclops.X(a)]).without_operations_touching([]) == alphaclops.Moment([alphaclops.X(a)])
    assert alphaclops.Moment([alphaclops.X(a)]).without_operations_touching([a]) == alphaclops.Moment()
    assert alphaclops.Moment([alphaclops.X(a)]).without_operations_touching([b]) == alphaclops.Moment([alphaclops.X(a)])

    # Two-qubit operation case.
    assert alphaclops.Moment([alphaclops.CZ(a, b)]).without_operations_touching([]) == alphaclops.Moment(
        [alphaclops.CZ(a, b)]
    )
    assert alphaclops.Moment([alphaclops.CZ(a, b)]).without_operations_touching([a]) == alphaclops.Moment()
    assert alphaclops.Moment([alphaclops.CZ(a, b)]).without_operations_touching([b]) == alphaclops.Moment()
    assert alphaclops.Moment([alphaclops.CZ(a, b)]).without_operations_touching([c]) == alphaclops.Moment(
        [alphaclops.CZ(a, b)]
    )

    # Multiple operation case.
    assert alphaclops.Moment([alphaclops.CZ(a, b), alphaclops.X(c)]).without_operations_touching([]) == alphaclops.Moment(
        [alphaclops.CZ(a, b), alphaclops.X(c)]
    )
    assert alphaclops.Moment([alphaclops.CZ(a, b), alphaclops.X(c)]).without_operations_touching([a]) == alphaclops.Moment(
        [alphaclops.X(c)]
    )
    assert alphaclops.Moment([alphaclops.CZ(a, b), alphaclops.X(c)]).without_operations_touching([b]) == alphaclops.Moment(
        [alphaclops.X(c)]
    )
    assert alphaclops.Moment([alphaclops.CZ(a, b), alphaclops.X(c)]).without_operations_touching([c]) == alphaclops.Moment(
        [alphaclops.CZ(a, b)]
    )
    assert alphaclops.Moment([alphaclops.CZ(a, b), alphaclops.X(c)]).without_operations_touching(
        [a, b]
    ) == alphaclops.Moment([alphaclops.X(c)])
    assert (
            alphaclops.Moment([alphaclops.CZ(a, b), alphaclops.X(c)]).without_operations_touching([a, c]) == alphaclops.Moment()
    )


def test_is_parameterized():
    a, b = alphaclops.LineQubit.range(2)
    moment = alphaclops.Moment(alphaclops.X(a) ** sympy.Symbol('v'), alphaclops.Y(b) ** sympy.Symbol('w'))
    assert alphaclops.is_parameterized(moment)
    assert not alphaclops.is_parameterized(alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b)))


def test_resolve_parameters():
    a, b = alphaclops.LineQubit.range(2)
    moment = alphaclops.Moment(alphaclops.X(a) ** sympy.Symbol('v'), alphaclops.Y(b) ** sympy.Symbol('w'))
    resolved_moment = alphaclops.resolve_parameters(moment, alphaclops.ParamResolver({'v': 0.1, 'w': 0.2}))
    assert resolved_moment == alphaclops.Moment(alphaclops.X(a) ** 0.1, alphaclops.Y(b) ** 0.2)


def test_resolve_parameters_no_change():
    a, b = alphaclops.LineQubit.range(2)
    moment = alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b))
    resolved_moment = alphaclops.resolve_parameters(moment, alphaclops.ParamResolver({'v': 0.1, 'w': 0.2}))
    assert resolved_moment is moment

    moment = alphaclops.Moment(alphaclops.X(a) ** sympy.Symbol('v'), alphaclops.Y(b) ** sympy.Symbol('w'))
    resolved_moment = alphaclops.resolve_parameters(moment, alphaclops.ParamResolver({}))
    assert resolved_moment is moment


def test_parameter_names():
    a, b = alphaclops.LineQubit.range(2)
    moment = alphaclops.Moment(alphaclops.X(a) ** sympy.Symbol('v'), alphaclops.Y(b) ** sympy.Symbol('w'))
    assert alphaclops.parameter_names(moment) == {'v', 'w'}
    assert alphaclops.parameter_names(alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b))) == set()


def test_with_measurement_keys():
    a, b = alphaclops.LineQubit.range(2)
    m = alphaclops.Moment(alphaclops.measure(a, key='m1'), alphaclops.measure(b, key='m2'))

    new_moment = alphaclops.with_measurement_key_mapping(m, {'m1': 'p1', 'm2': 'p2', 'x': 'z'})

    assert new_moment.operations[0] == alphaclops.measure(a, key='p1')
    assert new_moment.operations[1] == alphaclops.measure(b, key='p2')


def test_with_key_path():
    a, b = alphaclops.LineQubit.range(2)
    m = alphaclops.Moment(alphaclops.measure(a, key='m1'), alphaclops.measure(b, key='m2'))

    new_moment = alphaclops.with_key_path(m, ('a', 'b'))

    assert new_moment.operations[0] == alphaclops.measure(
        a, key=alphaclops.MeasurementKey.parse_serialized('a:b:m1')
    )
    assert new_moment.operations[1] == alphaclops.measure(
        b, key=alphaclops.MeasurementKey.parse_serialized('a:b:m2')
    )


def test_with_key_path_prefix():
    a, b, c = alphaclops.LineQubit.range(3)
    m = alphaclops.Moment(alphaclops.measure(a, key='m1'), alphaclops.measure(b, key='m2'), alphaclops.X(c))
    mb = alphaclops.with_key_path_prefix(m, ('b',))
    mab = alphaclops.with_key_path_prefix(mb, ('a',))
    assert mab.operations[0] == alphaclops.measure(a, key=alphaclops.MeasurementKey.parse_serialized('a:b:m1'))
    assert mab.operations[1] == alphaclops.measure(b, key=alphaclops.MeasurementKey.parse_serialized('a:b:m2'))
    assert mab.operations[2] is m.operations[2]


def test_copy():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    original = alphaclops.Moment([alphaclops.CZ(a, b)])
    copy = original.__copy__()
    assert original == copy
    assert id(original) != id(copy)


def test_qubits():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    assert alphaclops.Moment([alphaclops.X(a), alphaclops.X(b)]).qubits == {a, b}
    assert alphaclops.Moment([alphaclops.X(a)]).qubits == {a}
    assert alphaclops.Moment([alphaclops.CZ(a, b)]).qubits == {a, b}


def test_container_methods():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    m = alphaclops.Moment([alphaclops.H(a), alphaclops.H(b)])
    assert list(m) == list(m.operations)
    # __iter__
    assert list(iter(m)) == list(m.operations)
    # __contains__ for free.
    assert alphaclops.H(b) in m

    assert len(m) == 2


def test_decompose():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    m = alphaclops.Moment(alphaclops.X(a), alphaclops.X(b))
    assert list(alphaclops.decompose(m)) == list(m.operations)


def test_measurement_keys():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    m = alphaclops.Moment(alphaclops.X(a), alphaclops.X(b))
    assert alphaclops.measurement_key_names(m) == set()
    assert not alphaclops.is_measurement(m)

    m2 = alphaclops.Moment(alphaclops.measure(a, b, key='foo'))
    assert alphaclops.measurement_key_objs(m2) == {alphaclops.MeasurementKey('foo')}
    assert alphaclops.measurement_key_names(m2) == {'foo'}
    assert alphaclops.is_measurement(m2)


def test_measurement_key_objs_caching():
    q0, q1, q2, q3 = alphaclops.LineQubit.range(4)
    m = alphaclops.Moment(alphaclops.measure(q0, key='foo'))
    assert m._measurement_key_objs is None
    key_objs = alphaclops.measurement_key_objs(m)
    assert m._measurement_key_objs == key_objs

    # Make sure it gets updated when adding an operation.
    m = m.with_operation(alphaclops.measure(q1, key='bar'))
    assert m._measurement_key_objs == {
        alphaclops.MeasurementKey(name='bar'),
        alphaclops.MeasurementKey(name='foo'),
    }
    # Or multiple operations.
    m = m.with_operations(alphaclops.measure(q2, key='doh'), alphaclops.measure(q3, key='baz'))
    assert m._measurement_key_objs == {
        alphaclops.MeasurementKey(name='bar'),
        alphaclops.MeasurementKey(name='foo'),
        alphaclops.MeasurementKey(name='doh'),
        alphaclops.MeasurementKey(name='baz'),
    }


def test_control_keys_caching():
    q0, q1, q2, q3 = alphaclops.LineQubit.range(4)
    m = alphaclops.Moment(alphaclops.X(q0).with_classical_controls('foo'))
    assert m._control_keys is None
    keys = alphaclops.control_keys(m)
    assert m._control_keys == keys

    # Make sure it gets updated when adding an operation.
    m = m.with_operation(alphaclops.X(q1).with_classical_controls('bar'))
    assert m._control_keys == {alphaclops.MeasurementKey(name='bar'), alphaclops.MeasurementKey(name='foo')}
    # Or multiple operations.
    m = m.with_operations(
        alphaclops.X(q2).with_classical_controls('doh'), alphaclops.X(q3).with_classical_controls('baz')
    )
    assert m._control_keys == {
        alphaclops.MeasurementKey(name='bar'),
        alphaclops.MeasurementKey(name='foo'),
        alphaclops.MeasurementKey(name='doh'),
        alphaclops.MeasurementKey(name='baz'),
    }


def test_bool():
    assert not alphaclops.Moment()
    a = alphaclops.NamedQubit('a')
    assert alphaclops.Moment([alphaclops.X(a)])


def test_repr():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')

    alphaclops.testing.assert_equivalent_repr(alphaclops.Moment())
    alphaclops.testing.assert_equivalent_repr(alphaclops.Moment(alphaclops.CZ(a, b)))
    alphaclops.testing.assert_equivalent_repr(alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b)))


def test_json_dict():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    mom = alphaclops.Moment([alphaclops.CZ(a, b)])
    assert mom._json_dict_() == {'operations': (alphaclops.CZ(a, b),)}


def test_inverse():
    a, b, c = alphaclops.LineQubit.range(3)
    m = alphaclops.Moment([alphaclops.S(a), alphaclops.CNOT(b, c)])
    assert m**1 is m
    assert m ** -1 == alphaclops.Moment([alphaclops.S(a) ** -1, alphaclops.CNOT(b, c)])
    assert m ** 0.5 == alphaclops.Moment([alphaclops.T(a), alphaclops.CNOT(b, c) ** 0.5])
    assert alphaclops.inverse(m) == m ** -1
    assert alphaclops.inverse(alphaclops.inverse(m)) == m
    assert alphaclops.inverse(alphaclops.Moment([alphaclops.measure(a)]), default=None) is None


def test_immutable_moment():
    with pytest.raises(AttributeError):
        q1, q2 = alphaclops.LineQubit.range(2)
        circuit = alphaclops.Circuit(alphaclops.X(q1))
        moment = circuit.moments[0]
        moment.operations += (alphaclops.Y(q2),)


def test_add():
    a, b, c = alphaclops.LineQubit.range(3)
    expected_circuit = alphaclops.Circuit([alphaclops.CNOT(a, b), alphaclops.X(a), alphaclops.Y(b)])

    circuit1 = alphaclops.Circuit([alphaclops.CNOT(a, b), alphaclops.X(a)])
    circuit1[1] += alphaclops.Y(b)
    assert circuit1 == expected_circuit

    circuit2 = alphaclops.Circuit(alphaclops.CNOT(a, b), alphaclops.Y(b))
    circuit2[1] += alphaclops.X(a)
    assert circuit2 == expected_circuit

    m1 = alphaclops.Moment([alphaclops.X(a)])
    m2 = alphaclops.Moment([alphaclops.CNOT(a, b)])
    m3 = alphaclops.Moment([alphaclops.X(c)])
    assert m1 + m3 == alphaclops.Moment([alphaclops.X(a), alphaclops.X(c)])
    assert m2 + m3 == alphaclops.Moment([alphaclops.CNOT(a, b), alphaclops.X(c)])
    with pytest.raises(ValueError, match='Overlap'):
        _ = m1 + m2

    assert m1 + [[[[alphaclops.Y(b)]]]] == alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b))
    assert m1 + [] == m1
    assert m1 + [] is m1


def test_sub():
    a, b, c = alphaclops.LineQubit.range(3)
    m = alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b))
    assert m - [] == m
    assert m - alphaclops.X(a) == alphaclops.Moment(alphaclops.Y(b))
    assert m - [[[[alphaclops.X(a)]], []]] == alphaclops.Moment(alphaclops.Y(b))
    assert m - [alphaclops.X(a), alphaclops.Y(b)] == alphaclops.Moment()
    assert m - [alphaclops.Y(b)] == alphaclops.Moment(alphaclops.X(a))

    with pytest.raises(ValueError, match="missing operations"):
        _ = m - alphaclops.X(b)
    with pytest.raises(ValueError, match="missing operations"):
        _ = m - [alphaclops.X(a), alphaclops.Z(c)]

    # Preserves relative order.
    m2 = alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b), alphaclops.Z(c))
    assert m2 - alphaclops.Y(b) == alphaclops.Moment(alphaclops.X(a), alphaclops.Z(c))


def test_op_tree():
    eq = alphaclops.testing.EqualsTester()
    a, b = alphaclops.LineQubit.range(2)

    eq.add_equality_group(alphaclops.Moment(), alphaclops.Moment([]), alphaclops.Moment([[], [[[]]]]))

    eq.add_equality_group(
        alphaclops.Moment(alphaclops.X(a)), alphaclops.Moment([alphaclops.X(a)]), alphaclops.Moment({alphaclops.X(a)})
    )

    eq.add_equality_group(alphaclops.Moment(alphaclops.X(a), alphaclops.Y(b)), alphaclops.Moment([alphaclops.X(a), alphaclops.Y(b)]))


def test_indexes_by_qubit():
    a, b, c = alphaclops.LineQubit.range(3)
    moment = alphaclops.Moment([alphaclops.H(a), alphaclops.CNOT(b, c)])

    assert moment[a] == alphaclops.H(a)
    assert moment[b] == alphaclops.CNOT(b, c)
    assert moment[c] == alphaclops.CNOT(b, c)


def test_throws_when_indexed_by_unused_qubit():
    a, b = alphaclops.LineQubit.range(2)
    moment = alphaclops.Moment([alphaclops.H(a)])

    with pytest.raises(KeyError, match="Moment doesn't act on given qubit"):
        _ = moment[b]


def test_indexes_by_list_of_qubits():
    q = alphaclops.LineQubit.range(4)
    moment = alphaclops.Moment([alphaclops.Z(q[0]), alphaclops.CNOT(q[1], q[2])])

    assert moment[[q[0]]] == alphaclops.Moment([alphaclops.Z(q[0])])
    assert moment[[q[1]]] == alphaclops.Moment([alphaclops.CNOT(q[1], q[2])])
    assert moment[[q[2]]] == alphaclops.Moment([alphaclops.CNOT(q[1], q[2])])
    assert moment[[q[3]]] == alphaclops.Moment([])
    assert moment[q[0:2]] == moment
    assert moment[q[1:3]] == alphaclops.Moment([alphaclops.CNOT(q[1], q[2])])
    assert moment[q[2:4]] == alphaclops.Moment([alphaclops.CNOT(q[1], q[2])])
    assert moment[[q[0], q[3]]] == alphaclops.Moment([alphaclops.Z(q[0])])
    assert moment[q] == moment


def test_moment_text_diagram():
    a, b, c, d = alphaclops.TensorCircuit.rect(2, 2)
    m = alphaclops.Moment(alphaclops.CZ(a, b), alphaclops.CNOT(c, d))
    assert (
        str(m).strip()
        == """
  ╷ 0 1
╶─┼─────
0 │ @─@
  │
1 │ @─X
  │
    """.strip()
    )

    m = alphaclops.Moment(alphaclops.CZ(a, b), alphaclops.CNOT(c, d))
    alphaclops.testing.assert_has_diagram(
        m,
        """
   ╷ None 0 1
╶──┼──────────
aa │
   │
0  │      @─@
   │
1  │      @─X
   │
        """,
        extra_qubits=[alphaclops.NamedQubit("aa")],
    )

    m = alphaclops.Moment(alphaclops.S(c), alphaclops.ISWAP(a, d))
    alphaclops.testing.assert_has_diagram(
        m,
        """
  ╷ 0     1
╶─┼─────────────
0 │ iSwap─┐
  │       │
1 │ S     iSwap
  │
    """,
    )

    m = alphaclops.Moment(alphaclops.S(c) ** 0.1, alphaclops.ISWAP(a, d) ** 0.5)
    alphaclops.testing.assert_has_diagram(
        m,
        """
  ╷ 0         1
╶─┼─────────────────
0 │ iSwap^0.5─┐
  │           │
1 │ Z^0.05    iSwap
  │
    """,
    )

    a, b, c = alphaclops.LineQubit.range(3)
    m = alphaclops.Moment(alphaclops.X(a), alphaclops.SWAP(b, c))
    alphaclops.testing.assert_has_diagram(
        m,
        """
  ╷ a b c
╶─┼───────
0 │ X
  │
1 │   ×─┐
  │     │
2 │     ×
  │
    """,
        xy_breakdown_func=lambda q: ('abc'[q.x], q.x),
    )

    class EmptyGate(alphaclops.testing.SingleQubitGate):
        def __str__(self):
            return 'Empty'

    m = alphaclops.Moment(EmptyGate().on(a))
    alphaclops.testing.assert_has_diagram(
        m,
        """
  ╷ 0
╶─┼───────
0 │ Empty
  │
    """,
    )


def test_text_diagram_does_not_depend_on_insertion_order():
    q = alphaclops.LineQubit.range(4)
    ops = [alphaclops.CNOT(q[0], q[3]), alphaclops.CNOT(q[1], q[2])]
    m1, m2 = alphaclops.Moment(ops), alphaclops.Moment(ops[::-1])
    assert m1 == m2
    assert str(m1) == str(m2)


def test_commutes():
    a = alphaclops.NamedQubit('a')
    b = alphaclops.NamedQubit('b')
    c = alphaclops.NamedQubit('c')
    d = alphaclops.NamedQubit('d')

    moment = alphaclops.Moment([alphaclops.X(a), alphaclops.Y(b), alphaclops.H(c)])

    assert NotImplemented == alphaclops.commutes(moment, a, default=NotImplemented)

    assert alphaclops.commutes(moment, alphaclops.X(a))
    assert alphaclops.commutes(moment, alphaclops.Y(b))
    assert alphaclops.commutes(moment, alphaclops.H(c))
    assert alphaclops.commutes(moment, alphaclops.H(d))

    # X and H do not commute
    assert not alphaclops.commutes(moment, alphaclops.H(a))
    assert not alphaclops.commutes(moment, alphaclops.H(b))
    assert not alphaclops.commutes(moment, alphaclops.X(c))


def test_transform_qubits():
    a, b = alphaclops.LineQubit.range(2)
    x, y = alphaclops.TensorCircuit.rect(2, 1, 10, 20)

    original = alphaclops.Moment([alphaclops.X(a), alphaclops.Y(b)])
    modified = alphaclops.Moment([alphaclops.X(x), alphaclops.Y(y)])

    assert original.transform_qubits({a: x, b: y}) == modified
    assert original.transform_qubits(lambda q: alphaclops.TensorCircuit(10 + q.x, 20)) == modified
    with pytest.raises(TypeError, match='must be a function or dict'):
        _ = original.transform_qubits('bad arg')


def test_expand_to():
    a, b = alphaclops.LineQubit.range(2)
    m1 = alphaclops.Moment(alphaclops.H(a))
    m2 = m1.expand_to({a})
    assert m1 == m2

    m3 = m1.expand_to({a, b})
    assert m1 != m3
    assert m3.qubits == {a, b}
    assert m3.operations == (alphaclops.H(a), alphaclops.I(b))

    with pytest.raises(ValueError, match='superset'):
        _ = m1.expand_to({b})


def test_kraus():
    I = np.eye(2)
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.diag([1, -1])

    a, b = alphaclops.LineQubit.range(2)

    m = alphaclops.Moment()
    assert alphaclops.has_kraus(m)
    k = alphaclops.kraus(m)
    assert len(k) == 1
    assert np.allclose(k[0], np.array([[1.0]]))

    m = alphaclops.Moment(alphaclops.S(a))
    assert alphaclops.has_kraus(m)
    k = alphaclops.kraus(m)
    assert len(k) == 1
    assert np.allclose(k[0], np.diag([1, 1j]))

    m = alphaclops.Moment(alphaclops.CNOT(a, b))
    assert alphaclops.has_kraus(m)
    k = alphaclops.kraus(m)
    assert len(k) == 1
    assert np.allclose(k[0], np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]))

    p = 0.1
    m = alphaclops.Moment(alphaclops.depolarize(p).on(a))
    assert alphaclops.has_kraus(m)
    k = alphaclops.kraus(m)
    assert len(k) == 4
    assert np.allclose(k[0], np.sqrt(1 - p) * I)
    assert np.allclose(k[1], np.sqrt(p / 3) * X)
    assert np.allclose(k[2], np.sqrt(p / 3) * Y)
    assert np.allclose(k[3], np.sqrt(p / 3) * Z)

    p = 0.2
    q = 0.3
    m = alphaclops.Moment(alphaclops.bit_flip(p).on(a), alphaclops.phase_flip(q).on(b))
    assert alphaclops.has_kraus(m)
    k = alphaclops.kraus(m)
    assert len(k) == 4
    assert np.allclose(k[0], np.sqrt((1 - p) * (1 - q)) * np.kron(I, I))
    assert np.allclose(k[1], np.sqrt(q * (1 - p)) * np.kron(I, Z))
    assert np.allclose(k[2], np.sqrt(p * (1 - q)) * np.kron(X, I))
    assert np.allclose(k[3], np.sqrt(p * q) * np.kron(X, Z))


def test_kraus_too_big():
    m = alphaclops.Moment(alphaclops.IdentityGate(11).on(*alphaclops.LineQubit.range(11)))
    assert not alphaclops.has_kraus(m)
    assert not m._has_superoperator_()
    assert m._kraus_() is NotImplemented
    assert m._superoperator_() is NotImplemented
    assert alphaclops.kraus(m, default=None) is None


def test_op_has_no_kraus():
    class EmptyGate(alphaclops.testing.SingleQubitGate):
        pass

    m = alphaclops.Moment(EmptyGate().on(alphaclops.NamedQubit("a")))
    assert not alphaclops.has_kraus(m)
    assert not m._has_superoperator_()
    assert m._kraus_() is NotImplemented
    assert m._superoperator_() is NotImplemented
    assert alphaclops.kraus(m, default=None) is None


def test_superoperator():
    cnot = alphaclops.unitary(alphaclops.CNOT)

    a, b = alphaclops.LineQubit.range(2)

    m = alphaclops.Moment()
    assert m._has_superoperator_()
    s = m._superoperator_()
    assert np.allclose(s, np.array([[1.0]]))

    m = alphaclops.Moment(alphaclops.I(a))
    assert m._has_superoperator_()
    s = m._superoperator_()
    assert np.allclose(s, np.eye(4))

    m = alphaclops.Moment(alphaclops.IdentityGate(2).on(a, b))
    assert m._has_superoperator_()
    s = m._superoperator_()
    assert np.allclose(s, np.eye(16))

    m = alphaclops.Moment(alphaclops.S(a))
    assert m._has_superoperator_()
    s = m._superoperator_()
    assert np.allclose(s, np.diag([1, -1j, 1j, 1]))

    m = alphaclops.Moment(alphaclops.CNOT(a, b))
    assert m._has_superoperator_()
    s = m._superoperator_()
    assert np.allclose(s, np.kron(cnot, cnot))

    m = alphaclops.Moment(alphaclops.depolarize(0.75).on(a))
    assert m._has_superoperator_()
    s = m._superoperator_()
    assert np.allclose(s, np.array([[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1]]) / 2)
