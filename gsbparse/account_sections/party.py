from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class PartySection(GsbFileSection):
    Nb: int
    Na: str
    Txt: str
    Search: str
    IgnCase: bool
    UseRegex: bool

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nb=int(element.attrib.get("Nb")),
            Na=element.attrib.get("Na"),
            Txt=element.attrib.get("Txt"),
            Search=element.attrib.get("Search"),
            IgnCase=cls.parse_bool(element.attrib.get("IgnCase")),
            UseRegex=cls.parse_bool(element.attrib.get("UseRegex")),
        )
