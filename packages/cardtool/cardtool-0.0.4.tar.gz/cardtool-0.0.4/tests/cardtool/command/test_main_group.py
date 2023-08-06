from click.testing import CliRunner
from hamcrest import (
    assert_that,
    contains_string,
    equal_to,
    not_,
    string_contains_in_order,
)

from cardtool.command.main_group import WELCOME_MESSAGE, cli_card
from helper.common import SUCCESS_EXIT_CODE


class TestMainGroup:
    def test_should_show_a_welcome_message(self):
        runner = CliRunner()
        result = runner.invoke(cli_card, None)
        assert_that(result.exit_code, equal_to(SUCCESS_EXIT_CODE))
        assert_that(result.output, equal_to(WELCOME_MESSAGE + "\n"))

    def test_should_not_show_a_welcome_message_when_a_command_is_supplied(self):
        runner = CliRunner()
        result = runner.invoke(cli_card, ["gen-card", "--help"])
        assert_that(result.output, not_(contains_string(WELCOME_MESSAGE)))
        assert_that(result.exit_code, equal_to(SUCCESS_EXIT_CODE))

    def test_should_show_all_available_commands(self):
        runner = CliRunner()
        result = runner.invoke(cli_card, ["--help"])

        commands = ["decrypt-key", "gen-card"]
        assert_that(result.exit_code, equal_to(SUCCESS_EXIT_CODE))
        assert_that(result.output, string_contains_in_order(*commands))
