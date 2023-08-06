from abc import ABC, abstractmethod
from functools import cache
from typing import Callable

from Crypto.Cipher import DES3

from cardtool.dukpt.key_type import KeyType


class Cipher(ABC):
    @abstractmethod
    def encrypt(self, data: str, key: KeyType) -> str:  # pragma: no cover
        pass

    @abstractmethod
    def decrypt(self, data: str, key: KeyType) -> str:  # pragma: no cover
        pass


class DUKPTCipher(Cipher):
    def __init__(
        self, bdk: str, ksn: str, derive_key: Callable[[str, str, KeyType], str]
    ):
        self.__derive_key_ = derive_key
        self.__bdk_ = bdk
        self.__ksn_ = ksn

    def encrypt(self, data: str, key: KeyType) -> str:
        key = self.__get_key_(key)

        encrypt = DES3.new(
            bytes.fromhex(key), DES3.MODE_CBC, IV=bytes.fromhex("0" * 16)
        )
        raw_data = bytes.fromhex(data)
        data_to_encrypt = (
            raw_data
            if (len(raw_data) % 8 == 0)
            else DUKPTCipher.__append_bytes_(raw_data, 8 - (len(raw_data) % 8))
        )

        encrypted = encrypt.encrypt(data_to_encrypt)

        return encrypted.hex().upper()

    def decrypt(self, data: str, key: KeyType) -> str:
        key = self.__get_key_(key)

        decrypt = DES3.new(
            bytes.fromhex(key), DES3.MODE_CBC, IV=bytes.fromhex("0" * 16)
        )

        encrypted = decrypt.decrypt(bytes.fromhex(data))

        return encrypted.hex().upper()

    @staticmethod
    def __append_bytes_(data: bytes, n: int) -> bytes:
        bt = bytearray(data)
        [bt.append(0x00) for _ in range(n)]
        return bytes(bt)

    @cache
    def __get_key_(self, key_type: KeyType) -> str:
        key = self.__derive_key_(self.__bdk_, self.__ksn_, key_type)
        return key
