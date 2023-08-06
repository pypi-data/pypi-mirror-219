"""
Metadata attached to fields in a data class definition.
"""

from dataclasses import dataclass
from typing import Dict, List, TypeVar, Union

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

from strong_typing.auxiliary import CompactDataClass


T = TypeVar("T")


class DataClass(Protocol[T]):
    "Identifies a type as a dataclass type."

    __dataclass_fields__: Dict


@dataclass(frozen=True, repr=False)
class Reference(CompactDataClass):
    "Captures a set of columns in a table referenced by a foreign key constraint."

    table: str
    column: Union[str, List[str]]


@dataclass(frozen=True, repr=False)
class PrimaryKey(CompactDataClass):
    "Identifies a set of columns in a table as part of the primary key."

    name: str
    column: Union[str, List[str]]


@dataclass(frozen=True, repr=False)
class ForeignKey(CompactDataClass):
    "Declares a foreign key in a table."

    name: str
    references: Reference


@dataclass(frozen=True, repr=False)
class DiscriminatedKey(CompactDataClass):
    "Declares a discriminated union of foreign keys in a table."

    name: str
    discriminator: str
    references: List[Reference]
