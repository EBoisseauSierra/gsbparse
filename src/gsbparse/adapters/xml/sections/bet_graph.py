"""XML adapter: parse a ``<Bet_graph>`` element into a ``BetGraphSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_str
from gsbparse.domain.sections.bet_graph import BetGraphSection


def parse_bet_graph_section(element: ET.Element) -> BetGraphSection:
    """Parse a ``<Bet_graph>`` XML element into a :class:`BetGraphSection`.

    Args:
        element: The ``<Bet_graph>`` XML element.

    Returns:
        A fully populated :class:`BetGraphSection`.
    """
    return BetGraphSection(prefs=parse_str(element.attrib["prefs"]))
