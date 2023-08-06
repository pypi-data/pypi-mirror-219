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


def test_product_duplicate_keys():
    with pytest.raises(ValueError):
        _ = alphaclops.Linspace('a', 0, 9, 10) * alphaclops.Linspace('a', 0, 10, 11)


def test_zip_duplicate_keys():
    with pytest.raises(ValueError):
        _ = alphaclops.Linspace('a', 0, 9, 10) + alphaclops.Linspace('a', 0, 10, 11)


def test_product_wrong_type():
    with pytest.raises(TypeError):
        _ = alphaclops.Linspace('a', 0, 9, 10) * 2


def test_zip_wrong_type():
    with pytest.raises(TypeError):
        _ = alphaclops.Linspace('a', 0, 9, 10) + 2


def test_linspace():
    sweep = alphaclops.Linspace('a', 0.34, 9.16, 7)
    assert len(sweep) == 7
    params = list(sweep.param_tuples())
    assert len(params) == 7
    assert params[0] == (('a', 0.34),)
    assert params[-1] == (('a', 9.16),)


def test_linspace_one_point():
    sweep = alphaclops.Linspace('a', 0.34, 9.16, 1)
    assert len(sweep) == 1
    params = list(sweep.param_tuples())
    assert len(params) == 1
    assert params[0] == (('a', 0.34),)


def test_linspace_sympy_symbol():
    a = sympy.Symbol('a')
    sweep = alphaclops.Linspace(a, 0.34, 9.16, 7)
    assert len(sweep) == 7
    params = list(sweep.param_tuples())
    assert len(params) == 7
    assert params[0] == (('a', 0.34),)
    assert params[-1] == (('a', 9.16),)


def test_points():
    sweep = alphaclops.Points('a', [1, 2, 3, 4])
    assert len(sweep) == 4
    params = list(sweep)
    assert len(params) == 4


def test_zip():
    sweep = alphaclops.Points('a', [1, 2, 3]) + alphaclops.Points('b', [4, 5, 6, 7])
    assert len(sweep) == 3
    assert _values(sweep, 'a') == [1, 2, 3]
    assert _values(sweep, 'b') == [4, 5, 6]


def test_zip_longest():
    sweep = alphaclops.ZipLongest(alphaclops.Points('a', [1, 2, 3]), alphaclops.Points('b', [4, 5, 6, 7]))
    assert tuple(sweep.param_tuples()) == (
        (('a', 1), ('b', 4)),
        (('a', 2), ('b', 5)),
        (('a', 3), ('b', 6)),
        (('a', 3), ('b', 7)),
    )
    assert sweep.keys == ['a', 'b']
    assert (
        str(sweep) == 'ZipLongest(alphaclops.Points(\'a\', [1, 2, 3]), alphaclops.Points(\'b\', [4, 5, 6, 7]))'
    )
    assert (
        repr(sweep)
        == 'alphaclops_google.ZipLongest(alphaclops.Points(\'a\', [1, 2, 3]), alphaclops.Points(\'b\', [4, 5, 6, 7]))'
    )


def test_zip_longest_compatibility():
    sweep = alphaclops.Zip(alphaclops.Points('a', [1, 2, 3]), alphaclops.Points('b', [4, 5, 6]))
    sweep_longest = alphaclops.ZipLongest(alphaclops.Points('a', [1, 2, 3]), alphaclops.Points('b', [4, 5, 6]))
    assert tuple(sweep.param_tuples()) == tuple(sweep_longest.param_tuples())

    sweep = alphaclops.Zip(
        (alphaclops.Points('a', [1, 3]) * alphaclops.Points('b', [2, 4])), alphaclops.Points('c', [4, 5, 6, 7])
    )
    sweep_longest = alphaclops.ZipLongest(
        (alphaclops.Points('a', [1, 3]) * alphaclops.Points('b', [2, 4])), alphaclops.Points('c', [4, 5, 6, 7])
    )
    assert tuple(sweep.param_tuples()) == tuple(sweep_longest.param_tuples())


