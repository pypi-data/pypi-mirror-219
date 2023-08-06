from unittest.mock import MagicMock, Mock, call, mock_open, patch

from hamcrest import assert_that, same_instance

from cardtool.card.dump import CardDumper
from cardtool.card.model import Card, CardConfig, CardReadingData
from cardtool.util.serialize import Serializer


class TestDump:
    def serializer_side_effect(self, *args, **_):
        (card_dump, *_) = args
        list(card_dump)

    def test_dump_cards_should_generate_cards_successfully_when_called(self):
        m = mock_open()
        with patch("cardtool.card.dump.open", m):
            gen_cards = [
                CardReadingData("tlv", "track1", "track2", "pin_block1"),
                CardReadingData("tlv", "track1", "track2", "pin_block2"),
            ]
            card_config = CardConfig(
                cards=[
                    Card(
                        "pan",
                        "pin",
                        "brand",
                        "cardholder_name",
                        "expiry_month",
                        "expiry_year",
                        "service_code",
                        1,
                    ),
                    Card(
                        "pan",
                        "pin",
                        "brand",
                        "cardholder_name",
                        "expiry_month",
                        "expiry_year",
                        "service_code",
                        2,
                    ),
                ]
            )

            cipher = Mock(return_value="encrypt")
            generator = Mock(side_effect=gen_cards)
            serializer = MagicMock(
                spec=Serializer, side_effect=self.serializer_side_effect
            )
            serializer.serialize.side_effect = self.serializer_side_effect
            file = "test.test"
            gen_calls = [call(card) for card in card_config.cards]
            cipher_calls = [call(gen_card) for gen_card in gen_cards]

            dm = CardDumper(cipher=cipher, serializer=serializer, generator=generator)
            dm.dump_cards(file, card_config)

            generator.assert_has_calls(gen_calls, any_order=True)
            cipher.assert_has_calls(cipher_calls)
            (mapper, stream) = serializer.serialize.call_args[0]
            m.assert_called_once_with(file, mode="w", encoding="utf-8")
            assert_that(isinstance(mapper, map))
            assert_that(stream, same_instance(m.return_value))
