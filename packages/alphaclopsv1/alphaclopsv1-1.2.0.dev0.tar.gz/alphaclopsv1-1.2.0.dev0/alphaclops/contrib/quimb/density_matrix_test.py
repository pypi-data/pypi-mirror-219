# pylint: disable=wrong-or-nonexistent-copyright-notice
import numpy as np

import alphaclops
import alphaclops.contrib.quimb as ccq


def test_tensor_density_matrix_1():
    q = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.YPowGate(exponent=0.25).on(q[0]))

    rho1 = alphaclops.final_density_matrix(c, qubit_order=q, dtype=np.complex128)
    rho2 = ccq.tensor_density_matrix(c, q)
    np.testing.assert_allclose(rho1, rho2, atol=1e-15)


def test_tensor_density_matrix_optional_qubits():
    q = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(alphaclops.YPowGate(exponent=0.25).on(q[0]))

    rho1 = alphaclops.final_density_matrix(c, dtype=np.complex128)
    rho2 = ccq.tensor_density_matrix(c)
    np.testing.assert_allclose(rho1, rho2, atol=1e-15)


def test_tensor_density_matrix_noise_1():
    q = alphaclops.LineQubit.range(2)
    c = alphaclops.Circuit(
        alphaclops.YPowGate(exponent=0.25).on(q[0]),
        alphaclops.amplitude_damp(1e-2).on(q[0]),
        alphaclops.phase_damp(1e-3).on(q[0]),
    )

    rho1 = alphaclops.final_density_matrix(c, qubit_order=q, dtype=np.complex128)
    rho2 = ccq.tensor_density_matrix(c, q)
    np.testing.assert_allclose(rho1, rho2, atol=1e-15)


def test_tensor_density_matrix_2():
    q = alphaclops.LineQubit.range(2)
    rs = np.random.RandomState(52)
    for _ in range(10):
        g = alphaclops.MatrixGate(alphaclops.testing.random_unitary(dim=2 ** len(q), random_state=rs))
        c = alphaclops.Circuit(g.on(*q))
        rho1 = alphaclops.final_density_matrix(c, dtype=np.complex128)
        rho2 = ccq.tensor_density_matrix(c, q)
        np.testing.assert_allclose(rho1, rho2, atol=1e-8)


def test_tensor_density_matrix_3():
    qubits = alphaclops.LineQubit.range(10)
    circuit = alphaclops.testing.random_circuit(qubits=qubits, n_moments=10, op_density=0.8)
    rho1 = alphaclops.final_density_matrix(circuit, dtype=np.complex128)
    rho2 = ccq.tensor_density_matrix(circuit, qubits)
    np.testing.assert_allclose(rho1, rho2, atol=1e-8)


def test_tensor_density_matrix_4():
    qubits = alphaclops.LineQubit.range(4)
    circuit = alphaclops.testing.random_circuit(qubits=qubits, n_moments=100, op_density=0.8)
    circuit = alphaclops.drop_empty_moments(circuit)
    noise_model = alphaclops.ConstantQubitNoiseModel(alphaclops.DepolarizingChannel(p=1e-3))
    circuit = alphaclops.Circuit(noise_model.noisy_moments(circuit.moments, qubits))
    rho1 = alphaclops.final_density_matrix(circuit, dtype=np.complex128)
    rho2 = ccq.tensor_density_matrix(circuit, qubits)
    np.testing.assert_allclose(rho1, rho2, atol=1e-8)


def test_tensor_density_matrix_gridqubit():
    qubits = alphaclops.TensorCircuit.rect(2, 2)
    circuit = alphaclops.testing.random_circuit(qubits=qubits, n_moments=10, op_density=0.8)
    circuit = alphaclops.drop_empty_moments(circuit)
    noise_model = alphaclops.ConstantQubitNoiseModel(alphaclops.DepolarizingChannel(p=1e-3))
    circuit = alphaclops.Circuit(noise_model.noisy_moments(circuit.moments, qubits))
    rho1 = alphaclops.final_density_matrix(circuit, dtype=np.complex128)
    rho2 = ccq.tensor_density_matrix(circuit, qubits)
    np.testing.assert_allclose(rho1, rho2, atol=1e-8)
