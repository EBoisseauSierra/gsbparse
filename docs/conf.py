# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import importlib.metadata
from pathlib import Path

# -- Project information -----------------------------------------------------

project = "gsbparse"
author = "Étienne Boisseau-Sierra"
copyright = f"2024, {author}"
release = importlib.metadata.version("gsbparse")
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "design"]

# MyST-Parser settings
myst_enable_extensions = ["colon_fence"]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"

# -- autodoc settings --------------------------------------------------------

autodoc_member_order = "bysource"
autodoc_typehints = "description"
always_document_param_types = True

# -- doctest settings --------------------------------------------------------

_SIMPLE_EXAMPLE = Path(__file__).parent.parent / "tests" / "assets" / "simple_example.gsb"

doctest_global_setup = f"""
import datetime
from decimal import Decimal
import gsbparse
from gsbparse.pandas import to_df
from gsbparse import DetailedTransactionColumn

gsb = gsbparse.read_gsb(r"{_SIMPLE_EXAMPLE}")
"""
