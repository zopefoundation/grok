# -*- coding: utf-8 -*-
"""
    sphinx.roles
    ~~~~~~~~~~~~

    Handlers for additional ReST roles.

    :copyright: 2007 by Georg Brandl.
    :license: Python license.
"""

import re

from docutils import nodes, utils
from docutils.parsers.rst import roles

import addnodes

ws_re = re.compile(r'\s+')

generic_docroles = {
    'command' : nodes.strong,
    'dfn' : nodes.emphasis,
    'guilabel' : nodes.strong,
    'kbd' : nodes.literal,
    'keyword' : nodes.literal,
    'mailheader' : addnodes.literal_emphasis,
    'makevar' : nodes.Text,
    'manpage' : addnodes.literal_emphasis,
    'mimetype' : addnodes.literal_emphasis,
    'newsgroup' : addnodes.literal_emphasis,
    'option' : addnodes.literal_emphasis,
    'program' : nodes.strong,
    'regexp' : nodes.literal,
}

for rolename, nodeclass in generic_docroles.iteritems():
    roles.register_generic_role(rolename, nodeclass)

# default is `literal`
innernodetypes = {
    'ref': nodes.emphasis,
    'term': nodes.emphasis,
    'token': nodes.strong,
}

def xfileref_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    if text[0:1] == '!':
        text = text[1:]
        return [innernodetypes.get(typ, nodes.literal)(
            rawtext, text, classes=['xref'])], []
    pnode = addnodes.pending_xref(rawtext)
    pnode['reftype'] = typ
    # if the first character is a dot, search more specific namespaces first
    # else search builtins first
    if text[0:1] == '.' and \
       typ in ('data', 'exc', 'func', 'class', 'const', 'attr', 'meth'):
        text = text[1:]
        pnode['refspecific'] = True
    pnode['reftarget'] = ws_re.sub((typ == 'term' and ' ' or ''), text)
    pnode += innernodetypes.get(typ, nodes.literal)(rawtext, text,
                                                    classes=['xref'])
    return [pnode], []


_litvar_re = re.compile('{([^}]+)}')

def emph_literal_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    retnodes = []
    pos = 0
    for m in _litvar_re.finditer(text):
        if m.start() > pos:
            txt = text[pos:m.start()]
            retnodes.append(nodes.literal(txt, txt))
        retnodes.append(nodes.emphasis('', '', nodes.literal(m.group(1), m.group(1))))
        pos = m.end()
    if pos < len(text):
        retnodes.append(nodes.literal(text[pos:], text[pos:]))
    return retnodes, []


specific_docroles = {
    'data': xfileref_role,
    'exc': xfileref_role,
    'func': xfileref_role,
    'class': xfileref_role,
    'const': xfileref_role,
    'attr': xfileref_role,
    'meth': xfileref_role,

    'cfunc' : xfileref_role,
    'cdata' : xfileref_role,
    'ctype' : xfileref_role,
    'cmacro' : xfileref_role,

    'mod' : xfileref_role,

    'ref': xfileref_role,
    'token' : xfileref_role,
    'term': xfileref_role,

    'file' : emph_literal_role,
    'samp' : emph_literal_role,
}

for rolename, func in specific_docroles.iteritems():
    roles.register_canonical_role(rolename, func)
