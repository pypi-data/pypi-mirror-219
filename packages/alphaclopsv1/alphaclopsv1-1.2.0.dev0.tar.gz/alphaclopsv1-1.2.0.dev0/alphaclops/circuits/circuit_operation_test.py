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
import unittest.mock as mock
from typing import Optional

import numpy as np
import pytest
import sympy

import alphaclops
import alphaclops.circuits.circuit_operation as circuit_operation
from alphaclops import _compat
from alphaclops.circuits.circuit_operation import _full_join_string_lists

ALL_SIMULATORS = (alphaclops.Simulator(), alphaclops.DensityMatrixSimulator(), alphaclops.CliffordSimulator())


def test_properties():
    a, b, c = alphaclops.LineQubit.range(3)
    circuit = alphaclops.FrozenCircuit(
        alphaclops.X(a),
        alphaclops.Y(b),
        alphaclops.H(c),
        alphaclops.CX(a, b) ** sympy.Symbol('exp'),
        alphaclops.measure(a, b, c, key='m'),
    )
    op = alphaclops.CircuitOperation(circuit)
    assert op.circuit is circuit
    assert op.qubits == (a, b, c)
    assert op.qubit_map == {}
    assert op.measurement_key_map == {}
    assert op.param_resolver == alphaclops.ParamResolver()
    assert op.repetitions == 1
    assert op.repetition_ids is None
    # Despite having the same decomposition, these objects are not equal.
    assert op != circuit
    assert op == circuit.to_op()


def test_circuit_type():
    a, b, c = alphaclops.LineQubit.range(3)
    circuit = alphaclops.Circuit(
        alphaclops.X(a),
        alphaclops.Y(b),
        alphaclops.H(c),
        alphaclops.CX(a, b) ** sympy.Symbol('exp'),
        alphaclops.measure(a, b, c, key='m'),
    )
    with pytest.raises(TypeError, match='Expected circuit of type FrozenCircuit'):
        _ = alphaclops.CircuitOperation(circuit)


def test_non_invertible_circuit():
    a, b, c = alphaclops.LineQubit.range(3)
    circuit = alphaclops.FrozenCircuit(
        alphaclops.X(a),
        alphaclops.Y(b),
        alphaclops.H(c),
        alphaclops.CX(a, b) ** sympy.Symbol('exp'),
        alphaclops.measure(a, b, c, key='m'),
    )
    with pytest.raises(ValueError, match='circuit is not invertible'):
        _ = alphaclops.CircuitOperation(circuit, repetitions=-2)


def test_repetitions_and_ids_length_mismatch():
    a, b, c = alphaclops.LineQubit.range(3)
    circuit = alphaclops.FrozenCircuit(
        alphaclops.X(a),
        alphaclops.Y(b),
        alphaclops.H(c),
        alphaclops.CX(a, b) ** sympy.Symbol('exp'),
        alphaclops.measure(a, b, c, key='m'),
    )
    with pytest.raises(ValueError, match='Expected repetition_ids to be a list of length 2'):
        _ = alphaclops.CircuitOperation(circuit, repetitions=2, repetition_ids=['a', 'b', 'c'])


def test_is_measurement_memoization():
    a = alphaclops.LineQubit(0)
    circuit = alphaclops.FrozenCircuit(alphaclops.measure(a, key='m'))
    c_op = alphaclops.CircuitOperation(circuit)
    cache_name = _compat._method_cache_name(circuit._is_measurement_)
    assert not hasattr(circuit, cache_name)
    # Memoize `_is_measurement_` in the circuit.
    assert alphaclops.is_measurement(c_op)
    assert hasattr(circuit, cache_name)


def test_invalid_measurement_keys():
    a = alphaclops.LineQubit(0)
    circuit = alphaclops.FrozenCircuit(alphaclops.measure(a, key='m'))
    c_op = alphaclops.CircuitOperation(circuit)
    # Invalid key remapping
    with pytest.raises(ValueError, match='Mapping to invalid key: m:a'):
        _ = c_op.with_measurement_key_mapping({'m': 'm:a'})

    # Invalid key remapping nested CircuitOperation
    with pytest.raises(ValueError, match='Mapping to invalid key: m:a'):
        _ = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(c_op), measurement_key_map={'m': 'm:a'})

    # Originally invalid key
    with pytest.raises(ValueError, match='Invalid key name: m:a'):
        _ = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.measure(a, key='m:a')))

    # Remapped to valid key
    _ = alphaclops.CircuitOperation(circuit, measurement_key_map={'m:a': 'ma'})


def test_invalid_qubit_mapping():
    q = alphaclops.LineQubit(0)
    q3 = alphaclops.LineQid(1, dimension=3)

    # Invalid qid remapping dict in constructor
    with pytest.raises(ValueError, match='Qid dimension conflict'):
        _ = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(), qubit_map={q: q3})

    # Invalid qid remapping dict in with_qubit_mapping call
    c_op = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.X(q)))
    with pytest.raises(ValueError, match='Qid dimension conflict'):
        _ = c_op.with_qubit_mapping({q: q3})

    # Invalid qid remapping function in with_qubit_mapping call
    with pytest.raises(ValueError, match='Qid dimension conflict'):
        _ = c_op.with_qubit_mapping(lambda q: q3)


def test_circuit_sharing():
    a, b, c = alphaclops.LineQubit.range(3)
    circuit = alphaclops.FrozenCircuit(
        alphaclops.X(a),
        alphaclops.Y(b),
        alphaclops.H(c),
        alphaclops.CX(a, b) ** sympy.Symbol('exp'),
        alphaclops.measure(a, b, c, key='m'),
    )
    op1 = alphaclops.CircuitOperation(circuit)
    op2 = alphaclops.CircuitOperation(op1.circuit)
    op3 = circuit.to_op()
    assert op1.circuit is circuit
    assert op2.circuit is circuit
    assert op3.circuit is circuit

    assert hash(op1) == hash(op2)
    assert hash(op1) == hash(op3)


