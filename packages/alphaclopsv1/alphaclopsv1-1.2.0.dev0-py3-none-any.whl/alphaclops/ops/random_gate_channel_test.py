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
import numpy as np
import pytest
import sympy

import alphaclops


def test_init():
    p = alphaclops.RandomGateChannel(sub_gate=alphaclops.X, probability=0.5)
    assert p.sub_gate is alphaclops.X
    assert p.probability == 0.5

    with pytest.raises(ValueError, match='probability'):
        _ = alphaclops.RandomGateChannel(sub_gate=alphaclops.X, probability=2)
    with pytest.raises(ValueError, match='probability'):
        _ = alphaclops.RandomGateChannel(sub_gate=alphaclops.X, probability=-1)


def test_eq():
    eq = alphaclops.testing.EqualsTester()
    q = alphaclops.LineQubit(0)

    eq.add_equality_group(
        alphaclops.RandomGateChannel(sub_gate=alphaclops.X, probability=0.5), alphaclops.X.with_probability(0.5)
    )

    # Each field matters for equality.
    eq.add_equality_group(alphaclops.Y.with_probability(0.5))
    eq.add_equality_group(alphaclops.X.with_probability(0.25))

    # `with_probability(1)` doesn't wrap
    eq.add_equality_group(alphaclops.X, alphaclops.X.with_probability(1))
    eq.add_equality_group(
        alphaclops.X.with_probability(1).on(q), alphaclops.X.on(q).with_probability(1), alphaclops.X(q)
    )

    # `with_probability` with `on`.
    eq.add_equality_group(alphaclops.X.with_probability(0.5).on(q), alphaclops.X.on(q).with_probability(0.5))

    # Flattening.
    eq.add_equality_group(
        alphaclops.RandomGateChannel(sub_gate=alphaclops.Z, probability=0.25),
        alphaclops.RandomGateChannel(
            sub_gate=alphaclops.RandomGateChannel(sub_gate=alphaclops.Z, probability=0.5), probability=0.5
        ),
        alphaclops.Z.with_probability(0.5).with_probability(0.5),
        alphaclops.Z.with_probability(0.25),
    )

    # Supports approximate equality.
    assert alphaclops.approx_eq(alphaclops.X.with_probability(0.5), alphaclops.X.with_probability(0.50001), atol=1e-2)
    assert not alphaclops.approx_eq(
        alphaclops.X.with_probability(0.5), alphaclops.X.with_probability(0.50001), atol=1e-8
    )


def test_consistent_protocols():
    alphaclops.testing.assert_implements_consistent_protocols(
        alphaclops.RandomGateChannel(sub_gate=alphaclops.X, probability=1),
        ignore_decompose_to_default_gateset=True,
    )
    alphaclops.testing.assert_implements_consistent_protocols(
        alphaclops.RandomGateChannel(sub_gate=alphaclops.X, probability=0),
        ignore_decompose_to_default_gateset=True,
    )
    alphaclops.testing.assert_implements_consistent_protocols(
        alphaclops.RandomGateChannel(sub_gate=alphaclops.X, probability=sympy.Symbol('x') / 2),
        ignore_decompose_to_default_gateset=True,
    )
    alphaclops.testing.assert_implements_consistent_protocols(
        alphaclops.RandomGateChannel(sub_gate=alphaclops.X, probability=0.5),
        ignore_decompose_to_default_gateset=True,
    )


def test_diagram():
    class NoDetailsGate(alphaclops.Gate):
        def num_qubits(self) -> int:
            raise NotImplementedError()

    assert alphaclops.circuit_diagram_info(NoDetailsGate().with_probability(0.5), None) is None

    a, b = alphaclops.LineQubit.range(2)
    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(alphaclops.CNOT(a, b).with_probability(0.125)),
        """
0: ───@[prob=0.125]───
      │
1: ───X───────────────
        """,
    )

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(alphaclops.CNOT(a, b).with_probability(0.125)),
        """
0: ───@[prob=0.1]───
      │
1: ───X─────────────
        """,
        precision=1,
    )


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_parameterized(resolve_fn):
    op = alphaclops.X.with_probability(sympy.Symbol('x'))
    assert alphaclops.is_parameterized(op)
    assert not alphaclops.has_kraus(op)
    assert not alphaclops.has_mixture(op)

    op2 = resolve_fn(op, {'x': 0.5})
    assert op2 == alphaclops.X.with_probability(0.5)
    assert not alphaclops.is_parameterized(op2)
    assert alphaclops.has_kraus(op2)
    assert alphaclops.has_mixture(op2)


