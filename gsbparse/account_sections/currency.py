from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse.account_sections._abstract_section import GsbFileSection


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
            Nb=int(element.attrib.get("Nb")),
            Na=element.attrib.get("Na"),
            Co=element.attrib.get("Co"),
            Ico=element.attrib.get("Ico"),
            Fl=int(element.attrib.get("Fl")),
        )
