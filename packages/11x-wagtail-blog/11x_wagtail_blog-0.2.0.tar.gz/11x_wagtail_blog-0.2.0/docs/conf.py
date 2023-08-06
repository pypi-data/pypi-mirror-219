# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- System set up -----------------------------------------------------
import os
from pathlib import Path
import sys

import django

_docs_root = Path(__file__).parent

sys.path.insert(0, str(_docs_root.parent))
sys.path.insert(0, str(_docs_root.parent / "testapp"))

os.environ["DJANGO_SETTINGS_MODULE"] = "conf.settings.tests"
django.setup()

autodoc_class_signature = "separated"
autodoc_typehints = "none"
autodoc_member_order = "bysource"
autodoc_default_options = {
    "no-value": True,
    "member-order": "bysource",
}
# ---------------------------------------------------------------------------------------- #
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
# ---------------------------------------------------------------------------------------- #
project = '11x Wagtail Blog'
copyright = '2023, The Magnificant Nick'
author = 'The Magnificant Nick'


# ---------------------------------------------------------------------------------------- #
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# ---------------------------------------------------------------------------------------- #
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# ---------------------------------------------------------------------------------------- #
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# ---------------------------------------------------------------------------------------- #
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
