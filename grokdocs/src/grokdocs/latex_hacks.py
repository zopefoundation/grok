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
"""LaTeX hacks for sphinx problems.

The sphinx latextranslator currently lacks a few features that are
part of stock ``docutils`` translators. Some of the monkey patches in
here were already applied to the stock sphinx package, but some are
still missing. Therefore we 'inject' those changes here.
"""

from docutils import nodes
from sphinx.writers.latex import LaTeXTranslator

# Inject a working pygments workaround.
def depart_literal_block(self, node):
    hlcode = self.highlighter.highlight_block(self.verbatim.rstrip(
        '\n'), self.highlightlang)
    # workaround for Unicode issue
    hlcode = hlcode.replace(u'€', u'@texteuro[]')
    # workaround for Pygments bug
    hlcode = hlcode.replace('\\end{Verbatim}',
                            '\n\\end{Verbatim}')
    self.body.append('\n' + hlcode)
    self.verbatim = None
LaTeXTranslator.depart_literal_block = depart_literal_block
LaTeXTranslator.depart_doctest_block = depart_literal_block

# Inject a topic handler that frames sidebars and topics with a
# shadowbox instead of the normal fbox.
def visit_topic(self, node):
    self.body.append('\\setbox0\\vbox{\n'
                     '\\begin{minipage}{0.75\\textwidth}\n')
def depart_topic(self, node):
    self.body.append('\\end{minipage}}\n'
                     '\\begin{center}\\setlength{\\fboxsep}{5pt}'
                     '\\shadowbox{\\box0}\\end{center}\n')
LaTeXTranslator.visit_topic = visit_topic
LaTeXTranslator.depart_topic = depart_topic
LaTeXTranslator.visit_sidebar = visit_topic
LaTeXTranslator.depart_sidebar = depart_topic

def visit_image(self, node):
    attrs = node.attributes
    # Add image URI to dependency list, assuming that it's
    # referring to a local file.
    #self.settings.record_dependencies.add(attrs['uri'])
    pre = []                        # in reverse order
    post = []
    include_graphics_options = ""
    inline = isinstance(node.parent, nodes.TextElement)
    if attrs.has_key('scale'):
        # Could also be done with ``scale`` option to
        # ``\includegraphics``; doing it this way for consistency.
        pre.append('\\scalebox{%f}{' % (attrs['scale'] / 100.0,))
        post.append('}')
    if attrs.has_key('width'):
        include_graphics_options = '[width=%s]' % attrs['width']
    if attrs.has_key('align'):
        align_prepost = {
            # By default latex aligns the top of an image.
            (1, 'top'): ('', ''),
            (1, 'middle'): ('\\raisebox{-0.5\\height}{', '}'),
            (1, 'bottom'): ('\\raisebox{-\\height}{', '}'),
            (0, 'center'): ('{\\hfill', '\\hfill}'),
            # These 2 don't exactly do the right thing.
            # The image should be floated alongside the
            # paragraph.  See
            # http://www.w3.org/TR/html4/struct/objects.html#adef-align-IMG
            (0, 'left'): ('{', '\\hfill}'),
            (0, 'right'): ('{\\hfill', '}'),}
        try:
            pre.append(align_prepost[inline, attrs['align']][0])
            post.append(align_prepost[inline, attrs['align']][1])
        except KeyError:
            pass                    # XXX complain here?
    if not inline:
        pre.append('\n')
        post.append('\n')
        pre.reverse()
        self.body.extend( pre )
        self.body.append( '\\includegraphics%s{%s}' % (
            include_graphics_options, attrs['uri'] ) )
        self.body.extend( post )

def depart_image(self, node):
    pass

LaTeXTranslator.visit_image = visit_image
LaTeXTranslator.depart_image = depart_image

