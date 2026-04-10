"""XML adapter: parse a ``<Sub_category>`` element into a ``SubCategorySection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int
from gsbparse.domain.sections.sub_category import SubCategorySection


def parse_sub_category_section(element: ET.Element) -> SubCategorySection:
    """Parse a ``<Sub_category>`` XML element into a :class:`SubCategorySection`.

    Args:
        element: The ``<Sub_category>`` XML element.

    Returns:
        A fully populated :class:`SubCategorySection`.
    """
    a = element.attrib
    return SubCategorySection(
        Nbc=parse_int(a["Nbc"]),
        Nb=parse_int(a["Nb"]),
        Na=a["Na"],
    )
