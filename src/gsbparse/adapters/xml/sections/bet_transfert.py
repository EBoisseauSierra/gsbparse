"""XML adapter: parse a ``<Bet_transfert>`` element into a ``BetTransfert``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_bool, parse_date, parse_int, parse_null
from gsbparse.domain.sections.bet_transfert import BetTransfert, BetTransfertAccountType

_parse_nullable_date = parse_null(parse_date)


def parse_bet_transfert_section(element: ET.Element) -> BetTransfert:
    """Parse a ``<Bet_transfert>`` XML element into a :class:`BetTransfert`.

    Args:
        element: The ``<Bet_transfert>`` XML element.

    Returns:
        A fully populated :class:`BetTransfert`.
    """
    a = element.attrib
    return BetTransfert(
        Nb=parse_int(a["Nb"]),
        Dt=_parse_nullable_date(a["Dt"]),
        Ac=parse_int(a["Ac"]),
        Ty=BetTransfertAccountType(parse_int(a["Ty"])),
        Ra=parse_int(a["Ra"]),
        Rt=parse_bool(a["Rt"]),
        Dd=parse_bool(a["Dd"]),
        Dtb=_parse_nullable_date(a["Dtb"]),
        Mlbd=parse_bool(a["Mlbd"]),
        Pa=parse_int(a["Pa"]),
        Pn=parse_int(a["Pn"]),
        Ca=parse_int(a["Ca"]),
        Sca=parse_int(a["Sca"]),
        Bu=parse_int(a["Bu"]),
        Sbu=parse_int(a["Sbu"]),
        CPa=parse_int(a["CPa"]),
        CCa=parse_int(a["CCa"]),
        CSca=parse_int(a["CSca"]),
        CBu=parse_int(a["CBu"]),
        CSbu=parse_int(a["CSbu"]),
    )
