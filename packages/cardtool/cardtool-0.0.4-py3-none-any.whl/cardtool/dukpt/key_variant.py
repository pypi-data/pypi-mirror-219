from enum import Enum


class KeyVariant(Enum):
    """
    KeyMask mask types for key derivation.
    """

    DataKey = 0x0000000000FF00000000000000FF0000
    PinKey = 0x00000000000000FF00000000000000FF
    MacKey = 0x000000000000FF00000000000000FF00
