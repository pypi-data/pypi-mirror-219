# pylint: disable=wrong-or-nonexistent-copyright-notice
import IPython.display
import numpy as np
import pytest

import alphaclops
from alphaclops.contrib.svg import circuit_to_svg


def test_svg():
    a, b, c = alphaclops.LineQubit.range(3)

    svg_text = circuit_to_svg(
        alphaclops.Circuit(
            alphaclops.CNOT(a, b),
            alphaclops.CZ(b, c),
            alphaclops.SWAP(a, c),
            alphaclops.PhasedXPowGate(exponent=0.123, phase_exponent=0.456).on(c),
            alphaclops.Z(a),
            alphaclops.measure(a, b, c, key='z'),
            alphaclops.MatrixGate(np.eye(2)).on(a),
        )
    )
    assert '?' in svg_text
    assert '<svg' in svg_text
    assert '</svg>' in svg_text


def test_svg_noise():
    noise_model = alphaclops.ConstantQubitNoiseModel(alphaclops.DepolarizingChannel(p=1e-3))
    q = alphaclops.LineQubit(0)
    circuit = alphaclops.Circuit(alphaclops.X(q))
    circuit = alphaclops.Circuit(noise_model.noisy_moments(circuit.moments, [q]))
    svg = circuit_to_svg(circuit)
    assert '>D(0.001)</text>' in svg


def test_validation():
    with pytest.raises(ValueError):
        circuit_to_svg(alphaclops.Circuit())


def test_empty_moments():
    a, b = alphaclops.LineQubit.range(2)
    svg_1 = circuit_to_svg(
        alphaclops.Circuit(
            alphaclops.Moment(),
            alphaclops.Moment(alphaclops.CNOT(a, b)),
            alphaclops.Moment(),
            alphaclops.Moment(alphaclops.SWAP(a, b)),
            alphaclops.Moment(alphaclops.Z(a)),
            alphaclops.Moment(alphaclops.measure(a, b, key='z')),
            alphaclops.Moment(),
        )
    )
    assert '<svg' in svg_1
    assert '</svg>' in svg_1

    svg_2 = circuit_to_svg(alphaclops.Circuit(alphaclops.Moment()))
    assert '<svg' in svg_2
    assert '</svg>' in svg_2


@pytest.mark.parametrize(
    'symbol,svg_symbol',
    [
        ('<a', '&lt;a'),
        ('<=b', '&lt;=b'),
        ('>c', '&gt;c'),
        ('>=d', '&gt;=d'),
        ('>e<', '&gt;e&lt;'),
        ('A[<virtual>]B[alphaclops.VirtualTag()]C>D<E', 'ABC&gt;D&lt;E'),
    ],
)
def test_gate_with_less_greater_str(symbol, svg_symbol):
    class CustomGate(alphaclops.Gate):
        def _num_qubits_(self) -> int:
            return 1

        def _circuit_diagram_info_(self, _) -> alphaclops.CircuitDiagramInfo:
            return alphaclops.CircuitDiagramInfo(wire_symbols=[symbol])

    circuit = alphaclops.Circuit(CustomGate().on(alphaclops.LineQubit(0)))
    svg = circuit_to_svg(circuit)

    _ = IPython.display.SVG(svg)
    assert svg_symbol in svg
