# Copyright 2019 The alphaclops Developers
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

import random

import numpy as np
import pytest
import networkx as nx

import alphaclops
import alphaclops.contrib.routing as ccr


def get_seeded_initial_mapping(graph_seed, init_seed):
    logical_graph = nx.erdos_renyi_graph(10, 0.5, seed=graph_seed)
    logical_graph = nx.relabel_nodes(logical_graph, alphaclops.LineQubit)
    device_graph = ccr.get_grid_device_graph(4, 4)
    return ccr.initialization.get_initial_mapping(logical_graph, device_graph, init_seed)


@pytest.mark.parametrize('seed', [random.randint(0, 2**32) for _ in range(10)])
def test_initialization_reproducible_with_seed(seed):
    wrappers = (lambda s: s, np.random.RandomState)
    mappings = [
        get_seeded_initial_mapping(seed, wrapper(seed)) for wrapper in wrappers for _ in range(5)
    ]
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(*mappings)


def test_initialization_with_no_seed():
    graph_seed = random.randint(0, 2**32)
    state = np.random.get_state()
    mappings = []
    for _ in range(3):
        np.random.set_state(state)
        mappings.append(get_seeded_initial_mapping(graph_seed, None))
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(*mappings)


def test_initialization_reproducible_between_runs():
    seed = 45
    logical_graph = nx.erdos_renyi_graph(6, 0.5, seed=seed)
    logical_graph = nx.relabel_nodes(logical_graph, alphaclops.LineQubit)
    device_graph = ccr.get_grid_device_graph(2, 3)
    initial_mapping = ccr.initialization.get_initial_mapping(logical_graph, device_graph, seed)
    expected_mapping = {
        alphaclops.TensorCircuit(0, 0): alphaclops.LineQubit(5),
        alphaclops.TensorCircuit(0, 1): alphaclops.LineQubit(0),
        alphaclops.TensorCircuit(0, 2): alphaclops.LineQubit(2),
        alphaclops.TensorCircuit(1, 0): alphaclops.LineQubit(3),
        alphaclops.TensorCircuit(1, 1): alphaclops.LineQubit(4),
        alphaclops.TensorCircuit(1, 2): alphaclops.LineQubit(1),
    }
    assert initial_mapping == expected_mapping
