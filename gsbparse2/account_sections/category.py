from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class CategorySection(GsbFileSection):
    Nb: int
    Na: str
    Kd: int

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nb=cls.parse_int(element.attrib.get("Nb")),
            Na=cls.parse_str(element.attrib.get("Na")),
            Kd=cls.parse_int(element.attrib.get("Kd")),
        )
