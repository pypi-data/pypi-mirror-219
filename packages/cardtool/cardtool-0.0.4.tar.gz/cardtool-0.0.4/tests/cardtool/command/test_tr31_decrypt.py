from unittest.mock import MagicMock, Mock

import pytest
from click.testing import CliRunner
from hamcrest import assert_that, contains_string, equal_to

from cardtool.command.tr31_decrypt import decrypt_tr31
from cardtool.tr31.decrypt import TR31Decryption
from helper.common import (
    FAILURE_EXIT_CODE,
    KCV,
    PARAM_FAILURE_EXIT_CODE,
    PLAINTEXT_KEY,
    PLAINTEXT_ZMK,
    SUCCESS_EXIT_CODE,
    TR31_VERSION_A_KEY_BLOCK,
    TR31_VERSION_B_KEY_BLOCK,
)

testdata = [
    (
        PLAINTEXT_ZMK,
        KCV,
        TR31_VERSION_A_KEY_BLOCK,  # noqa: E501
    ),
    (
        PLAINTEXT_ZMK,
        KCV,
        TR31_VERSION_B_KEY_BLOCK,  # noqa: E501
    ),
]

test_ids = ["Version A", "Version B"]


class TestDecryptTR31:
    @pytest.mark.parametrize("kbpk,kcv,kblock", testdata, ids=test_ids)
    def test_should_decrypt_a_tr31_key_block_successfully(self, kbpk, kcv, kblock):
        runner = CliRunner()
        tr31_decrypt = MagicMock(spec=TR31Decryption)
        cmd = decrypt_tr31(tr31_decrypt)

        tr31_decrypt.decrypt.return_value = PLAINTEXT_KEY
        output = runner.invoke(cmd, ["--kbpk", kbpk, "--kcv", kcv, kblock])
        tr31_decrypt.decrypt.assert_called_with(kbpk, kcv, kblock)
        assert_that(output.output, equal_to(f"Plaintext Key: {PLAINTEXT_KEY}\n"))
        assert_that(output.exit_code, equal_to(SUCCESS_EXIT_CODE))

    @pytest.mark.parametrize(
        "kbpk,kcv,kblock,error",
        [
            (
                "fake",
                KCV,
                TR31_VERSION_A_KEY_BLOCK,
                "Invalid value for '--kbpk' / '-kbpk': fake does not conform with required pattern [A-F0-9]{32}",  # noqa: E501
            ),
            (
                PLAINTEXT_ZMK,
                "fake",
                TR31_VERSION_A_KEY_BLOCK,
                "Invalid value for '--kcv' / '-kcv': fake does not conform with required pattern [A-F0-9]{6}",  # noqa: E501
            ),
            (
                PLAINTEXT_ZMK,
                KCV,
                "fake",
                "Invalid value for 'KBLOCK': fake does not conform with required pattern [A-Z0-9]{72,80}",  # noqa: E501
            ),
        ],
        ids=["kbpk", "kcv", "kblock"],
    )
    def test_should_raise_an_error_when_it_receives_a_bad_parameter(
        self, kbpk, kcv, kblock, error
    ):
        runner = CliRunner()
        tr31_decrypt = Mock(spec=TR31Decryption)
        cmd = decrypt_tr31(tr31_decrypt)
        tr31_decrypt.decrypt = MagicMock(side_effect=Exception("error"))
        output = runner.invoke(cmd, ["--kbpk", kbpk, "--kcv", kcv, kblock])

        tr31_decrypt.decrypt.assert_not_called()
        assert_that(output.exit_code, equal_to(PARAM_FAILURE_EXIT_CODE))
        assert_that(output.output, contains_string(error))

    def test_should_log_an_error_when_it_decryption_raises_an_exception(self):
        runner = CliRunner()
        tr31_decrypt = Mock(spec=TR31Decryption)
        cmd = decrypt_tr31(tr31_decrypt)
        tr31_decrypt.decrypt = MagicMock(side_effect=Exception("failure"))
        output = runner.invoke(
            cmd, ["--kbpk", PLAINTEXT_ZMK, "--kcv", KCV, TR31_VERSION_B_KEY_BLOCK]
        )
        tr31_decrypt.decrypt.assert_called_with(
            PLAINTEXT_ZMK, KCV, TR31_VERSION_B_KEY_BLOCK
        )
        assert_that(output.exit_code, equal_to(FAILURE_EXIT_CODE))
        assert_that(output.output, contains_string("failure"))
