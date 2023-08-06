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

import pytest
import sympy

import alphaclops


def test_periodic_value_equality():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(
        alphaclops.PeriodicValue(1, 2),
        alphaclops.PeriodicValue(1, 2),
        alphaclops.PeriodicValue(3, 2),
        alphaclops.PeriodicValue(3, 2),
        alphaclops.PeriodicValue(5, 2),
        alphaclops.PeriodicValue(-1, 2),
    )
    eq.add_equality_group(alphaclops.PeriodicValue(1.5, 2.0), alphaclops.PeriodicValue(1.5, 2.0))
    eq.add_equality_group(alphaclops.PeriodicValue(0, 2))
    eq.add_equality_group(alphaclops.PeriodicValue(1, 3))
    eq.add_equality_group(alphaclops.PeriodicValue(2, 4))


def test_periodic_value_approx_eq_basic():
    assert alphaclops.approx_eq(alphaclops.PeriodicValue(1.0, 2.0), alphaclops.PeriodicValue(1.0, 2.0), atol=0.1)
    assert alphaclops.approx_eq(alphaclops.PeriodicValue(1.0, 2.0), alphaclops.PeriodicValue(1.2, 2.0), atol=0.3)
    assert not alphaclops.approx_eq(alphaclops.PeriodicValue(1.0, 2.0), alphaclops.PeriodicValue(1.2, 2.0), atol=0.1)
    assert not alphaclops.approx_eq(alphaclops.PeriodicValue(1.0, 2.0), alphaclops.PeriodicValue(1.0, 2.2), atol=0.3)
    assert not alphaclops.approx_eq(alphaclops.PeriodicValue(1.0, 2.0), alphaclops.PeriodicValue(1.0, 2.2), atol=0.1)
    assert not alphaclops.approx_eq(alphaclops.PeriodicValue(1.0, 2.0), alphaclops.PeriodicValue(1.2, 2.2), atol=0.3)
    assert not alphaclops.approx_eq(alphaclops.PeriodicValue(1.0, 2.0), alphaclops.PeriodicValue(1.2, 2.2), atol=0.1)


def test_periodic_value_approx_eq_normalized():
    assert alphaclops.approx_eq(alphaclops.PeriodicValue(1.0, 3.0), alphaclops.PeriodicValue(4.1, 3.0), atol=0.2)
    assert alphaclops.approx_eq(alphaclops.PeriodicValue(1.0, 3.0), alphaclops.PeriodicValue(-2.1, 3.0), atol=0.2)


def test_periodic_value_approx_eq_boundary():
    assert alphaclops.approx_eq(alphaclops.PeriodicValue(0.0, 2.0), alphaclops.PeriodicValue(1.9, 2.0), atol=0.2)
    assert alphaclops.approx_eq(alphaclops.PeriodicValue(0.1, 2.0), alphaclops.PeriodicValue(1.9, 2.0), atol=0.3)
    assert alphaclops.approx_eq(alphaclops.PeriodicValue(1.9, 2.0), alphaclops.PeriodicValue(0.1, 2.0), atol=0.3)
    assert not alphaclops.approx_eq(alphaclops.PeriodicValue(0.1, 2.0), alphaclops.PeriodicValue(1.9, 2.0), atol=0.1)
    assert alphaclops.approx_eq(alphaclops.PeriodicValue(0, 1.0), alphaclops.PeriodicValue(0.5, 1.0), atol=0.6)
    assert not alphaclops.approx_eq(alphaclops.PeriodicValue(0, 1.0), alphaclops.PeriodicValue(0.5, 1.0), atol=0.1)
    assert alphaclops.approx_eq(alphaclops.PeriodicValue(0.4, 1.0), alphaclops.PeriodicValue(0.6, 1.0), atol=0.3)


def test_periodic_value_types_mismatch():
    assert not alphaclops.approx_eq(alphaclops.PeriodicValue(0.0, 2.0), 0.0, atol=0.2)
    assert not alphaclops.approx_eq(0.0, alphaclops.PeriodicValue(0.0, 2.0), atol=0.2)


@pytest.mark.parametrize(
    'value, is_parameterized, parameter_names',
    [
        (alphaclops.PeriodicValue(1.0, 3.0), False, set()),
        (alphaclops.PeriodicValue(0.0, sympy.Symbol('p')), True, {'p'}),
        (alphaclops.PeriodicValue(sympy.Symbol('v'), 3.0), True, {'v'}),
        (alphaclops.PeriodicValue(sympy.Symbol('v'), sympy.Symbol('p')), True, {'p', 'v'}),
    ],
)
@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_periodic_value_is_parameterized(value, is_parameterized, parameter_names, resolve_fn):
    assert alphaclops.is_parameterized(value) == is_parameterized
    assert alphaclops.parameter_names(value) == parameter_names
    resolved = resolve_fn(value, {p: 1 for p in parameter_names})
    assert not alphaclops.is_parameterized(resolved)


@pytest.mark.parametrize(
    'val',
    [
        alphaclops.PeriodicValue(0.4, 1.0),
        alphaclops.PeriodicValue(0.0, 2.0),
        alphaclops.PeriodicValue(1.0, 3),
        alphaclops.PeriodicValue(-2.1, 3.0),
        alphaclops.PeriodicValue(sympy.Symbol('v'), sympy.Symbol('p')),
        alphaclops.PeriodicValue(2.0, sympy.Symbol('p')),
        alphaclops.PeriodicValue(sympy.Symbol('v'), 3),
    ],
)
def test_periodic_value_repr(val):
    alphaclops.testing.assert_equivalent_repr(val)
