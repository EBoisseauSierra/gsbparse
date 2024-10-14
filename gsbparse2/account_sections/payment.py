from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class PaymentSection(GsbFileSection):
    Number: int
    Name: str
    Sign: int
    Show_entry: bool
    Automatic_number: bool
    Current_number: str
    Account: int

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Number=cls.parse_int(element.attrib.get("Number")),
            Name=cls.parse_str(element.attrib.get("Name")),
            Sign=cls.parse_int(element.attrib.get("Sign")),
            Show_entry=cls.parse_bool(element.attrib.get("Show_entry")),
            Automatic_number=cls.parse_bool(element.attrib.get("Automatic_number")),
            Current_number=cls.parse_str(element.attrib.get("Current_number")),
            Account=cls.parse_int(element.attrib.get("Account")),
        )
