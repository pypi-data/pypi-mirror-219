# Configuration file for the Sphinx api_reference builder.
#
# This file only contains a selection of the most common options. For a full
# list see the api_reference:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# api_reference root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath(r'../..'))

autodoc_mock_imports = ['xarray', 'netCDF4', 'tqdm', 'scipy']

# -- Project information -----------------------------------------------------

project = 'tfv'
copyright = '2023 BMT'
author = 'TUFLOW'

# The full version, including alpha/beta/rc tags
release = '1.0.5'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = \
    [
        'sphinx.ext.intersphinx',
        'sphinx.ext.autodoc',
        'sphinx.ext.napoleon',
        # 'myst_parser',
        'myst_nb',
    ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source file names.
source_suffix = ['.rst', '.md']

# The master toc tree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the api_reference for
# a list of builtin themes.

# html_theme = 'alabaster'
# html_theme = "sphinx_rtd_theme"

# html_theme_path = [sphinx_readable_theme.get_html_theme_path()]
# html_theme = 'readable'

html_theme = 'piccolo_theme'  # or piccolo_theme

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']


# Switch off the making of docs when building
jupyter_execute_notebooks = "off"