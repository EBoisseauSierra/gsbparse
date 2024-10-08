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
            Nb=int(element.attrib["Nb"]),
            Na=element.attrib["Na"],
            Kd=int(element.attrib["Kd"]),
        )
