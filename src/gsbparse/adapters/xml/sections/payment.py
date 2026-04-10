"""XML adapter: parse a ``<Payment>`` element into a ``PaymentSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_bool, parse_int, parse_null, parse_str
from gsbparse.domain.sections.payment import PaymentSection

_parse_nullable_int = parse_null(parse_int)


def parse_payment_section(element: ET.Element) -> PaymentSection:
    """Parse a ``<Payment>`` XML element into a :class:`PaymentSection`.

    Args:
        element: The ``<Payment>`` XML element.

    Returns:
        A fully populated :class:`PaymentSection`.
    """
    a = element.attrib
    return PaymentSection(
        Number=parse_int(a["Number"]),
        Name=parse_str(a["Name"]),
        Sign=parse_int(a["Sign"]),
        Show_entry=parse_bool(a["Show_entry"]),
        Automatic_number=parse_bool(a["Automatic_number"]),
        Current_number=_parse_nullable_int(a["Current_number"]),
        Account=parse_int(a["Account"]),
    )
