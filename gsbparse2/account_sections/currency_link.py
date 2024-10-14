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
            Nb=int(element.attrib["Nb"]),
            Cu1=int(element.attrib["Cu1"]),
            Cu2=int(element.attrib["Cu2"]),
            Ex=cls.parse_amount(element.attrib["Ex"]),
            Fl=cls.parse_bool(element.attrib["Fl"]),
        )
