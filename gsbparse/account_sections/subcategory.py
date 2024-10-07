from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class SubcategorySection(GsbFileSection):
    Nbc: int
    Nb: int
    Na: str

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nbc=int(element.attrib.get("Nbc")),
            Nb=int(element.attrib.get("Nb")),
            Na=element.attrib.get("Na"),
        )
