"""XML adapter: parse a ``<Financial_year>`` element into a ``FinancialYear``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_bool, parse_date, parse_int, parse_null, parse_str
from gsbparse.domain.sections.financial_year import FinancialYear

_parse_nullable_date = parse_null(parse_date)


def parse_financial_year_section(element: ET.Element) -> FinancialYear:
    """Parse a ``<Financial_year>`` XML element into a :class:`FinancialYear`.

    Args:
        element: The ``<Financial_year>`` XML element.

    Returns:
        A fully populated :class:`FinancialYear`.
    """
    a = element.attrib
    return FinancialYear(
        Nb=parse_int(a["Nb"]),
        Na=parse_str(a["Na"]),
        Bdte=_parse_nullable_date(a["Bdte"]),
        Edte=_parse_nullable_date(a["Edte"]),
        Sho=parse_bool(a["Sho"]),
    )
