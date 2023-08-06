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


class ReturnsStr:
    def _measurement_key_name_(self):
        return 'door locker'


class ReturnsObj:
    def _measurement_key_obj_(self):
        return alphaclops.MeasurementKey(name='door locker')


@pytest.mark.parametrize('gate', [ReturnsStr(), ReturnsObj()])
def test_measurement_key_name(gate):
    assert isinstance(alphaclops.measurement_key_name(gate), str)
    assert alphaclops.measurement_key_name(gate) == 'door locker'
    assert alphaclops.measurement_key_obj(gate) == alphaclops.MeasurementKey(name='door locker')

    assert alphaclops.measurement_key_name(gate, None) == 'door locker'
    assert alphaclops.measurement_key_name(gate, NotImplemented) == 'door locker'
    assert alphaclops.measurement_key_name(gate, 'a') == 'door locker'


@pytest.mark.parametrize('gate', [ReturnsStr(), ReturnsObj()])
def test_measurement_key_obj(gate):
    assert isinstance(alphaclops.measurement_key_obj(gate), alphaclops.MeasurementKey)
    assert alphaclops.measurement_key_obj(gate) == alphaclops.MeasurementKey(name='door locker')
    assert alphaclops.measurement_key_obj(gate) == 'door locker'

    assert alphaclops.measurement_key_obj(gate, None) == 'door locker'
    assert alphaclops.measurement_key_obj(gate, NotImplemented) == 'door locker'
    assert alphaclops.measurement_key_obj(gate, 'a') == 'door locker'


@pytest.mark.parametrize('key_method', [alphaclops.measurement_key_name, alphaclops.measurement_key_obj])
def test_measurement_key_no_method(key_method):
    class NoMethod:
        pass

    with pytest.raises(TypeError, match='no measurement keys'):
        key_method(NoMethod())

    with pytest.raises(ValueError, match='multiple measurement keys'):
        key_method(
            alphaclops.Circuit(
                alphaclops.measure(alphaclops.LineQubit(0), key='a'), alphaclops.measure(alphaclops.LineQubit(0), key='b')
            )
        )

    assert key_method(NoMethod(), None) is None
    assert key_method(NoMethod(), NotImplemented) is NotImplemented
    assert key_method(NoMethod(), 'a') == 'a'

    assert key_method(alphaclops.X, None) is None
    assert key_method(alphaclops.X(alphaclops.LineQubit(0)), None) is None


@pytest.mark.parametrize('key_method', [alphaclops.measurement_key_name, alphaclops.measurement_key_obj])
def test_measurement_key_not_implemented_default_behavior(key_method):
    class ReturnsNotImplemented:
        def _measurement_key_name_(self):
            return NotImplemented

        def _measurement_key_obj_(self):
            return NotImplemented

    with pytest.raises(TypeError, match='NotImplemented'):
        key_method(ReturnsNotImplemented())

    assert key_method(ReturnsNotImplemented(), None) is None
    assert key_method(ReturnsNotImplemented(), NotImplemented) is NotImplemented
    assert key_method(ReturnsNotImplemented(), 'a') == 'a'


def test_is_measurement():
    q = alphaclops.NamedQubit('q')
    assert alphaclops.is_measurement(alphaclops.measure(q))
    assert alphaclops.is_measurement(alphaclops.MeasurementGate(num_qubits=1, key='b'))

    assert not alphaclops.is_measurement(alphaclops.X(q))
    assert not alphaclops.is_measurement(alphaclops.X)
    assert not alphaclops.is_measurement(alphaclops.bit_flip(1))

    class NotImplementedOperation(alphaclops.Operation):
        def with_qubits(self, *new_qubits) -> 'NotImplementedOperation':
            raise NotImplementedError()

        @property
        def qubits(self):
            return alphaclops.LineQubit.range(2)

    assert not alphaclops.is_measurement(NotImplementedOperation())


def test_measurement_without_key():
    class MeasurementWithoutKey:
        def _is_measurement_(self):
            return True

    with pytest.raises(TypeError, match='no measurement keys'):
        _ = alphaclops.measurement_key_name(MeasurementWithoutKey())

    assert alphaclops.is_measurement(MeasurementWithoutKey())


