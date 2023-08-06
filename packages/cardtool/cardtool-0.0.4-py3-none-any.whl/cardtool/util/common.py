from Crypto.Cipher import DES3
from Crypto.Hash import CMAC

from cardtool.util.model import Endianness


def get_as_hex_string(number: int) -> str:
    new_hex_number = hex(number).lstrip("0x")
    if len(new_hex_number) % 2 != 0:
        new_hex_number = "0" + new_hex_number
    return new_hex_number.upper()


def hex_xor(first: str, second: str, endianness: Endianness = Endianness.Big) -> int:
    first_int = int.from_bytes(bytes.fromhex(first), endianness.value)
    second_int = int.from_bytes(bytes.fromhex(second), endianness.value)
    return first_int ^ second_int


def get_cmac(data: str, key: str) -> str:
    cmac = CMAC.new(bytes.fromhex(key), ciphermod=DES3)
    cmac.update(bytes.fromhex(data))
    return cmac.digest().hex().upper()
