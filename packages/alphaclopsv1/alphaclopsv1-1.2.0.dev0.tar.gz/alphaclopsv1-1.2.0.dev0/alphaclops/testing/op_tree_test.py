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
import pytest

import alphaclops
from alphaclops.testing import assert_equivalent_op_tree


def test_assert_equivalent_op_tree():
    assert_equivalent_op_tree([], [])
    a = alphaclops.NamedQubit("a")
    assert_equivalent_op_tree([alphaclops.X(a)], [alphaclops.X(a)])

    assert_equivalent_op_tree(alphaclops.Circuit([alphaclops.X(a)]), [alphaclops.X(a)])
    assert_equivalent_op_tree(alphaclops.Circuit([alphaclops.X(a)], alphaclops.Moment()), [alphaclops.X(a)])

    with pytest.raises(AssertionError):
        assert_equivalent_op_tree([alphaclops.X(a)], [])
