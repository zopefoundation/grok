# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Builds HTML and Latex versions of the Official Grok Documentation using Sphinx.
"""
import sys
import os.path
from shutil import copyfile
import getopt
from docutils import nodes
from docutils.parsers.rst import directives
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import LatexFormatter
import sphinx
from sphinx.util.console import nocolor
import latex_hacks

ROOT = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', '..', '..') 
SRCDIR_ALL = os.path.join(ROOT, 'doc')
SRCDIR_REF = os.path.join(SRCDIR_ALL, 'reference')

BUILD_DIR = os.path.join(ROOT, 'build')

HTMLDIR_ALL = os.path.join(BUILD_DIR, 'html')
HTMLDIR_REF = os.path.join(BUILD_DIR, 'html', 'reference')

LATEX_ALL = os.path.join(BUILD_DIR, 'latex')

LATEX_SETTINGS = {
    'DEFAULT': LatexFormatter(),
    'VARIANTS' : {
       'linenos' : LatexFormatter(linenos=True),
       'nolinenos' : LatexFormatter(linenos=False)
       },
    'FORMAT': 'latex',
    }

for build_path in (BUILD_DIR, HTMLDIR_ALL, HTMLDIR_REF, LATEX_ALL):
    # Create the output directories, if they do not exist...
    if not os.path.exists(build_path):
        os.makedirs(build_path)


def pygments_latex_directive(name, arguments, options, content, lineno,
                             content_offset, block_text, state, state_machine):
    """A docutils directive that provides syntax highlighting for LaTeX.

    This is needed to circumvent highlighting quirks when doing
    non-HTML output. The pygments_directive delivers plain HTML, which
    we must avoid when generating LaTeX for example.
    """
    try:
        lexer = get_lexer_by_name(arguments[0])
    except ValueError:
        # no lexer found - use the text one instead of an exception
        lexer = TextLexer()
    # take an arbitrary option if more than one is given
    formatter = options and LATEX_SETTINGS['VARIANTS'][
        options.keys()[0]] or LATEX_SETTINGS['DEFAULT']
    parsed = highlight(u'\n'.join(content), lexer, formatter)
    return [nodes.raw('', parsed, format=LATEX_SETTINGS['FORMAT'])]

pygments_latex_directive.arguments = (1, 0, 1)
pygments_latex_directive.content = 1



def usage(argv, msg=None, default_src=None, default_out=None):
    """Some hints for users.

    Adapted from sphinx __init__. Because we add an `-h` option and
    provide a slightliy different syntax than stock sphinx (srcdir and
    targetdir have defaults here), we also need our own help texts.
    """

    if msg:
        print >>sys.stderr, msg
        print >>sys.stderr
    print >>sys.stderr, """\
usage: %s [options] [sourcedir [outdir [filenames...]]]
options: -b <builder> -- builder to use; default is html
         -a        -- write all files; default is to only write new and changed files
         -E        -- don't use a saved environment, always read all files
         -d <path> -- path for the cached environment and doctree files
                      (default outdir/.doctrees)
         -D <setting=value> -- override a setting in sourcedir/conf.py
         -N        -- do not do colored output
         -q        -- no output on stdout, just warnings on stderr
         -P        -- run Pdb on exception
         -h        -- print this help

default sourcedir is %s
default outputdir is %s

modi:
* without -a and without filenames, write new and changed files.
* with -a, write all files.
* with filenames, write these.""" % (argv[0],default_src, default_out)

def usage_grokdoc(argv, msg=None):
    """Wrapper that displays source and target of all docs.
    """
    return usage(argv, msg=msg, default_src=SRCDIR_ALL,
                 default_out=HTMLDIR_ALL)

def usage_grokref(argv, msg=None):
    """Wrapper that displays source and target of reference docs.
    """
    return usage(argv, msg=msg, default_src=SRCDIR_REF,
                 default_out=HTMLDIR_REF)


def render(argv=sys.argv, srcdir=SRCDIR_ALL, htmldir=HTMLDIR_ALL,
             latexdir=LATEX_ALL, do_latex=False):
    """Generate the whole docs, including howtos, reference, etc.
    """
    if srcdir == SRCDIR_ALL:
        sphinx.usage = usage_grokdoc
    if not sys.stdout.isatty() or sys.platform == 'win32':
        # Windows' poor cmd box doesn't understand ANSI sequences
        nocolor()
    opts, args = None, None
    try:
        opts, args = getopt.getopt(argv[1:], 'ab:d:D:NEqPh')
    except getopt.error:
        # sphinx will handle that errors
        pass
    if len(args) < 1:
        argv.append(srcdir)
    if len(args) < 2:
        argv.append(htmldir)

    if opts and '-h' in [x for x,y in opts]:
        sphinx.usage(argv, msg=None)
        return 1

    format = 'html'
    if do_latex:
        format = 'latex'
    if opts and '-b' in [x for x,y in opts]:
        val = filter(lambda x: x[0] == '-b', opts)
        format = val[-1][1]

    if format == 'latex':
        # disable code-block directive by substituting it with a
        # LaTeX-specialized version...
        directives.register_directive('sourcecode', pygments_latex_directive)
        directives.register_directive('code-block', pygments_latex_directive)

        # Set default sourcedir...
        if len(args) < 2:
            argv[-1] = latexdir
        # Copy fncychap.sty to targetdir...
        if os.path.isdir(argv[-1]):
            copyfile(os.path.join(os.path.dirname(__file__),
                                  'texinputs', 'fncychap.sty'),
                     os.path.join(argv[-1], 'fncychap.sty'))
        # Let sphinx know, we want LaTeX...
        argv.insert(1, ('latex'))
        argv.insert(1, ('-b'))
            
    args = argv                 

    print "Source directory is: ", argv[-2]
    print "Target directory is: ", argv[-1]
    print "(run `%s -h` to see the options available)" % argv[0]

    sphinx.main(argv)

    print "Generated docs are in %s." % os.path.abspath(argv[-1])

def render_latex(argv=sys.argv):
    """Generate all docs in LaTeX.
    """
    return render(argv, do_latex=True)

def grokref(argv=sys.argv, do_latex=False):
    """Generate the reference docs.
    """
    sphinx.usage = usage_grokref
    return render(argv, srcdir=SRCDIR_REF, htmldir=HTMLDIR_REF,
                    latexdir=LATEX_ALL, do_latex=do_latex)

def grokref_latex(argv=sys.argv):
    """Generate reference in LaTeX format.
    """
    return render(argv, do_latex=True)

