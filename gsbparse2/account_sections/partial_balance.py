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
            Nb=cls.parse_int(element.attrib.get("Nb")),
            Na=cls.parse_str(element.attrib.get("Na")),
            Acc=cls.parse_list_int(element.attrib.get("Acc"), separator=";"),
            Kind=cls.parse_int(element.attrib.get("Kind")),
            Currency=cls.parse_int(element.attrib.get("Currency")),
            Colorise=cls.parse_bool(element.attrib.get("Colorise")),
        )
