# pylint: disable=wrong-or-nonexistent-copyright-notice
import alphaclops
import numpy as np
import pytest


def test_matrix_mixture_from_mixture():
    q0 = alphaclops.LineQubit(0)
    dp = alphaclops.depolarize(0.1)
    mm = alphaclops.MixedUnitaryChannel.from_mixture(dp, key='dp')
    assert alphaclops.measurement_key_name(mm) == 'dp'
    alphaclops.testing.assert_consistent_channel(mm)
    alphaclops.testing.assert_consistent_mixture(mm)

    circuit = alphaclops.Circuit(mm.on(q0))
    sim = alphaclops.Simulator(seed=0)

    results = sim.simulate(circuit)
    assert 'dp' in results.measurements
    # The depolarizing channel is composed of four unitaries.
    assert results.measurements['dp'] in range(4)


def test_matrix_mixture_equality():
    dp_pt1 = alphaclops.depolarize(0.1)
    dp_pt2 = alphaclops.depolarize(0.2)
    mm_a1 = alphaclops.MixedUnitaryChannel.from_mixture(dp_pt1, key='a')
    mm_a2 = alphaclops.MixedUnitaryChannel.from_mixture(dp_pt2, key='a')
    mm_b1 = alphaclops.MixedUnitaryChannel.from_mixture(dp_pt1, key='b')

    # Even if their effect is the same, MixedUnitaryChannels are not treated
    # as equal to other channels defined in alphaclops.
    assert mm_a1 != dp_pt1
    assert mm_a1 != mm_a2
    assert mm_a1 != mm_b1
    assert mm_a2 != mm_b1

    mix = [(0.5, np.array([[1, 0], [0, 1]])), (0.5, np.array([[0, 1], [1, 0]]))]
    half_flip = alphaclops.MixedUnitaryChannel(mix)
    mix_inv = list(reversed(mix))
    half_flip_inv = alphaclops.MixedUnitaryChannel(mix_inv)
    # Even though these have the same effect on the circuit, their measurement
    # behavior differs, so they are considered non-equal.
    assert half_flip != half_flip_inv


def test_matrix_mixture_remap_keys():
    dp = alphaclops.depolarize(0.1)
    mm = alphaclops.MixedUnitaryChannel.from_mixture(dp)
    with pytest.raises(TypeError):
        _ = alphaclops.measurement_key_name(mm)
    assert alphaclops.with_measurement_key_mapping(mm, {'a': 'b'}) is NotImplemented

    mm_x = alphaclops.MixedUnitaryChannel.from_mixture(dp, key='x')
    assert alphaclops.with_measurement_key_mapping(mm_x, {'a': 'b'}) is mm_x
    assert alphaclops.measurement_key_name(alphaclops.with_key_path(mm_x, ('path',))) == 'path:x'

    mm_a = alphaclops.MixedUnitaryChannel.from_mixture(dp, key='a')
    mm_b = alphaclops.MixedUnitaryChannel.from_mixture(dp, key='b')
    assert mm_a != mm_b
    assert alphaclops.with_measurement_key_mapping(mm_a, {'a': 'b'}) == mm_b


def test_matrix_mixture_from_unitaries():
    q0 = alphaclops.LineQubit(0)
    mix = [(0.5, np.array([[1, 0], [0, 1]])), (0.5, np.array([[0, 1], [1, 0]]))]
    half_flip = alphaclops.MixedUnitaryChannel(mix, key='flip')
    assert alphaclops.measurement_key_name(half_flip) == 'flip'

    circuit = alphaclops.Circuit(half_flip.on(q0), alphaclops.measure(q0, key='m'))
    sim = alphaclops.Simulator(seed=0)

    results = sim.simulate(circuit)
    assert 'flip' in results.measurements
    assert results.measurements['flip'] == results.measurements['m']


def test_matrix_mixture_str():
    mix = [(0.5, np.array([[1, 0], [0, 1]])), (0.5, np.array([[0, 1], [1, 0]]))]
    half_flip = alphaclops.MixedUnitaryChannel(mix)
    assert (
        str(half_flip)
        == """MixedUnitaryChannel([(0.5, array([[1, 0],
       [0, 1]])), (0.5, array([[0, 1],
       [1, 0]]))])"""
    )
    half_flip_keyed = alphaclops.MixedUnitaryChannel(mix, key='flip')
    assert (
        str(half_flip_keyed)
        == """MixedUnitaryChannel([(0.5, array([[1, 0],
       [0, 1]])), (0.5, array([[0, 1],
       [1, 0]]))], key=flip)"""
    )


def test_matrix_mixture_repr():
    mix = [
        (0.5, np.array([[1, 0], [0, 1]], dtype=np.dtype('complex64'))),
        (0.5, np.array([[0, 1], [1, 0]], dtype=np.dtype('complex64'))),
    ]
    half_flip = alphaclops.MixedUnitaryChannel(mix, key='flip')
    assert (
        repr(half_flip)
        == """\
alphaclops.MixedUnitaryChannel(mixture=[\
(0.5, np.array([[(1+0j), 0j], [0j, (1+0j)]], dtype=np.dtype('complex64'))), \
(0.5, np.array([[0j, (1+0j)], [(1+0j), 0j]], dtype=np.dtype('complex64')))], \
key='flip')"""
    )


def test_mix_no_unitaries_fails():
    with pytest.raises(ValueError, match='must have at least one unitary'):
        _ = alphaclops.MixedUnitaryChannel(mixture=[], key='m')


def test_mix_bad_prob_fails():
    mix = [(0.5, np.array([[1, 0], [0, 0]]))]

    with pytest.raises(ValueError, match='Unitary probabilities must sum to 1'):
        _ = alphaclops.MixedUnitaryChannel(mixture=mix, key='m')


def test_mix_mismatch_fails():
    op2 = np.zeros((4, 4))
    op2[1][1] = 1
    mix = [(0.5, np.array([[1, 0], [0, 0]])), (0.5, op2)]

    with pytest.raises(ValueError, match='Inconsistent unitary shapes'):
        _ = alphaclops.MixedUnitaryChannel(mixture=mix, key='m')


def test_nonqubit_mixture_fails():
    mix = [(0.5, np.array([[1, 0, 0], [0, 1, 0]])), (0.5, np.array([[0, 1, 0], [1, 0, 0]]))]

    with pytest.raises(ValueError, match='Input mixture'):
        _ = alphaclops.MixedUnitaryChannel(mixture=mix, key='m')


def test_validate():
    mix = [(0.5, np.array([[1, 0], [0, 0]])), (0.5, np.array([[0, 0], [0, 1]]))]
    with pytest.raises(ValueError, match='non-unitary'):
        _ = alphaclops.MixedUnitaryChannel(mixture=mix, key='m', validate=True)
