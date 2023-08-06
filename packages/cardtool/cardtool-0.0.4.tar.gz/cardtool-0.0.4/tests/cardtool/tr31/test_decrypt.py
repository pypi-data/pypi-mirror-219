from unittest.mock import Mock

import pytest
from hamcrest import assert_that, equal_to

import cardtool.tr31.decrypt as tr31
from cardtool.tr31.key_block import KeyBlock, TR31Parse, TR31Version
from helper.common import (
    PLAINTEXT_KEY,
    TR31_VERSION_A_KEY_BLOCK,
    TR31_VERSION_B_KEY_BLOCK,
)

testdata = [
    (
        "EFE0853B256B583D868F251CE99EA1D9",
        "08D7B4",
        TR31_VERSION_A_KEY_BLOCK,  # noqa: E501
    ),
    ("EFE0853B256B583D868F251CE99EA1D9", "08D7B4", TR31_VERSION_B_KEY_BLOCK),
]
test_raise_data = map(lambda data: (data[0], "FF00FF", data[2]), testdata)

test_ids = ["Version A", "Version B"]


class TestDecrypt:
    @pytest.mark.parametrize("kbpk,kcv,block", testdata, ids=test_ids)
    def test_decrypt_key_block_successfully(self, kbpk: str, kcv: str, block: str):
        tr31_decrypt = tr31.new()
        plaintext_key = tr31_decrypt.decrypt(kbpk, kcv, block)
        assert_that(plaintext_key, equal_to(PLAINTEXT_KEY))

    @pytest.mark.parametrize("kbpk,kcv,block", test_raise_data, ids=test_ids)
    def test_decrypt_should_raise_exception_when_key_is_not_found(
        self, kbpk: str, kcv: str, block: str
    ):
        with pytest.raises(
            Exception, match=f"key decryption not implemented for {block}"
        ):
            tr31_decrypt = tr31.new()
            _ = tr31_decrypt.decrypt(kbpk, kcv, block)

    def test_decrypt_should_raise_exception_when_key_decryption_is_unknown(self):
        parser = Mock(spec=TR31Parse)
        with pytest.raises(Exception, match="key decryption not implemented for C"):
            parser.parse_key_block.return_value = KeyBlock(
                TR31Version.C, "", 1, "", "", "", "", "", "", "", "", ""
            )
            tr31_decrypt = tr31.new(parser)
            _ = tr31_decrypt.decrypt("kbpk", "kcv", "C")

        parser.parse_key_block.assert_called_with("C")
