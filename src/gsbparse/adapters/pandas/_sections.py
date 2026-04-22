"""Pandas adapter: convert a list of GsbFileSection instances to a DataFrame."""

from __future__ import annotations

import dataclasses
from datetime import datetime as _datetime

import pandas as pd

from gsbparse.domain.errors import MixedSectionsError
from gsbparse.domain.sections._base import GsbFileSection


def sections_to_df(sections: list[GsbFileSection]) -> pd.DataFrame:
    """Convert a list of section dataclass instances to a :class:`pd.DataFrame`.

    Each dataclass field becomes a column; the column names are the field names
    (i.e. Grisbi attribute codes such as ``Nb``, ``Na``, ``Co``).

    Args:
        sections: A non-empty list of section instances. All elements must be
            the same concrete type.

    Returns:
        A :class:`pd.DataFrame` with one row per section.

    Raises:
        MixedSectionsError: The list contains more than one concrete section type.
        ValueError: The list is empty.
    """
    if not sections:
        raise ValueError("sections_to_df requires a non-empty list")

    types = {type(s) for s in sections}
    if len(types) > 1:
        raise MixedSectionsError(list(types))

    return pd.DataFrame([_section_to_row(s) for s in sections])


def _section_to_row(section: GsbFileSection) -> dict[str, object]:
    """Serialize *section* to a plain dict, normalizing ``datetime`` → ``date``."""
    row: dict[str, object] = {}
    for field in dataclasses.fields(section):
        val = getattr(section, field.name)
        row[field.name] = val.date() if isinstance(val, _datetime) else val
    return row
