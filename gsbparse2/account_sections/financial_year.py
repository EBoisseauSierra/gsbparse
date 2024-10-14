from dataclasses import dataclass
from datetime import date
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class FinancialYearSection(GsbFileSection):
    Nb: int
    Na: str
    Bdte: date
    Edte: date
    Sho: bool

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nb=cls.parse_int(element.attrib.get("Nb")),
            Na=cls.parse_str(element.attrib.get("Na")),
            Bdte=cls.parse_date(element.attrib.get("Bdte")),
            Edte=cls.parse_date(element.attrib.get("Edte")),
            Sho=cls.parse_bool(element.attrib.get("Sho")),
        )
