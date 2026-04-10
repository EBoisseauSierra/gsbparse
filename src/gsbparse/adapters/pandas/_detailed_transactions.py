"""Pandas adapter: convert a list of DetailedTransaction instances to a DataFrame."""

from __future__ import annotations

import pandas as pd

from gsbparse.domain.detailed_transaction import (
    DEFAULT_DETAILED_TRANSACTION_COLUMNS,
    DetailedTransaction,
    DetailedTransactionColumn,
    validate_columns,
)


def detailed_transactions_to_df(
    transactions: list[DetailedTransaction],
    columns: list[DetailedTransactionColumn] | None = None,
) -> pd.DataFrame:
    """Convert detailed transactions to a :class:`pd.DataFrame`.

    Each :class:`~gsbparse.domain.detailed_transaction.DetailedTransactionColumn`
    spec is projected via its dotted ``path`` onto each transaction and placed
    in the output column named by ``output_name``.

    A ``None`` value at any step of a dotted path (e.g. ``Pa.Na`` when the
    transaction has no party) resolves to ``None`` in the output cell.

    Args:
        transactions: List of :class:`~gsbparse.domain.detailed_transaction.DetailedTransaction`
            instances to convert.
        columns: Column projection specs. Defaults to
            :data:`~gsbparse.domain.detailed_transaction.DEFAULT_DETAILED_TRANSACTION_COLUMNS`.

    Returns:
        A :class:`pd.DataFrame` with one row per transaction and one column
        per spec entry.

    Raises:
        UnknownDetailedTransactionPathError: A column spec references a
            non-existent attribute path (raised at validation time, before
            the DataFrame is built).
        ValueError: *transactions* is empty.
    """
    if not transactions:
        raise ValueError("detailed_transactions_to_df requires a non-empty list")

    cols = columns if columns is not None else DEFAULT_DETAILED_TRANSACTION_COLUMNS
    validate_columns(cols)

    rows = []
    for tx in transactions:
        row: dict[str, object] = {}
        for col in cols:
            row[col.output_name] = _resolve_nullable_path(tx, col.path)
        rows.append(row)

    return pd.DataFrame(rows)


def _resolve_nullable_path(tx: DetailedTransaction, path: str) -> object:
    """Walk *path* on *tx*, returning ``None`` at the first missing step."""
    obj: object = tx
    for attr in path.split("."):
        if obj is None:
            return None
        obj = getattr(obj, attr)
    return obj
