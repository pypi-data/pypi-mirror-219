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

import pytest, sympy

import alphaclops
from alphaclops.study import ParamResolver


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_resolve_parameters(resolve_fn):
    class NoMethod:
        pass

    class ReturnsNotImplemented:
        def _is_parameterized_(self):
            return NotImplemented

        def _resolve_parameters_(self, resolver, recursive):
            return NotImplemented

    class SimpleParameterSwitch:
        def __init__(self, var):
            self.parameter = var

        def _is_parameterized_(self) -> bool:
            return self.parameter != 0

        def _resolve_parameters_(self, resolver: ParamResolver, recursive: bool):
            self.parameter = resolver.value_of(self.parameter, recursive)
            return self

    assert not alphaclops.is_parameterized(NoMethod())
    assert not alphaclops.is_parameterized(ReturnsNotImplemented())
    assert alphaclops.is_parameterized(SimpleParameterSwitch('a'))
    assert not alphaclops.is_parameterized(SimpleParameterSwitch(0))

    ni = ReturnsNotImplemented()
    d = {'a': 0}
    r = alphaclops.ParamResolver(d)
    no = NoMethod()
    assert resolve_fn(no, r) == no
    assert resolve_fn(no, d) == no
    assert resolve_fn(ni, r) == ni
    assert resolve_fn(SimpleParameterSwitch(0), r).parameter == 0
    assert resolve_fn(SimpleParameterSwitch('a'), r).parameter == 0
    assert resolve_fn(SimpleParameterSwitch('a'), d).parameter == 0
    assert resolve_fn(sympy.Symbol('a'), r) == 0

    a, b, c = tuple(sympy.Symbol(l) for l in 'abc')
    x, y, z = 0, 4, 7
    resolver = {a: x, b: y, c: z}

    assert resolve_fn((a, b, c), resolver) == (x, y, z)
    assert resolve_fn([a, b, c], resolver) == [x, y, z]
    assert resolve_fn((x, y, z), resolver) == (x, y, z)
    assert resolve_fn([x, y, z], resolver) == [x, y, z]
    assert resolve_fn((), resolver) == ()
    assert resolve_fn([], resolver) == []
    assert resolve_fn(1, resolver) == 1
    assert resolve_fn(1.1, resolver) == 1.1
    assert resolve_fn(1j, resolver) == 1j


def test_is_parameterized():
    a, b = tuple(sympy.Symbol(l) for l in 'ab')
    x, y = 0, 4
    assert not alphaclops.is_parameterized((x, y))
    assert not alphaclops.is_parameterized([x, y])
    assert alphaclops.is_parameterized([a, b])
    assert alphaclops.is_parameterized([a, x])
    assert alphaclops.is_parameterized((a, b))
    assert alphaclops.is_parameterized((a, x))
    assert not alphaclops.is_parameterized(())
    assert not alphaclops.is_parameterized([])
    assert not alphaclops.is_parameterized(1)
    assert not alphaclops.is_parameterized(1.1)
    assert not alphaclops.is_parameterized(1j)


def test_parameter_names():
    a, b, c = tuple(sympy.Symbol(l) for l in 'abc')
    x, y, z = 0, 4, 7
    assert alphaclops.parameter_names((a, b, c)) == {'a', 'b', 'c'}
    assert alphaclops.parameter_names([a, b, c]) == {'a', 'b', 'c'}
    assert alphaclops.parameter_names((x, y, z)) == set()
    assert alphaclops.parameter_names([x, y, z]) == set()
    assert alphaclops.parameter_names(()) == set()
    assert alphaclops.parameter_names([]) == set()
    assert alphaclops.parameter_names(1) == set()
    assert alphaclops.parameter_names(1.1) == set()
    assert alphaclops.parameter_names(1j) == set()


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_skips_empty_resolution(resolve_fn):
    class Tester:
        def _resolve_parameters_(self, resolver, recursive):
            return 5

    t = Tester()
    assert resolve_fn(t, {}) is t
    assert resolve_fn(t, {'x': 2}) == 5


def test_recursive_resolve():
    a, b, c = [sympy.Symbol(l) for l in 'abc']
    resolver = alphaclops.ParamResolver({a: b + 3, b: c + 2, c: 1})
    assert alphaclops.resolve_parameters_once(a, resolver) == b + 3
    assert alphaclops.resolve_parameters(a, resolver) == 6
    assert alphaclops.resolve_parameters_once(b, resolver) == c + 2
    assert alphaclops.resolve_parameters(b, resolver) == 3
    assert alphaclops.resolve_parameters_once(c, resolver) == 1
    assert alphaclops.resolve_parameters(c, resolver) == 1

    assert alphaclops.resolve_parameters_once([a, b], {a: b, b: c}) == [b, c]
    assert alphaclops.resolve_parameters_once(a, {}) == a

    resolver = alphaclops.ParamResolver({a: b, b: a})
    assert alphaclops.resolve_parameters_once(a, resolver) == b
    with pytest.raises(RecursionError):
        _ = alphaclops.resolve_parameters(a, resolver)
