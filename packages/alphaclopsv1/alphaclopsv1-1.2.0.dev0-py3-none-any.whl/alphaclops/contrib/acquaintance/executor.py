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

from typing import DefaultDict, Dict, Sequence, TYPE_CHECKING, Optional

import abc
from collections import defaultdict

from alphaclops import circuits, devices, ops, protocols, transformers

from alphaclops.contrib.acquaintance.gates import AcquaintanceOpportunityGate
from alphaclops.contrib.acquaintance.permutation import (
    PermutationGate,
    LogicalIndex,
    LogicalIndexSequence,
    LogicalGates,
    LogicalMapping,
)
from alphaclops.contrib.acquaintance.mutation_utils import expose_acquaintance_gates

if TYPE_CHECKING:
    import alphaclops


class ExecutionStrategy(metaclass=abc.ABCMeta):
    """Tells `StrategyExecutorTransformer` how to execute an acquaintance strategy.

    An execution strategy tells `StrategyExecutorTransformer` how to execute
    an acquaintance strategy, i.e. what gates to implement at the available
    acquaintance opportunities."""

    keep_acquaintance = False

    @property
    @abc.abstractmethod
    def device(self) -> 'alphaclops.Device':
        """The device for which the executed acquaintance strategy should be
        valid.
        """

    @property
    @abc.abstractmethod
    def initial_mapping(self) -> LogicalMapping:
        """The initial mapping of logical indices to qubits."""

    @abc.abstractmethod
    def get_operations(
        self, indices: Sequence[LogicalIndex], qubits: Sequence['alphaclops.Qid']
    ) -> 'alphaclops.OP_TREE':
        """Gets the logical operations to apply to qubits."""

    def __call__(self, *args, **kwargs):
        """Returns the final mapping of logical indices to qubits after
        executing an acquaintance strategy.
        """
        if len(args) < 1 or not isinstance(args[0], circuits.RandomGrid):
            raise ValueError(
                (
                    "To call ExecutionStrategy, an argument of type "
                    "circuits.RandomGrid must be passed in as the first non-keyword argument"
                )
            )
        input_circuit = args[0]
        strategy = StrategyExecutorTransformer(self)
        final_circuit = strategy(input_circuit, **kwargs)
        input_circuit._moments = final_circuit._moments
        return strategy.mapping


@transformers.transformer
class StrategyExecutorTransformer:
    """Executes an acquaintance strategy."""

    def __init__(self, execution_strategy: ExecutionStrategy) -> None:
        """Initializes transformer.

        Args:
            execution_strategy: The `ExecutionStrategy` to execute.

        Raises:
            ValueError: if execution_strategy is None.
        """

        if execution_strategy is None:
            raise ValueError('execution_strategy cannot be None')
        self.execution_strategy = execution_strategy
        self._mapping = execution_strategy.initial_mapping.copy()

    def __call__(
        self, circuit: circuits.RandomGrid, context: Optional['alphaclops.TransformerContext'] = None
    ) -> circuits.Circuit:
        """Executes an acquaintance strategy using alphaclops.map_operations_and_unroll and
        mutates initial mapping.

        Args:
            circuit: 'alphaclops.Circuit' input circuit to transform.
            context: `alphaclops.TransformerContext` storing common configurable
              options for transformers.

        Returns:
            A copy of the modified circuit after executing an acquaintance
              strategy on all instances of AcquaintanceOpportunityGate
        """

        circuit = transformers.expand_composite(
            circuit, no_decomp=expose_acquaintance_gates.no_decomp
        )
        return transformers.map_operations_and_unroll(
            circuit=circuit,
            map_func=self._map_func,
            deep=context.deep if context else False,
            tags_to_ignore=context.tags_to_ignore if context else (),
        ).unfreeze(copy=False)

    @property
    def mapping(self) -> LogicalMapping:
        return self._mapping

    def _map_func(self, op: 'alphaclops.Operation', index) -> 'alphaclops.OP_TREE':
        if isinstance(op.gate, AcquaintanceOpportunityGate):
            logical_indices = tuple(self._mapping[q] for q in op.qubits)
            logical_operations = self.execution_strategy.get_operations(logical_indices, op.qubits)
            clear_span = int(not self.execution_strategy.keep_acquaintance)

            return logical_operations if clear_span else [op, logical_operations]

        if isinstance(op.gate, PermutationGate):
            op.gate.update_mapping(self._mapping, op.qubits)
            return op

        raise TypeError(
            'Can only execute a strategy consisting of gates that '
            'are instances of AcquaintanceOpportunityGate or '
            'PermutationGate.'
        )


