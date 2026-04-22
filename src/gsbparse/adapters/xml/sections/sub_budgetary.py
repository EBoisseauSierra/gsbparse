"""XML adapter: parse a ``<Sub_budgetary>`` element into a ``SubBudgetary``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int
from gsbparse.domain.sections.sub_budgetary import SubBudgetary


def parse_sub_budgetary_section(element: ET.Element) -> SubBudgetary:
    """Parse a ``<Sub_budgetary>`` XML element into a :class:`SubBudgetary`.

    Args:
        element: The ``<Sub_budgetary>`` XML element.

    Returns:
        A fully populated :class:`SubBudgetary`.
    """
    a = element.attrib
    return SubBudgetary(
        Nbb=parse_int(a["Nbb"]),
        Nb=parse_int(a["Nb"]),
        Na=a["Na"],
    )
