##############################################################################
#
# Copyright (c) 2006-2007 Zope Corporation and Contributors.
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
"""Grok ZCML directives."""

from zope.interface import Interface
from zope.configuration.fields import GlobalObject
from zope.configuration.config import ConfigurationMachine

import martian
from martian import scan
from martian.error import GrokError

class IGrokDirective(Interface):
    """Grok a package or module."""

    package = GlobalObject(
        title=u"Package",
        description=u"The package or module to be analyzed by grok.",
        required=False,
        )

# add a cleanup hook so that grok will bootstrap itself again whenever
# the Component Architecture is torn down.
def resetBootstrap():
    # we need to make sure that the grokker registry is clean again
    the_module_grokker.clear()
from zope.testing.cleanup import addCleanUp
addCleanUp(resetBootstrap)

the_multi_grokker = martian.MetaMultiGrokker()
the_module_grokker = martian.ModuleGrokker(the_multi_grokker)

def skip_tests(name):
    return name in ['tests', 'ftests']

def grokDirective(_context, package):
    do_grok(package.__name__, _context)

def do_grok(dotted_name, config):
    martian.grok_dotted_name(
        dotted_name, the_module_grokker, exclude_filter=skip_tests,
        config=config
        )