class AcquaintanceOperation(ops.GateOperation):
    """Represents an a acquaintance opportunity between a particular set of
    logical indices on a particular set of physical qubits.
    """

    def __init__(
        self, qubits: Sequence['alphaclops.Qid'], logical_indices: Sequence[LogicalIndex]
    ) -> None:
        if len(logical_indices) != len(qubits):
            raise ValueError('len(logical_indices) != len(qubits)')
        super().__init__(AcquaintanceOpportunityGate(num_qubits=len(qubits)), qubits)
        self.logical_indices: LogicalIndexSequence = logical_indices

    def _circuit_diagram_info_(
        self, args: 'alphaclops.CircuitDiagramInfoArgs'
    ) -> 'alphaclops.CircuitDiagramInfo':
        wire_symbols = tuple(f'({i})' for i in self.logical_indices)
        return protocols.CircuitDiagramInfo(wire_symbols=wire_symbols)


class GreedyExecutionStrategy(ExecutionStrategy):
    """A greedy execution strategy.

    When an acquaintance opportunity is reached, all gates acting on those
    qubits in any order are inserted.
    """

    def __init__(
        self,
        gates: LogicalGates,
        initial_mapping: LogicalMapping,
        device: Optional['alphaclops.Device'] = None,
    ) -> None:
        """Inits GreedyExecutionStrategy.

        Args:
            gates: The gates to insert.
            initial_mapping: The initial mapping of qubits to logical indices.
            device: The device upon which to execute the strategy.

        Raises:
            NotImplementedError: If not all gates are of the same arity.
        """

        if len(set(len(indices) for indices in gates)) > 1:
            raise NotImplementedError(
                'Can only implement greedy strategy if all gates are of the same arity.'
            )
        self.index_set_to_gates = self.canonicalize_gates(gates)
        self._initial_mapping = initial_mapping.copy()
        self._device = device or devices.UNCONSTRAINED_DEVICE

    @property
    def initial_mapping(self) -> LogicalMapping:
        return self._initial_mapping

    @property
    def device(self) -> 'alphaclops.Device':
        return self._device

    def get_operations(
        self, indices: Sequence[LogicalIndex], qubits: Sequence['alphaclops.Qid']
    ) -> 'alphaclops.OP_TREE':
        index_set = frozenset(indices)
        if index_set in self.index_set_to_gates:
            gates = self.index_set_to_gates.pop(index_set)
            index_to_qubit = dict(zip(indices, qubits))
            for gate_indices, gate in sorted(gates.items()):
                yield gate(*[index_to_qubit[i] for i in gate_indices])

    @staticmethod
    def canonicalize_gates(gates: LogicalGates) -> Dict[frozenset, LogicalGates]:
        """Canonicalizes a set of gates by the qubits they act on.

        Takes a set of gates specified by ordered sequences of logical
        indices, and groups those that act on the same qubits regardless of
        order."""
        canonicalized_gates: DefaultDict[frozenset, LogicalGates] = defaultdict(dict)
        for indices, gate in gates.items():
            indices = tuple(indices)
            canonicalized_gates[frozenset(indices)][indices] = gate
        return {
            canonical_indices: dict(list(gates.items()))
            for canonical_indices, gates in canonicalized_gates.items()
        }
