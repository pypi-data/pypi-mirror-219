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

import numpy as np
import pytest
import sympy
from sympy.parsing import sympy_parser

import alphaclops

ALL_SIMULATORS = (alphaclops.Simulator(), alphaclops.DensityMatrixSimulator(), alphaclops.CliffordSimulator())


def test_diagram():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(alphaclops.measure(q0, key='a'), alphaclops.X(q1).with_classical_controls('a'))

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ───M───────
      ║
1: ───╫───X───
      ║   ║
a: ═══@═══^═══
""",
        use_unicode_characters=True,
    )


def test_diagram_pauli():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure_single_paulistring(alphaclops.X(q0), key='a'),
        alphaclops.X(q1).with_classical_controls('a'),
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ───M(X)───────
      ║
1: ───╫──────X───
      ║      ║
a: ═══@══════^═══
""",
        use_unicode_characters=True,
    )


def test_diagram_extra_measurements():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.measure(q0, key='b'),
        alphaclops.X(q1).with_classical_controls('a'),
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ───M───M('b')───
      ║
1: ───╫───X────────
      ║   ║
a: ═══@═══^════════
""",
        use_unicode_characters=True,
    )


def test_diagram_extra_controlled_bits():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(alphaclops.measure(q0, key='a'), alphaclops.CX(q0, q1).with_classical_controls('a'))

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ───M───@───
      ║   ║
1: ───╫───X───
      ║   ║
a: ═══@═══^═══
""",
        use_unicode_characters=True,
    )


def test_diagram_extra_control_bits():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.measure(q0, key='b'),
        alphaclops.X(q1).with_classical_controls('a', 'b'),
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ───M───M───────
      ║   ║
1: ───╫───╫───X───
      ║   ║   ║
a: ═══@═══╬═══^═══
          ║   ║
b: ═══════@═══^═══
""",
        use_unicode_characters=True,
    )


def test_diagram_multiple_ops_single_moment():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.measure(q1, key='b'),
        alphaclops.X(q0).with_classical_controls('a'),
        alphaclops.X(q1).with_classical_controls('b'),
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
      ┌──┐   ┌──┐
0: ────M──────X─────
       ║      ║
1: ────╫M─────╫X────
       ║║     ║║
a: ════@╬═════^╬════
        ║      ║
b: ═════@══════^════
      └──┘   └──┘
""",
        use_unicode_characters=True,
    )


def test_diagram_subcircuit():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.measure(q0, key='a'), alphaclops.X(q1).with_classical_controls('a'))
        )
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
      [ 0: ───M─────── ]
      [       ║        ]
0: ───[ 1: ───╫───X─── ]───
      [       ║   ║    ]
      [ a: ═══@═══^═══ ]
      │
1: ───#2───────────────────
""",
        use_unicode_characters=True,
    )


def test_diagram_subcircuit_layered():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.measure(q0, key='a'), alphaclops.X(q1).with_classical_controls('a'))
        ),
        alphaclops.X(q1).with_classical_controls('a'),
    )

    alphaclops.testing.assert_has_diagram(
        circuit,
        """
          [ 0: ───M─────── ]
          [       ║        ]
0: ───M───[ 1: ───╫───X─── ]───────
      ║   [       ║   ║    ]
      ║   [ a: ═══@═══^═══ ]
      ║   ║
1: ───╫───#2───────────────────X───
      ║   ║                    ║
a: ═══@═══╩════════════════════^═══
""",
        use_unicode_characters=True,
    )


def test_qasm():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.X(q1).with_classical_controls(sympy.Eq(sympy.Symbol('a'), 0)),
    )
    qasm = alphaclops.qasm(circuit)
    assert (
        qasm
        == f"""// Generated from alphaclops v{alphaclops.__version__}

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1)]
qreg q[2];
creg m_a[1];


measure q[0] -> m_a[0];
if (m_a==0) x q[1];
"""
    )


def test_qasm_no_conditions():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'), alphaclops.ClassicallyControlledOperation(alphaclops.X(q1), [])
    )
    qasm = alphaclops.qasm(circuit)
    assert (
        qasm
        == f"""// Generated from alphaclops v{alphaclops.__version__}

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [q(0), q(1)]
qreg q[2];
creg m_a[1];


