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

from typing import Tuple, List, cast
import re
import pytest
import sympy
import alphaclops
from alphaclops._compat import proper_repr
import numpy as np


class CustomXPowGate(alphaclops.EigenGate):
    def _eigen_components(self) -> List[Tuple[float, np.ndarray]]:
        return [(0, np.array([[0.5, 0.5], [0.5, 0.5]])), (1, np.array([[0.5, -0.5], [-0.5, 0.5]]))]

    def __str__(self) -> str:
        if self._global_shift == 0:
            if self._exponent == 1:
                return 'CustomX'
            return f'CustomX**{self._exponent}'
        return f'CustomXPowGate(exponent={self._exponent}, global_shift={self._global_shift!r})'

    def __repr__(self) -> str:
        if self._global_shift == 0:
            if self._exponent == 1:
                return 'alphaclops.ops.gateset_test.CustomX'
            return f'(alphaclops.ops.gateset_test.CustomX**{proper_repr(self._exponent)})'
        return 'alphaclops.ops.gateset_test.CustomXPowGate(exponent={}, global_shift={!r})'.format(
            proper_repr(self._exponent), self._global_shift
        )

    def _num_qubits_(self) -> int:
        return 1


CustomX = CustomXPowGate()
q = alphaclops.NamedQubit("q")


@pytest.mark.parametrize('gate', [CustomX, CustomXPowGate])
def test_gate_family_init(gate):
    name = 'test_name'
    description = 'test_description'
    g = alphaclops.GateFamily(gate=gate, name=name, description=description)
    assert g.gate == gate
    assert g.name == name
    assert g.description == description


@pytest.mark.parametrize(
    'gate, tags_to_accept, tags_to_ignore',
    [
        (CustomX, [], []),
        (CustomX, ['tag1'], []),
        (CustomX, [], ['tag2']),
        (CustomX, ['tag3'], ['tag4']),
        (CustomXPowGate, [], []),
    ],
)
def test_gate_family_default_name_and_description(gate, tags_to_accept, tags_to_ignore):
    g = alphaclops.GateFamily(gate, tags_to_accept=tags_to_accept, tags_to_ignore=tags_to_ignore)
    assert re.match('.*GateFamily.*CustomX.*', g.name)
    assert re.match('Accepts.*instances.*CustomX.*', g.description)

    accepted_match = re.compile('.*Accepted tags.*', re.DOTALL).match(g.description)
    assert (accepted_match is None) == (tags_to_accept == [])

    ignored_match = re.compile('.*Ignored tags.*', re.DOTALL).match(g.description)
    assert (ignored_match is None) == (tags_to_ignore == [])


@pytest.mark.parametrize(
    'tags_to_accept_fam1, tags_to_ignore_fam1, tags_to_accept_fam2, tags_to_ignore_fam2',
    [
        (tuple("ab"), tuple("cd"), tuple("ba"), tuple("dc")),
        (tuple("ab"), [], tuple("ba"), []),
        ([], tuple("ab"), [], tuple("ba")),
    ],
)
def test_gate_family_equality_with_tags(
    tags_to_accept_fam1, tags_to_ignore_fam1, tags_to_accept_fam2, tags_to_ignore_fam2
):
    gate_fam1 = alphaclops.GateFamily(
        alphaclops.X, tags_to_accept=tags_to_accept_fam1, tags_to_ignore=tags_to_ignore_fam1
    )
    gate_fam2 = alphaclops.GateFamily(
        alphaclops.X, tags_to_accept=tags_to_accept_fam2, tags_to_ignore=tags_to_ignore_fam2
    )

    assert gate_fam1 == gate_fam2


def test_invalid_gate_family():
    with pytest.raises(ValueError, match='instance or subclass of `alphaclops.Gate`'):
        _ = alphaclops.GateFamily(gate=alphaclops.Operation)

    with pytest.raises(ValueError, match='non-parameterized instance of `alphaclops.Gate`'):
        _ = alphaclops.GateFamily(gate=CustomX ** sympy.Symbol('theta'))

    with pytest.raises(ValueError, match='cannot be in both'):
        _ = alphaclops.GateFamily(gate=alphaclops.H, tags_to_accept={'a', 'b'}, tags_to_ignore={'b', 'c'})


