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

"""Value conversion utilities and classes for time and quantum states."""
from alphaclops.value.abc_alt import TwoAltoptives, alternative

from alphaclops.value.angle import (
    canonicalize_half_turns,
    chosen_angle_to_canonical_half_turns,
    chosen_angle_to_half_turns,
)

from alphaclops.value.classical_data import (
    ClassicalDataDictionaryStore,
    ClassicalDataStore,
    ClassicalDataStoreReader,
    MeasurementType,
)

from alphaclops.value.condition import Condition, KeyCondition, SympyCondition

from alphaclops.value.digits import (
    big_endian_bits_to_int,
    big_endian_digits_to_int,
    big_endian_int_to_bits,
    big_endian_int_to_digits,
)

from alphaclops.value.duration import Duration, DURATION_LIKE

from alphaclops.value.linear_dict import LinearDict, Scalar

from alphaclops.value.measurement_key import MEASUREMENT_KEY_SEPARATOR, MeasurementKey

from alphaclops.value.probability import state_vector_to_probabilities, validate_probability

from alphaclops.value.product_state import (
    ProductState,
    KET_PLUS,
    KET_MINUS,
    KET_IMAG,
    KET_MINUS_IMAG,
    KET_ZERO,
    KET_ONE,
    PAULI_STATES,
)

from alphaclops.value.periodic_value import PeriodicValue

from alphaclops.value.random_state import parse_random_state, RANDOM_STATE_OR_SEED_LIKE

from alphaclops.value.timestamp import Timestamp

from alphaclops.value.type_alias import TParamKey, TParamVal, TParamValComplex

from alphaclops.value.value_equality_attr import value_equality
