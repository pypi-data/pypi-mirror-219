from typing import Iterator


def decapitalize(string: str):
    return string[:1].lower() + string[1:]


def concatenate_string(
    iterator: Iterator[str],
    delimiter: str = ", ",
    last_delimiter: str = " et ",
    last_ponctuation="",
) -> str:
    list_it = list(iterator)
    return (
        delimiter.join(list_it[:-1]) + last_delimiter + list_it[-1]
        if len(list_it) > 1
        else f"{list_it[0]}"
    ) + last_ponctuation