def test_with_qubits():
    a, b, c, d = alphaclops.LineQubit.range(4)
    circuit = alphaclops.FrozenCircuit(alphaclops.H(a), alphaclops.CX(a, b))
    op_base = alphaclops.CircuitOperation(circuit)

    op_with_qubits = op_base.with_qubits(d, c)
    assert op_with_qubits.base_operation() == op_base
    assert op_with_qubits.qubits == (d, c)
    assert op_with_qubits.qubit_map == {a: d, b: c}

    assert op_base.with_qubit_mapping({a: d, b: c, d: a}) == op_with_qubits

    def map_fn(qubit: 'alphaclops.Qid') -> 'alphaclops.Qid':
        if qubit == a:
            return d
        if qubit == b:
            return c
        return qubit

    fn_op = op_base.with_qubit_mapping(map_fn)
    assert fn_op == op_with_qubits
    # map_fn does not affect qubits c and d.
    assert fn_op.with_qubit_mapping(map_fn) == op_with_qubits

    # with_qubits must receive the same number of qubits as the circuit contains.
    with pytest.raises(ValueError, match='Expected 2 qubits, got 3'):
        _ = op_base.with_qubits(c, d, b)

    # Two qubits cannot be mapped onto the same target qubit.
    with pytest.raises(ValueError, match='Collision in qubit map'):
        _ = op_base.with_qubit_mapping({a: b})

    # Two qubits cannot be transformed into the same target qubit.
    with pytest.raises(ValueError, match='Collision in qubit map'):
        _ = op_base.with_qubit_mapping(lambda q: b)
    # with_qubit_mapping requires exactly one argument.
    with pytest.raises(TypeError, match='must be a function or dict'):
        _ = op_base.with_qubit_mapping('bad arg')


def test_with_measurement_keys():
    a, b = alphaclops.LineQubit.range(2)
    circuit = alphaclops.FrozenCircuit(alphaclops.X(a), alphaclops.measure(b, key='mb'), alphaclops.measure(a, key='ma'))
    op_base = alphaclops.CircuitOperation(circuit)

    op_with_keys = op_base.with_measurement_key_mapping({'ma': 'pa', 'x': 'z'})
    assert op_with_keys.base_operation() == op_base
    assert op_with_keys.measurement_key_map == {'ma': 'pa'}
    assert alphaclops.measurement_key_names(op_with_keys) == {'pa', 'mb'}

    assert alphaclops.with_measurement_key_mapping(op_base, {'ma': 'pa'}) == op_with_keys

    # Two measurement keys cannot be mapped onto the same target string.
    with pytest.raises(ValueError):
        _ = op_base.with_measurement_key_mapping({'ma': 'mb'})


def test_with_params():
    a = alphaclops.LineQubit(0)
    z_exp = sympy.Symbol('z_exp')
    x_exp = sympy.Symbol('x_exp')
    delta = sympy.Symbol('delta')
    theta = sympy.Symbol('theta')
    circuit = alphaclops.FrozenCircuit(alphaclops.Z(a) ** z_exp, alphaclops.X(a) ** x_exp, alphaclops.Z(a) ** delta)
    op_base = alphaclops.CircuitOperation(circuit)

    param_dict = {z_exp: 2, x_exp: theta, sympy.Symbol('k'): sympy.Symbol('phi')}
    op_with_params = op_base.with_params(param_dict)
    assert op_with_params.base_operation() == op_base
    assert op_with_params.param_resolver == alphaclops.ParamResolver(
        {
            z_exp: 2,
            x_exp: theta,
            # As 'k' is irrelevant to the circuit, it does not appear here.
        }
    )
    assert alphaclops.parameter_names(op_with_params) == {'theta', 'delta'}

    assert (
            alphaclops.resolve_parameters(op_base, alphaclops.ParamResolver(param_dict), recursive=False)
            == op_with_params
    )


def test_recursive_params():
    q = alphaclops.LineQubit(0)
    a, a2, b, b2 = sympy.symbols('a a2 b b2')
    circuitop = alphaclops.CircuitOperation(
        alphaclops.FrozenCircuit(alphaclops.X(q) ** a, alphaclops.Z(q) ** b),
        # Not recursive, a and b are swapped.
        param_resolver=alphaclops.ParamResolver({a: b, b: a}),
    )
    # Recursive, so a->a2->0 and b->b2->1.
    outer_params = {a: a2, a2: 0, b: b2, b2: 1}
    resolved = alphaclops.resolve_parameters(circuitop, outer_params)
    # Combined, a->b->b2->1, and b->a->a2->0.
    assert resolved.param_resolver.param_dict == {a: 1, b: 0}

    # Non-recursive, so a->a2 and b->b2.
    resolved = alphaclops.resolve_parameters(circuitop, outer_params, recursive=False)
    # Combined, a->b->b2, and b->a->a2.
    assert resolved.param_resolver.param_dict == {a: b2, b: a2}

    with pytest.raises(RecursionError):
        alphaclops.resolve_parameters(circuitop, {a: a2, a2: a})

    # Non-recursive, so a->b and b->a.
    resolved = alphaclops.resolve_parameters(circuitop, {a: b, b: a}, recursive=False)
    # Combined, a->b->a, and b->a->b.
    assert resolved.param_resolver.param_dict == {}

    # First example should behave like an X when simulated
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(circuitop), param_resolver=outer_params)
    assert np.allclose(result.state_vector(), [0, 1])


@pytest.mark.parametrize('add_measurements', [True, False])
@pytest.mark.parametrize('use_default_ids_for_initial_rep', [True, False])
def test_repeat(add_measurements: bool, use_default_ids_for_initial_rep: bool) -> None:
    a, b = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(alphaclops.H(a), alphaclops.CX(a, b))
    if add_measurements:
        circuit.append([alphaclops.measure(b, key='mb'), alphaclops.measure(a, key='ma')])
    op_base = alphaclops.CircuitOperation(circuit.freeze())
    assert op_base.repeat(1) is op_base
    assert op_base.repeat(1, ['0']) != op_base
    assert op_base.repeat(1, ['0']) == op_base.repeat(repetition_ids=['0'])
    assert op_base.repeat(1, ['0']) == op_base.with_repetition_ids(['0'])

    initial_repetitions = -3
    if add_measurements:
        with pytest.raises(ValueError, match='circuit is not invertible'):
            _ = op_base.repeat(initial_repetitions)
        initial_repetitions = abs(initial_repetitions)

    op_with_reps: Optional[alphaclops.CircuitOperation] = None
    rep_ids = []
    if use_default_ids_for_initial_rep:
        op_with_reps = op_base.repeat(initial_repetitions)
        rep_ids = ['0', '1', '2']
        assert op_base**initial_repetitions == op_with_reps
    else:
        rep_ids = ['a', 'b', 'c']
        op_with_reps = op_base.repeat(initial_repetitions, rep_ids)
        assert op_base**initial_repetitions != op_with_reps
        assert (op_base**initial_repetitions).replace(repetition_ids=rep_ids) == op_with_reps
    assert op_with_reps.repetitions == initial_repetitions
    assert op_with_reps.repetition_ids == rep_ids
    assert op_with_reps.repeat(1) is op_with_reps

    final_repetitions = 2 * initial_repetitions

    op_with_consecutive_reps = op_with_reps.repeat(2)
    assert op_with_consecutive_reps.repetitions == final_repetitions
    assert op_with_consecutive_reps.repetition_ids == _full_join_string_lists(['0', '1'], rep_ids)
    assert op_base**final_repetitions != op_with_consecutive_reps

    op_with_consecutive_reps = op_with_reps.repeat(2, ['a', 'b'])
    assert op_with_reps.repeat(repetition_ids=['a', 'b']) == op_with_consecutive_reps
    assert op_with_consecutive_reps.repetitions == final_repetitions
    assert op_with_consecutive_reps.repetition_ids == _full_join_string_lists(['a', 'b'], rep_ids)

    with pytest.raises(ValueError, match='length to be 2'):
        _ = op_with_reps.repeat(2, ['a', 'b', 'c'])

    with pytest.raises(
        ValueError, match='At least one of repetitions and repetition_ids must be set'
    ):
        _ = op_base.repeat()

    with pytest.raises(TypeError, match='Only integer or sympy repetitions are allowed'):
        _ = op_base.repeat(1.3)  # type: ignore[arg-type]
    assert op_base.repeat(3.00000000001).repetitions == 3  # type: ignore[arg-type]
    assert op_base.repeat(2.99999999999).repetitions == 3  # type: ignore[arg-type]


