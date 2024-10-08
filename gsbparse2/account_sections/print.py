from dataclasses import dataclass
from typing import Self
from xml.etree import ElementTree as ET

from gsbparse2.account_sections._abstract_section import GsbFileSection


@dataclass(frozen=True)
class PrintSection(GsbFileSection):
    Draw_lines: bool
    Draw_column: bool
    Draw_background: bool
    Draw_archives: bool
    Draw_columns_name: bool
    Draw_title: bool
    Draw_interval_dates: bool
    Draw_dates_are_value_dates: bool
    Font_transactions: str
    Font_title: str
    Report_font_transactions: str
    Report_font_title: str

    @classmethod
    def from_xml(cls, element: ET.Element) -> Self:
        return cls(
            Draw_lines=cls.parse_bool(element.attrib["Draw_lines"]),
            Draw_column=cls.parse_bool(element.attrib["Draw_column"]),
            Draw_background=cls.parse_bool(element.attrib["Draw_background"]),
            Draw_archives=cls.parse_bool(element.attrib["Draw_archives"]),
            Draw_columns_name=cls.parse_bool(element.attrib["Draw_columns_name"]),
            Draw_title=cls.parse_bool(element.attrib["Draw_title"]),
            Draw_interval_dates=cls.parse_bool(
                element.attrib["Draw_interval_dates"],
            ),
            Draw_dates_are_value_dates=cls.parse_bool(
                element.attrib["Draw_dates_are_value_dates"],
            ),
            Font_transactions=element.attrib["Font_transactions"],
            Font_title=element.attrib["Font_title"],
            Report_font_transactions=element.attrib["Report_font_transactions"],
            Report_font_title=element.attrib["Report_font_title"],
        )
