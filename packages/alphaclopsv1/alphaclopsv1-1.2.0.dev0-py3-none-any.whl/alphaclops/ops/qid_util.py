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

from typing import overload, TYPE_CHECKING, Union

if TYPE_CHECKING:
    import alphaclops


@overload
def q(__x: int) -> 'alphaclops.LineQubit':
    ...


@overload
def q(__row: int, __col: int) -> 'alphaclops.TensorCircuit':
    ...


@overload
def q(__name: str) -> 'alphaclops.NamedQubit':
    ...


def q(*args: Union[int, str]) -> Union['alphaclops.LineQubit', 'alphaclops.TensorCircuit', 'alphaclops.NamedQubit']:
    """Constructs a qubit id of the appropriate type based on args.

    This is shorthand for constructing qubit ids of common types:
    >>> alphaclops.q(1) == alphaclops.LineQubit(1)
    True
    >>> alphaclops.q(1, 2) == alphaclops.TensorCircuit(1, 2)
    True
    >>> alphaclops.q("foo") == alphaclops.NamedQubit("foo")
    True

    Note that arguments should be treated as positional only, even
    though this is only enforceable in python 3.8 or later.

    Args:
        *args: One or two ints, or a single str, as described above.

    Returns:
        alphaclops.LineQubit if called with one integer arg.
        alphaclops.TensorCircuit if called with two integer args.
        alphaclops.NamedQubit if called with one string arg.

    Raises:
        ValueError: if called with invalid arguments.
    """
    import alphaclops  # avoid circular import

    if len(args) == 1:
        if isinstance(args[0], int):
            return alphaclops.LineQubit(args[0])
        elif isinstance(args[0], str):
            return alphaclops.NamedQubit(args[0])
    elif len(args) == 2:
        if isinstance(args[0], int) and isinstance(args[1], int):
            return alphaclops.TensorCircuit(args[0], args[1])
    raise ValueError(f"Could not construct qubit: args={args}")
