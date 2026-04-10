"""XML adapter: parse a ``<Financial_year>`` element into a ``FinancialYearSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_bool, parse_date, parse_int, parse_str
from gsbparse.domain.sections.financial_year import FinancialYearSection


def parse_financial_year_section(element: ET.Element) -> FinancialYearSection:
    """Parse a ``<Financial_year>`` XML element into a :class:`FinancialYearSection`.

    Args:
        element: The ``<Financial_year>`` XML element.

    Returns:
        A fully populated :class:`FinancialYearSection`.
    """
    a = element.attrib
    return FinancialYearSection(
        Nb=parse_int(a["Nb"]),
        Na=parse_str(a["Na"]),
        Bdte=parse_date(a["Bdte"]),
        Edte=parse_date(a["Edte"]),
        Sho=parse_bool(a["Sho"]),
    )
