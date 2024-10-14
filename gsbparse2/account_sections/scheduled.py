from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class ScheduledSection(GsbFileSection):
    Nb: int
    Dt: date
    Ac: int
    Am: Decimal
    Cu: int
    Pa: int
    Ca: int
    Sca: int
    Tra: int
    Pn: int
    CPn: int
    Pc: str
    Fi: int
    Bu: int
    Sbu: int
    No: str
    Au: int
    Fd: int
    Pe: int
    Pei: int
    Pep: int
    Dtl: str
    Br: bool
    Mo: int

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nb=cls.parse_int(element.attrib.get("Nb")),
            Dt=cls.parse_date(element.attrib.get("Dt")),
            Ac=cls.parse_int(element.attrib.get("Ac")),
            Am=cls.parse_amount(element.attrib.get("Am")),
            Cu=cls.parse_int(element.attrib.get("Cu")),
            Pa=cls.parse_int(element.attrib.get("Pa")),
            Ca=cls.parse_int(element.attrib.get("Ca")),
            Sca=cls.parse_int(element.attrib.get("Sca")),
            Tra=cls.parse_int(element.attrib.get("Tra")),
            Pn=cls.parse_int(element.attrib.get("Pn")),
            CPn=cls.parse_int(element.attrib.get("CPn")),
            Pc=cls.parse_str(element.attrib.get("Pc")),
            Fi=cls.parse_int(element.attrib.get("Fi")),
            Bu=cls.parse_int(element.attrib.get("Bu")),
            Sbu=cls.parse_int(element.attrib.get("Sbu")),
            No=cls.parse_str(element.attrib.get("No")),
            Au=cls.parse_int(element.attrib.get("Au")),
            Fd=cls.parse_int(element.attrib.get("Fd")),
            Pe=cls.parse_int(element.attrib.get("Pe")),
            Pei=cls.parse_int(element.attrib.get("Pei")),
            Pep=cls.parse_int(element.attrib.get("Pep")),
            Dtl=cls.parse_str(element.attrib.get("Dtl")),
            Br=cls.parse_bool(element.attrib.get("Br")),
            Mo=cls.parse_int(element.attrib.get("Mo")),
        )
