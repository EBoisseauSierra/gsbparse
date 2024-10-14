from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class SubcategorySection(GsbFileSection):
    Nbc: int
    Nb: int
    Na: str

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nbc=cls.parse_int(element.attrib.get("Nbc")),
            Nb=cls.parse_int(element.attrib.get("Nb")),
            Na=cls.parse_str(element.attrib.get("Na")),
        )
