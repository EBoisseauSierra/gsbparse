"""XML adapter: parse a ``<Currency_link>`` element into a ``CurrencyLinkSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_amount, parse_bool, parse_int
from gsbparse.domain.sections.currency_link import CurrencyLinkSection


def parse_currency_link_section(element: ET.Element) -> CurrencyLinkSection:
    """Parse a ``<Currency_link>`` XML element into a :class:`CurrencyLinkSection`.

    Args:
        element: The ``<Currency_link>`` XML element.

    Returns:
        A fully populated :class:`CurrencyLinkSection`.
    """
    a = element.attrib
    return CurrencyLinkSection(
        Nb=parse_int(a["Nb"]),
        Cu1=parse_int(a["Cu1"]),
        Cu2=parse_int(a["Cu2"]),
        Ex=parse_amount(a["Ex"]),
        Fl=parse_bool(a["Fl"]),
    )
