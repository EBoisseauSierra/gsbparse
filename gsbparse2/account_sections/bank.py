from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class BankSection(GsbFileSection):
    Nb: int
    Na: str
    Co: str
    BIC: str
    Adr: str
    Tel: str
    Mail: str
    Web: str
    Nac: str
    Faxc: str
    Telc: str
    Mailc: str
    Rem: str

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Nb=cls.parse_int(element.attrib.get("Nb")),
            Na=cls.parse_str(element.attrib.get("Na")),
            Co=cls.parse_str(element.attrib.get("Co")),
            BIC=cls.parse_str(element.attrib.get("BIC")),
            Adr=cls.parse_str(element.attrib.get("Adr")),
            Tel=cls.parse_str(element.attrib.get("Tel")),
            Mail=cls.parse_str(element.attrib.get("Mail")),
            Web=cls.parse_str(element.attrib.get("Web")),
            Nac=cls.parse_str(element.attrib.get("Nac")),
            Faxc=cls.parse_str(element.attrib.get("Faxc")),
            Telc=cls.parse_str(element.attrib.get("Telc")),
            Mailc=cls.parse_str(element.attrib.get("Mailc")),
            Rem=cls.parse_str(element.attrib.get("Rem")),
        )
