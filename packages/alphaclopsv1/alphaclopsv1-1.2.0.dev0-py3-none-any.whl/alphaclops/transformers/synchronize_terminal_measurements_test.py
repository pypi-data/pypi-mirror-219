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

import alphaclops

NO_COMPILE_TAG = "no_compile_tag"


def assert_optimizes(before, after, measure_only_moment=True, with_context=False):
    context = alphaclops.TransformerContext(tags_to_ignore=(NO_COMPILE_TAG,)) if with_context else None
    transformed_circuit = alphaclops.synchronize_terminal_measurements(
        before, context=context, after_other_operations=measure_only_moment
    )
    alphaclops.testing.assert_same_circuits(transformed_circuit, after)

    # Test nested circuit ops.
    context = alphaclops.TransformerContext(
        tags_to_ignore=("ignore",) + tuple([NO_COMPILE_TAG] if with_context else []), deep=True
    )
    c_nested = alphaclops.Circuit(
        before,
        alphaclops.CircuitOperation(before.freeze()).repeat(5).with_tags("ignore"),
        before,
        alphaclops.CircuitOperation(before.freeze()).repeat(6).with_tags("preserve_tag"),
        before,
    )
    c_expected = alphaclops.Circuit(
        before,
        alphaclops.CircuitOperation(before.freeze()).repeat(5).with_tags("ignore"),
        before,
        alphaclops.CircuitOperation(after.freeze()).repeat(6).with_tags("preserve_tag"),
        after,
    )
    transformed_circuit = alphaclops.synchronize_terminal_measurements(
        c_nested, context=context, after_other_operations=measure_only_moment
    )
    alphaclops.testing.assert_same_circuits(transformed_circuit, c_expected)


def test_no_move():
    q1 = alphaclops.NamedQubit('q1')
    before = alphaclops.Circuit([alphaclops.Moment([alphaclops.H(q1)])])
    after = before
    assert_optimizes(before=before, after=after)


def test_simple_align():
    q1 = alphaclops.NamedQubit('q1')
    q2 = alphaclops.NamedQubit('q2')
    before = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.H(q1), alphaclops.H(q2)]),
            alphaclops.Moment([alphaclops.measure(q1).with_tags(NO_COMPILE_TAG), alphaclops.Z(q2)]),
            alphaclops.Moment([alphaclops.measure(q2)]),
        ]
    )
    after = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.H(q1), alphaclops.H(q2)]),
            alphaclops.Moment([alphaclops.Z(q2)]),
            alphaclops.Moment([alphaclops.measure(q1).with_tags(NO_COMPILE_TAG), alphaclops.measure(q2)]),
        ]
    )
    assert_optimizes(before=before, after=after)
    assert_optimizes(before=before, after=before, with_context=True)


def test_simple_partial_align():
    q1 = alphaclops.NamedQubit('q1')
    q2 = alphaclops.NamedQubit('q2')
    before = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.measure(q1), alphaclops.Z(q2)]),
            alphaclops.Moment([alphaclops.Z(q1), alphaclops.measure(q2).with_tags(NO_COMPILE_TAG)]),
        ]
    )
    after = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.measure(q1), alphaclops.Z(q2)]),
            alphaclops.Moment([alphaclops.Z(q1)]),
            alphaclops.Moment([alphaclops.measure(q2).with_tags(NO_COMPILE_TAG)]),
        ]
    )
    assert_optimizes(before=before, after=after)
    assert_optimizes(before=before, after=before, with_context=True)


def test_slide_forward_one():
    q1 = alphaclops.NamedQubit('q1')
    q2 = alphaclops.NamedQubit('q2')
    q3 = alphaclops.NamedQubit('q3')
    before = alphaclops.Circuit(
        [alphaclops.Moment([alphaclops.H(q1), alphaclops.measure(q2).with_tags(NO_COMPILE_TAG), alphaclops.measure(q3)])]
    )
    after = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.H(q1)]),
            alphaclops.Moment([alphaclops.measure(q2).with_tags(NO_COMPILE_TAG), alphaclops.measure(q3)]),
        ]
    )
    after_no_compile = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.H(q1), alphaclops.measure(q2).with_tags(NO_COMPILE_TAG)]),
            alphaclops.Moment([alphaclops.measure(q3)]),
        ]
    )
    assert_optimizes(before=before, after=after)
    assert_optimizes(before=before, after=after_no_compile, with_context=True)


