from dataclasses import dataclass
from decimal import Decimal
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class AmountComparisonSection(GsbFileSection):
    Comparison_number: int
    Report_nb: int
    Last_comparison: int
    Comparison_1: int
    Link_1_2: int
    Comparison_2: int
    Amount_1: Decimal
    Amount_2: Decimal

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Comparison_number=int(element.attrib["Comparison_number"]),
            Report_nb=int(element.attrib["Report_nb"]),
            Last_comparison=int(element.attrib["Last_comparison"]),
            Comparison_1=int(element.attrib["Comparison_1"]),
            Link_1_2=int(element.attrib["Link_1_2"]),
            Comparison_2=int(element.attrib["Comparison_2"]),
            Amount_1=cls.parse_amount(element.attrib["Amount_1"]),
            Amount_2=cls.parse_amount(element.attrib["Amount_2"]),
        )
