"""XML adapter: parse a ``<Reconcile>`` element into a ``ReconcileSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_amount, parse_date, parse_int, parse_str
from gsbparse.domain.sections.reconcile import ReconcileSection


def parse_reconcile_section(element: ET.Element) -> ReconcileSection:
    """Parse a ``<Reconcile>`` XML element into a :class:`ReconcileSection`.

    Args:
        element: The ``<Reconcile>`` XML element.

    Returns:
        A fully populated :class:`ReconcileSection`.
    """
    a = element.attrib
    return ReconcileSection(
        Nb=parse_int(a["Nb"]),
        Na=parse_str(a["Na"]),
        Acc=parse_int(a["Acc"]),
        Idate=parse_date(a["Idate"]),
        Fdate=parse_date(a["Fdate"]),
        Ibal=parse_amount(a["Ibal"]),
        Fbal=parse_amount(a["Fbal"]),
    )