measure q[0] -> m_a[0];
x q[1];
"""
    )


def test_qasm_multiple_conditions():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.measure(q0, key='b'),
        alphaclops.X(q1).with_classical_controls(
            sympy.Eq(sympy.Symbol('a'), 0), sympy.Eq(sympy.Symbol('b'), 0)
        ),
    )
    with pytest.raises(ValueError, match='QASM does not support multiple conditions'):
        _ = alphaclops.qasm(circuit)


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_key_unset(sim):
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.X(q1).with_classical_controls('a'),
        alphaclops.measure(q1, key='b'),
    )
    result = sim.run(circuit)
    assert result.measurements['a'] == 0
    assert result.measurements['b'] == 0


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_key_set(sim):
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.X(q0),
        alphaclops.measure(q0, key='a'),
        alphaclops.X(q1).with_classical_controls('a'),
        alphaclops.measure(q1, key='b'),
    )
    result = sim.run(circuit)
    assert result.measurements['a'] == 1
    assert result.measurements['b'] == 1


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_repeated_measurement_unset(sim):
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.X(q0),
        alphaclops.measure(q0, key='a'),
        alphaclops.X(q1).with_classical_controls(alphaclops.KeyCondition(alphaclops.MeasurementKey('a'), index=-2)),
        alphaclops.measure(q1, key='b'),
        alphaclops.X(q1).with_classical_controls(alphaclops.KeyCondition(alphaclops.MeasurementKey('a'), index=-1)),
        alphaclops.measure(q1, key='c'),
    )
    result = sim.run(circuit)
    assert result.records['a'][0][0][0] == 0
    assert result.records['a'][0][1][0] == 1
    assert result.records['b'][0][0][0] == 0
    assert result.records['c'][0][0][0] == 1


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_repeated_measurement_set(sim):
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.X(q0),
        alphaclops.measure(q0, key='a'),
        alphaclops.X(q0),
        alphaclops.measure(q0, key='a'),
        alphaclops.X(q1).with_classical_controls(alphaclops.KeyCondition(alphaclops.MeasurementKey('a'), index=-2)),
        alphaclops.measure(q1, key='b'),
        alphaclops.X(q1).with_classical_controls(alphaclops.KeyCondition(alphaclops.MeasurementKey('a'), index=-1)),
        alphaclops.measure(q1, key='c'),
    )
    result = sim.run(circuit)
    assert result.records['a'][0][0][0] == 1
    assert result.records['a'][0][1][0] == 0
    assert result.records['b'][0][0][0] == 1
    assert result.records['c'][0][0][0] == 1


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_subcircuit_key_unset(sim):
    q0, q1 = alphaclops.LineQubit.range(2)
    inner = alphaclops.Circuit(
        alphaclops.measure(q0, key='c'),
        alphaclops.X(q1).with_classical_controls('c'),
        alphaclops.measure(q1, key='b'),
    )
    circuit = alphaclops.Circuit(
        alphaclops.CircuitOperation(inner.freeze(), repetitions=2, measurement_key_map={'c': 'a'})
    )
    result = sim.run(circuit)
    assert result.measurements['0:a'] == 0
    assert result.measurements['0:b'] == 0
    assert result.measurements['1:a'] == 0
    assert result.measurements['1:b'] == 0


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_subcircuit_key_set(sim):
    q0, q1 = alphaclops.LineQubit.range(2)
    inner = alphaclops.Circuit(
        alphaclops.X(q0),
        alphaclops.measure(q0, key='c'),
        alphaclops.X(q1).with_classical_controls('c'),
        alphaclops.measure(q1, key='b'),
    )
    circuit = alphaclops.Circuit(
        alphaclops.CircuitOperation(inner.freeze(), repetitions=4, measurement_key_map={'c': 'a'})
    )
    result = sim.run(circuit)
    assert result.measurements['0:a'] == 1
    assert result.measurements['0:b'] == 1
    assert result.measurements['1:a'] == 0
    assert result.measurements['1:b'] == 1
    assert result.measurements['2:a'] == 1
    assert result.measurements['2:b'] == 0
    assert result.measurements['3:a'] == 0
    assert result.measurements['3:b'] == 0


def test_key_unset_in_subcircuit_outer_scope():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.measure(q0, key='a'),
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.X(q1).with_classical_controls('a'))),
    )
    circuit.append(alphaclops.measure(q1, key='b'))
    result = alphaclops.Simulator().run(circuit)
    assert result.measurements['a'] == 0
    assert result.measurements['b'] == 0


def test_key_set_in_subcircuit_outer_scope():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.X(q0),
        alphaclops.measure(q0, key='a'),
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.X(q1).with_classical_controls('a'))),
    )
    circuit.append(alphaclops.measure(q1, key='b'))
    result = alphaclops.Simulator().run(circuit)
    assert result.measurements['a'] == 1
    assert result.measurements['b'] == 1


def test_condition_types():
    q0 = alphaclops.LineQubit(0)
    sympy_cond = sympy_parser.parse_expr('a >= 2')
    op = alphaclops.X(q0).with_classical_controls(alphaclops.MeasurementKey('a'), 'b', 'a > b', sympy_cond)
    assert set(map(str, op.classical_controls)) == {'a', 'b', 'a > b', 'a >= 2'}


def test_condition_flattening():
    q0 = alphaclops.LineQubit(0)
    op = alphaclops.X(q0).with_classical_controls('a').with_classical_controls('b')
    assert set(map(str, op.classical_controls)) == {'a', 'b'}
    assert isinstance(op._sub_operation, alphaclops.GateOperation)


def test_condition_stacking():
    q0 = alphaclops.LineQubit(0)
    op = alphaclops.X(q0).with_classical_controls('a').with_tags('t').with_classical_controls('b')
    assert set(map(str, alphaclops.control_keys(op))) == {'a', 'b'}
    assert set(map(str, op.classical_controls)) == {'a', 'b'}
    assert not op.tags


def test_condition_removal():
    q0 = alphaclops.LineQubit(0)
    op = (
        alphaclops.X(q0)
        .with_tags('t1')
        .with_classical_controls('a')
        .with_tags('t2')
        .with_classical_controls('b')
    )
    op = op.without_classical_controls()
    assert not alphaclops.control_keys(op)
    assert not op.classical_controls
    assert not op.tags


def test_qubit_mapping():
    q0, q1 = alphaclops.LineQubit.range(2)
    op = alphaclops.X(q0).with_classical_controls('a')
    assert op.with_qubits(q1).qubits == (q1,)


def test_parameterizable():
    s = sympy.Symbol('s')
    q0 = alphaclops.LineQubit(0)
    op = alphaclops.X(q0).with_classical_controls('a')
    opa = alphaclops.XPowGate(exponent=s).on(q0).with_classical_controls('a')
    assert alphaclops.is_parameterized(opa)
    assert not alphaclops.is_parameterized(op)
    assert alphaclops.resolve_parameters(opa, alphaclops.ParamResolver({'s': 1})) == op


def test_decompose():
    q0 = alphaclops.LineQubit(0)
    op = alphaclops.H(q0).with_classical_controls('a')
    assert alphaclops.decompose(op) == [
        (alphaclops.Y(q0) ** 0.5).with_classical_controls('a'),
        alphaclops.XPowGate(exponent=1.0, global_shift=-0.25).on(q0).with_classical_controls('a'),
    ]


def test_str():
    q0 = alphaclops.LineQubit(0)
    op = alphaclops.X(q0).with_classical_controls('a')
    assert str(op) == 'X(q(0)).with_classical_controls(a)'


def test_scope_local():
    q = alphaclops.LineQubit(0)
    inner = alphaclops.Circuit(alphaclops.measure(q, key='a'), alphaclops.X(q).with_classical_controls('a'))
    middle = alphaclops.Circuit(alphaclops.CircuitOperation(inner.freeze(), repetitions=2))
    outer_subcircuit = alphaclops.CircuitOperation(middle.freeze(), repetitions=2)
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in alphaclops.control_keys(op)
    ]
    assert internal_control_keys == ['0:0:a', '0:1:a', '1:0:a', '1:1:a']
    assert not alphaclops.control_keys(outer_subcircuit)
    assert not alphaclops.control_keys(circuit)
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(outer_subcircuit),
        """
      [       [ 0: ───M───X─── ]             ]