def test_empty_zip():
    assert len(alphaclops.ZipLongest()) == 0
    with pytest.raises(ValueError, match='non-empty'):
        _ = alphaclops.ZipLongest(alphaclops.Points('e', []), alphaclops.Points('a', [1, 2, 3]))


def test_zip_eq():
    et = alphaclops.testing.EqualsTester()
    point_sweep1 = alphaclops.Points('a', [1, 2, 3])
    point_sweep2 = alphaclops.Points('b', [4, 5, 6, 7])
    point_sweep3 = alphaclops.Points('c', [1, 2])

    et.add_equality_group(alphaclops.ZipLongest(), alphaclops.ZipLongest())

    et.add_equality_group(
        alphaclops.ZipLongest(point_sweep1, point_sweep2), alphaclops.ZipLongest(point_sweep1, point_sweep2)
    )

    et.add_equality_group(alphaclops.ZipLongest(point_sweep3, point_sweep2))
    et.add_equality_group(alphaclops.ZipLongest(point_sweep2, point_sweep1))
    et.add_equality_group(alphaclops.ZipLongest(point_sweep1, point_sweep2, point_sweep3))

    et.add_equality_group(alphaclops.Zip(point_sweep1, point_sweep2, point_sweep3))
    et.add_equality_group(alphaclops.Zip(point_sweep1, point_sweep2))


