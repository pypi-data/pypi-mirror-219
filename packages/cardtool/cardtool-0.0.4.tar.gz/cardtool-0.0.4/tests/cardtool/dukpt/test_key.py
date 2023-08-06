from collections import namedtuple

import pytest
from hamcrest import assert_that, equal_to

from cardtool.dukpt.key import generate_key
from cardtool.dukpt.key_type import KeyType

KeyTuple = namedtuple("KeyTuple", "Data Mac Pin Session Ikey")

testdata = [
    # BDK, KSN
    (0, "0123456789ABCDEFFEDCBA9876543210", "FFFF4357486333600003"),
    (1, "0123456789ABCDEFFEDCBA9876543210", "FFFF444456444440000D"),
]

test_result = {
    0: KeyTuple(
        "CA7091701C616F92697955B77E723D27",
        "6FF19ADA821E250A87D77C0E1C000AA4",
        "6FF19ADA821EDAF587D77C0E1C00F55B",
        "6FF19ADA821EDA0A87D77C0E1C00F5A4",
        "D7147FDAFDC32CC450AA594D8D40FABF",
    ),
    1: KeyTuple(
        "68005F7AEF2F3D9008BA02AEAC7F4B2C",
        "5B1F91B01E2D7CBA23C84658675A0D5D",
        "5B1F91B01E2D834523C84658675AF2A2",
        "5B1F91B01E2D83BA23C84658675AF25D",
        "A383B0FCC4C426FAF5268E0532F3B59C",
    ),
}


class TestGenerateKey:
    @pytest.mark.parametrize("test_id,bdk,ksn", testdata)
    def test_should_get_data_key_when_requested(self, test_id, bdk, ksn):
        data_key = test_result[test_id].Data
        key = generate_key(bdk=bdk, ksn=ksn, key_type=KeyType.DATA)
        assert_that(key, equal_to(data_key))

    @pytest.mark.parametrize("test_id,bdk,ksn", testdata)
    def test_should_get_mac_key_when_requested(self, test_id, bdk, ksn):
        mac_key = test_result[test_id].Mac
        key = generate_key(bdk=bdk, ksn=ksn, key_type=KeyType.MAC)
        assert_that(key, equal_to(mac_key))

    @pytest.mark.parametrize("test_id,bdk,ksn", testdata)
    def test_should_get_pin_key_when_requested(self, test_id, bdk, ksn):
        pin_key = test_result[test_id].Pin
        key = generate_key(bdk=bdk, ksn=ksn, key_type=KeyType.PIN)
        assert_that(key, equal_to(pin_key))

    @pytest.mark.parametrize("test_id,bdk,ksn", testdata)
    def test_should_get_session_key_when_requested(self, test_id, bdk, ksn):
        session_key = test_result[test_id].Session
        key = generate_key(bdk=bdk, ksn=ksn, key_type=KeyType.SESSION)
        assert_that(key, equal_to(session_key))

    @pytest.mark.parametrize("test_id, bdk,ksn", testdata)
    def test_should_get_ikey_when_requested(self, test_id, bdk, ksn):
        ikey = test_result[test_id].Ikey
        key = generate_key(bdk=bdk, ksn=ksn, key_type=KeyType.IKEY)
        assert_that(key, equal_to(ikey))

    def test_should_throw_unknown_key_variant(self):
        with pytest.raises(Exception, match="unknown key variant"):
            (_, bdk, ksn) = testdata[0]
            generate_key(bdk=bdk, ksn=ksn, key_type=KeyType.UNKNOWN)
