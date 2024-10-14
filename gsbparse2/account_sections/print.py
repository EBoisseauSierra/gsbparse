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
            Draw_lines=cls.parse_bool(element.attrib.get("Draw_lines")),
            Draw_column=cls.parse_bool(element.attrib.get("Draw_column")),
            Draw_background=cls.parse_bool(element.attrib.get("Draw_background")),
            Draw_archives=cls.parse_bool(element.attrib.get("Draw_archives")),
            Draw_columns_name=cls.parse_bool(element.attrib.get("Draw_columns_name")),
            Draw_title=cls.parse_bool(element.attrib.get("Draw_title")),
            Draw_interval_dates=cls.parse_bool(
                element.attrib.get("Draw_interval_dates"),
            ),
            Draw_dates_are_value_dates=cls.parse_bool(
                element.attrib.get("Draw_dates_are_value_dates"),
            ),
            Font_transactions=cls.parse_str(element.attrib.get("Font_transactions")),
            Font_title=cls.parse_str(element.attrib.get("Font_title")),
            Report_font_transactions=cls.parse_str(
                element.attrib.get("Report_font_transactions")
            ),
            Report_font_title=cls.parse_str(element.attrib.get("Report_font_title")),
        )
