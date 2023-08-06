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

import alphaclops


def _make_qubits(n):
    return [alphaclops.NamedQubit(f'q{i}') for i in range(n)]


def test_op_calls_validate():
    q0, q1, q2 = _make_qubits(3)
    bad_qubit = alphaclops.NamedQubit('bad')

    class ValidError(Exception):
        pass

    class ValiGate(alphaclops.PauliStringGateOperation):
        def validate_args(self, qubits):
            super().validate_args(qubits)
            if bad_qubit in qubits:
                raise ValidError()

        def map_qubits(self, qubit_map):
            ps = self.pauli_string.map_qubits(qubit_map)
            return ValiGate(ps)

    g = ValiGate(alphaclops.PauliString({q0: alphaclops.X, q1: alphaclops.Y, q2: alphaclops.Z}))

    _ = g.with_qubits(q1, q0, q2)
    with pytest.raises(ValidError):
        _ = g.with_qubits(q0, q1, bad_qubit)


def test_on_wrong_number_qubits():
    q0, q1, q2 = _make_qubits(3)

    class DummyGate(alphaclops.PauliStringGateOperation):
        def map_qubits(self, qubit_map):
            ps = self.pauli_string.map_qubits(qubit_map)
            return DummyGate(ps)

    g = DummyGate(alphaclops.PauliString({q0: alphaclops.X, q1: alphaclops.Y}))

    _ = g.with_qubits(q1, q2)
    with pytest.raises(ValueError):
        _ = g.with_qubits()
    with pytest.raises(ValueError):
        _ = g.with_qubits(q2)
    with pytest.raises(ValueError):
        _ = g.with_qubits(q0, q1, q2)


def test_default_text_diagram():
    class DiagramGate(alphaclops.PauliStringGateOperation):
        def map_qubits(self, qubit_map):
            pass

        def _circuit_diagram_info_(
            self, args: alphaclops.CircuitDiagramInfoArgs
        ) -> alphaclops.CircuitDiagramInfo:
            return self._pauli_string_diagram_info(args)

    q0, q1, q2 = _make_qubits(3)
    ps = alphaclops.PauliString({q0: alphaclops.X, q1: alphaclops.Y, q2: alphaclops.Z})

    circuit = alphaclops.Circuit(DiagramGate(ps), DiagramGate(-ps))
    alphaclops.testing.assert_has_diagram(
        circuit,
        """
q0: ───[X]───[X]───
       │     │
q1: ───[Y]───[Y]───
       │     │
q2: ───[Z]───[Z]───
""",
    )