def test_non_measurement_with_key():
    class NonMeasurementGate(alphaclops.Gate):
        def _is_measurement_(self):
            return False

        def _decompose_(self, qubits):
            # Decompose should not be called by `is_measurement`
            assert False

        def _measurement_key_name_(self):
            # `measurement_key_name`` should not be called by `is_measurement`
            assert False

        def _measurement_key_names_(self):
            # `measurement_key_names`` should not be called by `is_measurement`
            assert False

        def _measurement_key_obj_(self):
            # `measurement_key_obj`` should not be called by `is_measurement`
            assert False

        def _measurement_key_objs_(self):
            # `measurement_key_objs`` should not be called by `is_measurement`
            assert False

        def num_qubits(self) -> int:
            return 2  # coverage: ignore

    assert not alphaclops.is_measurement(NonMeasurementGate())


@pytest.mark.parametrize(
    ('key_method', 'keys'),
    [(alphaclops.measurement_key_names, {'a', 'b'}), (alphaclops.measurement_key_objs, {'c', 'd'})],
)
def test_measurement_keys(key_method, keys):
    class MeasurementKeysGate(alphaclops.Gate):
        def _measurement_key_names_(self):
            return frozenset(['a', 'b'])

        def _measurement_key_objs_(self):
            return frozenset([alphaclops.MeasurementKey('c'), alphaclops.MeasurementKey('d')])

        def num_qubits(self) -> int:
            return 1

    a, b = alphaclops.LineQubit.range(2)
    assert key_method(None) == set()
    assert key_method([]) == set()
    assert key_method(alphaclops.X) == set()
    assert key_method(alphaclops.X(a)) == set()
    assert key_method(alphaclops.measure(a, key='out')) == {'out'}
    assert key_method(alphaclops.Circuit(alphaclops.measure(a, key='a'), alphaclops.measure(b, key='2'))) == {
        'a',
        '2',
    }
    assert key_method(MeasurementKeysGate()) == keys
    assert key_method(MeasurementKeysGate().on(a)) == keys


def test_measurement_key_mapping():
    class MultiKeyGate:
        def __init__(self, keys):
            self._keys = frozenset(keys)

        def _measurement_key_names_(self):
            return self._keys

        def _with_measurement_key_mapping_(self, key_map):
            if not all(key in key_map for key in self._keys):
                raise ValueError('missing keys')
            return MultiKeyGate([key_map[key] for key in self._keys])

    assert alphaclops.measurement_key_names(MultiKeyGate([])) == set()
    assert alphaclops.measurement_key_names(MultiKeyGate(['a'])) == {'a'}

    mkg_ab = MultiKeyGate(['a', 'b'])
    assert alphaclops.measurement_key_names(mkg_ab) == {'a', 'b'}

    mkg_cd = alphaclops.with_measurement_key_mapping(mkg_ab, {'a': 'c', 'b': 'd'})
    assert alphaclops.measurement_key_names(mkg_cd) == {'c', 'd'}

    mkg_ac = alphaclops.with_measurement_key_mapping(mkg_ab, {'a': 'a', 'b': 'c'})
    assert alphaclops.measurement_key_names(mkg_ac) == {'a', 'c'}

    mkg_ba = alphaclops.with_measurement_key_mapping(mkg_ab, {'a': 'b', 'b': 'a'})
    assert alphaclops.measurement_key_names(mkg_ba) == {'a', 'b'}

    with pytest.raises(ValueError):
        alphaclops.with_measurement_key_mapping(mkg_ab, {'a': 'c'})

    assert alphaclops.with_measurement_key_mapping(alphaclops.X, {'a': 'c'}) is NotImplemented

    mkg_cdx = alphaclops.with_measurement_key_mapping(mkg_ab, {'a': 'c', 'b': 'd', 'x': 'y'})
    assert alphaclops.measurement_key_names(mkg_cdx) == {'c', 'd'}


def test_measurement_key_path():
    class MultiKeyGate:
        def __init__(self, keys):
            self._keys = frozenset(alphaclops.MeasurementKey.parse_serialized(key) for key in keys)

        def _measurement_key_names_(self):
            return frozenset(str(key) for key in self._keys)

        def _with_key_path_(self, path):
            return MultiKeyGate([str(key._with_key_path_(path)) for key in self._keys])

    assert alphaclops.measurement_key_names(MultiKeyGate([])) == set()
    assert alphaclops.measurement_key_names(MultiKeyGate(['a'])) == {'a'}

    mkg_ab = MultiKeyGate(['a', 'b'])
    assert alphaclops.measurement_key_names(mkg_ab) == {'a', 'b'}

    mkg_cd = alphaclops.with_key_path(mkg_ab, ('c', 'd'))
    assert alphaclops.measurement_key_names(mkg_cd) == {'c:d:a', 'c:d:b'}

    assert alphaclops.with_key_path(alphaclops.X, ('c', 'd')) is NotImplemented