def test_product():
    sweep = alphaclops.Points('a', [1, 2, 3]) * alphaclops.Points('b', [4, 5, 6, 7])
    assert len(sweep) == 12
    assert _values(sweep, 'a') == [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    assert _values(sweep, 'b') == [4, 5, 6, 7, 4, 5, 6, 7, 4, 5, 6, 7]


def test_slice_access_error():
    sweep = alphaclops.Points('a', [1, 2, 3])
    with pytest.raises(TypeError, match='<class \'str\'>'):
        _ = sweep['junk']

    with pytest.raises(IndexError):
        _ = sweep[4]

    with pytest.raises(IndexError):
        _ = sweep[-4]


def test_slice_sweep():
    sweep = alphaclops.Points('a', [1, 2, 3]) * alphaclops.Points('b', [4, 5, 6, 7])

    first_two = sweep[:2]
    assert list(first_two.param_tuples())[0] == (('a', 1), ('b', 4))
    assert list(first_two.param_tuples())[1] == (('a', 1), ('b', 5))
    assert len(list(first_two)) == 2

    middle_three = sweep[5:8]
    assert list(middle_three.param_tuples())[0] == (('a', 2), ('b', 5))
    assert list(middle_three.param_tuples())[1] == (('a', 2), ('b', 6))
    assert list(middle_three.param_tuples())[2] == (('a', 2), ('b', 7))
    assert len(list(middle_three.param_tuples())) == 3

    odd_elems = sweep[6:1:-2]
    assert list(odd_elems.param_tuples())[2] == (('a', 1), ('b', 6))
    assert list(odd_elems.param_tuples())[1] == (('a', 2), ('b', 4))
    assert list(odd_elems.param_tuples())[0] == (('a', 2), ('b', 6))
    assert len(list(odd_elems.param_tuples())) == 3

    sweep_reversed = sweep[::-1]
    assert list(sweep) == list(reversed(list(sweep_reversed)))

    single_sweep = sweep[5:6]
    assert list(single_sweep.param_tuples())[0] == (('a', 2), ('b', 5))
    assert len(list(single_sweep.param_tuples())) == 1


def test_access_sweep():
    sweep = alphaclops.Points('a', [1, 2, 3]) * alphaclops.Points('b', [4, 5, 6, 7])

    first_elem = sweep[-12]
    assert first_elem == alphaclops.ParamResolver({'a': 1, 'b': 4})

    sixth_elem = sweep[5]
    assert sixth_elem == alphaclops.ParamResolver({'a': 2, 'b': 5})


# We use factories since some of these produce generators and we want to
# test for passing in a generator to initializer.
@pytest.mark.parametrize(
    'r_list_factory',
    [
        lambda: [{'a': a, 'b': a + 1} for a in (0, 0.5, 1, -10)],
        lambda: ({'a': a, 'b': a + 1} for a in (0, 0.5, 1, -10)),
        lambda: ({sympy.Symbol('a'): a, 'b': a + 1} for a in (0, 0.5, 1, -10)),
    ],
)
def test_list_sweep(r_list_factory):
    sweep = alphaclops.ListSweep(r_list_factory())
    assert sweep.keys == ['a', 'b']
    assert len(sweep) == 4
    assert len(list(sweep)) == 4
    assert list(sweep)[1] == alphaclops.ParamResolver({'a': 0.5, 'b': 1.5})
    params = list(sweep.param_tuples())
    assert len(params) == 4
    assert params[3] == (('a', -10), ('b', -9))


def test_list_sweep_empty():
    assert alphaclops.ListSweep([]).keys == []


def test_list_sweep_type_error():
    with pytest.raises(TypeError, match='Not a ParamResolver'):
        _ = alphaclops.ListSweep([alphaclops.ParamResolver(), 'bad'])


def _values(sweep, key):
    p = sympy.Symbol(key)
    return [resolver.value_of(p) for resolver in sweep]


def test_equality():
    et = alphaclops.testing.EqualsTester()

    et.add_equality_group(alphaclops.UnitSweep, alphaclops.UnitSweep)

    # Simple sweeps with the same key are equal to themselves, but different
    # from each other even if they happen to contain the same points.
    et.make_equality_group(lambda: alphaclops.Linspace('a', 0, 10, 11))
    et.make_equality_group(lambda: alphaclops.Linspace('b', 0, 10, 11))
    et.make_equality_group(lambda: alphaclops.Points('a', list(range(11))))
    et.make_equality_group(lambda: alphaclops.Points('b', list(range(11))))

    # Product and Zip sweeps can also be equated.
    et.make_equality_group(lambda: alphaclops.Linspace('a', 0, 5, 6) * alphaclops.Linspace('b', 10, 15, 6))
    et.make_equality_group(lambda: alphaclops.Linspace('a', 0, 5, 6) + alphaclops.Linspace('b', 10, 15, 6))
    et.make_equality_group(
        lambda: alphaclops.Points('a', [1, 2])
                * (alphaclops.Linspace('b', 0, 5, 6) + alphaclops.Linspace('c', 10, 15, 6))
    )

    # ListSweep
    et.make_equality_group(
        lambda: alphaclops.ListSweep([{'var': 1}, {'var': -1}]),
        lambda: alphaclops.ListSweep(({'var': 1}, {'var': -1})),
        lambda: alphaclops.ListSweep(r for r in ({'var': 1}, {'var': -1})),
    )
    et.make_equality_group(lambda: alphaclops.ListSweep([{'var': -1}, {'var': 1}]))
    et.make_equality_group(lambda: alphaclops.ListSweep([{'var': 1}]))
    et.make_equality_group(lambda: alphaclops.ListSweep([{'x': 1}, {'x': -1}]))


def test_repr():
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.study.sweeps.Product(alphaclops.UnitSweep),
        setup_code='import alphaclops\nfrom collections import OrderedDict',
    )
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.study.sweeps.Zip(alphaclops.UnitSweep),
        setup_code='import alphaclops\nfrom collections import OrderedDict',
    )
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.ListSweep(alphaclops.Linspace('a', start=0, stop=3, length=4)),
        setup_code='import alphaclops\nfrom collections import OrderedDict',
    )
    alphaclops.testing.assert_equivalent_repr(alphaclops.Points('zero&pi', [0, 3.14159]))
    alphaclops.testing.assert_equivalent_repr(alphaclops.Linspace('I/10', 0, 1, 10))
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.Points('zero&pi', [0, 3.14159], metadata='example str')
    )
    alphaclops.testing.assert_equivalent_repr(
        alphaclops.Linspace('for_q0', 0, 1, 10, metadata=alphaclops.LineQubit(0))
    )


