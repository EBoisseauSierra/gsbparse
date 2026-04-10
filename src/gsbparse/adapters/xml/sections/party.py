"""XML adapter: parse a ``<Party>`` element into a ``PartySection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_bool, parse_int, parse_nullable_str
from gsbparse.domain.sections.party import PartySection


def parse_party_section(element: ET.Element) -> PartySection:
    """Parse a ``<Party>`` XML element into a :class:`PartySection`.

    Args:
        element: The ``<Party>`` XML element.

    Returns:
        A fully populated :class:`PartySection`.
    """
    a = element.attrib
    return PartySection(
        Nb=parse_int(a["Nb"]),
        Na=a["Na"],
        Txt=parse_nullable_str(a["Txt"]),
        Search=parse_nullable_str(a["Search"]),
        IgnCase=parse_bool(a["IgnCase"]),
        UseRegex=parse_bool(a["UseRegex"]),
    )
