from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum
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
            Ac=cls.parse_int(element.attrib.get("Ac")),
            Nb=cls.parse_int(element.attrib.get("Nb")),
            Id=cls.parse_str(element.attrib.get("Id")),
            Dt=cls.parse_date(element.attrib.get("Dt")),
            Dv=cls.parse_date(element.attrib.get("Dv")),
            Cu=cls.parse_int(element.attrib.get("Cu")),
            Am=cls.parse_amount(element.attrib.get("Am")),
            Exb=cls.parse_int(element.attrib.get("Exb")),
            Exr=cls.parse_amount(element.attrib.get("Exr")),
            Exf=cls.parse_amount(element.attrib.get("Exf")),
            Pa=cls.parse_int(element.attrib.get("Pa")),
            Ca=cls.parse_int(element.attrib.get("Ca")),
            Sca=cls.parse_int(element.attrib.get("Sca")),
            Br=cls.parse_bool(element.attrib.get("Br")),
            No=cls.parse_str(element.attrib.get("No")),
            Pn=cls.parse_int(element.attrib.get("Pn")),
            Pc=cls.parse_str(element.attrib.get("Pc")),
            Ma=ReconcileStatus(cls.parse_int(element.attrib.get("Ma"))),
            Ar=cls.parse_int(element.attrib.get("Ar")),
            Au=cls.parse_bool(element.attrib.get("Au")),
            Re=cls.parse_int(element.attrib.get("Re")),
            Fi=cls.parse_int(element.attrib.get("Fi")),
            Bu=cls.parse_int(element.attrib.get("Bu")),
            Sbu=cls.parse_int(element.attrib.get("Sbu")),
            Vo=cls.parse_str(element.attrib.get("Vo")),
            Ba=cls.parse_str(element.attrib.get("Ba")),
            Trt=cls.parse_int(element.attrib.get("Trt")),
            Mo=cls.parse_int(element.attrib.get("Mo")),
        )


class ReconcileStatus(Enum):
    not_reconciled = 0
    pointed = 1
    t = 2
    reconciled = 3
    error = -1
