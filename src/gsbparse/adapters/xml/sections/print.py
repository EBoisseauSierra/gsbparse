"""XML adapter: parse a ``<Print>`` element into a ``Print``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_bool, parse_str
from gsbparse.domain.sections.print import Print


def parse_print_section(element: ET.Element) -> Print:
    """Parse a ``<Print>`` XML element into a :class:`Print`.

    Args:
        element: The ``<Print>`` XML element.

    Returns:
        A fully populated :class:`Print`.
    """
    a = element.attrib
    return Print(
        Draw_lines=parse_bool(a["Draw_lines"]),
        Draw_column=parse_bool(a["Draw_column"]),
        Draw_background=parse_bool(a["Draw_background"]),
        Draw_archives=parse_bool(a["Draw_archives"]),
        Draw_columns_name=parse_bool(a["Draw_columns_name"]),
        Draw_title=parse_bool(a["Draw_title"]),
        Draw_interval_dates=parse_bool(a["Draw_interval_dates"]),
        Draw_dates_are_value_dates=parse_bool(a["Draw_dates_are_value_dates"]),
        Font_transactions=parse_str(a["Font_transactions"]),
        Font_title=parse_str(a["Font_title"]),
        Report_font_transactions=parse_str(a["Report_font_transactions"]),
        Report_font_title=parse_str(a["Report_font_title"]),
    )
