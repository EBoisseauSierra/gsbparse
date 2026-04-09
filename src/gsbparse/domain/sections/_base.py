"""Base class for all Grisbi file section dataclasses."""

import abc
from dataclasses import dataclass


@dataclass(frozen=True)
class GsbFileSection(abc.ABC):
    """Marker base for every Grisbi section dataclass.

    All concrete section classes are frozen dataclasses that inherit from this
    base.  The base carries no fields; it exists solely as a common type for
    ``isinstance`` checks, :class:`~gsbparse.domain.file.GsbFile` field
    annotations, and the pandas adapter's dispatch logic.

    Domain purity: this class imports nothing outside the stdlib.  Parser
    logic, XML imports, and ``from_xml`` classmethods do NOT belong here —
    they live in ``adapters/xml/sections/``.
    """