@pytest.mark.parametrize('add_measurements', [True, False])
@pytest.mark.parametrize('use_repetition_ids', [True, False])
@pytest.mark.parametrize('initial_reps', [0, 1, 2, 3])
def test_repeat_zero_times(add_measurements, use_repetition_ids, initial_reps):
    q = alphaclops.LineQubit(0)
    subcircuit = alphaclops.Circuit(alphaclops.X(q))
    if add_measurements:
        subcircuit.append(alphaclops.measure(q))

    op = alphaclops.CircuitOperation(
        subcircuit.freeze(), repetitions=initial_reps, use_repetition_ids=use_repetition_ids
    )
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op))
    assert np.allclose(result.state_vector(), [0, 1] if initial_reps % 2 else [1, 0])
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op ** 0))
    assert np.allclose(result.state_vector(), [1, 0])


def test_no_repetition_ids():
    def default_repetition_ids(self):
        assert False, "Should not call default_repetition_ids"

    with mock.patch.object(circuit_operation, 'default_repetition_ids', new=default_repetition_ids):
        q = alphaclops.LineQubit(0)
        op = alphaclops.CircuitOperation(
            alphaclops.Circuit(alphaclops.X(q), alphaclops.measure(q)).freeze(),
            repetitions=1_000_000,
            use_repetition_ids=False,
        )
        assert op.repetitions == 1_000_000
        assert op.repetition_ids is None
        _ = repr(op)
        _ = str(op)

        op2 = op.repeat(10)
        assert op2.repetitions == 10_000_000
        assert op2.repetition_ids is None


def test_parameterized_repeat():
    q = alphaclops.LineQubit(0)
    op = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.X(q))) ** sympy.Symbol('a')
    assert alphaclops.parameter_names(op) == {'a'}
    assert not alphaclops.has_unitary(op)
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 0})
    assert np.allclose(result.state_vector(), [1, 0])
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 1})
    assert np.allclose(result.state_vector(), [0, 1])
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 2})
    assert np.allclose(result.state_vector(), [1, 0])
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': -1})
    assert np.allclose(result.state_vector(), [0, 1])
    with pytest.raises(TypeError, match='Only integer or sympy repetitions are allowed'):
        alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 1.5})
    with pytest.raises(ValueError, match='Circuit contains ops whose symbols were not specified'):
        alphaclops.Simulator().simulate(alphaclops.Circuit(op))
    op = op**-1
    assert alphaclops.parameter_names(op) == {'a'}
    assert not alphaclops.has_unitary(op)
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 0})
    assert np.allclose(result.state_vector(), [1, 0])
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 1})
    assert np.allclose(result.state_vector(), [0, 1])
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 2})
    assert np.allclose(result.state_vector(), [1, 0])
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': -1})
    assert np.allclose(result.state_vector(), [0, 1])
    with pytest.raises(TypeError, match='Only integer or sympy repetitions are allowed'):
        alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 1.5})
    with pytest.raises(ValueError, match='Circuit contains ops whose symbols were not specified'):
        alphaclops.Simulator().simulate(alphaclops.Circuit(op))
    op = op ** sympy.Symbol('b')
    assert alphaclops.parameter_names(op) == {'a', 'b'}
    assert not alphaclops.has_unitary(op)
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 1, 'b': 1})
    assert np.allclose(result.state_vector(), [0, 1])
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 2, 'b': 1})
    assert np.allclose(result.state_vector(), [1, 0])
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 1, 'b': 2})
    assert np.allclose(result.state_vector(), [1, 0])
    with pytest.raises(TypeError, match='Only integer or sympy repetitions are allowed'):
        alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 1.5, 'b': 1})
    with pytest.raises(ValueError, match='Circuit contains ops whose symbols were not specified'):
        alphaclops.Simulator().simulate(alphaclops.Circuit(op))
    op = op**2.0
    assert alphaclops.parameter_names(op) == {'a', 'b'}
    assert not alphaclops.has_unitary(op)
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 1, 'b': 1})
    assert np.allclose(result.state_vector(), [1, 0])
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 1.5, 'b': 1})
    assert np.allclose(result.state_vector(), [0, 1])
    result = alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 1, 'b': 1.5})
    assert np.allclose(result.state_vector(), [0, 1])
    with pytest.raises(TypeError, match='Only integer or sympy repetitions are allowed'):
        alphaclops.Simulator().simulate(alphaclops.Circuit(op), param_resolver={'a': 1.5, 'b': 1.5})
    with pytest.raises(ValueError, match='Circuit contains ops whose symbols were not specified'):
        alphaclops.Simulator().simulate(alphaclops.Circuit(op))


