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

"""Tests for the expand composite transformer pass."""

import alphaclops


def assert_equal_mod_empty(expected, actual):
    actual = alphaclops.drop_empty_moments(actual)
    alphaclops.testing.assert_same_circuits(actual, expected)


def test_empty_circuit():
    circuit = alphaclops.Circuit()
    circuit = alphaclops.expand_composite(circuit)
    assert_equal_mod_empty(alphaclops.Circuit(), circuit)


def test_empty_moment():
    circuit = alphaclops.Circuit([])
    circuit = alphaclops.expand_composite(circuit)
    assert_equal_mod_empty(alphaclops.Circuit([]), circuit)


def test_ignore_non_composite():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit()
    circuit.append([alphaclops.X(q0), alphaclops.Y(q1), alphaclops.CZ(q0, q1), alphaclops.Z(q0)])
    expected = circuit.copy()
    circuit = alphaclops.expand_composite(circuit)
    assert_equal_mod_empty(expected, circuit)


def test_composite_default():
    q0, q1 = alphaclops.LineQubit.range(2)
    cnot = alphaclops.CNOT(q0, q1)
    circuit = alphaclops.Circuit()
    circuit.append(cnot)
    circuit = alphaclops.expand_composite(circuit)
    expected = alphaclops.Circuit()
    expected.append([alphaclops.Y(q1) ** -0.5, alphaclops.CZ(q0, q1), alphaclops.Y(q1) ** 0.5])
    assert_equal_mod_empty(expected, circuit)


def test_multiple_composite_default():
    q0, q1 = alphaclops.LineQubit.range(2)
    cnot = alphaclops.CNOT(q0, q1)
    circuit = alphaclops.Circuit()
    circuit.append([cnot, cnot])
    circuit = alphaclops.expand_composite(circuit)
    expected = alphaclops.Circuit()
    decomp = [alphaclops.Y(q1) ** -0.5, alphaclops.CZ(q0, q1), alphaclops.Y(q1) ** 0.5]
    expected.append([decomp, decomp])
    assert_equal_mod_empty(expected, circuit)


def test_mix_composite_non_composite():
    q0, q1 = alphaclops.LineQubit.range(2)

    circuit = alphaclops.Circuit(alphaclops.X(q0), alphaclops.CNOT(q0, q1), alphaclops.X(q1))
    circuit = alphaclops.expand_composite(circuit)

    expected = alphaclops.Circuit(
        alphaclops.X(q0),
        alphaclops.Y(q1) ** -0.5,
        alphaclops.CZ(q0, q1),
        alphaclops.Y(q1) ** 0.5,
        alphaclops.X(q1),
        strategy=alphaclops.InsertStrategy.NEW,
    )
    assert_equal_mod_empty(expected, circuit)


def test_recursive_composite():
    q0, q1 = alphaclops.LineQubit.range(2)
    swap = alphaclops.SWAP(q0, q1)
    circuit = alphaclops.Circuit()
    circuit.append(swap)

    circuit = alphaclops.expand_composite(circuit)
    expected = alphaclops.Circuit(
        alphaclops.Y(q1) ** -0.5,
        alphaclops.CZ(q0, q1),
        alphaclops.Y(q1) ** 0.5,
        alphaclops.Y(q0) ** -0.5,
        alphaclops.CZ(q1, q0),
        alphaclops.Y(q0) ** 0.5,
        alphaclops.Y(q1) ** -0.5,
        alphaclops.CZ(q0, q1),
        alphaclops.Y(q1) ** 0.5,
    )
    assert_equal_mod_empty(expected, circuit)


def test_decompose_returns_not_flat_op_tree():
    class DummyGate(alphaclops.testing.SingleQubitGate):
        def _decompose_(self, qubits):
            (q0,) = qubits
            # Yield a tuple of gates instead of yielding a gate
            yield alphaclops.X(q0),

    q0 = alphaclops.NamedQubit('q0')
    circuit = alphaclops.Circuit(DummyGate()(q0))

    circuit = alphaclops.expand_composite(circuit)
    expected = alphaclops.Circuit(alphaclops.X(q0))
    assert_equal_mod_empty(expected, circuit)


def test_decompose_returns_deep_op_tree():
    class DummyGate(alphaclops.testing.TwoQubitGate):
        def _decompose_(self, qubits):
            q0, q1 = qubits
            # Yield a tuple
            yield ((alphaclops.X(q0), alphaclops.Y(q0)), alphaclops.Z(q0))
            # Yield nested lists
            yield [alphaclops.X(q0), [alphaclops.Y(q0), alphaclops.Z(q0)]]

            def generator(depth):
                if depth <= 0:
                    yield alphaclops.CZ(q0, q1), alphaclops.Y(q0)
                else:
                    yield alphaclops.X(q0), generator(depth - 1)
                    yield alphaclops.Z(q0)

            # Yield nested generators
            yield generator(2)

    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(DummyGate()(q0, q1))

    circuit = alphaclops.expand_composite(circuit)
    expected = alphaclops.Circuit(
        alphaclops.X(q0),
        alphaclops.Y(q0),
        alphaclops.Z(q0),  # From tuple
        alphaclops.X(q0),
        alphaclops.Y(q0),
        alphaclops.Z(q0),  # From nested lists
        # From nested generators
        alphaclops.X(q0),
        alphaclops.X(q0),
        alphaclops.CZ(q0, q1),
        alphaclops.Y(q0),
        alphaclops.Z(q0),
        alphaclops.Z(q0),
    )
    assert_equal_mod_empty(expected, circuit)


