from unittest.mock import Mock

import pytest
from hamcrest import assert_that, equal_to

from cardtool.dukpt.cipher import DUKPTCipher
from cardtool.dukpt.key_type import KeyType
from helper.common import KSN, PLAINTEXT_KEY


class TestDUKPTCipher:
    @pytest.mark.parametrize(
        "data,expected",
        [
            ("F" * 16, "1BFC569203335B41"),
            ("F" * 18, "1BFC569203335B4156FA8D87902CF18F"),
        ],
        ids=["called with complete data", "called with data to be padded"],
    )
    def test_cipher_should_encrypt_data_successfully_when_(
        self, data: str, expected: str
    ):
        derive_key = Mock()
        derive_key.return_value = "CA7091701C616F92697955B77E723D27"
        cipher = DUKPTCipher(PLAINTEXT_KEY, KSN, derive_key)
        encrypted = cipher.encrypt(data, KeyType.DATA)

        derive_key.assert_called_with(PLAINTEXT_KEY, KSN, KeyType.DATA)
        assert_that(encrypted, equal_to(expected))

    @pytest.mark.parametrize(
        "data,expected",
        [
            ("1BFC569203335B41", "F" * 16),
            ("1BFC569203335B4156FA8D87902CF18F", "{0}{1}".format("F" * 18, "0" * 14)),
        ],
        ids=["called with data without padding", "called with padded ciphertext"],
    )
    def test_cipher_should_decrypt_data_successfully_when_called(
        self, data: str, expected: str
    ):
        derive_key = Mock()
        derive_key.return_value = "CA7091701C616F92697955B77E723D27"
        cipher = DUKPTCipher(PLAINTEXT_KEY, KSN, derive_key)
        plaintext = cipher.decrypt(data, KeyType.DATA)

        derive_key.assert_called_with(PLAINTEXT_KEY, KSN, KeyType.DATA)
        assert_that(plaintext, equal_to(expected))

    def test_cipher_should_memoize_key_generation_when_decryption_is_called_n_times(
        self,
    ):
        derive_key = Mock()
        derive_key.return_value = "CA7091701C616F92697955B77E723D27"
        data = "1BFC569203335B41"
        expected = "F" * 16
        cipher = DUKPTCipher(PLAINTEXT_KEY, KSN, derive_key)
        plaintext = ""
        for i in range(0, 5):
            plaintext = cipher.decrypt(data, KeyType.DATA)

        derive_key.assert_called_once_with(PLAINTEXT_KEY, KSN, KeyType.DATA)
        assert_that(plaintext, equal_to(expected))

    def test_cipher_should_memoize_key_generation_when_encryption_is_called_n_times(
        self,
    ):
        derive_key = Mock()
        derive_key.return_value = "CA7091701C616F92697955B77E723D27"
        expected = "1BFC569203335B41"
        data = "F" * 16
        cipher = DUKPTCipher(PLAINTEXT_KEY, KSN, derive_key)
        encrypted_text = ""
        for i in range(0, 5):
            encrypted_text = cipher.encrypt(data, KeyType.DATA)

        derive_key.assert_called_once_with(PLAINTEXT_KEY, KSN, KeyType.DATA)
        assert_that(encrypted_text, equal_to(expected))
