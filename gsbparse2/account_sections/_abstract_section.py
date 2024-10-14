from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Self
from xml.etree import ElementTree as ET

from gsbparse2.exceptions import XmlParsingError


def parse_null(func):
    "Return None early if the value is '(null)'"

    def wrapper(value: str, *args, **kwargs):
        if value == "(null)":
            return None
        return func(value, *args, **kwargs)

    return wrapper


def parse_optional(func):
    "Catch exception gracefully if parsing the record failed and is optional"

    def wrapper(*args, is_optional: bool = False, **kwargs):
        try:
            return func(*args, **kwargs)
        except (XmlParsingError, KeyError) as e:
            if is_optional:
                return None
            raise e  # noqa: TRY201

    return wrapper


@dataclass(frozen=True)
class GsbFileSection(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_xml(cls, element: ET.Element) -> Self: ...

    @staticmethod
    @parse_null
    @parse_optional
    def parse_list_int(list_str: str, separator: str = "-") -> list[int] | None:
        return [int(i) for i in list_str.split(separator)]

    @staticmethod
    @parse_null
    @parse_optional
    def parse_amount(amount_str: str) -> Decimal:
        return Decimal(amount_str.replace(",", "."))

    @staticmethod
    @parse_null
    @parse_optional
    def parse_bool(bool_str: Literal["0", "1"]) -> bool:
        if bool_str not in {"0", "1"}:
            raise XmlParsingError(
                value=bool_str,
                expected_type=Literal["0", "1"],
            )
        return bool(int(bool_str))

    @staticmethod
    @parse_null
    @parse_optional
    def parse_date(date_str: str) -> date:
        try:
            parsed_date = datetime.strptime(date_str, "%m/%d/%Y").date()
        except ValueError as e:
            raise XmlParsingError(
                value=date_str,
                expected_type=date,
            ) from e
        return parsed_date
