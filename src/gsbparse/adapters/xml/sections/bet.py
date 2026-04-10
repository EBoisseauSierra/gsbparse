"""XML adapter: parse a ``<Bet>`` element into a ``BetSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int
from gsbparse.domain.sections.bet import BetSection


def parse_bet_section(element: ET.Element) -> BetSection:
    """Parse a ``<Bet>`` XML element into a :class:`BetSection`.

    Args:
        element: The ``<Bet>`` XML element.

    Returns:
        A fully populated :class:`BetSection`.
    """
    a = element.attrib
    return BetSection(
        Ddte=parse_int(a["Ddte"]),
        Bet_deb_cash_account_option=parse_int(a["Bet_deb_cash_account_option"]),
    )
