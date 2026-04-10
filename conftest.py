import datetime
from decimal import Decimal
from pathlib import Path

import pytest

import gsbparse
import gsbparse.pandas as gsbpd
from gsbparse import DetailedTransactionColumn

_SIMPLE_EXAMPLE = Path(__file__).parent / "tests" / "assets" / "simple_example.gsb"


@pytest.fixture(autouse=True)
def doctest_namespace(doctest_namespace: dict) -> dict:  # type: ignore[type-arg]
    """Populate the doctest namespace for README and docs examples."""
    doctest_namespace["gsb"] = gsbparse.read_gsb(_SIMPLE_EXAMPLE)
    doctest_namespace["gsbpd"] = gsbpd
    doctest_namespace["DetailedTransactionColumn"] = DetailedTransactionColumn
    doctest_namespace["datetime"] = datetime
    doctest_namespace["Decimal"] = Decimal
    return doctest_namespace
