# pylint: disable=wrong-or-nonexistent-copyright-notice
import random

import numpy as np
import pytest
import sympy

import alphaclops


def test_init_properties():
    g = alphaclops.PhasedXZGate(x_exponent=0.125, z_exponent=0.25, axis_phase_exponent=0.375)
    assert g.x_exponent == 0.125
    assert g.z_exponent == 0.25
    assert g.axis_phase_exponent == 0.375


def test_eq():
    eq = alphaclops.testing.EqualsTester()
    eq.make_equality_group(
        lambda: alphaclops.PhasedXZGate(x_exponent=0.25, z_exponent=0.5, axis_phase_exponent=0.75)
    )

    # Sensitive to each parameter.
    eq.add_equality_group(alphaclops.PhasedXZGate(x_exponent=0, z_exponent=0.5, axis_phase_exponent=0.75))
    eq.add_equality_group(
        alphaclops.PhasedXZGate(x_exponent=0.25, z_exponent=0, axis_phase_exponent=0.75)
    )
    eq.add_equality_group(alphaclops.PhasedXZGate(x_exponent=0.25, z_exponent=0.5, axis_phase_exponent=0))

    # Different from other gates.
    eq.add_equality_group(alphaclops.PhasedXPowGate(exponent=0.25, phase_exponent=0.75))
    eq.add_equality_group(alphaclops.X)
    eq.add_equality_group(alphaclops.PhasedXZGate(x_exponent=1, z_exponent=0, axis_phase_exponent=0))


def test_canonicalization():
    def f(x, z, a):
        return alphaclops.PhasedXZGate(x_exponent=x, z_exponent=z, axis_phase_exponent=a)

    # Canonicalizations are equivalent.
    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(f(-1, 0, 0), f(-3, 0, 0), f(1, 1, 0.5))
    """
    # Canonicalize X exponent (-1, +1].
    if isinstance(x, numbers.Real):
        x %= 2
        if x > 1:
            x -= 2
    # Axis phase exponent is irrelevant if there is no X exponent.
    # Canonicalize Z exponent (-1, +1].
    if isinstance(z, numbers.Real):
        z %= 2
        if z > 1:
            z -= 2

    # Canonicalize axis phase exponent into (-0.5, +0.5].
    if isinstance(a, numbers.Real):
        a %= 2
        if a > 1:
            a -= 2
        if a <= -0.5:
            a += 1
            x = -x
        elif a > 0.5:
            a -= 1
            x = -x
    """

    # X rotation gets canonicalized.
    t = f(3, 0, 0)._canonical()
    assert t.x_exponent == 1
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == 0
    t = f(1.5, 0, 0)._canonical()
    assert t.x_exponent == -0.5
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == 0

    # Z rotation gets canonicalized.
    t = f(0, 3, 0)._canonical()
    assert t.x_exponent == 0
    assert t.z_exponent == 1
    assert t.axis_phase_exponent == 0
    t = f(0, 1.5, 0)._canonical()
    assert t.x_exponent == 0
    assert t.z_exponent == -0.5
    assert t.axis_phase_exponent == 0

    # Axis phase gets canonicalized.
    t = f(0.5, 0, 2.25)._canonical()
    assert t.x_exponent == 0.5
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == 0.25
    t = f(0.5, 0, 1.25)._canonical()
    assert t.x_exponent == -0.5
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == 0.25
    t = f(0.5, 0, 0.75)._canonical()
    assert t.x_exponent == -0.5
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == -0.25

    # 180 degree rotations don't need a virtual Z.
    t = f(1, 1, 0.5)._canonical()
    assert t.x_exponent == 1
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == 0
    t = f(1, 0.25, 0.5)._canonical()
    assert t.x_exponent == 1
    assert t.z_exponent == 0
    assert t.axis_phase_exponent == -0.375
    alphaclops.testing.assert_allclose_up_to_global_phase(
        alphaclops.unitary(t), alphaclops.unitary(f(1, 0.25, 0.5)), atol=1e-8
    )

    # Axis phase is irrelevant when not rotating.
    t = f(0, 0.25, 0.5)._canonical()
    assert t.x_exponent == 0
    assert t.z_exponent == 0.25
    assert t.axis_phase_exponent == 0