def test_parameterized_repeat_side_effects():
    q = alphaclops.LineQubit(0)
    op = alphaclops.CircuitOperation(
        alphaclops.FrozenCircuit(alphaclops.X(q).with_classical_controls('c'), alphaclops.measure(q, key='m')),
        repetitions=sympy.Symbol('a'),
    )

    # Control keys can be calculated because they only "lift" if there's a matching
    # measurement, in which case they're not returned here.
    assert alphaclops.control_keys(op) == {alphaclops.MeasurementKey('c')}

    # "local" params do not bind to the repetition param.
    assert alphaclops.parameter_names(op.with_params({'a': 1})) == {'a'}

    # Check errors that require unrolling the circuit.
    with pytest.raises(
        ValueError, match='Cannot unroll circuit due to nondeterministic repetitions'
    ):
        alphaclops.measurement_key_objs(op)
    with pytest.raises(
        ValueError, match='Cannot unroll circuit due to nondeterministic repetitions'
    ):
        alphaclops.measurement_key_names(op)
    with pytest.raises(
        ValueError, match='Cannot unroll circuit due to nondeterministic repetitions'
    ):
        op.mapped_circuit()
    with pytest.raises(
        ValueError, match='Cannot unroll circuit due to nondeterministic repetitions'
    ):
        alphaclops.decompose(op)

    # Not compatible with repetition ids
    with pytest.raises(ValueError, match='repetition ids with parameterized repetitions'):
        op.with_repetition_ids(['x', 'y'])
    with pytest.raises(ValueError, match='repetition ids with parameterized repetitions'):
        op.repeat(repetition_ids=['x', 'y'])

    # TODO(daxfohl): This should work, but likely requires a new protocol that returns *just* the
    # name of the measurement keys. (measurement_key_names returns the full serialized string).
    with pytest.raises(
        ValueError, match='Cannot unroll circuit due to nondeterministic repetitions'
    ):
        alphaclops.with_measurement_key_mapping(op, {'m': 'm2'})

    # Everything should work once resolved
    op = alphaclops.resolve_parameters(op, {'a': 2})
    assert set(map(str, alphaclops.measurement_key_objs(op))) == {'0:m', '1:m'}
    assert op.mapped_circuit() == alphaclops.Circuit(
        alphaclops.X(q).with_classical_controls('c'),
        alphaclops.measure(q, key=alphaclops.MeasurementKey.parse_serialized('0:m')),
        alphaclops.X(q).with_classical_controls('c'),
        alphaclops.measure(q, key=alphaclops.MeasurementKey.parse_serialized('1:m')),
    )
    assert alphaclops.decompose(op) == alphaclops.decompose(
        alphaclops.Circuit(
            alphaclops.X(q).with_classical_controls('c'),
            alphaclops.measure(q, key=alphaclops.MeasurementKey.parse_serialized('0:m')),
            alphaclops.X(q).with_classical_controls('c'),
            alphaclops.measure(q, key=alphaclops.MeasurementKey.parse_serialized('1:m')),
        )
    )


def test_parameterized_repeat_side_effects_when_not_using_rep_ids():
    q = alphaclops.LineQubit(0)
    op = alphaclops.CircuitOperation(
        alphaclops.FrozenCircuit(alphaclops.X(q).with_classical_controls('c'), alphaclops.measure(q, key='m')),
        repetitions=sympy.Symbol('a'),
        use_repetition_ids=False,
    )
    assert alphaclops.control_keys(op) == {alphaclops.MeasurementKey('c')}
    assert alphaclops.parameter_names(op.with_params({'a': 1})) == {'a'}
    assert set(map(str, alphaclops.measurement_key_objs(op))) == {'m'}
    assert alphaclops.measurement_key_names(op) == {'m'}
    assert alphaclops.measurement_key_names(alphaclops.with_measurement_key_mapping(op, {'m': 'm2'})) == {'m2'}
    with pytest.raises(
        ValueError, match='Cannot unroll circuit due to nondeterministic repetitions'
    ):
        op.mapped_circuit()
    with pytest.raises(
        ValueError, match='Cannot unroll circuit due to nondeterministic repetitions'
    ):
        alphaclops.decompose(op)
    with pytest.raises(ValueError, match='repetition ids with parameterized repetitions'):
        op.with_repetition_ids(['x', 'y'])
    with pytest.raises(ValueError, match='repetition ids with parameterized repetitions'):
        op.repeat(repetition_ids=['x', 'y'])


def test_qid_shape():
    circuit = alphaclops.FrozenCircuit(
        alphaclops.IdentityGate(qid_shape=(q.dimension,)).on(q)
        for q in alphaclops.LineQid.for_qid_shape((1, 2, 3, 4))
    )
    op = alphaclops.CircuitOperation(circuit)
    assert alphaclops.qid_shape(op) == (1, 2, 3, 4)
    assert alphaclops.num_qubits(op) == 4

    id_circuit = alphaclops.FrozenCircuit(alphaclops.I(q) for q in alphaclops.LineQubit.range(3))
    id_op = alphaclops.CircuitOperation(id_circuit)
    assert alphaclops.qid_shape(id_op) == (2, 2, 2)
    assert alphaclops.num_qubits(id_op) == 3


