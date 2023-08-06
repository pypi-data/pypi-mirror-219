from abc import ABC, abstractmethod
from typing import Callable, Iterable, TypeVar

from toolz import compose

from cardtool.card.model import Card, CardConfig, CardReadingData
from cardtool.util.serialize import Serializer

T = TypeVar("T")
S = TypeVar("S")
C = Callable[[T], S]
Mapper = Callable[[C, Iterable[T]], Iterable[S]]


class Dumper(ABC):
    @abstractmethod
    def dump_cards(
        self, out_filepath: str, card_config: CardConfig, mapper: Mapper
    ):  # pragma: nocover
        pass


class CardDumper(Dumper):
    def __init__(
        self,
        cipher: Callable[[CardReadingData], CardReadingData],
        generator: Callable[[Card], CardReadingData],
        serializer: Serializer,
    ):
        self.__cipher_ = cipher
        self.__generator_ = generator
        self.__serializer_ = serializer

    def dump_cards(
        self, out_filepath: str, card_config: CardConfig, mapper: Mapper = map
    ):
        cards = card_config.cards
        pipeline = compose(self.__cipher_, self.__generator_)
        with open(out_filepath, mode="w", encoding="utf-8") as out_file:
            cards_dump = mapper(pipeline, cards)
            self.__serializer_.serialize(cards_dump, out_file)
