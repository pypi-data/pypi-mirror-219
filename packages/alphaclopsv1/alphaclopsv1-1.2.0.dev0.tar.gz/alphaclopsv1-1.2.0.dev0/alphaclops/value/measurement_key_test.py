# Copyright 2021 The alphaclops Developers
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


def test_empty_init():
    with pytest.raises(TypeError, match='required positional argument'):
        _ = alphaclops.MeasurementKey()  # pylint: disable=no-value-for-parameter
    with pytest.raises(ValueError, match='valid string'):
        _ = alphaclops.MeasurementKey(None)
    with pytest.raises(ValueError, match='valid string'):
        _ = alphaclops.MeasurementKey(4.2)
    # Initialization of empty string should be allowed
    _ = alphaclops.MeasurementKey('')


def test_nested_key():
    with pytest.raises(ValueError, match=': is not allowed.*use `MeasurementKey.parse_serialized'):
        _ = alphaclops.MeasurementKey('nested:key')
    nested_key = alphaclops.MeasurementKey.parse_serialized('nested:key')

    assert nested_key.name == 'key'
    assert nested_key.path == ('nested',)


def test_eq_and_hash():
    class SomeRandomClass:
        def __init__(self, some_str):
            self.some_str = some_str

        def __str__(self):
            return self.some_str  # coverage: ignore

    mkey = alphaclops.MeasurementKey('key')
    assert mkey == 'key'
    assert hash(mkey) == hash('key')
    nested_key = alphaclops.MeasurementKey.parse_serialized('nested:key')
    assert nested_key == 'nested:key'
    non_str_or_measurement_key = SomeRandomClass('key')
    assert mkey != non_str_or_measurement_key


@pytest.mark.parametrize('key_string', ['key', 'nested:key'])
def test_str(key_string):
    mkey = alphaclops.MeasurementKey.parse_serialized(key_string)
    assert str(mkey) == key_string
    assert str(mkey) == mkey


def test_repr():
    mkey = alphaclops.MeasurementKey('key_string')
    assert repr(mkey) == "alphaclops.MeasurementKey(name='key_string')"
    assert eval(repr(mkey)) == mkey
    mkey = alphaclops.MeasurementKey.parse_serialized('nested:key')
    assert repr(mkey) == "alphaclops.MeasurementKey(path=('nested',), name='key')"
    assert eval(repr(mkey)) == mkey


def test_json_dict():
    mkey = alphaclops.MeasurementKey('key')
    assert mkey._json_dict_() == {'name': 'key', 'path': tuple()}
    mkey = alphaclops.MeasurementKey.parse_serialized('nested:key')
    assert mkey._json_dict_() == {'name': 'key', 'path': ('nested',)}


def test_with_key_path():
    mkey = alphaclops.MeasurementKey('key')
    mkey2 = alphaclops.with_key_path(mkey, ('a',))
    assert mkey2.name == mkey.name
    assert mkey2.path == ('a',)
    assert mkey2 == mkey.with_key_path_prefix('a')

    mkey3 = mkey2.with_key_path_prefix('b')
    assert mkey3.name == mkey.name
    assert mkey3.path == ('b', 'a')


def test_with_measurement_key_mapping():
    mkey = alphaclops.MeasurementKey('key')
    mkey2 = alphaclops.with_measurement_key_mapping(mkey, {'key': 'new_key'})
    assert mkey2.name == 'new_key'

    mkey3 = mkey2.with_key_path_prefix('a')
    mkey3 = alphaclops.with_measurement_key_mapping(mkey3, {'new_key': 'newer_key'})
    assert mkey3.name == 'newer_key'
    assert mkey3.path == ('a',)


def test_compare():
    assert alphaclops.MeasurementKey('a') < alphaclops.MeasurementKey('b')
    assert alphaclops.MeasurementKey('a') <= alphaclops.MeasurementKey('b')
    assert alphaclops.MeasurementKey('a') <= alphaclops.MeasurementKey('a')
    assert alphaclops.MeasurementKey('b') > alphaclops.MeasurementKey('a')
    assert alphaclops.MeasurementKey('b') >= alphaclops.MeasurementKey('a')
    assert alphaclops.MeasurementKey('a') >= alphaclops.MeasurementKey('a')
    assert not alphaclops.MeasurementKey('a') > alphaclops.MeasurementKey('b')
    assert not alphaclops.MeasurementKey('a') >= alphaclops.MeasurementKey('b')
    assert not alphaclops.MeasurementKey('b') < alphaclops.MeasurementKey('a')
    assert not alphaclops.MeasurementKey('b') <= alphaclops.MeasurementKey('a')
    assert alphaclops.MeasurementKey(path=(), name='b') < alphaclops.MeasurementKey(path=('0',), name='a')
    assert alphaclops.MeasurementKey(path=('0',), name='n') < alphaclops.MeasurementKey(path=('1',), name='a')
    with pytest.raises(TypeError):
        _ = alphaclops.MeasurementKey('a') < 'b'
    with pytest.raises(TypeError):
        _ = alphaclops.MeasurementKey('a') <= 'b'
