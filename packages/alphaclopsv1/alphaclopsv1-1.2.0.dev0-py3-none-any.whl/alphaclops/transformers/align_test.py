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


def test_align_basic_no_context():
    q1 = alphaclops.NamedQubit('q1')
    q2 = alphaclops.NamedQubit('q2')
    c = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.X(q1)]),
            alphaclops.Moment([alphaclops.Y(q1), alphaclops.X(q2)]),
            alphaclops.Moment([alphaclops.X(q1)]),
        ]
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.align_left(c),
        alphaclops.Circuit(
            alphaclops.Moment([alphaclops.X(q1), alphaclops.X(q2)]),
            alphaclops.Moment([alphaclops.Y(q1)]),
            alphaclops.Moment([alphaclops.X(q1)]),
        ),
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.align_right(c),
        alphaclops.Circuit(
            alphaclops.Moment([alphaclops.X(q1)]),
            alphaclops.Moment([alphaclops.Y(q1)]),
            alphaclops.Moment([alphaclops.X(q1), alphaclops.X(q2)]),
        ),
    )


def test_align_left_no_compile_context():
    q1 = alphaclops.NamedQubit('q1')
    q2 = alphaclops.NamedQubit('q2')
    alphaclops.testing.assert_same_circuits(
        alphaclops.align_left(
            alphaclops.Circuit(
                [
                    alphaclops.Moment([alphaclops.X(q1)]),
                    alphaclops.Moment([alphaclops.Y(q1), alphaclops.X(q2)]),
                    alphaclops.Moment([alphaclops.X(q1), alphaclops.Y(q2).with_tags("nocompile")]),
                    alphaclops.Moment([alphaclops.Y(q1)]),
                    alphaclops.measure(*[q1, q2], key='a'),
                ]
            ),
            context=alphaclops.TransformerContext(tags_to_ignore=["nocompile"]),
        ),
        alphaclops.Circuit(
            [
                alphaclops.Moment([alphaclops.X(q1), alphaclops.X(q2)]),
                alphaclops.Moment([alphaclops.Y(q1)]),
                alphaclops.Moment([alphaclops.X(q1), alphaclops.Y(q2).with_tags("nocompile")]),
                alphaclops.Moment([alphaclops.Y(q1)]),
                alphaclops.measure(*[q1, q2], key='a'),
            ]
        ),
    )


def test_align_left_deep():
    q1, q2 = alphaclops.LineQubit.range(2)
    c_nested = alphaclops.FrozenCircuit(
        [
            alphaclops.Moment([alphaclops.X(q1)]),
            alphaclops.Moment([alphaclops.Y(q2)]),
            alphaclops.Moment([alphaclops.Z(q1), alphaclops.Y(q2).with_tags("nocompile")]),
            alphaclops.Moment([alphaclops.Y(q1)]),
            alphaclops.measure(q2, key='a'),
            alphaclops.Z(q1).with_classical_controls('a'),
        ]
    )
    c_nested_aligned = alphaclops.FrozenCircuit(
        alphaclops.Moment(alphaclops.X(q1), alphaclops.Y(q2)),
        alphaclops.Moment(alphaclops.Z(q1)),
        alphaclops.Moment([alphaclops.Y(q1), alphaclops.Y(q2).with_tags("nocompile")]),
        alphaclops.measure(q2, key='a'),
        alphaclops.Z(q1).with_classical_controls('a'),
    )
    c_orig = alphaclops.Circuit(
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(6).with_tags("nocompile"),
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(5).with_tags("preserve_tag"),
    )
    c_expected = alphaclops.Circuit(
        c_nested_aligned,
        alphaclops.CircuitOperation(c_nested).repeat(6).with_tags("nocompile"),
        c_nested_aligned,
        alphaclops.CircuitOperation(c_nested_aligned).repeat(5).with_tags("preserve_tag"),
    )
    context = alphaclops.TransformerContext(tags_to_ignore=["nocompile"], deep=True)
    alphaclops.testing.assert_same_circuits(alphaclops.align_left(c_orig, context=context), c_expected)