def test_zip_product_str():
    assert (
        str(alphaclops.UnitSweep + alphaclops.UnitSweep + alphaclops.UnitSweep)
        == 'alphaclops.UnitSweep + alphaclops.UnitSweep + alphaclops.UnitSweep'
    )
    assert (
        str(alphaclops.UnitSweep * alphaclops.UnitSweep * alphaclops.UnitSweep)
        == 'alphaclops.UnitSweep * alphaclops.UnitSweep * alphaclops.UnitSweep'
    )
    assert (
        str(alphaclops.UnitSweep + alphaclops.UnitSweep * alphaclops.UnitSweep)
        == 'alphaclops.UnitSweep + alphaclops.UnitSweep * alphaclops.UnitSweep'
    )
    assert (
        str((alphaclops.UnitSweep + alphaclops.UnitSweep) * alphaclops.UnitSweep)
        == '(alphaclops.UnitSweep + alphaclops.UnitSweep) * alphaclops.UnitSweep'
    )


def test_list_sweep_str():
    assert (
        str(alphaclops.UnitSweep)
        == '''Sweep:
{}'''
    )
    assert (
        str(alphaclops.Linspace('a', start=0, stop=3, length=4))
        == '''Sweep:
{'a': 0.0}
{'a': 1.0}
{'a': 2.0}
{'a': 3.0}'''
    )
    assert (
        str(alphaclops.Linspace('a', start=0, stop=15.75, length=64))
        == '''Sweep:
{'a': 0.0}
{'a': 0.25}
{'a': 0.5}
{'a': 0.75}
{'a': 1.0}
...
{'a': 14.75}
{'a': 15.0}
{'a': 15.25}
{'a': 15.5}
{'a': 15.75}'''
    )
    assert (
        str(alphaclops.ListSweep(alphaclops.Linspace('a', 0, 3, 4) + alphaclops.Linspace('b', 1, 2, 2)))
        == '''Sweep:
{'a': 0.0, 'b': 1.0}
{'a': 1.0, 'b': 2.0}'''
    )
    assert (
        str(alphaclops.ListSweep(alphaclops.Linspace('a', 0, 3, 4) * alphaclops.Linspace('b', 1, 2, 2)))
        == '''Sweep:
{'a': 0.0, 'b': 1.0}
{'a': 0.0, 'b': 2.0}
{'a': 1.0, 'b': 1.0}
{'a': 1.0, 'b': 2.0}
{'a': 2.0, 'b': 1.0}
{'a': 2.0, 'b': 2.0}
{'a': 3.0, 'b': 1.0}
{'a': 3.0, 'b': 2.0}'''
    )


def test_dict_to_product_sweep():
    assert alphaclops.dict_to_product_sweep({'t': [0, 2, 3]}) == (
        alphaclops.Product(alphaclops.Points('t', [0, 2, 3]))
    )

    assert alphaclops.dict_to_product_sweep({'t': [0, 1], 's': [2, 3], 'r': 4}) == (
        alphaclops.Product(alphaclops.Points('t', [0, 1]), alphaclops.Points('s', [2, 3]), alphaclops.Points('r', [4]))
    )


def test_dict_to_zip_sweep():
    assert alphaclops.dict_to_zip_sweep({'t': [0, 2, 3]}) == (alphaclops.Zip(alphaclops.Points('t', [0, 2, 3])))

    assert alphaclops.dict_to_zip_sweep({'t': [0, 1], 's': [2, 3], 'r': 4}) == (
        alphaclops.Zip(alphaclops.Points('t', [0, 1]), alphaclops.Points('s', [2, 3]), alphaclops.Points('r', [4]))
    )
