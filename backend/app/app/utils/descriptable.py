from enum import *
from typing import Annotated, Type, Any
from dataclasses import dataclass
import string


@dataclass
class Description:
    """
    Description dataclass for annotations
    """
    value: str


def Described(t: Type, description: str, *args) -> Type:
    """
    annotate type by description

    :param t: annotated type
    :param description: text of description
    :param args: extra args for annotation
    :return: annotated type
    """
    return Annotated[t, Description(description), *args]


def describe(
        enum_type: Type[Enum],
        line: str = "{0} - {1}  \n",
        descriptors_separator: str = " "
) -> str:
    """
    describe enum type using members' annotation

    :param enum_type: enum type
    :param line: format line for description of each member. The line must contain only indices 0 and 1
    :param descriptors_separator: separator for many description annotation
    :return: enum type description
    """

    if any(symbol not in ('0', '1', None) for _, symbol, *_ in string.Formatter().parse(line)):
        raise ValueError("The line must contain only indices 0 and 1")

    description: str = ""

    annotations_map: dict[str, Type] = {
                                           i.name: Described(type(i.value), i.name)
                                           for i
                                           in enum_type
                                       } | enum_type.__annotations__

    for name, annotations in annotations_map.items():

        member: Enum = getattr(enum_type, name)

        val: Any = member.value
        descriptors: list[str] = []
        for annotation in annotations.__metadata__:
            if isinstance(annotation, Description):
                descriptors.append(annotation.value)

        formatted_line: str = line.format(val, descriptors_separator.join(descriptors))
        description += formatted_line

    return description
