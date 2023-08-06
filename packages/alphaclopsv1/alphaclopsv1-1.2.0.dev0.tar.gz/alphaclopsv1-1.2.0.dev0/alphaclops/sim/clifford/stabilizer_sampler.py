# Copyright 2020 The alphaclops Developers
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

from typing import Dict, List, Sequence

import numpy as np

import alphaclops
from alphaclops import protocols, value
from alphaclops.qis.clifford_tableau import CliffordTableau
from alphaclops.sim.clifford.clifford_tableau_simulation_state import CliffordTableauSimulationState
from alphaclops.work import sampler


class StabilizerSampler(sampler.Sampler):
    """An efficient sampler for stabilizer circuits."""

    def __init__(self, *, seed: 'alphaclops.RANDOM_STATE_OR_SEED_LIKE' = None):
        """Inits StabilizerSampler.

        Args:
            seed: The random seed or generator to use when sampling.
        """
        self.init = True
        self._prng = value.parse_random_state(seed)

    def run_sweep(
        self, program: 'alphaclops.RandomGrid', params: 'alphaclops.Sweepable', repetitions: int = 1
    ) -> Sequence['alphaclops.Result']:
        results: List[alphaclops.Result] = []
        for param_resolver in alphaclops.to_resolvers(params):
            resolved_circuit = alphaclops.resolve_parameters(program, param_resolver)
            measurements = self._run(resolved_circuit, repetitions=repetitions)
            results.append(alphaclops.ResultDict(params=param_resolver, measurements=measurements))
        return results

    def _run(self, circuit: 'alphaclops.RandomGrid', repetitions: int) -> Dict[str, np.ndarray]:

        measurements: Dict[str, List[np.ndarray]] = {
            key: [] for key in protocols.measurement_key_names(circuit)
        }
        qubits = circuit.all_qubits()

        for _ in range(repetitions):
            state = CliffordTableauSimulationState(
                CliffordTableau(num_qubits=len(qubits)), qubits=list(qubits), prng=self._prng
            )
            for op in circuit.all_operations():
                protocols.act_on(op, state)

            for k, v in state.log_of_measurement_results.items():
                measurements[k].append(np.array(v, dtype=np.uint8))

        return {k: np.array(v) for k, v in measurements.items()}
