from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class TransactionSection(GsbFileSection):
    Ac: int
    Nb: int
    Id: str
    Dt: date
    Dv: date | None
    Cu: int
    Am: Decimal
    Exb: int
    Exr: Decimal
    Exf: Decimal
    Pa: int
    Ca: int
    Sca: int
    Br: bool
    No: str
    Pn: int
    Pc: str
    Ma: int
    Ar: int
    Au: int
    Re: int
    Fi: int
    Bu: int
    Sbu: int
    Vo: str
    Ba: str
    Trt: int
    Mo: int

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Ac=int(element.attrib["Ac"]),
            Nb=int(element.attrib["Nb"]),
            Id=element.attrib["Id"],
            Dt=cls.parse_date(element.attrib["Dt"]),
            Dv=cls.parse_date(element.attrib["Dv"]),
            Cu=int(element.attrib["Cu"]),
            Am=cls.parse_amount(element.attrib["Am"]),
            Exb=int(element.attrib["Exb"]),
            Exr=cls.parse_amount(element.attrib["Exr"]),
            Exf=cls.parse_amount(element.attrib["Exf"]),
            Pa=int(element.attrib["Pa"]),
            Ca=int(element.attrib["Ca"]),
            Sca=int(element.attrib["Sca"]),
            Br=cls.parse_bool(element.attrib["Br"]),
            No=element.attrib["No"],
            Pn=int(element.attrib["Pn"]),
            Pc=element.attrib["Pc"],
            Ma=int(element.attrib["Ma"]),
            Ar=int(element.attrib["Ar"]),
            Au=int(element.attrib["Au"]),
            Re=int(element.attrib["Re"]),
            Fi=int(element.attrib["Fi"]),
            Bu=int(element.attrib["Bu"]),
            Sbu=int(element.attrib["Sbu"]),
            Vo=element.attrib["Vo"],
            Ba=element.attrib["Ba"],
            Trt=int(element.attrib["Trt"]),
            Mo=int(element.attrib["Mo"]),
        )
