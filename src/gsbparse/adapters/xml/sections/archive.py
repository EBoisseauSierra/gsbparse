"""XML adapter: parse an ``<Archive>`` element into an ``Archive``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import (
    parse_date,
    parse_int,
    parse_null,
    parse_nullable_str,
    parse_str,
)
from gsbparse.domain.sections.archive import Archive

_parse_nullable_date = parse_null(parse_date)


def parse_archive_section(element: ET.Element) -> Archive:
    """Parse an ``<Archive>`` XML element into an :class:`Archive`.

    Args:
        element: The ``<Archive>`` XML element.

    Returns:
        A fully populated :class:`Archive`.
    """
    a = element.attrib
    return Archive(
        Nb=parse_int(a["Nb"]),
        Na=parse_str(a["Na"]),
        Bdte=_parse_nullable_date(a["Bdte"]),
        Edte=_parse_nullable_date(a["Edte"]),
        Fye=parse_int(a["Fye"]),
        Rep=parse_nullable_str(a["Rep"]),
    )
