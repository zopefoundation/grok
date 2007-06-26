##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""Grok ZCML-Directives
"""
from zope import interface
import zope.configuration.fields
import grok

class IGrokDirective(interface.Interface):
    """Grok a package or module.
    """

    package = zope.configuration.fields.GlobalObject(
        title=u"Package",
        description=u"The package or module to be analyzed by grok.",
        required=False,
        )

def grokDirective(_context, package):
    grok.grok(package.__name__)