0: ───[ 0: ───[       ║   ║    ]──────────── ]────────────
      [       [ a: ═══@═══^═══ ](loops=2)    ](loops=2)
""",
        use_unicode_characters=True,
    )
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ───────M───X───M───X───M───X───M───X───
          ║   ║   ║   ║   ║   ║   ║   ║
0:0:a: ═══@═══^═══╬═══╬═══╬═══╬═══╬═══╬═══
                  ║   ║   ║   ║   ║   ║
0:1:a: ═══════════@═══^═══╬═══╬═══╬═══╬═══
                          ║   ║   ║   ║
1:0:a: ═══════════════════@═══^═══╬═══╬═══
                                  ║   ║
1:1:a: ═══════════════════════════@═══^═══
""",
        use_unicode_characters=True,
    )
    assert circuit == alphaclops.Circuit(alphaclops.decompose(outer_subcircuit))


def test_scope_flatten_both():
    q = alphaclops.LineQubit(0)
    inner = alphaclops.Circuit(alphaclops.measure(q, key='a'), alphaclops.X(q).with_classical_controls('a'))
    middle = alphaclops.Circuit(
        alphaclops.CircuitOperation(inner.freeze(), repetitions=2, use_repetition_ids=False)
    )
    outer_subcircuit = alphaclops.CircuitOperation(
        middle.freeze(), repetitions=2, use_repetition_ids=False
    )
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in alphaclops.control_keys(op)
    ]
    assert internal_control_keys == ['a', 'a', 'a', 'a']
    assert not alphaclops.control_keys(outer_subcircuit)
    assert not alphaclops.control_keys(circuit)
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(outer_subcircuit),
        """
      [       [ 0: ───M───X─── ]                         ]
0: ───[ 0: ───[       ║   ║    ]──────────────────────── ]────────────────────────
      [       [ a: ═══@═══^═══ ](loops=2, no_rep_ids)    ](loops=2, no_rep_ids)
""",
        use_unicode_characters=True,
    )
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ───M───X───M───X───M───X───M───X───
      ║   ║   ║   ║   ║   ║   ║   ║
