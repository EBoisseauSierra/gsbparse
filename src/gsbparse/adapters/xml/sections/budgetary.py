"""XML adapter: parse a ``<Budgetary>`` element into a ``Budgetary``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int
from gsbparse.domain.sections.budgetary import Budgetary
from gsbparse.domain.sections.category import CategoryKind


def parse_budgetary_section(element: ET.Element) -> Budgetary:
    """Parse a ``<Budgetary>`` XML element into a :class:`Budgetary`.

    Args:
        element: The ``<Budgetary>`` XML element.

    Returns:
        A fully populated :class:`Budgetary`.
    """
    a = element.attrib
    return Budgetary(
        Nb=parse_int(a["Nb"]),
        Na=a["Na"],
        Kd=CategoryKind(parse_int(a["Kd"])),
    )
