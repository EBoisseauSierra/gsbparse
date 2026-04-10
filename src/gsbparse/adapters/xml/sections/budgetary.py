"""XML adapter: parse a ``<Budgetary>`` element into a ``BudgetarySection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int
from gsbparse.domain.sections.budgetary import BudgetarySection


def parse_budgetary_section(element: ET.Element) -> BudgetarySection:
    """Parse a ``<Budgetary>`` XML element into a :class:`BudgetarySection`.

    Args:
        element: The ``<Budgetary>`` XML element.

    Returns:
        A fully populated :class:`BudgetarySection`.
    """
    a = element.attrib
    return BudgetarySection(
        Nb=parse_int(a["Nb"]),
        Na=a["Na"],
        Kd=parse_int(a["Kd"]),
    )
