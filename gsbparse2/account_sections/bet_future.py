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
            Nb=cls.parse_int(element.attrib.get("Nb")),
            Dt=cls.parse_date(element.attrib.get("Dt")),
            Ac=cls.parse_int(element.attrib.get("Ac")),
            Am=cls.parse_amount(element.attrib.get("Am")),
            Pa=cls.parse_int(element.attrib.get("Pa")),
            IsT=cls.parse_bool(element.attrib.get("IsT")),
            Tra=cls.parse_int(element.attrib.get("Tra")),
            Ca=cls.parse_int(element.attrib.get("Ca")),
            Sca=cls.parse_int(element.attrib.get("Sca")),
            Pn=cls.parse_int(element.attrib.get("Pn")),
            Fi=cls.parse_int(element.attrib.get("Fi")),
            Bu=cls.parse_int(element.attrib.get("Bu")),
            Sbu=cls.parse_int(element.attrib.get("Sbu")),
            No=cls.parse_int(element.attrib.get("No")),
            Au=cls.parse_int(element.attrib.get("Au")),
            Pe=cls.parse_int(element.attrib.get("Pe")),
            Pei=cls.parse_int(element.attrib.get("Pei")),
            Pep=cls.parse_int(element.attrib.get("Pep")),
            Dtl=cls.parse_date(element.attrib.get("Dtl")),
            Mo=cls.parse_int(element.attrib.get("Mo")),
        )
