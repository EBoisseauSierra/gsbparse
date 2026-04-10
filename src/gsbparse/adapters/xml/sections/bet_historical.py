"""XML adapter: parse a ``<Bet_historical>`` element into a ``BetHistoricalSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_amount, parse_bool, parse_int
from gsbparse.domain.sections.bet_historical import BetHistoricalSection


def parse_bet_historical_section(element: ET.Element) -> BetHistoricalSection:
    """Parse a ``<Bet_historical>`` XML element into a :class:`BetHistoricalSection`.

    Args:
        element: The ``<Bet_historical>`` XML element.

    Returns:
        A fully populated :class:`BetHistoricalSection`.
    """
    a = element.attrib
    return BetHistoricalSection(
        Nb=parse_int(a["Nb"]),
        AC=parse_int(a["AC"]),
        Ori=parse_int(a["Ori"]),
        Div=parse_int(a["Div"]),
        Edit=parse_bool(a["Edit"]),
        Damount=parse_amount(a["Damount"]),
        SDiv=parse_int(a["SDiv"]),
        SEdit=parse_bool(a["SEdit"]),
        SDamount=parse_amount(a["SDamount"]),
    )
