import sys

from Crypto.Cipher import DES, DES3

from cardtool.dukpt.key_type import KeyType
from cardtool.dukpt.key_variant import KeyVariant
from cardtool.util.common import get_as_hex_string
from cardtool.util.model import Endianness

KeyMask = 0xC0C0C0C000000000C0C0C0C000000000
KsnMask = 0xFFFFFFFFFFFFFFE00000


def generate_key(
    bdk: str,
    ksn: str,
    key_type: KeyType,
    endianness: sys.byteorder = Endianness.Big.value,
) -> str:
    ikey = create_ipek(bdk, ksn, endianness)
    session_key = __derive_key_(ikey, ksn, endianness)

    if key_type == KeyType.SESSION:
        return get_as_hex_string(session_key)
    if key_type == KeyType.IKEY:
        return get_as_hex_string(ikey)
    if key_type == KeyType.PIN:
        return get_as_hex_string(session_key ^ KeyVariant.PinKey.value)
    if key_type == KeyType.MAC:
        return get_as_hex_string(session_key ^ KeyVariant.MacKey.value)
    if key_type == KeyType.DATA:
        data_key = __get_data_key_(session_key ^ KeyVariant.DataKey.value, endianness)
        return get_as_hex_string(data_key)

    raise Exception("unknown key variant")


def __get_data_key_(key: int, byteorder=sys.byteorder) -> int:
    ede3_key = __get_ede3_key_(get_as_hex_string(key))
    top8 = (key & 0xFFFFFFFFFFFFFFFF0000000000000000) >> 64
    bottom8 = key & 0xFFFFFFFFFFFFFFFF

    first_enc = DES3.new(
        bytes.fromhex(ede3_key),
        mode=DES3.MODE_CBC,
        IV=bytes.fromhex("0000000000000000"),
    )
    second_enc = DES3.new(
        bytes.fromhex(ede3_key),
        mode=DES3.MODE_CBC,
        IV=bytes.fromhex("0000000000000000"),
    )
    first_half = (
        int.from_bytes(
            first_enc.encrypt(bytes.fromhex(get_as_hex_string(top8))),
            byteorder=byteorder,
        )
        << 64
    )
    second_half = int.from_bytes(
        second_enc.encrypt(bytes.fromhex(get_as_hex_string(bottom8))),
        byteorder=byteorder,
    )

    return first_half | second_half


def __derive_key_(ikey: int, ksn: str, byteorder=sys.byteorder):
    original_ksn = int.from_bytes(bytes.fromhex(ksn), byteorder)

    ksn_right8_bytes = (
        int.from_bytes(bytes.fromhex(ksn), byteorder) & 0xFFFFFFFFFFFFFFFF
    )
    base_ksn = ksn_right8_bytes & 0xFFFFFFFFFFE00000

    counter = original_ksn & 0x1FFFFF
    cur_key = ikey
    shift_reg = 0x100000

    while shift_reg > 0:
        if (shift_reg & counter) > 0:
            base_ksn |= shift_reg
            cur_key = __generate_key_(cur_key, base_ksn, byteorder)
        shift_reg >>= 1
    return cur_key


def create_ipek(bdk: str, ksn: str, byteorder=sys.byteorder) -> int:
    ede3_bkd = __get_ede3_key_(bdk)

    masked_ksn = int.from_bytes(bytes.fromhex(ksn), byteorder) & KsnMask
    ksn_top8 = get_as_hex_string(masked_ksn >> 16)
    ksn_top8_bytes = bytes.fromhex(ksn_top8)

    first_key = bytes.fromhex(ede3_bkd)
    ede3_second_key = __get_ede3_key_(
        get_as_hex_string(int.from_bytes(bytes.fromhex(bdk), byteorder) ^ KeyMask)
    )
    second_key = bytes.fromhex(ede3_second_key)

    first_decrypt = DES3.new(
        first_key, mode=DES3.MODE_CBC, IV=bytes.fromhex("0000000000000000")
    )
    first_half = int.from_bytes(first_decrypt.encrypt(ksn_top8_bytes), byteorder) << 64

    second_decrypt = DES3.new(
        second_key, mode=DES3.MODE_CBC, IV=bytes.fromhex("0000000000000000")
    )
    second_half = int.from_bytes(second_decrypt.encrypt(ksn_top8_bytes), byteorder)

    return first_half | second_half


def __generate_key_(key: int, ksn: int, byteorder=sys.byteorder):
    return __encrypt_register_(
        key ^ KeyMask, ksn, byteorder
    ) << 64 | __encrypt_register_(key, ksn, byteorder)


def __encrypt_register_(key: int, ksn: int, byteorder=sys.byteorder):
    bottom8 = key & 0xFFFFFFFFFFFFFFFF
    top8 = (key & 0xFFFFFFFFFFFFFFFF0000000000000000) >> 64
    enc_key = top8.to_bytes(8, byteorder, signed=False)

    data_to_encrypt = bytes.fromhex(get_as_hex_string(bottom8 ^ ksn))
    encryptor = DES.new(enc_key, DES.MODE_CBC, IV=bytes.fromhex("0000000000000000"))
    encrypted_data = int.from_bytes(encryptor.encrypt(data_to_encrypt), byteorder)
    return bottom8 ^ encrypted_data


def __get_ede3_key_(raw_bdk):
    # DUKPT is designed to use double-length keys only.
    return raw_bdk + raw_bdk[:16]
