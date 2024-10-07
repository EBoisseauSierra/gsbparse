from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse.account_sections._abstract_section import GsbFileSection


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
            Nb=int(element.attrib.get("Nb")),
            Na=element.attrib.get("Na"),
            Co=element.attrib.get("Co"),
            BIC=element.attrib.get("BIC"),
            Adr=element.attrib.get("Adr"),
            Tel=element.attrib.get("Tel"),
            Mail=element.attrib.get("Mail"),
            Web=element.attrib.get("Web"),
            Nac=element.attrib.get("Nac"),
            Faxc=element.attrib.get("Faxc"),
            Telc=element.attrib.get("Telc"),
            Mailc=element.attrib.get("Mailc"),
            Rem=element.attrib.get("Rem"),
        )
