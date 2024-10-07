from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class RGBASection(GsbFileSection):
    Background_color_0: str
    Background_color_1: str
    Couleur_jour: str
    Background_scheduled: str
    Background_archive: str
    Selection: str
    Background_split: str
    Text_color_0: str
    Text_color_1: str
    Couleur_bet_division: str
    Couleur_bet_future: str
    Couleur_bet_solde: str
    Couleur_bet_transfert: str

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Background_color_0=element.attrib.get("Background_color_0"),
            Background_color_1=element.attrib.get("Background_color_1"),
            Couleur_jour=element.attrib.get("Couleur_jour"),
            Background_scheduled=element.attrib.get("Background_scheduled"),
            Background_archive=element.attrib.get("Background_archive"),
            Selection=element.attrib.get("Selection"),
            Background_split=element.attrib.get("Background_split"),
            Text_color_0=element.attrib.get("Text_color_0"),
            Text_color_1=element.attrib.get("Text_color_1"),
            Couleur_bet_division=element.attrib.get("Couleur_bet_division"),
            Couleur_bet_future=element.attrib.get("Couleur_bet_future"),
            Couleur_bet_solde=element.attrib.get("Couleur_bet_solde"),
            Couleur_bet_transfert=element.attrib.get("Couleur_bet_transfert"),
        )
