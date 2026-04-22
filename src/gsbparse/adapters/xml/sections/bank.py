"""XML adapter: parse a ``<Bank>`` element into a ``Bank``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_int, parse_nullable_str, parse_str
from gsbparse.domain.sections.bank import Bank


def parse_bank_section(element: ET.Element) -> Bank:
    """Parse a ``<Bank>`` XML element into a :class:`Bank`.

    Args:
        element: The ``<Bank>`` XML element.

    Returns:
        A fully populated :class:`Bank`.
    """
    a = element.attrib
    return Bank(
        Nb=parse_int(a["Nb"]),
        Na=parse_str(a["Na"]),
        Co=parse_str(a["Co"]),
        BIC=parse_str(a["BIC"]),
        Adr=parse_str(a["Adr"]),
        Tel=parse_str(a["Tel"]),
        Mail=parse_nullable_str(a["Mail"]),
        Web=parse_nullable_str(a["Web"]),
        Nac=parse_str(a["Nac"]),
        Faxc=parse_str(a["Faxc"]),
        Telc=parse_str(a["Telc"]),
        Mailc=parse_str(a["Mailc"]),
        Rem=parse_nullable_str(a["Rem"]),
    )
