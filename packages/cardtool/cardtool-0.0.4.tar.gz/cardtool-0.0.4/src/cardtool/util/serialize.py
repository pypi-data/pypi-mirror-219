from __future__ import annotations

from abc import ABC
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import IO, Any, Generic, Iterable, Sequence, TypeVar

import simplejson as json
import yaml


class Serializer(ABC):
    def serialize(self, it: Iterable[Any], stream: IO):  # pragma: nocover
        pass


S = TypeVar("S", bound=Serializer)


class Serialize(Enum):
    JSON = "json"
    YAML = "yaml"


def new_serializer(serializer: str) -> Generic[S]:
    if serializer == Serialize.YAML.value:
        return YAMLSerializer()

    if serializer == Serialize.JSON.value:
        return JSONSerializer()

    raise ValueError("unknown serializer")


class CustomJSONSerializer(json.JSONEncoder):
    def default(self, o: Any):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


class JSONSerializer(Serializer):
    def serialize(self, it: Iterable[Any], stream: IO):
        json.dump(it, stream, iterable_as_array=True, cls=CustomJSONSerializer)

    def __call__(self, *args, **kwargs):
        (data, stream, *_) = args
        return self.serialize(it=data, stream=stream)


class YAMLSerializer(Serializer):
    def serialize(self, it: Sequence[Any], stream: IO):
        yaml.dump_all(it, stream)

    def __call__(self, *args, **kwargs):
        (data, stream, *_) = args
        return self.serialize(it=data, stream=stream)
