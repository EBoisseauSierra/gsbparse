"""XML adapter: parse a ``<Category>`` element into a ``Category``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int
from gsbparse.domain.sections.category import Category, CategoryKind


def parse_category_section(element: ET.Element) -> Category:
    """Parse a ``<Category>`` XML element into a :class:`Category`.

    Args:
        element: The ``<Category>`` XML element.

    Returns:
        A fully populated :class:`Category`.
    """
    a = element.attrib
    return Category(
        Nb=parse_int(a["Nb"]),
        Na=a["Na"],
        Kd=CategoryKind(parse_int(a["Kd"])),
    )