def test_string_format():
    x, y, z = alphaclops.LineQubit.range(3)

    fc0 = alphaclops.FrozenCircuit()
    op0 = alphaclops.CircuitOperation(fc0)
    assert str(op0) == "[  ]"

    fc0_global_phase_inner = alphaclops.FrozenCircuit(
        alphaclops.global_phase_operation(1j), alphaclops.global_phase_operation(1j)
    )
    op0_global_phase_inner = alphaclops.CircuitOperation(fc0_global_phase_inner)
    fc0_global_phase_outer = alphaclops.FrozenCircuit(
        op0_global_phase_inner, alphaclops.global_phase_operation(1j)
    )
    op0_global_phase_outer = alphaclops.CircuitOperation(fc0_global_phase_outer)
    assert (
        str(op0_global_phase_outer)
        == """\
[                       ]
[                       ]
[ global phase:   -0.5π ]"""
    )

    fc1 = alphaclops.FrozenCircuit(alphaclops.X(x), alphaclops.H(y), alphaclops.CX(y, z), alphaclops.measure(x, y, z, key='m'))
    op1 = alphaclops.CircuitOperation(fc1)
    assert (
        str(op1)
        == """\
[ 0: ───X───────M('m')─── ]
[               │         ]
[ 1: ───H───@───M──────── ]
[           │   │         ]
[ 2: ───────X───M──────── ]"""
    )
    assert (
        repr(op1)
        == """\
alphaclops.CircuitOperation(
    circuit=alphaclops.FrozenCircuit([
        alphaclops.Moment(
            alphaclops.X(alphaclops.LineQubit(0)),
            alphaclops.H(alphaclops.LineQubit(1)),
        ),
        alphaclops.Moment(
            alphaclops.CNOT(alphaclops.LineQubit(1), alphaclops.LineQubit(2)),
        ),
        alphaclops.Moment(
            alphaclops.measure(alphaclops.LineQubit(0), alphaclops.LineQubit(1), alphaclops.LineQubit(2), key=alphaclops.MeasurementKey(name='m')),
        ),
    ]),
)"""
    )

    fc2 = alphaclops.FrozenCircuit(alphaclops.X(x), alphaclops.H(y), alphaclops.CX(y, x))
    op2 = alphaclops.CircuitOperation(
        circuit=fc2,
        qubit_map=({y: z}),
        repetitions=3,
        parent_path=('outer', 'inner'),
        repetition_ids=['a', 'b', 'c'],
    )
    assert (
        str(op2)
        == """\
[ 0: ───X───X─── ]
[           │    ]
[ 1: ───H───@─── ](qubit_map={q(1): q(2)}, parent_path=('outer', 'inner'),\
 repetition_ids=['a', 'b', 'c'])"""
    )
    assert (
        repr(op2)
        == """\
alphaclops.CircuitOperation(
    circuit=alphaclops.FrozenCircuit([
        alphaclops.Moment(
            alphaclops.X(alphaclops.LineQubit(0)),
            alphaclops.H(alphaclops.LineQubit(1)),
        ),
        alphaclops.Moment(
            alphaclops.CNOT(alphaclops.LineQubit(1), alphaclops.LineQubit(0)),
        ),
    ]),
    repetitions=3,
    qubit_map={alphaclops.LineQubit(1): alphaclops.LineQubit(2)},
    parent_path=('outer', 'inner'),
    repetition_ids=['a', 'b', 'c'],
)"""
    )

    fc3 = alphaclops.FrozenCircuit(alphaclops.X(x) ** sympy.Symbol('b'), alphaclops.measure(x, key='m'))
    op3 = alphaclops.CircuitOperation(
        circuit=fc3,
        qubit_map={x: y},
        measurement_key_map={'m': 'p'},
        param_resolver={sympy.Symbol('b'): 2},
    )
    indented_fc3_repr = repr(fc3).replace('\n', '\n    ')
    assert (
        str(op3)
        == """\
[ 0: ───X^b───M('m')─── ](qubit_map={q(0): q(1)}, \
key_map={m: p}, params={b: 2})"""
    )
    assert (
        repr(op3)
        == f"""\
alphaclops.CircuitOperation(
    circuit={indented_fc3_repr},
    qubit_map={{alphaclops.LineQubit(0): alphaclops.LineQubit(1)}},
    measurement_key_map={{'m': 'p'}},
    param_resolver=alphaclops.ParamResolver({{sympy.Symbol('b'): 2}}),
)"""
    )

    fc4 = alphaclops.FrozenCircuit(alphaclops.X(y))
    op4 = alphaclops.CircuitOperation(fc4)
    fc5 = alphaclops.FrozenCircuit(alphaclops.X(x), op4)
    op5 = alphaclops.CircuitOperation(fc5)
    assert (
        repr(op5)
        == """\
alphaclops.CircuitOperation(
    circuit=alphaclops.FrozenCircuit([
        alphaclops.Moment(
            alphaclops.X(alphaclops.LineQubit(0)),
            alphaclops.CircuitOperation(
                circuit=alphaclops.FrozenCircuit([
                    alphaclops.Moment(
                        alphaclops.X(alphaclops.LineQubit(1)),
                    ),
                ]),
            ),
        ),
    ]),
)"""
    )
    op6 = alphaclops.CircuitOperation(fc5, use_repetition_ids=False)
    assert (
        repr(op6)
        == """\
alphaclops.CircuitOperation(
    circuit=alphaclops.FrozenCircuit([
        alphaclops.Moment(
            alphaclops.X(alphaclops.LineQubit(0)),
            alphaclops.CircuitOperation(
                circuit=alphaclops.FrozenCircuit([
                    alphaclops.Moment(
                        alphaclops.X(alphaclops.LineQubit(1)),
                    ),
                ]),
            ),
        ),
    ]),
    use_repetition_ids=False,
)"""
    )
    op7 = alphaclops.CircuitOperation(
        alphaclops.FrozenCircuit(alphaclops.measure(x, key='a')),
        use_repetition_ids=False,
        repeat_until=alphaclops.KeyCondition(alphaclops.MeasurementKey('a')),
    )
    assert (
        repr(op7)
        == """\
alphaclops.CircuitOperation(
    circuit=alphaclops.FrozenCircuit([
        alphaclops.Moment(
            alphaclops.measure(alphaclops.LineQubit(0), key=alphaclops.MeasurementKey(name='a')),
        ),
    ]),
    use_repetition_ids=False,
    repeat_until=alphaclops.KeyCondition(alphaclops.MeasurementKey(name='a')),
)"""
    )


def test_json_dict():
    a, b, c = alphaclops.LineQubit.range(3)
    circuit = alphaclops.FrozenCircuit(
        alphaclops.X(a),
        alphaclops.Y(b),
        alphaclops.H(c),
        alphaclops.CX(a, b) ** sympy.Symbol('exp'),
        alphaclops.measure(a, b, c, key='m'),
    )
    op = alphaclops.CircuitOperation(
        circuit=circuit,
        qubit_map={c: b, b: c},
        measurement_key_map={'m': 'p'},
        param_resolver={'exp': 'theta'},
        parent_path=('nested', 'path'),
    )

    assert op._json_dict_() == {
        'circuit': circuit,
        'repetitions': 1,
        'qubit_map': sorted([(k, v) for k, v in op.qubit_map.items()]),
        'measurement_key_map': op.measurement_key_map,
        'param_resolver': op.param_resolver,
        'parent_path': op.parent_path,
        'repetition_ids': None,
    }


def test_terminal_matches():
    a, b = alphaclops.LineQubit.range(2)
    fc = alphaclops.FrozenCircuit(alphaclops.H(a), alphaclops.measure(b, key='m1'))
    op = alphaclops.CircuitOperation(fc)

    c = alphaclops.Circuit(alphaclops.X(a), op)
    assert c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = alphaclops.Circuit(alphaclops.X(b), op)
    assert c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = alphaclops.Circuit(alphaclops.measure(a), op)
    assert not c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = alphaclops.Circuit(alphaclops.measure(b), op)
    assert not c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = alphaclops.Circuit(op, alphaclops.X(a))
    assert c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = alphaclops.Circuit(op, alphaclops.X(b))
    assert not c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()

    c = alphaclops.Circuit(op, alphaclops.measure(a))
    assert c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()

    c = alphaclops.Circuit(op, alphaclops.measure(b))
    assert not c.are_all_measurements_terminal()
    assert c.are_any_measurements_terminal()


