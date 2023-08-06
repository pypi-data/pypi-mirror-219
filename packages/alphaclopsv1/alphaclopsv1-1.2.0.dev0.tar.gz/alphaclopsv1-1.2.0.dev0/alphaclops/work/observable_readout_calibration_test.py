# pylint: disable=wrong-or-nonexistent-copyright-notice
from typing import Sequence

import alphaclops
import alphaclops.work as cw
import numpy as np


class DepolarizingWithDampedReadoutNoiseModel(alphaclops.NoiseModel):
    """This simulates asymmetric readout error.

    The noise is structured so the T1 decay is applied, then the readout bitflip, then measurement.
    If a circuit contains measurements, they must be in moments that don't also contain gates.
    """

    def __init__(self, depol_prob: float, bitflip_prob: float, decay_prob: float):
        self.qubit_noise_gate = alphaclops.DepolarizingChannel(depol_prob)
        self.readout_noise_gate = alphaclops.BitFlipChannel(bitflip_prob)
        self.readout_decay_gate = alphaclops.AmplitudeDampingChannel(decay_prob)

    def noisy_moment(self, moment: 'alphaclops.Moment', system_qubits: Sequence['alphaclops.Qid']):
        if alphaclops.devices.noise_model.validate_all_measurements(moment):
            return [
                alphaclops.Moment(self.readout_decay_gate(q) for q in system_qubits),
                alphaclops.Moment(self.readout_noise_gate(q) for q in system_qubits),
                moment,
            ]
        else:
            return [moment, alphaclops.Moment(self.qubit_noise_gate(q) for q in system_qubits)]


def test_calibrate_readout_error():
    sampler = alphaclops.DensityMatrixSimulator(
        noise=DepolarizingWithDampedReadoutNoiseModel(
            depol_prob=1e-3, bitflip_prob=0.03, decay_prob=0.03
        ),
        seed=10,
    )
    readout_calibration = cw.calibrate_readout_error(
        qubits=alphaclops.LineQubit.range(2),
        sampler=sampler,
        stopping_criteria=cw.RepetitionsStoppingCriteria(100_000),
    )
    means = readout_calibration.means()
    assert len(means) == 2, 'Two qubits'
    assert np.all(means > 0.89)
    assert np.all(means < 0.91)
