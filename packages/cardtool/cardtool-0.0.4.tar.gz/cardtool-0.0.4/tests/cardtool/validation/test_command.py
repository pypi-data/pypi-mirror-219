from contextlib import nullcontext as does_not_raise
from unittest.mock import Mock

import click
import pytest
from hamcrest import assert_that, equal_to

from cardtool.validation.command import apply_in_order, validate_string_callable


@pytest.mark.parametrize(
    "input,validators,expected_out,expectation",
    [
        (
            "1",
            [Mock(return_value="21"), Mock(return_value="12")],
            "12",
            does_not_raise(),
        ),
        (
            "2",
            [Mock(return_value="12"), Mock(side_effect=ValueError("error"))],
            None,
            pytest.raises(ValueError, match="^error$"),
        ),
    ],
    ids=["valid input", "invalid input"],
)
def test_should_trigger_a_chain_of_validators_when_called(
    input, validators, expected_out, expectation
):
    with expectation:
        validate = apply_in_order(*validators)
        out = validate(input)
        assert_that(out, equal_to(expected_out))
        first_validator = validators[0]
        first_validator.assert_called_with(input)
    for validator in reversed(validators[1:]):
        previous_validator = validators[validators.index(validator) - 1]
        validator.assert_called_with(previous_validator())


@pytest.mark.parametrize(
    "input,validator,expected_out,expectation",
    [
        ("1", Mock(return_value="1"), "1", does_not_raise()),
        (
            "2",
            Mock(side_effect=ValueError("error")),
            None,
            pytest.raises(click.BadParameter, match="error"),
        ),
        (
            3,
            Mock(side_effect=ValueError("parameter is not string")),
            None,
            pytest.raises(click.BadParameter, match="^parameter is not string$"),
        ),
        ("2", Mock(return_value="21"), "21", does_not_raise()),
    ],
    ids=[
        "valid input",
        "invalid input",
        "invalid int input",
        "valid input with transform",
    ],
)
def test_should_validate_an_option_when_called(
    input, validator, expected_out, expectation
):
    with expectation:
        callable_validator = validate_string_callable(validator)
        out = callable_validator({}, "", input)
        validator.assert_called_with(input)
        assert_that(out, equal_to(expected_out))
