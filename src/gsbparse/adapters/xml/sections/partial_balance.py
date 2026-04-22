"""XML adapter: parse a ``<Partial_balance>`` element into a ``PartialBalance``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_bool, parse_int, parse_str
from gsbparse.domain.sections.partial_balance import PartialBalance


def parse_partial_balance_section(element: ET.Element) -> PartialBalance:
    """Parse a ``<Partial_balance>`` XML element into a :class:`PartialBalance`.

    Args:
        element: The ``<Partial_balance>`` XML element.

    Returns:
        A fully populated :class:`PartialBalance`.
    """
    a = element.attrib
    return PartialBalance(
        Nb=parse_int(a["Nb"]),
        Na=parse_str(a["Na"]),
        Acc=parse_str(a["Acc"]),
        Kind=parse_int(a["Kind"]),
        Currency=parse_int(a["Currency"]),
        Colorise=parse_bool(a["Colorise"]),
    )