def test_gate_family_immutable():
    g = alphaclops.GateFamily(CustomX)
    # Match one of two strings. The second one is message returned since python 3.11.
    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'gate' of 'GateFamily' object has no setter)",
    ):
        g.gate = CustomXPowGate
    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'name' of 'GateFamily' object has no setter)",
    ):
        g.name = 'new name'
    with pytest.raises(
        AttributeError,
        match="(can't set attribute)|(property 'description' of 'GateFamily' object has no setter)",
    ):
        g.description = 'new description'


@pytest.mark.parametrize(
    'gate', [CustomX, CustomXPowGate(exponent=0.5, global_shift=0.1), CustomXPowGate]
)
@pytest.mark.parametrize('name, description', [(None, None), ('custom_name', 'custom_description')])
def test_gate_family_repr_and_str(gate, name, description):
    g = alphaclops.GateFamily(gate, name=name, description=description)
    alphaclops.testing.assert_equivalent_repr(g)
    assert g.name in str(g)
    assert g.description in str(g)


@pytest.mark.parametrize('gate', [alphaclops.X, alphaclops.XPowGate(), alphaclops.XPowGate])
@pytest.mark.parametrize('name, description', [(None, None), ('custom_name', 'custom_description')])
def test_gate_family_json(gate, name, description):
    g = alphaclops.GateFamily(gate, name=name, description=description)
    g_json = alphaclops.to_json(g)
    assert alphaclops.read_json(json_text=g_json) == g


def test_gate_family_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(alphaclops.GateFamily(CustomX))
    eq.add_equality_group(alphaclops.GateFamily(CustomX ** 3))
    eq.add_equality_group(
        alphaclops.GateFamily(CustomX, name='custom_name', description='custom_description'),
        alphaclops.GateFamily(CustomX ** 3, name='custom_name', description='custom_description'),
    )
    eq.add_equality_group(alphaclops.GateFamily(CustomXPowGate))
    eq.add_equality_group(
        alphaclops.GateFamily(CustomXPowGate, name='custom_name', description='custom_description')
    )


@pytest.mark.parametrize(
    'gate_family, gates_to_check',
    [
        (
                alphaclops.GateFamily(CustomXPowGate),
                [
                (CustomX, True),
                (CustomX**0.5, True),
                (CustomX ** sympy.Symbol('theta'), True),
                (CustomXPowGate(exponent=0.25, global_shift=0.15), True),
                (alphaclops.testing.SingleQubitGate(), False),
                (alphaclops.X ** 0.5, False),
                (None, False),
                (alphaclops.global_phase_operation(1j), False),
            ],
        ),
        (
                alphaclops.GateFamily(CustomX),
                [
                (CustomX, True),
                (CustomXPowGate(exponent=1, global_shift=0.15), True),
                (CustomX**2, False),
                (CustomX**3, True),
                (CustomX ** sympy.Symbol('theta'), False),
                (None, False),
                (alphaclops.global_phase_operation(1j), False),
            ],
        ),
        (
                alphaclops.GateFamily(CustomX, ignore_global_phase=False),
                [(CustomX, True), (CustomXPowGate(exponent=1, global_shift=0.15), False)],
        ),
    ],
)
def test_gate_family_predicate_and_containment(gate_family, gates_to_check):
    for gate, result in gates_to_check:
        assert gate_family._predicate(gate) == result
        assert (gate in gate_family) == result
        if isinstance(gate, alphaclops.Gate):
            assert (gate(q) in gate_family) == result
            assert (gate(q).with_tags('tags') in gate_family) == result


