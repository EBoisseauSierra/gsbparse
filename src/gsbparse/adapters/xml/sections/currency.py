"""XML adapter: parse a ``<Currency>`` element into a ``Currency``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int, parse_str
from gsbparse.domain.sections.currency import Currency


def parse_currency_section(element: ET.Element) -> Currency:
    """Parse a ``<Currency>`` XML element into a :class:`Currency`.

    Args:
        element: The ``<Currency>`` XML element.

    Returns:
        A fully populated :class:`Currency`.
    """
    return Currency(
        Nb=parse_int(element.attrib["Nb"]),
        Na=parse_str(element.attrib["Na"]),
        Co=parse_str(element.attrib["Co"]),
        Ico=parse_str(element.attrib["Ico"]),
        Fl=parse_int(element.attrib["Fl"]),
    )
