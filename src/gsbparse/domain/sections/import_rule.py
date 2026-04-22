"""Domain section: Import rule."""

from dataclasses import dataclass

from gsbparse.domain.sections._base import GsbFileSection


@dataclass(frozen=True)
class ImportRule(GsbFileSection):
    """An import rule for automatic transaction import.

    Attributes:
        Nb: Rule number.
        Na: Rule name.
        Acc: Account number concerned.
        Cur: Currency identifier for the rule.
        Inv: Invert the transaction amount.
        Enc: Character encoding of the import file.
        Fil: Last file used.
        Act: Action (import or mark transactions).
        Typ: File type (``"OFX"``, ``"CSV"``, ``"QIF"``).
        IdC: Column index of the account name (1-based).
        IdR: Row index of the account name (1-based).
        FiS: Grisbi field-to-column mapping string.
        Fld: First data row (including header row if present, 1-based).
        Hp: Header row present (1 = yes).
        Sep: CSV field separator.
        SkiS: Skip-lines specification string.
        SpL: Number of special lines in the rule.
    """

    Nb: int
    Na: str
    Acc: int
    Cur: int
    Inv: bool
    Enc: str
    Fil: str
    Act: int
    Typ: str
    IdC: int
    IdR: int
    FiS: str
    Fld: int
    Hp: bool
    Sep: str
    SkiS: str
    SpL: int
