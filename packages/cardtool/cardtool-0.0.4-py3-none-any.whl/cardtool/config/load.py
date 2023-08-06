import json
from dataclasses import asdict, is_dataclass
from functools import partial
from os.path import abspath, dirname, join
from typing import Generic, TypeVar

import jsonschema.exceptions
import yaml
from jsonschema import validate

T = TypeVar("T")


def safe_load(file: str, schema: str) -> Generic[T]:
    open_file = partial(open, mode="r", encoding="utf-8")
    with open_file(file) as data_file, open_file(schema) as schema_file:
        try:
            data: T = yaml.safe_load(data_file)
            schema = json.load(schema_file)
            data_dict = data
            if is_dataclass(data):
                data_dict = asdict(data)

            validate(instance=data_dict, schema=schema)
            return data
        except jsonschema.exceptions.ValidationError as err:
            raise ValueError("invalid configuration file") from err


def get_abs_path(path: str) -> str:
    project_dir = dirname(abspath(__file__))
    complete_path = join(project_dir, path)
    return complete_path
