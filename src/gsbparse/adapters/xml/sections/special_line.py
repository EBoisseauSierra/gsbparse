"""XML adapter: parse a ``<Special_line>`` element into a ``SpecialLine``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int, parse_str
from gsbparse.domain.sections.special_line import SpecialLine, SpecialLineAction


def parse_special_line_section(element: ET.Element) -> SpecialLine:
    """Parse a ``<Special_line>`` XML element into a :class:`SpecialLine`.

    Args:
        element: The ``<Special_line>`` XML element.

    Returns:
        A fully populated :class:`SpecialLine`.
    """
    a = element.attrib
    return SpecialLine(
        Nb=parse_int(a["Nb"]),
        NuR=parse_int(a["NuR"]),
        SpA=SpecialLineAction(parse_int(a["SpA"])),
        SpAD=parse_int(a["SpAD"]),
        SpUD=parse_int(a["SpUD"]),
        SpUT=parse_str(a["SpUT"]),
    )
