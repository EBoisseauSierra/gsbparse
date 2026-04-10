"""XML adapter: parse a ``<Scheduled>`` element into a ``ScheduledSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import (
    parse_amount,
    parse_bool,
    parse_date,
    parse_int,
    parse_null,
    parse_nullable_str,
)
from gsbparse.domain.sections.scheduled import ScheduledSection

_parse_nullable_date = parse_null(parse_date)


def parse_scheduled_section(element: ET.Element) -> ScheduledSection:
    """Parse a ``<Scheduled>`` XML element into a :class:`ScheduledSection`.

    Args:
        element: The ``<Scheduled>`` XML element.

    Returns:
        A fully populated :class:`ScheduledSection`.
    """
    a = element.attrib
    return ScheduledSection(
        Nb=parse_int(a["Nb"]),
        Dt=parse_date(a["Dt"]),
        Ac=parse_int(a["Ac"]),
        Am=parse_amount(a["Am"]),
        Cu=parse_int(a["Cu"]),
        Pa=parse_int(a["Pa"]),
        Ca=parse_int(a["Ca"]),
        Sca=parse_int(a["Sca"]),
        Tra=parse_int(a["Tra"]),
        Pn=parse_int(a["Pn"]),
        CPn=parse_int(a["CPn"]),
        Pc=parse_nullable_str(a["Pc"]),
        Fi=parse_int(a["Fi"]),
        Bu=parse_int(a["Bu"]),
        Sbu=parse_int(a["Sbu"]),
        No=parse_nullable_str(a["No"]),
        Au=parse_bool(a["Au"]),
        Fd=parse_int(a["Fd"]),
        Pe=parse_int(a["Pe"]),
        Pei=parse_int(a["Pei"]),
        Pep=parse_int(a["Pep"]),
        Dtl=_parse_nullable_date(a["Dtl"]),
        Br=parse_bool(a["Br"]),
        Mo=parse_int(a["Mo"]),
    )
