from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse.account_sections._abstract_section import GsbFileSection


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
            Ac=int(element.attrib.get("Ac")),
            Nb=int(element.attrib.get("Nb")),
            Id=element.attrib.get("Id"),
            Dt=cls.parse_date(element.attrib.get("Dt")),
            Dv=cls.parse_date(element.attrib.get("Dv")),
            Cu=int(element.attrib.get("Cu")),
            Am=cls.parse_amount(element.attrib.get("Am")),
            Exb=int(element.attrib.get("Exb")),
            Exr=cls.parse_amount(element.attrib.get("Exr")),
            Exf=cls.parse_amount(element.attrib.get("Exf")),
            Pa=int(element.attrib.get("Pa")),
            Ca=int(element.attrib.get("Ca")),
            Sca=int(element.attrib.get("Sca")),
            Br=cls.parse_bool(element.attrib.get("Br")),
            No=element.attrib.get("No"),
            Pn=int(element.attrib.get("Pn")),
            Pc=element.attrib.get("Pc"),
            Ma=int(element.attrib.get("Ma")),
            Ar=int(element.attrib.get("Ar")),
            Au=int(element.attrib.get("Au")),
            Re=int(element.attrib.get("Re")),
            Fi=int(element.attrib.get("Fi")),
            Bu=int(element.attrib.get("Bu")),
            Sbu=int(element.attrib.get("Sbu")),
            Vo=element.attrib.get("Vo"),
            Ba=element.attrib.get("Ba"),
            Trt=int(element.attrib.get("Trt")),
            Mo=int(element.attrib.get("Mo")),
        )
