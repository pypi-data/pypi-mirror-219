import pytest
from hamcrest import assert_that, equal_to

from cardtool.tr31.key_block import KeyBlock, KeyData, TR31Parser, TR31Version
from helper.common import (
    PLAINTEXT_KEY_DATA,
    TR31_VERSION_A_KEY_BLOCK,
    TR31_VERSION_B_KEY_BLOCK,
)

testdata = [
    (TR31Version.A, TR31_VERSION_A_KEY_BLOCK),
    (TR31Version.B, TR31_VERSION_B_KEY_BLOCK),
]

test_result = {
    TR31Version.A: KeyBlock(
        TR31Version.A,
        "0072",
        114,
        "B0",
        "T",
        "N",
        "00",
        "N",
        "00",
        "00",
        "7B2782C0DB0AFAA96F8C67EF76CD6FBD1DC71685FCFA09B5",
        "764076C0",
    ),
    TR31Version.B: KeyBlock(
        TR31Version.B,
        "0080",
        128,
        "B0",
        "T",
        "N",
        "00",
        "N",
        "00",
        "00",
        "302AE1EF9E3BAAEF3446D9580D2F505485BCE347BCD3810B",
        "E13678DE57D97A96",
    ),
}

ids = ["Version A", "Version B"]


class TestKeyBlock:
    @pytest.mark.parametrize("version,key_block", testdata, ids=ids)
    def test_should_parse_key_block_successfully(self, version, key_block):
        parser = TR31Parser()
        parsed = parser.parse_key_block(key_block)
        expected_block = test_result.get(version)
        assert_that(parsed, equal_to(expected_block))

    def test_should_parse_key_data_successfully(
        self,
    ):
        parser = TR31Parser()
        key_data = parser.parse_key_data(PLAINTEXT_KEY_DATA)
        expected_key_data = KeyData(
            128, "0080", "0123456789abcdeffedcba9876543210", "4296910ad287"
        )
        assert_that(key_data, equal_to(expected_key_data))

    def test_should_raise_not_implemented_error_when_it_receives_an_unknown_version(
        self,
    ):
        with pytest.raises(NotImplementedError, match="unknown key block version T"):
            parser = TR31Parser()
            _ = parser.parse_key_block("T0")
