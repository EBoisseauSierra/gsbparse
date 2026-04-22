"""XML adapter: parse a ``<Party>`` element into a ``Party``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_bool, parse_int, parse_nullable_str
from gsbparse.domain.sections.party import Party


def parse_party_section(element: ET.Element) -> Party:
    """Parse a ``<Party>`` XML element into a :class:`Party`.

    Args:
        element: The ``<Party>`` XML element.

    Returns:
        A fully populated :class:`Party`.
    """
    a = element.attrib
    return Party(
        Nb=parse_int(a["Nb"]),
        Na=a["Na"],
        Txt=parse_nullable_str(a["Txt"]),
        Search=parse_nullable_str(a["Search"]),
        IgnCase=parse_bool(a["IgnCase"]),
        UseRegex=parse_bool(a["UseRegex"]),
    )
