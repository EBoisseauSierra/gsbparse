"""XML adapter: parse a ``<Sub_category>`` element into a ``SubCategory``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int
from gsbparse.domain.sections.sub_category import SubCategory


def parse_sub_category_section(element: ET.Element) -> SubCategory:
    """Parse a ``<Sub_category>`` XML element into a :class:`SubCategory`.

    Args:
        element: The ``<Sub_category>`` XML element.

    Returns:
        A fully populated :class:`SubCategory`.
    """
    a = element.attrib
    return SubCategory(
        Nbc=parse_int(a["Nbc"]),
        Nb=parse_int(a["Nb"]),
        Na=a["Na"],
    )