a: ═══@═══^═══@═══^═══@═══^═══@═══^═══
""",
        use_unicode_characters=True,
    )


def test_scope_flatten_inner():
    q = alphaclops.LineQubit(0)
    inner = alphaclops.Circuit(alphaclops.measure(q, key='a'), alphaclops.X(q).with_classical_controls('a'))
    middle = alphaclops.Circuit(
        alphaclops.CircuitOperation(inner.freeze(), repetitions=2, use_repetition_ids=False)
    )
    outer_subcircuit = alphaclops.CircuitOperation(middle.freeze(), repetitions=2)
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in alphaclops.control_keys(op)
    ]
    assert internal_control_keys == ['0:a', '0:a', '1:a', '1:a']
    assert not alphaclops.control_keys(outer_subcircuit)
    assert not alphaclops.control_keys(circuit)
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(outer_subcircuit),
        """
      [       [ 0: ───M───X─── ]                         ]
0: ───[ 0: ───[       ║   ║    ]──────────────────────── ]────────────
      [       [ a: ═══@═══^═══ ](loops=2, no_rep_ids)    ](loops=2)
""",
        use_unicode_characters=True,
    )
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ─────M───X───M───X───M───X───M───X───
        ║   ║   ║   ║   ║   ║   ║   ║
0:a: ═══@═══^═══@═══^═══╬═══╬═══╬═══╬═══
                        ║   ║   ║   ║
1:a: ═══════════════════@═══^═══@═══^═══
""",
        use_unicode_characters=True,
    )


def test_scope_flatten_outer():
    q = alphaclops.LineQubit(0)
    inner = alphaclops.Circuit(alphaclops.measure(q, key='a'), alphaclops.X(q).with_classical_controls('a'))
    middle = alphaclops.Circuit(alphaclops.CircuitOperation(inner.freeze(), repetitions=2))
    outer_subcircuit = alphaclops.CircuitOperation(
        middle.freeze(), repetitions=2, use_repetition_ids=False
    )
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in alphaclops.control_keys(op)
    ]
    assert internal_control_keys == ['0:a', '1:a', '0:a', '1:a']
    assert not alphaclops.control_keys(outer_subcircuit)
    assert not alphaclops.control_keys(circuit)
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(outer_subcircuit),
        """
      [       [ 0: ───M───X─── ]             ]
0: ───[ 0: ───[       ║   ║    ]──────────── ]────────────────────────
      [       [ a: ═══@═══^═══ ](loops=2)    ](loops=2, no_rep_ids)
""",
        use_unicode_characters=True,
    )
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ─────M───X───M───X───M───X───M───X───
        ║   ║   ║   ║   ║   ║   ║   ║
0:a: ═══@═══^═══╬═══╬═══@═══^═══╬═══╬═══
                ║   ║           ║   ║
1:a: ═══════════@═══^═══════════@═══^═══
""",
        use_unicode_characters=True,
    )


def test_scope_extern():
    q = alphaclops.LineQubit(0)
    inner = alphaclops.Circuit(alphaclops.measure(q, key='a'), alphaclops.X(q).with_classical_controls('b'))
    middle = alphaclops.Circuit(
        alphaclops.measure(q, key=alphaclops.MeasurementKey('b')),
        alphaclops.CircuitOperation(inner.freeze(), repetitions=2),
    )
    outer_subcircuit = alphaclops.CircuitOperation(middle.freeze(), repetitions=2)
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in alphaclops.control_keys(op)
    ]
    assert internal_control_keys == ['0:b', '0:b', '1:b', '1:b']
    assert not alphaclops.control_keys(outer_subcircuit)
    assert not alphaclops.control_keys(circuit)
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(outer_subcircuit),
        """
      [           [ 0: ───M('a')───X─── ]             ]
      [ 0: ───M───[                ║    ]──────────── ]
0: ───[       ║   [ b: ════════════^═══ ](loops=2)    ]────────────
      [       ║   ║                                   ]
      [ b: ═══@═══╩══════════════════════════════════ ](loops=2)
