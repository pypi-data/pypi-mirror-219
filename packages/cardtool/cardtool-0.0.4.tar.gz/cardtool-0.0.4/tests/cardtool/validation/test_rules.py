import re
from contextlib import nullcontext as does_not_raise

import pytest
from hamcrest import assert_that, equal_to

from cardtool.validation.rules import length, length_between, regex


@pytest.mark.parametrize(
    "input,rule,expectation",
    [
        ("1" * 10, 10, does_not_raise()),
        (
            "2" * 10,
            8,
            pytest.raises(
                ValueError, match=f"{'2' * 10} does not have required length {8}"
            ),
        ),
    ],
    ids=["valid input", "invalid input"],
)
def test_should_validate_expected_length_when_called(input, rule, expectation):
    with expectation:
        validate = length(rule)
        out = validate(input)
        assert_that(out, equal_to(input))


@pytest.mark.parametrize(
    "input,rule,expectation,msg",
    [
        ("1" * 10, (1, 10), does_not_raise(), ""),
        (
            "2" * 11,
            (1, 10),
            pytest.raises(ValueError),
            f"{'2' * 11} length is not between (1, 10)",
        ),
        (
            "2" * 0,
            (1, 10),
            pytest.raises(ValueError),
            f"{'2' * 0} length is not between (1, 10)",
        ),
    ],
    ids=["valid input", "invalid max input", "invalid min input"],
)
def test_should_validate_length_between_expected_range_when_called(
    input, rule, expectation, msg
):
    with expectation as e:
        (min, max) = rule
        validate = length_between(min, max)
        out = validate(input)
        assert_that(out, equal_to(input))
    if e is not None:
        assert_that(e.value.args[0], equal_to(msg))


@pytest.mark.parametrize(
    "input,rule,expectation",
    [
        ("2" * 10, "2{1,10}", does_not_raise()),
        (
            "2" * 10,
            "[A-Z]{1,10}",
            pytest.raises(
                ValueError,
                match=re.escape(
                    "2222222222 does not conform with required pattern [A-Z]{1,10}"
                ),
            ),
        ),
    ],
    ids=["valid input", "invalid input"],
)
def test_should_validate_str_conforms_to_expected_regex_when_called(
    input, rule, expectation
):
    with expectation:
        validate = regex(rule, flags=0)
        out = validate(input)
        assert_that(out, equal_to(input))
