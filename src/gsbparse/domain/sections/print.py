"""Domain section: Print preferences."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class Print(GsbFileSection):
    """Print/report rendering preferences stored in the Grisbi file.

    Attributes:
        Draw_lines: Draw horizontal separator lines between rows.
        Draw_column: Draw vertical separator lines between columns.
        Draw_background: Draw alternating row backgrounds.
        Draw_archives: Include archived transactions in printouts.
        Draw_columns_name: Print column header names.
        Draw_title: Print a report title.
        Draw_interval_dates: Print the date interval covered.
        Draw_dates_are_value_dates: Use value dates instead of transaction dates.
        Font_transactions: Font descriptor for transaction rows.
        Font_title: Font descriptor for the report title.
        Report_font_transactions: Font descriptor for report transaction rows.
        Report_font_title: Font descriptor for report titles.
    """

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