""",
        use_unicode_characters=True,
    )
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ─────M───M('0:0:a')───X───M('0:1:a')───X───M───M('1:0:a')───X───M('1:1:a')───X───
        ║                ║                ║   ║                ║                ║
0:b: ═══@════════════════^════════════════^═══╬════════════════╬════════════════╬═══
                                              ║                ║                ║
1:b: ═════════════════════════════════════════@════════════════^════════════════^═══
""",
        use_unicode_characters=True,
    )
    assert circuit == alphaclops.Circuit(alphaclops.decompose(outer_subcircuit))


def test_scope_extern_wrapping_with_non_repeating_subcircuits():
    def wrap(*ops):
        return alphaclops.CircuitOperation(alphaclops.FrozenCircuit(*ops))

    def wrap_frozen(*ops):
        return alphaclops.FrozenCircuit(wrap(*ops))

    q = alphaclops.LineQubit(0)
    inner = wrap_frozen(
        wrap(alphaclops.measure(q, key='a')), wrap(alphaclops.X(q).with_classical_controls('b'))
    )
    middle = wrap_frozen(
        wrap(alphaclops.measure(q, key=alphaclops.MeasurementKey('b'))),
        wrap(alphaclops.CircuitOperation(inner, repetitions=2)),
    )
    outer_subcircuit = alphaclops.CircuitOperation(middle, repetitions=2)
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in alphaclops.control_keys(op)
    ]
    assert internal_control_keys == ['0:b', '0:b', '1:b', '1:b']
    assert not alphaclops.control_keys(outer_subcircuit)
    assert not alphaclops.control_keys(circuit)
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ─────M───M('0:0:a')───X───M('0:1:a')───X───M───M('1:0:a')───X───M('1:1:a')───X───
        ║                ║                ║   ║                ║                ║
0:b: ═══@════════════════^════════════════^═══╬════════════════╬════════════════╬═══
                                              ║                ║                ║
1:b: ═════════════════════════════════════════@════════════════^════════════════^═══
""",
        use_unicode_characters=True,
    )
    assert circuit == alphaclops.Circuit(alphaclops.decompose(outer_subcircuit))


def test_scope_root():
    q = alphaclops.LineQubit(0)
    inner = alphaclops.Circuit(alphaclops.measure(q, key='a'), alphaclops.X(q).with_classical_controls('b'))
    middle = alphaclops.Circuit(
        alphaclops.measure(q, key=alphaclops.MeasurementKey('c')),
        alphaclops.CircuitOperation(inner.freeze(), repetitions=2),
    )
    outer_subcircuit = alphaclops.CircuitOperation(middle.freeze(), repetitions=2)
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in alphaclops.control_keys(op)
    ]
    assert internal_control_keys == ['b', 'b', 'b', 'b']
    assert alphaclops.control_keys(outer_subcircuit) == {alphaclops.MeasurementKey('b')}
    assert alphaclops.control_keys(circuit) == {alphaclops.MeasurementKey('b')}
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(outer_subcircuit),
        """
      [                [ 0: ───M('a')───X─── ]             ]
      [ 0: ───M('c')───[                ║    ]──────────── ]
0: ───[                [ b: ════════════^═══ ](loops=2)    ]────────────
      [                ║                                   ]
      [ b: ════════════╩══════════════════════════════════ ](loops=2)
      ║
b: ═══╩═════════════════════════════════════════════════════════════════
""",
        use_unicode_characters=True,
    )
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ───M('0:c')───M('0:0:a')───X───M('0:1:a')───X───M('1:c')───M('1:0:a')───X───M('1:1:a')───X───
                              ║                ║                           ║                ║
b: ═══════════════════════════^════════════════^═══════════════════════════^════════════════^═══
""",
        use_unicode_characters=True,
    )
    assert circuit == alphaclops.Circuit(alphaclops.decompose(outer_subcircuit))


def test_scope_extern_mismatch():
    q = alphaclops.LineQubit(0)
    inner = alphaclops.Circuit(alphaclops.measure(q, key='a'), alphaclops.X(q).with_classical_controls('b'))
    middle = alphaclops.Circuit(
        alphaclops.measure(q, key=alphaclops.MeasurementKey('b', ('0',))),
        alphaclops.CircuitOperation(inner.freeze(), repetitions=2),
    )
    outer_subcircuit = alphaclops.CircuitOperation(middle.freeze(), repetitions=2)
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_control_keys = [
        str(condition) for op in circuit.all_operations() for condition in alphaclops.control_keys(op)
    ]
    assert internal_control_keys == ['b', 'b', 'b', 'b']
    assert alphaclops.control_keys(outer_subcircuit) == {alphaclops.MeasurementKey('b')}
    assert alphaclops.control_keys(circuit) == {alphaclops.MeasurementKey('b')}
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(outer_subcircuit),
        """
      [                  [ 0: ───M('a')───X─── ]             ]
      [ 0: ───M('0:b')───[                ║    ]──────────── ]
0: ───[                  [ b: ════════════^═══ ](loops=2)    ]────────────
      [                  ║                                   ]
      [ b: ══════════════╩══════════════════════════════════ ](loops=2)
      ║
b: ═══╩═══════════════════════════════════════════════════════════════════
""",
        use_unicode_characters=True,
    )
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ───M('0:0:b')───M('0:0:a')───X───M('0:1:a')───X───M('1:0:b')───M('1:0:a')───X───M('1:1:a')───X───
                                ║                ║                             ║                ║
