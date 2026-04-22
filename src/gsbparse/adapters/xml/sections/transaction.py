"""XML adapter: parse a ``<Transaction>`` element into a ``Transaction``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import (
    parse_amount,
    parse_bool,
    parse_date,
    parse_int,
    parse_null,
    parse_nullable_str,
)
from gsbparse.domain.sections.transaction import Transaction, TransactionMarkedState

_parse_nullable_date = parse_null(parse_date)


def parse_transaction_section(element: ET.Element) -> Transaction:
    """Parse a ``<Transaction>`` XML element into a :class:`Transaction`.

    Args:
        element: The ``<Transaction>`` XML element.

    Returns:
        A fully populated :class:`Transaction`.
    """
    a = element.attrib
    return Transaction(
        Ac=parse_int(a["Ac"]),
        Nb=parse_int(a["Nb"]),
        Id=parse_nullable_str(a["Id"]),
        Dt=_parse_nullable_date(a["Dt"]),
        Dv=_parse_nullable_date(a["Dv"]),
        Am=parse_amount(a["Am"]),
        Cu=parse_int(a["Cu"]),
        Exb=parse_bool(a["Exb"]),
        Exr=parse_amount(a["Exr"]),
        Exf=parse_amount(a["Exf"]),
        Pa=parse_int(a["Pa"]),
        Ca=parse_int(a["Ca"]),
        Sca=parse_int(a["Sca"]),
        Br=parse_bool(a["Br"]),
        No=parse_nullable_str(a["No"]),
        Pn=parse_int(a["Pn"]),
        Pc=parse_nullable_str(a["Pc"]),
        Ma=TransactionMarkedState(parse_int(a["Ma"])),
        Ar=parse_int(a["Ar"]),
        Au=parse_bool(a["Au"]),
        Re=parse_int(a["Re"]),
        Fi=parse_int(a["Fi"]),
        Bu=parse_int(a["Bu"]),
        Sbu=parse_int(a["Sbu"]),
        Vo=parse_nullable_str(a["Vo"]),
        Ba=parse_nullable_str(a["Ba"]),
        Trt=parse_int(a["Trt"]),
        Mo=parse_int(a["Mo"]),
    )
