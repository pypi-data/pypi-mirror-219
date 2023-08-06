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

import numpy as np
import sympy

import alphaclops


class GoodGateDecompose(alphaclops.testing.SingleQubitGate):
    def _decompose_(self, qubits):
        return alphaclops.X(qubits[0])

    def _unitary_(self):
        return np.array([[0, 1], [1, 0]])


class BadGateDecompose(alphaclops.testing.SingleQubitGate):
    def _decompose_(self, qubits):
        return alphaclops.Y(qubits[0])

    def _unitary_(self):
        return np.array([[0, 1], [1, 0]])


def test_assert_decompose_is_consistent_with_unitary():
    alphaclops.testing.assert_decompose_is_consistent_with_unitary(GoodGateDecompose())

    alphaclops.testing.assert_decompose_is_consistent_with_unitary(
        GoodGateDecompose().on(alphaclops.NamedQubit('q'))
    )

    with pytest.raises(AssertionError):
        alphaclops.testing.assert_decompose_is_consistent_with_unitary(BadGateDecompose())

    with pytest.raises(AssertionError):
        alphaclops.testing.assert_decompose_is_consistent_with_unitary(
            BadGateDecompose().on(alphaclops.NamedQubit('q'))
        )


class GateDecomposesToDefaultGateset(alphaclops.Gate):
    def _num_qubits_(self):
        return 2

    def _decompose_(self, qubits):
        return [GoodGateDecompose().on(qubits[0]), BadGateDecompose().on(qubits[1])]


class GateDecomposeDoesNotEndInDefaultGateset(alphaclops.Gate):
    def _num_qubits_(self):
        return 4

    def _decompose_(self, qubits):
        yield GateDecomposeNotImplemented().on_each(*qubits)


class GateDecomposeNotImplemented(alphaclops.testing.SingleQubitGate):
    def _decompose_(self, qubits):
        return NotImplemented


class ParameterizedGate(alphaclops.Gate):
    def _num_qubits_(self):
        return 2

    def _decompose_(self, qubits):
        yield alphaclops.X(qubits[0]) ** sympy.Symbol("x")
        yield alphaclops.Y(qubits[1]) ** sympy.Symbol("y")


def test_assert_decompose_ends_at_default_gateset():

    alphaclops.testing.assert_decompose_ends_at_default_gateset(GateDecomposesToDefaultGateset())
    alphaclops.testing.assert_decompose_ends_at_default_gateset(
        GateDecomposesToDefaultGateset().on(*alphaclops.LineQubit.range(2))
    )

    alphaclops.testing.assert_decompose_ends_at_default_gateset(ParameterizedGate())
    alphaclops.testing.assert_decompose_ends_at_default_gateset(
        ParameterizedGate().on(*alphaclops.LineQubit.range(2))
    )

    with pytest.raises(AssertionError):
        alphaclops.testing.assert_decompose_ends_at_default_gateset(GateDecomposeNotImplemented())

    with pytest.raises(AssertionError):
        alphaclops.testing.assert_decompose_ends_at_default_gateset(
            GateDecomposeNotImplemented().on(alphaclops.NamedQubit('q'))
        )
    with pytest.raises(AssertionError):
        alphaclops.testing.assert_decompose_ends_at_default_gateset(
            GateDecomposeDoesNotEndInDefaultGateset()
        )

    with pytest.raises(AssertionError):
        alphaclops.testing.assert_decompose_ends_at_default_gateset(
            GateDecomposeDoesNotEndInDefaultGateset().on(*alphaclops.LineQubit.range(4))
        )
