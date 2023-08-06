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

"""Tools for creating and using acquaintance strategies."""

from alphaclops.contrib.acquaintance.bipartite import BipartiteGraphType, BipartiteSwapNetworkGate

from alphaclops.contrib.acquaintance.devices import get_acquaintance_size, UnconstrainedAcquaintanceDevice

from alphaclops.contrib.acquaintance.executor import (
    AcquaintanceOperation,
    GreedyExecutionStrategy,
    StrategyExecutorTransformer,
)

from alphaclops.contrib.acquaintance.gates import acquaint, AcquaintanceOpportunityGate, SwapNetworkGate

from alphaclops.contrib.acquaintance.inspection_utils import get_logical_acquaintance_opportunities

from alphaclops.contrib.acquaintance.mutation_utils import (
    expose_acquaintance_gates,
    rectify_acquaintance_strategy,
    replace_acquaintance_with_swap_network,
)

from alphaclops.contrib.acquaintance.optimizers import remove_redundant_acquaintance_opportunities

from alphaclops.contrib.acquaintance.permutation import (
    LinearPermutationGate,
    PermutationGate,
    SwapPermutationGate,
    update_mapping,
    get_logical_operations,
    display_mapping,
    return_to_initial_mapping,
    uses_consistent_swap_gate,
    EXPAND_PERMUTATION_GATES,
    DECOMPOSE_PERMUTATION_GATES,
)

from alphaclops.contrib.acquaintance.shift import CircularShiftGate

from alphaclops.contrib.acquaintance.shift_swap_network import ShiftSwapNetworkGate

from alphaclops.contrib.acquaintance.strategies import (
    complete_acquaintance_strategy,
    cubic_acquaintance_strategy,
    quartic_paired_acquaintance_strategy,
)

from alphaclops.contrib.acquaintance.topological_sort import (
    is_topologically_sorted,
    random_topological_sort,
)

from alphaclops.contrib.acquaintance import testing