@pytest.mark.parametrize(
    'gate_family, gates_to_check',
    [
        (
            # Accept only if the input operation contains at least one of the accepted tags.
                alphaclops.GateFamily(alphaclops.ZPowGate, tags_to_accept=['a', 'b']),
                [
                (alphaclops.Z(q).with_tags('a', 'b'), True),
                (alphaclops.Z(q).with_tags('a'), True),
                (alphaclops.Z(q).with_tags('b'), True),
                (alphaclops.Z(q).with_tags('c'), False),
                (alphaclops.Z(q).with_tags('a', 'c'), True),
                (alphaclops.Z(q).with_tags(), False),
                (alphaclops.Z(q), False),
                (alphaclops.Z, False),
                (alphaclops.X(q).with_tags('a'), False),
                (alphaclops.X(q).with_tags('c'), False),
            ],
        ),
        (
            # Reject if input operation contains at least one of the rejected tags.
                alphaclops.GateFamily(alphaclops.ZPowGate, tags_to_ignore=['a', 'b']),
                [
                (alphaclops.Z(q).with_tags('a', 'b'), False),
                (alphaclops.Z(q).with_tags('a'), False),
                (alphaclops.Z(q).with_tags('b'), False),
                (alphaclops.Z(q).with_tags('c'), True),
                (alphaclops.Z(q).with_tags('a', 'c'), False),
                (alphaclops.Z(q).with_tags(), True),
                (alphaclops.Z(q), True),
                (alphaclops.Z, True),
                (alphaclops.X(q).with_tags('a'), False),
                (alphaclops.X(q).with_tags('c'), False),
            ],
        ),
        (
                alphaclops.GateFamily(alphaclops.ZPowGate, tags_to_accept=['a'], tags_to_ignore=['c']),
                [
                (alphaclops.Z(q).with_tags('a', 'c'), False),  # should prioritize tags_to_ignore
                (alphaclops.Z(q).with_tags('a'), True),
                (alphaclops.Z(q).with_tags('c'), False),
                (alphaclops.Z(q).with_tags(), False),
                (alphaclops.Z(q), False),
                (alphaclops.Z, False),
                (alphaclops.X(q).with_tags('a'), False),
                (alphaclops.X(q).with_tags('c'), False),
            ],
        ),
    ],
)
def test_gate_family_tagged_operations(gate_family, gates_to_check):
    for gate, result in gates_to_check:
        assert (gate in gate_family) == result


class CustomXGateFamily(alphaclops.GateFamily):
    """Accepts all integer powers of CustomXPowGate"""

    def __init__(self) -> None:
        super().__init__(
            gate=CustomXPowGate,
            name='CustomXGateFamily',
            description='Accepts all integer powers of CustomXPowGate',
        )

    def _predicate(self, g: alphaclops.Gate) -> bool:
        """Checks whether gate instance `g` belongs to this GateFamily."""
        if not super()._predicate(g) or alphaclops.is_parameterized(g):
            return False
        exp = cast(CustomXPowGate, g).exponent
        return int(exp) == exp

    def __repr__(self):
        return 'alphaclops.ops.gateset_test.CustomXGateFamily()'


gateset = alphaclops.Gateset(
    CustomX**0.5, alphaclops.testing.TwoQubitGate, CustomXGateFamily(), name='custom gateset'
)


def test_gateset_init():
    assert gateset.name == 'custom gateset'
    assert gateset.gates == frozenset(
        [
            alphaclops.GateFamily(CustomX ** 0.5),
            alphaclops.GateFamily(alphaclops.testing.TwoQubitGate),
            CustomXGateFamily(),
        ]
    )


@pytest.mark.parametrize('g', [gateset, alphaclops.Gateset(name='empty gateset')])
def test_gateset_repr_and_str(g):
    alphaclops.testing.assert_equivalent_repr(g)
    assert g.name in str(g)
    for gate_family in g.gates:
        assert str(gate_family) in str(g)


@pytest.mark.parametrize(
    'gate, result',
    [
        (CustomX, True),
        (CustomX**2, True),
        (CustomXPowGate(exponent=3, global_shift=0.5), True),
        (CustomX**0.5, True),
        (CustomXPowGate(exponent=0.5, global_shift=0.5), True),
        (CustomX**0.25, False),
        (CustomX ** sympy.Symbol('theta'), False),
        (alphaclops.testing.TwoQubitGate(), True),
    ],
)
def test_gateset_contains(gate, result):
    assert (gate in gateset) is result
    op = gate(*alphaclops.LineQubit.range(gate.num_qubits()))
    assert (op in gateset) is result
    assert (op.with_tags('tags') in gateset) is result
    circuit_op = alphaclops.CircuitOperation(alphaclops.FrozenCircuit([op] * 5), repetitions=5)
    assert (circuit_op in gateset) is result
    assert circuit_op not in gateset.with_params(unroll_circuit_op=False)


