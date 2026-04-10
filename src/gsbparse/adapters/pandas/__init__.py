"""Pandas adapter for gsbparse — converts domain objects to ``pd.DataFrame``."""

from __future__ import annotations

from typing import overload

import pandas as pd

from gsbparse.adapters.pandas._detailed_transactions import detailed_transactions_to_df
from gsbparse.adapters.pandas._sections import sections_to_df
from gsbparse.domain.detailed_transaction import DetailedTransaction, DetailedTransactionColumn
from gsbparse.domain.sections._base import GsbFileSection


@overload
def to_df(
    items: list[GsbFileSection],
    columns: None = ...,
) -> pd.DataFrame: ...


@overload
def to_df(
    items: list[DetailedTransaction],
    columns: list[DetailedTransactionColumn] | None = ...,
) -> pd.DataFrame: ...


def to_df(
    items: list[GsbFileSection] | list[DetailedTransaction],
    columns: list[DetailedTransactionColumn] | None = None,
) -> pd.DataFrame:
    """Convert a list of domain objects to a :class:`pd.DataFrame`.

    Dispatches on the element type of *items*:

    - ``list[GsbFileSection]`` — each dataclass field becomes a column;
      column names are Grisbi attribute codes (``Nb``, ``Na``, ...).
    - ``list[DetailedTransaction]`` — projected via *columns* specs;
      defaults to
      :data:`~gsbparse.domain.detailed_transaction.DEFAULT_DETAILED_TRANSACTION_COLUMNS`.

    Args:
        items: A non-empty list of :class:`~gsbparse.domain.sections._base.GsbFileSection`
            or :class:`~gsbparse.domain.detailed_transaction.DetailedTransaction` instances.
        columns: Column projection specs, only applicable for
            :class:`~gsbparse.domain.detailed_transaction.DetailedTransaction` input.
            Ignored (and must be ``None``) for section lists.

    Returns:
        A :class:`pd.DataFrame`.

    Raises:
        MixedSectionsError: A section list contains more than one concrete type.
        UnknownDetailedTransactionPathError: A column spec references a
            non-existent attribute path.
        ValueError: *items* is empty.
    """
    if not items:
        raise ValueError("to_df requires a non-empty list")

    if isinstance(items[0], DetailedTransaction):
        return detailed_transactions_to_df(
            items,  # type: ignore[arg-type]
            columns=columns,
        )

    return sections_to_df(items)  # type: ignore[arg-type]


__all__ = ["to_df"]
