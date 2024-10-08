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
            Nb=int(element.attrib["Nb"]),
            Na=element.attrib["Na"],
            Co=element.attrib["Co"],
            BIC=element.attrib["BIC"],
            Adr=element.attrib["Adr"],
            Tel=element.attrib["Tel"],
            Mail=element.attrib["Mail"],
            Web=element.attrib["Web"],
            Nac=element.attrib["Nac"],
            Faxc=element.attrib["Faxc"],
            Telc=element.attrib["Telc"],
            Mailc=element.attrib["Mailc"],
            Rem=element.attrib["Rem"],
        )
