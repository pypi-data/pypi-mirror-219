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

import alphaclops


def test_inconclusive():
    class No:
        pass

    assert not alphaclops.has_unitary(object())
    assert not alphaclops.has_unitary('boo')
    assert not alphaclops.has_unitary(No())


@pytest.mark.parametrize(
    'measurement_gate', (alphaclops.MeasurementGate(1, 'a'), alphaclops.PauliMeasurementGate([alphaclops.X], 'a'))
)
def test_fail_fast_measure(measurement_gate):
    assert not alphaclops.has_unitary(measurement_gate)

    qubit = alphaclops.NamedQubit('q0')
    circuit = alphaclops.Circuit()
    circuit += measurement_gate(qubit)
    circuit += alphaclops.H(qubit)
    assert not alphaclops.has_unitary(circuit)


def test_fail_fast_measure_large_memory():
    num_qubits = 100
    measurement_op = alphaclops.MeasurementGate(num_qubits, 'a').on(*alphaclops.LineQubit.range(num_qubits))
    assert not alphaclops.has_unitary(measurement_op)


def test_via_unitary():
    class No1:
        def _unitary_(self):
            return NotImplemented

    class No2:
        def _unitary_(self):
            return None

    class Yes:
        def _unitary_(self):
            return np.array([[1]])

    assert not alphaclops.has_unitary(No1())
    assert not alphaclops.has_unitary(No2())
    assert alphaclops.has_unitary(Yes())
    assert alphaclops.has_unitary(Yes(), allow_decompose=False)


def test_via_apply_unitary():
    class No1(EmptyOp):
        def _apply_unitary_(self, args):
            return None

    class No2(EmptyOp):
        def _apply_unitary_(self, args):
            return NotImplemented

    class No3(alphaclops.testing.SingleQubitGate):
        def _apply_unitary_(self, args):
            return NotImplemented

    class No4:  # A non-operation non-gate.
        def _apply_unitary_(self, args):
            assert False  # Because has_unitary doesn't understand how to call.

    class Yes1(EmptyOp):
        def _apply_unitary_(self, args):
            return args.target_tensor

    class Yes2(alphaclops.testing.SingleQubitGate):
        def _apply_unitary_(self, args):
            return args.target_tensor

    assert alphaclops.has_unitary(Yes1())
    assert alphaclops.has_unitary(Yes1(), allow_decompose=False)
    assert alphaclops.has_unitary(Yes2())
    assert not alphaclops.has_unitary(No1())
    assert not alphaclops.has_unitary(No2())
    assert not alphaclops.has_unitary(No3())
    assert not alphaclops.has_unitary(No4())


def test_via_decompose():
    class Yes1:
        def _decompose_(self):
            return []

    class Yes2:
        def _decompose_(self):
            return [alphaclops.X(alphaclops.LineQubit(0))]

    class No1:
        def _decompose_(self):
            return [alphaclops.depolarize(0.5).on(alphaclops.LineQubit(0))]

    class No2:
        def _decompose_(self):
            return None

    class No3:
        def _decompose_(self):
            return NotImplemented

    assert alphaclops.has_unitary(Yes1())
    assert alphaclops.has_unitary(Yes2())
    assert not alphaclops.has_unitary(No1())
    assert not alphaclops.has_unitary(No2())
    assert not alphaclops.has_unitary(No3())

    assert not alphaclops.has_unitary(Yes1(), allow_decompose=False)
    assert not alphaclops.has_unitary(Yes2(), allow_decompose=False)
    assert not alphaclops.has_unitary(No1(), allow_decompose=False)


def test_via_has_unitary():
    class No1:
        def _has_unitary_(self):
            return NotImplemented

    class No2:
        def _has_unitary_(self):
            return False

    class Yes:
        def _has_unitary_(self):
            return True

    assert not alphaclops.has_unitary(No1())
    assert not alphaclops.has_unitary(No2())
    assert alphaclops.has_unitary(Yes())


def test_order():
    class Yes1(EmptyOp):
        def _has_unitary_(self):
            return True

        def _decompose_(self):
            assert False

        def _apply_unitary_(self, args):
            assert False

        def _unitary_(self):
            assert False

    class Yes2(EmptyOp):
        def _has_unitary_(self):
            return NotImplemented

        def _decompose_(self):
            return []

        def _apply_unitary_(self, args):
            assert False

        def _unitary_(self):
            assert False

    class Yes3(EmptyOp):
        def _has_unitary_(self):
            return NotImplemented

        def _decompose_(self):
            return NotImplemented

        def _apply_unitary_(self, args):
            return args.target_tensor

        def _unitary_(self):
            assert False

    class Yes4(EmptyOp):
        def _has_unitary_(self):
            return NotImplemented

        def _decompose_(self):
            return NotImplemented

        def _apply_unitary_(self, args):
            return NotImplemented

        def _unitary_(self):
            return np.array([[1]])

    assert alphaclops.has_unitary(Yes1())
    assert alphaclops.has_unitary(Yes2())
    assert alphaclops.has_unitary(Yes3())
    assert alphaclops.has_unitary(Yes4())


class EmptyOp(alphaclops.Operation):
    """A trivial operation that will be recognized as `_apply_unitary_`-able."""

    @property
    def qubits(self):
        # coverage: ignore
        return ()

    def with_qubits(self, *new_qubits):
        # coverage: ignore
        return self
