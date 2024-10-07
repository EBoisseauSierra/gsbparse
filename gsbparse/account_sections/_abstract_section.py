from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET


@dataclass(frozen=True)
class GsbFileSection(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_xml(cls, element: ET.Element) -> Self: ...

    @staticmethod
    def parse_list_int(list_str: str, separator: str = "-") -> list[int] | None:
        if list_str == "(null)":
            return None
        return [int(i) for i in list_str.split(separator)]

    @staticmethod
    def parse_amount(amount_str: str) -> Decimal:
        return Decimal(amount_str.replace(",", "."))

    @staticmethod
    def parse_bool(bool_str: str) -> bool:
        return bool(int(bool_str))

    @staticmethod
    def parse_date(date_str: str) -> date | None:
        if date_str == "(null)":
            return None
        return datetime.strptime(date_str, "%m/%d/%Y").date()
