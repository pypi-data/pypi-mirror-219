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
"""Tests for sweepable.py."""

import itertools

import pytest
import sympy

import alphaclops


def test_to_resolvers_none():
    assert list(alphaclops.to_resolvers(None)) == [alphaclops.ParamResolver({})]


def test_to_resolvers_single():
    resolver = alphaclops.ParamResolver({})
    assert list(alphaclops.to_resolvers(resolver)) == [resolver]
    assert list(alphaclops.to_resolvers({})) == [resolver]


def test_to_resolvers_sweep():
    sweep = alphaclops.Linspace('a', 0, 1, 10)
    assert list(alphaclops.to_resolvers(sweep)) == list(sweep)


def test_to_resolvers_iterable():
    resolvers = [alphaclops.ParamResolver({'a': 2}), alphaclops.ParamResolver({'a': 1})]
    assert list(alphaclops.to_resolvers(resolvers)) == resolvers
    assert list(alphaclops.to_resolvers([{'a': 2}, {'a': 1}])) == resolvers


def test_to_resolvers_iterable_sweeps():
    sweeps = [alphaclops.Linspace('a', 0, 1, 10), alphaclops.Linspace('b', 0, 1, 10)]
    assert list(alphaclops.to_resolvers(sweeps)) == list(itertools.chain(*sweeps))


def test_to_resolvers_bad():
    with pytest.raises(TypeError, match='Unrecognized sweepable'):
        for _ in alphaclops.study.to_resolvers('nope'):
            pass


def test_to_sweeps_none():
    assert alphaclops.study.to_sweeps(None) == [alphaclops.UnitSweep]


def test_to_sweeps_single():
    resolver = alphaclops.ParamResolver({})
    assert alphaclops.study.to_sweeps(resolver) == [alphaclops.UnitSweep]
    assert alphaclops.study.to_sweeps({}) == [alphaclops.UnitSweep]


def test_to_sweeps_sweep():
    sweep = alphaclops.Linspace('a', 0, 1, 10)
    assert alphaclops.study.to_sweeps(sweep) == [sweep]


def test_to_sweeps_iterable():
    resolvers = [alphaclops.ParamResolver({'a': 2}), alphaclops.ParamResolver({'a': 1})]
    sweeps = [alphaclops.study.Zip(alphaclops.Points('a', [2])), alphaclops.study.Zip(alphaclops.Points('a', [1]))]
    assert alphaclops.study.to_sweeps(resolvers) == sweeps
    assert alphaclops.study.to_sweeps([{'a': 2}, {'a': 1}]) == sweeps


def test_to_sweeps_iterable_sweeps():
    sweeps = [alphaclops.Linspace('a', 0, 1, 10), alphaclops.Linspace('b', 0, 1, 10)]
    assert alphaclops.study.to_sweeps(sweeps) == sweeps


def test_to_sweeps_dictionary_of_list():
    with pytest.warns(DeprecationWarning, match='dict_to_product_sweep'):
        assert alphaclops.study.to_sweeps({'t': [0, 2, 3]}) == alphaclops.study.to_sweeps(
            [{'t': 0}, {'t': 2}, {'t': 3}]
        )
        assert alphaclops.study.to_sweeps({'t': [0, 1], 's': [2, 3], 'r': 4}) == alphaclops.study.to_sweeps(
            [
                {'t': 0, 's': 2, 'r': 4},
                {'t': 0, 's': 3, 'r': 4},
                {'t': 1, 's': 2, 'r': 4},
                {'t': 1, 's': 3, 'r': 4},
            ]
        )


def test_to_sweeps_invalid():
    with pytest.raises(TypeError, match='Unrecognized sweepable'):
        alphaclops.study.to_sweeps('nope')


def test_to_sweep_sweep():
    sweep = alphaclops.Linspace('a', 0, 1, 10)
    assert alphaclops.to_sweep(sweep) is sweep


@pytest.mark.parametrize(
    'r_gen',
    [
        lambda: {'a': 1},
        lambda: {sympy.Symbol('a'): 1},
        lambda: alphaclops.ParamResolver({'a': 1}),
        lambda: alphaclops.ParamResolver({sympy.Symbol('a'): 1}),
    ],
)
def test_to_sweep_single_resolver(r_gen):
    sweep = alphaclops.to_sweep(r_gen())
    assert isinstance(sweep, alphaclops.Sweep)
    assert list(sweep) == [alphaclops.ParamResolver({'a': 1})]


@pytest.mark.parametrize(
    'r_list_gen',
    [
        # Lists
        lambda: [{'a': 1}, {'a': 1.5}],
        lambda: [{sympy.Symbol('a'): 1}, {sympy.Symbol('a'): 1.5}],
        lambda: [alphaclops.ParamResolver({'a': 1}), alphaclops.ParamResolver({'a': 1.5})],
        lambda: [
            alphaclops.ParamResolver({sympy.Symbol('a'): 1}),
            alphaclops.ParamResolver({sympy.Symbol('a'): 1.5}),
        ],
        lambda: [{'a': 1}, alphaclops.ParamResolver({sympy.Symbol('a'): 1.5})],
        lambda: ({'a': 1}, {'a': 1.5}),
        # Iterators
        lambda: (r for r in [{'a': 1}, {'a': 1.5}]),
        lambda: {object(): r for r in [{'a': 1}, {'a': 1.5}]}.values(),
    ],
)
def test_to_sweep_resolver_list(r_list_gen):
    sweep = alphaclops.to_sweep(r_list_gen())
    assert isinstance(sweep, alphaclops.Sweep)
    assert list(sweep) == [alphaclops.ParamResolver({'a': 1}), alphaclops.ParamResolver({'a': 1.5})]


def test_to_sweep_type_error():
    with pytest.raises(TypeError, match='Unexpected sweep'):
        alphaclops.to_sweep(5)