def test_nonterminal_in_subcircuit():
    a, b = alphaclops.LineQubit.range(2)
    fc = alphaclops.FrozenCircuit(alphaclops.H(a), alphaclops.measure(b, key='m1'), alphaclops.X(b))
    op = alphaclops.CircuitOperation(fc)
    c = alphaclops.Circuit(alphaclops.X(a), op)
    assert isinstance(op, alphaclops.CircuitOperation)
    assert not c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()

    op = op.with_tags('test')
    c = alphaclops.Circuit(alphaclops.X(a), op)
    assert not isinstance(op, alphaclops.CircuitOperation)
    assert not c.are_all_measurements_terminal()
    assert not c.are_any_measurements_terminal()


def test_decompose_applies_maps():
    a, b, c = alphaclops.LineQubit.range(3)
    exp = sympy.Symbol('exp')
    theta = sympy.Symbol('theta')
    circuit = alphaclops.FrozenCircuit(
        alphaclops.X(a) ** theta,
        alphaclops.Y(b),
        alphaclops.H(c),
        alphaclops.CX(a, b) ** exp,
        alphaclops.measure(a, b, c, key='m'),
    )
    op = alphaclops.CircuitOperation(
        circuit=circuit,
        qubit_map={c: b, b: c},
        measurement_key_map={'m': 'p'},
        param_resolver={exp: theta, theta: exp},
    )

    expected_circuit = alphaclops.Circuit(
        alphaclops.X(a) ** exp,
        alphaclops.Y(c),
        alphaclops.H(b),
        alphaclops.CX(a, c) ** theta,
        alphaclops.measure(a, c, b, key='p'),
    )
    assert alphaclops.Circuit(alphaclops.decompose_once(op)) == expected_circuit


def test_decompose_loops():
    a, b = alphaclops.LineQubit.range(2)
    circuit = alphaclops.FrozenCircuit(alphaclops.H(a), alphaclops.CX(a, b))
    base_op = alphaclops.CircuitOperation(circuit)

    op = base_op.with_qubits(b, a).repeat(3)
    expected_circuit = alphaclops.Circuit(
        alphaclops.H(b), alphaclops.CX(b, a), alphaclops.H(b), alphaclops.CX(b, a), alphaclops.H(b), alphaclops.CX(b, a)
    )
    assert alphaclops.Circuit(alphaclops.decompose_once(op)) == expected_circuit

    op = base_op.repeat(-2)
    expected_circuit = alphaclops.Circuit(alphaclops.CX(a, b), alphaclops.H(a), alphaclops.CX(a, b), alphaclops.H(a))
    assert alphaclops.Circuit(alphaclops.decompose_once(op)) == expected_circuit


def test_decompose_loops_with_measurements():
    a, b = alphaclops.LineQubit.range(2)
    circuit = alphaclops.FrozenCircuit(alphaclops.H(a), alphaclops.CX(a, b), alphaclops.measure(a, b, key='m'))
    base_op = alphaclops.CircuitOperation(circuit)

    op = base_op.with_qubits(b, a).repeat(3)
    expected_circuit = alphaclops.Circuit(
        alphaclops.H(b),
        alphaclops.CX(b, a),
        alphaclops.measure(b, a, key=alphaclops.MeasurementKey.parse_serialized('0:m')),
        alphaclops.H(b),
        alphaclops.CX(b, a),
        alphaclops.measure(b, a, key=alphaclops.MeasurementKey.parse_serialized('1:m')),
        alphaclops.H(b),
        alphaclops.CX(b, a),
        alphaclops.measure(b, a, key=alphaclops.MeasurementKey.parse_serialized('2:m')),
    )
    assert alphaclops.Circuit(alphaclops.decompose_once(op)) == expected_circuit


def test_decompose_nested():
    a, b, c, d = alphaclops.LineQubit.range(4)
    exp1 = sympy.Symbol('exp1')
    exp_half = sympy.Symbol('exp_half')
    exp_one = sympy.Symbol('exp_one')
    exp_two = sympy.Symbol('exp_two')
    circuit1 = alphaclops.FrozenCircuit(alphaclops.X(a) ** exp1, alphaclops.measure(a, key='m1'))
    op1 = alphaclops.CircuitOperation(circuit1)
    circuit2 = alphaclops.FrozenCircuit(
        op1.with_qubits(a).with_measurement_key_mapping({'m1': 'ma'}),
        op1.with_qubits(b).with_measurement_key_mapping({'m1': 'mb'}),
        op1.with_qubits(c).with_measurement_key_mapping({'m1': 'mc'}),
        op1.with_qubits(d).with_measurement_key_mapping({'m1': 'md'}),
    )
    op2 = alphaclops.CircuitOperation(circuit2)
    circuit3 = alphaclops.FrozenCircuit(
        op2.with_params({exp1: exp_half}),
        op2.with_params({exp1: exp_one})
        .with_measurement_key_mapping({'ma': 'ma1'})
        .with_measurement_key_mapping({'mb': 'mb1'})
        .with_measurement_key_mapping({'mc': 'mc1'})
        .with_measurement_key_mapping({'md': 'md1'}),
        op2.with_params({exp1: exp_two})
        .with_measurement_key_mapping({'ma': 'ma2'})
        .with_measurement_key_mapping({'mb': 'mb2'})
        .with_measurement_key_mapping({'mc': 'mc2'})
        .with_measurement_key_mapping({'md': 'md2'}),
    )
    op3 = alphaclops.CircuitOperation(circuit3)

    final_op = op3.with_params({exp_half: 0.5, exp_one: 1.0, exp_two: 2.0})

    expected_circuit1 = alphaclops.Circuit(
        op2.with_params({exp1: 0.5, exp_half: 0.5, exp_one: 1.0, exp_two: 2.0}),
        op2.with_params({exp1: 1.0, exp_half: 0.5, exp_one: 1.0, exp_two: 2.0})
        .with_measurement_key_mapping({'ma': 'ma1'})
        .with_measurement_key_mapping({'mb': 'mb1'})
        .with_measurement_key_mapping({'mc': 'mc1'})
        .with_measurement_key_mapping({'md': 'md1'}),
        op2.with_params({exp1: 2.0, exp_half: 0.5, exp_one: 1.0, exp_two: 2.0})
        .with_measurement_key_mapping({'ma': 'ma2'})
        .with_measurement_key_mapping({'mb': 'mb2'})
        .with_measurement_key_mapping({'mc': 'mc2'})
        .with_measurement_key_mapping({'md': 'md2'}),
    )

    result_ops1 = alphaclops.decompose_once(final_op)
    assert alphaclops.Circuit(result_ops1) == expected_circuit1

    expected_circuit = alphaclops.Circuit(
        alphaclops.X(a) ** 0.5,
        alphaclops.measure(a, key='ma'),
        alphaclops.X(b) ** 0.5,
        alphaclops.measure(b, key='mb'),
        alphaclops.X(c) ** 0.5,
        alphaclops.measure(c, key='mc'),
        alphaclops.X(d) ** 0.5,
        alphaclops.measure(d, key='md'),
        alphaclops.X(a) ** 1.0,
        alphaclops.measure(a, key='ma1'),
        alphaclops.X(b) ** 1.0,
        alphaclops.measure(b, key='mb1'),
        alphaclops.X(c) ** 1.0,
        alphaclops.measure(c, key='mc1'),
        alphaclops.X(d) ** 1.0,
        alphaclops.measure(d, key='md1'),
        alphaclops.X(a) ** 2.0,
        alphaclops.measure(a, key='ma2'),
        alphaclops.X(b) ** 2.0,
        alphaclops.measure(b, key='mb2'),
        alphaclops.X(c) ** 2.0,
        alphaclops.measure(c, key='mc2'),
        alphaclops.X(d) ** 2.0,
        alphaclops.measure(d, key='md2'),
    )
    assert alphaclops.Circuit(alphaclops.decompose(final_op)) == expected_circuit
    # Verify that mapped_circuit gives the same operations.
    assert final_op.mapped_circuit(deep=True) == expected_circuit


