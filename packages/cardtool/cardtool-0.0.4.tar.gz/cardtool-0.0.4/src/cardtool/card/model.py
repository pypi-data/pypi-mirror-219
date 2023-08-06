from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Type

import yaml


@dataclass(frozen=True)
class CardReadingData(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = "!CardData"
    tlv: str = ""
    track1: str = ""
    track2: str = ""
    pin_block: str = ""
    label: str = ""


@dataclass(frozen=True)
class Card(yaml.YAMLObject):  # pragma: no cover
    yaml_tag = "!Card"
    yaml_loader = yaml.SafeLoader
    pan: str
    pin: str
    brand: str
    cardholder_name: str
    expiry_month: str
    expiry_year: str
    service_code: str
    sequence_number: int
    label: str = uuid.uuid4().hex


@dataclass(frozen=True)
class Terminal(yaml.YAMLObject):  # pragma: no cover
    yaml_tag = "!Terminal"
    yaml_loader = yaml.SafeLoader
    country: str = ""


@dataclass(frozen=True)
class Transaction(yaml.YAMLObject):  # pragma: no cover
    yaml_tag = "!Transaction"
    yaml_loader = yaml.SafeLoader
    type: str = ""
    amount: float = 0.0
    other_amount: float = 0.0
    currency: str = ""
    date: str = ""
    counter: int = 0


@dataclass(frozen=True)
class Key(yaml.YAMLObject):  # pragma: no cover
    yaml_tag = "!Key"
    yaml_loader = yaml.SafeLoader
    bdk: str = ""
    ksn: str = ""


@dataclass(frozen=True)
class CardConfig(yaml.YAMLObject):  # pragma: no cover
    yaml_tag = "!CardConfig"
    yaml_loader = yaml.SafeLoader
    version: str = "0.0.1"
    transaction: Transaction = field(default=Transaction())
    key: dict[str, Key] = field(default_factory=dict)
    terminal: Terminal = Terminal()
    cards: list[Card] = field(default_factory=list)

    @staticmethod
    def empty(cls: Type[CardConfig]):
        return cls()


class Brand(Enum):
    MASTERCARD = "Mastercard"
    VISA = "Visa"
    CARNET = "Carnet"
