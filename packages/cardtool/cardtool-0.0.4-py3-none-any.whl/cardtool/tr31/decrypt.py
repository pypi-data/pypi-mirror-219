import codecs
from abc import ABC, abstractmethod
from typing import Callable, Tuple

from Crypto.Cipher import DES3
from loguru import logger

from cardtool.tr31.key_block import KeyBlock, TR31Parse, TR31Parser, TR31Version
from cardtool.util.common import get_as_hex_string, get_cmac, hex_xor

KBEKAVariant = "45" * 16
KBMKAVariant = "4D" * 16

KBEKComponent1 = "0100000000000080"
KBEKComponent2 = "0200000000000080"

KBMKComponent1 = "0100010000000080"
KBMKComponent2 = "0200010000000080"


class TR31Decryption(ABC):
    @abstractmethod
    def decrypt(self, kbpk: str, kcv: str, block: str) -> str:  # pragma: no cover
        pass


class TR31Decrypt(TR31Decryption):
    def __init__(self, parser: TR31Parse):
        self.__parser_ = parser

    def decrypt(self, kbpk: str, kcv: str, block: str) -> str:
        try:
            key_block = self.__parser_.parse_key_block(block)

            if key_block.version == TR31Version.A:
                return self.__decrypt_(kbpk, kcv, key_block, self.__decrypt_A_)

            if key_block.version == TR31Version.B:
                return self.__decrypt_(kbpk, kcv, key_block, self.__decrypt_B_)

            raise Exception("unknown key block version")
        except Exception as e:
            logger.error(e)
            raise NotImplementedError(
                f"key decryption not implemented for {block}"
            ) from e

    def __decrypt_(
        self,
        kbpk: str,
        kcv: str,
        block: KeyBlock,
        decrypt_fn: Callable[[str, KeyBlock], str],
    ):
        plain_key_data = decrypt_fn(kbpk, block)
        key_data = self.__parser_.parse_key_data(plain_key_data)
        self.__check_kcv_(kcv, key_data.key)

        return key_data.key.upper()

    def __decrypt_A_(self, kbpk: str, block: KeyBlock) -> str:
        kbek = hex_xor(kbpk, KBEKAVariant)
        header = [
            block.version.value,
            block.hex_length,
            block.key_usage,
            block.algorithm,
        ]
        kbek_iv = bytes.fromhex(codecs.encode("".join(header), "ascii").hex())
        decrypt = DES3.new(
            bytes.fromhex(get_as_hex_string(kbek)), DES3.MODE_CBC, IV=kbek_iv
        )

        plain_key_data = decrypt.decrypt(bytes.fromhex(block.key_data))

        return plain_key_data.hex()

    def __decrypt_B_(self, kbpk: str, block: KeyBlock) -> str:
        kbek, _ = self.__get_version_b_keys(kbpk)
        decrypt = DES3.new(
            bytes.fromhex(kbek),
            mode=DES3.MODE_CBC,
            IV=bytes.fromhex(block.authenticator),
        )
        plain_key_data = decrypt.decrypt(bytes.fromhex(block.key_data))
        return plain_key_data.hex()

    def __get_version_b_keys(self, kbpk: str) -> Tuple[str, str]:
        kbek1 = get_cmac(KBEKComponent1, kbpk)
        kbek2 = get_cmac(KBEKComponent2, kbpk)
        kbek = kbek1 + kbek2

        kbmk1 = get_cmac(KBMKComponent1, kbpk)
        kbmk2 = get_cmac(KBMKComponent2, kbpk)
        kbmk = kbmk1 + kbmk2

        return (kbek, kbmk)

    def __check_kcv_(self, kcv: str, key: str):
        encrypt = DES3.new(
            bytes.fromhex(key), mode=DES3.MODE_CBC, IV=bytes.fromhex("0" * 16)
        )

        clear_kvc = encrypt.encrypt(bytes.fromhex("0" * 16))
        clear_hex_kcv = clear_kvc.hex().upper()[:6]
        if clear_hex_kcv.casefold() != kcv.casefold():
            raise Exception("could not find clear text key, kcv does not match")


def new(parser: TR31Parse = TR31Parser()) -> TR31Decrypt:
    return TR31Decrypt(parser)