@pytest.mark.parametrize('use_circuit_op', [True, False])
def test_gateset_validate(use_circuit_op):
    def optree_and_circuit(optree):
        yield optree
        yield alphaclops.Circuit(optree)

    def get_ops(use_circuit_op):
        q = alphaclops.LineQubit.range(3)
        yield [CustomX(q[0]).with_tags('custom tags'), CustomX(q[1]) ** 2, CustomX(q[2]) ** 3]
        yield [CustomX(q[0]) ** 0.5, alphaclops.testing.TwoQubitGate()(*q[:2])]
        if use_circuit_op:
            circuit_op = alphaclops.CircuitOperation(
                alphaclops.FrozenCircuit(get_ops(False)), repetitions=10
            ).with_tags('circuit op tags')
            recursive_circuit_op = alphaclops.CircuitOperation(
                alphaclops.FrozenCircuit([circuit_op, CustomX(q[2]) ** 0.5]),
                repetitions=10,
                qubit_map={q[0]: q[1], q[1]: q[2], q[2]: q[0]},
            )
            yield [circuit_op, recursive_circuit_op]

    def assert_validate_and_contains_consistent(gateset, op_tree, result):
        assert all(op in gateset for op in alphaclops.flatten_to_ops(op_tree)) is result
        for item in optree_and_circuit(op_tree):
            assert gateset.validate(item) is result

    op_tree = [*get_ops(use_circuit_op)]
    assert_validate_and_contains_consistent(
        gateset.with_params(unroll_circuit_op=use_circuit_op), op_tree, True
    )
    if use_circuit_op:
        assert_validate_and_contains_consistent(
            gateset.with_params(unroll_circuit_op=False), op_tree, False
        )


def test_gateset_validate_circuit_op_negative_reps():
    gate = CustomXPowGate(exponent=0.5)
    op = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(gate.on(alphaclops.LineQubit(0))), repetitions=-1)
    assert op not in alphaclops.Gateset(gate)
    assert op ** -1 in alphaclops.Gateset(gate)


def test_with_params():
    assert gateset.with_params() is gateset
    assert (
        gateset.with_params(name=gateset.name, unroll_circuit_op=gateset._unroll_circuit_op)
        is gateset
    )
    gateset_with_params = gateset.with_params(name='new name', unroll_circuit_op=False)
    assert gateset_with_params.name == 'new name'
    assert gateset_with_params._unroll_circuit_op is False


def test_gateset_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(alphaclops.Gateset(CustomX))
    eq.add_equality_group(alphaclops.Gateset(CustomX ** 3))
    eq.add_equality_group(alphaclops.Gateset(CustomX, name='Custom Gateset'))
    eq.add_equality_group(alphaclops.Gateset(CustomX, name='Custom Gateset', unroll_circuit_op=False))
    eq.add_equality_group(alphaclops.Gateset(CustomX, alphaclops.GlobalPhaseGate, name='Custom Gateset'))
    eq.add_equality_group(
        alphaclops.Gateset(
            alphaclops.GateFamily(CustomX, name='custom_name', description='custom_description'),
            alphaclops.GateFamily(CustomX, name='custom_name', description='custom_description'),
        ),
        alphaclops.Gateset(
            alphaclops.GateFamily(CustomX ** 3, name='custom_name', description='custom_description'),
            alphaclops.GateFamily(CustomX, name='custom_name', description='custom_description'),
        ),
    )
    eq.add_equality_group(
        alphaclops.Gateset(CustomX, CustomXPowGate),
        alphaclops.Gateset(CustomXPowGate, CustomX),
        alphaclops.Gateset(CustomX, CustomX, CustomXPowGate),
        alphaclops.Gateset(CustomXPowGate, CustomX, CustomXPowGate),
    )
    eq.add_equality_group(alphaclops.Gateset(CustomXGateFamily()))
    eq.add_equality_group(
        alphaclops.Gateset(
            alphaclops.GateFamily(
                gate=CustomXPowGate,
                name='CustomXGateFamily',
                description='Accepts all integer powers of CustomXPowGate',
            )
        )
    )


def test_gateset_contains_with_tags():
    tag = "PhysicalZTag"
    gf_accept = alphaclops.GateFamily(alphaclops.ZPowGate, tags_to_accept=[tag])
    gf_ignore = alphaclops.GateFamily(alphaclops.ZPowGate, tags_to_ignore=[tag])
    op = alphaclops.Z(q)
    op_with_tag = alphaclops.Z(q).with_tags(tag)

    # Only tags to ignore.
    assert op in alphaclops.Gateset(gf_ignore)
    assert op_with_tag not in alphaclops.Gateset(gf_ignore)

    # Only tags to accept
    assert op not in alphaclops.Gateset(gf_accept)
    assert op_with_tag in alphaclops.Gateset(gf_accept)

    # Both tags to accept and tags to ignore
    assert op in alphaclops.Gateset(gf_accept, gf_ignore)
    assert op_with_tag in alphaclops.Gateset(gf_accept, gf_ignore)