def test_decompose_repeated_nested_measurements():
    # Details of this test described at
    # https://tinyurl.com/measurement-repeated-circuitop#heading=h.sbgxcsyin9wt.
    a = alphaclops.LineQubit(0)

    op1 = (
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.measure(a, key='A')))
        .with_measurement_key_mapping({'A': 'B'})
        .repeat(2, ['zero', 'one'])
    )

    op2 = (
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.measure(a, key='P'), op1))
        .with_measurement_key_mapping({'B': 'C', 'P': 'Q'})
        .repeat(2, ['zero', 'one'])
    )

    op3 = (
        alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.measure(a, key='X'), op2))
        .with_measurement_key_mapping({'C': 'D', 'X': 'Y'})
        .repeat(2, ['zero', 'one'])
    )

    expected_measurement_keys_in_order = [
        'zero:Y',
        'zero:zero:Q',
        'zero:zero:zero:D',
        'zero:zero:one:D',
        'zero:one:Q',
        'zero:one:zero:D',
        'zero:one:one:D',
        'one:Y',
        'one:zero:Q',
        'one:zero:zero:D',
        'one:zero:one:D',
        'one:one:Q',
        'one:one:zero:D',
        'one:one:one:D',
    ]
    assert alphaclops.measurement_key_names(op3) == set(expected_measurement_keys_in_order)

    expected_circuit = alphaclops.Circuit()
    for key in expected_measurement_keys_in_order:
        expected_circuit.append(alphaclops.measure(a, key=alphaclops.MeasurementKey.parse_serialized(key)))

    assert alphaclops.Circuit(alphaclops.decompose(op3)) == expected_circuit
    assert alphaclops.measurement_key_names(expected_circuit) == set(expected_measurement_keys_in_order)

    # Verify that mapped_circuit gives the same operations.
    assert op3.mapped_circuit(deep=True) == expected_circuit


def test_keys_under_parent_path():
    a = alphaclops.LineQubit(0)
    op1 = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.measure(a, key='A')))
    assert alphaclops.measurement_key_names(op1) == {'A'}
    op2 = op1.with_key_path(('B',))
    assert alphaclops.measurement_key_names(op2) == {'B:A'}
    op3 = alphaclops.with_key_path_prefix(op2, ('C',))
    assert alphaclops.measurement_key_names(op3) == {'C:B:A'}
    op4 = op3.repeat(2)
    assert alphaclops.measurement_key_names(op4) == {'C:B:0:A', 'C:B:1:A'}


def test_mapped_circuit_preserves_moments():
    q0, q1 = alphaclops.LineQubit.range(2)
    fc = alphaclops.FrozenCircuit(alphaclops.Moment(alphaclops.X(q0)), alphaclops.Moment(alphaclops.X(q1)))
    op = alphaclops.CircuitOperation(fc)
    assert op.mapped_circuit() == fc
    assert op.repeat(3).mapped_circuit(deep=True) == fc * 3


def test_mapped_op():
    q0, q1 = alphaclops.LineQubit.range(2)
    a, b = (sympy.Symbol(x) for x in 'ab')
    fc1 = alphaclops.FrozenCircuit(alphaclops.X(q0) ** a, alphaclops.measure(q0, q1, key='m'))
    op1 = (
        alphaclops.CircuitOperation(fc1)
        .with_params({'a': 'b'})
        .with_qubits(q1, q0)
        .with_measurement_key_mapping({'m': 'k'})
    )
    fc2 = alphaclops.FrozenCircuit(alphaclops.X(q1) ** b, alphaclops.measure(q1, q0, key='k'))
    op2 = alphaclops.CircuitOperation(fc2)

    assert op1.mapped_op() == op2


def test_tag_propagation():
    # Tags are not propagated from the CircuitOperation to its components.
    # TODO: support tag propagation for better serialization.
    a, b, c = alphaclops.LineQubit.range(3)
    circuit = alphaclops.FrozenCircuit(alphaclops.X(a), alphaclops.H(b), alphaclops.H(c), alphaclops.CZ(a, c))
    op = alphaclops.CircuitOperation(circuit)
    test_tag = 'test_tag'
    op = op.with_tags(test_tag)

    assert test_tag in op.tags

    # TODO: Tags must propagate during decomposition.
    sub_ops = alphaclops.decompose(op)
    for op in sub_ops:
        assert test_tag not in op.tags


