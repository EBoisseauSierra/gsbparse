"""XML adapter: parse a ``<Text_comparison>`` element into a ``TextComparisonSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_amount, parse_bool, parse_int, parse_str
from gsbparse.domain.sections.text_comparison import TextComparisonSection


def parse_text_comparison_section(element: ET.Element) -> TextComparisonSection:
    """Parse a ``<Text_comparison>`` XML element into a :class:`TextComparisonSection`.

    Args:
        element: The ``<Text_comparison>`` XML element.

    Returns:
        A fully populated :class:`TextComparisonSection`.
    """
    a = element.attrib
    return TextComparisonSection(
        Comparison_number=parse_int(a["Comparison_number"]),
        Report_nb=parse_int(a["Report_nb"]),
        Last_comparison=parse_int(a["Last_comparison"]),
        Object=parse_int(a["Object"]),
        Operator=parse_int(a["Operator"]),
        Text=parse_str(a["Text"]),
        Use_text=parse_bool(a["Use_text"]),
        Comparison_1=parse_int(a["Comparison_1"]),
        Link_1_2=parse_int(a["Link_1_2"]),
        Comparison_2=parse_int(a["Comparison_2"]),
        Amount_1=parse_amount(a["Amount_1"]),
        Amount_2=parse_amount(a["Amount_2"]),
    )
