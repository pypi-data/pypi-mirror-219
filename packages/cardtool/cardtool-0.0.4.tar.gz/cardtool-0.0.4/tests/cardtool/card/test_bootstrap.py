from hamcrest import assert_that, instance_of

from cardtool.card.bootstrap import bootstrap
from cardtool.card.dump import CardDumper, Dumper
from cardtool.card.model import CardConfig, Key
from cardtool.util.serialize import Serialize


def test_bootstrap_should_create_a_dumper_when_called():
    cfg = CardConfig(key={"shared": Key()})
    dumper = bootstrap(cfg, Serialize.JSON.value)
    assert_that(dumper, instance_of(CardDumper))
    assert_that(issubclass(dumper.__class__, Dumper))
