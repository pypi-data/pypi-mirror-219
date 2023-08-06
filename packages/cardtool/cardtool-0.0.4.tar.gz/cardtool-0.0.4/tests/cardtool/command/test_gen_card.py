import os.path
from unittest.mock import MagicMock, Mock, patch

import pytest
from click.testing import CliRunner
from hamcrest import assert_that, contains_string, equal_to

from cardtool.card.dump import Dumper
from cardtool.card.model import CardConfig
from cardtool.command.gen_card import init_gen_card
from helper.common import PARAM_FAILURE_EXIT_CODE


@pytest.mark.parametrize(
    "config_file,fmt", [("card-config.yaml", "json"), ("card-config.yaml", "yaml")]
)
@patch("cardtool.command.gen_card.safe_load")
@patch("cardtool.command.gen_card.Pool", new_callable=MagicMock())
def test_gen_card_should_run_successfully(
    pool, safe_load, config_file, fmt, data_resolver, tmp_path
):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        card_cfg = CardConfig()
        safe_load.return_value = card_cfg
        dumper = Mock(spec=Dumper)
        bootstrap = MagicMock(return_value=dumper)

        cmd = init_gen_card(bootstrap)
        cfg_file = data_resolver("data", config_file)
        out_file = os.path.join(td, "test-gen.{0}".format(fmt))
        result = runner.invoke(
            cmd,
            [
                "-cfg",
                cfg_file,
                "-fmt",
                fmt,
                out_file,
            ],
        )
        bootstrap.assert_called_once_with(card_cfg, fmt)
        dumper.dump_cards.assert_called_once()
        safe_load.assert_called_once()
        assert_that(result.output, equal_to("Done!\n"))
        assert_that(result.exit_code, equal_to(0))


@pytest.mark.parametrize(
    "config_file,fmt,out_file,msg",
    [
        ("bad-config.yaml", "json", "out.json", "invalid configuration file"),
        (
            "card-config.yaml",
            "fake",
            "out.yaml",
            """'fake' is not one of 'json', 'yaml'""",
        ),
        ("card-config.yaml", "json", ".", """is a directory"""),
    ],
    ids=["invalid config", "invalid format", "invalid out file"],
)
def test_gen_card_should_raise_an_error_when_it_receives_a_bad_parameter_as_(
    config_file, fmt, out_file, msg, data_resolver, tmp_path
):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        dumper = Mock(spec=Dumper)
        bootstrap = MagicMock(return_value=dumper)

        cmd = init_gen_card(bootstrap)
        cfg_file = data_resolver("data", config_file)
        out_file = os.path.join(td, out_file)
        result = runner.invoke(
            cmd,
            [
                "-cfg",
                cfg_file,
                "-fmt",
                fmt,
                out_file,
            ],
        )
        bootstrap.assert_not_called()
        assert_that(result.output, contains_string(msg))
        assert_that(result.exit_code, equal_to(PARAM_FAILURE_EXIT_CODE))