def test_mapped_circuit_keeps_keys_under_parent_path():
    q = alphaclops.LineQubit(0)
    op1 = alphaclops.CircuitOperation(
        alphaclops.FrozenCircuit(
            alphaclops.measure(q, key='A'),
            alphaclops.measure_single_paulistring(alphaclops.X(q), key='B'),
            alphaclops.MixedUnitaryChannel.from_mixture(alphaclops.bit_flip(0.5), key='C').on(q),
            alphaclops.KrausChannel.from_channel(alphaclops.phase_damp(0.5), key='D').on(q),
        )
    )
    op2 = op1.with_key_path(('X',))
    assert alphaclops.measurement_key_names(op2.mapped_circuit()) == {'X:A', 'X:B', 'X:C', 'X:D'}


def test_mapped_circuit_allows_repeated_keys():
    q = alphaclops.LineQubit(0)
    op1 = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(alphaclops.measure(q, key='A')))
    op2 = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(op1, op1))
    circuit = op2.mapped_circuit(deep=True)
    alphaclops.testing.assert_has_diagram(
        circuit, "0: ───M('A')───M('A')───", use_unicode_characters=True
    )
    op1 = alphaclops.measure(q, key='A')
    op2 = alphaclops.CircuitOperation(alphaclops.FrozenCircuit(op1, op1))
    circuit = op2.mapped_circuit()
    alphaclops.testing.assert_has_diagram(
        circuit, "0: ───M('A')───M('A')───", use_unicode_characters=True
    )


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_simulate_no_repetition_ids_both_levels(sim):
    q = alphaclops.LineQubit(0)
    inner = alphaclops.Circuit(alphaclops.measure(q, key='a'))
    middle = alphaclops.Circuit(
        alphaclops.CircuitOperation(inner.freeze(), repetitions=2, use_repetition_ids=False)
    )
    outer_subcircuit = alphaclops.CircuitOperation(
        middle.freeze(), repetitions=2, use_repetition_ids=False
    )
    circuit = alphaclops.Circuit(outer_subcircuit)
    result = sim.run(circuit)
    assert result.records['a'].shape == (1, 4, 1)


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_simulate_no_repetition_ids_outer(sim):
    q = alphaclops.LineQubit(0)
    inner = alphaclops.Circuit(alphaclops.measure(q, key='a'))
    middle = alphaclops.Circuit(alphaclops.CircuitOperation(inner.freeze(), repetitions=2))
    outer_subcircuit = alphaclops.CircuitOperation(
        middle.freeze(), repetitions=2, use_repetition_ids=False
    )
    circuit = alphaclops.Circuit(outer_subcircuit)
    result = sim.run(circuit)
    assert result.records['0:a'].shape == (1, 2, 1)
    assert result.records['1:a'].shape == (1, 2, 1)


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_simulate_no_repetition_ids_inner(sim):
    q = alphaclops.LineQubit(0)
    inner = alphaclops.Circuit(alphaclops.measure(q, key='a'))
    middle = alphaclops.Circuit(
        alphaclops.CircuitOperation(inner.freeze(), repetitions=2, use_repetition_ids=False)
    )
    outer_subcircuit = alphaclops.CircuitOperation(middle.freeze(), repetitions=2)
    circuit = alphaclops.Circuit(outer_subcircuit)
    result = sim.run(circuit)
    assert result.records['0:a'].shape == (1, 2, 1)
    assert result.records['1:a'].shape == (1, 2, 1)


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_repeat_until(sim):
    q = alphaclops.LineQubit(0)
    key = alphaclops.MeasurementKey('m')
    c = alphaclops.Circuit(
        alphaclops.X(q),
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.X(q), alphaclops.measure(q, key=key)),
            use_repetition_ids=False,
            repeat_until=alphaclops.KeyCondition(key),
        ),
    )
    measurements = sim.run(c).records['m'][0]
    assert len(measurements) == 2
    assert measurements[0] == (0,)
    assert measurements[1] == (1,)


@pytest.mark.parametrize('sim', ALL_SIMULATORS)
def test_repeat_until_sympy(sim):
    q1, q2 = alphaclops.LineQubit.range(2)
    circuitop = alphaclops.CircuitOperation(
        alphaclops.FrozenCircuit(alphaclops.X(q2), alphaclops.measure(q2, key='b')),
        use_repetition_ids=False,
        repeat_until=alphaclops.SympyCondition(sympy.Eq(sympy.Symbol('a'), sympy.Symbol('b'))),
    )
    c = alphaclops.Circuit(alphaclops.measure(q1, key='a'), circuitop)
    # Validate commutation
    assert len(c) == 2
    assert alphaclops.control_keys(circuitop) == {alphaclops.MeasurementKey('a')}
    measurements = sim.run(c).records['b'][0]
    assert len(measurements) == 2
    assert measurements[0] == (1,)
    assert measurements[1] == (0,)


@pytest.mark.parametrize('sim', [alphaclops.Simulator(), alphaclops.DensityMatrixSimulator()])
def test_post_selection(sim):
    q = alphaclops.LineQubit(0)
    key = alphaclops.MeasurementKey('m')
    c = alphaclops.Circuit(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.X(q) ** 0.2, alphaclops.measure(q, key=key)),
            use_repetition_ids=False,
            repeat_until=alphaclops.KeyCondition(key),
        )
    )
    result = sim.run(c)
    assert result.records['m'][0][-1] == (1,)
    for i in range(len(result.records['m'][0]) - 1):
        assert result.records['m'][0][i] == (0,)


def test_repeat_until_diagram():
    q = alphaclops.LineQubit(0)
    key = alphaclops.MeasurementKey('m')
    c = alphaclops.Circuit(
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.X(q) ** 0.2, alphaclops.measure(q, key=key)),
            use_repetition_ids=False,
            repeat_until=alphaclops.KeyCondition(key),
        )
    )
    alphaclops.testing.assert_has_diagram(
        c,
        """
0: ───[ 0: ───X^0.2───M('m')─── ](no_rep_ids, until=m)───
""",
        use_unicode_characters=True,
    )


def test_repeat_until_error():
    q = alphaclops.LineQubit(0)
    with pytest.raises(ValueError, match='Cannot use repetitions with repeat_until'):
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(),
            use_repetition_ids=True,
            repeat_until=alphaclops.KeyCondition(alphaclops.MeasurementKey('a')),
        )
    with pytest.raises(ValueError, match='Infinite loop'):
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(alphaclops.measure(q, key='m')),
            use_repetition_ids=False,
            repeat_until=alphaclops.KeyCondition(alphaclops.MeasurementKey('a')),
        )


# TODO: Operation has a "gate" property. What is this for a CircuitOperation?
