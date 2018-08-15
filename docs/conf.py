# Copyright 2018 PIQuIL - All Rights Reserved

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# ----------------------------------------------------------------------------

# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import inspect
import os
import shutil
import subprocess
import sys
from operator import attrgetter

sys.path.insert(0, os.path.abspath("../"))

# -- Project information -----------------------------------------------------

project = "QuCumber"
copyright = "2018, PIQuIL"
author = "PIQuIL"


init_file = {}
with open("../qucumber/__version__.py", "r") as f:
    # The short X.Y version
    exec(f.read(), init_file)
    version = init_file["__version__"]
    # The full version, including alpha/beta/rc tags
    release = version


print("Building version: " + version + "; release: " + release)

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.imgmath",
    "sphinx.ext.ifconfig",
    "sphinx.ext.linkcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "nbsphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# Things that nitpick mode should ignore.
nitpick_ignore = [
    ("py:class", "int"),
    ("py:class", "float"),
    ("py:class", "bool"),
    ("py:class", "dict"),
    ("py:class", "list"),
    ("py:class", "tuple"),
    ("py:class", "str"),
    ("py:class", "file"),
    ("py:obj", "None"),
    ("py:exc", "ValueError"),
    ("py:class", "callable"),
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {"canonical_url": "http://piquil.github.io/QuCumber/en/stable/"}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------


autodoc_member_order = "bysource"

# Output file base name for HTML help builder.
htmlhelp_basename = "QuCumberdoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    "preamble": (r"\usepackage{physics}" r"\DeclareMathOperator{\sgn}{sgn}"),
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "QuCumber.tex", "QuCumber Documentation", "PIQuIL", "manual")
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "qucumber", "QuCumber Documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "QuCumber",
        "QuCumber Documentation",
        author,
        "QuCumber",
        "One line description of project.",
        "Miscellaneous",
    )
]


# -- Extension configuration -------------------------------------------------

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for imgmath -----------------------------------------------------

imgmath_use_preview = True
imgmath_latex_preamble = latex_elements["preamble"]
imgmath_image_format = "svg"
imgmath_font_size = 13
imgmath_dvisvgm_args = ["--no-fonts", "-e"]


# -- Options for napoleon ----------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True

# -- Options for intersphinx -------------------------------------------------


intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "torch": ("https://pytorch.org/docs/stable/", None),
    "numpy": ("http://docs.scipy.org/doc/numpy", None),
}

# -- Options for linkcode extension ------------------------------------------


# adapted from scikit-learn's github_link.py
# https://github.com/scikit-learn/scikit-learn/blob/1870d6d/doc/sphinxext/github_link.py


def _get_git_revision():
    REVISION_CMD = "git rev-parse --short HEAD"
    try:
        revision = subprocess.check_output(REVISION_CMD.split()).strip()
    except (subprocess.CalledProcessError, OSError):
        print("Failed to execute git to get revision")
        return None
    return revision.decode("utf-8")


def linkcode_resolve(domain, info):
    revision = _get_git_revision()
    if revision is None:
        return None
    if domain not in ("py", "pyx"):
        return None
    if not info.get("module") or not info.get("fullname"):
        return None

    class_name = info["fullname"].split(".")[0]
    module = __import__(info["module"], fromlist=[class_name])
    obj = attrgetter(info["fullname"])(module)

    try:
        file_name = inspect.getsourcefile(obj)
    except Exception:
        file_name = None

    if not file_name:
        try:
            file_name = inspect.getsourcefile(sys.modules[obj.__module__])
        except Exception:
            file_name = None

    if not file_name:
        return None

    relpath_start = os.path.dirname(__import__("qucumber").__file__)
    file_name = os.path.relpath(file_name, start=relpath_start)

    try:
        line_number = inspect.getsourcelines(obj)[1]
    except Exception:
        line_number = ""

    return (
        "https://github.com/PIQuIL/QuCumber/blob"
        "/{revision}/qucumber/{file_name}#L{line_number}".format(
            revision=revision, file_name=file_name, line_number=line_number
        )
    )


# -- Options for nbsphinx ----------------------------------------------------


nbsphinx_execute = "never"

conf_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


print("Copy example notebooks into docs/_examples")


# adapted from:
# https://github.com/spatialaudio/nbsphinx/issues/170#issuecomment-373497587
def all_but_ipynb(directory, contents):
    return [
        c
        for c in contents
        if os.path.isfile(os.path.join(directory, c)) and (not c.endswith(".ipynb"))
    ]


shutil.rmtree(os.path.join(conf_location, "..", "docs/_examples"), ignore_errors=True)
shutil.copytree(
    os.path.join(conf_location, "..", "examples"),
    os.path.join(conf_location, "..", "docs/_examples"),
    ignore=all_but_ipynb,
)
