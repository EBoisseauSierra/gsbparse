from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class BetGraphSection(GsbFileSection):
    prefs: str

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            prefs=element.attrib["prefs"],
        )
