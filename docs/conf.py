# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import importlib.metadata

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
