from dataclasses import dataclass
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class CurrencyLinkSection(GsbFileSection):
    Nb: int
    Cu1: int
    Cu2: int
    Ex: Decimal
    Fl: bool

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nb=cls.parse_int(element.attrib.get("Nb")),
            Cu1=cls.parse_int(element.attrib.get("Cu1")),
            Cu2=cls.parse_int(element.attrib.get("Cu2")),
            Ex=cls.parse_amount(element.attrib.get("Ex")),
            Fl=cls.parse_bool(element.attrib.get("Fl")),
        )
