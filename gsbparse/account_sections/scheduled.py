from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse.account_sections._abstract_section import GsbFileSection


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
            Nb=int(element.attrib.get("Nb")),
            Dt=cls.parse_date(element.attrib.get("Dt")),
            Ac=int(element.attrib.get("Ac")),
            Am=cls.parse_amount(element.attrib.get("Am")),
            Cu=int(element.attrib.get("Cu")),
            Pa=int(element.attrib.get("Pa")),
            Ca=int(element.attrib.get("Ca")),
            Sca=int(element.attrib.get("Sca")),
            Tra=int(element.attrib.get("Tra")),
            Pn=int(element.attrib.get("Pn")),
            CPn=int(element.attrib.get("CPn")),
            Pc=element.attrib.get("Pc"),
            Fi=int(element.attrib.get("Fi")),
            Bu=int(element.attrib.get("Bu")),
            Sbu=int(element.attrib.get("Sbu")),
            No=element.attrib.get("No"),
            Au=int(element.attrib.get("Au")),
            Fd=int(element.attrib.get("Fd")),
            Pe=int(element.attrib.get("Pe")),
            Pei=int(element.attrib.get("Pei")),
            Pep=int(element.attrib.get("Pep")),
            Dtl=element.attrib.get("Dtl"),
            Br=cls.parse_bool(element.attrib.get("Br")),
            Mo=int(element.attrib.get("Mo")),
        )
