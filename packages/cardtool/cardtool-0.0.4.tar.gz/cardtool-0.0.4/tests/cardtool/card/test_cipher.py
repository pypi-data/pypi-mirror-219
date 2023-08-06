from dataclasses import asdict
from unittest.mock import Mock, call

from hamcrest import assert_that, equal_to

from cardtool.card.cipher import encrypt_card
from cardtool.card.model import CardReadingData
from cardtool.dukpt.cipher import Cipher
from cardtool.dukpt.key_type import KeyType


def test_should_cipher_card_data_successfully_when_called():
    cipher = Mock(spec=Cipher)
    cipher.encrypt.return_value = "encrypt"
    card_data = CardReadingData("tlv", "track1", "track2", "pin", "test")
    encrypted_data = encrypt_card(cipher, card_data)
    expected_data = CardReadingData("encrypt", "encrypt", "encrypt", "encrypt", "test")

    keys = [KeyType.DATA, KeyType.DATA, KeyType.DATA, KeyType.PIN]
    data_values = asdict(card_data).values()

    cipher.encrypt.assert_has_calls(
        [call(data, key) for data, key in zip(data_values, keys)]
    )
    assert_that(encrypted_data, equal_to(expected_data))
