from contextlib import nullcontext as does_not_raise
from dataclasses import dataclass
from typing import Any, Type
from unittest.mock import call, mock_open, patch

import pytest
import yaml
from hamcrest import assert_that, equal_to

from cardtool.config.load import get_abs_path, safe_load


@dataclass
class Data(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!Test"
    name: str
    age: int


yaml_data = """
name: test
age: 1
"""

schema_data = """
{
  "$id": "https://d4n13l-4lf4.com/test-config.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TestConfig",
  "description": "A test configuration file",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "name": {
      "type": "string"
    },
    "age": {
      "type": "integer"
    }
  },
  "required": ["name"]
}
"""

dataclass_yaml_data = f"""
!Test{yaml_data}
"""


@pytest.mark.parametrize(
    "data,schema,cls,expected,expectation",
    [
        (yaml_data, schema_data, dict, {"name": "test", "age": 1}, does_not_raise()),
        (
            dataclass_yaml_data,
            schema_data,
            Data,
            Data("test", 1),
            does_not_raise(),
        ),
        (
            "",
            schema_data,
            dict,
            None,
            pytest.raises(ValueError, match="invalid configuration file"),
        ),
    ],
    ids=[
        "successfully when called",
        "successfully with py object when called",
        "with failure when it does not satisfies the schema",
    ],
)
def test_should_load_a_yaml_file_(
    data: str, schema: str, cls: Type, expected: Any, expectation
):
    data_open_mock = mock_open(read_data=data).return_value
    schema_open_mock = mock_open(read_data=schema).return_value
    root_open = mock_open()
    root_open.side_effect = (data_open_mock, schema_open_mock)

    with expectation, patch("cardtool.config.load.open", root_open):
        data_file = "test.yaml"
        schema_file = "schema.json"
        object_data: cls = safe_load(data_file, schema_file)
        calls = [
            call(data_file, mode="r", encoding="utf-8"),
            call(schema_file, mode="r", encoding="utf-8"),
        ]
        root_open.assert_has_calls(calls)
        assert_that(object_data, equal_to(expected))


@patch("cardtool.config.load.abspath")
def test_get_abs_path(abspath_patch):
    path = "test.yaml"
    test_dir = "test/"
    abspath_patch.side_effect = [test_dir]
    abs_path = get_abs_path(path)
    expected_path = "test/test.yaml"
    assert_that(abs_path, equal_to(expected_path))
