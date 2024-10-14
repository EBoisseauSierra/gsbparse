from dataclasses import dataclass
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class BetHistoricalSection(GsbFileSection):
    Nb: int
    Ac: int
    Ori: int
    Div: int
    Edit: int
    Damount: Decimal
    SDiv: int
    SDamount: Decimal

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nb=cls.parse_int(element.attrib.get("Nb")),
            Ac=cls.parse_int(element.attrib.get("Ac")),
            Ori=cls.parse_int(element.attrib.get("Ori")),
            Div=cls.parse_int(element.attrib.get("Div")),
            Edit=cls.parse_int(element.attrib.get("Edit")),
            Damount=cls.parse_amount(element.attrib.get("Damount")),
            SDiv=cls.parse_int(element.attrib.get("SDiv")),
            SDamount=cls.parse_amount(element.attrib.get("SDamount")),
        )