def test_align_left_subset_of_operations():
    q1 = alphaclops.NamedQubit('q1')
    q2 = alphaclops.NamedQubit('q2')
    tag = "op_to_align"
    c_orig = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.Y(q1)]),
            alphaclops.Moment([alphaclops.X(q2)]),
            alphaclops.Moment([alphaclops.X(q1).with_tags(tag)]),
            alphaclops.Moment([alphaclops.Y(q2)]),
            alphaclops.measure(*[q1, q2], key='a'),
        ]
    )
    c_exp = alphaclops.Circuit(
        [
            alphaclops.Moment([alphaclops.Y(q1)]),
            alphaclops.Moment([alphaclops.X(q1).with_tags(tag), alphaclops.X(q2)]),
            alphaclops.Moment(),
            alphaclops.Moment([alphaclops.Y(q2)]),
            alphaclops.measure(*[q1, q2], key='a'),
        ]
    )
    alphaclops.testing.assert_same_circuits(
        alphaclops.toggle_tags(
            alphaclops.align_left(
                alphaclops.toggle_tags(c_orig, [tag]),
                context=alphaclops.TransformerContext(tags_to_ignore=[tag]),
            ),
            [tag],
        ),
        c_exp,
    )


def test_align_right_no_compile_context():
    q1 = alphaclops.NamedQubit('q1')
    q2 = alphaclops.NamedQubit('q2')
    alphaclops.testing.assert_same_circuits(
        alphaclops.align_right(
            alphaclops.Circuit(
                [
                    alphaclops.Moment([alphaclops.X(q1)]),
                    alphaclops.Moment([alphaclops.Y(q1), alphaclops.X(q2).with_tags("nocompile")]),
                    alphaclops.Moment([alphaclops.X(q1), alphaclops.Y(q2)]),
                    alphaclops.Moment([alphaclops.Y(q1)]),
                    alphaclops.measure(*[q1, q2], key='a'),
                ]
            ),
            context=alphaclops.TransformerContext(tags_to_ignore=["nocompile"]),
        ),
        alphaclops.Circuit(
            [
                alphaclops.Moment([alphaclops.X(q1)]),
                alphaclops.Moment([alphaclops.Y(q1), alphaclops.X(q2).with_tags("nocompile")]),
                alphaclops.Moment([alphaclops.X(q1)]),
                alphaclops.Moment([alphaclops.Y(q1), alphaclops.Y(q2)]),
                alphaclops.measure(*[q1, q2], key='a'),
            ]
        ),
    )


def test_align_right_deep():
    q1, q2 = alphaclops.LineQubit.range(2)
    c_nested = alphaclops.FrozenCircuit(
        alphaclops.Moment([alphaclops.X(q1)]),
        alphaclops.Moment([alphaclops.Y(q1), alphaclops.X(q2).with_tags("nocompile")]),
        alphaclops.Moment([alphaclops.X(q2)]),
        alphaclops.Moment([alphaclops.Y(q1)]),
        alphaclops.measure(q1, key='a'),
        alphaclops.Z(q2).with_classical_controls('a'),
    )
    c_nested_aligned = alphaclops.FrozenCircuit(
        alphaclops.Moment([alphaclops.X(q1), alphaclops.X(q2).with_tags("nocompile")]),
        [alphaclops.Y(q1), alphaclops.Y(q1)],
        alphaclops.Moment(alphaclops.measure(q1, key='a'), alphaclops.X(q2)),
        alphaclops.Z(q2).with_classical_controls('a'),
    )
    c_orig = alphaclops.Circuit(
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(6).with_tags("nocompile"),
        c_nested,
        alphaclops.CircuitOperation(c_nested).repeat(5).with_tags("preserve_tag"),
    )
    c_expected = alphaclops.Circuit(
        c_nested_aligned,
        alphaclops.CircuitOperation(c_nested).repeat(6).with_tags("nocompile"),
        alphaclops.Moment(),
        c_nested_aligned,
        alphaclops.CircuitOperation(c_nested_aligned).repeat(5).with_tags("preserve_tag"),
    )
    context = alphaclops.TransformerContext(tags_to_ignore=["nocompile"], deep=True)
    alphaclops.testing.assert_same_circuits(alphaclops.align_right(c_orig, context=context), c_expected)


def test_classical_control():
    q0, q1 = alphaclops.LineQubit.range(2)
    circuit = alphaclops.Circuit(
        alphaclops.H(q0), alphaclops.measure(q0, key='m'), alphaclops.X(q1).with_classical_controls('m')
    )
    alphaclops.testing.assert_same_circuits(alphaclops.align_left(circuit), circuit)
    alphaclops.testing.assert_same_circuits(alphaclops.align_right(circuit), circuit)