def test_from_matrix():
    # Axis rotations.
    assert alphaclops.approx_eq(
        alphaclops.PhasedXZGate.from_matrix(alphaclops.unitary(alphaclops.X ** 0.1)),
        alphaclops.PhasedXZGate(x_exponent=0.1, z_exponent=0, axis_phase_exponent=0),
        atol=1e-8,
    )
    assert alphaclops.approx_eq(
        alphaclops.PhasedXZGate.from_matrix(alphaclops.unitary(alphaclops.X ** -0.1)),
        alphaclops.PhasedXZGate(x_exponent=-0.1, z_exponent=0, axis_phase_exponent=0),
        atol=1e-8,
    )
    assert alphaclops.approx_eq(
        alphaclops.PhasedXZGate.from_matrix(alphaclops.unitary(alphaclops.Y ** 0.1)),
        alphaclops.PhasedXZGate(x_exponent=0.1, z_exponent=0, axis_phase_exponent=0.5),
        atol=1e-8,
    )
    assert alphaclops.approx_eq(
        alphaclops.PhasedXZGate.from_matrix(alphaclops.unitary(alphaclops.Y ** -0.1)),
        alphaclops.PhasedXZGate(x_exponent=-0.1, z_exponent=0, axis_phase_exponent=0.5),
        atol=1e-8,
    )
    assert alphaclops.approx_eq(
        alphaclops.PhasedXZGate.from_matrix(alphaclops.unitary(alphaclops.Z ** -0.1)),
        alphaclops.PhasedXZGate(x_exponent=0, z_exponent=-0.1, axis_phase_exponent=0),
        atol=1e-8,
    )
    assert alphaclops.approx_eq(
        alphaclops.PhasedXZGate.from_matrix(alphaclops.unitary(alphaclops.Z ** 0.1)),
        alphaclops.PhasedXZGate(x_exponent=0, z_exponent=0.1, axis_phase_exponent=0),
        atol=1e-8,
    )

    # Pauli matrices.
    assert alphaclops.approx_eq(
        alphaclops.PhasedXZGate.from_matrix(np.eye(2)),
        alphaclops.PhasedXZGate(x_exponent=0, z_exponent=0, axis_phase_exponent=0),
        atol=1e-8,
    )
    assert alphaclops.approx_eq(
        alphaclops.PhasedXZGate.from_matrix(alphaclops.unitary(alphaclops.X)),
        alphaclops.PhasedXZGate(x_exponent=1, z_exponent=0, axis_phase_exponent=0),
        atol=1e-8,
    )
    assert alphaclops.approx_eq(
        alphaclops.PhasedXZGate.from_matrix(alphaclops.unitary(alphaclops.Y)),
        alphaclops.PhasedXZGate(x_exponent=1, z_exponent=0, axis_phase_exponent=0.5),
        atol=1e-8,
    )
    assert alphaclops.approx_eq(
        alphaclops.PhasedXZGate.from_matrix(alphaclops.unitary(alphaclops.Z)),
        alphaclops.PhasedXZGate(x_exponent=0, z_exponent=1, axis_phase_exponent=0),
        atol=1e-8,
    )

    # Round trips.
    a = random.random()
    b = random.random()
    c = random.random()
    g = alphaclops.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=c)
    assert alphaclops.approx_eq(alphaclops.PhasedXZGate.from_matrix(alphaclops.unitary(g)), g, atol=1e-8)


@pytest.mark.parametrize(
    'unitary',
    [
        alphaclops.testing.random_unitary(2),
        alphaclops.testing.random_unitary(2),
        alphaclops.testing.random_unitary(2),
        np.array([[0, 1], [1j, 0]]),
    ],
)
def test_from_matrix_close_unitary(unitary: np.ndarray):
    alphaclops.testing.assert_allclose_up_to_global_phase(
        alphaclops.unitary(alphaclops.PhasedXZGate.from_matrix(unitary)), unitary, atol=1e-8
    )


