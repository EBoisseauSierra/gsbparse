"""XML adapter: parse a ``<Bet>`` element into a ``Bet``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int
from gsbparse.domain.sections.bet import Bet


def parse_bet_section(element: ET.Element) -> Bet:
    """Parse a ``<Bet>`` XML element into a :class:`Bet`.

    Args:
        element: The ``<Bet>`` XML element.

    Returns:
        A fully populated :class:`Bet`.
    """
    a = element.attrib
    return Bet(
        Ddte=parse_int(a["Ddte"]),
        Bet_deb_cash_account_option=parse_int(a["Bet_deb_cash_account_option"]),
    )
