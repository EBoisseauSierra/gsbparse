"""XML adapter: parse a ``<Bet_loan>`` element into a ``BetLoan``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import (
    parse_amount,
    parse_bool,
    parse_date,
    parse_int,
    parse_null,
)
from gsbparse.domain.sections.bet_loan import BetLoan

_parse_nullable_date = parse_null(parse_date)


def parse_bet_loan_section(element: ET.Element) -> BetLoan:
    """Parse a ``<Bet_loan>`` XML element into a :class:`BetLoan`.

    Args:
        element: The ``<Bet_loan>`` XML element.

    Returns:
        A fully populated :class:`BetLoan`.
    """
    a = element.attrib
    return BetLoan(
        Nb=parse_int(a["Nb"]),
        Ac=parse_int(a["Ac"]),
        Ver=parse_int(a["Ver"]),
        InCol=parse_bool(a["InCol"]),
        Ca=parse_amount(a["Ca"]),
        Duree=parse_int(a["Duree"]),
        FDate=_parse_nullable_date(a["FDate"]),
        Fees=parse_amount(a["Fees"]),
        Taux=parse_amount(a["Taux"]),
        TyTaux=parse_int(a["TyTaux"]),
        NbreDec=parse_int(a["NbreDec"]),
        FEchDif=parse_bool(a["FEchDif"]),
        FCa=parse_amount(a["FCa"]),
        FIn=parse_amount(a["FIn"]),
        OEch=parse_amount(a["OEch"]),
        ISchWL=parse_bool(a["ISchWL"]),
        AAc=parse_int(a["AAc"]),
        ASch=parse_int(a["ASch"]),
        AFr=parse_int(a["AFr"]),
        CaDu=parse_amount(a["CaDu"]),
    )
