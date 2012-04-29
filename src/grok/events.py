##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
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
"""Events for Grok application components.

The events described here are *not* trigged by Grok itself. They are
conveniently provided to be used in your own application.

"""
import grok
import grokcore.site.interfaces
from zope.interface import implements


class ApplicationInitializedEvent(object):
    """A Grok Application has been created and is now ready to be used.
    """
    implements(grok.IApplicationInitializedEvent)

    def __init__(self, app):
        assert grok.IApplication.providedBy(app)
        self.object = app
