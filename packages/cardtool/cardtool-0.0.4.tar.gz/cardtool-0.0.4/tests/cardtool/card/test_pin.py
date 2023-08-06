import pytest
from hamcrest import assert_that, equal_to

from cardtool.card.pin import generate_pin_block


@pytest.mark.parametrize(
    "pan,pin,expected",
    [
        ("5516422217375116", "1234", "041250DDDE8C8AEE"),
        ("4516422217375116", "123456", "06125074DE8C8AEE"),
    ],
    ids=["with four digit pin", "with six digit pin"],
)
def test_generate_pin_block_successfully_when_called_(pan, pin, expected):
    pin_block = generate_pin_block(pan, pin)
    assert_that(pin_block, equal_to(expected))
