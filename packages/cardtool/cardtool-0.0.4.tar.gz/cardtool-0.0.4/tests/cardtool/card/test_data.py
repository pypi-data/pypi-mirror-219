from unittest.mock import Mock

import pytest
from hamcrest import assert_that, equal_to

from cardtool.card.data import CardGen
from cardtool.card.model import Brand, Card, CardReadingData, Terminal, Transaction

TLV_DATA = {
    0: "9F02060000000011349F03060000000012209F2701809C01009F330360F8C89F10120310A04001240000000000000000000000FF820239009F0607A00000000410109F360200019F260867867D992FEC13D49A032201259F1A0204845F2A020484950500000080009F37044A37ADDF8407A00000000410105F3401015F2004546573749F6E07021800003030009F34031E030057125516422217375116D25012011234000012305A0855164222173751169F5B0512345678909F090200019F350122",  # noqa: E501
    1: "9F02060000000011359F03060000000012109F2701809C01319F330360F8C89F10120310A04001240000000000000000000000FF820239009F0607A00000000310109F3602000C9F260867867D992FEC13D49A032201289F1A0204845F2A020484950500000080009F37044A37ADDF8407A00000000310105F3401025F20095465737420566973619F6E07021800003030009F34031E030057124516422217375116D28022031234000012305A0845164222173751169F5B0512345678909F090200019F350122",  # noqa: E501
    2: "9F02060000000011359F03060000000012109F2701809C01209F330360F8C89F10120310A04001240000000000000000000000FF820239009F0607A00000000410109F3602000E9F260867867D992FEC13D49A032201289F1A0200325F2A020032950500000080009F37044A37ADDF8407A00000000410105F3401045F200B54657374204361726E65749F6E07021800003030009F34031E030057125316422217375116D28022031234000012305A0853164222173751169F5B0512345678909F090200019F350122",  # noqa: E501
}

PIN_BLOCK = "041250DDDE8C8AEE"


class TestGenerator:
    @pytest.mark.parametrize(
        "terminal,transaction,card,expected_data",
        [
            (
                Terminal(country="MEX"),
                Transaction(
                    currency="MXN",
                    other_amount=12.20,
                    amount=11.34,
                    date="220125",
                    type="charge",
                ),
                Card(
                    brand=Brand.MASTERCARD.value,
                    pan="5516422217375116",
                    pin="1234",
                    cardholder_name="Test",
                    expiry_year="25",
                    expiry_month="01",
                    service_code="201",
                    sequence_number=1,
                    label="MC",
                ),
                CardReadingData(
                    TLV_DATA[0],
                    "42353531363432323231373337353131365e54657374202020202020202020202020202020202020202020205e323530313230313132333430303030313233302020",  # noqa: E501
                    "5516422217375116D2501201123400001230",
                    PIN_BLOCK,
                    "MC",
                ),
            ),
            (
                Terminal(country="FAKE"),
                Transaction(
                    currency="FAKE",
                    other_amount=12.10,
                    amount=11.35,
                    counter=12,
                    date="220128",
                    type="balance",
                ),
                Card(
                    brand=Brand.VISA.value,
                    pan="4516422217375116",
                    pin="123456",
                    cardholder_name="Test Visa",
                    expiry_year="28",
                    expiry_month="02",
                    service_code="203",
                    sequence_number=2,
                    label="Visa test",
                ),
                CardReadingData(
                    TLV_DATA[1],
                    "42343531363432323231373337353131365e54657374205669736120202020202020202020202020202020205e323830323230333132333430303030313233302020",  # noqa: E501
                    "4516422217375116D2802203123400001230",
                    PIN_BLOCK,
                    "Visa test",
                ),
            ),
            (
                Terminal(country="ARG"),
                Transaction(
                    currency="ARS",
                    other_amount=12.10,
                    amount=11.35,
                    counter=14,
                    date="220128",
                    type="credit voucher",
                ),
                Card(
                    brand=Brand.CARNET.value,
                    pan="5316422217375116",
                    pin="123456",
                    cardholder_name="Test Carnet",
                    expiry_year="28",
                    expiry_month="02",
                    service_code="203",
                    sequence_number=4,
                    label="",
                ),
                CardReadingData(
                    TLV_DATA[2],
                    "42353331363432323231373337353131365e54657374204361726e65742020202020202020202020202020205e323830323230333132333430303030313233302020",  # noqa: E501
                    "5316422217375116D2802203123400001230",
                    PIN_BLOCK,
                ),
            ),
        ],
        ids=[
            "with MC card brand",
            "with Visa and unknown currency/country values",
            "with Carnet brand",
        ],
    )
    def test_generate_data_successfully_when_called_(
        self,
        terminal: Terminal,
        transaction: Transaction,
        card: Card,
        expected_data: CardReadingData,
    ):
        pin_gen = Mock()
        pin_gen.return_value = PIN_BLOCK
        gen = CardGen(pin_gen)
        card_reading_data = gen.generate_data(terminal, transaction, card)
        assert_that(card_reading_data, equal_to(expected_data))
        pin_gen.assert_called_once_with(card.pan, card.pin)
