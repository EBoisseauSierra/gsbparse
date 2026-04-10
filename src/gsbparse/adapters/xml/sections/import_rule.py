"""XML adapter: parse an ``<Import_rule>`` element into an ``ImportRuleSection``."""

import xml.etree.ElementTree as ET

from gsbparse.adapters.xml.parsers import parse_bool, parse_int, parse_str
from gsbparse.domain.sections.import_rule import ImportRuleSection


def parse_import_rule_section(element: ET.Element) -> ImportRuleSection:
    """Parse an ``<Import_rule>`` XML element into an :class:`ImportRuleSection`.

    Args:
        element: The ``<Import_rule>`` XML element.

    Returns:
        A fully populated :class:`ImportRuleSection`.
    """
    a = element.attrib
    return ImportRuleSection(
        Nb=parse_int(a["Nb"]),
        Na=parse_str(a["Na"]),
        Acc=parse_int(a["Acc"]),
        Cur=parse_int(a["Cur"]),
        Inv=parse_bool(a["Inv"]),
        Enc=parse_str(a["Enc"]),
        Fil=parse_str(a["Fil"]),
        Act=parse_int(a["Act"]),
        Typ=parse_str(a["Typ"]),
        IdC=parse_int(a["IdC"]),
        IdR=parse_int(a["IdR"]),
        FiS=parse_str(a["FiS"]),
        Fld=parse_int(a["Fld"]),
        Hp=parse_bool(a["Hp"]),
        Sep=parse_str(a["Sep"]),
        SkiS=parse_str(a["SkiS"]),
        SpL=parse_int(a["SpL"]),
    )
