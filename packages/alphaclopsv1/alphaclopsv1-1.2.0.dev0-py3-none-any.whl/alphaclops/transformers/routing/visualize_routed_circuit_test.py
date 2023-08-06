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

import pytest
import alphaclops


def test_routed_circuit_with_mapping_simple():
    q = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit([alphaclops.Moment(alphaclops.SWAP(q[0], q[1]).with_tags(alphaclops.RoutingSwapTag()))])
    expected_diagram = """
0: ───q(0)───×[alphaclops.RoutingSwapTag()]───q(1)───
      │      │                          │
1: ───q(1)───×──────────────────────────q(0)───"""
    alphaclops.testing.assert_has_diagram(alphaclops.routed_circuit_with_mapping(circuit), expected_diagram)

    expected_diagram_with_initial_mapping = """
0: ───a───×[alphaclops.RoutingSwapTag()]───b───
      │   │                          │
1: ───b───×──────────────────────────a───"""
    alphaclops.testing.assert_has_diagram(
        alphaclops.routed_circuit_with_mapping(
            circuit, {alphaclops.NamedQubit("a"): q[0], alphaclops.NamedQubit("b"): q[1]}
        ),
        expected_diagram_with_initial_mapping,
    )

    # if swap is untagged should not affect the mapping
    circuit = alphaclops.Circuit([alphaclops.Moment(alphaclops.SWAP(q[0], q[1]))])
    expected_diagram = """
0: ───q(0)───×───
      │      │
1: ───q(1)───×───"""
    alphaclops.testing.assert_has_diagram(alphaclops.routed_circuit_with_mapping(circuit), expected_diagram)

    circuit = alphaclops.Circuit(
        [
            alphaclops.Moment(alphaclops.X(q[0]).with_tags(alphaclops.RoutingSwapTag())),
            alphaclops.Moment(alphaclops.SWAP(q[0], q[1])),
        ]
    )
    with pytest.raises(
        ValueError, match="Invalid circuit. A non-SWAP gate cannot be tagged a RoutingSwapTag."
    ):
        alphaclops.routed_circuit_with_mapping(circuit)


def test_routed_circuit_with_mapping_multi_swaps():
    q = alphaclops.LineQubit.range(6)
    circuit = alphaclops.Circuit(
        [
            alphaclops.Moment(alphaclops.CNOT(q[3], q[4])),
            alphaclops.Moment(alphaclops.CNOT(q[5], q[4]), alphaclops.CNOT(q[2], q[3])),
            alphaclops.Moment(
                alphaclops.CNOT(q[2], q[1]), alphaclops.SWAP(q[4], q[3]).with_tags(alphaclops.RoutingSwapTag())
            ),
            alphaclops.Moment(
                alphaclops.SWAP(q[0], q[1]).with_tags(alphaclops.RoutingSwapTag()),
                alphaclops.SWAP(q[3], q[2]).with_tags(alphaclops.RoutingSwapTag()),
            ),
            alphaclops.Moment(alphaclops.CNOT(q[2], q[1])),
            alphaclops.Moment(alphaclops.CNOT(q[1], q[0])),
        ]
    )
    expected_diagram = """
0: ───q(0)──────────────────────────────────────q(0)───×[alphaclops.RoutingSwapTag()]───q(1)───────X───
      │                                         │      │                          │          │
1: ───q(1)───────────X──────────────────────────q(1)───×──────────────────────────q(0)───X───@───
      │              │                          │                                 │      │
2: ───q(2)───────@───@──────────────────────────q(2)───×──────────────────────────q(4)───@───────
      │          │                              │      │                          │
3: ───q(3)───@───X───×──────────────────────────q(4)───×[alphaclops.RoutingSwapTag()]───q(2)───────────
      │      │       │                          │                                 │
4: ───q(4)───X───X───×[alphaclops.RoutingSwapTag()]───q(3)──────────────────────────────q(3)───────────
      │          │                              │                                 │
5: ───q(5)───────@──────────────────────────────q(5)──────────────────────────────q(5)───────────
"""
    alphaclops.testing.assert_has_diagram(alphaclops.routed_circuit_with_mapping(circuit), expected_diagram)
