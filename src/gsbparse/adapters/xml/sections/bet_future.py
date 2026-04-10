"""XML adapter: parse a ``<Bet_future>`` element into a ``BetFutureSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import (
    parse_amount,
    parse_bool,
    parse_date,
    parse_int,
    parse_null,
    parse_nullable_str,
)
from gsbparse.domain.sections.bet_future import BetFutureSection

_parse_nullable_date = parse_null(parse_date)


def parse_bet_future_section(element: ET.Element) -> BetFutureSection:
    """Parse a ``<Bet_future>`` XML element into a :class:`BetFutureSection`.

    Args:
        element: The ``<Bet_future>`` XML element.

    Returns:
        A fully populated :class:`BetFutureSection`.
    """
    a = element.attrib
    return BetFutureSection(
        Nb=parse_int(a["Nb"]),
        Dt=parse_date(a["Dt"]),
        Ac=parse_int(a["Ac"]),
        Am=parse_amount(a["Am"]),
        Pa=parse_int(a["Pa"]),
        IsT=parse_bool(a["IsT"]),
        Tra=parse_int(a["Tra"]),
        Ca=parse_int(a["Ca"]),
        Sca=parse_int(a["Sca"]),
        Pn=parse_int(a["Pn"]),
        Fi=parse_int(a["Fi"]),
        Bu=parse_int(a["Bu"]),
        Sbu=parse_int(a["Sbu"]),
        No=parse_nullable_str(a["No"]),
        Au=parse_bool(a["Au"]),
        Pe=parse_int(a["Pe"]),
        Pei=parse_int(a["Pei"]),
        Pep=parse_int(a["Pep"]),
        Dtl=_parse_nullable_date(a["Dtl"]),
        Mo=parse_int(a["Mo"]),
    )
