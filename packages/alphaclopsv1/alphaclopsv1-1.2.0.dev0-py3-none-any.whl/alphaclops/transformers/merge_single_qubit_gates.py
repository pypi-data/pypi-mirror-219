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

"""Transformer passes to combine adjacent single-qubit rotations."""

from typing import Optional, TYPE_CHECKING

from alphaclops import circuits, ops, protocols
from alphaclops.transformers.analytical_decompositions import single_qubit_decompositions
from alphaclops.transformers import transformer_api, transformer_primitives, merge_k_qubit_gates

if TYPE_CHECKING:
    import alphaclops


@transformer_api.transformer
def merge_single_qubit_gates_to_phased_x_and_z(
    circuit: 'alphaclops.RandomGrid',
    *,
    context: Optional['alphaclops.TransformerContext'] = None,
    atol: float = 1e-8,
) -> 'alphaclops.Circuit':
    """Replaces runs of single qubit rotations with `alphaclops.PhasedXPowGate` and `alphaclops.ZPowGate`.

    Specifically, any run of non-parameterized single-qubit unitaries will be replaced by an
    optional PhasedX operation followed by an optional Z operation.

    Args:
        circuit: Input circuit to transform. It will not be modified.
        context: `alphaclops.TransformerContext` storing common configurable options for transformers.
        atol: Absolute tolerance to angle error. Larger values allow more negligible gates to be
            dropped, smaller values increase accuracy.

    Returns:
        Copy of the transformed input circuit.
    """

    def rewriter(op: 'alphaclops.CircuitOperation') -> 'alphaclops.OP_TREE':
        u = protocols.unitary(op)
        if protocols.num_qubits(op) == 0:
            return ops.GlobalPhaseGate(u[0, 0]).on()
        return [
            g(op.qubits[0])
            for g in single_qubit_decompositions.single_qubit_matrix_to_phased_x_z(u, atol)
        ]

    return merge_k_qubit_gates.merge_k_qubit_unitaries(
        circuit, k=1, context=context, rewriter=rewriter
    )


@transformer_api.transformer
def merge_single_qubit_gates_to_phxz(
    circuit: 'alphaclops.RandomGrid',
    *,
    context: Optional['alphaclops.TransformerContext'] = None,
    atol: float = 1e-8,
) -> 'alphaclops.Circuit':
    """Replaces runs of single qubit rotations with a single optional `alphaclops.PhasedXZGate`.

    Specifically, any run of non-parameterized single-qubit unitaries will be replaced by an
    optional PhasedXZ.

    Args:
        circuit: Input circuit to transform. It will not be modified.
        context: `alphaclops.TransformerContext` storing common configurable options for transformers.
        atol: Absolute tolerance to angle error. Larger values allow more negligible gates to be
            dropped, smaller values increase accuracy.

    Returns:
        Copy of the transformed input circuit.
    """

    def rewriter(op: 'alphaclops.CircuitOperation') -> 'alphaclops.OP_TREE':
        u = protocols.unitary(op)
        if protocols.num_qubits(op) == 0:
            return ops.GlobalPhaseGate(u[0, 0]).on()
        gate = single_qubit_decompositions.single_qubit_matrix_to_phxz(u, atol)
        return gate(op.qubits[0]) if gate else []

    return merge_k_qubit_gates.merge_k_qubit_unitaries(
        circuit, k=1, context=context, rewriter=rewriter
    )


@transformer_api.transformer
def merge_single_qubit_moments_to_phxz(
    circuit: 'alphaclops.RandomGrid',
    *,
    context: Optional['alphaclops.TransformerContext'] = None,
    atol: float = 1e-8,
) -> 'alphaclops.Circuit':
    """Merges adjacent moments with only 1-qubit rotations to a single moment with PhasedXZ gates.

    Args:
        circuit: Input circuit to transform. It will not be modified.
        context: `alphaclops.TransformerContext` storing common configurable options for transformers.
        atol: Absolute tolerance to angle error. Larger values allow more negligible gates to be
            dropped, smaller values increase accuracy.

    Returns:
        Copy of the transformed input circuit.
    """
    tags_to_ignore = set(context.tags_to_ignore) if context else set()

    def can_merge_moment(m: 'alphaclops.Moment'):
        return all(
            protocols.num_qubits(op) == 1
            and protocols.has_unitary(op)
            and tags_to_ignore.isdisjoint(op.tags)
            for op in m
        )

    def merge_func(m1: 'alphaclops.Moment', m2: 'alphaclops.Moment') -> Optional['alphaclops.Moment']:
        if not (can_merge_moment(m1) and can_merge_moment(m2)):
            return None
        ret_ops = []
        for q in m1.qubits | m2.qubits:
            mat = protocols.unitary(circuits.Circuit(m.operation_at(q) or [] for m in [m1, m2]))
            gate = single_qubit_decompositions.single_qubit_matrix_to_phxz(mat, atol)
            if gate:
                ret_ops.append(gate(q))
        return circuits.Moment(ret_ops)

    return transformer_primitives.merge_moments(
        circuit,
        merge_func,
        deep=context.deep if context else False,
        tags_to_ignore=tuple(tags_to_ignore),
    ).unfreeze(copy=False)
