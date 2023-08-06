# Copyright 2022 The alphaclops Developers
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

import alphaclops

NO_COMPILE_TAG = "no_compile_tag"


def test_leaves_big():
    a = alphaclops.NamedQubit('a')
    circuit = alphaclops.Circuit(alphaclops.Moment(alphaclops.Z(a) ** 0.1))
    alphaclops.testing.assert_same_circuits(alphaclops.drop_negligible_operations(circuit, atol=0.001), circuit)


def test_clears_small():
    a = alphaclops.NamedQubit('a')
    circuit = alphaclops.Circuit(alphaclops.Moment(alphaclops.Z(a) ** 0.000001))
    alphaclops.testing.assert_same_circuits(
        alphaclops.drop_negligible_operations(circuit, atol=0.001), alphaclops.Circuit(alphaclops.Moment())
    )


def test_does_not_clear_small_no_compile():
    a = alphaclops.NamedQubit('a')
    circuit = alphaclops.Circuit(alphaclops.Moment((alphaclops.Z(a) ** 0.000001).with_tags(NO_COMPILE_TAG)))
    alphaclops.testing.assert_same_circuits(
        alphaclops.drop_negligible_operations(
            circuit, context=alphaclops.TransformerContext(tags_to_ignore=(NO_COMPILE_TAG,)), atol=0.001
        ),
        circuit,
    )


def test_clears_known_empties_even_at_zero_tolerance():
    a, b = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.Z(a) ** 0, alphaclops.Y(a) ** 0.0000001, alphaclops.X(a) ** -0.0000001, alphaclops.CZ(a, b) ** 0
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.drop_negligible_operations(circuit, atol=0.001), alphaclops.Circuit([alphaclops.Moment()] * 4)
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.drop_negligible_operations(circuit, atol=0),
        alphaclops.Circuit(
            alphaclops.Moment(),
            alphaclops.Moment(alphaclops.Y(a) ** 0.0000001),
            alphaclops.Moment(alphaclops.X(a) ** -0.0000001),
            alphaclops.Moment(),
        ),
    )


def test_recursively_runs_inside_circuit_ops_deep():
    a = alphaclops.NamedQubit('a')
    small_op = alphaclops.Z(a) ** 0.000001
    nested_circuit = alphaclops.FrozenCircuit(
        alphaclops.X(a), small_op, small_op.with_tags(NO_COMPILE_TAG), small_op, alphaclops.Y(a)
    )
    nested_circuit_dropped = alphaclops.FrozenCircuit(
        alphaclops.Moment(alphaclops.X(a)),
        alphaclops.Moment(),
        alphaclops.Moment(small_op.with_tags(NO_COMPILE_TAG)),
        alphaclops.Moment(),
        alphaclops.Moment(alphaclops.Y(a)),
    )
    c_orig = alphaclops.Circuit(
        small_op,
        alphaclops.CircuitOperation(nested_circuit).repeat(6).with_tags(NO_COMPILE_TAG),
        small_op,
        alphaclops.CircuitOperation(nested_circuit).repeat(5).with_tags("preserve_tag"),
        small_op,
    )
    c_expected = alphaclops.Circuit(
        alphaclops.Moment(),
        alphaclops.Moment(alphaclops.CircuitOperation(nested_circuit).repeat(6).with_tags(NO_COMPILE_TAG)),
        alphaclops.Moment(),
        alphaclops.Moment(
            alphaclops.CircuitOperation(nested_circuit_dropped).repeat(5).with_tags("preserve_tag")
        ),
        alphaclops.Moment(),
    )
    context = alphaclops.TransformerContext(tags_to_ignore=[NO_COMPILE_TAG], deep=True)
    alphaclops.testing.assert_same_circuits(
        alphaclops.drop_negligible_operations(c_orig, context=context, atol=0.001), c_expected
    )


def test_ignores_large_ops():
    qnum = 20
    qubits = alphaclops.LineQubit.range(qnum)
    subcircuit = alphaclops.FrozenCircuit(alphaclops.X.on_each(*qubits))
    circuit = alphaclops.Circuit(
        alphaclops.CircuitOperation(subcircuit).repeat(10), alphaclops.measure(*qubits, key='out')
    )
    alphaclops.testing.assert_same_circuits(
        circuit,
        alphaclops.drop_negligible_operations(circuit, context=alphaclops.TransformerContext(deep=True)),
    )
