import pytest
from hamcrest import assert_that, equal_to

from cardtool.util.common import get_as_hex_string, get_cmac, hex_xor
from helper.common import PLAINTEXT_KEY


@pytest.mark.parametrize(
    "number,expected",
    [(1, "01"), (10, "0A"), (16, "10")],
)
def test_should_get_an_int_as_a_hex_string(number: int, expected: str):
    hex_string = get_as_hex_string(number)
    assert_that(hex_string, equal_to(expected))


@pytest.mark.parametrize(
    "first,second,expected", [("1111", "0000", 4369), ("1101", "0101", 4096)]
)
def test_hex_xor_should_perform_xor_successfully(
    first: str, second: str, expected: int
):
    result = hex_xor(first, second)
    assert_that(result, equal_to(expected))


@pytest.mark.parametrize(
    "data,key,expected",
    [
        ("1111", PLAINTEXT_KEY, "D8559813F0D39246"),
        ("1101", PLAINTEXT_KEY, "F35AE56BAF0736BC"),
    ],
)
def test_get_cmac_should_get_cmac_successfully(data: str, key: str, expected: str):
    result = get_cmac(data, key)
    assert_that(result, equal_to(expected))
