"""XML adapter: parse an ``<Archive>`` element into an ``ArchiveSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import (
    parse_date,
    parse_int,
    parse_null,
    parse_nullable_str,
    parse_str,
)
from gsbparse.domain.sections.archive import ArchiveSection

_parse_nullable_date = parse_null(parse_date)


def parse_archive_section(element: ET.Element) -> ArchiveSection:
    """Parse an ``<Archive>`` XML element into an :class:`ArchiveSection`.

    Args:
        element: The ``<Archive>`` XML element.

    Returns:
        A fully populated :class:`ArchiveSection`.
    """
    a = element.attrib
    return ArchiveSection(
        Nb=parse_int(a["Nb"]),
        Na=parse_str(a["Na"]),
        Bdte=_parse_nullable_date(a["Bdte"]),
        Edte=_parse_nullable_date(a["Edte"]),
        Fye=parse_int(a["Fye"]),
        Rep=parse_nullable_str(a["Rep"]),
    )