def test_non_recursive_expansion():
    qubits = [alphaclops.NamedQubit(s) for s in 'xy']
    no_decomp = lambda op: (isinstance(op, alphaclops.GateOperation) and op.gate == alphaclops.ISWAP)
    unexpanded_circuit = alphaclops.Circuit(alphaclops.ISWAP(*qubits))

    circuit = alphaclops.expand_composite(unexpanded_circuit, no_decomp=no_decomp)
    assert circuit == unexpanded_circuit

    no_decomp = lambda op: (
        isinstance(op, alphaclops.GateOperation)
        and isinstance(op.gate, (alphaclops.CNotPowGate, alphaclops.HPowGate))
    )
    circuit = alphaclops.expand_composite(unexpanded_circuit, no_decomp=no_decomp)
    actual_text_diagram = circuit.to_text_diagram().strip()
    expected_text_diagram = """
x: ───@───H───X───S───X───S^-1───H───@───
      │       │       │              │
y: ───X───────@───────@──────────────X───
    """.strip()
    assert actual_text_diagram == expected_text_diagram


def test_do_not_decompose_no_compile():
    q0, q1 = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.CNOT(q0, q1).with_tags("no_compile"))
    context = alphaclops.TransformerContext(tags_to_ignore=("no_compile",))
    assert_equal_mod_empty(c, alphaclops.expand_composite(c, context=context))


def test_expands_composite_recursively_preserving_structur():
    q = alphaclops.LineQubit.range(2)
    c_nested = alphaclops.FrozenCircuit(
        alphaclops.SWAP(*q[:2]), alphaclops.SWAP(*q[:2]).with_tags("ignore"), alphaclops.SWAP(*q[:2])
    )
    c_nested_expanded = alphaclops.FrozenCircuit(
        [alphaclops.CNOT(*q), alphaclops.CNOT(*q[::-1]), alphaclops.CNOT(*q)],
        alphaclops.SWAP(*q[:2]).with_tags("ignore"),
        [alphaclops.CNOT(*q), alphaclops.CNOT(*q[::-1]), alphaclops.CNOT(*q)],
    )
    c_orig = alphaclops.Circuit(
        c_nested,
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                c_nested,
                alphaclops.CircuitOperation(c_nested).repeat(5).with_tags("ignore"),
                alphaclops.CircuitOperation(c_nested).repeat(6).with_tags("preserve_tag"),
                alphaclops.CircuitOperation(c_nested).repeat(7),
                c_nested,
            )
        )
        .repeat(4)
        .with_tags("ignore"),
        c_nested,
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                c_nested,
                alphaclops.CircuitOperation(c_nested).repeat(5).with_tags("ignore"),
                alphaclops.CircuitOperation(c_nested).repeat(6).with_tags("preserve_tag"),
                alphaclops.CircuitOperation(c_nested).repeat(7),
                c_nested,
            )
        )
        .repeat(5)
        .with_tags("preserve_tag"),
        c_nested,
    )
    c_expected = alphaclops.Circuit(
        c_nested_expanded,
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                c_nested,
                alphaclops.CircuitOperation(c_nested).repeat(5).with_tags("ignore"),
                alphaclops.CircuitOperation(c_nested).repeat(6).with_tags("preserve_tag"),
                alphaclops.CircuitOperation(c_nested).repeat(7),
                c_nested,
            )
        )
        .repeat(4)
        .with_tags("ignore"),
        c_nested_expanded,
        alphaclops.CircuitOperation(
            alphaclops.FrozenCircuit(
                c_nested_expanded,
                alphaclops.CircuitOperation(c_nested).repeat(5).with_tags("ignore"),
                alphaclops.CircuitOperation(c_nested_expanded).repeat(6).with_tags("preserve_tag"),
                alphaclops.CircuitOperation(c_nested_expanded).repeat(7),
                c_nested_expanded,
            )
        )
        .repeat(5)
        .with_tags("preserve_tag"),
        c_nested_expanded,
    )

    context = alphaclops.TransformerContext(tags_to_ignore=["ignore"], deep=True)
    c_expanded = alphaclops.expand_composite(
        c_orig, no_decomp=lambda op: op.gate == alphaclops.CNOT, context=context
    )
    alphaclops.testing.assert_same_circuits(c_expanded, c_expected)
