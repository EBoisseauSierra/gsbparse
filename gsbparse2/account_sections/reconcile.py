from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class ReconcileSection(GsbFileSection):
    Nb: int
    Na: str
    Acc: int
    Idate: date
    Fdate: date
    Ibal: Decimal
    Fbal: Decimal

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nb=int(element.attrib["Nb"]),
            Na=element.attrib["Na"],
            Acc=int(element.attrib["Acc"]),
            Idate=cls.parse_date(element.attrib["Idate"]),
            Fdate=cls.parse_date(element.attrib["Fdate"]),
            Ibal=cls.parse_amount(element.attrib["Ibal"]),
            Fbal=cls.parse_amount(element.attrib["Fbal"]),
        )
