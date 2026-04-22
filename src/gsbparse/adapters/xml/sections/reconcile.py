"""XML adapter: parse a ``<Reconcile>`` element into a ``Reconcile``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_amount, parse_date, parse_int, parse_null, parse_str
from gsbparse.domain.sections.reconcile import Reconcile

_parse_nullable_date = parse_null(parse_date)


def parse_reconcile_section(element: ET.Element) -> Reconcile:
    """Parse a ``<Reconcile>`` XML element into a :class:`Reconcile`.

    Args:
        element: The ``<Reconcile>`` XML element.

    Returns:
        A fully populated :class:`Reconcile`.
    """
    a = element.attrib
    return Reconcile(
        Nb=parse_int(a["Nb"]),
        Na=parse_str(a["Na"]),
        Acc=parse_int(a["Acc"]),
        Idate=_parse_nullable_date(a["Idate"]),
        Fdate=_parse_nullable_date(a["Fdate"]),
        Ibal=parse_amount(a["Ibal"]),
        Fbal=parse_amount(a["Fbal"]),
    )
