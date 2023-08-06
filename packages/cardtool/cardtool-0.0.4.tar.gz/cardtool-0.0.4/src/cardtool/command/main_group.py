import click

from cardtool.card.bootstrap import bootstrap
from cardtool.command.gen_card import init_gen_card
from cardtool.command.tr31_decrypt import decrypt_tr31
from cardtool.log.logger import configure_logger
from cardtool.tr31 import decrypt

WELCOME_MESSAGE = (
    "Welcome to our card data generation tool. Please see usage with --help flag"
)


@click.group(invoke_without_command=True)
@click.pass_context
def cli_card(ctx):
    configure_logger()
    if ctx.invoked_subcommand is None:
        click.echo(WELCOME_MESSAGE)
    else:
        pass


cli_card.add_command(init_gen_card(bootstrap))
# TODO: change this to use a factory.
cli_card.add_command(decrypt_tr31(decrypt.new()))
