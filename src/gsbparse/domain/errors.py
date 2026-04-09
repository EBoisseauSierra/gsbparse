"""Typed exception hierarchy for gsbparse.

Every exception raised by the library subclasses :class:`GsbParseError` so
callers can catch all library errors with a single ``except GsbParseError``.
"""


class GsbParseError(Exception):
    """Base class for every exception raised by gsbparse."""


class InvalidGsbFileError(GsbParseError):
    """The file could not be parsed as XML or the structure is invalid."""


class InvalidGsbFileRootError(InvalidGsbFileError):
    """The XML root element is not ``<Grisbi>``."""


class SectionNotFoundError(GsbParseError):
    """A mandatory section is missing from the file."""


class InvalidElementCountError(GsbParseError):
    """A section's cardinality is violated (e.g. multiple ``<General>`` elements)."""


class XmlParsingError(GsbParseError):
    """An attribute value could not be parsed as its expected type."""


class UnknownDetailedTransactionPathError(GsbParseError):
    """A ``DetailedTransactionColumn.path`` references a non-existent attribute."""


class MixedSectionsError(GsbParseError, TypeError):
    """``to_df`` was called with a list containing more than one concrete section type.

    Multiple-inherits from :class:`TypeError` so generic handlers that catch
    ``TypeError`` still catch it.  The ``found_types`` attribute exposes the
    concrete types discovered in the list for programmatic introspection.
    """

    def __init__(self, found_types: list[type]) -> None:
        self.found_types = found_types
        type_names = ", ".join(t.__name__ for t in found_types)
        super().__init__(
            f"to_df expected a homogeneous list of one section type, "
            f"but found multiple: {type_names}. Call to_df separately "
            f"for each section type."
        )
