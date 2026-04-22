"""XML adapter: parse an ``<Amount_comparison>`` element into an ``AmountComparison``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_amount, parse_int
from gsbparse.domain.sections.amount_comparison import AmountComparison


def parse_amount_comparison_section(element: ET.Element) -> AmountComparison:
    """Parse an ``<Amount_comparison>`` XML element into an :class:`AmountComparison`.

    Args:
        element: The ``<Amount_comparison>`` XML element.

    Returns:
        A fully populated :class:`AmountComparison`.
    """
    a = element.attrib
    return AmountComparison(
        Comparison_number=parse_int(a["Comparison_number"]),
        Report_nb=parse_int(a["Report_nb"]),
        Last_comparison=parse_int(a["Last_comparison"]),
        Comparison_1=parse_int(a["Comparison_1"]),
        Link_1_2=parse_int(a["Link_1_2"]),
        Comparison_2=parse_int(a["Comparison_2"]),
        Amount_1=parse_amount(a["Amount_1"]),
        Amount_2=parse_amount(a["Amount_2"]),
    )
