from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class BetFutureSection(GsbFileSection):
    Nb: int
    Dt: date
    Ac: int
    Am: Decimal
    Pa: int
    IsT: bool
    Tra: int
    Ca: int
    Sca: int
    Pn: int
    Fi: int
    Bu: int
    Sbu: int
    No: int
    Au: int
    Pe: int
    Pei: int
    Pep: int
    Dtl: date
    Mo: int

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nb=int(element.attrib["Nb"]),
            Dt=cls.parse_date(element.attrib["Dt"]),
            Ac=int(element.attrib["Ac"]),
            Am=cls.parse_amount(element.attrib["Am"]),
            Pa=int(element.attrib["Pa"]),
            IsT=cls.parse_bool(element.attrib["IsT"]),
            Tra=int(element.attrib["Tra"]),
            Ca=int(element.attrib["Ca"]),
            Sca=int(element.attrib["Sca"]),
            Pn=int(element.attrib["Pn"]),
            Fi=int(element.attrib["Fi"]),
            Bu=int(element.attrib["Bu"]),
            Sbu=int(element.attrib["Sbu"]),
            No=int(element.attrib["No"]),
            Au=int(element.attrib["Au"]),
            Pe=int(element.attrib["Pe"]),
            Pei=int(element.attrib["Pei"]),
            Pep=int(element.attrib["Pep"]),
            Dtl=cls.parse_date(element.attrib["Dtl"]),
            Mo=int(element.attrib["Mo"]),
        )
