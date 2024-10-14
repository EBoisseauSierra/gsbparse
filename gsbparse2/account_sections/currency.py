from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class CurrencySection(GsbFileSection):
    Nb: int
    Na: str
    Co: str
    Ico: str
    Fl: int

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nb=cls.parse_int(element.attrib.get("Nb")),
            Na=cls.parse_str(element.attrib.get("Na")),
            Co=cls.parse_str(element.attrib.get("Co")),
            Ico=cls.parse_str(element.attrib.get("Ico")),
            Fl=cls.parse_int(element.attrib.get("Fl")),
        )
