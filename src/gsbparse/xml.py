"""Public re-export shim: ``from gsbparse.xml import read_gsb_file``.

Exposes the XML adapter's reader function at the ``gsbparse.xml`` path.
Most callers should use :func:`gsbparse.read_gsb` instead; this module
is provided for completeness and for callers who prefer the explicit
adapter import style.
"""

from gsbparse.adapters.xml.reader import read_gsb_file

__all__ = ["read_gsb_file"]