def test_mixture():
    class NoDetailsGate(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 1

    assert not alphaclops.has_mixture(NoDetailsGate().with_probability(0.5))
    assert alphaclops.mixture(NoDetailsGate().with_probability(0.5), None) is None

    assert alphaclops.mixture(alphaclops.X.with_probability(sympy.Symbol('x')), None) is None

    m = alphaclops.mixture(alphaclops.X.with_probability(0.25))
    assert len(m) == 2
    assert m[0][0] == 0.25
    np.testing.assert_allclose(alphaclops.unitary(alphaclops.X), m[0][1])
    assert m[1][0] == 0.75
    np.testing.assert_allclose(alphaclops.unitary(alphaclops.I), m[1][1])

    m = alphaclops.mixture(alphaclops.bit_flip(1 / 4).with_probability(1 / 8))
    assert len(m) == 3
    assert {p for p, _ in m} == {7 / 8, 1 / 32, 3 / 32}


def assert_channel_sums_to_identity(val):
    m = alphaclops.kraus(val)
    s = sum(np.conj(e.T) @ e for e in m)
    np.testing.assert_allclose(s, np.eye(np.prod(alphaclops.qid_shape(val), dtype=np.int64)), atol=1e-8)


def test_channel():
    class NoDetailsGate(alphaclops.Gate):
        def num_qubits(self) -> int:
            return 1

    assert not alphaclops.has_kraus(NoDetailsGate().with_probability(0.5))
    assert alphaclops.kraus(NoDetailsGate().with_probability(0.5), None) is None
    assert alphaclops.kraus(alphaclops.X.with_probability(sympy.Symbol('x')), None) is None
    alphaclops.testing.assert_consistent_channel(alphaclops.X.with_probability(0.25))
    alphaclops.testing.assert_consistent_channel(alphaclops.bit_flip(0.75).with_probability(0.25))
    alphaclops.testing.assert_consistent_channel(alphaclops.amplitude_damp(0.75).with_probability(0.25))

    alphaclops.testing.assert_consistent_mixture(alphaclops.X.with_probability(0.25))
    alphaclops.testing.assert_consistent_mixture(alphaclops.bit_flip(0.75).with_probability(0.25))
    assert not alphaclops.has_mixture(alphaclops.amplitude_damp(0.75).with_probability(0.25))

    m = alphaclops.kraus(alphaclops.X.with_probability(0.25))
    assert len(m) == 2
    np.testing.assert_allclose(m[0], alphaclops.unitary(alphaclops.X) * np.sqrt(0.25), atol=1e-8)
    np.testing.assert_allclose(m[1], alphaclops.unitary(alphaclops.I) * np.sqrt(0.75), atol=1e-8)

    m = alphaclops.kraus(alphaclops.bit_flip(0.75).with_probability(0.25))
    assert len(m) == 3
    np.testing.assert_allclose(
        m[0], alphaclops.unitary(alphaclops.I) * np.sqrt(0.25) * np.sqrt(0.25), atol=1e-8
    )
    np.testing.assert_allclose(
        m[1], alphaclops.unitary(alphaclops.X) * np.sqrt(0.25) * np.sqrt(0.75), atol=1e-8
    )
    np.testing.assert_allclose(m[2], alphaclops.unitary(alphaclops.I) * np.sqrt(0.75), atol=1e-8)

    m = alphaclops.kraus(alphaclops.amplitude_damp(0.75).with_probability(0.25))
    assert len(m) == 3
    np.testing.assert_allclose(
        m[0], np.array([[1, 0], [0, np.sqrt(1 - 0.75)]]) * np.sqrt(0.25), atol=1e-8
    )
    np.testing.assert_allclose(
        m[1], np.array([[0, np.sqrt(0.75)], [0, 0]]) * np.sqrt(0.25), atol=1e-8
    )
    np.testing.assert_allclose(m[2], alphaclops.unitary(alphaclops.I) * np.sqrt(0.75), atol=1e-8)


def test_trace_distance():
    t = alphaclops.trace_distance_bound
    assert 0.999 <= t(alphaclops.X.with_probability(sympy.Symbol('x')))
    assert t(alphaclops.X.with_probability(0)) == 0
    assert 0.49 <= t(alphaclops.X.with_probability(0.5)) <= 0.51
    assert 0.7 <= t(alphaclops.S.with_probability(sympy.Symbol('x'))) <= 0.71
    assert 0.35 <= t(alphaclops.S.with_probability(0.5)) <= 0.36


def test_str():
    assert str(alphaclops.X.with_probability(0.5)) == 'X[prob=0.5]'


def test_stabilizer_supports_probability():
    q = alphaclops.LineQubit(0)
    c = alphaclops.Circuit(alphaclops.X(q).with_probability(0.5), alphaclops.measure(q, key='m'))
    m = np.sum(alphaclops.StabilizerSampler().sample(c, repetitions=100)['m'])
    assert 5 < m < 95


def test_unsupported_stabilizer_safety():
    from alphaclops.protocols.act_on_protocol_test import DummySimulationState

    with pytest.raises(TypeError, match="act_on"):
        for _ in range(100):
            alphaclops.act_on(alphaclops.X.with_probability(0.5), DummySimulationState(), qubits=())
    with pytest.raises(TypeError, match="act_on"):
        alphaclops.act_on(alphaclops.X.with_probability(sympy.Symbol('x')), DummySimulationState(), qubits=())

    q = alphaclops.LineQubit(0)
    c = alphaclops.Circuit((alphaclops.X(q) ** 0.25).with_probability(0.5), alphaclops.measure(q, key='m'))
    with pytest.raises(TypeError, match='Failed to act'):
        alphaclops.StabilizerSampler().sample(c, repetitions=100)
