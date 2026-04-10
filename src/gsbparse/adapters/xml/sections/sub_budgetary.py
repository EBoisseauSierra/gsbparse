"""XML adapter: parse a ``<Sub_budgetary>`` element into a ``SubBudgetarySection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int
from gsbparse.domain.sections.sub_budgetary import SubBudgetarySection


def parse_sub_budgetary_section(element: ET.Element) -> SubBudgetarySection:
    """Parse a ``<Sub_budgetary>`` XML element into a :class:`SubBudgetarySection`.

    Args:
        element: The ``<Sub_budgetary>`` XML element.

    Returns:
        A fully populated :class:`SubBudgetarySection`.
    """
    a = element.attrib
    return SubBudgetarySection(
        Nbb=parse_int(a["Nbb"]),
        Nb=parse_int(a["Nb"]),
        Na=a["Na"],
    )
