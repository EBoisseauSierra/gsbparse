from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class PartialBalanceSection(GsbFileSection):
    Nb: int
    Na: str
    Acc: list[int]
    Kind: int
    Currency: int
    Colorise: bool

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nb=int(element.attrib["Nb"]),
            Na=element.attrib["Na"],
            Acc=cls.parse_list_int(element.attrib["Acc"], separator=";"),
            Kind=int(element.attrib["Kind"]),
            Currency=int(element.attrib["Currency"]),
            Colorise=cls.parse_bool(element.attrib["Colorise"]),
        )
