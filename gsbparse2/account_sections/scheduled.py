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
            Nb=int(element.attrib["Nb"]),
            Dt=cls.parse_date(element.attrib["Dt"]),
            Ac=int(element.attrib["Ac"]),
            Am=cls.parse_amount(element.attrib["Am"]),
            Cu=int(element.attrib["Cu"]),
            Pa=int(element.attrib["Pa"]),
            Ca=int(element.attrib["Ca"]),
            Sca=int(element.attrib["Sca"]),
            Tra=int(element.attrib["Tra"]),
            Pn=int(element.attrib["Pn"]),
            CPn=int(element.attrib["CPn"]),
            Pc=element.attrib["Pc"],
            Fi=int(element.attrib["Fi"]),
            Bu=int(element.attrib["Bu"]),
            Sbu=int(element.attrib["Sbu"]),
            No=element.attrib["No"],
            Au=int(element.attrib["Au"]),
            Fd=int(element.attrib["Fd"]),
            Pe=int(element.attrib["Pe"]),
            Pei=int(element.attrib["Pei"]),
            Pep=int(element.attrib["Pep"]),
            Dtl=element.attrib["Dtl"],
            Br=cls.parse_bool(element.attrib["Br"]),
            Mo=int(element.attrib["Mo"]),
        )
