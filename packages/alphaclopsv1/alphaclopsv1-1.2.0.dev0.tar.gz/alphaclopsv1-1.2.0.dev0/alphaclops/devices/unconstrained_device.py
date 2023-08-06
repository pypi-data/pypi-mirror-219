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

from typing import Any, Dict, TYPE_CHECKING

from alphaclops import value, protocols
from alphaclops._doc import document
from alphaclops.devices import device

if TYPE_CHECKING:
    import alphaclops


@value.value_equality()
class _UnconstrainedDevice(device.Device):
    """A device that allows everything, infinitely fast."""

    def duration_of(self, operation: 'alphaclops.Operation') -> 'alphaclops.Duration':
        return value.Duration(picos=0)

    def validate_moment(self, moment) -> None:
        pass

    def validate_circuit(self, circuit) -> None:
        pass

    def __repr__(self) -> str:
        return 'alphaclops.UNCONSTRAINED_DEVICE'

    def _value_equality_values_(self) -> Any:
        return ()

    def _json_dict_(self) -> Dict[str, Any]:
        return protocols.obj_to_dict_helper(self, [])


UNCONSTRAINED_DEVICE: device.Device = _UnconstrainedDevice()
document(UNCONSTRAINED_DEVICE, """A device with no constraints on operations or qubits.""")
