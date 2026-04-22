"""Domain section: Text comparison (filter rule attached to a report)."""

from dataclasses import dataclass
from decimal import Decimal

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class TextComparison(GsbFileSection):
    """A text-comparison filter rule attached to a report.

    Attributes:
        Comparison_number: Index within the report (1-based).
        Report_nb: Parent report identifier.
        Last_comparison: Last comparison index (-1 = none).
        Object: Object type to compare.
        Operator: Comparison operator.
        Text: Text to match.
        Use_text: Apply this text comparison.
        Comparison_1: First comparison operand.
        Link_1_2: Logical link between comparison operands.
        Comparison_2: Second comparison operand.
        Amount_1: First amount operand.
        Amount_2: Second amount operand.
    """

    Comparison_number: int
    Report_nb: int
    Last_comparison: int
    Object: int
    Operator: int
    Text: str
    Use_text: bool
    Comparison_1: int
    Link_1_2: int
    Comparison_2: int
    Amount_1: Decimal
    Amount_2: Decimal