b: ═════════════════════════════^════════════════^═════════════════════════════^════════════════^═══
""",
        use_unicode_characters=True,
    )
    assert circuit == alphaclops.Circuit(alphaclops.decompose(outer_subcircuit))


def test_repr():
    q0 = alphaclops.LineQubit(0)
    op = alphaclops.X(q0).with_classical_controls('a')
    assert repr(op) == (
        "alphaclops.ClassicallyControlledOperation("
        "alphaclops.X(alphaclops.LineQubit(0)), [alphaclops.KeyCondition(alphaclops.MeasurementKey(name='a'))]"
        ")"
    )


def test_no_measurement_gates():
    q0 = alphaclops.LineQubit(0)
    with pytest.raises(ValueError, match='with measurements'):
        _ = alphaclops.measure(q0).with_classical_controls('a')


def test_unmeasured_condition():
    q0 = alphaclops.LineQubit(0)
    bad_circuit = alphaclops.Circuit(alphaclops.X(q0).with_classical_controls('a'))
    with pytest.raises(
        ValueError, match='Measurement key a missing when testing classical control'
    ):
        _ = alphaclops.Simulator().simulate(bad_circuit)


def test_layered_circuit_operations_with_controls_in_between():
    q = alphaclops.LineQubit(0)
    outer_subcircuit = alphaclops.CircuitOperation(
        alphaclops.Circuit(
            alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.X(q), alphaclops.Y(q))).with_classical_controls(
                'm'
            )
        ).freeze()
    )
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(outer_subcircuit),
        """
      [ 0: ───[ 0: ───X───Y─── ].with_classical_controls(m)─── ]
0: ───[       ║                                                ]───
      [ m: ═══╩═══════════════════════════════════════════════ ]
      ║
m: ═══╩════════════════════════════════════════════════════════════
""",
        use_unicode_characters=True,
    )
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ───[ 0: ───X───Y─── ].with_classical_controls(m)───
      ║
m: ═══╩═══════════════════════════════════════════════
""",
        use_unicode_characters=True,
    )
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(alphaclops.decompose(outer_subcircuit)),
        """
0: ───X───Y───
      ║   ║
m: ═══^═══^═══
""",
        use_unicode_characters=True,
    )


def test_sympy():
    q0, q1, q2, q3, q_result = alphaclops.LineQubit.range(5)
    for i in range(4):
        for j in range(4):
            # Put first two qubits into a state representing bitstring(i), next two qubits into a
            # state representing bitstring(j) and measure those into m_i and m_j respectively. Then
            # add a conditional X(q_result) based on m_i > m_j and measure that.
            bitstring_i = alphaclops.big_endian_int_to_bits(i, bit_count=2)
            bitstring_j = alphaclops.big_endian_int_to_bits(j, bit_count=2)
            circuit = alphaclops.Circuit(
                alphaclops.X(q0) ** bitstring_i[0],
                alphaclops.X(q1) ** bitstring_i[1],
                alphaclops.X(q2) ** bitstring_j[0],
                alphaclops.X(q3) ** bitstring_j[1],
                alphaclops.measure(q0, q1, key='m_i'),
                alphaclops.measure(q2, q3, key='m_j'),
                alphaclops.X(q_result).with_classical_controls(sympy_parser.parse_expr('m_j > m_i')),
                alphaclops.measure(q_result, key='m_result'),
            )

            # m_result should now be set iff j > i.
            result = alphaclops.Simulator().run(circuit)
            assert result.measurements['m_result'][0][0] == (j > i)


