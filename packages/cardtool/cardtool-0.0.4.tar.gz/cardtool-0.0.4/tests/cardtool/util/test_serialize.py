from contextlib import nullcontext as does_not_raise
from io import StringIO
from typing import Type

import pytest
from hamcrest import assert_that, equal_to, instance_of

from cardtool.card.model import CardReadingData
from cardtool.util.serialize import (
    CustomJSONSerializer,
    JSONSerializer,
    Serializer,
    YAMLSerializer,
    new_serializer,
)


@pytest.mark.parametrize(
    "serializer,tp,expectation",
    [
        ("yaml", YAMLSerializer, does_not_raise()),
        ("json", JSONSerializer, does_not_raise()),
        ("other", None, pytest.raises(ValueError, match="unknown serializer")),
    ],
)
def test_new_serializer_should_a_custom_serializer_when_called(
    serializer: str, tp: Type, expectation
):
    with expectation:
        serialize = new_serializer(serializer)
        assert_that(serialize, instance_of(tp))
        assert_that(issubclass(serialize.__class__, Serializer))


@pytest.mark.parametrize(
    "data,expected,expectation",
    [
        (
            "1",
            '"1"',
            pytest.raises(
                TypeError, match="^Object of type str is not JSON serializable$"
            ),
        ),
        (
            CardReadingData(),
            {"tlv": "", "track1": "", "track2": "", "pin_block": "", "label": ""},
            does_not_raise(),
        ),
    ],
    ids=[
        "raise an error when it cannot serialize a type",
        "serialize a dataclass turning it into a dict",
    ],
)
def test_custom_json_serializer_should_(data, expected, expectation):
    with expectation:
        custom_ser = CustomJSONSerializer()
        out = custom_ser.default(data)
        assert_that(out, equal_to(expected))


@pytest.mark.parametrize(
    "data,expected",
    [
        ((1, 2), """[1, 2]"""),
        (
            (CardReadingData() for i in range(2)),
            """[{"tlv": "", "track1": "", "track2": "", "pin_block": "", "label": ""}, {"tlv": "", "track1": "", "track2": "", "pin_block": "", "label": ""}]""",  # noqa: E501
        ),
    ],
)
def test_serialize_json_should_dump_successfully_when_called(data, expected):
    out = StringIO()
    serialize = JSONSerializer()
    serialize(data, out)
    out_data = out.getvalue()
    assert_that(out_data, equal_to(expected))


def test_serialize_yaml_should_dump_successfully_when_called():
    out = StringIO()
    serialize = YAMLSerializer()
    data = ({i: i} for i in range(2))
    serialize(data, out)
    out_data = out.getvalue()
    expected_data = """0: 0
---
1: 1
"""
    assert_that(out_data, equal_to(expected_data))