@pytest.mark.parametrize(
    'unitary',
    [
        alphaclops.testing.random_unitary(2),
        alphaclops.testing.random_unitary(2),
        alphaclops.testing.random_unitary(2),
        np.array([[0, 1], [1j, 0]]),
    ],
)
def test_from_matrix_close_kraus(unitary: np.ndarray):
    gate = alphaclops.PhasedXZGate.from_matrix(unitary)
    kraus = alphaclops.kraus(gate)
    assert len(kraus) == 1
    alphaclops.testing.assert_allclose_up_to_global_phase(kraus[0], unitary, atol=1e-8)


def test_protocols():
    a = random.random()
    b = random.random()
    c = random.random()
    g = alphaclops.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=c)
    alphaclops.testing.assert_implements_consistent_protocols(g)

    # Symbolic.
    t = sympy.Symbol('t')
    g = alphaclops.PhasedXZGate(x_exponent=t, z_exponent=b, axis_phase_exponent=c)
    alphaclops.testing.assert_implements_consistent_protocols(g)
    g = alphaclops.PhasedXZGate(x_exponent=a, z_exponent=t, axis_phase_exponent=c)
    alphaclops.testing.assert_implements_consistent_protocols(g)
    g = alphaclops.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=t)
    alphaclops.testing.assert_implements_consistent_protocols(g)


def test_inverse():
    a = random.random()
    b = random.random()
    c = random.random()
    q = alphaclops.LineQubit(0)
    g = alphaclops.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=c).on(q)

    alphaclops.testing.assert_allclose_up_to_global_phase(
        alphaclops.unitary(g ** -1), np.transpose(np.conjugate(alphaclops.unitary(g))), atol=1e-8
    )


@pytest.mark.parametrize('resolve_fn', [alphaclops.resolve_parameters, alphaclops.resolve_parameters_once])
def test_parameterized(resolve_fn):
    a = random.random()
    b = random.random()
    c = random.random()
    g = alphaclops.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=c)
    assert not alphaclops.is_parameterized(g)

    t = sympy.Symbol('t')
    gt = alphaclops.PhasedXZGate(x_exponent=t, z_exponent=b, axis_phase_exponent=c)
    assert alphaclops.is_parameterized(gt)
    assert resolve_fn(gt, {'t': a}) == g
    gt = alphaclops.PhasedXZGate(x_exponent=a, z_exponent=t, axis_phase_exponent=c)
    assert alphaclops.is_parameterized(gt)
    assert resolve_fn(gt, {'t': b}) == g
    gt = alphaclops.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=t)
    assert alphaclops.is_parameterized(gt)
    assert resolve_fn(gt, {'t': c}) == g

    resolver = {'t': 0.5j}
    with pytest.raises(ValueError, match='Complex exponent'):
        resolve_fn(alphaclops.PhasedXZGate(x_exponent=t, z_exponent=b, axis_phase_exponent=c), resolver)
    with pytest.raises(ValueError, match='Complex exponent'):
        resolve_fn(alphaclops.PhasedXZGate(x_exponent=a, z_exponent=t, axis_phase_exponent=c), resolver)
    with pytest.raises(ValueError, match='Complex exponent'):
        resolve_fn(alphaclops.PhasedXZGate(x_exponent=a, z_exponent=b, axis_phase_exponent=t), resolver)


def test_str_diagram():
    g = alphaclops.PhasedXZGate(x_exponent=0.5, z_exponent=0.25, axis_phase_exponent=0.125)

    assert str(g) == "PhXZ(a=0.125,x=0.5,z=0.25)"

    alphaclops.testing.assert_has_diagram(
        alphaclops.Circuit(g.on(alphaclops.LineQubit(0))),
        """
0: ───PhXZ(a=0.125,x=0.5,z=0.25)───
    """,
    )
