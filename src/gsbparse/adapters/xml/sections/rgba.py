"""XML adapter: parse an ``<RGBA>`` element into an ``RgbaSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_str
from gsbparse.domain.sections.rgba import RgbaSection


def parse_rgba_section(element: ET.Element) -> RgbaSection:
    """Parse an ``<RGBA>`` XML element into an :class:`RgbaSection`.

    Args:
        element: The ``<RGBA>`` XML element.

    Returns:
        A fully populated :class:`RgbaSection`.
    """
    a = element.attrib
    return RgbaSection(
        Background_color_0=parse_str(a["Background_color_0"]),
        Background_color_1=parse_str(a["Background_color_1"]),
        Couleur_jour=parse_str(a["Couleur_jour"]),
        Background_scheduled=parse_str(a["Background_scheduled"]),
        Background_archive=parse_str(a["Background_archive"]),
        Selection=parse_str(a["Selection"]),
        Background_split=parse_str(a["Background_split"]),
        Text_color_0=parse_str(a["Text_color_0"]),
        Text_color_1=parse_str(a["Text_color_1"]),
        Couleur_bet_division=parse_str(a["Couleur_bet_division"]),
        Couleur_bet_future=parse_str(a["Couleur_bet_future"]),
        Couleur_bet_solde=parse_str(a["Couleur_bet_solde"]),
        Couleur_bet_transfert=parse_str(a["Couleur_bet_transfert"]),
    )
