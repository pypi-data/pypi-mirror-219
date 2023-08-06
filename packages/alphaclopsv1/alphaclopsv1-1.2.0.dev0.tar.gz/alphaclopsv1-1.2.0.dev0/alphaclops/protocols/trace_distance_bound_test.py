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
import alphaclops


def test_trace_distance_bound():
    class NoMethod:
        pass

    class ReturnsNotImplemented:
        def _trace_distance_bound_(self):
            return NotImplemented

    class ReturnsTwo:
        def _trace_distance_bound_(self) -> float:
            return 2.0

    class ReturnsConstant:
        def __init__(self, bound):
            self.bound = bound

        def _trace_distance_bound_(self) -> float:
            return self.bound

    x = alphaclops.MatrixGate(alphaclops.unitary(alphaclops.X))
    cx = alphaclops.MatrixGate(alphaclops.unitary(alphaclops.CX))
    cxh = alphaclops.MatrixGate(alphaclops.unitary(alphaclops.CX ** 0.5))

    assert np.isclose(alphaclops.trace_distance_bound(x), alphaclops.trace_distance_bound(alphaclops.X))
    assert np.isclose(alphaclops.trace_distance_bound(cx), alphaclops.trace_distance_bound(alphaclops.CX))
    assert np.isclose(alphaclops.trace_distance_bound(cxh), alphaclops.trace_distance_bound(alphaclops.CX ** 0.5))
    assert alphaclops.trace_distance_bound(NoMethod()) == 1.0
    assert alphaclops.trace_distance_bound(ReturnsNotImplemented()) == 1.0
    assert alphaclops.trace_distance_bound(ReturnsTwo()) == 1.0
    assert alphaclops.trace_distance_bound(ReturnsConstant(0.1)) == 0.1
    assert alphaclops.trace_distance_bound(ReturnsConstant(0.5)) == 0.5
    assert alphaclops.trace_distance_bound(ReturnsConstant(1.0)) == 1.0
    assert alphaclops.trace_distance_bound(ReturnsConstant(2.0)) == 1.0
