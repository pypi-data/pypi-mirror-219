from abc import ABC, abstractmethod
from typing import Callable, List, Tuple

import pydash.objects
from ber_tlv.tlv import Tlv
from pycountry import countries, currencies

from cardtool.card.model import Card, CardReadingData, Terminal, Transaction
from cardtool.card.tags import TlvTag
from cardtool.util.common import get_as_hex_string

TlvData = Tuple[int, bytes]


class Generator(ABC):
    @abstractmethod
    def generate_data(
        self, terminal: Terminal, transaction: Transaction, card: Card
    ) -> CardReadingData:  # pragma: nocover
        pass


class CardGen(Generator):
    def __init__(self, pin_generator: Callable[[str, str], str]):
        self.__pin_generator_ = pin_generator

    def generate_data(
        self, terminal: Terminal, transaction: Transaction, card: Card
    ) -> CardReadingData:
        pin_block = self.__pin_generator_(card.pan, card.pin)
        tlv = self.__generate_tlv_(terminal, transaction, card)
        track1 = self.__generate_track1(card)
        track2 = self.__generate_track2(card)

        return CardReadingData(tlv, track1, track2, pin_block, card.label)

    def __generate_tlv_(
        self, terminal: Terminal, transaction: Transaction, card: Card
    ) -> str:
        card_tlv: List[TlvData] = []
        amount = "{0}".format(round(transaction.amount * 100)).rjust(12, "0")
        other_amount = "{0}".format(round(transaction.other_amount * 100)).rjust(
            12, "0"
        )
        tx_type = self.__get_transaction_type_(transaction.type)
        aid = CardGen.__get_aid_(card.brand)
        tx_counter = get_as_hex_string(
            1 if transaction.counter == 0 else transaction.counter
        ).rjust(4, "0")

        card_tlv.append((TlvTag.AMOUNT.value, bytes.fromhex(amount)))
        card_tlv.append((TlvTag.AMOUNT_OTHER.value, bytes.fromhex(other_amount)))
        card_tlv.append((TlvTag.CID.value, bytes.fromhex("80")))
        card_tlv.append((TlvTag.TRANSACTION_TYPE.value, bytes.fromhex(tx_type)))
        card_tlv.append((TlvTag.TERM_CAP.value, bytes.fromhex("60F8C8")))
        card_tlv.append(
            (TlvTag.IAD.value, bytes.fromhex("0310A04001240000000000000000000000FF"))
        )
        card_tlv.append((TlvTag.AIP.value, bytes.fromhex("3900")))
        card_tlv.append((TlvTag.AID.value, bytes.fromhex(aid)))
        card_tlv.append(
            (TlvTag.ATC.value, bytes.fromhex(tx_counter[len(tx_counter) - 4 :]))
        )
        card_tlv.append((TlvTag.APP_CRYPTO.value, bytes.fromhex("67867D992FEC13D4")))
        card_tlv.append((TlvTag.TX_DATE.value, bytes.fromhex(transaction.date)))

        term_country = pydash.default_to(
            countries.get(alpha_3=terminal.country), countries.get(alpha_3="MEX")
        ).numeric.rjust(4, "0")
        tx_currency = pydash.default_to(
            currencies.get(alpha_3=transaction.currency), currencies.get(alpha_3="MXN")
        ).numeric.rjust(4, "0")
        card_tlv.append((TlvTag.TERM_COUNTRY.value, bytes.fromhex(term_country)))
        card_tlv.append((TlvTag.TX_CURRENCY.value, bytes.fromhex(tx_currency)))
        card_tlv.append((TlvTag.TERM_VER_RESULTS.value, bytes.fromhex("0000008000")))
        card_tlv.append((TlvTag.UNP_NUMBER.value, bytes.fromhex("4A37ADDF")))
        card_tlv.append((TlvTag.DED_FILE.value, bytes.fromhex(aid)))
        card_tlv.append(
            (
                TlvTag.APP_SEQ_NUM.value,
                bytes.fromhex(get_as_hex_string(card.sequence_number)),
            )
        )

        cardholder_name = bytes(card.cardholder_name, "ascii")
        track2_equivalent = self.__generate_track2(card)
        card_tlv.append((TlvTag.CARDHOLDER_NAME.value, cardholder_name))
        card_tlv.append((TlvTag.FFI.value, bytes.fromhex("02180000303000")))
        card_tlv.append((TlvTag.CVM_RESULTS.value, bytes.fromhex("1E0300")))
        card_tlv.append(
            (TlvTag.TRACK2_EQUIVALENT.value, bytes.fromhex(track2_equivalent))
        )
        card_tlv.append((TlvTag.APP_PAN.value, bytes.fromhex(card.pan)))
        card_tlv.append((TlvTag.ISS_SCRIPT_RESULTS.value, bytes.fromhex("1234567890")))
        card_tlv.append((TlvTag.APP_VER_NUMBER.value, bytes.fromhex("0001")))
        card_tlv.append((TlvTag.TERM_TYPE.value, bytes.fromhex("22")))

        tlv_bytes = Tlv.build(card_tlv)

        return tlv_bytes.hex().upper()

    @staticmethod
    def __get_aid_(brand: str) -> str:
        aid = {
            "Mastercard": "A0000000041010",
            "Visa": "A0000000031010",
            "Carnet": "A0000000041010",
        }

        return pydash.objects.get(aid, brand, "A0000000041010")

    @staticmethod
    def __get_transaction_type_(tx_type: str) -> str:
        processing_codes = {
            "charge": "00",
            "balance": "31",
            "cash": "01",
            "credit voucher": "20",
            "void": "02",
        }
        return pydash.objects.get(processing_codes, tx_type, "00")

    @staticmethod
    def __generate_track1(card: Card) -> str:
        expiry_date = "{0}{1}".format(card.expiry_year, card.expiry_month)
        cardholder_name = card.cardholder_name.ljust(26, " ")
        track1_data = "B{0}^{1}^{2}{3}123400001230  ".format(
            card.pan, cardholder_name, expiry_date, card.service_code
        )
        return bytes(track1_data, "ascii").hex()

    @staticmethod
    def __generate_track2(card: Card) -> str:
        expiry_date = "{0}{1}".format(card.expiry_year, card.expiry_month)
        track2_data = "{0}D{1}{2}123400001230".format(
            card.pan, expiry_date, card.service_code
        )
        return track2_data
