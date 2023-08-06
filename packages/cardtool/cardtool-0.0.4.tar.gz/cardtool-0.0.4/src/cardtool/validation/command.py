from functools import wraps
from typing import Callable

import click


def validate_string_callable(validate: Callable[[str], str]):
    @wraps(validate)
    def wrapper(*args, **_) -> str:
        (_, _, value) = args
        if not isinstance(value, str):
            raise click.BadParameter("parameter is not string")
        try:
            out = validate(value)
            return out
        except ValueError as e:
            raise click.BadParameter("{0}".format(e))

    return wrapper


def apply_in_order(*validator: Callable[[str], str]):
    def __inner_(data: str):
        out = data
        for validate in validator:
            out = validate(out)
        return out

    return __inner_
