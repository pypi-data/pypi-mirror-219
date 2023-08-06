import sys

import click
from loguru import logger

from cardtool.tr31.decrypt import TR31Decryption
from cardtool.validation.command import apply_in_order, validate_string_callable
from cardtool.validation.rules import regex


def validate_kcv():
    validate = apply_in_order(regex("[A-F0-9]{6}"))
    return validate_string_callable(validate)


def validate_kbpk():
    validate = apply_in_order(regex("[A-F0-9]{32}"))
    return validate_string_callable(validate)


def validate_kblock():
    validate = apply_in_order(regex("[A-Z0-9]{72,80}"))
    return validate_string_callable(validate)


def decrypt_tr31(decrypt: TR31Decryption):
    @click.command(name="decrypt-key")
    @click.option(
        "--kbpk",
        "-kbpk",
        type=str,
        required=True,
        callback=validate_kbpk(),
        help="Key block protection key",
    )
    @click.option(
        "--kcv",
        "-kcv",
        type=str,
        required=True,
        callback=validate_kcv(),
        help="Key check value",
    )
    @click.argument("kblock", type=str, callback=validate_kblock())
    def __inner_(kbpk: str, kcv: str, kblock: str):
        try:
            plaintext_key = decrypt.decrypt(kbpk, kcv, kblock)
            click.echo(f"Plaintext Key: {plaintext_key}")
        except Exception as e:
            logger.error(e)
            click.echo("Error: {0}".format(e))
            sys.exit(1)

    return __inner_
