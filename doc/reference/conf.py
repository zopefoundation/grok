# -*- coding: utf-8 -*-
#
# Grok Reference documentation build configuration file, created by
# sphinx-quickstart.py on Wed Feb 20 02:11:17 2008.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).
#
# All configuration values have a default value; values that are commented out
# show the default value as assigned to them.

import sys

#import os
from os import path, curdir
import re


version = 'Unknown'
setupfilepath = path.join(path.dirname(
    path.dirname(path.abspath(curdir))), 'setup.py')
reg = re.compile("^\s*version=.(.+).,.*")
for line in open(setupfilepath, 'r').read().split():
    m = reg.match(line)
    if m:
        version = m.groups()[0]




# If your extensions are in another directory, add it here.
#sys.path.append('some/directory')

# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.addons.*') or your custom ones.
#extensions = []

# Add any paths that contain templates here, relative to this directory.
#templates_path = []

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'contents'

# General substitutions.
project = 'Grok Reference'
copyright = '2006-2008, The Zope Foundation'

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
#
# The short X.Y version.
version = version
# The full version, including alpha/beta/rc tags.
release = version

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True


# Options for HTML output
# -----------------------

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# Content template for the index page, filename relative to this file.
#html_index = ''

# Custom sidebar templates, maps page names to filenames relative to this file.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# filenames relative to this file.
#html_additional_pages = {}

# If true, the reST sources are included in the HTML build as _sources/<name>.
#html_copy_source = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'Grok Referencedoc'

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
html_style = 'default.css'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = [path.join(path.abspath(curdir), '.static')]


# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
#latex_documents = []
latex_documents = [
    ('reference.tex', 'Grok Reference', 'The Grok Team', 'manual')
    ]

# Additional stuff for the LaTeX preamble.
#latex_preamble = '

# Documents to append as an appendix to all manuals.
#latex_appendices = []
