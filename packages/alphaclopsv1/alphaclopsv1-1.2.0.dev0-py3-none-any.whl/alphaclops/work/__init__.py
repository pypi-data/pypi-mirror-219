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

"""Workflow utilities for sampling and measurement collection."""

from alphaclops.work.collector import CircuitSampleJob, Collector
from alphaclops.work.pauli_sum_collector import PauliSumCollector
from alphaclops.work.observable_settings import InitObsSetting, _MeasurementSpec, observables_to_settings
from alphaclops.work.observable_grouping import group_settings_greedy
from alphaclops.work.observable_measurement_data import (
    ObservableMeasuredResult,
    BitstringAccumulator,
    flatten_grouped_results,
)
from alphaclops.work.observable_measurement import (
    VarianceStoppingCriteria,
    RepetitionsStoppingCriteria,
    measure_grouped_settings,
)
from alphaclops.work.observable_readout_calibration import calibrate_readout_error
from alphaclops.work.sampler import Sampler
from alphaclops.work.zeros_sampler import ZerosSampler
