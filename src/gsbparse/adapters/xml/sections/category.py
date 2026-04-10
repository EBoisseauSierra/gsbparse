"""XML adapter: parse a ``<Category>`` element into a ``CategorySection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int
from gsbparse.domain.sections.category import CategorySection


def parse_category_section(element: ET.Element) -> CategorySection:
    """Parse a ``<Category>`` XML element into a :class:`CategorySection`.

    Args:
        element: The ``<Category>`` XML element.

    Returns:
        A fully populated :class:`CategorySection`.
    """
    a = element.attrib
    return CategorySection(
        Nb=parse_int(a["Nb"]),
        Na=a["Na"],
        Kd=parse_int(a["Kd"]),
    )
