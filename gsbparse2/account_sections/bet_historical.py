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
            Nb=int(element.attrib["Nb"]),
            Ac=int(element.attrib["Ac"]),
            Ori=int(element.attrib["Ori"]),
            Div=int(element.attrib["Div"]),
            Edit=int(element.attrib["Edit"]),
            Damount=cls.parse_amount(element.attrib["Damount"]),
            SDiv=int(element.attrib["SDiv"]),
            SDamount=cls.parse_amount(element.attrib["SDamount"]),
        )
