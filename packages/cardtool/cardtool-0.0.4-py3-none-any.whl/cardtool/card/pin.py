from cardtool.util.common import get_as_hex_string
from cardtool.util.model import Endianness


def generate_pin_block(
    pan: str, pin: str, endianness: Endianness = Endianness.Big
) -> str:
    pin_part = f"0{len(pin)}{pin}{'F'*(16-len(pin)-2)}"
    card_part = f"0000{pan[3:len(pan) - 1]}"

    byte_pin_part = int.from_bytes(bytes.fromhex(pin_part), byteorder=endianness.value)
    byte_card_part = int.from_bytes(
        bytes.fromhex(card_part), byteorder=endianness.value
    )
    xor_pin = byte_pin_part ^ byte_card_part
    return get_as_hex_string(xor_pin)