def test_no_slide_forward_one():
    q1 = alphaclops.NamedQubit('q1')
    q2 = alphaclops.NamedQubit('q2')
    q3 = alphaclops.NamedQubit('q3')
    before = alphaclops.Circuit([alphaclops.Moment([alphaclops.H(q1), alphaclops.measure(q2), alphaclops.measure(q3)])])
    after = alphaclops.Circuit([alphaclops.Moment([alphaclops.H(q1), alphaclops.measure(q2), alphaclops.measure(q3)])])
    assert_optimizes(before=before, after=after, measure_only_moment=False)


def test_blocked_shift_one():
    q1 = alphaclops.NamedQubit('q1')
    q2 = alphaclops.NamedQubit('q2')
    before = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.H(q1), alphaclops.H(q2)]),
            alphaclops.Moment([alphaclops.measure(q1), alphaclops.Z(q2)]),
            alphaclops.Moment([alphaclops.H(q1), alphaclops.measure(q2).with_tags(NO_COMPILE_TAG)]),
        ]
    )
    after = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.H(q1), alphaclops.H(q2)]),
            alphaclops.Moment([alphaclops.measure(q1), alphaclops.Z(q2)]),
            alphaclops.Moment([alphaclops.H(q1)]),
            alphaclops.Moment([alphaclops.measure(q2).with_tags(NO_COMPILE_TAG)]),
        ]
    )
    assert_optimizes(before=before, after=after)
    assert_optimizes(before=before, after=before, with_context=True)


def test_complex_move():
    q1 = alphaclops.NamedQubit('q1')
    q2 = alphaclops.NamedQubit('q2')
    q3 = alphaclops.NamedQubit('q3')
    before = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.H(q1), alphaclops.H(q2)]),
            alphaclops.Moment([alphaclops.measure(q1), alphaclops.Z(q2)]),
            alphaclops.Moment([alphaclops.H(q1), alphaclops.measure(q2).with_tags(NO_COMPILE_TAG)]),
            alphaclops.Moment([alphaclops.H(q3)]),
            alphaclops.Moment([alphaclops.X(q1), alphaclops.measure(q3).with_tags(NO_COMPILE_TAG)]),
        ]
    )
    after = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.H(q1), alphaclops.H(q2)]),
            alphaclops.Moment([alphaclops.measure(q1), alphaclops.Z(q2)]),
            alphaclops.Moment([alphaclops.H(q1)]),
            alphaclops.Moment([alphaclops.H(q3)]),
            alphaclops.Moment([alphaclops.X(q1)]),
            alphaclops.Moment(
                [
                    alphaclops.measure(q2).with_tags(NO_COMPILE_TAG),
                    alphaclops.measure(q3).with_tags(NO_COMPILE_TAG),
                ]
            ),
        ]
    )
    assert_optimizes(before=before, after=after)
    assert_optimizes(before=before, after=before, with_context=True)


def test_complex_move_no_slide():
    q1 = alphaclops.NamedQubit('q1')
    q2 = alphaclops.NamedQubit('q2')
    q3 = alphaclops.NamedQubit('q3')
    before = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.H(q1), alphaclops.H(q2)]),
            alphaclops.Moment([alphaclops.measure(q1), alphaclops.Z(q2)]),
            alphaclops.Moment([alphaclops.H(q1), alphaclops.measure(q2).with_tags(NO_COMPILE_TAG)]),
            alphaclops.Moment([alphaclops.H(q3)]),
            alphaclops.Moment([alphaclops.X(q1), alphaclops.measure(q3)]),
        ]
    )
    after = alphaclops.Circuit(
        [
            alphaclops.Moment(alphaclops.H(q1), alphaclops.H(q2)),
            alphaclops.Moment(alphaclops.measure(q1), alphaclops.Z(q2)),
            alphaclops.Moment(alphaclops.H(q1)),
            alphaclops.Moment(alphaclops.H(q3)),
            alphaclops.Moment(alphaclops.X(q1), alphaclops.measure(q2).with_tags(NO_COMPILE_TAG), alphaclops.measure(q3)),
        ]
    )
    assert_optimizes(before=before, after=after, measure_only_moment=False)
    assert_optimizes(before=before, after=before, measure_only_moment=False, with_context=True)


def test_multi_qubit():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(alphaclops.H(q1), alphaclops.measure(q0, q1, key='m'))
    assert_optimizes(before=circuit, after=circuit)


def test_classically_controlled_op():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.H(q0), alphaclops.measure(q0, key='m'), alphaclops.X(q1).with_classical_controls('m')
    )
    assert_optimizes(before=circuit, after=circuit)
