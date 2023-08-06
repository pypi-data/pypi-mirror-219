from enum import Enum


class KeyType(Enum):
    IKEY = 0
    SESSION = 1
    DATA = 2
    MAC = 3
    PIN = 4
    UNKNOWN = 5
