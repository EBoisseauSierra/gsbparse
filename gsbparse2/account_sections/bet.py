from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class BetSection(GsbFileSection):
    Ddte: int
    Bet_deb_cash_account_option: int

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Ddte=cls.parse_int(element.attrib.get("Ddte")),
            Bet_deb_cash_account_option=int(
                element.attrib.get("Bet_deb_cash_account_option"),
            ),
        )