def test_sympy_qudits():
    q0 = alphaclops.LineQid(0, 3)
    q1 = alphaclops.LineQid(1, 5)
    q_result = alphaclops.LineQubit(2)

    class PlusGate(alphaclops.Gate):
        def __init__(self, dimension, increment=1):
            self.dimension = dimension
            self.increment = increment % dimension

        def _qid_shape_(self):
            return (self.dimension,)

        def _unitary_(self):
            inc = (self.increment - 1) % self.dimension + 1
            u = np.empty((self.dimension, self.dimension))
            u[inc:] = np.eye(self.dimension)[:-inc]
            u[:inc] = np.eye(self.dimension)[-inc:]
            return u

    for i in range(15):
        digits = alphaclops.big_endian_int_to_digits(i, digit_count=2, base=(3, 5))
        circuit = alphaclops.Circuit(
            PlusGate(3, digits[0]).on(q0),
            PlusGate(5, digits[1]).on(q1),
            alphaclops.measure(q0, q1, key='m'),
            alphaclops.X(q_result).with_classical_controls(sympy_parser.parse_expr('m % 4 <= 1')),
            alphaclops.measure(q_result, key='m_result'),
        )

        result = alphaclops.Simulator().run(circuit)
        assert result.measurements['m_result'][0][0] == (i % 4 <= 1)


def test_sympy_path_prefix():
    q = alphaclops.LineQubit(0)
    op = alphaclops.X(q).with_classical_controls(sympy.Symbol('b'))
    prefixed = alphaclops.with_key_path_prefix(op, ('0',))
    assert alphaclops.control_keys(prefixed) == {'0:b'}


def test_sympy_scope():
    q = alphaclops.LineQubit(0)
    a, b, c, d = sympy.symbols('a b c d')
    inner = alphaclops.Circuit(
        alphaclops.measure(q, key='a'),
        alphaclops.X(q).with_classical_controls(a & b).with_classical_controls(c | d),
    )
    middle = alphaclops.Circuit(
        alphaclops.measure(q, key='b'),
        alphaclops.measure(q, key=alphaclops.MeasurementKey('c', ('0',))),
        alphaclops.CircuitOperation(inner.freeze(), repetitions=2),
    )
    outer_subcircuit = alphaclops.CircuitOperation(middle.freeze(), repetitions=2)
    circuit = outer_subcircuit.mapped_circuit(deep=True)
    internal_controls = [str(k) for op in circuit.all_operations() for k in alphaclops.control_keys(op)]
    assert set(internal_controls) == {'0:0:a', '0:1:a', '1:0:a', '1:1:a', '0:b', '1:b', 'c', 'd'}
    assert alphaclops.control_keys(outer_subcircuit) == {'c', 'd'}
    assert alphaclops.control_keys(circuit) == {'c', 'd'}
    assert circuit == alphaclops.Circuit(alphaclops.decompose(outer_subcircuit))
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(outer_subcircuit),
        """
      [                      [ 0: ───M───X(conditions=[c | d, a & b])─── ]             ]
      [                      [       ║   ║                               ]             ]
      [                      [ a: ═══@═══^══════════════════════════════ ]             ]
      [                      [           ║                               ]             ]
      [ 0: ───M───M('0:c')───[ b: ═══════^══════════════════════════════ ]──────────── ]
      [       ║              [           ║                               ]             ]
      [       ║              [ c: ═══════^══════════════════════════════ ]             ]
0: ───[       ║              [           ║                               ]             ]────────────
      [       ║              [ d: ═══════^══════════════════════════════ ](loops=2)    ]
      [       ║              ║                                                         ]
      [ b: ═══@══════════════╬════════════════════════════════════════════════════════ ]
      [                      ║                                                         ]
      [ c: ══════════════════╬════════════════════════════════════════════════════════ ]
      [                      ║                                                         ]
      [ d: ══════════════════╩════════════════════════════════════════════════════════ ](loops=2)
      ║
c: ═══╬═════════════════════════════════════════════════════════════════════════════════════════════
      ║
d: ═══╩═════════════════════════════════════════════════════════════════════════════════════════════
""",
        use_unicode_characters=True,
    )

    # pylint: disable=line-too-long
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
0: ───────M───M('0:0:c')───M───X(conditions=[c | d, 0:0:a & 0:b])───M───X(conditions=[c | d, 0:1:a & 0:b])───M───M('1:0:c')───M───X(conditions=[c | d, 1:0:a & 1:b])───M───X(conditions=[c | d, 1:1:a & 1:b])───
          ║                ║   ║                                    ║   ║                                    ║                ║   ║                                    ║   ║
0:0:a: ═══╬════════════════@═══^════════════════════════════════════╬═══╬════════════════════════════════════╬════════════════╬═══╬════════════════════════════════════╬═══╬════════════════════════════════════
          ║                    ║                                    ║   ║                                    ║                ║   ║                                    ║   ║
0:1:a: ═══╬════════════════════╬════════════════════════════════════@═══^════════════════════════════════════╬════════════════╬═══╬════════════════════════════════════╬═══╬════════════════════════════════════
          ║                    ║                                        ║                                    ║                ║   ║                                    ║   ║
