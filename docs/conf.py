# -*- coding: utf-8 -*-
#
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
# sys.path.insert(0, os.path.abspath('..'))
import os
import sys
import sphinx_rtd_theme
from sphinx.ext.autodoc.mock import mock
from sphinx.ext.autodoc import between, ClassDocumenter, AttributeDocumenter
from sphinx.util import inspect
from builtins import str
from enum import Enum
import re
import subprocess

# -- Project information -----------------------------------------------------

project = u'NVIDIA DALI'
copyright = u'2018-2021, NVIDIA Corporation'
author = u'NVIDIA Corporation'

version_long = u'0.0.0'
with open("../VERSION") as f:
    version_long = f.readline()

version_short = re.match('^[\d]+\.[\d]+', version_long).group(0)

git_sha = os.getenv("GIT_SHA")

if not git_sha:
    try:
        git_sha = subprocess.check_output(["git", "log", "--pretty=format:'%h'", "-n1"]).decode('ascii').replace("'","").strip()
    except:
        git_sha = u'0000000'

git_sha = git_sha[:7] if len(git_sha) > 7 else git_sha

version = str(version_long + u"-" + git_sha)
# The full version, including alpha/beta/rc tags
release = str(version_long)

# generate table of supported operators and their devices
# mock torch required by supported_op_devices
with mock(["torch", "numba"]):
    sys.path.insert(0, os.path.abspath('./'))
    import operations_table
    operations_table.operations_table("fn_table")
    operations_table.fn_to_op_table("fn_to_op_table")

    import autodoc_submodules
    autodoc_submodules.op_autodoc("op_autodoc")
    autodoc_submodules.fn_autodoc("fn_autodoc")

# Uncomment to keep warnings in the output. Useful for verbose build and output debugging.
# keep_warnings = True

# hack: version is used for html creation, so put the version picker
# link here as well:
option_on = " selected"
option_off = ""
if "dev" in version_long:
    release_opt = option_off
    main_opt = option_on
    option_nr = 1
else:
    release_opt = option_on
    main_opt = option_off
    option_nr = 0
version = version + """<br/>
Version select: <select onChange="window.location.href = this.value" onFocus="this.selectedIndex = {0}">
    <option value="https://docs.nvidia.com/deeplearning/dali/user-guide/docs/index.html"{1}>Current release</option>
    <option value="https://docs.nvidia.com/deeplearning/dali/master-user-guide/docs/index.html"{2}>master (unstable)</option>
    <option value="https://docs.nvidia.com/deeplearning/dali/archives/index.html">Older releases</option>
</select>""".format(option_nr, release_opt, main_opt)

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.ifconfig',
    'sphinx.ext.extlinks',
    'IPython.sphinxext.ipython_console_highlighting',
    'nbsphinx',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The main toctree document.
main_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = [u'_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Mock some of the dependencies for building docs. tf-plugin doc check tf version before loading,
# so we do not mock tensorflow so we do not need to extend the logic there.
autodoc_mock_imports = ['paddle', 'torch', 'torchvision']

# -- Options for Napoleon ----------------------------------------------------

napoleon_custom_sections = ['Supported backends']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'canonical_url': 'https://docs.nvidia.com/deeplearning/dali/user-guide/docs/index.html',
    'collapse_navigation': False,
    'display_version': True,
    'logo_only': False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# We remove the `_static` as we do not use it
html_static_path = []

# Download favicon and set it (the variable `html_favicon`) for this project.
# It must be relative path.
favicon_rel_path = "nvidia.ico"
subprocess.call(["wget", "-O", favicon_rel_path, "https://docs.nvidia.com/images/nvidia.ico"])
html_favicon = favicon_rel_path

subprocess.call(["wget", "-O", "dali.png", "https://raw.githubusercontent.com/NVIDIA/DALI/master/dali.png"])

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

# Output file base name for HTML help builder.
htmlhelp_basename = 'NVIDIADALIdoc'


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
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (main_doc, 'NVIDIADALI.tex', u'NVIDIA DALI Documentation',
     u'NVIDIA Corporation', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (main_doc, 'nvidiadali', u'NVIDIA DALI Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (main_doc, 'NVIDIADALI', u'NVIDIA DALI Documentation',
     author, 'NVIDIADALI', 'One line description of project.',
     'Miscellaneous'),
]


# -- Extension configuration -------------------------------------------------
extlinks = {'issue': ('https://github.com/NVIDIA/DALI/issues/%s',
                      'issue '),
            'fileref': ('https://github.com/NVIDIA/DALI/tree/' + (git_sha if git_sha != u'0000000' else "master") + '/%s', ''),}


from typing import (
    Any, Callable, Dict, Iterator, List, Optional, Sequence, Set, Tuple, Type, TypeVar, Union
)
from typing import get_type_hints


_dali_enums = ["DALIDataType", "DALIIterpType", "DALIImageType", "PipelineAPIType"]

class EnumDocumenter(ClassDocumenter):
    # Register as .. autoenum::
    objtype = 'enum'
    # Produce .. py:class:: fields in the RST doc
    directivetype = 'class'

    def __init__(self, *args):
        super().__init__(*args)

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        """Verify that we handle only the registered DALI enums. Pybind doesn't subclass Enum class,
        so we need an explicit list.
        """
        return membername in _dali_enums and isinstance(parent, ClassDocumenter)

    def filter_members(self, members, want_all):
        """After self.get_object_members() obtained all members, this function filters only
        the ones we're interested in.
        We can do the sorting here based on the values, and pass through in self.sort_members()
        """
        # Since pybind11 https://github.com/pybind/pybind11/pull/2739 there is an extra `value` member
        # returned by get_object_members(). Here we are filtering the list, to keep only enum members
        filtered = [member for member in members if member[0] in self.object.__members__.keys()]

        filtered = super().filter_members(filtered, want_all)

        # sort by the actual value of enum - this is a tuple of (name, value, boolean)
        def get_member_value(member_desc):
            _, member_value, _ = member_desc
            if isinstance(member_value, Enum):
                return member_value.value
            else:
                return int(member_value)
        filtered.sort(key = get_member_value)

        return filtered

    def sort_members(self, documenters, order):
        """Ignore the order. Here we have access only to documenters that carry the name
        and not the object. We need to sort based on the enum values and we do it in
        self.filter_members()
        """
        return documenters

class EnumAttributeDocumenter(AttributeDocumenter):
    # Give us higher priority over Sphinx native AttributeDocumenter which is 10, or 11 in case
    # of more specialized attributes.
    priority = 12

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        """Run only for the Enums supported by DALI
        """
        return isinstance(parent, EnumDocumenter)

    def add_directive_header(self, sig):
        """Greatly simplified AttributeDocumenter.add_directive_header()
        as we know we're dealing with only specific enums here, we can append a line of doc
        with just their value.
        """
        super(AttributeDocumenter, self).add_directive_header(sig)


def setup(app):
    count_unique_visitor_script = os.getenv("ADD_NVIDIA_VISITS_COUNTING_SCRIPT")
    if count_unique_visitor_script:
        app.add_js_file(count_unique_visitor_script)
    # Register a sphinx.ext.autodoc.between listener to ignore everything
    # between lines that contain the word <SPHINX_IGNORE>
    app.connect('autodoc-process-docstring', between('^.*<SPHINX_IGNORE>.*$', exclude=True))
    app.add_autodocumenter(EnumDocumenter)
    app.add_autodocumenter(EnumAttributeDocumenter)
    return app
