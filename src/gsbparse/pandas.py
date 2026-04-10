"""Public re-export shim: ``from gsbparse.pandas import to_df``.

This module exists so that users write ``from gsbparse.pandas import to_df``
and the adapter identity stays visible in the import line.  Future adapters
will follow the same pattern::

    from gsbparse.polars import to_df   # polars (future)
    from gsbparse.arrow  import to_table  # arrow (future)

Swapping the output format is then a one-line change on the caller side.
"""

from gsbparse.adapters.pandas import to_df

__all__ = ["to_df"]
