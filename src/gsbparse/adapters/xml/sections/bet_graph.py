"""XML adapter: parse a ``<Bet_graph>`` element into a ``BetGraph``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_str
from gsbparse.domain.sections.bet_graph import BetGraph


def parse_bet_graph_section(element: ET.Element) -> BetGraph:
    """Parse a ``<Bet_graph>`` XML element into a :class:`BetGraph`.

    Args:
        element: The ``<Bet_graph>`` XML element.

    Returns:
        A fully populated :class:`BetGraph`.
    """
    return BetGraph(prefs=parse_str(element.attrib["prefs"]))
