import functools
import os
from multiprocessing import Pool
from typing import Callable

import click
import dill as pickle  # NOQA

from cardtool.card.dump import Dumper
from cardtool.card.model import CardConfig
from cardtool.config.load import get_abs_path, safe_load
from cardtool.util.serialize import Serialize
from cardtool.validation.command import validate_string_callable


def validate_file():
    validator = functools.partial(safe_load, schema=get_abs_path("card-config.json"))
    return validate_string_callable(validator)


def init_gen_card(bootstrap: Callable[[CardConfig, str], Dumper]):
    @click.command(name="gen-card")
    @click.option(
        "--config",
        "-cfg",
        type=click.Path(exists=True, readable=True, file_okay=True, dir_okay=False),
        required=True,
        callback=validate_file(),
    )
    @click.option(
        "--fmt",
        "-fmt",
        type=click.Choice(
            [Serialize.JSON.value, Serialize.YAML.value], case_sensitive=True
        ),
        required=True,
    )
    @click.argument(
        "out_file",
        type=click.Path(
            writable=True,
            resolve_path=True,
            dir_okay=False,
            file_okay=True,
            exists=False,
        ),
    )
    def __inner_(config: CardConfig, fmt: str, out_file: str):
        with Pool(os.cpu_count()) as p:
            dumper = bootstrap(config, fmt)
            imap = functools.partial(p.imap_unordered, chunksize=10)
            dumper.dump_cards(out_file, config, imap)
            click.echo("Done!")

    return __inner_
