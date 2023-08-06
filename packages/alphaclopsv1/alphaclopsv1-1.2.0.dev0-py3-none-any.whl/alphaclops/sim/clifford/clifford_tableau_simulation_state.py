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
"""A protocol for implementing high performance clifford tableau evolutions
 for Clifford Simulator."""

from typing import Optional, Sequence, TYPE_CHECKING

import numpy as np

from alphaclops.qis import clifford_tableau
from alphaclops.sim.clifford.stabilizer_simulation_state import StabilizerSimulationState

if TYPE_CHECKING:
    import alphaclops


class CliffordTableauSimulationState(StabilizerSimulationState[clifford_tableau.CliffordTableau]):
    """State and context for an operation acting on a clifford tableau."""

    def __init__(
        self,
        tableau: 'alphaclops.CliffordTableau',
        prng: Optional[np.random.RandomState] = None,
        qubits: Optional[Sequence['alphaclops.Qid']] = None,
        classical_data: Optional['alphaclops.ClassicalDataStore'] = None,
    ):
        """Inits CliffordTableauSimulationState.

        Args:
            tableau: The CliffordTableau to act on. Operations are expected to
                perform inplace edits of this object.
            qubits: Determines the canonical ordering of the qubits. This
                is often used in specifying the initial state, i.e. the
                ordering of the computational basis states.
            prng: The pseudo random number generator to use for probabilistic
                effects.
            classical_data: The shared classical data container for this
                simulation.
        """
        super().__init__(state=tableau, prng=prng, qubits=qubits, classical_data=classical_data)

    @property
    def tableau(self) -> 'alphaclops.CliffordTableau':
        return self.state
