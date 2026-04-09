"""XML parsing helpers for Grisbi attribute values.

All helpers accept a raw string (the XML attribute value) and return a typed
Python value.  They encode Grisbi's XML conventions:

- ``"(null)"`` sentinel → ``None`` (via :func:`parse_null` decorator).
- Booleans are ``"0"`` / ``"1"`` strings.
- Amounts use a comma as the decimal separator (e.g. ``"42,50"``).
- Dates use ``%m/%d/%Y`` format in the format spec but the example file
  shows ``%d/%m/%Y`` — the adapter detects which format to use by trying
  both.
- ``"(null)"`` for optional fields that may be absent.

The :func:`parse_optional` wrapper swallows :class:`~gsbparse.domain.errors.XmlParsingError`
when a field is marked optional.
"""

import functools
import logging
from collections.abc import Callable
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import TypeVar

from gsbparse.domain.errors import XmlParsingError

logger = logging.getLogger(__name__)

_T = TypeVar("_T")

_NULL_SENTINEL = "(null)"

# Date formats tried in order when parsing dates.
# The spec says %m/%d/%Y but the example file uses %d/%m/%Y.
_DATE_FORMATS = ("%m/%d/%Y", "%d/%m/%Y")


def parse_null(fn: Callable[[str], _T]) -> Callable[[str], _T | None]:
    """Decorator: return ``None`` when the raw value is ``"(null)"``.

    Args:
        fn: The parser function to wrap.

    Returns:
        A wrapped function that returns ``None`` on the null sentinel.
    """

    @functools.wraps(fn)
    def wrapper(raw: str) -> _T | None:
        if raw == _NULL_SENTINEL:
            return None
        return fn(raw)

    return wrapper


def parse_optional(fn: Callable[[str], _T]) -> Callable[[str], _T | None]:
    """Decorator: return ``None`` when parsing raises :class:`XmlParsingError`.

    Use this on fields that may be absent or unparseable in some file versions.

    Args:
        fn: The parser function to wrap.

    Returns:
        A wrapped function that returns ``None`` on parse failure.
    """

    @functools.wraps(fn)
    def wrapper(raw: str) -> _T | None:
        try:
            return fn(raw)
        except XmlParsingError:
            return None

    return wrapper


def parse_str(raw: str) -> str:
    """Return the raw string unchanged.

    Args:
        raw: The raw XML attribute value.

    Returns:
        The string as-is.
    """
    return raw


@parse_null
def parse_nullable_str(raw: str) -> str | None:
    """Return ``None`` for ``"(null)"``, otherwise return the string.

    Args:
        raw: The raw XML attribute value.

    Returns:
        The string, or ``None`` for the null sentinel.
    """
    return raw


def parse_int(raw: str) -> int:
    """Parse a string as a base-10 integer.

    Args:
        raw: The raw XML attribute value.

    Returns:
        The parsed integer.

    Raises:
        XmlParsingError: If the value cannot be parsed as an integer.
    """
    try:
        return int(raw)
    except ValueError as err:
        raise XmlParsingError(f"Cannot parse {raw!r} as int") from err


def parse_bool(raw: str) -> bool:
    """Parse Grisbi's boolean encoding (``"0"`` / ``"1"``).

    Args:
        raw: The raw XML attribute value.

    Returns:
        ``False`` for ``"0"``, ``True`` for ``"1"``.

    Raises:
        XmlParsingError: If the value is not ``"0"`` or ``"1"``.
    """
    if raw == "0":
        return False
    if raw == "1":
        return True
    raise XmlParsingError(f"Cannot parse {raw!r} as bool: expected '0' or '1'")


def parse_amount(raw: str) -> Decimal:
    """Parse a Grisbi amount string (comma as decimal separator).

    Args:
        raw: The raw XML attribute value (e.g. ``"42,50"`` or ``"42.50"``).

    Returns:
        A :class:`~decimal.Decimal` with the parsed value.

    Raises:
        XmlParsingError: If the value cannot be parsed as a Decimal.
    """
    normalised = raw.replace(",", ".")
    try:
        return Decimal(normalised)
    except InvalidOperation as err:
        raise XmlParsingError(f"Cannot parse {raw!r} as Decimal amount") from err


def parse_date(raw: str) -> date:
    """Parse a Grisbi date string, trying multiple formats.

    Grisbi files have historically used both ``%m/%d/%Y`` and ``%d/%m/%Y``.
    Both formats are tried in order; the first successful parse wins.

    Args:
        raw: The raw XML attribute value (e.g. ``"01/15/2023"`` or
            ``"15/01/2023"``).

    Returns:
        A :class:`~datetime.date` with the parsed value.

    Raises:
        XmlParsingError: If the value cannot be parsed in any known format.
    """
    for fmt in _DATE_FORMATS:
        try:
            return date.fromisoformat(
                f"{raw.split('/')[2]}-{raw.split('/')[0]:>02}-{raw.split('/')[1]:>02}"
                if fmt == "%m/%d/%Y"
                else f"{raw.split('/')[2]}-{raw.split('/')[1]:>02}-{raw.split('/')[0]:>02}"
            )
        except (ValueError, IndexError):
            continue
    raise XmlParsingError(f"Cannot parse {raw!r} as date: tried {_DATE_FORMATS}")


def parse_list_int(raw: str, sep: str = ";") -> list[int]:
    """Parse a separator-delimited list of integers.

    Args:
        raw: The raw XML attribute value (e.g. ``"1;2;3"``).
        sep: The separator character (default ``";"``).

    Returns:
        A list of parsed integers.

    Raises:
        XmlParsingError: If any element cannot be parsed as an integer.
    """
    if not raw:
        return []
    try:
        return [int(part.strip()) for part in raw.split(sep)]
    except ValueError as err:
        raise XmlParsingError(f"Cannot parse {raw!r} as list[int] with sep={sep!r}") from err
