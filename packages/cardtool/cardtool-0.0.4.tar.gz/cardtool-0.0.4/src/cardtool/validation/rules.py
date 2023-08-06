import re


def length_between(min: int, max: int):
    def __inner_(data: str):
        len_data = len(data)
        if len_data < min or len_data > max:
            raise ValueError(
                "{0} length is not between ({1}, {2})".format(data, min, max)
            )
        return data

    return __inner_


def length(total: int):
    def __inner_(data: str):
        len_data = len(data)
        if len_data != total:
            raise ValueError(
                "{0} does not have required length {1}".format(data, total)
            )
        return data

    return __inner_


def regex(pattern: str, flags: re.RegexFlag = 0):
    rex = re.compile(pattern)

    def __inner_(data: str):
        if not re.fullmatch(rex, data, flags=flags):
            raise ValueError(
                "{0} does not conform with required pattern {1}".format(data, pattern)
            )
        return data

    return __inner_