0:b: ═════@════════════════════^════════════════════════════════════════^════════════════════════════════════╬════════════════╬═══╬════════════════════════════════════╬═══╬════════════════════════════════════
                               ║                                        ║                                    ║                ║   ║                                    ║   ║
1:0:a: ════════════════════════╬════════════════════════════════════════╬════════════════════════════════════╬════════════════@═══^════════════════════════════════════╬═══╬════════════════════════════════════
                               ║                                        ║                                    ║                    ║                                    ║   ║
1:1:a: ════════════════════════╬════════════════════════════════════════╬════════════════════════════════════╬════════════════════╬════════════════════════════════════@═══^════════════════════════════════════
                               ║                                        ║                                    ║                    ║                                        ║
1:b: ══════════════════════════╬════════════════════════════════════════╬════════════════════════════════════@════════════════════^════════════════════════════════════════^════════════════════════════════════
                               ║                                        ║                                                         ║                                        ║
c: ════════════════════════════^════════════════════════════════════════^═════════════════════════════════════════════════════════^════════════════════════════════════════^════════════════════════════════════
                               ║                                        ║                                                         ║                                        ║
d: ════════════════════════════^════════════════════════════════════════^═════════════════════════════════════════════════════════^════════════════════════════════════════^════════════════════════════════════
""",
        use_unicode_characters=True,
    )
    # pylint: enable=line-too-long


def test_sympy_scope_simulation():
    q0, q1, q2, q3, q_ignored, q_result = alphaclops.LineQubit.range(6)
    condition = sympy_parser.parse_expr('a & b | c & d')
    # We set up condition (a & b | c & d) plus an ignored measurement key, and run through the
    # combinations of possible values of those (by doing X(q_i)**bits[i] on each), then verify
    # that the final measurement into m_result is True iff that condition was met.
    for i in range(32):
        bits = alphaclops.big_endian_int_to_bits(i, bit_count=5)
        inner = alphaclops.Circuit(
            alphaclops.X(q0) ** bits[0],
            alphaclops.measure(q0, key='a'),
            alphaclops.X(q_result).with_classical_controls(condition),
            alphaclops.measure(q_result, key='m_result'),
        )
        middle = alphaclops.Circuit(
            alphaclops.X(q1) ** bits[1],
            alphaclops.measure(q1, key='b'),
            alphaclops.X(q_ignored) ** bits[4],
            alphaclops.measure(q_ignored, key=alphaclops.MeasurementKey('c', ('0',))),
            alphaclops.CircuitOperation(inner.freeze(), repetition_ids=['0']),
        )
        circuit = alphaclops.Circuit(
            alphaclops.X(q2) ** bits[2],
            alphaclops.measure(q2, key='c'),
            alphaclops.X(q3) ** bits[3],
            alphaclops.measure(q3, key='d'),
            alphaclops.CircuitOperation(middle.freeze(), repetition_ids=['0']),
        )
        result = alphaclops.CliffordSimulator().run(circuit)
        assert result.measurements['0:0:m_result'][0][0] == (
            bits[0] and bits[1] or bits[2] and bits[3]  # bits[4] irrelevant
        )


def test_commutes():
    q0, q1 = alphaclops.LineQubit.range(2)
    assert alphaclops.commutes(alphaclops.measure(q0, key='a'), alphaclops.X(q1).with_classical_controls('b'))
    assert alphaclops.commutes(alphaclops.X(q1).with_classical_controls('b'), alphaclops.measure(q0, key='a'))
    assert alphaclops.commutes(
        alphaclops.X(q0).with_classical_controls('a'), alphaclops.H(q1).with_classical_controls('a')
    )
    assert alphaclops.commutes(
        alphaclops.X(q0).with_classical_controls('a'), alphaclops.X(q0).with_classical_controls('a')
    )
    assert not alphaclops.commutes(alphaclops.measure(q0, key='a'), alphaclops.X(q1).with_classical_controls('a'))
    assert not alphaclops.commutes(alphaclops.X(q1).with_classical_controls('a'), alphaclops.measure(q0, key='a'))
    assert not alphaclops.commutes(
        alphaclops.X(q0).with_classical_controls('a'), alphaclops.H(q0).with_classical_controls('a')
    )


def test_moment_diagram():
    a, _, c, d = alphaclops.TensorCircuit.rect(2, 2)
    m = alphaclops.Moment(alphaclops.CZ(a, d), alphaclops.X(c).with_classical_controls('m'))
    assert (
        str(m).strip()
        == """
  ╷ 0                 1
╶─┼─────────────────────
0 │ @─────────────────┐
  │                   │
1 │ X(conditions=[m]) @
  │
    """.strip()
    )
