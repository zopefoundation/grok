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
"""Grok security-related stuff
"""

class GrokChecker(object):
    # ME GROK ANGRY.
    # ME GROK NOT KNOW WHY CHECKER.

    # We have no idea why we need a custom checker here. One hint was
    # that the DirectoryResource already does something manually with
    # setting up the 'correct' checker for itself and we seem to interfere
    # with that. However, we couldn't figure out what's going on and this
    # solves our problem for now. 

    # XXX re-implement this in a sane way.

    def __init__(self):
        pass

    def check_getattr(self, object, name):
        pass

    def check_setattr(self, ob, name):
        pass

    def check(self, ob, operation):
        pass

    def proxy(self, value):
        return value



